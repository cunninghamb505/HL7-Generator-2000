"""OBX (Observation/Result) segment builder."""

from __future__ import annotations

from typing import Any

from src.utils.hl7_helpers import format_timestamp


def build_obx(
    set_id: int,
    value_type: str,
    observation_id: str,
    observation_name: str,
    value: Any,
    units: str = "",
    reference_range: str = "",
    abnormal_flag: str = "",
    result_status: str = "F",
    coding_system: str = "LN",
) -> str:
    """Build OBX segment.

    value_type: NM=Numeric, ST=String, TX=Text, CE=Coded Entry, FT=Formatted Text
    result_status: F=Final, P=Preliminary, C=Correction
    """
    obs_id = f"{observation_id}^{observation_name}^{coding_system}"

    fields = [
        "OBX",
        str(set_id),          # OBX.1 Set ID
        value_type,           # OBX.2 Value Type
        obs_id,               # OBX.3 Observation Identifier
        "",                   # OBX.4 Observation Sub-ID
        str(value),           # OBX.5 Observation Value
        units,                # OBX.6 Units
        reference_range,      # OBX.7 References Range
        abnormal_flag,        # OBX.8 Abnormal Flags
        "",                   # OBX.9 Probability
        "",                   # OBX.10 Nature of Abnormal Test
        result_status,        # OBX.11 Observation Result Status
    ]
    return "|".join(fields)
