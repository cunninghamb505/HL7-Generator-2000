"""Tests for message generators."""

from src.core.config import FacilityConfig
from src.core.patient import Order, Patient, PatientClass, PatientName, PatientStatus
from src.data.fake_provider import generate_patient
from src.generators.message_factory import MessageFactory
from src.generators.message_types.adt import ADTGenerator
from src.generators.message_types.orm import ORMGenerator
from src.generators.message_types.oru import ORUGenerator


def _make_patient() -> Patient:
    p = generate_patient()
    p.status = PatientStatus.ACTIVE
    p.patient_class = PatientClass.EMERGENCY
    p.location = "ED-01"
    p.attending_doctor_id = "DR12345"
    p.attending_doctor_name = "Smith^John"
    return p


def _make_facility() -> FacilityConfig:
    return FacilityConfig(
        sending_application="TEST",
        sending_facility="TEST_HOSP",
    )


def test_adt_a01():
    gen = ADTGenerator(_make_facility())
    msg = gen.generate("A01", _make_patient())
    assert msg.startswith("MSH|")
    assert "ADT^A01" in msg
    assert "PID|" in msg
    assert "PV1|" in msg
    assert "EVN|A01" in msg


def test_adt_a03():
    gen = ADTGenerator(_make_facility())
    msg = gen.generate("A03", _make_patient())
    assert "ADT^A03" in msg


def test_adt_a04():
    gen = ADTGenerator(_make_facility())
    msg = gen.generate("A04", _make_patient())
    assert "ADT^A04" in msg


def test_orm_o01():
    gen = ORMGenerator(_make_facility())
    order = Order(
        placer_order_number="PLC0000001",
        filler_order_number="FIL0000001",
        order_code="80053",
        order_name="CMP",
        priority="R",
        status="IP",
    )
    msg = gen.generate("O01", _make_patient(), order=order)
    assert "ORM^O01" in msg
    assert "ORC|" in msg
    assert "OBR|" in msg


def test_oru_r01():
    gen = ORUGenerator(_make_facility())
    order = Order(
        placer_order_number="PLC0000001",
        filler_order_number="FIL0000001",
        order_code="80053",
        order_name="CMP",
    )
    results = [
        {
            "observation_id": "2345-7",
            "observation_name": "Glucose",
            "value_type": "NM",
            "value": "95",
            "units": "mg/dL",
            "reference_range": "70-100",
            "abnormal_flag": "",
        }
    ]
    msg = gen.generate("R01", _make_patient(), order=order, results=results)
    assert "ORU^R01" in msg
    assert "OBX|" in msg
    assert "Glucose" in msg


def test_message_factory():
    factory = MessageFactory(_make_facility())
    assert "ADT" in factory.supported_types
    assert "ORM" in factory.supported_types
    assert "ORU" in factory.supported_types
    assert len(factory.supported_types) == 12


def test_message_factory_generate():
    factory = MessageFactory(_make_facility())
    msg = factory.generate("ADT", "A01", _make_patient())
    assert "ADT^A01" in msg


def test_all_generators_listed():
    factory = MessageFactory(_make_facility())
    generators = factory.list_generators()
    assert len(generators) == 12
    type_names = [g["message_type"] for g in generators]
    assert "ADT" in type_names
    assert "VXU" in type_names
    assert "SIU" in type_names
