"""Tests for message log."""

import time

from src.utils.message_log import LogEntry, MessageLog


def test_message_log_add_and_get():
    log = MessageLog(max_size=100)
    entry = LogEntry(
        timestamp=time.time(),
        message_type="ADT",
        trigger_event="A01",
        patient_mrn="MRN001",
        patient_name="John Doe",
        raw_message="MSH|...",
    )
    log.add(entry)
    assert log.total_count == 1

    recent = log.get_recent(10)
    assert len(recent) == 1
    assert recent[0]["message_type"] == "ADT"


def test_message_log_search():
    log = MessageLog()
    for i in range(10):
        log.add(LogEntry(
            timestamp=time.time(),
            message_type="ADT" if i % 2 == 0 else "ORM",
            trigger_event="A01" if i % 2 == 0 else "O01",
            patient_mrn=f"MRN{i:03d}",
            patient_name=f"Patient {i}",
            raw_message=f"MSH|test|{i}",
        ))

    results = log.search(message_type="ADT")
    assert len(results) == 5

    results = log.search(query="MRN003")
    assert len(results) == 1


def test_message_log_max_size():
    log = MessageLog(max_size=5)
    for i in range(10):
        log.add(LogEntry(
            timestamp=time.time(),
            message_type="ADT",
            trigger_event="A01",
            patient_mrn=f"MRN{i}",
            patient_name="Test",
            raw_message="test",
        ))
    assert log.total_count == 5


def test_message_log_clear():
    log = MessageLog()
    log.add(LogEntry(
        timestamp=time.time(),
        message_type="ADT",
        trigger_event="A01",
        patient_mrn="MRN001",
        patient_name="Test",
        raw_message="test",
    ))
    assert log.total_count == 1
    log.clear()
    assert log.total_count == 0
