from foundation_schema.shared_types import DataModel
from foundation_schema.validator import validate_data_model

dm = DataModel(
    id="sku-123",
    attributes={
        "concentration": "10% Vitamin C",
        "price": "₹999",
        "skin_types": ["Oily", "Sensitive"],
        "benefits": ["Brightening", "Even tone"],
        "key_ingredients": ["Vitamin C", "Ferulic acid"],
    },
)

result = validate_data_model(dm)
print(result)