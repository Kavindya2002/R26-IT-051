# # # # import h5py

# # # # from tensorflow.keras.models import Sequential
# # # # from tensorflow.keras.layers import (
# # # #     LSTM,
# # # #     Dense,
# # # #     Dropout,
# # # #     BatchNormalization
# # # # )

# # # # # ==================================================
# # # # # FALL DETECTION MODEL
# # # # # ==================================================
# # # # def load_fall_detection():

# # # #     model = Sequential([

# # # #         LSTM(
# # # #             64,
# # # #             return_sequences=True,
# # # #             input_shape=(50, 11)
# # # #         ),

# # # #         Dropout(0.3),

# # # #         LSTM(64),

# # # #         Dropout(0.3),

# # # #         Dense(32, activation='relu'),

# # # #         Dense(10, activation='softmax')
# # # #     ])

# # # #     with h5py.File(
# # # #         "models/fall_detection_model.h5",
# # # #         "r"
# # # #     ) as f:

# # # #         layer_names = [
# # # #             n.decode() if isinstance(n, bytes) else n
# # # #             for n in f["model_weights"].attrs["layer_names"]
# # # #         ]

# # # #         weights = []

# # # #         for layer_name in layer_names:

# # # #             group = f["model_weights"][layer_name]

# # # #             weight_names = [
# # # #                 n.decode() if isinstance(n, bytes) else n
# # # #                 for n in group.attrs["weight_names"]
# # # #             ]

# # # #             for w in weight_names:
# # # #                 weights.append(group[w][()])

# # # #     model.set_weights(weights)

# # # #     print("✔ Fall Detection Model Loaded")

# # # #     return model


# # # # # ==================================================
# # # # # FALL TYPE MODEL
# # # # # ==================================================
# # # # def load_fall_type():

# # # #     model = Sequential([

# # # #         LSTM(
# # # #             128,
# # # #             return_sequences=True,
# # # #             input_shape=(80, 11)
# # # #         ),

# # # #         BatchNormalization(),

# # # #         Dropout(0.4),

# # # #         LSTM(
# # # #             128,
# # # #             return_sequences=True
# # # #         ),

# # # #         Dropout(0.4),

# # # #         LSTM(64),

# # # #         Dropout(0.3),

# # # #         Dense(128, activation='relu'),

# # # #         Dropout(0.3),

# # # #         Dense(3, activation='softmax')
# # # #     ])

# # # #     with h5py.File(
# # # #         "models/fall_type_model.h5",
# # # #         "r"
# # # #     ) as f:

# # # #         layer_names = [
# # # #             n.decode() if isinstance(n, bytes) else n
# # # #             for n in f["model_weights"].attrs["layer_names"]
# # # #         ]

# # # #         weights = []

# # # #         for layer_name in layer_names:

# # # #             group = f["model_weights"][layer_name]

# # # #             weight_names = [
# # # #                 n.decode() if isinstance(n, bytes) else n
# # # #                 for n in group.attrs["weight_names"]
# # # #             ]

# # # #             for w in weight_names:
# # # #                 weights.append(group[w][()])

# # # #     model.set_weights(weights)

# # # #     print("✔ Fall Type Model Loaded")

# # # #     return model

# # # # ============================================================
# # # # load_models_fixed.py
# # # # ============================================================

# # # # ============================================================
# # # # load_models_fixed.py
# # # # FINAL CORRECT VERSION
# # # # ============================================================

# # # import h5py

# # # from tensorflow.keras.models import Sequential
# # # from tensorflow.keras.layers import (
# # #     LSTM,
# # #     Dense,
# # #     Dropout,
# # #     BatchNormalization
# # # )

# # # # ============================================================
# # # # FALL DETECTION MODEL
# # # # ============================================================

# # # def load_fall_detection():

# # #     model = Sequential([

# # #         LSTM(
# # #             64,
# # #             return_sequences=True,
# # #             input_shape=(50, 11)
# # #         ),

# # #         Dropout(0.3),

# # #         LSTM(64),

# # #         Dropout(0.3),

# # #         Dense(
# # #             32,
# # #             activation='relu'
# # #         ),

# # #         Dense(
# # #             10,
# # #             activation='softmax'
# # #         )
# # #     ])

