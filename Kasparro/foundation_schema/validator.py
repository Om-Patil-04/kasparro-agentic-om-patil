from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List

from .shared_types import DataModel

CONCENTRATION_RE = re.compile(r"^\d+% .+$")
PRICE_RE = re.compile(r"^₹\d+$")
ALLOWED_SKIN_TYPES = {"Oily", "Dry", "Combination", "Sensitive", "Normal"}


@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str] = field(default_factory=list)


def validate_data_model(dm: DataModel) -> ValidationResult:
    errors: List[str] = []
    attrs = dm.attributes

    required_fields = ["concentration", "price", "skin_types", "benefits", "key_ingredients"]
    for field_name in required_fields:
        if field_name not in attrs:
            errors.append(f"Missing field: {field_name}")
    if errors:
        return ValidationResult(is_valid=False, errors=errors)

    concentration = attrs.get("concentration")
    if not isinstance(concentration, str) or not CONCENTRATION_RE.match(concentration):
        errors.append("Invalid concentration: must match ^\\d+% .+$")

    price = attrs.get("price")
    if not isinstance(price, str) or not PRICE_RE.match(price):
        errors.append("Invalid price: must match ^₹\\d+$")

    skin_types = attrs.get("skin_types")
    if not isinstance(skin_types, list) or not skin_types:
        errors.append("Invalid skin_types: must be a non-empty list")
    else:
        invalid_skin = [s for s in skin_types if s not in ALLOWED_SKIN_TYPES]
        if invalid_skin:
            errors.append(f"Invalid skin_types values: {invalid_skin}")

    benefits = attrs.get("benefits")
    if not isinstance(benefits, list) or not benefits:
        errors.append("Invalid benefits: must be a non-empty list")

    key_ingredients = attrs.get("key_ingredients")
    if not isinstance(key_ingredients, list) or not key_ingredients:
        errors.append("Invalid key_ingredients: must be a non-empty list")

    return ValidationResult(is_valid=not errors, errors=errors)