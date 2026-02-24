"""Tests for patient model and patient pool."""

from src.core.patient import Patient, PatientName, PatientStatus
from src.core.patient_pool import PatientPool
from src.data.fake_provider import generate_patient


def test_generate_patient():
    patient = generate_patient()
    assert patient.mrn.startswith("MRN")
    assert patient.name.family
    assert patient.name.given
    assert patient.date_of_birth is not None
    assert patient.gender in ("M", "F")
    assert patient.status == PatientStatus.IDLE


def test_patient_age():
    patient = generate_patient(min_age=30, max_age=30)
    age = patient.age()
    assert 29 <= age <= 31  # Allow for date boundary


def test_patient_name_hl7():
    name = PatientName(family="Smith", given="John", middle="Q", prefix="Mr.")
    assert name.to_hl7() == "Smith^John^Q^^Mr."


def test_patient_pool_init():
    pool = PatientPool(pool_size=10)
    pool.initialize()
    assert pool.total_count == 10
    assert pool.idle_count == 10
    assert pool.active_count == 0


def test_patient_pool_acquire_release():
    pool = PatientPool(pool_size=5)
    pool.initialize()

    patient = pool.acquire_patient()
    assert patient is not None
    assert patient.status == PatientStatus.ACTIVE
    assert pool.idle_count == 4
    assert pool.active_count == 1

    pool.release_patient(patient.mrn)
    assert pool.idle_count == 5
    assert pool.active_count == 0


def test_patient_to_dict():
    patient = generate_patient()
    d = patient.to_dict()
    assert "mrn" in d
    assert "name" in d
    assert "gender" in d
    assert "status" in d
