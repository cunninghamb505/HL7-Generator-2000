"""Tests for patient timeline functionality."""

import time

from src.utils.message_log import LogEntry, MessageLog


def test_get_by_patient():
    log = MessageLog()

    # Add messages for two patients
    for i in range(5):
        log.add(LogEntry(
            timestamp=time.time() + i,
            message_type="ADT",
            trigger_event="A01",
            patient_mrn="MRN001",
            patient_name="John Doe",
            raw_message=f"MSH|msg{i}",
        ))
    for i in range(3):
        log.add(LogEntry(
            timestamp=time.time() + i + 10,
            message_type="ORM",
            trigger_event="O01",
            patient_mrn="MRN002",
            patient_name="Jane Smith",
            raw_message=f"MSH|other{i}",
        ))

    # Get MRN001 timeline
    events = log.get_by_patient("MRN001")
    assert len(events) == 5
    assert all(e["patient_mrn"] == "MRN001" for e in events)

    # Should be chronological (oldest first)
    timestamps = [e["timestamp"] for e in events]
    assert timestamps == sorted(timestamps)


def test_get_by_patient_empty():
    log = MessageLog()
    events = log.get_by_patient("NONEXISTENT")
    assert events == []


def test_get_by_patient_limit():
    log = MessageLog()
    for i in range(300):
        log.add(LogEntry(
            timestamp=time.time() + i,
            message_type="ADT",
            trigger_event="A01",
            patient_mrn="MRN001",
            patient_name="John Doe",
            raw_message=f"MSH|msg{i}",
        ))
    events = log.get_by_patient("MRN001", limit=50)
    assert len(events) == 50


def test_get_by_index():
    log = MessageLog()
    entry = LogEntry(
        timestamp=time.time(),
        message_type="ADT",
        trigger_event="A01",
        patient_mrn="MRN001",
        patient_name="John Doe",
        raw_message="MSH|test",
    )
    log.add(entry)

    result = log.get_by_index(0)
    assert result is not None
    assert result.patient_mrn == "MRN001"


def test_get_by_index_out_of_range():
    log = MessageLog()
    assert log.get_by_index(0) is None
    assert log.get_by_index(-1) is None
    assert log.get_by_index(100) is None


def test_log_entry_validation_errors_field():
    entry = LogEntry(
        timestamp=time.time(),
        message_type="ADT",
        trigger_event="A01",
        patient_mrn="MRN001",
        patient_name="Test",
        raw_message="MSH|...",
        validation_errors=["Missing EVN segment"],
    )
    d = entry.to_dict()
    assert d["validation_errors"] == ["Missing EVN segment"]


def test_log_entry_validation_errors_default_empty():
    entry = LogEntry(
        timestamp=time.time(),
        message_type="ADT",
        trigger_event="A01",
        patient_mrn="MRN001",
        patient_name="Test",
        raw_message="MSH|...",
    )
    d = entry.to_dict()
    assert d["validation_errors"] == []
