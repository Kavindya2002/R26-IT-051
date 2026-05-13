# # ============================================================
# # system.py
# # FINAL WORKING VERSION
# # ============================================================

# import os
# import datetime
# import numpy as np
# import pandas as pd
# import tensorflow as tf
# import joblib


# # ============================================================
# # PATHS
# # ============================================================

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# MODELS_DIR = os.path.join(BASE_DIR, "models")

# FALL_DETECTION_WEIGHTS = os.path.join(
#     MODELS_DIR,
#     "fall_detection.weights.h5"
# )

# FALL_TYPE_WEIGHTS = os.path.join(
#     MODELS_DIR,
#     "fall_type.weights.h5"
# )

# XGBOOST_MODEL = os.path.join(
#     MODELS_DIR,
#     "xgboost_model.pkl"
# )

# TRAINING_COLUMNS = os.path.join(
#     MODELS_DIR,
#     "training_columns.pkl"
# )


# # ============================================================
# # LABELS
# # ============================================================

# ACTIVITY_LABELS = [

#     "bend",
#     "fall_backward",
#     "fall_forward",
#     "fall_side_left",
#     "fall_side_right",
#     "fall_slump",
#     "lie_down",
#     "sit",
#     "stand",
#     "walk"
# ]

# FALL_TYPE_LABELS = [

#     "bend",
#     "fall_backward",
#     "fall_forward",
#     "fall_side_left",
#     "fall_side_right",
#     "fall_slump",
#     "lie_down",
#     "sit",
#     "stand",
#     "walk"
# ]


# # ============================================================
# # MAIN SYSTEM
# # ============================================================

# class FallSystem:

#     def __init__(self):

#         print("\n========== LOADING SYSTEM ==========\n")

#         print("TensorFlow Version:", tf.__version__)

#         # ====================================================
#         # CHECK FILES
#         # ====================================================

#         self.check_file(FALL_DETECTION_WEIGHTS)

#         self.check_file(FALL_TYPE_WEIGHTS)

#         self.check_file(XGBOOST_MODEL)

#         self.check_file(TRAINING_COLUMNS)

#         # ====================================================
#         # LOAD MODELS
#         # ====================================================

#         self.fall_detection_model = self.load_fall_detection()

#         self.fall_type_model = self.load_fall_type()

#         self.xgb_model = joblib.load(
#             XGBOOST_MODEL
#         )

#         self.training_columns = joblib.load(
#             TRAINING_COLUMNS
#         )

#         print("\n✔ SYSTEM READY")

#         print("====================================\n")


#     # ========================================================
#     # FILE CHECK
#     # ========================================================

#     def check_file(self, path):

#         if not os.path.exists(path):

#             raise FileNotFoundError(
#                 f"\n❌ FILE NOT FOUND:\n{path}"
#             )

#         print(f"✔ Found: {os.path.basename(path)}")


#     # ========================================================
#     # BUILD FALL DETECTION MODEL
#     # ========================================================

#     def build_fall_detection_model(self):

#         model = tf.keras.Sequential([

#             tf.keras.layers.Input(
#                 shape=(50, 11)
#             ),

#             tf.keras.layers.LSTM(
#                 128,
#                 return_sequences=True
#             ),

#             tf.keras.layers.BatchNormalization(),

#             tf.keras.layers.Dropout(0.4),

#             tf.keras.layers.LSTM(
#                 128,
#                 return_sequences=True
#             ),

#             tf.keras.layers.Dropout(0.4),

#             tf.keras.layers.LSTM(64),

#             tf.keras.layers.Dropout(0.3),

#             tf.keras.layers.Dense(
#                 128,
#                 activation='relu'
#             ),

#             tf.keras.layers.Dropout(0.3),

#             tf.keras.layers.Dense(
#                 10,
#                 activation='softmax'
#             )
#         ])

#         model.compile(

#             optimizer=tf.keras.optimizers.Adam(
#                 learning_rate=0.0003
#             ),

#             loss='sparse_categorical_crossentropy',

#             metrics=['accuracy']
#         )

#         return model


