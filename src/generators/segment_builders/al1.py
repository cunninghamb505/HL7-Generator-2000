"""AL1 (Allergy) segment builder."""

from __future__ import annotations

from src.core.patient import Allergy


def build_al1(allergy: Allergy, set_id: int = 1) -> str:
    """Build AL1 segment from allergy data."""
    fields = [
        "AL1",
        str(set_id),                    # AL1.1 Set ID
        allergy.allergy_type,           # AL1.2 Allergen Type Code
        f"{allergy.code}^{allergy.description}",  # AL1.3 Allergen Code
        allergy.severity,               # AL1.4 Allergy Severity Code
        allergy.reaction,               # AL1.5 Allergy Reaction Code
    ]
    return "|".join(fields)


def build_al1_segments(allergies: list[Allergy]) -> list[str]:
    """Build AL1 segments for all patient allergies."""
    return [build_al1(a, i + 1) for i, a in enumerate(allergies)]
