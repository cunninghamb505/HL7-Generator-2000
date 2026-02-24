"""RXE (Pharmacy/Treatment Encoded Order) segment builder."""

from __future__ import annotations

from typing import Any

from src.utils.hl7_helpers import format_timestamp


def build_rxe(
    drug_code: str,
    drug_name: str,
    dose: str,
    dose_units: str,
    route: str = "PO",
    frequency: str = "",
    quantity: str = "",
    coding_system: str = "NDC",
    ordering_provider: str = "",
) -> str:
    """Build RXE segment for pharmacy encoded order."""
    drug = f"{drug_code}^{drug_name}^{coding_system}"

    fields = [
        "RXE",
        "",                     # RXE.1 Quantity/Timing
        drug,                   # RXE.2 Give Code
        dose,                   # RXE.3 Give Amount - Minimum
        dose,                   # RXE.4 Give Amount - Maximum
        dose_units,             # RXE.5 Give Units
        "",                     # RXE.6 Give Dosage Form
        "",                     # RXE.7 Provider's Administration Instructions
        "",                     # RXE.8 Deliver-To Location
        "",                     # RXE.9 Substitution Status
        quantity,               # RXE.10 Dispense Amount
        "",                     # RXE.11 Dispense Units
        "",                     # RXE.12 Number of Refills
        ordering_provider,      # RXE.13 Ordering Provider's DEA Number
        "",                     # RXE.14 Pharmacist/Treatment Supplier's Verifier ID
        "",                     # RXE.15 Prescription Number
        "",                     # RXE.16 Number of Refills Remaining
        "",                     # RXE.17 Number of Refills/Doses Dispensed
        "",                     # RXE.18 D/T of Most Recent Refill
        "",                     # RXE.19 Total Daily Dose
        "",                     # RXE.20 Needs Human Review
        "",                     # RXE.21 Pharmacy/Treatment Supplier's Special Dispensing
        "",                     # RXE.22 Give Per (Time Unit)
        "",                     # RXE.23 Give Rate Amount
        "",                     # RXE.24 Give Rate Units
        route,                  # RXE.25 -- non-standard position but common
    ]
    return "|".join(fields)
