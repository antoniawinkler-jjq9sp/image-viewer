
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#******************************************************************************
#File: 12-remove-glucose.py
#TITLE
#Author Antonia Winkler
#Date: 2026-06-05
#PRIMARY OBJECTIVE:
#SECONDARY OBJECTIVE: Null
#******************************************************************************

# Standard library imports
import os
import sys

# Third-party imports
import pandas as pd
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import plotly.graph_objects as go

ROOT_PATH = Path("/Users/antoniawinkler/Library/CloudStorage/OneDrive-UniversityofVirginia")
print("here")

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


def process_one_file(csv_path, pri_col, sub_col, oxy_col,
                     expression, out_dir, mode,
                     expression2=None, gt_col="Triglycerides"):

    df = pd.read_csv(csv_path)

    # Optional datetime
    if "time" in df.columns:
        try:
            df["time"] = pd.to_datetime(df["time"])
            df = df.set_index("time")
        except Exception:
            pass

    print(f"\nProcessing: {csv_path.name}")
    print("Columns:", df.columns.tolist())

    # ✅ First expression
    signal1 = evaluate_signal(df, expression, pri_col, sub_col, oxy_col)

    # ✅ Second expression (optional)
    signal2 = None
    if expression2:
        signal2 = evaluate_signal(df, expression2, pri_col, sub_col, oxy_col)

    # ✅ Ground Truth (TG)
    tg = None
    if gt_col in df.columns:
        tg = df[gt_col]

    # =========================
    # ✅ PLOT
    # =========================
    fig, ax1 = plt.subplots()

    # ✅ Left axis = Lumos signals
    ax1.set_ylabel("Lumos Signal")

    ax1.plot(signal1, label=expression, color="purple")

    if signal2 is not None:
        ax1.plot(signal2, label=expression2, color="pink")

    ax1.legend(loc="upper left")

    # ✅ Right axis = Ground truth
    if tg is not None:
        ax2 = ax1.twinx()
        ax2.set_ylabel("Triglycerides (mg/dL)")
        ax2.plot(tg, color="blue", marker="o", linewidth=2, label="Triglycerides")

    plt.title(f"{csv_path.stem} | {mode}")
    plt.xlabel("Time")

    out_path = Path(out_dir) / f"{csv_path.stem}.png"
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out_path}")


def build_dashboard(all_data, out_path="dashboard.html"):

    fig = go.Figure()

    trace_map = []  # ✅ track indices per file

    current_index = 0

    # ✅ Add traces and track them
    for i, data in enumerate(all_data):
        indices = []

        # Expression 1
        fig.add_trace(go.Scatter(
            y=data["signal1"],
            name=f"{data['name']} - expr1",
            visible=(i == 0)
        ))
        indices.append(current_index)
        current_index += 1

        # Expression 2
        if data["signal2"] is not None:
            fig.add_trace(go.Scatter(
                y=data["signal2"],
                name=f"{data['name']} - expr2",
                visible=(i == 0)
            ))
            indices.append(current_index)
            current_index += 1

        # Ground truth
        if data["tg"] is not None:
            fig.add_trace(go.Scatter(
                y=data["tg"],
                name=f"{data['name']} - TG",
                visible=(i == 0),
                yaxis="y2",
                mode="lines+markers"
            ))
            indices.append(current_index)
            current_index += 1

        trace_map.append(indices)

    # ✅ Create dropdown buttons safely
    buttons = []

    for i, indices in enumerate(trace_map):
        visible = [False] * len(fig.data)

        for idx in indices:
            visible[idx] = True

        buttons.append(dict(
            label=all_data[i]["name"],
            method="update",
            args=[{"visible": visible}]
        ))

        fig.update_layout(
        title="Lumos Dashboard",
        updatemenus=[dict(
            buttons=buttons,
            direction="down",
            showactive=True,
            x=0.1,
            y=1.15
        )],
        yaxis=dict(title="Signal"),
        yaxis2=dict(
            title="Triglycerides",
            overlaying="y",
            side="right"
        )
    )

    fig.write_html(out_path)

    print(f"Dashboard saved at: {out_path}")



# ========================= main
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--pri_col", required=True)
    parser.add_argument("--sub_col", required=True)
    parser.add_argument("--oxy_col", required=True)
    parser.add_argument("--mode", choices=["continuous", "window"], required=True)

    # ✅ user-defined math
    parser.add_argument("--expression", required=True)

    parser.add_argument("--out_dir", required=True)
    parser.add_argument("--expression2", default=None)
    parser.add_argument("--gt_col", default="Triglycerides")

    args = parser.parse_args()

    pri_col = args.pri_col
    sub_col = args.sub_col
    oxy_col = args.oxy_col
    expression = args.expression
    mode = args.mode
    expression2=args.expression2
    gt_col=args.gt_col


    # ✅ IMPORTANT: relative to your project folder
    data_dir = Path(ROOT_PATH / "lumos/AllignedLMData/RemoveRepeatRows/CSV_TG")

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

    all_data = []

    for csv_path in csv_files:

        print("Processing:", csv_path.name)

        df = pd.read_csv(csv_path)

        signal1 = evaluate_signal(df, expression, pri_col, sub_col, oxy_col)

        signal2 = None
        if args.expression2:
            signal2 = evaluate_signal(df, args.expression2, pri_col, sub_col, oxy_col)

        tg = None
        if args.gt_col in df.columns:
            tg = df[args.gt_col]

        all_data.append({
            "name": csv_path.stem,
            "signal1": signal1,
            "signal2": signal2,
            "tg": tg
        })

    output_path = Path(__file__).parent / "dashboard.html"
    build_dashboard(all_data, out_path=str(output_path))



# =========================
if __name__ == "__main__":
    main()