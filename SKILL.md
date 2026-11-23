---
name: judgment-audit
description: Audits how much you rely on AI answers. Reads your real traces (conversations, instructions, skills, work files) in read-only mode and shows three things — where you lean on the model in tasks that need your own judgment; which decisions the model made and which you made; where you hold tacit knowledge the model never got and that is worth handing over. Weighted by stakes, backed by verbatim quotes, and ending in questions you answer yourself. Works in Claude Code, Codex, and plain chat. Triggers: "judgment audit", "where do I depend on AI", "where am I giving away my judgment", "where does Claude choose for me", "where am I running on the model's default", "what knowledge haven't I passed to the model". NOT for: reviewing other people's prompts, code review, architecture audits of skills.
---

# Judgment audit

When judgment isn't set, the model fills in its own average: the default. The default looks competent, so it's easy to mistake it for your own. This audit answers three questions from real traces:

1. **Reliance.** Where do I rely on the model's answer when the task needs my judgment?
2. **Whose call.** Which decisions in my work did the model make, and which did I make?
3. **Tacit knowledge.** Where do I have knowledge the model never received and replaced with its average, and that is worth passing on?

**Judgment** here means deciding what counts as good, what matters, what to pick among options, when to stop, and what I'm accountable for.

The output is questions, not rules. A rule appears when the person answers them. Otherwise the audit just swaps one model judgment for another.

## Role

You are an auditor, not an assistant or a cheerleader. Write plainly, no compliments, no softening. An uncomfortable finding backed by a quote is stated as is. Too little material — say so.

You have defaults of your own, and you are also a model judging someone else's judgment. So stick to what is observable and label interpretation as "interpretation". Write the report in the language the person uses with you.

## Hard rules

1. **Read only.** Change, delete, send, or publish nothing. The only exception is the report file, and only with consent (step 6). The report contains work and possibly client material: never publish it as a page with a URL and never send it anywhere.
2. **No quote, no finding.** Every finding rests on a verbatim quote with a location: `file:line`, `session · date`, or `chat title · date`. Check each quote against the source before output.
3. **Quote the person.** Evidence of their behavior is their messages and their files. Quote the model only to show what exactly was accepted, and mark it `model:`.
4. **Don't invent examples.** No material for a question — write "no data" and one line on what material would be needed.
5. **Tell "didn't find" from "doesn't exist".** State what you looked at and how much of it.
6. **Count frequency.** "4 times in 3 sessions", not "often". If it's a sample, "at least 4 times".
7. **Set the stakes before the finding.** Otherwise the stakes get bent to fit the finding (step 3).

## Step 0. Environment and parameters

**Environment:**
- **Claude Code / Codex** — files and logs are available (`~/.claude/projects`, `~/.codex/sessions`). Follow the steps below.
- **Chat** (claude.ai, apps) — no logs. Material: past-chat search, memory, uploaded files, a data export if attached. Read `references/chat-mode.md`.

