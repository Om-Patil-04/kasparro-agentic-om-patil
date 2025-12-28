from __future__ import annotations

import json
import uuid
from typing import Any, Dict, List, Optional

from foundation_schema.validator import ValidationResult, validate_data_model
from product_b_config import PRODUCT_B
from product_narrative_agents.logic_block_composer_agent import execute as compose_blocks
from product_narrative_agents.output_formatter_agent import execute as format_output
from product_narrative_agents.parser_agent import execute as parse
from product_narrative_agents.qa_matcher_agent import execute as match_qa
from product_narrative_agents.question_generator_agent import execute as gen_questions
from product_narrative_agents.template_engine_agent import execute as render_pages


Message = Dict[str, Any]


def _make_msg(
    trace_id: str,
    agent_id: str,
    inp: Any,
    out: Any,
    success: bool,
    error: Optional[Dict[str, Any]] = None,
) -> Message:
    return {
        "trace_id": trace_id,
        "agent_id": agent_id,
        "input": inp,
        "output": out,
        "success": success,
        "error": error,
    }


def run(raw_input: Dict[str, Any], product_b_input: Dict[str, Any]) -> Dict[str, Any]:

    trace_id = str(uuid.uuid4())
    messages: List[Message] = []

    try:
        dm_a = parse(raw_input)
        messages.append(_make_msg(trace_id, "parser_agent:A", {"raw": raw_input}, {"dm": "parsed"}, True))
    except Exception as e:
        err = {"message": str(e), "stage": "parse"}
        messages.append(_make_msg(trace_id, "parser_agent:A", {"raw": raw_input}, None, False, err))
        return {"trace_id": trace_id, "success": False, "messages": messages, "error": err}

    try:
        dm_b = parse(product_b_input)
        messages.append(_make_msg(trace_id, "parser_agent:B", {"raw": product_b_input}, {"dm": "parsed"}, True))
    except Exception as e:
        dm_b = None
        err = {"message": f"product_b parse failed: {e}", "stage": "parse_b"}
        messages.append(_make_msg(trace_id, "parser_agent:B", {"raw": product_b_input}, None, False, err))

    try:
        validation: ValidationResult = validate_data_model(dm_a)
        messages.append(
            _make_msg(
                trace_id,
                "validator",
                {"dm": "parsed"},
                {"is_valid": validation.is_valid, "errors": validation.errors},
                True,
            )
        )
        if not validation.is_valid:
            err = {"message": f"Validation failed: {validation.errors}", "stage": "validate"}
            return {"trace_id": trace_id, "success": False, "messages": messages, "error": err}
    except Exception as e:
        err = {"message": str(e), "stage": "validate"}
        messages.append(_make_msg(trace_id, "validator", {"dm": "parsed"}, None, False, err))
        return {"trace_id": trace_id, "success": False, "messages": messages, "error": err}

    try:
        questions = gen_questions(dm_a)
        messages.append(_make_msg(trace_id, "question_generator_agent", {"dm": "parsed"}, {"count": len(questions)}, True))
    except Exception as e:
        err = {"message": str(e), "stage": "question_gen"}
        messages.append(_make_msg(trace_id, "question_generator_agent", {"dm": "parsed"}, None, False, err))
        return {"trace_id": trace_id, "success": False, "messages": messages, "error": err}

    try:
        answers = match_qa(questions, dm_a, dm_b) if dm_b is not None else match_qa(questions, dm_a, dm_a)
        messages.append(_make_msg(trace_id, "qa_matcher_agent", {"questions": len(questions)}, {"answers": len(answers)}, True))
    except Exception as e:
        err = {"message": str(e), "stage": "qa_matcher"}
        messages.append(_make_msg(trace_id, "qa_matcher_agent", {"questions": len(questions)}, None, False, err))
        return {"trace_id": trace_id, "success": False, "messages": messages, "error": err}

    try:
        blocks = compose_blocks(dm_a, dm_b if dm_b is not None else dm_a)
        block_ids = [b.block_id for b in blocks]
        messages.append(
            _make_msg(
                trace_id,
                "logic_block_composer_agent",
                {"dm_a": True, "dm_b": dm_b is not None},
                {"blocks": block_ids},
                True,
            )
        )
    except Exception as e:
        blocks = []
        block_ids = []
        err = {"message": f"compose failed, continuing with empty blocks: {e}", "stage": "logic_block_composer"}
        messages.append(
            _make_msg(
                trace_id,
                "logic_block_composer_agent",
                {"dm_a": True, "dm_b": dm_b is not None},
                {"blocks": block_ids},
                False,
                err,
            )
        )

    try:
        pages = render_pages(blocks, answers, dm_a, dm_b if dm_b is not None else dm_a)
        messages.append(_make_msg(trace_id, "template_engine_agent", {"blocks": len(blocks)}, {"pages": len(pages)}, True))
    except Exception as e:
        pages = {}
        err = {"message": f"template render failed, continuing with empty pages: {e}", "stage": "template_engine"}
        messages.append(_make_msg(trace_id, "template_engine_agent", {"blocks": len(blocks)}, {"pages": 0}, False, err))

    try:
        output = format_output(pages)
        messages.append(_make_msg(trace_id, "output_formatter_agent", {"pages": len(pages)}, {"files": list(output.keys())}, True))
    except Exception as e:
        output = {}
        err = {"message": f"output formatting failed, returning empty output: {e}", "stage": "output_formatter"}
        messages.append(_make_msg(trace_id, "output_formatter_agent", {"pages": len(pages)}, {"files": []}, False, err))

    return {"trace_id": trace_id, "success": True, "messages": messages, "result": output}


if __name__ == "__main__":
    raw_a = {
        "name": "GlowBoost Vitamin C Serum",
        "concentration": "10% Vitamin C",
        "skin_types": "Oily, Combination",
        "key_ingredients": "Vitamin C, Hyaluronic Acid",
        "benefits": "Brightening, Fades dark spots",
        "usage": "Apply 2–3 drops in the morning before sunscreen",
        "side_effects": "Mild tingling for sensitive skin",
        "price": "₹699",
    }
    raw_b = PRODUCT_B

    result = run(raw_a, raw_b)
    print("TRACE:", result["trace_id"])
    print("SUCCESS:", result["success"])
    for m in result["messages"]:
        print(json.dumps(m, indent=2, ensure_ascii=False, default=str))
    if "result" in result:
        for fname, data in result["result"].items():
            print(f"\n--- {fname} ---")
            print(json.dumps(data, indent=2, ensure_ascii=False, default=str))