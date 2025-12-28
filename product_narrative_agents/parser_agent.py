from __future__ import annotations

from typing import Any, Dict, List

from foundation_schema.shared_types import DataModel

ENUM_NORMALIZATION = {
    "informational": "Informational",
    "suitability": "Suitability",
    "benefits": "Benefits",
    "usage": "Usage",
    "safety": "Safety",
    "purchase": "Purchase",
    "comparison": "Comparison",
    "oily": "Oily",
    "dry": "Dry",
    "combination": "Combination",
    "sensitive": "Sensitive",
    "normal": "Normal",
}


def _trim(value: Any) -> Any:
    if isinstance(value, str):
        return value.strip()
    return value


def _split_to_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [_trim(v) for v in value if isinstance(v, str) and _trim(v)]
    if isinstance(value, str):
        parts = [p.strip() for p in value.split(",")]
        return [p for p in parts if p]
    return []


def _normalize_skin_types(values: List[str]) -> List[str]:
    normalized = []
    for v in values:
        key = v.strip().lower()
        normalized.append(ENUM_NORMALIZATION.get(key, v.strip()))
    return normalized


def _normalize_enums(value: str) -> str:
    key = value.strip().lower()
    return ENUM_NORMALIZATION.get(key, value.strip())


def execute(raw_input: Dict[str, Any]) -> DataModel:
    trimmed = {k: _trim(v) for k, v in raw_input.items()}

    skin_types = _normalize_skin_types(_split_to_list(trimmed.get("skin_types")))
    key_ingredients = _split_to_list(trimmed.get("key_ingredients"))
    benefits = _split_to_list(trimmed.get("benefits"))
    side_effects = _split_to_list(trimmed.get("side_effects"))

    attributes: Dict[str, Any] = {
        **{k: v for k, v in trimmed.items() if k not in {"skin_types", "key_ingredients", "benefits", "side_effects"}},
        "skin_types": skin_types,
        "key_ingredients": key_ingredients,
        "benefits": benefits,
        "side_effects": side_effects,
    }

    if "category" in attributes and isinstance(attributes["category"], str):
        attributes["category"] = _normalize_enums(attributes["category"])

    dm_id = str(attributes.get("id") or attributes.get("name") or raw_input.get("id") or "unknown")
    attributes.pop("id", None)

    return DataModel(id=dm_id, attributes=attributes)