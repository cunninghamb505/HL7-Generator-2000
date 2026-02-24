"""Validation rules per HL7 message type."""

from __future__ import annotations

RULES: dict[str, dict] = {
    "ADT": {
        "required_segments": ["MSH", "EVN", "PID", "PV1"],
        "optional_segments": ["NK1", "PV2", "AL1", "DG1", "IN1", "IN2", "IN3", "MRG", "GT1"],
        "field_rules": {
            "MSH.9": {"required": True, "description": "Message Type"},
            "MSH.10": {"required": True, "description": "Message Control ID"},
            "PID.3": {"required": True, "description": "Patient Identifier List"},
            "PID.5": {"required": True, "description": "Patient Name"},
            "PV1.2": {"required": True, "description": "Patient Class"},
        },
    },
    "ORM": {
        "required_segments": ["MSH", "PID", "ORC", "OBR"],
        "optional_segments": ["PV1", "NTE", "DG1", "IN1"],
        "field_rules": {
            "MSH.9": {"required": True, "description": "Message Type"},
            "MSH.10": {"required": True, "description": "Message Control ID"},
            "PID.3": {"required": True, "description": "Patient Identifier List"},
            "ORC.1": {"required": True, "description": "Order Control"},
            "OBR.4": {"required": True, "description": "Universal Service ID"},
        },
    },
    "ORU": {
        "required_segments": ["MSH", "PID", "OBR", "OBX"],
        "optional_segments": ["PV1", "ORC", "NTE"],
        "field_rules": {
            "MSH.9": {"required": True, "description": "Message Type"},
            "MSH.10": {"required": True, "description": "Message Control ID"},
            "PID.3": {"required": True, "description": "Patient Identifier List"},
            "OBR.4": {"required": True, "description": "Universal Service ID"},
            "OBX.3": {"required": True, "description": "Observation Identifier"},
            "OBX.5": {"required": True, "description": "Observation Value"},
        },
    },
    "RDE": {
        "required_segments": ["MSH", "PID", "ORC", "RXE"],
        "optional_segments": ["PV1", "AL1", "NTE"],
        "field_rules": {
            "MSH.9": {"required": True, "description": "Message Type"},
            "PID.3": {"required": True, "description": "Patient Identifier List"},
            "ORC.1": {"required": True, "description": "Order Control"},
            "RXE.2": {"required": True, "description": "Give Code"},
        },
    },
    "RDS": {
        "required_segments": ["MSH", "PID", "ORC", "RXD"],
        "optional_segments": ["PV1"],
        "field_rules": {
            "MSH.9": {"required": True, "description": "Message Type"},
            "PID.3": {"required": True, "description": "Patient Identifier List"},
            "RXD.2": {"required": True, "description": "Dispense/Give Code"},
        },
    },
    "MDM": {
        "required_segments": ["MSH", "EVN", "PID", "PV1", "TXA"],
        "optional_segments": ["OBX"],
        "field_rules": {
            "MSH.9": {"required": True, "description": "Message Type"},
            "PID.3": {"required": True, "description": "Patient Identifier List"},
            "TXA.2": {"required": True, "description": "Document Type"},
        },
    },
    "DFT": {
        "required_segments": ["MSH", "EVN", "PID", "PV1", "FT1"],
        "optional_segments": ["DG1", "IN1", "GT1"],
        "field_rules": {
            "MSH.9": {"required": True, "description": "Message Type"},
            "PID.3": {"required": True, "description": "Patient Identifier List"},
            "FT1.4": {"required": True, "description": "Transaction Date"},
            "FT1.6": {"required": True, "description": "Transaction Type"},
        },
    },
    "VXU": {
        "required_segments": ["MSH", "PID", "ORC", "RXA"],
        "optional_segments": ["PV1", "NK1", "RXR", "OBX"],
        "field_rules": {
            "MSH.9": {"required": True, "description": "Message Type"},
            "PID.3": {"required": True, "description": "Patient Identifier List"},
            "RXA.5": {"required": True, "description": "Administered Code"},
        },
    },
    "BAR": {
        "required_segments": ["MSH", "EVN", "PID", "PV1"],
        "optional_segments": ["DG1", "IN1", "GT1", "FT1"],
        "field_rules": {
            "MSH.9": {"required": True, "description": "Message Type"},
            "PID.3": {"required": True, "description": "Patient Identifier List"},
        },
    },
    "SIU": {
        "required_segments": ["MSH", "SCH", "PID"],
        "optional_segments": ["PV1", "AIG", "AIL", "AIP", "NTE"],
        "field_rules": {
            "MSH.9": {"required": True, "description": "Message Type"},
            "SCH.1": {"required": True, "description": "Placer Appointment ID"},
            "PID.3": {"required": True, "description": "Patient Identifier List"},
        },
    },
    "MFN": {
        "required_segments": ["MSH", "MFI", "MFE"],
        "optional_segments": [],
        "field_rules": {
            "MSH.9": {"required": True, "description": "Message Type"},
            "MFI.1": {"required": True, "description": "Master File Identifier"},
        },
    },
    "ACK": {
        "required_segments": ["MSH", "MSA"],
        "optional_segments": ["ERR"],
        "field_rules": {
            "MSH.9": {"required": True, "description": "Message Type"},
            "MSA.1": {"required": True, "description": "Acknowledgment Code"},
        },
    },
}
