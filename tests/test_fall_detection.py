"""
tests/test_fall_detection.py

Run with:  pytest tests/ -v
Each test shows that changing input values changes the output.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pickle
import pytest
from fall_detection import run_system, get_stability, analyze_sequence


# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def models():
    """Load saved models once for the whole test module."""
    def load(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return {
        "scaler":      load("models/scaler.pkl"),
        "le_activity": load("models/le_activity.pkl"),
        "le_fall":     load("models/le_fall.pkl"),
        "best_model":  load("models/best_model.pkl"),
        "fall_model":  load("models/fall_model.pkl"),
    }


# ── Stability unit tests (no model needed) ───────────────────────────────────

class TestStability:
    def test_large_lateral_sway_is_unstable(self):
        # accel_y = 3.0 exceeds the 2.0 lateral threshold
        assert get_stability(0.0, 3.0, 9.3) == "Unstable"

    def test_large_variance_is_unstable(self):
        # values with high variance (no gravity component) → Unstable
        assert get_stability(5.0, 0.0, 3.0) == "Unstable"

    def test_extreme_lateral_sway_is_unstable(self):
        # ax far exceeds 2.0 → Unstable
        assert get_stability(4.5, 0.2, 3.5) == "Unstable"

    def test_small_lateral_accel_is_stable(self):
        # Both ax and ay well under 2.0; variance of [0.5, 0.3, 0.4] is tiny
        assert get_stability(0.5, 0.3, 0.4) == "Stable"


# ── Context awareness unit tests (no model needed) ───────────────────────────

class TestSequenceAnalysis:
    def _make_entry(self, activity, stability, ax=0.0, ay=0.0):
        return {"activity": activity, "stability": stability,
                "ax_raw": ax, "ay_raw": ay}

    def test_single_reading_is_low_risk(self):
        history = [self._make_entry("Walking", "Stable")]
        risk, pred = analyze_sequence(history)
        assert risk == "LOW"

    def test_walking_to_unstable_standing_is_high(self):
        history = [
            self._make_entry("Walking", "Stable"),
            self._make_entry("Standing", "Unstable"),
        ]
        risk, pred = analyze_sequence(history)
        assert risk == "HIGH"
        assert pred is not None

    def test_sitting_to_unstable_standing_is_medium(self):
        history = [
            self._make_entry("Sitting", "Stable"),
            self._make_entry("Standing", "Unstable"),
        ]
        risk, _ = analyze_sequence(history)
        assert risk == "MEDIUM"

    def test_forward_tilt_is_critical(self):
        history = [
            self._make_entry("Standing", "Stable"),
            self._make_entry("Standing", "Unstable", ax=4.5),  # ax > 3.0
        ]
        risk, pred = analyze_sequence(history)
        assert risk == "CRITICAL"
        assert "Forward" in pred

    def test_backward_tilt_is_critical(self):
        history = [
            self._make_entry("Walking", "Stable"),
            self._make_entry("Standing", "Unstable", ax=-4.0),  # ax < -3.0
        ]
        risk, pred = analyze_sequence(history)
        assert risk == "CRITICAL"
        assert "Backward" in pred

    def test_right_side_fall_is_critical(self):
        history = [
            self._make_entry("Standing", "Stable"),
            self._make_entry("Standing", "Unstable", ay=5.0),  # ay > 3.0
        ]
        risk, pred = analyze_sequence(history)
        assert risk == "CRITICAL"
        assert "Right" in pred


# ── Full pipeline tests (require trained models) ─────────────────────────────

class TestPipeline:
    """These tests verify end-to-end inference and that changing inputs
       changes the output as expected."""

    def _run(self, models, sample_data):
        history = []
        return run_system(
            sample_data, history,
            models["scaler"], models["best_model"], models["fall_model"],
            models["le_activity"], models["le_fall"],
        )

    def test_normal_walking_gives_low_risk(self, models):
        result = self._run(models, {
            "accel_x": 0.3, "accel_y": 0.1, "accel_z": 9.6,
            "gyro_x": 1.0,  "gyro_y": 1.0,  "gyro_z": 0.5,
        })
        assert result["risk_level"] == "LOW"
        assert result["fall_detected"] is False

    def test_upright_posture_gives_low_risk(self, models):
        result = self._run(models, {
            "accel_x": 0.05, "accel_y": 0.05, "accel_z": 9.80,
            "gyro_x": 0.2,   "gyro_y": 0.2,   "gyro_z": 0.1,
        })
        assert result["risk_level"] == "LOW"

    def test_forward_fall_detected(self, models):
        """accel_x = 5.0, accel_z = 3.0 → forward fall pattern."""
        result = self._run(models, {
            "accel_x": 5.0, "accel_y": 0.2, "accel_z": 3.0,
            "gyro_x": 8.0,  "gyro_y": 7.0,  "gyro_z": 5.0,
        })
        # Should detect a fall
        assert result["fall_detected"] is True

    def test_changing_accel_x_changes_output(self, models):
        """
        ✅ Core 'changing value → output changes' test.
        Low accel_x = safe walk; high accel_x = forward fall.
        """
        safe = self._run(models, {
            "accel_x": 0.3, "accel_y": 0.1, "accel_z": 9.6,
            "gyro_x": 1.0,  "gyro_y": 1.0,  "gyro_z": 0.5,
        })
        fall = self._run(models, {
            "accel_x": 5.5, "accel_y": 0.2, "accel_z": 3.0,
            "gyro_x": 8.0,  "gyro_y": 7.0,  "gyro_z": 5.0,
        })
        # The two samples must produce different fall_detected results
        assert safe["fall_detected"] != fall["fall_detected"], (
            "Changing accel_x from 0.3 to 5.5 should change fall_detected"
        )

    def test_changing_gyro_affects_stability(self, models):
        """High gyro values increase instability / risk."""
        calm = self._run(models, {
            "accel_x": 0.1, "accel_y": 0.1, "accel_z": 9.8,
            "gyro_x": 0.3,  "gyro_y": 0.3,  "gyro_z": 0.1,
        })
        chaotic = self._run(models, {
            "accel_x": 0.0, "accel_y": 2.5, "accel_z": 9.3,
            "gyro_x": 6.0,  "gyro_y": 6.0,  "gyro_z": 4.0,
        })
        risk_order = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        assert risk_order.index(chaotic["risk_level"]) >= risk_order.index(calm["risk_level"])

    def test_result_has_all_required_keys(self, models):
        result = self._run(models, {
            "accel_x": 0.1, "accel_y": 0.1, "accel_z": 9.8,
            "gyro_x": 0.3,  "gyro_y": 0.3,  "gyro_z": 0.1,
        })
        required = ["activity", "stability", "sequence", "risk_level",
                    "fall_detected", "fall_type", "explanation", "confidence"]
        for key in required:
            assert key in result, f"Missing key: {key}"

    def test_activity_is_valid_class(self, models):
        result = self._run(models, {
            "accel_x": 0.1, "accel_y": 0.1, "accel_z": 9.8,
            "gyro_x": 0.3,  "gyro_y": 0.3,  "gyro_z": 0.1,
        })
        assert result["activity"] in ["Sitting", "Standing", "Walking"]

    def test_risk_level_is_valid(self, models):
        result = self._run(models, {
            "accel_x": 0.1, "accel_y": 0.1, "accel_z": 9.8,
            "gyro_x": 0.3,  "gyro_y": 0.3,  "gyro_z": 0.1,
        })
        assert result["risk_level"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
