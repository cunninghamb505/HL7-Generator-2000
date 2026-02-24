"""Tests for step handlers."""

from src.core.patient import PatientStatus
from src.data.fake_provider import generate_patient
from src.workflows.step_handlers.admission import AdmissionHandler
from src.workflows.step_handlers.billing import BillingHandler
from src.workflows.step_handlers.discharge import DischargeHandler
from src.workflows.step_handlers.lab_order import LabOrderHandler
from src.workflows.step_handlers.lab_result import LabResultHandler
from src.workflows.step_handlers.pharmacy_order import PharmacyOrderHandler
from src.workflows.step_handlers.scheduling import SchedulingHandler
from src.workflows.step_handlers.vaccination import VaccinationHandler


def test_admission_handler():
    patient = generate_patient()
    handler = AdmissionHandler()
    events = handler.handle(patient, {"patient_class": "E", "loc": "ED"})
    assert len(events) == 1
    assert events[0].message_type == "ADT"
    assert events[0].trigger_event == "A04"
    assert patient.status == PatientStatus.ACTIVE
    assert patient.location.startswith("ED")


def test_admission_inpatient():
    patient = generate_patient()
    handler = AdmissionHandler()
    events = handler.handle(patient, {"patient_class": "I"})
    assert events[0].trigger_event == "A01"


def test_discharge_handler():
    patient = generate_patient()
    patient.status = PatientStatus.ACTIVE
    handler = DischargeHandler()
    events = handler.handle(patient, {})
    assert len(events) == 1
    assert events[0].message_type == "ADT"
    assert events[0].trigger_event == "A03"
    assert patient.status == PatientStatus.DISCHARGED
    assert patient.discharge_datetime is not None


def test_lab_order_handler():
    patient = generate_patient()
    handler = LabOrderHandler()
    events = handler.handle(patient, {"order_profile": "CBC"})
    assert len(events) == 1
    assert events[0].message_type == "ORM"
    assert events[0].trigger_event == "O01"
    assert len(patient.orders) == 1


def test_lab_result_handler():
    patient = generate_patient()
    # First create an order
    order_handler = LabOrderHandler()
    order_handler.handle(patient, {"order_profile": "CMP"})

    result_handler = LabResultHandler()
    events = result_handler.handle(patient, {"order_profile": "CMP"})
    assert len(events) == 1
    assert events[0].message_type == "ORU"
    assert "results" in events[0].kwargs
    assert len(events[0].kwargs["results"]) > 0


def test_pharmacy_order_handler():
    patient = generate_patient()
    handler = PharmacyOrderHandler()
    events = handler.handle(patient, {})
    assert len(events) == 1
    assert events[0].message_type == "RDE"


def test_vaccination_handler():
    patient = generate_patient()
    handler = VaccinationHandler()
    events = handler.handle(patient, {})
    assert len(events) == 1
    assert events[0].message_type == "VXU"
    assert events[0].trigger_event == "V04"


def test_scheduling_handler():
    patient = generate_patient()
    handler = SchedulingHandler()
    events = handler.handle(patient, {})
    assert len(events) == 1
    assert events[0].message_type == "SIU"
    assert events[0].trigger_event == "S12"


def test_billing_handler():
    patient = generate_patient()
    handler = BillingHandler()
    events = handler.handle(patient, {"num_charges": 3})
    assert len(events) == 1
    assert events[0].message_type == "DFT"
    assert len(events[0].kwargs["transactions"]) == 3
