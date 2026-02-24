"""Loads YAML value sets for reference data."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class ValueSetLoader:
    def __init__(self) -> None:
        self._sets: dict[str, list[dict[str, Any]]] = {}

    def load_from_directory(self, directory: str | Path) -> int:
        directory = Path(directory)
        count = 0
        if not directory.exists():
            return 0

        for filepath in sorted(directory.glob("*.yaml")):
            try:
                with open(filepath) as f:
                    data = yaml.safe_load(f) or {}
                name = filepath.stem
                if isinstance(data, dict) and "values" in data:
                    self._sets[name] = data["values"]
                elif isinstance(data, list):
                    self._sets[name] = data
                count += 1
            except Exception:
                pass
        return count

    def get(self, name: str) -> list[dict[str, Any]]:
        return self._sets.get(name, [])

    def list_sets(self) -> list[str]:
        return list(self._sets.keys())
