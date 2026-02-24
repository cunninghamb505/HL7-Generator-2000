"""HL7 message structural validator."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.validators.rules import RULES


@dataclass
class ValidationResult:
    valid: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
        }


def validate_message(raw_message: str, message_type: str = "") -> ValidationResult:
    """Validate an HL7 message for structural correctness.

    Checks: MSH present, required segments, field counts, required fields.
    """
    result = ValidationResult()

    if not raw_message or not raw_message.strip():
        result.valid = False
        result.errors.append("Empty message")
        return result

    segments = raw_message.strip().split("\r")

    # Parse segments into a dict of name -> list of field arrays
    parsed: dict[str, list[list[str]]] = {}
    for seg_str in segments:
        if not seg_str.strip():
            continue
        fields = seg_str.split("|")
        seg_name = fields[0]
        if seg_name not in parsed:
            parsed[seg_name] = []
        parsed[seg_name].append(fields)

    # MSH must be first
    first_seg = segments[0].split("|")[0] if segments else ""
    if first_seg != "MSH":
        result.valid = False
        result.errors.append("First segment must be MSH")
        return result

    # Determine message type from MSH.9 if not provided
    if not message_type:
        msh_fields = parsed.get("MSH", [[]])[0]
        if len(msh_fields) > 8:
            # MSH.9 = Message Type, e.g., "ADT^A04"
            msg_type_field = msh_fields[8]
            message_type = msg_type_field.split("^")[0] if msg_type_field else ""

    message_type = message_type.upper()
    rules = RULES.get(message_type)

    if not rules:
        result.warnings.append(f"No validation rules defined for message type '{message_type}'")
        return result

    # Check required segments
    for req_seg in rules.get("required_segments", []):
        if req_seg not in parsed:
            result.valid = False
            result.errors.append(f"Missing required segment: {req_seg}")

    # Check field rules
    for field_ref, field_rule in rules.get("field_rules", {}).items():
        seg_name, field_idx_str = field_ref.split(".")
        field_idx = int(field_idx_str)

        if seg_name not in parsed:
            continue  # already flagged as missing segment

        seg_fields = parsed[seg_name][0]  # check first occurrence

        # MSH is special: MSH.1 = field separator, MSH.2 = encoding chars
        # So MSH.9 is actually index 8 in the split array
        if seg_name == "MSH":
            actual_idx = field_idx - 1
        else:
            actual_idx = field_idx

        if actual_idx >= len(seg_fields):
            if field_rule.get("required"):
                result.valid = False
                desc = field_rule.get("description", field_ref)
                result.errors.append(f"Missing required field {field_ref} ({desc})")
        elif not seg_fields[actual_idx].strip():
            if field_rule.get("required"):
                result.valid = False
                desc = field_rule.get("description", field_ref)
                result.errors.append(f"Empty required field {field_ref} ({desc})")

    # Check for Z-segments (informational)
    z_segs = [name for name in parsed if name.startswith("Z")]
    if z_segs:
        result.warnings.append(f"Contains custom Z-segments: {', '.join(z_segs)}")

    return result
