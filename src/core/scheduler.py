"""Time-of-day rate control scheduler."""

from __future__ import annotations

import random
from datetime import datetime, time

from src.core.config import SchedulingConfig, TimeSlot


class Scheduler:
    def __init__(self, config: SchedulingConfig):
        self._config = config
        self._rate_override: float | None = None

    @property
    def current_rate(self) -> float:
        """Get current message rate (messages per minute)."""
        if self._rate_override is not None:
            return self._rate_override
        return self._get_time_based_rate()

    @property
    def interval(self) -> float:
        """Seconds between workflow launches."""
        rate = self.current_rate
        if rate <= 0:
            return 60.0
        return 60.0 / rate

    def set_rate(self, rate: float) -> None:
        """Override the rate (set to None to use time-based)."""
        self._rate_override = rate if rate > 0 else None

    def clear_override(self) -> None:
        self._rate_override = None

    def jittered_interval(self) -> float:
        """Get interval with some randomness to avoid perfectly regular spacing."""
        base = self.interval
        jitter = base * random.uniform(-0.3, 0.3)
        return max(0.1, base + jitter)

    def _get_time_based_rate(self) -> float:
        """Determine rate based on current time of day."""
        now = datetime.now().time()

        for slot in self._config.time_of_day:
            start = _parse_time(slot.start)
            end = _parse_time(slot.end)

            if start <= end:
                if start <= now <= end:
                    return slot.rate
            else:
                # Crosses midnight
                if now >= start or now <= end:
                    return slot.rate

        return self._config.default_rate


def _parse_time(time_str: str) -> time:
    """Parse HH:MM string to time object."""
    parts = time_str.split(":")
    return time(int(parts[0]), int(parts[1]) if len(parts) > 1 else 0)
