# Python Code Style

## Functions
- Never write complex logic in a single function — break it into smaller focused functions
- Each function should do one thing
- Compose functions: use small functions inside larger ones
- Main/orchestrator functions (like `run()`) should only call sub-functions, never contain logic directly
- Sub-functions with logic should be nested inside the parent function, prefixed with `_`, and called immediately after definition
- Every function must have a docstring describing what it does
