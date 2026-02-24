"""Pydantic config models and YAML loader."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class FacilityConfig(BaseModel):
    sending_application: str = "HIS"
    sending_facility: str = "GENERAL_HOSPITAL"
    receiving_application: str = ""
    receiving_facility: str = ""


class TimeSlot(BaseModel):
    start: str = "00:00"
    end: str = "23:59"
    rate: float = 5.0


class SchedulingConfig(BaseModel):
    default_rate: float = 5.0
    time_of_day: list[TimeSlot] = Field(default_factory=list)


class DestinationConfig(BaseModel):
    name: str = "default"
    type: str = "console"  # mllp, file, console
    host: str = "127.0.0.1"
    port: int = 2575
    enabled: bool = True
    file_path: str = ""


class TransportConfig(BaseModel):
    destinations: list[DestinationConfig] = Field(
        default_factory=lambda: [DestinationConfig()]
    )


class PatientPoolConfig(BaseModel):
    pool_size: int = 500
    min_age: int = 1
    max_age: int = 95
    insurance_rate: float = 0.85  # 0.0-1.0, percentage of patients with insurance


class AuthConfig(BaseModel):
    username: str = "admin"
    password: str = "admin"


class WebConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080
    enabled: bool = True


class SimulatorConfig(BaseModel):
    facility: FacilityConfig = Field(default_factory=FacilityConfig)
    scheduling: SchedulingConfig = Field(default_factory=SchedulingConfig)
    transport: TransportConfig = Field(default_factory=TransportConfig)
    patient_pool: PatientPoolConfig = Field(default_factory=PatientPoolConfig)
    web: WebConfig = Field(default_factory=WebConfig)
    auth: AuthConfig = Field(default_factory=AuthConfig)
    hl7_version: str = "2.5.1"
    auto_start: bool = False
    workflows_dir: str = "config/workflows"
    value_sets_dir: str = "config/value_sets"


def load_config(path: str | Path | None = None) -> SimulatorConfig:
    """Load config from YAML file, falling back to defaults.

    Environment variables HL7GEN_USERNAME and HL7GEN_PASSWORD override
    the auth config (useful for Docker deployments with .env files).
    """
    import os

    if path is None:
        path = Path("config/default.yaml")
    else:
        path = Path(path)

    if path.exists():
        with open(path) as f:
            raw: dict[str, Any] = yaml.safe_load(f) or {}
        config = SimulatorConfig(**raw)
    else:
        config = SimulatorConfig()

    # Env vars override auth config
    env_user = os.environ.get("HL7GEN_USERNAME")
    env_pass = os.environ.get("HL7GEN_PASSWORD")
    if env_user:
        config.auth.username = env_user
    if env_pass:
        config.auth.password = env_pass

    return config
