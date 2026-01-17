# demo/generate_data.py
import os
import numpy as np
import csv

np.random.seed(42)
os.makedirs("data", exist_ok=True)

t = list(range(1000))
common_drift = [0.0005 * ti for ti in t]

def write_station(path, bias=0.0, noise=0.02):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["timestamp", "value"])
        for ti, base in zip(t, common_drift):
            y = base + bias + float(np.random.normal(0, noise))
            w.writerow([ti, y])

write_station("data/station_A.csv")
write_station("data/station_B.csv")
write_station("data/station_C.csv")
write_station("data/station_D_outlier.csv", bias=0.3)

print("✅ Demo CSV generated in demo/data/")
