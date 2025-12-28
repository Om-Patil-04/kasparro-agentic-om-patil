# Blocks

Each LogicBlock = {block_id, payload, source_fields, confidence, generated_at, payload.dependencies?, payload.source_product}

## Defined Blocks
- benefits_block: payload = benefits list; source_fields=["benefits"]; confidence=1.0
- usage_block: payload = usage string; source_fields=["usage"]; confidence=1.0
- safety_block: payload = side_effects list; source_fields=["side_effects"]; confidence=1.0
- pricing_block: payload = price; source_fields=["price"]; confidence=1.0
- ingredients_block: payload = key_ingredients list; source_fields=["key_ingredients"]; confidence=1.0
- highlights_block: payload = up to 4 highlights from concentration/key_ingredients/benefits/skin_types; confidence=0.8
- comparison_block: payload = {price, ingredients, benefits, suitability} comparing A vs B; confidence=0.7; source_fields=["price","key_ingredients","benefits","skin_types"]

Confidence Rules
- High (1.0) when directly copying normalized fields.
- Slightly lower (0.8–0.7) for composed/highlight/comparison logic.

Dependencies
- Highlights/comparison may list dependencies in payload["dependencies"] (empty if none).