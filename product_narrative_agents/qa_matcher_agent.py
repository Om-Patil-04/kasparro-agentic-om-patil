from __future__ import annotations

from typing import List

from foundation_schema.shared_types import Answer, Category, DataModel


def _find_field_source(question_text: str) -> str:
    mapping = {
        "concentration": "concentration",
        "ingredient": "key_ingredients",
        "key ingredients": "key_ingredients",
        "benefit": "benefits",
        "price": "price",
        "apply": "usage",
        "side effect": "side_effects",
        "suitable": "skin_types",
        "compare": "comparison",
        "name": "name",
    }
    lower_q = question_text.lower()
    for key, field in mapping.items():
        if key in lower_q:
            return field
    return ""


def _answer_suitability(question: str, dm: DataModel) -> str:
    skin_types = dm.attributes.get("skin_types", [])
    for st in skin_types:
        if st.lower() in question.lower():
            return f"Yes, suitable for {st} skin."
    return "Not specified."


def _answer_comparison(dm_a: DataModel, dm_b: DataModel) -> str:
    price_a = dm_a.attributes.get("price", "Not specified")
    price_b = dm_b.attributes.get("price", "Not specified")
    ingredients_a = ", ".join(dm_a.attributes.get("key_ingredients", []) or []) or "Not specified"
    ingredients_b = ", ".join(dm_b.attributes.get("key_ingredients", []) or []) or "Not specified"
    benefits_a = ", ".join(dm_a.attributes.get("benefits", []) or []) or "Not specified"
    benefits_b = ", ".join(dm_b.attributes.get("benefits", []) or []) or "Not specified"
    skin_a = ", ".join(dm_a.attributes.get("skin_types", []) or []) or "Not specified"
    skin_b = ", ".join(dm_b.attributes.get("skin_types", []) or []) or "Not specified"
    return (
        f"Product A price: {price_a}; Product B price: {price_b}. "
        f"Ingredients A: {ingredients_a}; B: {ingredients_b}. "
        f"Benefits A: {benefits_a}; B: {benefits_b}. "
        f"Suitability A: {skin_a}; B: {skin_b}."
    )


def _answer_contains(question: str, values: List[str]) -> str:
    q_lower = question.lower()
    for v in values:
        if v.lower() in q_lower:
            return f"Yes, it contains {v}."
    return "Not specified."


def _answer_help_with(question: str, values: List[str]) -> str:
    q_lower = question.lower()
    for v in values:
        if v.lower() in q_lower:
            return f"Yes, it helps with {v}."
    return ", ".join(values) if values else "Not specified."


def execute(questions: List[Answer] | List, dm: DataModel, product_b: DataModel) -> List[Answer]:
    answers: List[Answer] = []
    attrs = dm.attributes

    for q in questions:
        q_text = q.question if hasattr(q, "question") else str(q)
        category = q.category if hasattr(q, "category") else Category.INFORMATIONAL
        source_fields = getattr(q, "source_fields", []) or []

        answer_text = "Not specified from provided data."
        confidence = 0.1
        lower_q = q_text.lower()

        if category == Category.COMPARISON:
            answer_text = _answer_comparison(dm, product_b)
            confidence = 0.7

        elif category == Category.SUITABILITY:
            answer_text = _answer_suitability(q_text, dm)
            confidence = 0.7 if "Not specified" not in answer_text else 0.3

        elif category == Category.SAFETY:
            side_effects = attrs.get("side_effects")
            if side_effects:
                answer_text = ", ".join(side_effects)
                confidence = 0.8

        elif category == Category.USAGE:
            usage = attrs.get("usage")
            if usage:
                answer_text = str(usage)
                confidence = 0.8

        elif category == Category.PURCHASE:
            price = attrs.get("price")
            if price:
                answer_text = str(price)
                confidence = 0.9

        elif category == Category.BENEFITS:
            benefits = attrs.get("benefits") or []
            if benefits:
                answer_text = _answer_help_with(q_text, benefits)
                confidence = 0.8  # bumped from 0.6 so the generic benefits question isn’t underconfident

        elif category == Category.INFORMATIONAL:
            if "concentration" in lower_q and attrs.get("concentration"):
                answer_text = attrs["concentration"]
                confidence = 0.85
            elif "what is" in lower_q and attrs.get("name"):
                answer_text = attrs["name"]
                confidence = 0.7
            elif "contain" in lower_q and attrs.get("key_ingredients"):
                answer_text = _answer_contains(q_text, attrs["key_ingredients"])
                confidence = 0.8 if "Yes" in answer_text else 0.3
            else:
                field = _find_field_source(q_text)
                value = attrs.get(field) if field else None
                if isinstance(value, list) and value:
                    answer_text = ", ".join(value)
                    confidence = 0.8
                elif value:
                    answer_text = str(value)
                    confidence = 0.8

        answers.append(
            Answer(
                question=q_text,
                answer=answer_text,
                category=category,
                confidence=confidence,
                source_fields=source_fields if source_fields else [_find_field_source(q_text)],
            )
        )
    return answers