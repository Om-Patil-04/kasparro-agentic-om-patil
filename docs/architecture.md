# Architecture

## Agents & Responsibilities
- parser_agent: normalize raw input → DataModel (id, attributes).
- validator: schema/regex/enums validation → ValidationResult.
- question_generator_agent: generate ≥15 questions with categories and source_fields.
- qa_matcher_agent: answer questions from data only; low confidence + “Not specified…” if unknown.
- logic_block_composer_agent: produce LogicBlock[] with block_id, payload, source_fields, confidence.
- template_engine_agent: assemble pages (faq, product_page, comparison_page) from blocks + answers; includes meta.blocks_used.
- output_formatter_agent: ensure JSON-serializable; outputs {page}.json.
- orchestrator: DAG runner with tracing, error handling, message log.

## DAG / Flow
raw_input → parser(A) → validator → question_generator → qa_matcher → logic_block_composer → template_engine → output_formatter
product_b_input → parser(B) ┐
                         └─────────────↑
Errors:
- Parse/Validate: halt with error.
- Downstream (blocks/templates/formatter): continue with fallbacks; mark success=False in message where applicable.

## Message Schema (per agent)
{
  trace_id: str (UUID),
  agent_id: str,
  input: Any,
  output: Any,
  success: bool,
  error: {message: str, stage: str} | null
}

## Confidence & Lineage
- Each Answer: confidence, source_fields.
- Each LogicBlock: confidence, source_fields, block_id.
- meta.blocks_used: list of block_ids consumed for each page.
- template_engine preserves source_product, blocks_used.