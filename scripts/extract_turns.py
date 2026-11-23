#!/usr/bin/env python3
"""Collects the person's messages from Claude Code / Codex logs or a claude.ai export
into one markdown file for the judgment audit. Read-only. Writes one --out file (or stdout).
Flag patterns cover English and Russian.

  python3 extract_turns.py --days 28 --out /tmp/turns.md
  python3 extract_turns.py --since 2026-10-01 --project my-repo --sample 25
  python3 extract_turns.py --export ~/Downloads/data.zip --days 60
"""
import argparse, glob, json, os, random, re, sys, zipfile
from datetime import datetime, timedelta, timezone

DEFAULT_ROOTS = ["~/.claude/projects", "~/.codex/sessions"]

# Flags are hints on where to read closely. Not findings.
FLAGS = {
    "choice-delegated": re.compile(
        r"(выбери (сам|сама)|реши (сам|сама)|что посоветуешь|на твой (вкус|выбор)|какой (лучше|выбрать)|"
        r"you (decide|choose|pick)|your call|whatever you think|which (one )?is better|up to you)", re.I),
    "no-criterion": re.compile(
        r"(сделай (хорошо|красиво|лучше|нормально)|улучши|доработай|как (считаешь|думаешь) лучше|"
        r"make it (better|good|nice)|\bimprove\b|polish it)", re.I),
    "ready-answer": re.compile(
        r"(просто скажи|дай ответ|коротко,? без|без ссылок|какой лучший|что (это )?значит|"
        r"just tell me|short answer|no sources|what'?s the best)", re.I),
    "correction": re.compile(
        r"(^|\s)(нет[,.!\s]|не так|не то\b|переделай|перепиши|я же (говорила|просила|писала)|опять|снова|"
        r"убери|неправильно|зачем ты|no[,.!]|nope|not what i|redo|try again|i (said|asked|told you)|that'?s wrong)", re.I),
    "evaluation": re.compile(
        r"(не люблю|так не пиш|всегда|никогда|слишком|мне важно|у нас (принято|так)|не моё|не мое|"
        r"звучит как|терпеть не могу|i (hate|prefer|always|never)|too (long|formal|generic)|sounds like)", re.I),
}
ACCEPT = re.compile(
    r"^\s*(ок|окей|ok|okay|супер|отлично|класс|го|давай( дальше)?|да|норм|кайф|принято|топ|"
    r"great|perfect|nice|cool|lgtm|ship it|next|sounds good|go ahead|yes|yep|sure)\s*[!.)]*\s*$", re.I)
NOISE = ("<environment_context", "<user_instructions", "<command-", "<local-command",
         "<system-reminder", "Caveat:", "[Request interrupted")


def text_of(c):
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return "\n".join(b.get("text", "") for b in c
                         if isinstance(b, dict) and b.get("type") in ("text", "input_text", "output_text"))
    return ""


def is_tool_result(c):
    return isinstance(c, list) and c and all(
        isinstance(b, dict) and b.get("type") in ("tool_result", "function_call_output") for b in c)


def parse_ts(s):
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00")) if s else None
    except ValueError:
        return None


def clean(turns):
    return [t for t in turns if t["text"].strip() and not t["text"].lstrip().startswith(NOISE)]


def read_session(path):
    turns, fallback = [], []
    meta = {"path": os.path.basename(path), "cwd": None, "source": "claude-code"}
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                try:
                    o = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not isinstance(o, dict):
                    continue
                ts = parse_ts(o.get("timestamp"))
                p = o.get("payload") if isinstance(o.get("payload"), dict) else {}
                meta["cwd"] = meta["cwd"] or o.get("cwd") or p.get("cwd")
                if o.get("type") in ("user", "assistant") and isinstance(o.get("message"), dict):
                    if o.get("isMeta") or o.get("isSidechain"):
                        continue
                    c = o["message"].get("content")
                    if not is_tool_result(c):
                        turns.append({"role": o["type"], "text": text_of(c), "ts": ts})
                    continue
                if o.get("type") in ("session_meta", "response_item", "event_msg", "turn_context"):
                    meta["source"] = "codex"
                if o.get("type") == "response_item" and p.get("type") == "message":
                    turns.append({"role": p.get("role"), "text": text_of(p.get("content")), "ts": ts})
                elif o.get("type") == "event_msg" and p.get("type") == "user_message":
                    fallback.append({"role": "user", "text": p.get("message", ""), "ts": ts})
                elif o.get("type") == "message" and o.get("role") in ("user", "assistant"):
                    meta["source"] = "codex"
                    turns.append({"role": o["role"], "text": text_of(o.get("content")), "ts": ts})
    except OSError as e:
        print(f"skip {path}: {e}", file=sys.stderr)
    if not any(t["role"] == "user" for t in turns):
        turns += fallback
    return meta, clean(turns)