#     # ========================================================
#     # BUILD FALL TYPE MODEL
#     # ========================================================

#     def build_fall_type_model(self):

#         model = tf.keras.Sequential([

#             tf.keras.layers.Input(
#                 shape=(80, 11)
#             ),

#             tf.keras.layers.LSTM(
#                 128,
#                 return_sequences=True
#             ),

#             tf.keras.layers.BatchNormalization(),

#             tf.keras.layers.Dropout(0.4),

#             tf.keras.layers.LSTM(
#                 128,
#                 return_sequences=True
#             ),

#             tf.keras.layers.Dropout(0.4),

#             tf.keras.layers.LSTM(64),

#             tf.keras.layers.Dropout(0.3),

#             tf.keras.layers.Dense(
#                 128,
#                 activation='relu'
#             ),

#             tf.keras.layers.Dropout(0.3),

#             tf.keras.layers.Dense(
#                 10,
#                 activation='softmax'
#             )
#         ])

#         model.compile(

#             optimizer=tf.keras.optimizers.Adam(
#                 learning_rate=0.0003
#             ),

#             loss='sparse_categorical_crossentropy',

#             metrics=['accuracy']
#         )

#         return model


#     # ========================================================
#     # LOAD FALL DETECTION MODEL
#     # ========================================================

#     def load_fall_detection(self):

#         print("\nLoading Fall Detection Model...")

#         model = self.build_fall_detection_model()

#         model.load_weights(
#             FALL_DETECTION_WEIGHTS
#         )

#         print("✔ Fall Detection Model Loaded")

#         return model


#     # ========================================================
#     # LOAD FALL TYPE MODEL
#     # ========================================================

#     def load_fall_type(self):

#         print("\nLoading Fall Type Model...")

#         model = self.build_fall_type_model()

#         model.load_weights(
#             FALL_TYPE_WEIGHTS
#         )

#         print("✔ Fall Type Model Loaded")

#         return model


#     # ========================================================
#     # FALL DETECTION
#     # ========================================================

#     def detect_fall(self, sensor_data):

#         print("\n===== FALL DETECTION =====")

#         data = np.array(
#             sensor_data,
#             dtype=np.float32
#         )

#         model_input = np.expand_dims(
#             data,
#             axis=0
#         )

#         prediction = self.fall_detection_model.predict(
#             model_input,
#             verbose=0
#         )

#         idx = int(
#             np.argmax(prediction[0])
#         )

#         activity = ACTIVITY_LABELS[idx]

#         print("Detected Activity:", activity)

#         return activity


#     # ========================================================
#     # FALL TYPE CLASSIFICATION
#     # ========================================================

#     def classify_fall_type(self, sensor_data):

#         print("\n===== FALL TYPE CLASSIFICATION =====")

#         data = np.array(
#             sensor_data,
#             dtype=np.float32
#         )

#         model_input = np.expand_dims(
#             data,
#             axis=0
#         )

#         prediction = self.fall_type_model.predict(
#             model_input,
#             verbose=0
#         )

#         idx = int(
#             np.argmax(prediction[0])
#         )

#         fall_type = FALL_TYPE_LABELS[idx]

#         print("Fall Type:", fall_type)

#         return fall_type


#     # ========================================================
#     # ALERT PREDICTION
#     # ========================================================

#     def predict_alert(self, risk_data):

#         print("\n===== ALERT PREDICTION =====")

#         # ----------------------------------------------------
#         # CONVERT TO DATAFRAME
#         # ----------------------------------------------------

#         df = pd.DataFrame(risk_data)

#         # ----------------------------------------------------
#         # ONE HOT ENCODING
#         # ----------------------------------------------------

#         df_encoded = pd.get_dummies(df)

#         # ----------------------------------------------------
#         # MATCH TRAINING COLUMNS
#         # ----------------------------------------------------

#         df_encoded = df_encoded.reindex(

#             columns=self.training_columns,

#             fill_value=0
#         )

#         # ----------------------------------------------------
#         # REAL XGBOOST PREDICTION
#         # ----------------------------------------------------

#         prediction = self.xgb_model.predict(
#             df_encoded
#         )[0]

