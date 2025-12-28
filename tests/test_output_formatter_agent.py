from product_narrative_agents.output_formatter_agent import execute
from foundation_schema.shared_types import Meta, TemplateResult

def test_output_formatter_json_serializable():
    meta = Meta(version="1.0", generated_at="now", orchestrator="test", blocks_used=["x"], source_product="Glow")
    pages = {
        "faq": TemplateResult(page_type="faq", content={"qa": []}, meta=meta),
        "product_page": TemplateResult(page_type="product_page", content={}, meta=meta),
    }
    out = execute(pages)
    assert "faq.json" in out
    assert "product_page.json" in out