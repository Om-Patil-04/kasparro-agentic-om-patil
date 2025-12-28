from product_narrative_agents.question_generator_agent import execute
from foundation_schema.shared_types import DataModel

def test_question_count_and_no_hallucinations():
    dm = DataModel(
        id="sku",
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
    qs = execute(dm)
    assert len(qs) >= 15
    # ensure no unknown fields in source_fields
    allowed = {
        "name","concentration","skin_types","key_ingredients",
        "benefits","usage","side_effects","price"
    }
    for q in qs:
        assert set(q.source_fields).issubset(allowed)