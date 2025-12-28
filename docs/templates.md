# Templates

## FAQ Page
- content.qa: list of {question, answer, category, confidence} (≥5 entries; generator produces 15).
- meta: {page_type="faq", version, generated_at, orchestrator, blocks_used (["qa_matcher" or empty]), source_product}.

## Product Page
- content.name: product name or id.
- content.highlights: top highlights from highlights_block (fallback: "Not specified.").
- content.details: {price, benefits, usage, ingredients, side_effects, suitability}, each fallback to "Not specified".
- meta.blocks_used: includes benefits_block, usage_block, safety_block, pricing_block, ingredients_block, highlights_block, comparison_block (as available).

## Comparison Page
- content: {product_a, product_b, comparison: {price, ingredients, benefits, suitability}} from comparison_block; fallback "Not specified." when missing.
- meta.blocks_used: ["comparison_block"] when present.

Fallbacks:
- Missing block → default dict/payload "Not specified."
- Missing field → "Not specified."