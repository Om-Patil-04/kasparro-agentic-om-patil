from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation_schema.validator import validate_data_model
from product_narrative_agents.parser_agent import execute as parse
from product_narrative_agents.question_generator_agent import execute as gen_questions
from product_narrative_agents.qa_matcher_agent import execute as match_qa
from product_narrative_agents.logic_block_composer_agent import execute as compose_blocks
from product_narrative_agents.template_engine_agent import execute as render_pages
from product_narrative_agents.output_formatter_agent import execute as format_output


def main():
    raw_a = {
        "id": "sku-123",
        "name": "Glow Serum",
        "concentration": "10% Vitamin C",
        "price": "₹999",
        "skin_types": "Oily, Sensitive",
        "benefits": "Brightening, Even tone",
        "key_ingredients": "Vitamin C, Ferulic acid",
        "side_effects": "Mild tingling",
        "usage": "Apply 2-3 drops daily",
    }

    raw_b = {
        "id": "sku-b",
        "name": "Product B",
        "price": "₹799",
        "key_ingredients": "Niacinamide, Hyaluronic Acid",
        "benefits": "Hydration, Barrier support",
        "skin_types": "Normal, Dry",
    }

    dm_a = parse(raw_a)
    dm_b = parse(raw_b)

    print("Validation (Product A):", validate_data_model(dm_a))

    questions = gen_questions(dm_a)
    answers = match_qa(questions, dm_a, dm_b)
    blocks = compose_blocks(dm_a, dm_b)
    pages = render_pages(blocks, answers, dm_a, dm_b)
    output = format_output(pages)

    for fname, data in output.items():
        print(f"\n--- {fname} ---")
        # ensure_ascii=False to show ₹ instead of \u20b9
        print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()