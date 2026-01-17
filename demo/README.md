# Common-Time Demo — Ground Station Common Drift

This demo generates 4 ground-station-like time series:
- a slow **common drift** shared by all stations
- independent noise per station
- one station with an additional **local bias** (outlier)

## Visual output

After running the demo, two figures are generated in `demo/output/`:

- **common_signal.png**  
  Extracted slow common drift shared by all stations.

- **residual_rms.png**  
  Residual energy per station. The faulty station is clearly isolated.

These plots provide immediate visual validation of the method.

## Run (Windows / Linux / macOS)

From the `demo/` folder:

1) Generate demo CSV files:
```bash
python generate_data.py

## Quick demo
```bash
pip install -e .
common-time demo
