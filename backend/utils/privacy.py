import numpy as np

def add_noise(value, epsilon=0.1):
    """
    Add Laplace noise to the value for differential privacy.
    """
    scale = 1.0 / epsilon
    noise = np.random.laplace(0, scale)
    return value + noise