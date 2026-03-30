# Logging

- Use `loguru` for all logging (`from loguru import logger`)
- Never use stdlib `logging` module
- Configure logger using `lib/logger.py` snippet from `.amazonq/snippets/logger.py`
- Call `setup_logger()` once at the entry point before any other code
- Log format must output relative file paths (`lib/actions.py:99`) so they are clickable in VS Code terminal
- Log everything: function entry/exit, key decisions, state changes, errors
- Keep logs concise: log file names, row counts, element IDs — not full contents
- Never dump large data to logs (file contents, full tables, lists of all elements)
- Good: `logger.info("Read spreadsheet: {rows} rows", rows=len(data))`
- Bad: `logger.info("Spreadsheet data: {data}", data=data)`
