"""HL7 timestamp formatting, escaping, and utility functions."""

from __future__ import annotations

from datetime import date, datetime


def format_timestamp(dt: datetime | None = None, precision: str = "full") -> str:
    """Format a datetime to HL7 timestamp format.

    precision: 'full' = YYYYMMDDHHmmss, 'date' = YYYYMMDD, 'minute' = YYYYMMDDHHmm
    """
    if dt is None:
        dt = datetime.now()
    if precision == "date":
        return dt.strftime("%Y%m%d")
    if precision == "minute":
        return dt.strftime("%Y%m%d%H%M")
    return dt.strftime("%Y%m%d%H%M%S")


def format_date(d: date | None) -> str:
    if d is None:
        return ""
    return d.strftime("%Y%m%d")


def escape_hl7(text: str) -> str:
    """Escape special HL7 characters."""
    if not text:
        return text
    text = text.replace("\\", "\\E\\")
    text = text.replace("|", "\\F\\")
    text = text.replace("^", "\\S\\")
    text = text.replace("&", "\\T\\")
    text = text.replace("~", "\\R\\")
    return text


def build_coded_element(code: str, description: str, coding_system: str = "") -> str:
    """Build a CE (coded element) field: code^description^coding_system."""
    return f"{code}^{description}^{coding_system}"


def build_extended_composite_name(
    family: str, given: str, middle: str = "",
    suffix: str = "", prefix: str = "",
    degree: str = "", name_type: str = "L"
) -> str:
    """Build an XPN field."""
    return f"{family}^{given}^{middle}^{suffix}^{prefix}^{degree}^{name_type}"
