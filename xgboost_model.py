import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

# Load
df = pd.read_csv('environmental_risk_dataset.csv')

df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
df['location_enc'] = LabelEncoder().fit_transform(df['location'])

X = df[['temperature_c','humidity_pct','light_intensity_lux','motion_detected','hour','location_enc']]
y = LabelEncoder().fit_transform(df['risk_label'])

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train
model = xgb.XGBClassifier(n_estimators=200, max_depth=6)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save model
model.save_model("risk_model.json")
