import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv('environmental_risk_dataset.csv')

# Feature engineering
df['hour'] = pd.to_datetime(df['timestamp']).dt.hour

le_loc = LabelEncoder()
df['location_enc'] = le_loc.fit_transform(df['location'])

# Features & target
X = df[['temperature_c', 'humidity_pct', 'light_intensity_lux', 'motion_detected', 'hour', 'location_enc']]

le_risk = LabelEncoder()
y = le_risk.fit_transform(df['risk_label'])

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train
model = RandomForestClassifier(n_estimators=100, class_weight='balanced')
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluation
print(classification_report(y_test, y_pred))

# Feature importance
pd.Series(model.feature_importances_, index=X.columns).plot(kind='bar')
plt.title("Feature Importance")
plt.show()

# Confusion matrix
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d')
plt.title("Confusion Matrix")
plt.show()
