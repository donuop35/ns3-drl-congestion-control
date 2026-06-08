#!/usr/bin/env python3
"""
Phase 4 Step 6: DQN vs Baseline Comparison Script
Project: DRL for Congestion Control and Throughput Optimization
OpenSpec Change 04: dqn-mvp-agent | Change 02: ns3-baseline-benchmark

Reads:
  - experiments/summaries/baseline_summary.csv   (Phase 3)
  - experiments/drl/summaries/dqn_summary.csv    (Phase 4)

Produces:
  - experiments/drl/summaries/dqn_vs_baseline_summary.csv
  - figures/comparison/dqn_vs_baseline_{metric}.png  (4 metrics)
  - figures/drl/dqn_reward_curve.png (if training log available)
  - figures/drl/dqn_action_distribution.png

Honest reporting rules (per Change 04 spec):
  - If DQN underperforms, document it — do NOT hide
  - Reward curve is diagnostic only
  - Network metrics are primary comparison
  - DQN column omitted from table if training failed
"""

import sys
import csv
import argparse
from pathlib import Path

import numpy as np

SCRIPT_DIR   = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

BASELINE_CSV = PROJECT_ROOT / "experiments" / "summaries" / "baseline_summary.csv"
DQN_SUMM_CSV = PROJECT_ROOT / "experiments" / "drl" / "summaries" / "dqn_summary.csv"
COMP_SUMM    = PROJECT_ROOT / "experiments" / "drl" / "summaries" / "dqn_vs_baseline_summary.csv"
COMP_FIG_DIR = PROJECT_ROOT / "figures" / "comparison"
DRL_FIG_DIR  = PROJECT_ROOT / "figures" / "drl"
LOGS_DIR     = PROJECT_ROOT / "experiments" / "drl" / "logs"

for d in [COMP_FIG_DIR, DRL_FIG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# Matplotlib
# ─────────────────────────────────────────────────────────────────────────────
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("[WARN] matplotlib not available. Tables only.")

COLORS = {
    "ns3::TcpLinuxReno": "#2196F3",
    "ns3::TcpCubic":     "#FF9800",
    "ns3::TcpBbr":       "#4CAF50",
    "DQN":               "#E91E63",  # Pink/magenta for DQN
}
LABELS = {
    "ns3::TcpLinuxReno": "NewReno",
    "ns3::TcpCubic":     "CUBIC",
    "ns3::TcpBbr":       "BBR",
    "DQN":               "DQN (ours)",
}


# ─────────────────────────────────────────────────────────────────────────────
def load_csv(path: Path) -> list:
    if not path.exists():
        return []
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                rows.append({
                    "scenario_id":    row["scenario_id"],
                    "method":         row["method"],
                    "throughput_mbps": float(row["throughput_mbps"]),
                    "avg_delay_ms":   float(row["avg_delay_ms"]),
                    "loss_rate":      float(row["loss_rate"]),
                    "utility_score":  float(row["utility_score"]),
                })
            except (KeyError, ValueError):
                continue
    return rows


def make_comparison_bar(
    rows: list,
    metric_key: str,
    metric_label: str,
    metric_unit: str,
    out_path: Path,
    scenario: str,
):
    if not HAS_MATPLOTLIB:
        return
    scen_rows = [r for r in rows if r["scenario_id"] == scenario]
    if not scen_rows:
        return

    methods = [r["method"] for r in scen_rows]
    values  = [r[metric_key] for r in scen_rows]
    colors  = [COLORS.get(m, "#9E9E9E") for m in methods]
    labels  = [LABELS.get(m, m) for m in methods]

    fig, ax = plt.subplots(figsize=(max(6, len(methods) * 1.5 + 2), 5))
    bars = ax.bar(labels, values, color=colors, alpha=0.85, edgecolor="white", width=0.6)

    # Value labels on bars
    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(values) * 0.01,
            f"{val:.3f}", ha="center", va="bottom", fontsize=9,
        )

    scenario_desc = {"S1": "S1 (Low Delay, 10ms)", "S2": "S2 (High Delay, 50ms)"}
    ax.set_title(
        f"{metric_label} Comparison — {scenario_desc.get(scenario, scenario)}",
        fontsize=13, fontweight="bold",
    )
    ax.set_ylabel(f"{metric_label}" + (f" [{metric_unit}]" if metric_unit else ""), fontsize=11)
    ax.set_xlabel("Algorithm", fontsize=11)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.set_ylim(bottom=min(0.0, min(values) * 1.2))
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"  [Figure] {out_path}")


