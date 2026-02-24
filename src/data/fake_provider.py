"""Faker-based patient data generator with HL7-specific fields."""

from __future__ import annotations

import random
from datetime import date, timedelta

from faker import Faker

from src.core.patient import (
    Address,
    Allergy,
    Insurance,
    NextOfKin,
    Patient,
    PatientName,
    PatientStatus,
)
from src.data.identifiers import (
    generate_account_number,
    generate_doctor_id,
    generate_mrn,
)

fake = Faker()
Faker.seed(0)

RELIGIONS = ["CHR", "JEW", "MOS", "HIN", "BUD", "NON", "OTH", ""]
MARITAL_STATUSES = ["S", "M", "D", "W", "A"]
RACES = [
    "2106-3",  # White
    "2054-5",  # Black
    "2028-9",  # Asian
    "1002-5",  # American Indian
    "2076-8",  # Native Hawaiian
    "2131-1",  # Other
]
ETHNICITIES = ["2135-2", "2186-5"]  # Hispanic, Not Hispanic

LOCATIONS = [
    "ED-01", "ED-02", "ED-03", "ED-04", "ED-05",
    "ICU-01", "ICU-02", "ICU-03", "ICU-04",
    "MED-101", "MED-102", "MED-103", "MED-104", "MED-105",
    "SURG-201", "SURG-202", "SURG-203",
    "OBS-301", "OBS-302", "OBS-303",
    "PEDS-401", "PEDS-402",
    "CARD-501", "CARD-502",
    "ORTH-601", "ORTH-602",
    "OUT-01", "OUT-02", "OUT-03",
    "RAD-01", "RAD-02",
    "LAB-01", "PHARM-01",
]

ALLERGIES = [
    ("PCN", "Penicillin", "DA"),
    ("ASA", "Aspirin", "DA"),
    ("SUL", "Sulfa Drugs", "DA"),
    ("COD", "Codeine", "DA"),
    ("LAT", "Latex", "EA"),
    ("PNT", "Peanuts", "FA"),
    ("SHL", "Shellfish", "FA"),
    ("EGG", "Eggs", "FA"),
    ("IOD", "Iodine", "DA"),
    ("MOR", "Morphine", "DA"),
]

INSURANCE_COMPANIES = [
    ("BC01", "Blue Cross Blue Shield", "BCBS", "PPO"),
    ("AET1", "Aetna Health", "AETNA", "HMO"),
    ("UHC1", "UnitedHealthcare", "UHC", "PPO"),
    ("CIG1", "Cigna Healthcare", "CIGNA", "EPO"),
    ("HUM1", "Humana", "HUMANA", "POS"),
    ("KAI1", "Kaiser Permanente", "KAISER", "HMO"),
    ("MCD1", "Medicaid", "MEDICAID", "MCD"),
    ("MCR1", "Medicare", "MEDICARE", "MCR"),
]

EMPLOYER_NAMES = [
    "General Motors", "Walmart Inc", "Amazon LLC", "State Government",
    "County Hospital", "City Schools", "Tech Solutions Inc", "Federal Agency",
    "Regional Health System", "National Bank Corp", "Self-Employed", "",
]

DOCTOR_NAMES = [
    ("Smith", "John"), ("Johnson", "Sarah"), ("Williams", "Robert"),
    ("Brown", "Emily"), ("Jones", "Michael"), ("Garcia", "Maria"),
    ("Miller", "David"), ("Davis", "Jennifer"), ("Rodriguez", "Carlos"),
    ("Martinez", "Patricia"), ("Anderson", "James"), ("Taylor", "Linda"),
    ("Thomas", "Christopher"), ("Hernandez", "Ana"), ("Moore", "Daniel"),
    ("Wilson", "Susan"), ("Lee", "Kevin"), ("Clark", "Lisa"),
    ("Patel", "Raj"), ("Chen", "Wei"),
]


