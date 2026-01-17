import argparse
import os
import sys
import subprocess

def _run_py(script_path: str):
    # Run a python script using the same interpreter
    cmd = [sys.executable, script_path]
    return subprocess.check_call(cmd)

def main():
    parser = argparse.ArgumentParser(prog="common-time", description="Common-Time CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_demo = sub.add_parser("demo", help="Run the demo (generate data, run extraction, generate plots)")
    p_demo.add_argument("--demo-dir", default="demo", help="Path to demo folder (default: demo)")
    p_demo.add_argument("--no-plots", action="store_true", help="Skip plot generation")

    args = parser.parse_args()

    if args.cmd == "demo":
        demo_dir = os.path.abspath(args.demo_dir)

        gen = os.path.join(demo_dir, "generate_data.py")
        run = os.path.join(demo_dir, "run_demo.py")
        plot = os.path.join(demo_dir, "plot_demo.py")

        for p in [gen, run]:
            if not os.path.isfile(p):
                raise SystemExit(f"❌ Missing file: {p}")

        print(f"[Common-Time] Demo directory: {demo_dir}")
        print("[Common-Time] 1/3 Generating demo dataset...")
        _run_py(gen)

        print("[Common-Time] 2/3 Running common signal extraction...")
        _run_py(run)

        if not args.no_plots:
            if not os.path.isfile(plot):
                print("[Common-Time] 3/3 plot_demo.py not found, skipping plots.")
            else:
                print("[Common-Time] 3/3 Generating plots...")
                _run_py(plot)

        out_dir = os.path.join(demo_dir, "output")
        print(f"[Common-Time] ✅ Done. Outputs in: {out_dir}")
