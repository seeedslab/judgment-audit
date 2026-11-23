# Signals: markers, false positives, evidence

The script's flags show where to look. A finding is made only after reading the context: the messages before and after the flag.

---

## 1. Reliance: the model where my judgment is needed

**Markers of reliance:**
- `[accepted-at-once]`: "ok", "great", "go", "next" right after a long answer in a judgment task;
- `[no-criterion]`: "make it good", "improve it", "whatever you think is best", "your call on style" — and the result is accepted;
- `[ready-answer]`: "just tell me", "what's the best", "no sources" where the fact affects a decision, and the sources were never opened afterwards;
- a confident model answer in a domain the person doesn't know, accepted without "I don't know, give me sources";
- data interpretation (what the numbers, survey, or reviews mean) taken from the model with no hypothesis of their own before the answer.

**Their judgment is visible when:**
- a criterion is set before the answer: for whom, what for, what counts as success, what to avoid;
- they bring their own hypothesis, draft, or position and ask to test or challenge it;
- they argue with the answer on substance, ask for counterarguments, open and comment on sources.

**False positives:**
- "ok" on an execution task or a low-stakes one is normal delegation;
- the criterion may have been set earlier: in CLAUDE.md, a skill, the first message of the session. Check the written-down layer;
- a manual file edit is visible after "ok" — that's not "accepted as is".

**Wasted judgment** (the flip side): repeated formatting fixes, arguing over the wording of an internal draft, manually checking something that could be written down once.

**Evidence:** the person's message + `model:` start of the accepted answer + what happened next.

---

## 2. Whose call

**How to break down an output:**
1. List the decisions visible in it: framing, structure, what's in and what got cut, emphasis, tone, conclusion, recommendation.
2. For each, find the moment in the conversation where it appeared.
3. Assign the author:
   - **mine** — their message before the model's answer sets this decision, or they picked from options and gave a reason ("taking the second one because…");
   - **model's, accepted** — the model proposed it, their reaction is agreement without a reason;
   - **model's, unnoticed** — the decision is in the output, but it was never discussed in the conversation.

**`[choice-delegated]`:** "you pick", "whatever you recommend, we'll do", "you decide". This is direct delegation of a choice — check the stakes.

**False positives:** the model's decision matches a rule the person wrote down earlier — that's their judgment, executed by the model. Name the rule.

**Evidence:** a quote from the output (what was decided) + a quote from the conversation (who decided) or "not discussed in the conversation".

---

## 3. Tacit knowledge

**Markers:**
- `[evaluation]`: "I don't like", "don't write like that", "always", "never", "too", "what matters to me", "how we do it here", "not me", "sounds like…";
- `[correction]` after a short request in their domain: "no", "not like that", "I told you", "again";
- explaining to the model "how it works here", "why this won't work with these people", "what the client actually means".

**How to look:**
- group evaluations and corrections by meaning, not by words;
- for each group, check the written-down layer. If the rule exists but the correction keeps repeating, the rule doesn't work: give both quotes;
- separately note domains where the person is an expert (by profile, projects, topic frequency) but their requests are short and without context.

**Kind of knowledge** — name it, but don't formulate the knowledge itself:
quality criterion · threshold ("good enough means…") · prohibition · priority · context knowledge (people, client, history) · taste / voice.

**False positives:** a repeat within one session; a one-off reaction to a specific text.

**Evidence:** ≥2 quotes from different sessions with dates + "not found in the written-down layer" with the list of files checked.

---

## Stakes × type

| | Execution | Judgment |
|---|---|---|
| **High stakes** | check the result, but it can be handed off | **main risk**: reliance here goes first in the report |
| **Medium** | hand it off | check whether a criterion was set |
| **Low** | hand it off; manual work here is **wasted judgment** | handing off is fine |

---

## Questions for "Three places"

A good question:
- can't be answered by the model on the person's behalf: it's about their choice, threshold, value, or accountability;
- turns into a rule in one or two sentences once answered;
- is tied to the situation found.

Don't ask:
- rhetorically ("Shouldn't you consider…?");
- with the answer inside ("Maybe you should always ask for sources?");
- about the model's taste ("Which style would work better?").

Working forms:
- "What has to be in [output] for you to sign it with your name, no edits?"
- "Which decision in [output] would you have made differently if you'd decided before reading the answer?"
- "Under what condition do you check [this] yourself, and when do you hand it off?"
- "What have you already explained three times about [topic], and which file should it go into?"
- "What are you accountable for in [task] if the result turns out wrong?"
