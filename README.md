# judgment-audit

A skill for Claude Code, Codex, or plain chat that reads your own AI history and shows where the call was yours and where you just took the model's default.

When you don't set the judgment, the model fills in its average. That average looks competent, so it passes as yours. This audit goes through your real traces (session logs, CLAUDE.md / AGENTS.md, skills, memory, work files) and answers three questions:

1. **Reliance.** Where do you lean on the model in tasks that need your judgment?
2. **Whose call.** Which decisions in your outputs did you make, which did the model make and you accepted, and which did it make without anyone noticing?
3. **Tacit knowledge.** What do you keep correcting session after session but never wrote down?

Every finding needs a verbatim quote with a location, and every task is weighted by stakes first: a model default on a code rename is fine, on a client invoice it isn't. The report ends in questions, not rules. You write the rule yourself, otherwise you've just swapped one model judgment for another.

## Install

Claude Code:

```
git clone https://github.com/seeedslab/judgment-audit ~/.claude/skills/judgment-audit
```

Codex: clone into `~/.codex/skills/judgment-audit`.

Chat (claude.ai): upload the folder as a skill. Without session logs it works from past-chat search and memory, or from a data export if you attach one (see `references/chat-mode.md`).

## Run

Ask for a "judgment audit". Defaults: last 28 days, all sources it can reach, all projects. You can name a project or a window.

It's read-only. It runs `scripts/extract_turns.py` to pull your messages from `~/.claude/projects` and `~/.codex/sessions` into a temp file, and asks before saving the report anywhere. The report quotes your work, so keep it to yourself.

## What it can't see

Judgment that leaves no text trace: what's in your head, live conversations, files you edited by hand. And the auditor is a model too, with its own defaults, so it labels its interpretations.

## Files

- `SKILL.md` — the procedure
- `references/signals.md` — what counts as reliance, whose call, tacit knowledge; false positives
- `references/report-template.md` — report format
- `references/chat-mode.md` — running without logs
- `scripts/extract_turns.py` — log extraction with hint flags (English and Russian patterns)

By Nailia Aglitskaya.