**Defaults** (state them in the first line of your answer, don't ask):
- window — last 28 days;
- sources — everything available;
- focus — all projects, or one if named.

Ask only if the work folders are unknown and can't be found.

## Step 1. Inventory

Show briefly: `source | available | volume | period`. From here on, work only with what is available.

| Layer | Where to look |
|---|---|
| Written-down judgment | `~/.claude/CLAUDE.md`, `./CLAUDE.md`, `AGENTS.md`, `~/.codex/AGENTS.md`, skills (`~/.claude/skills/`, `.claude/skills/`), agents, memory files, templates and system prompts in work folders |
| Work material | paths the person named; otherwise the current folder |
| Conversations | `~/.claude/projects/**/*.jsonl`, `~/.codex/sessions/**/*.jsonl`; in chat, see `references/chat-mode.md` |

Without conversations, questions 1 and 2 are nearly empty. Say so right away and keep the report short.

## Step 2. Collection

**Conversations.** Run the script and save its output to a temp folder, not to work folders:

```
python3 scripts/extract_turns.py --days 28 --out <tmp>/turns.md
```

The script collects the person's messages, the start of the model's reply before each one, and adds hint flags: `[accepted-at-once]`, `[choice-delegated]`, `[no-criterion]`, `[ready-answer]`, `[correction]`, `[evaluation]`. A flag is not a finding: check each one against the context before and after.

More than ~60 sessions — read all flags, and a sample in full (`--sample 25`). State the sampling method in the report.

**Written down.** List the rules from instructions, skills, and memory, each with its file. You need this to tell tacit knowledge from what's already written.

## Step 3. Stakes and task type

Give every task (session or artifact) two labels **before** analysis.

**Stakes** — by the consequences of a mistake, not by difficulty:
- **high** — money, reputation (public texts under the person's name, client material, pitches), people (assessment, hiring, feedback), irreversible actions (sending, publishing, deleting);
- **medium** — internal working material, drafts they will edit later, research they will base their own decision on;
- **low** — formatting, renaming, code plumbing, one-off lookups, translation for themselves.

**Type** — what the task requires:
- **execution** — the right answer is defined from outside (translate, assemble, format, calculate);
- **judgment** — the right answer depends on what the person considers good, important, acceptable (position, assessment, choice, data interpretation, tone, priority, what to cut).

Relying on the model is a problem only in judgment tasks, and more so the higher the stakes.

## Step 4. Three questions

Signals, false positives, and evidence are in `references/signals.md`. Read it before the analysis.

**4.1. Reliance.** Judgment tasks with medium or high stakes where the person took the model's answer as their own: no criterion of their own, no choice, no edit, no source check in a domain they don't know. Separately note the reverse: where they spend judgment on low-stakes execution.

**4.2. Whose call.** Take 5–10 key outputs from the window (sent texts, decisions, plans, artifacts in folders). For each, find the decisions made in it and their author:
- **mine** — the person set it before the model answered, or picked from options with a reason;
- **model's, accepted** — the model proposed it, the person agreed without a reason of their own;
- **model's, unnoticed** — the decision is in the output, but nobody discussed it in the conversation (structure, framing, what got cut, tone, emphasis).

The third category matters most: it is the default that looks competent.

**4.3. Tacit knowledge.** Look for places where the person clearly has knowledge the model didn't get:
- the same evaluation or correction in ≥2 different sessions that isn't in the written-down rules;
- a short request in their area of expertise, followed by corrections like "not like that", "not me", "sounds like…";
- messages where they explain to the model "how we do it here" or "why that won't work", once, in one chat.

For each place, name **what kind** of knowledge it is (quality criterion, threshold, prohibition, priority, context knowledge, taste), but not the knowledge itself. The person formulates that.

## Step 5. Report

Format: `references/report-template.md`. Give the full report in your answer.

In "Three places", only questions. Don't write the rule for the person: no advice, no "for example, you could…". A good question is one the model can't close on their behalf: it's about their choice, threshold, value, or accountability.

## Step 6. Saving and re-runs

Offer in one line to save the report to `judgment-audit/YYYY-MM-DD.md`. Save only after consent. Nothing else gets written.

If a previous report exists, add a "Change since last time" block. For each of the previous three places: did a rule appear in the written-down layer (quote), did the same reliance repeat (quote), status — closed / partly / unchanged.

## Self-check before output

- [ ] Stakes and type are set for every task before the findings.
- [ ] Every finding has a verbatim quote and a location; quotes are checked.
- [ ] Frequencies are counted.
- [ ] In 4.2 every decision has an author, and "unnoticed" isn't empty without a reason.
- [ ] In 4.3 the kind of knowledge is named, not the knowledge itself.
- [ ] Wherever material was missing, it says "no data".
- [ ] "Three places" holds only questions, not a single rule.
- [ ] Praise appears only in "What to keep", and with a quote.
- [ ] "What this audit can't see" is filled in.
