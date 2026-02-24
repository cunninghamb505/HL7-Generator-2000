"""ZPD (Custom/Z-Segment) segment builder."""

from __future__ import annotations


def build_zpd(**kwargs: str) -> str:
    """Build a custom ZPD segment with arbitrary fields."""
    fields = ["ZPD"]
    for key in sorted(kwargs.keys()):
        fields.append(kwargs[key])
    return "|".join(fields)
