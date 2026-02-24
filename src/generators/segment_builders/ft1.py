"""FT1 (Financial Transaction) segment builder."""

from __future__ import annotations

from datetime import datetime

from src.utils.hl7_helpers import format_timestamp


def build_ft1(
    set_id: int = 1,
    transaction_id: str = "",
    transaction_date: datetime | None = None,
    transaction_type: str = "CG",
    transaction_code: str = "",
    transaction_description: str = "",
    transaction_amount: str = "",
    quantity: str = "1",
    department_code: str = "",
    insurance_plan: str = "",
    diagnosis_code: str = "",
    performed_by: str = "",
    ordering_provider: str = "",
) -> str:
    """Build FT1 segment.

    transaction_type: CG=Charge, CR=Credit, PA=Payment, AJ=Adjustment
    """
    ts = format_timestamp(transaction_date)
    tx_code = f"{transaction_code}^{transaction_description}" if transaction_code else ""

    fields = [
        "FT1",
        str(set_id),              # FT1.1 Set ID
        transaction_id,           # FT1.2 Transaction ID
        "",                       # FT1.3 Transaction Batch ID
        ts,                       # FT1.4 Transaction Date
        ts,                       # FT1.5 Transaction Posting Date
        transaction_type,         # FT1.6 Transaction Type
        tx_code,                  # FT1.7 Transaction Code
        "",                       # FT1.8 Transaction Description (deprecated)
        "",                       # FT1.9 Transaction Description - Alt
        quantity,                 # FT1.10 Transaction Quantity
        transaction_amount,       # FT1.11 Transaction Amount - Extended
        "",                       # FT1.12 Transaction Amount - Unit
        department_code,          # FT1.13 Department Code
        insurance_plan,           # FT1.14 Insurance Plan ID
        "",                       # FT1.15 Insurance Amount
        "",                       # FT1.16 Assigned Patient Location
        "",                       # FT1.17 Fee Schedule
        "",                       # FT1.18 Patient Type
        diagnosis_code,           # FT1.19 Diagnosis Code
        performed_by,             # FT1.20 Performed By Code
        ordering_provider,        # FT1.21 Ordered By Code
    ]
    return "|".join(fields)
