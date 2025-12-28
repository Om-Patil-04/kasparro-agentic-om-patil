# Kasparro Agentic Content Generation System

## Overview
A modular, multi-agent pipeline that turns a small product dataset into structured, machine-readable JSON pages (FAQ, Product Page, Comparison). It enforces clear agent boundaries, reusable logic blocks, lineage, and confidence tracking.

## Features
- Parsing and normalization → `DataModel`
- Validation with regex/enums
- Question generation (≥15) across categories
- Data-grounded QA (no new facts; low confidence for unknowns)
- Logic blocks (benefits, usage, safety, pricing, ingredients, highlights, comparison)
- Template assembly into three JSON pages
- Lineage (`blocks_used`, `source_fields`) and confidence per answer/block
- Tests per agent (pytest)

## Repository Structure
- `foundation_schema/`: shared types, validator, helper script
- `product_narrative_agents/`: parser, question generator, QA matcher, block composer, template engine, formatter
- `product_b_config.py`: static Product B config
- `orchestrator.py`: DAG runner
- `tests/`: one test file per agent
- `docs/`: architecture, templates, blocks, runbook, extensibility, projectdocumentation

## Prerequisites
- Python 3.12+
- (Optional) Docker if you want containerized runs

## Setup
```bash
cd <repo-root>
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # on Windows; use source .venv/bin/activate on macOS/Linux
pip install -r requirements.txt  # installs pytest for tests
```

## Run the Pipeline (Golden Input)
```bash
cd <repo-root>
python -m orchestrator
# or
python orchestrator.py
```
You should see `faq.json`, `product_page.json`, `comparison_page.json` printed with `meta` then `content`, `orchestrator: "agentic-v1"`, and lineage in `blocks_used`.

## Run Tests
```bash
cd <repo-root>
pytest -q
```

## Containerize (Optional)
1) Build:
```bash
docker build -t kasparro-agentic:latest .
```
2) Run:
```bash
docker run --rm kasparro-agentic:latest
```

## Notes on Data & Guardrails
- Uses only the provided product data; no external facts.
- Unknown fields → “Not specified from provided data.” with low confidence.
- Comparison strictly between Product A (input) and static Product B.

## Submission Naming
Name the repo: `kasparro-ai-agentic-content-generation-system-<first_name-last_name>`.

## Key Outputs
- `faq.json`: ≥15 Q&As, with confidence and lineage.
- `product_page.json`: highlights and details, with block lineage.
- `comparison_page.json`: A vs. B differences, with block lineage.