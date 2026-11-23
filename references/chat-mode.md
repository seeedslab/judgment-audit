# Chat mode (claude.ai, apps)

No session logs and no file system. Steps 1, 2, and 6 change as follows.

## Step 1. Inventory

Check and show what is available:
- **past-chat search** (conversation_search, recent_chats, read_conversation) — the main source;
- **memory** — saved preferences and rules, this is the written-down judgment layer;
- **project instructions and project files**, if the chat is inside a project;
- **uploaded files** — work outputs for question 4.2;
- **data export** (`conversations.json` or a zip) if the person attached it: then work as in Claude Code via `scripts/extract_turns.py --export <file>`.

Without a chat export, say it plainly: the sample is incomplete, frequencies are a lower bound.

## Step 2. Collection

- `recent_chats` for the window: page through up to 5 pages of 20 chats.
- Pick 8–12 chats: the longest, the ones with work outputs, the ones with judgment tasks and high stakes. State the sampling method.
- Inside a chat, search for signals with `within_conversation_id`: "ok go", "you pick", "what's better", "not like that", "I said", "just tell me", "how we do it". Open the chat at the hit, don't read it whole.
- For 4.3, look for repeats across all chats: the same evaluation or correction words.

Every quote gets the chat title and date.

## Step 6. Saving

There's no file. Offer in one line: the report can be saved as a document, but only if the person asks, and never published as a page with a link. Don't write audit findings to memory.
