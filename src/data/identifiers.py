"""Thread-safe identifier generators for MRN, order numbers, etc."""

from __future__ import annotations

import random
import threading
from datetime import datetime


class _Counter:
    def __init__(self, start: int = 1):
        self._value = start
        self._lock = threading.Lock()

    def next(self) -> int:
        with self._lock:
            val = self._value
            self._value += 1
            return val


_mrn_counter = _Counter(100000)
_account_counter = _Counter(200000)
_visit_counter = _Counter(300000)
_order_counter = _Counter(400000)
_message_control_counter = _Counter(1)


def generate_mrn() -> str:
    return f"MRN{_mrn_counter.next():07d}"


def generate_account_number() -> str:
    return f"ACCT{_account_counter.next():07d}"


def generate_visit_number() -> str:
    return f"VN{_visit_counter.next():07d}"


def generate_order_number(prefix: str = "ORD") -> str:
    return f"{prefix}{_order_counter.next():07d}"


def generate_placer_order_number() -> str:
    return generate_order_number("PLC")


def generate_filler_order_number() -> str:
    return generate_order_number("FIL")


def generate_message_control_id() -> str:
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    seq = _message_control_counter.next()
    return f"{ts}.{seq:06d}"


def generate_doctor_id() -> str:
    return f"DR{random.randint(10000, 99999)}"