#         print("Raw Prediction:", prediction)

#         # ----------------------------------------------------
#         # RISK LABELS
#         # ----------------------------------------------------

#         risk_map = {

#             0: "high",

#             1: "medium",

#             2: "low"
#         }

#         risk_level = risk_map.get(

#             int(prediction),

#             "unknown"
#         )

#         print("Risk Level:", risk_level)

#         return risk_level


#     # ========================================================
#     # POSTURE DETECTION
#     # ========================================================

#     def detect_posture(self, latest_sensor_row):

#         print("\n===== POSTURE DETECTION =====")

#         accel_z = latest_sensor_row[2]

#         if accel_z < 2:

#             posture = "lying"

#         elif accel_z < 7:

#             posture = "sitting"

#         else:

#             posture = "standing"

#         print("Posture:", posture)

#         return posture


#     # ========================================================
#     # GUIDANCE SYSTEM
#     # ========================================================

#     def generate_guidance(
#         self,
#         risk_level,
#         posture
#     ):

#         print("\n===== GUIDANCE SYSTEM =====")

#         # ====================================================
#         # HIGH RISK
#         # ====================================================

#         if risk_level == "high":

#             return [

#                 "🚨 Emergency alert triggered",

#                 "Medical assistance required immediately",

#                 "Do not move",

#                 "Caregiver notified"
#             ]


#         # ====================================================
#         # MEDIUM RISK
#         # ====================================================

#         elif risk_level == "medium":

#             return [

#                 "⚠ Caregiver alert sent",

#                 "Please remain calm",

#                 "Stay still until assistance arrives"
#             ]


#         # ====================================================
#         # LOW RISK
#         # ====================================================

#         elif risk_level == "low":

#             if posture == "lying":

#                 return [

#                     "Stay calm",

#                     "Turn sideways slowly",

#                     "Use nearby support",

#                     "Try sitting carefully",

#                     "Stand slowly if stable"
#                 ]

#             elif posture == "sitting":

#                 return [

#                     "Sit steadily",

#                     "Take deep breaths",

#                     "Stand slowly using support"
#                 ]

#             elif posture == "standing":

#                 return [

#                     "Check your balance",

#                     "Walk slowly",

#                     "Rest if needed"
#                 ]

#         return [

#             "System monitoring"
#         ]


#     # ========================================================
#     # MAIN PREDICTION
#     # ========================================================

#     def predict(
#         self,
#         fall_sensor_data,
#         type_sensor_data,
#         risk_data
#     ):

#         print("\n========== START SYSTEM ==========\n")

#         # ====================================================
#         # FALL DETECTION
#         # ====================================================

#         activity = self.detect_fall(
#             fall_sensor_data
#         )

#         # ====================================================
#         # FALL TYPE
#         # ====================================================

#         fall_type = self.classify_fall_type(
#             type_sensor_data
#         )

#         # ====================================================
#         # RISK LEVEL
#         # ====================================================

#         risk_level = self.predict_alert(
#             risk_data
#         )

#         # ====================================================
#         # POSTURE
#         # ====================================================

#         posture = self.detect_posture(
#             fall_sensor_data[-1]
#         )

#         # ====================================================
#         # GUIDANCE
#         # ====================================================

#         guidance = self.generate_guidance(
#             risk_level,
#             posture
#         )

#         # ====================================================
#         # STATUS
#         # ====================================================

#         if "fall" in activity:

#             if risk_level == "high":

#                 status = "EMERGENCY ALERT"

#             elif risk_level == "medium":

#                 status = "CAREGIVER ALERT"

#             else:

#                 status = "VOICE GUIDANCE"

#         else:

#             status = "NORMAL"


#         # ====================================================
#         # FINAL RESULT
#         # ====================================================

#         result = {

#             "status": status,

#             "activity": activity,

#             "fall_type": fall_type,

#             "risk_level": risk_level,

#             "posture": posture,

#             "guidance": guidance,

#             "time": datetime.datetime.now().strftime(
#                 "%Y-%m-%d %H:%M:%S"
#             )
#         }

