"""OBR (Observation Request) segment builder."""

from __future__ import annotations

from datetime import datetime

from src.core.patient import Order
from src.utils.hl7_helpers import format_timestamp


def build_obr(
    order: Order,
    set_id: int = 1,
    ordering_provider_id: str = "",
    ordering_provider_name: str = "",
    result_status: str = "",
    timestamp: datetime | None = None,
) -> str:
    """Build OBR segment."""
    ts = format_timestamp(timestamp)
    provider = ""
    if ordering_provider_id:
        provider = f"{ordering_provider_id}^{ordering_provider_name}"

    order_code = f"{order.order_code}^{order.order_name}"

    fields = [
        "OBR",
        str(set_id),                      # OBR.1 Set ID
        order.placer_order_number,        # OBR.2 Placer Order Number
        order.filler_order_number,        # OBR.3 Filler Order Number
        order_code,                       # OBR.4 Universal Service Identifier
        order.priority,                   # OBR.5 Priority
        ts,                               # OBR.6 Requested Date/Time
        ts,                               # OBR.7 Observation Date/Time
        "",                               # OBR.8 Observation End Date/Time
        "",                               # OBR.9 Collection Volume
        "",                               # OBR.10 Collector Identifier
        "",                               # OBR.11 Specimen Action Code
        "",                               # OBR.12 Danger Code
        "",                               # OBR.13 Relevant Clinical Info
        "",                               # OBR.14 Specimen Received Date/Time
        "",                               # OBR.15 Specimen Source
        provider,                         # OBR.16 Ordering Provider
        "",                               # OBR.17 Order Callback Phone
        "",                               # OBR.18 Placer Field 1
        "",                               # OBR.19 Placer Field 2
        "",                               # OBR.20 Filler Field 1
        "",                               # OBR.21 Filler Field 2
        ts if result_status else "",      # OBR.22 Results Rpt/Status Chng Date
        "",                               # OBR.23 Charge to Practice
        "",                               # OBR.24 Diagnostic Service Section ID
        result_status,                    # OBR.25 Result Status
    ]
    return "|".join(fields)
