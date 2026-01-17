import numpy as np

def extract_common_time(X):
    """
    X: array-like, shape (n_series, n_time)
    Returns:
        S: common temporal signal
        weights: contribution of each series
    """
    X = np.asarray(X)
    X = X - X.mean(axis=1, keepdims=True)
    U, S, Vt = np.linalg.svd(X, full_matrices=False)
    common = Vt[0]
    weights = U[:, 0] * S[0]
    return common, weights
