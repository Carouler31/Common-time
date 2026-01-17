# demo/run_demo.py
import os
import sys
import csv
import json
import numpy as np

# --- Make src/ importable (no install needed) ---
HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, ".."))
SRC_DIR = os.path.join(REPO_ROOT, "src")
sys.path.insert(0, SRC_DIR)

from common_time.core import extract_common_time  # noqa: E402


def read_csv_timeseries(path):
    t, y = [], []
    with open(path, "r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            t.append(float(row["timestamp"]))
            y.append(float(row["value"]))
    return np.array(t), np.array(y)


def mad(x):
    med = np.median(x)
    return np.median(np.abs(x - med)) + 1e-12


def main():
    data_dir = os.path.join(HERE, "data")
    out_dir = os.path.join(HERE, "output")
    os.makedirs(out_dir, exist_ok=True)

    files = sorted([f for f in os.listdir(data_dir) if f.endswith(".csv")])
    if not files:
        raise SystemExit("❌ No CSV files found in demo/data/. Run: python generate_data.py")

    # Read and align (assumes same timestamps in this demo)
    series_names = []
    Y = []
    t_ref = None

    for fn in files:
        path = os.path.join(data_dir, fn)
        t, y = read_csv_timeseries(path)
        if t_ref is None:
            t_ref = t
        else:
            if len(t) != len(t_ref) or np.max(np.abs(t - t_ref)) > 0:
                raise SystemExit(f"❌ Timestamp mismatch in {fn}. This demo expects aligned timestamps.")
        series_names.append(fn.replace(".csv", ""))
        Y.append(y)

    X = np.vstack(Y)  # shape (n_series, n_time)

    # Extract common signal
    common, weights = extract_common_time(X)

    # Residuals
    residuals = X - (weights[:, None] * common[None, :])

    # Simple outlier detection: residual RMS
    rms = np.sqrt(np.mean(residuals**2, axis=1))
    med = np.median(rms)
    score = (rms - med) / mad(rms)

    outliers = [series_names[i] for i in range(len(series_names)) if score[i] > 6.0]  # threshold
    if not outliers:
        # fallback: flag max if it's clearly above the rest
        i_max = int(np.argmax(rms))
        if rms[i_max] > med + 6.0 * mad(rms):
            outliers = [series_names[i_max]]

    # Write outputs
    # common_signal.csv
    with open(os.path.join(out_dir, "common_signal.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["timestamp", "S"])
        for ti, si in zip(t_ref, common):
            w.writerow([ti, float(si)])

    # residuals per station
    for i, name in enumerate(series_names):
        with open(os.path.join(out_dir, f"residuals_{name}.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["timestamp", "residual"])
            for ti, ri in zip(t_ref, residuals[i]):
                w.writerow([ti, float(ri)])

    summary = {
        "stations": series_names,
        "weights": {series_names[i]: float(weights[i]) for i in range(len(series_names))},
        "residual_rms": {series_names[i]: float(rms[i]) for i in range(len(series_names))},
        "outliers": outliers,
    }

    with open(os.path.join(out_dir, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("✅ Common-Time demo finished")
    print(f"   Loaded series: {len(series_names)}")
    print(f"   Outliers: {outliers if outliers else 'none'}")
    print(f"   Output folder: {out_dir}")


if __name__ == "__main__":
    main()
