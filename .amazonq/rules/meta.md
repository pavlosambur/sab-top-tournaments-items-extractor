# How to Manage Rules

When user asks to add a rule or requirement:

1. Determine if it fits an existing file in `.amazonq/rules/` or needs a new one
2. New file — if the topic is a separate library/technology (e.g. `selenium.md`, `google-sheets.md`)
3. Existing file — if it extends a topic that already has a file
4. Write rules concisely: 1-2 lines per rule, no fluff
5. Use format: `- Do X` or `- Never do Y` or `- Prefer X over Y`

When user shares a code snippet they like:

1. Save it to `.amazonq/snippets/` with a descriptive filename (e.g. `logger.py`, `sheets_client.py`)
2. When user needs similar functionality in the project — use the saved snippet as a reference
