# Runbook

## Prereqs
- Python 3.12+
- From repo root:
  ```
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt   # if present
  ```

## Run Orchestrator (golden input)
```
cd <repo-root>
python -m orchestrator
# or
python orchestrator.py
```

## Expected Outputs
- Prints faq.json, product_page.json, comparison_page.json to stdout.
- FAQ ≥15 Q&As (>=5 required), product page, comparison page.

## Tests
```
cd <repo-root>
pytest -q
```

## Error Handling
- Parse/Validate failures: pipeline halts, success=False, error logged in messages.
- Downstream errors (blocks/templates/formatter): continue with fallbacks, success=False on that agent message, output may be empty/default.
- Module import errors: ensure running from repo root; ensure product_b_config.py exists in root; use `python -m orchestrator` or `python orchestrator.py`.

## Logging/Trace
- Each run has trace_id (UUID) and per-agent messages with success/error.