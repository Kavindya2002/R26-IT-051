import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier

from imblearn.over_sampling import SMOTE

import xgboost as xgb

print("Loading dataset...")

# =========================
# LOAD DATA
# =========================

df = pd.read_csv("Environmental data.csv")

print(df.head())

# =========================
# FEATURE ENGINEERING
# =========================

df['timestamp'] = pd.to_datetime(df['timestamp'])

df['hour'] = df['timestamp'].dt.hour
df['day'] = df['timestamp'].dt.day
df['month'] = df['timestamp'].dt.month
df['weekday'] = df['timestamp'].dt.weekday

# Encode location
loc_encoder = LabelEncoder()
df['location_enc'] = loc_encoder.fit_transform(df['location'])

# Features
X = df[[
    'temperature_c',
    'humidity_pct',
    'light_intensity_lux',
    'motion_detected',
    'hour',
    'day',
    'month',
    'weekday',
    'location_enc'
]]

# Encode labels
risk_encoder = LabelEncoder()
y = risk_encoder.fit_transform(df['risk_label'])

print("Classes:", risk_encoder.classes_)

# =========================
# TRAIN TEST SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# =========================
# SMOTE BALANCING
# =========================

print("Applying SMOTE...")

smote = SMOTE(random_state=42)

X_train, y_train = smote.fit_resample(X_train, y_train)

# =========================
# RANDOM FOREST
# =========================

print("\nTraining Random Forest...")

rf_model = RandomForestClassifier(
    n_estimators=300,
    max_depth=15,
    min_samples_split=5,
    class_weight='balanced',
    random_state=42
)

rf_model.fit(X_train, y_train)

rf_pred = rf_model.predict(X_test)

rf_acc = accuracy_score(y_test, rf_pred)

print("\nRandom Forest Accuracy:", rf_acc)

print(classification_report(y_test, rf_pred))

# =========================
# XGBOOST
# =========================

print("\nTraining XGBoost...")

xgb_model = xgb.XGBClassifier(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=8,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

xgb_model.fit(X_train, y_train)

xgb_pred = xgb_model.predict(X_test)

xgb_acc = accuracy_score(y_test, xgb_pred)

print("\nXGBoost Accuracy:", xgb_acc)

print(classification_report(y_test, xgb_pred))

# =========================
# SAVE MODEL
# =========================

xgb_model.save_model("best_risk_model.json")

print("\nModel saved successfully!")
