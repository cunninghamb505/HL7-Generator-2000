"""Tests for clinical data generation."""

from src.data.clinical_data import generate_lab_results, get_order_profile_code


def test_generate_cmp_results():
    results = generate_lab_results("CMP")
    assert len(results) == 14  # CMP has 14 tests
    for r in results:
        assert "observation_id" in r
        assert "observation_name" in r
        assert "value" in r


def test_generate_cbc_results():
    results = generate_lab_results("CBC")
    assert len(results) == 8


def test_generate_results_abnormal_rate():
    # With 100% abnormal rate, all numeric results should have flags
    results = generate_lab_results("CBC", abnormal_rate=1.0)
    for r in results:
        if r["value_type"] == "NM":
            assert r["abnormal_flag"] in ("H", "L")


def test_order_profile_code():
    code, name = get_order_profile_code("CMP")
    assert code == "80053"
    assert "Comprehensive" in name

    code, name = get_order_profile_code("CBC")
    assert code == "85025"


def test_unknown_profile():
    code, name = get_order_profile_code("UNKNOWN")
    assert code == "UNKNOWN"
