"""Clinical data: lab test definitions, result ranges, and realistic value generation."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any


@dataclass
class LabTestDef:
    code: str
    name: str
    loinc: str
    units: str
    ref_low: float
    ref_high: float
    value_type: str = "NM"
    coding_system: str = "LN"


# Common lab tests with LOINC codes and reference ranges
LAB_TESTS: dict[str, list[LabTestDef]] = {
    "CMP": [
        LabTestDef("2345-7", "Glucose", "2345-7", "mg/dL", 70, 100),
        LabTestDef("3094-0", "BUN", "3094-0", "mg/dL", 7, 20),
        LabTestDef("2160-0", "Creatinine", "2160-0", "mg/dL", 0.7, 1.3),
        LabTestDef("2951-2", "Sodium", "2951-2", "mmol/L", 136, 145),
        LabTestDef("2823-3", "Potassium", "2823-3", "mmol/L", 3.5, 5.1),
        LabTestDef("2075-0", "Chloride", "2075-0", "mmol/L", 98, 106),
        LabTestDef("2028-9", "CO2", "2028-9", "mmol/L", 23, 29),
        LabTestDef("17861-6", "Calcium", "17861-6", "mg/dL", 8.5, 10.5),
        LabTestDef("2885-2", "Total Protein", "2885-2", "g/dL", 6.0, 8.3),
        LabTestDef("1751-7", "Albumin", "1751-7", "g/dL", 3.5, 5.5),
        LabTestDef("1975-2", "Total Bilirubin", "1975-2", "mg/dL", 0.1, 1.2),
        LabTestDef("6768-6", "Alk Phosphatase", "6768-6", "U/L", 44, 147),
        LabTestDef("1742-6", "ALT", "1742-6", "U/L", 7, 56),
        LabTestDef("1920-8", "AST", "1920-8", "U/L", 10, 40),
    ],
    "CBC": [
        LabTestDef("26464-8", "WBC", "26464-8", "K/uL", 4.5, 11.0),
        LabTestDef("789-8", "RBC", "789-8", "M/uL", 4.2, 5.9),
        LabTestDef("718-7", "Hemoglobin", "718-7", "g/dL", 12.0, 17.5),
        LabTestDef("4544-3", "Hematocrit", "4544-3", "%", 36.0, 51.0),
        LabTestDef("787-2", "MCV", "787-2", "fL", 80.0, 100.0),
        LabTestDef("786-4", "MCH", "786-4", "pg", 27.0, 33.0),
        LabTestDef("785-6", "MCHC", "785-6", "g/dL", 32.0, 36.0),
        LabTestDef("777-3", "Platelet Count", "777-3", "K/uL", 150, 400),
    ],
    "BMP": [
        LabTestDef("2345-7", "Glucose", "2345-7", "mg/dL", 70, 100),
        LabTestDef("3094-0", "BUN", "3094-0", "mg/dL", 7, 20),
        LabTestDef("2160-0", "Creatinine", "2160-0", "mg/dL", 0.7, 1.3),
        LabTestDef("2951-2", "Sodium", "2951-2", "mmol/L", 136, 145),
        LabTestDef("2823-3", "Potassium", "2823-3", "mmol/L", 3.5, 5.1),
        LabTestDef("2075-0", "Chloride", "2075-0", "mmol/L", 98, 106),
        LabTestDef("2028-9", "CO2", "2028-9", "mmol/L", 23, 29),
        LabTestDef("17861-6", "Calcium", "17861-6", "mg/dL", 8.5, 10.5),
    ],
    "LIPID": [
        LabTestDef("2093-3", "Total Cholesterol", "2093-3", "mg/dL", 0, 200),
        LabTestDef("2571-8", "Triglycerides", "2571-8", "mg/dL", 0, 150),
        LabTestDef("2085-9", "HDL Cholesterol", "2085-9", "mg/dL", 40, 60),
        LabTestDef("2089-1", "LDL Cholesterol", "2089-1", "mg/dL", 0, 100),
    ],
    "UA": [
        LabTestDef("5778-6", "Color", "5778-6", "", 0, 0, value_type="ST"),
        LabTestDef("5767-9", "Appearance", "5767-9", "", 0, 0, value_type="ST"),
        LabTestDef("2756-5", "pH", "2756-5", "", 5.0, 8.0),
        LabTestDef("5811-5", "Specific Gravity", "5811-5", "", 1.005, 1.030),
        LabTestDef("5804-0", "Protein", "5804-0", "", 0, 0, value_type="ST"),
        LabTestDef("5792-7", "Glucose UA", "5792-7", "", 0, 0, value_type="ST"),
    ],
    "COAG": [
        LabTestDef("5902-2", "PT", "5902-2", "seconds", 11.0, 13.5),
        LabTestDef("6301-6", "INR", "6301-6", "", 0.8, 1.1),
        LabTestDef("3173-2", "PTT", "3173-2", "seconds", 25.0, 35.0),
    ],
    "TSH": [
        LabTestDef("3016-3", "TSH", "3016-3", "mIU/L", 0.4, 4.0),
    ],
    "TROPONIN": [
        LabTestDef("49563-0", "Troponin I", "49563-0", "ng/mL", 0, 0.04),
    ],
    "HBA1C": [
        LabTestDef("4548-4", "Hemoglobin A1c", "4548-4", "%", 4.0, 5.6),
    ],
}


def generate_lab_results(
    order_profile: str,
    abnormal_rate: float = 0.15,
) -> list[dict[str, Any]]:
    """Generate realistic lab results for a given order profile."""
    tests = LAB_TESTS.get(order_profile.upper(), [])
    results: list[dict[str, Any]] = []

    for test in tests:
        if test.value_type == "ST":
            # String-valued results
            value = _generate_string_result(test.code)
            results.append({
                "observation_id": test.loinc,
                "observation_name": test.name,
                "value_type": "ST",
                "value": value,
                "units": "",
                "reference_range": "",
                "abnormal_flag": "",
                "result_status": "F",
            })
        else:
            # Numeric results
            is_abnormal = random.random() < abnormal_rate
            value, flag = _generate_numeric_result(
                test.ref_low, test.ref_high, is_abnormal
            )
            ref_range = f"{test.ref_low}-{test.ref_high}"
            results.append({
                "observation_id": test.loinc,
                "observation_name": test.name,
                "value_type": "NM",
                "value": str(round(value, 2)),
                "units": test.units,
                "reference_range": ref_range,
                "abnormal_flag": flag,
                "result_status": "F",
            })

    return results


def _generate_numeric_result(
    ref_low: float, ref_high: float, abnormal: bool
) -> tuple[float, str]:
    """Generate a numeric result value and abnormal flag."""
    if abnormal:
        if random.random() > 0.5:
            # High
            value = ref_high * random.uniform(1.05, 1.5)
            flag = "H"
        else:
            # Low
            value = ref_low * random.uniform(0.5, 0.95)
            flag = "L"
    else:
        value = random.uniform(ref_low, ref_high)
        flag = ""
    return value, flag


def _generate_string_result(code: str) -> str:
    """Generate string-valued result based on test code."""
    if code == "5778-6":  # Color
        return random.choice(["Yellow", "Straw", "Amber", "Dark Yellow"])
    if code == "5767-9":  # Appearance
        return random.choice(["Clear", "Slightly Cloudy", "Cloudy"])
    if code == "5804-0":  # Protein
        return random.choice(["Negative", "Trace", "1+", "2+"])
    if code == "5792-7":  # Glucose UA
        return random.choice(["Negative", "Trace", "1+"])
    return "Normal"


def get_order_profile_code(profile: str) -> tuple[str, str]:
    """Get order code and name for a profile."""
    profiles: dict[str, tuple[str, str]] = {
        "CMP": ("80053", "Comprehensive Metabolic Panel"),
        "CBC": ("85025", "Complete Blood Count with Differential"),
        "BMP": ("80048", "Basic Metabolic Panel"),
        "LIPID": ("80061", "Lipid Panel"),
        "UA": ("81001", "Urinalysis"),
        "COAG": ("85610", "Prothrombin Time/INR"),
        "TSH": ("84443", "Thyroid Stimulating Hormone"),
        "TROPONIN": ("93971", "Troponin I"),
        "HBA1C": ("83036", "Hemoglobin A1c"),
    }
    return profiles.get(profile.upper(), (profile, profile))
