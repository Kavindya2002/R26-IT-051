"""
tests/test_sample.py
--------------------
Interactive test: change any sensor value below and re-run.
The output WILL change to reflect your input.

Run:  python tests/test_sample.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.fall_detection import generate_dataset, train_models, run_system

# ════════════════════════════════════════════════════════════════
#  🔧 CHANGE THESE VALUES — output changes automatically
# ════════════════════════════════════════════════════════════════

TEST_SAMPLES = [
    {
        "label": "SCENARIO 1 — Normal Walking",
        "sample": {
            "accel_x":  0.3,   # small forward lean
            "accel_y":  0.1,   # minimal side lean
            "accel_z":  9.6,   # close to gravity (upright)
            "gyro_x":   1.0,   # slow rotation
            "gyro_y":   1.0,
            "gyro_z":   0.5,
        }
    },
    {
        "label": "SCENARIO 2 — Sitting Still",
        "sample": {
            "accel_x":  0.01,  # nearly zero (no lean)
            "accel_y":  0.01,
            "accel_z":  9.80,  # full gravity on Z = sitting/standing upright
            "gyro_x":   0.1,
            "gyro_y":   0.1,
            "gyro_z":   0.05,
        }
    },
    {
        "label": "SCENARIO 3 — Forward Fall (CRITICAL)",
        "sample": {
            "accel_x":  5.5,   # ← HIGH: strong forward tilt → triggers Forward Fall
            "accel_y":  0.2,
            "accel_z":  2.5,   # ← LOW: body no longer upright
            "gyro_x":   9.0,   # ← HIGH: fast spinning motion
            "gyro_y":   8.0,
            "gyro_z":   5.0,
        }
    },
    {
        "label": "SCENARIO 4 — Backward Fall (CRITICAL)",
        "sample": {
            "accel_x": -5.5,   # ← NEGATIVE: backward lean
            "accel_y":  0.1,
            "accel_z":  2.5,
            "gyro_x":  -8.0,
            "gyro_y":   7.5,
            "gyro_z":   4.0,
        }
    },
    {
        "label": "SCENARIO 5 — Side Fall Right (CRITICAL)",
        "sample": {
            "accel_x":  0.2,
            "accel_y":  5.5,   # ← HIGH Y: rightward lean
            "accel_z":  2.5,
            "gyro_x":   7.0,
            "gyro_y":   9.0,
            "gyro_z":   4.5,
        }
    },
    {
        "label": "SCENARIO 6 — Unstable Standing (HIGH RISK)",
        "sample": {
            "accel_x":  2.5,   # moderate lean — unstable but not fallen yet
            "accel_y":  2.1,
            "accel_z":  9.3,
            "gyro_x":   5.0,
            "gyro_y":   4.5,
            "gyro_z":   2.0,
        }
    },
]

# ════════════════════════════════════════════════════════════════
#  🚀 Run Test — do not modify below this line
# ════════════════════════════════════════════════════════════════

def run_tests():
    print("=" * 65)
    print("  🏥 FALL DETECTION — Interactive Test")
    print("  Change values in TEST_SAMPLES above and re-run!")
    print("=" * 65)

    print("\n⚙️  Training models (first run only — ~30s)...\n")
    df = generate_dataset(10000)
    trained = train_models(df)
    print(f"✅ Models ready.  Best model: {trained['best_model_name']}\n")

    for test in TEST_SAMPLES:
        history = []  # fresh history per scenario
        result = run_system(test["sample"], history, trained)

        risk_icon = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🟠", "CRITICAL": "🔴"}.get(result['risk_level'], "⚪")
        fall_icon = "❗" if result['fall_type'] != 'No Fall' else "✅"

        print(f"┌─ {test['label']}")
        print(f"│  Activity   : {result['activity']}")
        print(f"│  Stability  : {result['stability']}")
        print(f"│  Risk Level : {risk_icon} {result['risk_level']}")
        if result['prediction']:
            print(f"│  Prediction : {result['prediction']}  ({result['confidence']}% confidence)")
        print(f"│  Fall Type  : {fall_icon} {result['fall_type']}")
        print(f"│  Insight    : {result['explanation']}")
        print(f"└{'─'*62}\n")

    print("=" * 65)
    print("  💡 TIP: Edit accel_x / accel_y / accel_z values:")
    print("     accel_x  → + forward lean  |  - backward lean")
    print("     accel_y  → + right lean    |  - left lean")
    print("     accel_z  → ~9.8 upright    |  <3.0 falling")
    print("     gyro_*   → higher = faster rotation")
    print("=" * 65)

if __name__ == "__main__":
    run_tests()
