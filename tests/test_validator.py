from foundation_schema.shared_types import DataModel
from foundation_schema.validator import validate_data_model

def test_validator_happy_path():
    dm = DataModel(
        id="sku",
        attributes={
            "concentration": "10% Vitamin C",
            "price": "₹699",
            "skin_types": ["Oily", "Combination"],
            "benefits": ["Brightening", "Fades dark spots"],
            "key_ingredients": ["Vitamin C", "Hyaluronic Acid"],
        },
    )
    result = validate_data_model(dm)
    assert result.is_valid
    assert result.errors == []

def test_validator_rejects_bad_price():
    dm = DataModel(
        id="sku",
        attributes={
            "concentration": "10% Vitamin C",
            "price": "699",  # missing currency symbol
            "skin_types": ["Oily"],
            "benefits": ["Brightening"],
            "key_ingredients": ["Vitamin C"],
        },
    )
    result = validate_data_model(dm)
    assert not result.is_valid
    assert any("Invalid price" in e for e in result.errors)