"""Tests for config loading."""

from src.core.config import SimulatorConfig, load_config


def test_default_config():
    config = SimulatorConfig()
    assert config.facility.sending_application == "HIS"
    assert config.scheduling.default_rate == 5.0
    assert config.patient_pool.pool_size == 500
    assert config.web.port == 8080


def test_load_config_from_file():
    config = load_config("config/default.yaml")
    assert config.facility.sending_facility == "GENERAL_HOSPITAL"
    assert config.hl7_version == "2.5.1"
    assert len(config.transport.destinations) >= 1


def test_load_config_missing_file():
    config = load_config("nonexistent.yaml")
    assert config.facility.sending_application == "HIS"


def test_scheduling_time_slots():
    config = load_config("config/default.yaml")
    assert len(config.scheduling.time_of_day) >= 1
