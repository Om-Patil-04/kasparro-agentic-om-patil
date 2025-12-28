from __future__ import annotations

from typing import List, Set

from foundation_schema.shared_types import Category, DataModel, Question


def execute(dm: DataModel) -> List[Question]:
    attrs = dm.attributes
    name = attrs.get("name", "the product")

    questions: List[Question] = []
    seen: Set[str] = set()

    def add(q: str, category: Category, sources: List[str]):
        if q in seen:
            return
        seen.add(q)
        questions.append(Question(question=q, category=category, source_fields=sources))

    add(f"What is {name}?", Category.INFORMATIONAL, ["name"])
    if "concentration" in attrs:
        add(f"What is the Vitamin C concentration in {name}?", Category.INFORMATIONAL, ["concentration", "name"])
    if "key_ingredients" in attrs:
        add(f"What are the key ingredients in {name}?", Category.INFORMATIONAL, ["key_ingredients", "name"])
        for ki in attrs.get("key_ingredients", [])[:4]:
            add(f"Does {name} contain {ki}?", Category.INFORMATIONAL, ["key_ingredients", "name"])
    if "benefits" in attrs:
        add(f"What benefits does {name} offer?", Category.BENEFITS, ["benefits", "name"])
        for benefit in attrs.get("benefits", [])[:5]:
            add(f"Does {name} help with {benefit}?", Category.BENEFITS, ["benefits", "name"])
    if "usage" in attrs:
        add(f"How should I apply {name}?", Category.USAGE, ["usage", "name"])
    if "side_effects" in attrs:
        add(f"Can {name} cause any side effects?", Category.SAFETY, ["side_effects", "name"])
    if "price" in attrs:
        add(f"What is the price of {name}?", Category.PURCHASE, ["price", "name"])
    if "skin_types" in attrs:
        for st in attrs.get("skin_types", [])[:5]:
            add(f"Is {name} suitable for {st} skin?", Category.SUITABILITY, ["skin_types", "name"])

    add(f"How does {name} compare to Product B on ingredients?", Category.COMPARISON, ["key_ingredients", "name"])

    fillers = [
        (f"Is {name} suitable for daily use?", Category.USAGE, ["usage", "name"]),
        (f"Is {name} fragrance-free?", Category.SAFETY, ["side_effects", "name"]),
        (f"Does {name} help with hydration?", Category.BENEFITS, ["benefits", "name"]),
        (f"How long before seeing results with {name}?", Category.USAGE, ["usage", "benefits", "name"]),
        (f"Can I use {name} with sunscreen?", Category.USAGE, ["usage", "name"]),
    ]
    for q, cat, sources in fillers:
        if len(questions) >= 15:
            break
        add(q, cat, sources)

    while len(questions) < 15:
        add(f"What else should I know about {name}?", Category.INFORMATIONAL, ["name"])

    return questions