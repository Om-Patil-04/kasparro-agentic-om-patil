from product_narrative_agents.parser_agent import execute

def test_parser_trims_and_splits():
    raw = {
        "name": " GlowBoost Vitamin C Serum ",
        "skin_types": "Oily, Combination ",
        "key_ingredients": "Vitamin C, Hyaluronic Acid",
        "benefits": "Brightening, Fades dark spots",
        "side_effects": " Mild tingling ",
        "usage": " Apply 2–3 drops ",
        "price": "₹699",
        "concentration": "10% Vitamin C",
    }
    dm = execute(raw)
    attrs = dm.attributes
    assert attrs["name"] == "GlowBoost Vitamin C Serum"
    assert attrs["skin_types"] == ["Oily", "Combination"]
    assert attrs["key_ingredients"] == ["Vitamin C", "Hyaluronic Acid"]
    assert attrs["benefits"] == ["Brightening", "Fades dark spots"]
    assert attrs["side_effects"] == ["Mild tingling"]
    assert attrs["usage"] == "Apply 2–3 drops"
    assert attrs["price"] == "₹699"
    assert attrs["concentration"] == "10% Vitamin C"