"""IN1 (Insurance) segment builder."""

from __future__ import annotations

from src.core.patient import Patient
from src.utils.hl7_helpers import format_date


def build_in1(patient: Patient, set_id: int = 1) -> str:
    """Build IN1 segment from patient insurance data."""
    ins = patient.insurance
    if not ins or not ins.plan_id:
        return ""

    # Build insured address from patient address if insured is self
    insured_address = ""
    if ins.insured_relationship == "01":
        insured_address = patient.address.to_hl7()

    # Insured DOB from patient if insured is self
    insured_dob = ""
    if ins.insured_relationship == "01" and patient.date_of_birth:
        insured_dob = format_date(patient.date_of_birth)

    fields = [
        "IN1",
        str(set_id),                   # IN1.1  Set ID
        ins.plan_id,                   # IN1.2  Insurance Plan ID
        ins.company_name,              # IN1.3  Insurance Company ID
        ins.plan_name,                 # IN1.4  Insurance Company Name
        ins.company_address,           # IN1.5  Insurance Company Address
        "",                            # IN1.6  Insurance Co Contact Person
        ins.company_phone,             # IN1.7  Insurance Co Phone Number
        ins.group_number,              # IN1.8  Group Number
        ins.group_name,                # IN1.9  Group Name
        "",                            # IN1.10 Insured's Group Emp ID
        ins.insured_employer_name,     # IN1.11 Insured's Group Emp Name
        ins.plan_effective_date,       # IN1.12 Plan Effective Date
        ins.plan_expiration_date,      # IN1.13 Plan Expiration Date
        ins.authorization_info,        # IN1.14 Authorization Information
        ins.plan_type,                 # IN1.15 Plan Type
        patient.name.to_hl7(),         # IN1.16 Name of Insured
        ins.insured_relationship,      # IN1.17 Insured's Relationship to Patient
        insured_dob,                   # IN1.18 Insured's Date of Birth
        insured_address,               # IN1.19 Insured's Address
        "Y",                           # IN1.20 Assignment of Benefits
        "",                            # IN1.21 Coordination of Benefits
        "",                            # IN1.22 Coord of Ben. Priority
        "",                            # IN1.23 Notice of Admission Flag
        "",                            # IN1.24 Notice of Admission Date
        "",                            # IN1.25 Report of Eligibility Flag
        "",                            # IN1.26 Report of Eligibility Date
        "",                            # IN1.27 Release Information Code
        "",                            # IN1.28 Pre-Admit Cert
        "",                            # IN1.29 Verification Date/Time
        "",                            # IN1.30 Verification By
        "",                            # IN1.31 Type of Agreement Code
        "",                            # IN1.32 Billing Status
        "",                            # IN1.33 Lifetime Reserve Days
        "",                            # IN1.34 Delay Before L.R. Day
        "",                            # IN1.35 Company Plan Code
        ins.policy_number,             # IN1.36 Policy Number
        ins.subscriber_id,             # IN1.37 Policy Deductible (reused for subscriber)
    ]
    return "|".join(fields)
