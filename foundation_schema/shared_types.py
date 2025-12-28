from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List


class Category(str, Enum):
    INFORMATIONAL = "Informational"
    SUITABILITY = "Suitability"
    BENEFITS = "Benefits"
    USAGE = "Usage"
    SAFETY = "Safety"
    PURCHASE = "Purchase"
    COMPARISON = "Comparison"


@dataclass
class DataModel:
    id: str
    attributes: Dict[str, Any]


@dataclass
class Question:
    question: str
    category: Category
    source_fields: List[str]


@dataclass
class Answer:
    question: str
    answer: str
    category: Category
    confidence: float
    source_fields: List[str]


@dataclass
class LogicBlock:
    block_id: str
    payload: Any
    source_fields: List[str]
    confidence: float
    generated_at: str


@dataclass
class Meta:
    version: str
    generated_at: str
    orchestrator: str
    blocks_used: List[str]
    source_product: str


@dataclass
class TemplateResult:
    page_type: str
    content: Dict[str, Any]
    meta: Meta