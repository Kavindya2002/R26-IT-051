# ============================================================
# test_system.py
# FINAL HIGH RISK TEST VERSION
# ============================================================

from system import FallSystem


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n===== STARTING HIGH RISK TEST =====\n")

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
    # HIGH RISK FALL SENSOR DATA
    # Shape: (50, 11)
    # ========================================================

    fall_50 = []

    for i in range(50):

        row = [

            # accel_x
            8.5,

            # accel_y
            7.8,

            # accel_z
            1.0,

            # gyro_x
            5.2,

            # gyro_y
            4.8,

            # gyro_z
            4.1,

            # pitch
            55.0,

            # roll
            48.0,

            # yaw
            40.0,

            # accel_mag
            14.5,

            # gyro_mag
            8.2
        ]

        fall_50.append(row)

    # ========================================================
    # HIGH RISK FALL TYPE SENSOR DATA
    # Shape: (80, 11)
    # ========================================================

    type_80 = []

    for i in range(80):

        row = [

            9.0,
            8.2,
            0.8,
            5.5,
            4.5,
            4.0,
            60.0,
            50.0,
            42.0,
            15.0,
            9.0
        ]

        type_80.append(row)

    # ========================================================
    # HIGH RISK ALERT INPUT
    # ========================================================

    risk_data = {

        "RiskScore": [0.95],

        "Age": [92],

        "PreviousFalls": [10],

        "Location": ["stairs"],

        "Time": ["night"],

        "Movement": ["critical"],

        "AssistiveDevice": ["wheelchair"],

        # ====================================================
        # NEW FEATURES
        # ====================================================

        "ImpactForce": [14.0],

        "RecoveryTime": [120],

        "TimeOnGround": [300],

        "OrientationAngle": [80],

        "MotionVariance": [9.0]
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

    print("\n===== HIGH RISK TEST COMPLETE =====")

    print("\n========== FINAL RESULT ==========\n")

    for key, value in result.items():

        print(f"{key}: {value}")

    print("\n==================================\n")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()