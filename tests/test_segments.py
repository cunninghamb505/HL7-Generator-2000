"""Tests for individual segment builders."""

from datetime import date, datetime

from src.core.config import FacilityConfig
from src.core.patient import Address, Allergy, Patient, PatientClass, PatientName
from src.generators.segment_builders.al1 import build_al1
from src.generators.segment_builders.evn import build_evn
from src.generators.segment_builders.msh import build_msh
from src.generators.segment_builders.obx import build_obx
from src.generators.segment_builders.pid import build_pid
from src.generators.segment_builders.pv1 import build_pv1


def test_msh_segment():
    facility = FacilityConfig(
        sending_application="HIS",
        sending_facility="HOSP",
    )
    msh = build_msh("ADT", "A01", facility, hl7_version="2.5.1")
    assert msh.startswith("MSH|^~\\&|HIS|HOSP")
    assert "ADT^A01" in msh
    assert "2.5.1" in msh


def test_pid_segment():
    patient = Patient(
        mrn="MRN0001",
        name=PatientName(family="Doe", given="Jane"),
        date_of_birth=date(1990, 5, 15),
        gender="F",
        address=Address(street="123 Main St", city="Springfield", state="IL", zip_code="62701"),
        phone_home="555-0100",
        account_number="ACCT0001",
    )
    pid = build_pid(patient)
    assert pid.startswith("PID|1|")
    assert "MRN0001" in pid
    assert "Doe^Jane" in pid
    assert "19900515" in pid
    assert "F" in pid


def test_evn_segment():
    evn = build_evn("A01")
    assert evn.startswith("EVN|A01|")


def test_pv1_segment():
    patient = Patient(
        mrn="MRN0001",
        name=PatientName(family="Doe", given="Jane"),
        patient_class=PatientClass.INPATIENT,
        location="MED-101",
        visit_number="VN001",
    )
    pv1 = build_pv1(patient)
    assert "PV1|1|I|MED-101" in pv1


def test_al1_segment():
    allergy = Allergy(
        code="PCN",
        description="Penicillin",
        severity="SV",
        reaction="Anaphylaxis",
        allergy_type="DA",
    )
    al1 = build_al1(allergy)
    assert al1.startswith("AL1|1|DA|PCN^Penicillin|SV|Anaphylaxis")


def test_obx_segment():
    obx = build_obx(
        set_id=1,
        value_type="NM",
        observation_id="2345-7",
        observation_name="Glucose",
        value="95",
        units="mg/dL",
        reference_range="70-100",
        abnormal_flag="",
        result_status="F",
    )
    assert obx.startswith("OBX|1|NM|")
    assert "Glucose" in obx
    assert "95" in obx
    assert "mg/dL" in obx
