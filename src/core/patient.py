"""Patient dataclass with demographics and clinical state."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Any


class PatientStatus(str, Enum):
    IDLE = "idle"
    ACTIVE = "active"
    DISCHARGED = "discharged"
    RETIRED = "retired"


class PatientClass(str, Enum):
    INPATIENT = "I"
    OUTPATIENT = "O"
    EMERGENCY = "E"
    PREADMIT = "P"
    RECURRING = "R"


@dataclass
class PatientName:
    family: str
    given: str
    middle: str = ""
    suffix: str = ""
    prefix: str = ""

    def to_hl7(self) -> str:
        return f"{self.family}^{self.given}^{self.middle}^{self.suffix}^{self.prefix}"


@dataclass
class Address:
    street: str = ""
    city: str = ""
    state: str = ""
    zip_code: str = ""
    country: str = "USA"

    def to_hl7(self) -> str:
        return f"{self.street}^^{self.city}^{self.state}^{self.zip_code}^{self.country}"


@dataclass
class Insurance:
    plan_id: str = ""
    plan_name: str = ""
    group_number: str = ""
    subscriber_id: str = ""
    company_name: str = ""
    company_address: str = ""
    company_phone: str = ""
    group_name: str = ""
    plan_effective_date: str = ""
    plan_expiration_date: str = ""
    plan_type: str = ""          # HMO, PPO, EPO, POS, IND, MCR, MCD
    insured_relationship: str = "01"  # 01=Self, 02=Spouse, 03=Child
    policy_number: str = ""
    authorization_info: str = ""
    # IN2 fields
    insured_employer_name: str = ""
    insured_employer_id: str = ""
    employer_info_data: str = ""
    mail_claim_party: str = ""
    medicare_id: str = ""
    medicaid_id: str = ""
    military_sponsor_name: str = ""
    military_id_number: str = ""
    military_status: str = ""     # ACT, RET, ""
    # IN3 fields
    certification_number: str = ""
    certification_required: str = ""  # Y, N
    certification_datetime: str = ""
    certification_begin_date: str = ""
    certification_end_date: str = ""
    pre_certification_required: str = ""  # Y, N
    certified_by: str = ""
    penalty: str = ""  # COPAY, DEDUCT, ""


@dataclass
class NextOfKin:
    name: PatientName | None = None
    relationship: str = ""
    phone: str = ""
    address: Address | None = None


@dataclass
class Allergy:
    code: str = ""
    description: str = ""
    severity: str = "MO"  # MI=Mild, MO=Moderate, SV=Severe
    reaction: str = ""
    allergy_type: str = "DA"  # DA=Drug, FA=Food, EA=Environmental


@dataclass
class Diagnosis:
    code: str = ""
    description: str = ""
    coding_system: str = "I10"
    diagnosis_type: str = "A"  # A=Admitting, W=Working, F=Final


@dataclass
class Order:
    order_number: str = ""
    placer_order_number: str = ""
    filler_order_number: str = ""
    order_type: str = ""
    order_code: str = ""
    order_name: str = ""
    priority: str = "R"
    status: str = "IP"  # IP=In Progress, CM=Completed, CA=Cancelled
    order_datetime: datetime | None = None
    results: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class Patient:
    mrn: str = ""
    account_number: str = ""
    name: PatientName = field(default_factory=lambda: PatientName("", ""))
    date_of_birth: date | None = None
    gender: str = "U"  # M, F, U, O
    race: str = ""
    ethnicity: str = ""
    ssn: str = ""
    phone_home: str = ""
    phone_work: str = ""
    address: Address = field(default_factory=Address)
    marital_status: str = "S"  # S=Single, M=Married, D=Divorced, W=Widowed
    language: str = "ENG"
    religion: str = ""

    # Clinical state
    status: PatientStatus = PatientStatus.IDLE
    patient_class: PatientClass = PatientClass.OUTPATIENT
    location: str = ""
    attending_doctor_id: str = ""
    attending_doctor_name: str = ""
    admit_datetime: datetime | None = None
    discharge_datetime: datetime | None = None
    visit_number: str = ""

    # Associated data
    insurance: Insurance = field(default_factory=Insurance)
    next_of_kin: NextOfKin = field(default_factory=NextOfKin)
    allergies: list[Allergy] = field(default_factory=list)
    diagnoses: list[Diagnosis] = field(default_factory=list)
    orders: list[Order] = field(default_factory=list)

    # Workflow tracking
    active_workflow: str = ""
    workflow_step: int = 0

    def age(self) -> int:
        if self.date_of_birth is None:
            return 0
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "mrn": self.mrn,
            "name": f"{self.name.given} {self.name.family}",
            "dob": self.date_of_birth.isoformat() if self.date_of_birth else "",
            "gender": self.gender,
            "age": self.age(),
            "status": self.status.value,
            "patient_class": self.patient_class.value,
            "location": self.location,
            "active_workflow": self.active_workflow,
            "account_number": self.account_number,
        }
