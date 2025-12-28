# Extensibility: Adding a New Field (example: fragrance_free: boolean)

1) Schema / Types
- Update `foundation_schema/shared_types.py` (DataModel attrs need no strict typing change, but document the new key).

2) Validation
- In `foundation_schema/validator.py`, add a check:
  ```
  val = attrs.get("fragrance_free")
  if val is not None and not isinstance(val, bool):
      errors.append("Invalid fragrance_free: must be boolean")
  ```

3) Parser
- In `parser_agent.py`, allow passthrough of `fragrance_free` (bool). No splitting; just trim if string or convert to bool if you decide (optional). Default: leave as-is.

4) Question Generation
- In `question_generator_agent.py`, add templates:
  - "Is {name} fragrance-free?" → Category.SAFETY, source_fields=["fragrance_free","name"]

5) QA Matcher
- In `qa_matcher_agent.py`, map intent:
  - If category SAFETY and field fragrance_free exists:
    - True → "Yes, it is fragrance-free."
    - False → "No, it is not fragrance-free."
    - Else → "Not specified from provided data." with low confidence (e.g., 0.2–0.3).

6) Logic Blocks (optional)
- If you want a block: add `fragrance_block` in `logic_block_composer_agent.py` with source_fields=["fragrance_free"], confidence=1.0.

7) Templates
- In `template_engine_agent.py`, surface the new field:
  - product_page.details["fragrance_free"] = attrs.get("fragrance_free", "Not specified")
  - If you added a block, wire it as a dependency; include block_id in blocks_used.

8) Tests
- Add unit tests:
  - parser: passes/normalizes fragrance_free.
  - validator: rejects non-bool.
  - question_gen: question appears when field present.
  - qa_matcher: answers based on bool; “Not specified” when missing.
  - template_engine: field surfaces with fallback.
  - formatter: still JSON-serializable.

9) Docs
- Update `docs/templates.md` and `docs/blocks.md` to reflect the new field/block.