def read_export(path):
    """claude.ai export: conversations.json or a zip containing it."""
    try:
        if zipfile.is_zipfile(path):
            with zipfile.ZipFile(path) as z:
                name = next((n for n in z.namelist() if n.endswith("conversations.json")), None)
                if not name:
                    print(f"{path}: no conversations.json in the archive", file=sys.stderr)
                    return []
                data = json.loads(z.read(name).decode("utf-8", errors="replace"))
        else:
            with open(path, encoding="utf-8", errors="replace") as f:
                data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"skip {path}: {e}", file=sys.stderr)
        return []
    out = []
    for conv in data if isinstance(data, list) else []:
        if not isinstance(conv, dict):
            continue
        meta = {"path": conv.get("name") or conv.get("uuid") or "untitled", "cwd": "claude.ai",
                "source": "claude.ai"}
        turns = []
        for m in conv.get("chat_messages") or []:
            role = {"human": "user", "assistant": "assistant"}.get(m.get("sender"))
            if role:
                turns.append({"role": role, "text": m.get("text") or text_of(m.get("content")) or "",
                              "ts": parse_ts(m.get("created_at"))})
        out.append((meta, clean(turns)))
    return out


def flag_turns(turns):
    prev, out = "", []
    for t in turns:
        if t["role"] != "user":
            prev = t["text"]
            continue
        head = t["text"][:500]
        flags = [n for n, rx in FLAGS.items() if rx.search(head)]
        if prev and len(prev) > 400 and ACCEPT.match(t["text"]):
            flags.append("accepted-at-once")
        out.append({**t, "flags": flags, "prev": prev})
    return out


def short(s, n):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=28)
    ap.add_argument("--since", help="YYYY-MM-DD, overrides --days")
    ap.add_argument("--root", action="append", help="log folder; can repeat")
    ap.add_argument("--export", action="append", help="claude.ai export: conversations.json or zip")
    ap.add_argument("--project", help="substring of the path or cwd")
    ap.add_argument("--sample", type=int, default=0, help="sample size if there are more sessions")
    ap.add_argument("--max-chars", type=int, default=1500)
    ap.add_argument("--out")
    a = ap.parse_args()

    since = (datetime.fromisoformat(a.since).replace(tzinfo=timezone.utc) if a.since
             else datetime.now(timezone.utc) - timedelta(days=a.days))
    raw = []
    if not a.export or a.root:
        roots = [os.path.expanduser(r) for r in (a.root or DEFAULT_ROOTS)]
        for r in roots:
            if os.path.isdir(r):
                for f in glob.glob(os.path.join(r, "**", "*.jsonl"), recursive=True):
                    if os.path.getmtime(f) >= since.timestamp():
                        raw.append(read_session(f))
    for e in a.export or []:
        raw += read_export(os.path.expanduser(e))

    sessions = []
    for meta, turns in raw:
        if a.project and a.project not in meta["path"] and a.project not in (meta["cwd"] or ""):
            continue
        turns = [t for t in turns if t["ts"] is None or t["ts"] >= since]
        ut = flag_turns(turns)
        if not ut:
            continue
        start = next((t["ts"] for t in ut if t["ts"]), None)
        sessions.append({"meta": meta, "turns": ut, "start": start,
                         "n_fix": sum("correction" in t["flags"] for t in ut)})

    total, note = len(sessions), "all sessions"
    if a.sample and total > a.sample:
        k = a.sample * 2 // 5
        picked = {id(s): s for s in sorted(sessions, key=lambda s: -len(s["turns"]))[:k]
                  + sorted(sessions, key=lambda s: -s["n_fix"])[:k]}
        rest = [s for s in sessions if id(s) not in picked]
        random.seed(0)
        for s in random.sample(rest, min(len(rest), max(0, a.sample - len(picked)))):
            picked[id(s)] = s
        sessions = list(picked.values())
        note = f"sample {len(sessions)} of {total}: longest + most corrections + random (seed 0)"

    sessions.sort(key=lambda s: s["start"] or datetime.min.replace(tzinfo=timezone.utc))
    counts = {}
    for s in sessions:
        for t in s["turns"]:
            for fl in t["flags"]:
                counts[fl] = counts.get(fl, 0) + 1

    L = [f"# Person's messages since {since.date()}",
         f"Sessions found: {total}; in this file: {len(sessions)} ({note})",
         "Flags (hints, not findings): " + (", ".join(f"{k}={v}" for k, v in sorted(counts.items())) or "none"),
         ""]
    for s in sessions:
        m = s["meta"]
        d = s["start"].strftime("%Y-%m-%d %H:%M") if s["start"] else "date?"
        L += [f"## {d} · {m['source']} · {m['path']}",
              f"cwd: {m['cwd'] or '?'} · messages: {len(s['turns'])} · corrections: {s['n_fix']}", ""]
        for i, t in enumerate(s["turns"], 1):
            ts = t["ts"].strftime("%H:%M") if t["ts"] else "--:--"
            fl = " " + " ".join(f"[{x}]" for x in t["flags"]) if t["flags"] else ""
            if t["prev"]:
                L.append(f"> model: {short(t['prev'], 160)}")
            body = t["text"].strip()
            if len(body) > a.max_chars:
                body = body[: a.max_chars] + f"… [+{len(t['text']) - a.max_chars} chars]"
            L += [f"**{i}. {ts}**{fl}", body, ""]
    out = "\n".join(L)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"{a.out}: {len(sessions)} sessions, flags: {counts}")
    else:
        print(out)


if __name__ == "__main__":
    main()
