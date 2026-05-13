# ============================================================
# test_medium_risk.py
# MEDIUM RISK TEST VERSION
# ============================================================

from system import FallSystem


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n===== STARTING MEDIUM RISK TEST =====\n")

    # ========================================================
    # CREATE SYSTEM
    # ========================================================

    try:

        system = FallSystem()

    except Exception as e:

        print("\n❌ SYSTEM INITIALIZATION FAILED")

        print(e)

        return

    # ========================================================
    # MEDIUM RISK SENSOR DATA
    # Shape: (50, 11)
    # ========================================================

    fall_50 = []

    for i in range(50):

        row = [

            # accel_x
            4.5,

            # accel_y
            3.8,

            # accel_z
            2.5,

            # gyro_x
            2.2,

            # gyro_y
            2.0,

            # gyro_z
            1.8,

            # pitch
            30.0,

            # roll
            25.0,

            # yaw
            20.0,

            # accel_mag
            6.5,

            # gyro_mag
            3.5
        ]

        fall_50.append(row)

    # ========================================================
    # MEDIUM RISK FALL TYPE DATA
    # Shape: (80, 11)
    # ========================================================

    type_80 = []

    for i in range(80):

        row = [

            4.8,
            4.0,
            2.0,
            2.5,
            2.2,
            2.0,
            35.0,
            30.0,
            25.0,
            7.0,
            4.0
        ]

        type_80.append(row)

    # ========================================================
    # MEDIUM RISK ALERT INPUT
    # ========================================================

    risk_data = {

        "RiskScore": [0.55],

        "Age": [72],

        "PreviousFalls": [3],

        "Location": ["bathroom"],

        "Time": ["evening"],

        "Movement": ["unstable"],

        "AssistiveDevice": ["walker"],

        # ====================================================
        # EXTRA FEATURES
        # ====================================================

        "ImpactForce": [5.5],

        "RecoveryTime": [35],

        "TimeOnGround": [40],

        "OrientationAngle": [45],

        "MotionVariance": [3.5]
    }

    # ========================================================
    # RUN SYSTEM
    # ========================================================

    try:

        result = system.predict(

            fall_sensor_data=fall_50,

            type_sensor_data=type_80,

            risk_data=risk_data
        )

    except Exception as e:

        print("\n❌ PREDICTION FAILED")

        print(e)

        return

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print("\n===== MEDIUM RISK TEST COMPLETE =====")

    print("\n========== FINAL RESULT ==========\n")

    for key, value in result.items():

        print(f"{key}: {value}")

    print("\n==================================\n")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()