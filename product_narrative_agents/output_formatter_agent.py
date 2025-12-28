from __future__ import annotations

import json
from typing import Dict, Any

from foundation_schema.shared_types import TemplateResult


def _to_dict(result: TemplateResult) -> Dict[str, Any]:
    return {
        "page_type": result.page_type,
        "content": result.content,
        "meta": {
            "version": result.meta.version,
            "generated_at": result.meta.generated_at,
            "orchestrator": result.meta.orchestrator,
            "blocks_used": result.meta.blocks_used,
            "source_product": result.meta.source_product,
        },
    }


def execute(pages: Dict[str, TemplateResult]) -> Dict[str, Any]:
    output: Dict[str, Any] = {}
    for key, page in pages.items():
        data = _to_dict(page)
        json.dumps(data)  # ensure serializable
        filename = f"{key}.json" if not key.endswith(".json") else key
        output[filename] = data
    return output