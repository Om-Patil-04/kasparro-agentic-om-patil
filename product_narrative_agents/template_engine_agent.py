from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List

from foundation_schema.shared_types import Answer, DataModel, LogicBlock, Meta, TemplateResult


def _block_map(blocks: List[LogicBlock]) -> Dict[str, LogicBlock]:
    return {b.block_id: b for b in blocks}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def execute(blocks: List[LogicBlock], answers: List[Answer], dm: DataModel, product_b: DataModel):
    block_lookup = _block_map(blocks)

    def get_payload(block_id: str, default):
        block = block_lookup.get(block_id)
        return block.payload if block else default

    faq = {
        "qa": [
            {"question": a.question, "answer": a.answer, "category": a.category, "confidence": a.confidence}
            for a in answers
        ],
    }
    faq_meta = Meta(
        version="1.0",
        generated_at=_now_iso(),
        orchestrator="template_engine_agent",
        blocks_used=[],
        source_product=dm.attributes.get("name", dm.id),
    )
    faq_result = TemplateResult(page_type="faq", content=faq, meta=faq_meta)

    product_page = {
        "name": dm.attributes.get("name", dm.id),
        "highlights": get_payload("highlights_block", {}).get("payload", "Not specified."),
        "details": {
            "price": dm.attributes.get("price", "Not specified"),
            "benefits": dm.attributes.get("benefits", "Not specified"),
            "usage": dm.attributes.get("usage", "Not specified"),
            "ingredients": dm.attributes.get("key_ingredients", "Not specified"),
            "side_effects": dm.attributes.get("side_effects", "Not specified"),
            "suitability": dm.attributes.get("skin_types", "Not specified"),
        },
    }
    product_meta = Meta(
        version="1.0",
        generated_at=_now_iso(),
        orchestrator="template_engine_agent",
        blocks_used=[b.block_id for b in blocks],
        source_product=dm.attributes.get("name", dm.id),
    )
    product_result = TemplateResult(page_type="product_page", content=product_page, meta=product_meta)

    comparison_block = get_payload("comparison_block", {"payload": "Not specified."})
    comparison_page = {
        "product_a": dm.attributes.get("name", dm.id),
        "product_b": product_b.attributes.get("name", product_b.id),
        "comparison": comparison_block.get("payload", "Not specified."),
    }
    comparison_meta = Meta(
        version="1.0",
        generated_at=_now_iso(),
        orchestrator="template_engine_agent",
        blocks_used=["comparison_block"],
        source_product=dm.attributes.get("name", dm.id),
    )
    comparison_result = TemplateResult(page_type="comparison_page", content=comparison_page, meta=comparison_meta)

    return {"faq": faq_result, "product_page": product_result, "comparison_page": comparison_result}