# # #     with h5py.File(
# # #         "models/fall_detection.weights.h5",
# # #         "r"
# # #     ) as f:

# # #         layer_names = [
# # #             n.decode() if isinstance(n, bytes) else n
# # #             for n in f["model_weights"].attrs["layer_names"]
# # #         ]

# # #         weights = []

# # #         for layer_name in layer_names:

# # #             group = f["model_weights"][layer_name]

# # #             weight_names = [
# # #                 n.decode() if isinstance(n, bytes) else n
# # #                 for n in group.attrs["weight_names"]
# # #             ]

# # #             for w in weight_names:
# # #                 weights.append(group[w][()])

# # #     model.set_weights(weights)

# # #     print("✔ Fall Detection Model Loaded")

# # #     return model


# # # # ============================================================
# # # # FALL TYPE MODEL
# # # # ============================================================

# # # def load_fall_type():

# # #     model = Sequential([

# # #         LSTM(
# # #             128,
# # #             return_sequences=True,
# # #             input_shape=(80, 11)
# # #         ),

# # #         BatchNormalization(),

# # #         Dropout(0.4),

# # #         LSTM(
# # #             128,
# # #             return_sequences=True
# # #         ),

# # #         Dropout(0.4),

# # #         LSTM(64),

# # #         Dropout(0.3),

# # #         Dense(
# # #             128,
# # #             activation='relu'
# # #         ),

# # #         Dropout(0.3),

# # #         Dense(
# # #             10,
# # #             activation='softmax'
# # #         )
# # #     ])

# # #     with h5py.File(
# # #         "models/fall_type.weights.h5",
# # #         "r"
# # #     ) as f:

# # #         layer_names = [
# # #             n.decode() if isinstance(n, bytes) else n
# # #             for n in f["model_weights"].attrs["layer_names"]
# # #         ]

# # #         weights = []

# # #         for layer_name in layer_names:

# # #             group = f["model_weights"][layer_name]

# # #             weight_names = [
# # #                 n.decode() if isinstance(n, bytes) else n
# # #                 for n in group.attrs["weight_names"]
# # #             ]

# # #             for w in weight_names:
# # #                 weights.append(group[w][()])

# # #     model.set_weights(weights)

# # #     print("✔ Fall Type Model Loaded")

# # #     return model

# # from tensorflow.keras.models import Sequential
# # from tensorflow.keras.layers import (
# #     LSTM,
# #     Dense,
# #     Dropout,
# #     BatchNormalization
# # )

# # # ==================================================
# # # FALL DETECTION MODEL
# # # ==================================================

# # def load_fall_detection():

# #     model = Sequential([

# #         LSTM(
# #             64,
# #             return_sequences=True,
# #             input_shape=(50, 11)
# #         ),

# #         Dropout(0.3),

# #         LSTM(64),

# #         Dropout(0.3),

# #         Dense(32, activation='relu'),

# #         Dense(10, activation='softmax')
# #     ])

# #     model.load_weights(
# #         "models/fall_detection.weights.h5"
# #     )

# #     print("✔ Fall Detection Model Loaded")

# #     return model


# # # ==================================================
# # # FALL TYPE MODEL
# # # ==================================================

# # def load_fall_type():

# #     model = Sequential([

# #         LSTM(
# #             128,
# #             return_sequences=True,
# #             input_shape=(80, 11)
# #         ),

# #         BatchNormalization(),

# #         Dropout(0.4),

# #         LSTM(
# #             128,
# #             return_sequences=True
# #         ),

# #         Dropout(0.4),

# #         LSTM(64),

# #         Dropout(0.3),

# #         Dense(128, activation='relu'),

# #         Dropout(0.3),

# #         Dense(10, activation='softmax')
# #     ])

# #     model.load_weights(
# #         "models/fall_type.weights.h5"
# #     )

# #     print("✔ Fall Type Model Loaded")

# #     return model

# # ============================================================
# # load_models_fixed.py
# # FINAL UPDATED VERSION
# # ============================================================

# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import (
#     LSTM,
#     Dense,
#     Dropout,
#     BatchNormalization
# )

# # ============================================================
# # FALL DETECTION MODEL
# # ============================================================

# def load_fall_detection():

#     model = Sequential([

#         # ====================================================
#         # LSTM 1
#         # ====================================================

