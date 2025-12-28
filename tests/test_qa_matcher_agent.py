from product_narrative_agents.qa_matcher_agent import execute
from foundation_schema.shared_types import Answer, Category, DataModel, Question

def test_qa_matcher_answers_from_data():
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
    dm_b = DataModel(
        id="b",
        attributes={
            "name": "LumiCare Bright Serum",
            "price": "₹649",
            "key_ingredients": ["Niacinamide 5%", "Licorice Extract"],
            "benefits": ["Brightening", "Evens tone"],
            "skin_types": ["Normal", "Combination"],
        },
    )
    qs = [
        Question("What is the price?", Category.PURCHASE, ["price"]),
        Question("Is it fragrance free?", Category.SAFETY, ["side_effects"]),
    ]
    answers = execute(qs, dm_a, dm_b)
    assert len(answers) == 2
    price_answer = answers[0].answer
    assert "₹699" in price_answer
    unknown_answer = answers[1].answer
    assert "Not specified" in unknown_answer or "Mild tingling" in unknown_answer  # allows data-based safety
    if "Not specified" in unknown_answer:
        assert answers[1].confidence <= 0.3