#!/usr/bin/env python3

import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# =========================
# ✅ SAFE EXPRESSION EVALUATOR
# =========================
def evaluate_signal(sensor_window, expr, pri_col, sub_col, oxy_col):
    """
    Evaluate user expression safely.
    Available variables:
        sub -> SUB_COL
        pri -> PRI_COL
        oxy -> OXY_COL
    """

    allowed_names = {
        "sub": sensor_window[sub_col],
        "pri": sensor_window[pri_col],
        "oxy": sensor_window[oxy_col],
        "np": np,
        "pd": pd
    }

    try:
        result = eval(expr, {"__builtins__": {}}, allowed_names)
    except Exception as e:
        raise ValueError(f"\nInvalid expression:\n{expr}\n\n{e}")

    return result


# =========================
# ✅ PROCESS ONE FILE
# =========================
def process_one_file(csv_path, pri_col, sub_col, oxy_col,
                     expression, out_dir, mode):

    df = pd.read_csv(csv_path)

    # Optional: handle time column if it exists
    if "time" in df.columns:
        try:
            df["time"] = pd.to_datetime(df["time"])
            df = df.set_index("time")
        except Exception:
            pass

    # ✅ DEBUG: show columns so you never guess again
    print(f"\nProcessing: {csv_path.name}")
    print("Columns:", df.columns.tolist())

    # ✅ Build signal from expression
    signal_series = evaluate_signal(
        df,
        expression,
        pri_col,
        sub_col,
        oxy_col
    )

    # =========================
    # ✅ PLOT
    # =========================
    plt.figure()

    plt.plot(signal_series)

    plt.title(f"{csv_path.stem} | {mode}")
    plt.xlabel("Index")
    plt.ylabel("Signal")

    out_path = Path(out_dir) / f"{csv_path.stem}.png"

    plt.savefig(out_path, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out_path}")


# =========================
# ✅ MAIN
# =========================
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--pri_col", required=True)
    parser.add_argument("--sub_col", required=True)
    parser.add_argument("--oxy_col", required=True)
    parser.add_argument("--mode", choices=["continuous", "window"], required=True)

    # ✅ user-defined math
    parser.add_argument("--expression", required=True)

    parser.add_argument("--out_dir", required=True)

    args = parser.parse_args()

    pri_col = args.pri_col
    sub_col = args.sub_col
    oxy_col = args.oxy_col
    expression = args.expression
    mode = args.mode

    # ✅ IMPORTANT: relative to your project folder
    data_dir = Path("/Volumes/WALL-E/python-workspace/lumos/AllignedLMData/RemoveRepeatRows/CSV_TG")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("\n========== CONFIG ==========")
    print("PRI:", pri_col)
    print("SUB:", sub_col)
    print("OXY:", oxy_col)
    print("MODE:", mode)
    print("EXPR:", expression)
    print("Expression received:", args.expression)
    print("============================\n")

    csv_files = list(data_dir.glob("*.csv"))

    if len(csv_files) == 0:
        raise FileNotFoundError(
            f"\nNo CSV files found in:\n{data_dir}\n"
        )

    for csv_path in csv_files:
        process_one_file(
            csv_path,
            pri_col,
            sub_col,
            oxy_col,
            expression,
            out_dir,
            mode
        )


# =========================
# ✅ RUN
# =========================
if __name__ == "__main__":
    main()