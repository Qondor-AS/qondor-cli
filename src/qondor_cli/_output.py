"""Output formatting: JSON-first for AI agent consumption."""

from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel


def format_output(data: Any, *, raw: bool = False) -> str:
    """Format SDK model(s) as JSON string.

    - Single model: pretty-printed JSON (or compact with raw=True)
    - List of models: JSON array
    - None: empty string (for void operations like delete)
    """
    if data is None:
        return ""

    if isinstance(data, list):
        serialized = [_dump(item) for item in data]
    else:
        serialized = _dump(data)

    if raw:
        return json.dumps(serialized, ensure_ascii=False)
    return json.dumps(serialized, indent=2, ensure_ascii=False)


def _dump(obj: Any) -> Any:
    if isinstance(obj, BaseModel):
        return obj.model_dump(mode="json", by_alias=True)
    return obj
