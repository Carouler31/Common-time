# demo/plot_demo.py
import os
import csv
import numpy as np
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
out_dir = os.path.join(HERE, "output")

def read_csv(path, xcol, ycol):
    x, y = [], []
    with open(path, "r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            x.append(float(row[xcol]))
            y.append(float(row[ycol]))
    return np.array(x), np.array(y)

# --- Plot 1: Common signal ---
t, s = read_csv(os.path.join(out_dir, "common_signal.csv"), "timestamp", "S")

plt.figure()
plt.plot(t, s)
plt.title("Extracted Common Signal S(t)")
plt.xlabel("Time")
plt.ylabel("S(t)")
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "common_signal.png"))
plt.close()

# --- Plot 2: Residual RMS per station ---
res_files = sorted([
    f for f in os.listdir(out_dir)
    if f.startswith("residuals_") and f.endswith(".csv")
])

names = []
rms = []

for fn in res_files:
    name = fn.replace("residuals_", "").replace(".csv", "")
    _, r = read_csv(os.path.join(out_dir, fn), "timestamp", "residual")
    names.append(name)
    rms.append(np.sqrt(np.mean(r**2)))

plt.figure()
plt.bar(names, rms)
plt.title("Residual RMS by Station (Outlier Detection)")
plt.xlabel("Station")
plt.ylabel("Residual RMS")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "residual_rms.png"))
plt.close()

print("✅ Plots generated:")
print(" - common_signal.png")
print(" - residual_rms.png")