#         print("\n========== FINAL RESULT ==========\n")

#         for k, v in result.items():

#             print(f"{k}: {v}")

#         print("\n==================================\n")

#         return result

# ============================================================
# system.py
# FINAL WORKING VERSION
# ============================================================

import os
import datetime
import numpy as np
import pandas as pd
import tensorflow as tf
import joblib

from load_models_fixed import (
    load_fall_detection,
    load_fall_type
)

# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODELS_DIR = os.path.join(
    BASE_DIR,
    "models"
)

FALL_DETECTION_WEIGHTS = os.path.join(
    MODELS_DIR,
    "fall_detection.weights.h5"
)

FALL_TYPE_WEIGHTS = os.path.join(
    MODELS_DIR,
    "fall_type.weights.h5"
)

XGBOOST_MODEL = os.path.join(
    MODELS_DIR,
    "xgboost_model.pkl"
)

TRAINING_COLUMNS = os.path.join(
    MODELS_DIR,
    "training_columns.pkl"
)

LABEL_ENCODER = os.path.join(
    MODELS_DIR,
    "label_encoder.pkl"
)

# ============================================================
# LABELS
# ============================================================

ACTIVITY_LABELS = [

    "bend",
    "fall_backward",
    "fall_forward",
    "fall_side_left",
    "fall_side_right",
    "fall_slump",
    "lie_down",
    "sit",
    "stand",
    "walk"
]

FALL_TYPE_LABELS = ACTIVITY_LABELS


# ============================================================
# MAIN SYSTEM
# ============================================================

