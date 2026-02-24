"""Dynamic Z-segment engine: loads definitions from YAML and builds segments at runtime."""

from __future__ import annotations

import random
from pathlib import Path
from typing import Any

import yaml
from faker import Faker

_faker = Faker()


def load_z_segments(path: str | Path) -> list[dict[str, Any]]:
    """Load Z-segment definitions from a YAML file.

    Returns a list of segment definitions, each with name, attach_to, and fields.
    """
    path = Path(path)
    if not path.exists():
        return []

    with open(path) as f:
        data = yaml.safe_load(f) or {}

    return data.get("segments", [])


def build_z_segment(definition: dict[str, Any]) -> str:
    """Build a pipe-delimited Z-segment string from its definition."""
    name = definition["name"]
    fields_defs = sorted(definition.get("fields", []), key=lambda f: f.get("position", 0))

    # Determine how many field slots we need
    max_pos = max((f.get("position", 0) for f in fields_defs), default=0)
    values = [""] * max_pos

    for fdef in fields_defs:
        pos = fdef.get("position", 1) - 1  # 1-indexed to 0-indexed
        if pos < 0:
            continue
        values[pos] = _resolve_field_value(fdef)

    return "|".join([name] + values)


def _resolve_field_value(fdef: dict[str, Any]) -> str:
    """Resolve a field definition to a concrete string value."""
    # Static value
    if "value" in fdef:
        return str(fdef["value"])

    field_type = fdef.get("type", "")

    if field_type == "random_int":
        lo = fdef.get("min", 0)
        hi = fdef.get("max", 100)
        return str(random.randint(lo, hi))

    if field_type == "random_choice":
        choices = fdef.get("choices", [])
        return random.choice(choices) if choices else ""

    if field_type.startswith("faker_"):
        faker_method = field_type[6:]  # strip "faker_" prefix
        fn = getattr(_faker, faker_method, None)
        if callable(fn):
            return str(fn())
        return ""

    return ""


def get_z_segments_for_type(
    definitions: list[dict[str, Any]], message_type: str
) -> list[str]:
    """Build all Z-segments that should be attached to a given message type."""
    results = []
    mt = message_type.upper()
    for defn in definitions:
        attach_to = [t.upper() for t in defn.get("attach_to", [])]
        if mt in attach_to:
            results.append(build_z_segment(defn))
    return results
