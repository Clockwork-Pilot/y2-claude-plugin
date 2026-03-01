#!/usr/bin/env python3
"""Document model for structured JSON storage with Pydantic validation."""

from typing import Any, Dict, Optional, Literal
from pydantic import BaseModel


class Doc(BaseModel):
    """Document node with type-based extensibility and optional children."""

    id: str
    label: str
    type: Literal["Doc"] = "Doc"
    metadata: Dict[str, Any] = {}
    children: Optional[Dict[str, "Doc"]] = None


Doc.model_rebuild()
