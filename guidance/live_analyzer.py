import numpy as np


def analyze_sensor_state(sensor_data):

    sensor_data = np.array(sensor_data)

    accel_mean = np.mean(sensor_data[:, 0:3])
    gyro_mean = np.mean(sensor_data[:, 3:6])

    # =====================================
    # VERY LOW MOVEMENT
    # =====================================
    if accel_mean < 0.1:

        return "no_movement"

    # =====================================
    # SIDE POSITION
    # =====================================
    elif sensor_data[-1][1] > 1.5:

        return "lying_side"

    # =====================================
    # BACK POSITION
    # =====================================
    elif sensor_data[-1][2] > 1.5:

        return "lying_back"

    # =====================================
    # SITTING
    # =====================================
    elif accel_mean > 0.3 and accel_mean < 0.8:

        return "sitting"

    # =====================================
    # STANDING
    # =====================================
    elif accel_mean > 1.0:

        return "standing"

    return "unknown"