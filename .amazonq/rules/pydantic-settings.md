# Pydantic Settings

- Use `pydantic-settings` (`BaseSettings` + `SettingsConfigDict`) for all env config
- One model per `.env` source — never mix different files in one model
- Name models descriptively by what they contain (e.g. `BackofficeCredentials`, `GoogleSheetsConfig`)
- Store all settings models in `config/settings.py`
- Export instances at module level: `settings = Settings()`, `credentials = BackofficeCredentials()`
- Path to external `.env` files — store in project `.env`, read via parent model
