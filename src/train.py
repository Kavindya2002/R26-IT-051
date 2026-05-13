"""
train.py — Train and save all fall-detection models.

Usage:
    python src/train.py                        # generate synthetic data
    python src/train.py --csv data/my_data.csv # use your own CSV
"""

import argparse
import os
import pickle
import pandas as pd
from fall_detection import (
    generate_dataset, preprocess, train_models, FEATURE_COLS
)


def main(csv_path=None):
    # ── 1. Load or generate dataset ────────────────────────────
    if csv_path and os.path.exists(csv_path):
        print(f"📂 Loading dataset from: {csv_path}")
        df = pd.read_csv(csv_path)
    else:
        print("🔧 Generating synthetic dataset (10 000 rows)…")
        df = generate_dataset(10000)
        os.makedirs("data", exist_ok=True)
        df.to_csv("data/fall_detection_dataset.csv", index=False)
        print("✅ Dataset saved → data/fall_detection_dataset.csv")

    print(f"   Shape: {df.shape}")
    print(f"   Activities : {df['activity'].value_counts().to_dict()}")

    # ── 2. Preprocess ──────────────────────────────────────────
    print("\n⚙️  Preprocessing…")
    (scaler, le_activity, le_fall, le_risk,
     X_train, X_test,
     y_act_train, y_act_test,
     y_fall_train, y_fall_test,
     y_risk_train, y_risk_test) = preprocess(df)

    # ── 3. Train ───────────────────────────────────────────────
    print("🤖 Training models…")
    (trained_models, best_model, best_name,
     fall_model, risk_model, results) = train_models(
        X_train, X_test,
        y_act_train, y_act_test,
        y_fall_train, y_fall_test,
        y_risk_train, y_risk_test
    )

    # ── 4. Print results ────────────────────────────────────────
    print("\n" + "=" * 50)
    print("       MODEL RESULTS")
    print("=" * 50)
    for name, metrics in results.items():
        status = "✅" if metrics['Accuracy'] >= 0.80 else "⚠️"
        print(f"\n── {name} {status}")
        for k, v in metrics.items():
            print(f"   {k:10s}: {v*100:.2f}%")
    print(f"\n🏆 Best Model: {best_name}  ({results[best_name]['Accuracy']*100:.2f}%)")
    print("=" * 50)

    # ── 5. Save models ──────────────────────────────────────────
    os.makedirs("models", exist_ok=True)
    artifacts = {
        "models/scaler.pkl":      scaler,
        "models/le_activity.pkl": le_activity,
        "models/le_fall.pkl":     le_fall,
        "models/le_risk.pkl":     le_risk,
        "models/best_model.pkl":  best_model,
        "models/fall_model.pkl":  fall_model,
        "models/risk_model.pkl":  risk_model,
    }
    for path, obj in artifacts.items():
        with open(path, "wb") as f:
            pickle.dump(obj, f)

    # Save best model name
    with open("models/best_model_name.txt", "w") as f:
        f.write(best_name)

    print("\n✅ All models saved to models/")
    print("   Run  python src/predict.py  to test predictions.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", help="Path to your own CSV dataset", default=None)
    args = parser.parse_args()
    main(args.csv)
