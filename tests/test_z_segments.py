"""Tests for Z-segment engine."""

import os
import tempfile

from src.generators.z_segment_engine import (
    build_z_segment,
    get_z_segments_for_type,
    load_z_segments,
)


def test_load_z_segments_from_file():
    defs = load_z_segments("config/z_segments.yaml")
    assert len(defs) >= 2
    names = [d["name"] for d in defs]
    assert "ZPD" in names
    assert "ZPI" in names


def test_load_z_segments_missing_file():
    defs = load_z_segments("nonexistent.yaml")
    assert defs == []


def test_build_z_segment_static_value():
    defn = {
        "name": "ZPD",
        "fields": [
            {"name": "dept", "position": 1, "value": "CARDIO"},
        ],
    }
    result = build_z_segment(defn)
    assert result == "ZPD|CARDIO"


def test_build_z_segment_random_int():
    defn = {
        "name": "ZPD",
        "fields": [
            {"name": "score", "position": 1, "type": "random_int", "min": 1, "max": 10},
        ],
    }
    result = build_z_segment(defn)
    parts = result.split("|")
    assert parts[0] == "ZPD"
    val = int(parts[1])
    assert 1 <= val <= 10


def test_build_z_segment_random_choice():
    defn = {
        "name": "ZPI",
        "fields": [
            {"name": "status", "position": 1, "type": "random_choice", "choices": ["A", "B", "C"]},
        ],
    }
    result = build_z_segment(defn)
    parts = result.split("|")
    assert parts[0] == "ZPI"
    assert parts[1] in ["A", "B", "C"]


def test_build_z_segment_multiple_fields():
    defn = {
        "name": "ZPD",
        "fields": [
            {"name": "dept", "position": 1, "value": "CARDIO"},
            {"name": "score", "position": 2, "type": "random_int", "min": 5, "max": 5},
            {"name": "status", "position": 3, "type": "random_choice", "choices": ["Y"]},
        ],
    }
    result = build_z_segment(defn)
    assert result == "ZPD|CARDIO|5|Y"


def test_build_z_segment_faker_field():
    defn = {
        "name": "ZPD",
        "fields": [
            {"name": "city", "position": 1, "type": "faker_city"},
        ],
    }
    result = build_z_segment(defn)
    parts = result.split("|")
    assert parts[0] == "ZPD"
    assert len(parts[1]) > 0  # faker should produce a non-empty city


def test_get_z_segments_for_type():
    defs = [
        {"name": "ZPD", "attach_to": ["ADT", "ORM"], "fields": [{"name": "x", "position": 1, "value": "A"}]},
        {"name": "ZPI", "attach_to": ["ADT", "BAR"], "fields": [{"name": "y", "position": 1, "value": "B"}]},
        {"name": "ZXX", "attach_to": ["ORU"], "fields": [{"name": "z", "position": 1, "value": "C"}]},
    ]

    adt_segs = get_z_segments_for_type(defs, "ADT")
    assert len(adt_segs) == 2
    assert adt_segs[0] == "ZPD|A"
    assert adt_segs[1] == "ZPI|B"

    orm_segs = get_z_segments_for_type(defs, "ORM")
    assert len(orm_segs) == 1
    assert orm_segs[0] == "ZPD|A"

    oru_segs = get_z_segments_for_type(defs, "ORU")
    assert len(oru_segs) == 1
    assert oru_segs[0] == "ZXX|C"

    mfn_segs = get_z_segments_for_type(defs, "MFN")
    assert len(mfn_segs) == 0


def test_get_z_segments_case_insensitive():
    defs = [
        {"name": "ZPD", "attach_to": ["adt"], "fields": [{"name": "x", "position": 1, "value": "V"}]},
    ]
    result = get_z_segments_for_type(defs, "ADT")
    assert len(result) == 1


def test_load_z_segments_yaml_content():
    content = """
segments:
  - name: ZTT
    description: "Test segment"
    attach_to: ["ADT"]
    fields:
      - name: test_field
        position: 1
        value: "HELLO"
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(content)
        f.flush()
        defs = load_z_segments(f.name)

    os.unlink(f.name)
    assert len(defs) == 1
    assert defs[0]["name"] == "ZTT"
