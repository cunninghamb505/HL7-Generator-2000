"""ORC (Common Order) segment builder."""

from __future__ import annotations

from datetime import datetime

from src.core.patient import Order
from src.utils.hl7_helpers import format_timestamp


def build_orc(
    order: Order,
    order_control: str = "NW",
    ordering_provider_id: str = "",
    ordering_provider_name: str = "",
    timestamp: datetime | None = None,
) -> str:
    """Build ORC segment.

    order_control: NW=New, SC=Status Changed, CA=Cancel, etc.
    """
    ts = format_timestamp(timestamp)
    provider = ""
    if ordering_provider_id:
        provider = f"{ordering_provider_id}^{ordering_provider_name}"

    fields = [
        "ORC",
        order_control,                    # ORC.1 Order Control
        order.placer_order_number,        # ORC.2 Placer Order Number
        order.filler_order_number,        # ORC.3 Filler Order Number
        "",                               # ORC.4 Placer Group Number
        order.status,                     # ORC.5 Order Status
        "",                               # ORC.6 Response Flag
        "",                               # ORC.7 Quantity/Timing
        "",                               # ORC.8 Parent
        ts,                               # ORC.9 Date/Time of Transaction
        "",                               # ORC.10 Entered By
        "",                               # ORC.11 Verified By
        provider,                         # ORC.12 Ordering Provider
        "",                               # ORC.13 Enterer's Location
        "",                               # ORC.14 Call Back Phone Number
        ts,                               # ORC.15 Order Effective Date/Time
    ]
    return "|".join(fields)