def generate_patient(min_age: int = 1, max_age: int = 95, insurance_rate: float = 0.85) -> Patient:
    """Generate a realistic fake patient."""
    gender = random.choice(["M", "F"])
    if gender == "M":
        first = fake.first_name_male()
        prefix = random.choice(["Mr.", ""])
    else:
        first = fake.first_name_female()
        prefix = random.choice(["Ms.", "Mrs.", ""])

    last = fake.last_name()
    middle = fake.first_name()[0] if random.random() > 0.3 else ""

    today = date.today()
    age = random.randint(min_age, max_age)
    dob = today - timedelta(days=age * 365 + random.randint(0, 364))

    phone_home = fake.phone_number()[:14]
    phone_work = fake.phone_number()[:14] if random.random() > 0.4 else ""

    ssn = fake.ssn() if random.random() > 0.2 else ""

    patient = Patient(
        mrn=generate_mrn(),
        account_number=generate_account_number(),
        name=PatientName(
            family=last,
            given=first,
            middle=middle,
            prefix=prefix,
        ),
        date_of_birth=dob,
        gender=gender,
        race=random.choice(RACES),
        ethnicity=random.choice(ETHNICITIES),
        ssn=ssn,
        phone_home=phone_home,
        phone_work=phone_work,
        address=Address(
            street=fake.street_address(),
            city=fake.city(),
            state=fake.state_abbr(),
            zip_code=fake.zipcode(),
            country="USA",
        ),
        marital_status=random.choice(MARITAL_STATUSES),
        language=random.choice(["ENG", "SPA", "FRE", "CHI", "VIE"]),
        religion=random.choice(RELIGIONS),
        status=PatientStatus.IDLE,
    )

    # Random allergies (0-3)
    num_allergies = random.choices([0, 1, 2, 3], weights=[40, 35, 20, 5])[0]
    if num_allergies > 0:
        for code, desc, atype in random.sample(ALLERGIES, min(num_allergies, len(ALLERGIES))):
            patient.allergies.append(
                Allergy(
                    code=code,
                    description=desc,
                    severity=random.choice(["MI", "MO", "SV"]),
                    reaction=random.choice(["Rash", "Hives", "Anaphylaxis", "Nausea", "Swelling"]),
                    allergy_type=atype,
                )
            )

    # Insurance (optional based on insurance_rate)
    if random.random() < insurance_rate:
        ins_co = random.choice(INSURANCE_COMPANIES)
        plan_id, plan_name, company_code, plan_type = ins_co

        # Effective/expiration dates
        effective_year = today.year - random.randint(0, 5)
        effective_date = f"{effective_year}0101"
        expiration_date = f"{effective_year + 1}1231"

        # Employer info
        employer = random.choice(EMPLOYER_NAMES)

        # Build enriched insurance
        ins_data = Insurance(
            plan_id=plan_id,
            plan_name=plan_name,
            company_name=company_code,
            company_phone=fake.phone_number()[:14],
            group_number=f"GRP{random.randint(10000, 99999)}",
            group_name=f"{company_code} Group Plan",
            subscriber_id=f"SUB{random.randint(100000, 999999)}",
            plan_effective_date=effective_date,
            plan_expiration_date=expiration_date,
            plan_type=plan_type,
            insured_relationship=random.choices(["01", "02", "03"], weights=[70, 20, 10])[0],
            policy_number=f"POL{random.randint(100000, 999999)}",
            insured_employer_name=employer,
        )

        # IN2 extra fields for Medicare/Medicaid
        if plan_type == "MCR":
            ins_data.medicare_id = f"MCR{random.randint(100000000, 999999999)}"
            ins_data.insured_employer_id = f"EMP{random.randint(10000, 99999)}"
        elif plan_type == "MCD":
            ins_data.medicaid_id = f"MCD{random.randint(100000000, 999999999)}"
            ins_data.insured_employer_id = f"EMP{random.randint(10000, 99999)}"
        elif employer and random.random() > 0.4:
            ins_data.insured_employer_id = f"EMP{random.randint(10000, 99999)}"
            ins_data.employer_info_data = employer

        # Mail claim party (random)
        if random.random() > 0.6:
            ins_data.mail_claim_party = random.choice(["E", "G", "I", "O", "P"])

        # IN3 certification fields (more common for inpatient scenarios)
        if random.random() > 0.5:
            ins_data.certification_required = random.choice(["Y", "N"])
            ins_data.pre_certification_required = random.choice(["Y", "N"])
            if ins_data.certification_required == "Y" and random.random() > 0.3:
                ins_data.certification_number = f"CERT{random.randint(100000, 999999)}"
                ins_data.certification_begin_date = effective_date
                ins_data.certification_end_date = expiration_date
                ins_data.penalty = random.choice(["COPAY", "DEDUCT", ""])

        patient.insurance = ins_data

    # Next of kin
    if random.random() > 0.2:
        nok_gender = random.choice(["M", "F"])
        nok_first = fake.first_name_male() if nok_gender == "M" else fake.first_name_female()
        patient.next_of_kin = NextOfKin(
            name=PatientName(family=last, given=nok_first),
            relationship=random.choice(["SPO", "PAR", "SIB", "CHD", "OTH"]),
            phone=fake.phone_number()[:14],
        )

    return patient


def pick_doctor() -> tuple[str, str]:
    """Return (doctor_id, doctor_name_hl7)."""
    last, first = random.choice(DOCTOR_NAMES)
    doc_id = generate_doctor_id()
    return doc_id, f"{last}^{first}"


def pick_location(area: str = "") -> str:
    """Pick a location, optionally filtering by area prefix."""
    if area:
        candidates = [loc for loc in LOCATIONS if loc.startswith(area.upper())]
        if candidates:
            return random.choice(candidates)
    return random.choice(LOCATIONS)
