# 🏥 Fall Detection System — VS Code Project

Context-Aware Activity Recognition for Early Fall Risk Detection  
Converted from Google Colab to a fully local VS Code project.

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
├── main.py                        ← Run the full pipeline (train + demo)
├── requirements.txt               ← All required Python libraries
│
├── src/
│   └── fall_detection.py          ← All model logic converted from Colab
│
├── tests/
│   └── test_sample.py             ← ⭐ CHANGE VALUES HERE to test
│
├── notebooks/
│   └── Fall_Detection_Colab.ipynb ← Original Colab notebook (reference only)
│
├── data/
│   └── fall_detection_dataset.csv ← Auto-generated on first run
│
├── models/                        ← Trained model files saved here (.pkl)
├── outputs/                       ← Results CSV saved here
│
└── .vscode/
    ├── settings.json              ← Python interpreter config
    └── launch.json                ← Pre-configured Run buttons
```

---

## Requirements

- Python 3.10 or higher — https://www.python.org/downloads/
- Visual Studio Code — https://code.visualstudio.com/
- VS Code Extensions: **Python** (Microsoft) and **Jupyter** (Microsoft)

---

## Setup Steps

### 1. Extract the project

Unzip `fall_detection_vscode.zip` to any folder on your computer.

### 2. Open in VS Code

```
File → Open Folder → select the fall_detection folder
```

### 3. Open the terminal

Press `Ctrl + `` ` `` ` (backtick) to open the integrated terminal.

### 4. Create a virtual environment

```bash
python -m venv venv
```

### 5. Activate the virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac / Linux:**
```bash
source venv/bin/activate
```

You will see `(venv)` appear at the start of the terminal prompt.

### 6. Install all libraries

```bash
pip install -r requirements.txt
```

### 7. Select the Python interpreter in VS Code

Press `Ctrl + Shift + P` → type **Python: Select Interpreter** → choose the entry that contains `venv` in the path.

---

## Running the Project

### Run the full pipeline

This generates the dataset, trains all models, and prints a demo output.

```bash
python main.py
```

First run takes about 30 seconds to train. Subsequent runs load the saved dataset from `data/`.

### Run the interactive test

```bash
python tests/test_sample.py
```

This is the file you edit to test different sensor values. Open `tests/test_sample.py`, change any number in the `TEST_SAMPLES` block, save with `Ctrl + S`, and run again.

---

## How to Test — Change Values and See Output Change

Open `tests/test_sample.py`. At the top you will find this block:

```python
TEST_SAMPLES = [
    {
        "label": "SCENARIO 1 — Normal Walking",
        "sample": {
            "accel_x":  0.3,   # ← change this
            "accel_y":  0.1,   # ← change this
            "accel_z":  9.6,   # ← change this
            "gyro_x":   1.0,
            "gyro_y":   1.0,
            "gyro_z":   0.5,
        }
    },
    ...
]
```

Edit the numbers, save the file, then run:

```bash
python tests/test_sample.py
```

The output updates immediately to reflect your new values.

---

## Sensor Value Reference

| Sensor Input | What it Represents |
|---|---|
| `accel_x` positive and large (e.g. 5.5) | Forward body lean |
| `accel_x` negative and large (e.g. -5.5) | Backward body lean |
| `accel_y` positive and large (e.g. 5.5) | Lean to the right |
| `accel_y` negative and large (e.g. -5.5) | Lean to the left |
| `accel_z` close to 9.8 | Body upright (gravity on Z axis) |
| `accel_z` below 3.0 | Body fallen / falling |
| `gyro_x/y/z` above 6.0 | Fast rotation — fall in progress |
| All gyro values below 1.0 | Slow / no rotation — stable |

---

## Quick Test Presets

Copy any of these directly into `TEST_SAMPLES` to see that scenario:

**Normal walking**
```python
"accel_x": 0.3,  "accel_y": 0.1,  "accel_z": 9.6,
"gyro_x":  1.0,  "gyro_y":  1.0,  "gyro_z":  0.5
```

**Sitting still**
```python
"accel_x": 0.01, "accel_y": 0.01, "accel_z": 9.80,
"gyro_x":  0.1,  "gyro_y":  0.1,  "gyro_z":  0.05
```

**Forward fall — CRITICAL**
```python
"accel_x": 5.5,  "accel_y": 0.2,  "accel_z": 2.5,
"gyro_x":  9.0,  "gyro_y":  8.0,  "gyro_z":  5.0
```

**Backward fall — CRITICAL**
```python
"accel_x": -5.5, "accel_y": 0.1,  "accel_z": 2.5,
"gyro_x": -8.0,  "gyro_y":  7.5,  "gyro_z":  4.0
```

**Side fall right — CRITICAL**
```python
"accel_x": 0.2,  "accel_y": 5.5,  "accel_z": 2.5,
"gyro_x":  7.0,  "gyro_y":  9.0,  "gyro_z":  4.5
```

**Unstable standing — HIGH RISK**
```python
"accel_x": 2.5,  "accel_y": 2.1,  "accel_z": 9.3,
"gyro_x":  5.0,  "gyro_y":  4.5,  "gyro_z":  2.0
```

---

## About the Dataset

In Google Colab you uploaded the CSV manually. In VS Code this is automatic:

- If `data/fall_detection_dataset.csv` already exists → it loads that file
- If the file does not exist → 10,000 rows of synthetic IMU data are generated and saved there automatically

No manual uploading is needed.

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

## Output Files

After running `main.py`, the following files are created:

| File | Contents |
|---|---|
| `data/fall_detection_dataset.csv` | Full 10,000-row synthetic dataset |
| `outputs/model_results_summary.csv` | Accuracy, Precision, Recall, F1 for all models |
| `models/*.pkl` | Saved trained model files |

---

## Troubleshooting

**`ModuleNotFoundError`** — Libraries not installed. Run `pip install -r requirements.txt` with the venv activated.

**`python` not recognised on Windows** — Try `python3` instead of `python`, or check that Python is added to PATH during installation.

**VS Code shows wrong Python version** — Press `Ctrl + Shift + P` → Python: Select Interpreter → pick the venv entry.

**Training takes too long** — In `src/fall_detection.py`, change `generate_dataset(10000)` to `generate_dataset(2000)` for faster testing.
