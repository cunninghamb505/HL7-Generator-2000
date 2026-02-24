"""RXG (Pharmacy/Treatment Give) segment builder."""

from __future__ import annotations


def build_rxg(
    give_code: str,
    give_name: str,
    give_amount: str,
    give_units: str,
    coding_system: str = "NDC",
    set_id: int = 1,
    sub_id: int = 1,
) -> str:
    """Build RXG segment."""
    drug = f"{give_code}^{give_name}^{coding_system}"

    fields = [
        "RXG",
        str(set_id),       # RXG.1 Give Sub-ID Counter
        str(sub_id),       # RXG.2 Dispense Sub-ID Counter
        "",                # RXG.3 Quantity/Timing
        drug,              # RXG.4 Give Code
        give_amount,       # RXG.5 Give Amount - Minimum
        give_amount,       # RXG.6 Give Amount - Maximum
        give_units,        # RXG.7 Give Units
    ]
    return "|".join(fields)
