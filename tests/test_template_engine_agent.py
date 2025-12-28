from product_narrative_agents.template_engine_agent import execute
from foundation_schema.shared_types import Answer, Category, DataModel, LogicBlock

def test_template_engine_fallbacks():
    dm_a = DataModel(id="a", attributes={"name": "GlowBoost", "price": "₹699"})
    dm_b = DataModel(id="b", attributes={"name": "LumiCare", "price": "₹649"})
    answers = [Answer("What is the price?", "₹699", Category.PURCHASE, 0.9, ["price"])]
    blocks = [LogicBlock("pricing_block", {"payload": "₹699", "dependencies": [], "source_product": "GlowBoost"}, ["price"], 1.0, "")]
    pages = execute(blocks, answers, dm_a, dm_b)
    assert "faq" in pages and "product_page" in pages and "comparison_page" in pages
    # ensure missing blocks don’t crash; comparison content should exist
    comparison = pages["comparison_page"].content["comparison"]
    assert "price" in comparison