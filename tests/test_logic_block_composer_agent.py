from product_narrative_agents.logic_block_composer_agent import execute
from foundation_schema.shared_types import DataModel

def test_logic_blocks_and_highlights():
    dm_a = DataModel(
        id="a",
        attributes={
            "name": "GlowBoost Vitamin C Serum",
            "concentration": "10% Vitamin C",
            "skin_types": ["Oily", "Combination"],
            "key_ingredients": ["Vitamin C", "Hyaluronic Acid"],
            "benefits": ["Brightening", "Fades dark spots"],
            "usage": "Apply 2–3 drops in the morning before sunscreen",
            "side_effects": ["Mild tingling for sensitive skin"],
            "price": "₹699",
        },
    )
    dm_b = DataModel(id="b", attributes={"key_ingredients": [], "benefits": [], "skin_types": [], "price": "₹649"})
    blocks = execute(dm_a, dm_b)
    ids = {b.block_id for b in blocks}
    assert {"benefits_block","usage_block","safety_block","pricing_block","ingredients_block","highlights_block","comparison_block"}.issubset(ids)
    highlights = next(b for b in blocks if b.block_id == "highlights_block").payload["payload"]
    assert len(highlights) <= 4