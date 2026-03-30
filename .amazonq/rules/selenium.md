# Selenium

## State verification
- After every action (click, form submit, navigation) — always verify the expected state change
- Never assume an action succeeded — check for element appearance/disappearance or attribute change
- If user forgets to describe expected state change — ask before writing code

## Retries and waits
- Use `click_and_wait()` from `lib/actions.py` for click actions that change state
- Use `fill_and_verify()` from `lib/actions.py` for filling input fields
- Use `click_and_wait_attribute()` from `lib/actions.py` for click actions that change element attributes
- Timeout and retry count come from settings (`selenium_wait_timeout`, `selenium_retries`)
- If all retries exhausted — raise RuntimeError and stop execution
- Don't write one universal helper — add focused helpers per interaction pattern as needed

## Selectors
- Store all selectors in `config/selenium.py`
- Never hardcode selectors in business logic
- Never use CSS class names for locating elements — they are hashed and unreliable
- Use text content, placeholders, labels, IDs, and DOM structure (following/preceding/ancestor) instead