class FallSystem:

    def __init__(self):

        print("\n========== LOADING SYSTEM ==========\n")

        print("TensorFlow Version:", tf.__version__)

        # ====================================================
        # CHECK FILES
        # ====================================================

        self.check_file(FALL_DETECTION_WEIGHTS)

        self.check_file(FALL_TYPE_WEIGHTS)

        self.check_file(XGBOOST_MODEL)

        self.check_file(TRAINING_COLUMNS)

        self.check_file(LABEL_ENCODER)

        # ====================================================
        # LOAD MODELS
        # ====================================================

        print("\nLoading Fall Detection Model...")

        self.fall_detection_model = load_fall_detection(
            FALL_DETECTION_WEIGHTS
        )

        print("\nLoading Fall Type Model...")

        self.fall_type_model = load_fall_type(
            FALL_TYPE_WEIGHTS
        )

        self.xgb_model = joblib.load(
            XGBOOST_MODEL
        )

        self.training_columns = joblib.load(
            TRAINING_COLUMNS
        )

        self.label_encoder = joblib.load(
            LABEL_ENCODER
        )

        print("\n✔ SYSTEM READY")

        print("====================================\n")

    # ========================================================
    # FILE CHECK
    # ========================================================

    def check_file(self, path):

        if not os.path.exists(path):

            raise FileNotFoundError(
                f"\n❌ FILE NOT FOUND:\n{path}"
            )

        print(f"✔ Found: {os.path.basename(path)}")

    # ========================================================
    # FALL DETECTION
    # ========================================================

    def detect_fall(self, sensor_data):

        print("\n===== FALL DETECTION =====")

        data = np.array(
            sensor_data,
            dtype=np.float32
        )

        model_input = np.expand_dims(
            data,
            axis=0
        )

        prediction = self.fall_detection_model.predict(
            model_input,
            verbose=0
        )

        idx = int(
            np.argmax(prediction[0])
        )

        activity = ACTIVITY_LABELS[idx]

        print("Detected Activity:", activity)

        return activity

    # ========================================================
    # FALL TYPE CLASSIFICATION
    # ========================================================

    def classify_fall_type(self, sensor_data):

        print("\n===== FALL TYPE CLASSIFICATION =====")

        data = np.array(
            sensor_data,
            dtype=np.float32
        )

        model_input = np.expand_dims(
            data,
            axis=0
        )

        prediction = self.fall_type_model.predict(
            model_input,
            verbose=0
        )

        idx = int(
            np.argmax(prediction[0])
        )

        fall_type = FALL_TYPE_LABELS[idx]

        print("Fall Type:", fall_type)

        return fall_type

    # ========================================================
    # ALERT PREDICTION
    # ========================================================

    def predict_alert(self, risk_data):

        print("\n===== ALERT PREDICTION =====")

        df = pd.DataFrame(risk_data)

        # ====================================================
        # FEATURE ENGINEERING
        # ====================================================

        df["FallSeverity"] = (

            df["RiskScore"] *

            df["ImpactForce"]
        )

        df["RecoveryRisk"] = (

            df["RecoveryTime"] *

            df["RiskScore"]
        )

        df["AgeRisk"] = (

            df["Age"] *

            df["RiskScore"]
        )

        df["GroundRisk"] = (

            df["TimeOnGround"] *

            df["RiskScore"]
        )

        # ====================================================
        # ENCODING
        # ====================================================

        df_encoded = pd.get_dummies(df)

        df_encoded = df_encoded.reindex(

            columns=self.training_columns,

            fill_value=0
        )

        # ====================================================
        # PREDICT
        # ====================================================

        prediction = self.xgb_model.predict(
            df_encoded
        )[0]

        print("Raw Prediction:", prediction)

        risk_level = self.label_encoder.inverse_transform(

            [int(prediction)]

        )[0]

        print("Predicted Alert:", risk_level)

        return risk_level

    # ========================================================
    # POSTURE DETECTION
    # ========================================================

    def detect_posture(self, latest_sensor_row):

        print("\n===== POSTURE DETECTION =====")

        accel_z = latest_sensor_row[2]

        if accel_z < 2:

            posture = "lying"

        elif accel_z < 7:

            posture = "sitting"

        else:

            posture = "standing"

        print("Posture:", posture)

        return posture

    # ========================================================
    # GUIDANCE
    # ========================================================

    def generate_guidance(
        self,
        risk_level,
        posture
    ):

        print("\n===== GUIDANCE SYSTEM =====")

        if risk_level == "Emergency Alert":

            return [

                "🚨 Emergency alert triggered",

                "Medical assistance required immediately",

                "Do not move",

                "Caregiver notified"
            ]

        elif risk_level == "Caregiver Alert":

            return [

                "⚠ Caregiver alert sent",

                "Please remain calm",

                "Stay still until assistance arrives"
            ]

        else:

            if posture == "lying":

                return [

                    "Stay calm",

                    "Turn sideways slowly",

                    "Use nearby support",

                    "Try sitting carefully",

                    "Stand slowly if stable"
                ]

            elif posture == "sitting":

                return [

                    "Sit steadily",

                    "Take deep breaths",

                    "Stand slowly using support"
                ]

            else:

                return [

                    "Check your balance",

                    "Walk slowly",

                    "Rest if needed"
                ]

    # ========================================================
    # MAIN PREDICTION
    # ========================================================

    def predict(

        self,

        fall_sensor_data,

        type_sensor_data,

        risk_data
    ):

        print("\n========== START SYSTEM ==========\n")

        activity = self.detect_fall(
            fall_sensor_data
        )

        fall_type = self.classify_fall_type(
            type_sensor_data
        )

        risk_level = self.predict_alert(
            risk_data
        )

        posture = self.detect_posture(
            fall_sensor_data[-1]
        )

        guidance = self.generate_guidance(
            risk_level,
            posture
        )

        # ====================================================
        # STATUS
        # ====================================================

        if "fall" in activity:

            if risk_level == "Emergency Alert":

                status = "EMERGENCY ALERT"

            elif risk_level == "Caregiver Alert":

                status = "CAREGIVER ALERT"

            else:

                status = "VOICE GUIDANCE"

        else:

            status = "NORMAL"

        # ====================================================
        # FINAL RESULT
        # ====================================================

        result = {

            "status": status,

            "activity": activity,

            "fall_type": fall_type,

            "risk_level": risk_level,

            "posture": posture,

            "guidance": guidance,

            "time": datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        # print("\n========== FINAL RESULT ==========\n")

        # for k, v in result.items():

        #     print(f"{k}: {v}")

        # print("\n==================================\n")

        return result