#         LSTM(
#             128,
#             return_sequences=True,
#             input_shape=(50, 11)
#         ),

#         Dropout(0.3),

#         # ====================================================
#         # LSTM 2
#         # ====================================================

#         LSTM(
#             128
#         ),

#         Dropout(0.3),

#         # ====================================================
#         # DENSE
#         # ====================================================

#         Dense(
#             64,
#             activation='relu'
#         ),

#         # ====================================================
#         # OUTPUT
#         # ====================================================

#         Dense(
#             10,
#             activation='softmax'
#         )
#     ])

#     # ========================================================
#     # LOAD WEIGHTS
#     # ========================================================

#     model.load_weights(
#         "models/fall_detection.weights.h5"
#     )

#     print("✔ Fall Detection Model Loaded")

#     return model


# # ============================================================
# # FALL TYPE MODEL
# # ============================================================

# def load_fall_type():

#     model = Sequential([

#         # ====================================================
#         # LSTM 1
#         # ====================================================

#         LSTM(
#             128,
#             return_sequences=True,
#             input_shape=(80, 11)
#         ),

#         BatchNormalization(),

#         Dropout(0.4),

#         # ====================================================
#         # LSTM 2
#         # ====================================================

#         LSTM(
#             128,
#             return_sequences=True
#         ),

#         Dropout(0.4),

#         # ====================================================
#         # LSTM 3
#         # ====================================================

#         LSTM(
#             64
#         ),

#         Dropout(0.3),

#         # ====================================================
#         # DENSE
#         # ====================================================

#         Dense(
#             128,
#             activation='relu'
#         ),

#         Dropout(0.3),

#         # ====================================================
#         # OUTPUT
#         # ====================================================

#         Dense(
#             10,
#             activation='softmax'
#         )
#     ])

#     # ========================================================
#     # LOAD WEIGHTS
#     # ========================================================

#     model.load_weights(
#         "models/fall_type.weights.h5"
#     )

#     print("✔ Fall Type Model Loaded")

#     return model

# ============================================================
# load_models_fixed.py
# ============================================================

import tensorflow as tf


# ============================================================
# FALL DETECTION MODEL
# ============================================================

def load_fall_detection(weights_path):

    model = tf.keras.Sequential([

        tf.keras.layers.Input(
            shape=(50, 11)
        ),

        tf.keras.layers.LSTM(
            128,
            return_sequences=True
        ),

        tf.keras.layers.BatchNormalization(),

        tf.keras.layers.Dropout(0.4),

        tf.keras.layers.LSTM(
            128,
            return_sequences=True
        ),

        tf.keras.layers.Dropout(0.4),

        tf.keras.layers.LSTM(64),

        tf.keras.layers.Dropout(0.3),

        tf.keras.layers.Dense(
            128,
            activation='relu'
        ),

        tf.keras.layers.Dropout(0.3),

        tf.keras.layers.Dense(
            10,
            activation='softmax'
        )
    ])

    model.compile(

        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.0003
        ),

        loss='sparse_categorical_crossentropy',

        metrics=['accuracy']
    )

    model.load_weights(
        weights_path
    )

    print("✔ Fall Detection Model Loaded")

    return model


# ============================================================
# FALL TYPE MODEL
# ============================================================

def load_fall_type(weights_path):

    model = tf.keras.Sequential([

        tf.keras.layers.Input(
            shape=(80, 11)
        ),

        tf.keras.layers.LSTM(
            128,
            return_sequences=True
        ),

        tf.keras.layers.BatchNormalization(),

        tf.keras.layers.Dropout(0.4),

        tf.keras.layers.LSTM(
            128,
            return_sequences=True
        ),

        tf.keras.layers.Dropout(0.4),

        tf.keras.layers.LSTM(64),

        tf.keras.layers.Dropout(0.3),

        tf.keras.layers.Dense(
            128,
            activation='relu'
        ),

        tf.keras.layers.Dropout(0.3),

        tf.keras.layers.Dense(
            10,
            activation='softmax'
        )
    ])

    model.compile(

        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.0003
        ),

        loss='sparse_categorical_crossentropy',

        metrics=['accuracy']
    )

    model.load_weights(
        weights_path
    )

    print("✔ Fall Type Model Loaded")

    return model