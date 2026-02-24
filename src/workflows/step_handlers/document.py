"""Document step handler -> MDM^T01-T11."""

from __future__ import annotations

import random
from typing import Any

from src.core.patient import Patient
from src.data.identifiers import generate_order_number
from src.workflows.step_handlers.base import Event, StepHandler

DOCUMENT_TYPES = [
    ("HP", "History and Physical"),
    ("DS", "Discharge Summary"),
    ("CN", "Consultation Note"),
    ("PN", "Progress Note"),
    ("OP", "Operative Note"),
    ("ER", "Emergency Note"),
    ("SR", "Surgical Report"),
    ("PR", "Pathology Report"),
    ("RR", "Radiology Report"),
]

SAMPLE_TEXTS = [
    "Patient presents with chief complaint as noted. Physical examination performed. Assessment and plan documented.",
    "Patient evaluated and treated per protocol. Vital signs stable. Continue current management plan.",
    "Follow-up visit. Patient reports improvement in symptoms. Medication regimen continued without changes.",
    "Consultation requested and performed. Findings and recommendations documented in medical record.",
]


class DocumentHandler(StepHandler):
    def handle(self, patient: Patient, params: dict[str, Any]) -> list[Event]:
        doc_type = params.get("document_type", "")
        trigger = params.get("trigger", "T02")
        text = params.get("document_text", "")

        if not doc_type:
            dt = random.choice(DOCUMENT_TYPES)
            doc_type = dt[0]

        if not text:
            text = random.choice(SAMPLE_TEXTS)

        doc_id = generate_order_number("DOC")

        return [Event(
            message_type="MDM",
            trigger_event=trigger,
            patient=patient,
            kwargs={
                "document_type": doc_type,
                "document_id": doc_id,
                "document_text": text,
                "completion_status": params.get("completion_status", "AU"),
            },
        )]