def plot_reward_curve(scenario: str = "S1", seed: int = 42):
    """Plot DQN training reward curve from Monitor log."""
    if not HAS_MATPLOTLIB:
        return
    log_file = LOGS_DIR / f"dqn_train_{scenario.lower()}_seed{seed}.monitor.csv"
    if not log_file.exists():
        print(f"  [WARN] Training log not found: {log_file}")
        return

    rewards = []
    try:
        with open(log_file) as f:
            # Monitor CSV has a header comment line, skip it
            lines = f.readlines()
            reader = csv.DictReader(l for l in lines if not l.startswith("#"))
            for row in reader:
                try:
                    rewards.append(float(row["r"]))
                except (KeyError, ValueError):
                    continue
    except Exception as e:
        print(f"  [WARN] Failed to parse training log: {e}")
        return

    if not rewards:
        return

    # Smooth with rolling average
    window = min(50, len(rewards) // 5 + 1)
    smoothed = np.convolve(rewards, np.ones(window) / window, mode="valid")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(rewards, alpha=0.3, color="#E91E63", label="Episode reward (raw)")
    ax.plot(range(window - 1, len(rewards)), smoothed, color="#E91E63",
            linewidth=2, label=f"Smoothed (window={window})")
    ax.axhline(0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("Episode", fontsize=11)
    ax.set_ylabel("Reward", fontsize=11)
    ax.set_title(f"DQN Training Reward Curve — {scenario} (seed={seed})\n"
                 "(diagnostic only; network metrics are primary comparison)",
                 fontsize=12, fontweight="bold")
    ax.legend(fontsize=10)
    ax.grid(linestyle="--", alpha=0.4)
    fig.tight_layout()
    out = DRL_FIG_DIR / f"dqn_reward_curve_{scenario.lower()}.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"  [Figure] {out}")


def plot_action_distribution(dqn_rows: list, scenario: str = "S1"):
    """Plot DQN action distribution."""
    if not HAS_MATPLOTLIB:
        return
    scen = [r for r in dqn_rows if r["scenario_id"] == scenario]
    if not scen or not all(k in scen[0] for k in ["action_0_decrease_pct"]):
        return

    fig, ax = plt.subplots(figsize=(5, 4))
    labels  = ["Decrease (0)", "Keep (1)", "Increase (2)"]
    values  = [
        float(scen[0].get("action_0_decrease_pct", 0)),
        float(scen[0].get("action_1_keep_pct", 0)),
        float(scen[0].get("action_2_increase_pct", 0)),
    ]
    colors  = ["#F44336", "#2196F3", "#4CAF50"]
    bars = ax.bar(labels, [v * 100 for v in values], color=colors, alpha=0.85, edgecolor="white")
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f"{val*100:.1f}%", ha="center", va="bottom", fontsize=10)
    ax.set_ylabel("Action frequency (%)", fontsize=11)
    ax.set_title(f"DQN Action Distribution — {scenario}", fontsize=12, fontweight="bold")
    ax.set_ylim(0, 110)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    fig.tight_layout()
    out = DRL_FIG_DIR / f"dqn_action_distribution_{scenario.lower()}.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"  [Figure] {out}")


# ─────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Phase 4 DQN vs Baseline Comparison")
    parser.add_argument("--scenarios", nargs="+", default=["S1", "S2"])
    parser.add_argument("--seed",     type=int, default=42)
    args = parser.parse_args()

    print("╔══════════════════════════════════════════════════════════╗")
    print("║  Phase 4 Step 6: DQN vs Baseline Comparison             ║")
    print("╚══════════════════════════════════════════════════════════╝")

    # ── Load data ──────────────────────────────────────────────────────────────
    baseline_rows = load_csv(BASELINE_CSV)
    dqn_rows_raw  = []

    # Load full dqn_summary.csv for action distribution
    dqn_meta_rows = []
    if DQN_SUMM_CSV.exists():
        with open(DQN_SUMM_CSV, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                dqn_meta_rows.append(dict(row))

    dqn_rows = load_csv(DQN_SUMM_CSV)

    if not baseline_rows:
        print(f"[WARN] Baseline CSV not found or empty: {BASELINE_CSV}")
        print("  Phase 3 must be complete before running comparison.")
    else:
        print(f"  Baseline rows: {len(baseline_rows)}")

    if not dqn_rows:
        print(f"[WARN] DQN summary CSV not found or empty: {DQN_SUMM_CSV}")
        print("  Run eval_dqn.py first.")
    else:
        print(f"  DQN rows: {len(dqn_rows)}")

    # Combine for comparison CSV
    all_rows = baseline_rows + dqn_rows
    import csv as csv_module
    if all_rows:
        with open(COMP_SUMM, "w", newline="") as f:
            keys = ["scenario_id", "method", "throughput_mbps", "avg_delay_ms",
                    "loss_rate", "utility_score"]
            writer = csv_module.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(all_rows)
        print(f"  Comparison CSV: {COMP_SUMM}")

    # ── Figures ────────────────────────────────────────────────────────────────
    print("\n  [Step G-DRL] Generating comparison figures...")
    metrics = [
        ("throughput_mbps", "Throughput", "Mbps"),
        ("avg_delay_ms",    "Avg Delay",  "ms"),
        ("loss_rate",       "Loss Rate",  "fraction"),
        ("utility_score",   "Utility Score", ""),
    ]

    for scenario in args.scenarios:
        for metric_key, metric_label, metric_unit in metrics:
            out = COMP_FIG_DIR / f"dqn_vs_baseline_{metric_key.replace('_mbps','').replace('_ms','').replace('_rate','')}_{scenario.lower()}.png"
            make_comparison_bar(all_rows, metric_key, metric_label, metric_unit, out, scenario)

        # DQN-specific figures
        plot_reward_curve(scenario=scenario, seed=args.seed)
        plot_action_distribution(dqn_meta_rows, scenario=scenario)

    # ── Print comparison tables ────────────────────────────────────────────────
    print("\n  === DQN vs Baseline Comparison Tables ===")
    for scenario in args.scenarios:
        scen_rows = [r for r in all_rows if r["scenario_id"] == scenario]
        if not scen_rows:
            continue
        scenario_desc = {"S1": "S1 (Low Delay, 10ms)", "S2": "S2 (High Delay, 50ms)"}
        print(f"\n--- {scenario_desc.get(scenario, scenario)} ---")
        header = "| Algorithm | Throughput (Mbps) | Delay (ms) | Loss Rate | Utility |"
        divider = "|-----------|:-----------------:|:----------:|:---------:|:-------:|"
        print(header)
        print(divider)
        for r in sorted(scen_rows, key=lambda x: -x["utility_score"]):
            lbl = LABELS.get(r["method"], r["method"])
            note = " ⚠️" if r["method"] == "ns3::TcpBbr" and scenario == "S2" else ""
            print(f"| {lbl}{note:4s} | {r['throughput_mbps']:17.4f} | "
                  f"{r['avg_delay_ms']:10.2f} | {r['loss_rate']:9.6f} | "
                  f"{r['utility_score']:7.4f} |")

    print("\n  > Note: DQN results are preliminary MVP. ")
    print("  > Reward curve is diagnostic only; network metrics are primary.")
    print("  > BBR S2 anomaly (ns-3.40 high-RTT limitation) documented separately.")
    print(f"\n✅ Comparison complete. Files in: {COMP_FIG_DIR}")


if __name__ == "__main__":
    main()
