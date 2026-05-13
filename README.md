# 🏥 Fall Detection System

Context-Aware Activity Recognition for Early Fall Risk Detection  


---

## What This Project Does

This system reads IMU sensor data (accelerometer + gyroscope) and:

- Recognises the current activity — Sitting, Standing, or Walking
- Detects body instability in real time
- Predicts the fall type (Forward, Backward, Side Left, Side Right) **before** a fall occurs
- Assigns a risk level — LOW, MEDIUM, HIGH, or CRITICAL
- Generates a human-readable explanation of the risk

Three machine learning models are trained and compared: Decision Tree, Random Forest, and K-Nearest Neighbours. The best-performing model is used automatically.

---

## Project Folder Structure

```
fall_detection/
│
├── main.py                        
├── requirements.txt               
│
├── src/
│   └── fall_detection.py         
│
├── tests/
│   └── test_sample.py            
│
├── notebooks/
│   └── Fall_Detection_Colab.ipynb 
│
├── data/
│   └── fall_detection_dataset.csv 
│
├── models/                        
├── outputs/                       
│
└── .vscode/
    ├── settings.json             
    └── launch.json              
```

---




## Risk Level Meanings

| Risk Level | Meaning |
|---|---|
| 🟢 LOW | Normal activity, no danger detected |
| 🟡 MEDIUM | Mild instability — monitor closely |
| 🟠 HIGH | Significant instability — warning |
| 🔴 CRITICAL | Fall likely or already occurring — alert triggered |

---

## Models Used

| Model | Role |
|---|---|
| Decision Tree | Activity recognition (baseline) |
| Random Forest | Activity recognition + fall type + risk level |
| K-Nearest Neighbours | Activity recognition (comparison) |

The model with the highest accuracy on the test set is selected automatically as the best model.

---




