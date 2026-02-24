"""Simulation clock supporting real-time and accelerated modes."""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta


class SimulationClock:
    def __init__(self, speed: float = 1.0):
        self._speed = speed
        self._start_real = datetime.now()
        self._start_sim = datetime.now()
        self._paused = False

    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, value: float) -> None:
        self._start_sim = self.now()
        self._start_real = datetime.now()
        self._speed = max(0.1, value)

    def now(self) -> datetime:
        if self._paused:
            return self._start_sim
        elapsed = datetime.now() - self._start_real
        sim_elapsed = timedelta(seconds=elapsed.total_seconds() * self._speed)
        return self._start_sim + sim_elapsed

    def pause(self) -> None:
        self._start_sim = self.now()
        self._start_real = datetime.now()
        self._paused = True

    def resume(self) -> None:
        self._start_real = datetime.now()
        self._paused = False

    async def sleep(self, seconds: float) -> None:
        real_seconds = seconds / self._speed
        await asyncio.sleep(real_seconds)
