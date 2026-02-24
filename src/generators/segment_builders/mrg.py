"""MRG (Merge) segment builder."""

from __future__ import annotations


def build_mrg(
    prior_mrn: str,
    prior_account: str = "",
    prior_visit: str = "",
    prior_name: str = "",
) -> str:
    """Build MRG segment for patient merge events."""
    fields = [
        "MRG",
        f"{prior_mrn}^^^MRN^MR",  # MRG.1 Prior Patient Identifier List
        "",                        # MRG.2 Prior Alternate Patient ID
        prior_account,             # MRG.3 Prior Patient Account Number
        "",                        # MRG.4 Prior Patient ID
        prior_visit,               # MRG.5 Prior Visit Number
        "",                        # MRG.6 Prior Alternate Visit ID
        prior_name,                # MRG.7 Prior Patient Name
    ]
    return "|".join(fields)
