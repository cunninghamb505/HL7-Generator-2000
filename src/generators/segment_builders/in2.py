"""IN2 (Insurance Additional Information) segment builder."""

from __future__ import annotations

from src.core.patient import Patient


def build_in2(patient: Patient) -> str:
    """Build IN2 segment from patient insurance data.

    IN2 provides extended insurance information such as employer details,
    Medicare/Medicaid IDs, and military information.
    """
    ins = patient.insurance
    if not ins or not ins.plan_id:
        return ""

    # Only emit IN2 if we have meaningful additional data
    has_data = any([
        ins.insured_employer_id,
        ins.medicare_id,
        ins.medicaid_id,
        ins.military_id_number,
        ins.mail_claim_party,
        ins.employer_info_data,
    ])
    if not has_data:
        return ""

    fields = [
        "IN2",
        ins.insured_employer_id,       # IN2.1  Insured's Employee ID
        patient.ssn,                   # IN2.2  Insured's Social Security Number
        ins.insured_employer_name,     # IN2.3  Insured's Employer's Name and ID
        ins.employer_info_data,        # IN2.4  Employer Information Data
        ins.mail_claim_party,          # IN2.5  Mail Claim Party
        ins.medicare_id,               # IN2.6  Medicare Health Ins Card Number
        ins.medicaid_id,               # IN2.7  Medicaid Case Name
        "",                            # IN2.8  Medicaid Case Number
        ins.military_sponsor_name,     # IN2.9  Military Sponsor Name
        ins.military_id_number,        # IN2.10 Military ID Number
        "",                            # IN2.11 Dependent of Military Recipient
        "",                            # IN2.12 Military Organization
        ins.military_status,           # IN2.13 Military Station
        "",                            # IN2.14 Military Service
        "",                            # IN2.15 Military Rank/Grade
        ins.military_status,           # IN2.16 Military Status
        "",                            # IN2.17 Military Retire Date
        "",                            # IN2.18 Military Non-Avail Cert on File
        "",                            # IN2.19 Baby Coverage
        "",                            # IN2.20 Combine Baby Bill
        "",                            # IN2.21 Blood Deductible
        "",                            # IN2.22 Special Coverage Approval Name
        "",                            # IN2.23 Special Coverage Approval Title
        "",                            # IN2.24 Non-Covered Insurance Code
        "",                            # IN2.25 Payor ID
        "",                            # IN2.26 Payor Subscriber ID
    ]
    return "|".join(fields)
