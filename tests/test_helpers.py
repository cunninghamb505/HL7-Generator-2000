"""Tests for HL7 helpers."""

from datetime import date, datetime

from src.utils.hl7_helpers import (
    build_coded_element,
    escape_hl7,
    format_date,
    format_timestamp,
)


def test_format_timestamp_full():
    dt = datetime(2024, 3, 15, 14, 30, 45)
    assert format_timestamp(dt) == "20240315143045"


def test_format_timestamp_date():
    dt = datetime(2024, 3, 15, 14, 30, 45)
    assert format_timestamp(dt, precision="date") == "20240315"


def test_format_timestamp_minute():
    dt = datetime(2024, 3, 15, 14, 30, 45)
    assert format_timestamp(dt, precision="minute") == "202403151430"


def test_format_date():
    d = date(1990, 5, 15)
    assert format_date(d) == "19900515"


def test_format_date_none():
    assert format_date(None) == ""


def test_escape_hl7():
    assert escape_hl7("normal text") == "normal text"
    assert escape_hl7("pipe|here") == "pipe\\F\\here"
    assert escape_hl7("caret^here") == "caret\\S\\here"
    assert escape_hl7("amp&here") == "amp\\T\\here"
    assert escape_hl7("tilde~here") == "tilde\\R\\here"


def test_build_coded_element():
    ce = build_coded_element("2345-7", "Glucose", "LN")
    assert ce == "2345-7^Glucose^LN"
