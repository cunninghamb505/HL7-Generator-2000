"""Tests for message validation."""

from src.validators.message_validator import validate_message, ValidationResult


def _make_adt_a01():
    """Create a valid ADT^A01 message."""
    segments = [
        "MSH|^~\\&|HIS|GENERAL_HOSPITAL|||20240101120000||ADT^A01|MSG001|P|2.5.1",
        "EVN|A01|20240101120000",
        "PID|||MRN001||Doe^John||19800101|M",
        "PV1||I|ICU-01",
    ]
    return "\r".join(segments)


def _make_orm_o01():
    """Create a valid ORM^O01 message."""
    segments = [
        "MSH|^~\\&|HIS|GENERAL_HOSPITAL|||20240101120000||ORM^O01|MSG002|P|2.5.1",
        "PID|||MRN001||Doe^John||19800101|M",
        "ORC|NW|ORD001",
        "OBR||||CBC^Complete Blood Count",
    ]
    return "\r".join(segments)


def test_validate_valid_adt():
    result = validate_message(_make_adt_a01())
    assert result.valid is True
    assert len(result.errors) == 0


def test_validate_valid_orm():
    result = validate_message(_make_orm_o01())
    assert result.valid is True
    assert len(result.errors) == 0


def test_validate_empty_message():
    result = validate_message("")
    assert result.valid is False
    assert "Empty message" in result.errors


def test_validate_missing_msh():
    result = validate_message("PID|||MRN001||Doe^John")
    assert result.valid is False
    assert "First segment must be MSH" in result.errors


def test_validate_missing_required_segment():
    # ADT^A01 without EVN segment
    msg = "\r".join([
        "MSH|^~\\&|HIS|GENERAL_HOSPITAL|||20240101120000||ADT^A01|MSG001|P|2.5.1",
        "PID|||MRN001||Doe^John||19800101|M",
        "PV1||I|ICU-01",
    ])
    result = validate_message(msg)
    assert result.valid is False
    assert any("EVN" in e for e in result.errors)


def test_validate_missing_required_field():
    # PID without patient ID (field 3)
    msg = "\r".join([
        "MSH|^~\\&|HIS|GENERAL_HOSPITAL|||20240101120000||ADT^A01|MSG001|P|2.5.1",
        "EVN|A01|20240101120000",
        "PID|||||Doe^John||19800101|M",
        "PV1||I|ICU-01",
    ])
    result = validate_message(msg)
    assert result.valid is False
    assert any("PID.3" in e for e in result.errors)


def test_validate_unknown_message_type():
    msg = "\r".join([
        "MSH|^~\\&|HIS|GENERAL_HOSPITAL|||20240101120000||XYZ^X01|MSG001|P|2.5.1",
    ])
    result = validate_message(msg)
    # Unknown type should not be invalid, just warned
    assert result.valid is True
    assert any("No validation rules" in w for w in result.warnings)


def test_validate_z_segment_warning():
    msg = _make_adt_a01() + "\rZPD|CARDIO|5|Y"
    result = validate_message(msg)
    assert result.valid is True
    assert any("Z-segments" in w for w in result.warnings)


def test_validate_oru_r01():
    msg = "\r".join([
        "MSH|^~\\&|HIS|GENERAL_HOSPITAL|||20240101120000||ORU^R01|MSG003|P|2.5.1",
        "PID|||MRN001||Doe^John||19800101|M",
        "OBR||||CBC^Complete Blood Count",
        "OBX||NM|WBC^White Blood Count||7.5|10*3/uL",
    ])
    result = validate_message(msg)
    assert result.valid is True


def test_validate_ack():
    msg = "\r".join([
        "MSH|^~\\&|HIS|GENERAL_HOSPITAL|||20240101120000||ACK|MSG004|P|2.5.1",
        "MSA|AA|MSG001",
    ])
    result = validate_message(msg)
    assert result.valid is True


def test_validation_result_to_dict():
    result = ValidationResult(valid=False, errors=["Missing PID"], warnings=["Has Z-segments"])
    d = result.to_dict()
    assert d["valid"] is False
    assert "Missing PID" in d["errors"]
    assert "Has Z-segments" in d["warnings"]


def test_validate_explicit_message_type():
    # Pass message type explicitly even if MSH.9 is different
    msg = _make_adt_a01()
    result = validate_message(msg, message_type="ADT")
    assert result.valid is True
