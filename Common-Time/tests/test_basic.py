import numpy as np
from common_time import extract_common_time

def test_common_time():
    t = np.linspace(0, 10, 500)
    s = np.cos(t)
    X = np.vstack([s + 0.05*np.random.randn(len(t)) for _ in range(4)])
    common, w = extract_common_time(X)
    assert len(common) == len(t)
