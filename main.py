"""
main.py — Run the complete Fall Detection pipeline
Usage: python main.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from src.fall_detection import generate_dataset, train_models, run_system

def main():
    print("=" * 60)
    print("  🏥 Fall Detection System — VS Code Version")
    print("=" * 60)

    # ── Step 1: Dataset ──────────────────────────────────────
    csv_path = "data/fall_detection_dataset.csv"
    if os.path.exists(csv_path):
        import pandas as pd
        df = pd.read_csv(csv_path)
        print(f"✅ Loaded dataset from {csv_path}: {df.shape}")
    else:
        print("⚙️  Generating synthetic dataset (10,000 rows)...")
        df = generate_dataset(10000)
        os.makedirs("data", exist_ok=True)
        df.to_csv(csv_path, index=False)
        print(f"✅ Dataset generated and saved to {csv_path}: {df.shape}")

    # ── Step 2: Train ────────────────────────────────────────
    print("\n⚙️  Training models — this may take ~30 seconds...")
    trained = train_models(df)
    print(f"\n🏆 Best model: {trained['best_model_name']}")
    for name, scores in trained['results'].items():
        print(f"   {name}: Accuracy={scores['Accuracy']*100:.1f}%  F1={scores['F1-Score']*100:.1f}%")

    # ── Step 3: Demo Readings ────────────────────────────────
    history = []
    readings = [
        ("Walking (Stable)",        {'accel_x':0.3,  'accel_y':0.1,  'accel_z':9.6, 'gyro_x':1.0, 'gyro_y':1.0, 'gyro_z':0.5}),
        ("Standing (Stable)",       {'accel_x':0.1,  'accel_y':0.1,  'accel_z':9.8, 'gyro_x':0.5, 'gyro_y':0.5, 'gyro_z':0.2}),
        ("Unstable + Forward Tilt", {'accel_x':4.8,  'accel_y':0.2,  'accel_z':3.5, 'gyro_x':7.5, 'gyro_y':6.0, 'gyro_z':4.0}),
    ]
    for label, sample in readings:
        print(f"\n{'─'*60}")
        print(f"📍 {label}")
        result = run_system(sample, history, trained)
        print(f"   Activity   : {result['activity']}")
        print(f"   Stability  : {result['stability']}")
        print(f"   Sequence   : {result['sequence']}")
        print(f"   Risk Level : {result['risk_level']}")
        if result['prediction']:
            print(f"   Prediction : {result['prediction']}  (Confidence: {result['confidence']}%)")
        print(f"   Fall Type  : {result['fall_type']}")
        print(f"   Insight    : {result['explanation']}")
        if result['alert']:
            print("   ⚠️  WARNING ALERT TRIGGERED!")
        else:
            print("   ✅ Normal — monitoring continues")

if __name__ == "__main__":
    main()
