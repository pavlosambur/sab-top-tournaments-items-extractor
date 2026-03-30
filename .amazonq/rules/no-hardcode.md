# No Hardcoding

## General
- Never hardcode strings, numbers, timeouts, file paths, selectors, or any literal values in code
- Always define a variable or constant first, then use it
- If a value can be typed — create a Pydantic model or dataclass for it

## Config files (`config/`)
- Store all project configuration in `config/` as separate files per module (e.g. `config/google_sheets.py`, `config/selenium.py`)
- Examples: spreadsheet IDs, XPath selectors, column names, timeouts, URLs, file paths
- Import and use these variables throughout the project

## Sensitive values (`.env`)
- Store secrets, credentials, API keys, tokens in `.env`
- Load via `pydantic-settings` or `python-dotenv`
- Never commit `.env` to git

## Models
- When a group of related constants forms a structure (e.g. column names, page selectors) — create a typed model in `models/`
