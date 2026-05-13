"""
predict.py — Run the fall-detection pipeline on test samples.

Usage:
    python src/predict.py            # runs all built-in test scenarios
    python src/predict.py --sample 3 # run only sample 3 (1-based)
"""

import argparse
import pickle
import sys
import os

# Allow running from project root
sys.path.insert(0, os.path.dirname(__file__))
from fall_detection import run_system

# ── Pre-defined test samples ─────────────────────────────────────────────────
# Changing any accel / gyro value will immediately change the output.

TEST_SAMPLES = [
    {
        "label": "Normal Walking (Stable)",
        "data": {
            "accel_x": 0.3,   # small forward lean — typical walk
            "accel_y": 0.1,
            "accel_z": 9.6,   # close to gravity (upright)
            "gyro_x":  1.0,
            "gyro_y":  1.0,
            "gyro_z":  0.5,
        },
    },
    {
        "label": "Standing Still (Stable)",
        "data": {
            "accel_x": 0.1,
            "accel_y": 0.1,
            "accel_z": 9.8,   # near 9.81 m/s² = perfectly upright
            "gyro_x":  0.5,
            "gyro_y":  0.5,
            "gyro_z":  0.2,
        },
    },
    {
        "label": "Sitting Down (Very Stable)",
        "data": {
            "accel_x": 0.02,
            "accel_y": 0.01,
            "accel_z": 9.79,
            "gyro_x":  0.1,
            "gyro_y":  0.1,
            "gyro_z":  0.05,
        },
    },
    {
        "label": "⚠️  Unstable Standing — HIGH Risk (large lateral sway)",
        "data": {
            "accel_x": 0.0,
            "accel_y": 2.5,   # ← increase this → more lateral instability
            "accel_z": 9.3,
            "gyro_x":  5.0,
            "gyro_y":  5.0,
            "gyro_z":  2.5,
        },
    },
    {
        "label": "🚨 Forward Fall (CRITICAL) — accel_x tilt > 3.0",
        "data": {
            "accel_x": 4.8,   # ← KEY VALUE: try 1.0, 3.0, 5.0 — changes risk level
            "accel_y": 0.2,
            "accel_z": 3.5,   # z drops during a fall
            "gyro_x":  7.5,
            "gyro_y":  6.0,
            "gyro_z":  4.0,
        },
    },
    {
        "label": "🚨 Backward Fall (CRITICAL) — negative accel_x",
        "data": {
            "accel_x": -5.0,  # ← negative x = falling backwards
            "accel_y":  0.2,
            "accel_z":  3.0,
            "gyro_x":   8.0,
            "gyro_y":   7.0,
            "gyro_z":   5.0,
        },
    },
    {
        "label": "🚨 Side Fall — Right (accel_y > 3.0)",
        "data": {
            "accel_x": 0.2,
            "accel_y": 5.5,   # ← positive y = falling right
            "accel_z": 2.5,
            "gyro_x":  9.0,
            "gyro_y":  9.0,
            "gyro_z":  7.0,
        },
    },
]


# ── Helpers ──────────────────────────────────────────────────────────────────

def load_models():
    required = [
        "models/scaler.pkl", "models/le_activity.pkl", "models/le_fall.pkl",
        "models/best_model.pkl", "models/fall_model.pkl",
    ]
    for p in required:
        if not os.path.exists(p):
            print(f"❌ Missing: {p}")
            print("   Run  python src/train.py  first to create the models.")
            sys.exit(1)

    def load(path):
        with open(path, "rb") as f:
            return pickle.load(f)

    return (load("models/scaler.pkl"),
            load("models/le_activity.pkl"),
            load("models/le_fall.pkl"),
            load("models/best_model.pkl"),
            load("models/fall_model.pkl"))


def print_result(result, label):
    risk_icons = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🟠", "CRITICAL": "🔴"}
    icon = risk_icons.get(result["risk_level"], "⚪")

    print(f"\n{'='*62}")
    print(f"  Test: {label}")
    print(f"{'='*62}")
    print(f"  Activity      : {result['activity']}")
    print(f"  Stability     : {result['stability']}")
    print(f"  Sequence      : {result['sequence']}")
    print(f"  Risk Level    : {icon}  {result['risk_level']}")
    if result["prediction"]:
        print(f"  Prediction    : {result['prediction']}")
        print(f"  Confidence    : {result['confidence']}%")
    print(f"  Fall Detected : {'YES ❗' if result['fall_detected'] else 'NO ✅'}")
    if result["fall_detected"]:
        print(f"  Fall Type     : {result['fall_type']}")
    print(f"\n  Insight: \"{result['explanation']}\"")
    if result["risk_level"] in ("HIGH", "CRITICAL"):
        print("\n  ⚠️  ACTION: WARNING ALERT TRIGGERED!")
    else:
        print("\n  ✅  ACTION: Normal — monitoring continues")
    print("=" * 62)


# ── Main ─────────────────────────────────────────────────────────────────────

def main(only_sample=None):
    print("🔄 Loading trained models…")
    scaler, le_activity, le_fall, best_model, fall_model = load_models()
    print("✅ Models loaded.\n")

    history = []

    samples = TEST_SAMPLES
    if only_sample is not None:
        idx = only_sample - 1
        if idx < 0 or idx >= len(TEST_SAMPLES):
            print(f"❌ Invalid sample number {only_sample}. Must be 1–{len(TEST_SAMPLES)}.")
            sys.exit(1)
        samples = [TEST_SAMPLES[idx]]
        history = []  # fresh history for single-sample run

    for i, sample in enumerate(samples, 1):
        print(f"\n📍 Sample {i}/{len(samples)}")
        result = run_system(
            sample["data"], history,
            scaler, best_model, fall_model,
            le_activity, le_fall,
        )
        print_result(result, sample["label"])

    print("\n\n💡 TIP — Edit TEST_SAMPLES in predict.py to change inputs:")
    print("   • Increase accel_x above 3.0  → Forward Fall")
    print("   • Set accel_x below -3.0      → Backward Fall")
    print("   • Set accel_y above 3.0       → Side Fall Right")
    print("   • Set accel_y below -3.0      → Side Fall Left")
    print("   • Lower accel_z (< 5.0)       → Body is no longer upright")
    print("   • Raise gyro values (> 5)     → Rapid rotation / spin")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", type=int, default=None,
                        help="Run only this sample number (1-based)")
    args = parser.parse_args()
    main(args.sample)
