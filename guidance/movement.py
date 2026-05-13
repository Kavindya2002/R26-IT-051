import numpy as np

def check_movement(prev, curr, threshold=0.02):
    return np.mean(np.abs(curr - prev)) > threshold