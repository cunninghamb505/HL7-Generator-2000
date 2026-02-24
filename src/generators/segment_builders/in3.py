"""IN3 (Insurance Additional Information - Certification) segment builder."""

from __future__ import annotations

from src.core.patient import Patient


def build_in3(patient: Patient, set_id: int = 1) -> str:
    """Build IN3 segment from patient insurance data.

    IN3 contains certification/pre-authorization information
    required by many insurance plans.
    """
    ins = patient.insurance
    if not ins or not ins.plan_id:
        return ""

    # Only emit IN3 if we have certification data
    has_data = any([
        ins.certification_number,
        ins.certification_required,
        ins.pre_certification_required,
        ins.penalty,
    ])
    if not has_data:
        return ""

    fields = [
        "IN3",
        str(set_id),                       # IN3.1  Set ID
        ins.certification_number,          # IN3.2  Certification Number
        ins.certified_by,                  # IN3.3  Certified By
        ins.certification_required,        # IN3.4  Certification Required
        ins.penalty,                       # IN3.5  Penalty
        ins.certification_datetime,        # IN3.6  Certification Date/Time
        ins.certification_begin_date,      # IN3.7  Certification Modify Date/Time
        "",                                # IN3.8  Operator
        "",                                # IN3.9  Certification Begin Date
        ins.certification_end_date,        # IN3.10 Certification End Date
        "",                                # IN3.11 Days
        "",                                # IN3.12 Non-Concur Code/Description
        "",                                # IN3.13 Non-Concur Effective Date/Time
        "",                                # IN3.14 Physician Reviewer
        "",                                # IN3.15 Certification Contact
        "",                                # IN3.16 Certification Contact Phone
        "",                                # IN3.17 Appeal Reason
        "",                                # IN3.18 Certification Agency
        "",                                # IN3.19 Certification Agency Phone
        ins.pre_certification_required,    # IN3.20 Pre-Certification Required
        "",                                # IN3.21 Case Manager
        "",                                # IN3.22 Second Opinion Date
        "",                                # IN3.23 Second Opinion Status
        "",                                # IN3.24 Second Opinion Doc ID
        "",                                # IN3.25 Second Opinion Documentation Received
    ]
    return "|".join(fields)
