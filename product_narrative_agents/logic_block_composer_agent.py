from __future__ import annotations

from typing import List

from foundation_schema.shared_types import DataModel, LogicBlock


def execute(dm: DataModel, product_b: DataModel) -> List[LogicBlock]:
    blocks: List[LogicBlock] = []
    attrs = dm.attributes
    source_product = attrs.get("name", dm.id)

    def add_block(block_id: str, payload, source_fields, confidence: float = 1.0, dependencies=None):
        blocks.append(
            LogicBlock(
                block_id=block_id,
                payload={
                    "payload": payload,
                    "dependencies": dependencies or [],
                    "source_product": source_product,
                },
                source_fields=source_fields,
                confidence=confidence,
                generated_at="",
            )
        )

    if "benefits" in attrs:
        add_block("benefits_block", attrs.get("benefits", []), ["benefits"])
    if "usage" in attrs:
        add_block("usage_block", attrs.get("usage"), ["usage"])
    if "side_effects" in attrs:
        add_block("safety_block", attrs.get("side_effects", []), ["side_effects"])
    if "price" in attrs:
        add_block("pricing_block", attrs.get("price"), ["price"])
    if "key_ingredients" in attrs:
        add_block("ingredients_block", attrs.get("key_ingredients", []), ["key_ingredients"])

    highlights = []
    if attrs.get("concentration"):
        highlights.append(f"{attrs['concentration']} for brightening")
    if attrs.get("key_ingredients"):
        highlights.append(f"Contains {attrs['key_ingredients'][0]}")
    if attrs.get("benefits"):
        highlights.append(attrs["benefits"][0])
    if attrs.get("skin_types"):
        highlights.append(f"Suitable for {', '.join(attrs['skin_types'])} skin")
    highlights = highlights[:4]
    add_block("highlights_block", highlights, ["concentration", "key_ingredients", "benefits", "skin_types"], confidence=0.8)

    comp_payload = {
        "price": {"product_a": attrs.get("price"), "product_b": product_b.attributes.get("price")},
        "ingredients": {
            "product_a": attrs.get("key_ingredients", []),
            "product_b": product_b.attributes.get("key_ingredients", []),
        },
        "benefits": {
            "product_a": attrs.get("benefits", []),
            "product_b": product_b.attributes.get("benefits", []),
        },
        "suitability": {
            "product_a": attrs.get("skin_types", []),
            "product_b": product_b.attributes.get("skin_types", []),
        },
    }
    add_block("comparison_block", comp_payload, ["price", "key_ingredients", "benefits", "skin_types"], confidence=0.7)

    return blocks