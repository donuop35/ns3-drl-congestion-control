#!/usr/bin/env python3
"""
Phase 4 Step 5: DQN Evaluation Script
Project: DRL for Congestion Control and Throughput Optimization
OpenSpec Change 04: dqn-mvp-agent

Evaluation requirements (per Change 04 spec):
  - Deterministic policy (exploration disabled)
  - Output baseline-compatible metrics (NOT just reward)
  - Per-episode CSV + evaluation_summary.csv
  - Aligned with baseline_summary.csv columns
  - Honest reporting: if DQN underperforms, document it

SCOPE: Evaluation only. No training. No PPO. No fake results.
"""

import sys
import csv
import yaml
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict

import numpy as np

SCRIPT_DIR   = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT))

BASELINE_CSV = PROJECT_ROOT / "experiments" / "summaries" / "baseline_summary.csv"
EVAL_DIR     = PROJECT_ROOT / "experiments" / "drl" / "evaluations"
SUMM_DIR     = PROJECT_ROOT / "experiments" / "drl" / "summaries"
META_DIR     = PROJECT_ROOT / "experiments" / "drl" / "metadata"

for d in [EVAL_DIR, SUMM_DIR, META_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def eval_dqn(
    model_path: str,
    scenario: str = "S1",
    n_eval_episodes: int = 5,
    seed: int = 42,
    port: int = 5556,
    deterministic: bool = True,
    verbose: bool = False,
) -> Dict:
    """Run deterministic evaluation of a trained DQN model."""
    try:
        from stable_baselines3 import DQN
        from stable_baselines3.common.evaluation import evaluate_policy
    except ImportError as e:
        print(f"⛔ stable_baselines3 not installed: {e}")
        sys.exit(1)

    from gym_env.ns3_congestion_env import Ns3CongestionEnv

    print(f"\n{'='*60}")
    print(f"  DQN Evaluation: scenario={scenario} model={model_path}")
    print(f"  Episodes: {n_eval_episodes} | Deterministic: {deterministic}")
    print(f"{'='*60}\n")

    # ── Load model ─────────────────────────────────────────────────────────────
    if not Path(model_path).exists():
        print(f"⛔ Model not found: {model_path}")
        sys.exit(1)

    model = DQN.load(model_path, device="cpu")
    print(f"  Model loaded: {model_path}")

    # ── Evaluation environment ─────────────────────────────────────────────────
    env = Ns3CongestionEnv(
        scenario=scenario,
        sim_duration=60.0,
        max_steps=100,
        seed=seed,
        port=port,
        verbose=verbose,
    )

    # ── Per-episode evaluation ─────────────────────────────────────────────────
    episode_results = []
    action_counts   = {0: 0, 1: 0, 2: 0}

    for ep in range(n_eval_episodes):
        obs, info = env.reset(seed=seed + ep)
        ep_reward = 0.0
        ep_throughputs = []
        ep_delays      = []
        ep_losses      = []
        ep_utilities   = []
        ep_actions     = []
        done = False

        while not done:
            action, _ = model.predict(obs, deterministic=deterministic)
            action = int(action)
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

            ep_reward += reward
            ep_throughputs.append(info.get("raw_throughput_mbps", 0.0))
            ep_delays.append(info.get("raw_delay_ms", 0.0))
            ep_losses.append(info.get("raw_loss_rate", 0.0))
            ep_utilities.append(info.get("utility_score", 0.0))
            ep_actions.append(action)
            action_counts[action] = action_counts.get(action, 0) + 1

        avg_t  = float(np.mean(ep_throughputs))  if ep_throughputs else 0.0
        avg_d  = float(np.mean(ep_delays))        if ep_delays      else 0.0
        avg_l  = float(np.mean(ep_losses))        if ep_losses      else 0.0
        avg_u  = float(np.mean(ep_utilities))     if ep_utilities   else 0.0

        episode_results.append({
            "scenario_id":        scenario,
            "method":             "DQN",
            "run_id":             f"ep_{ep+1:03d}",
            "seed":               seed + ep,
            "throughput_mbps":    avg_t,
            "avg_delay_ms":       avg_d,
            "loss_rate":          avg_l,
            "utility_score":      avg_u,
            "episode_reward":     ep_reward,
            "n_steps":            len(ep_actions),
            "action_0_pct":       ep_actions.count(0) / max(len(ep_actions), 1),
            "action_1_pct":       ep_actions.count(1) / max(len(ep_actions), 1),
            "action_2_pct":       ep_actions.count(2) / max(len(ep_actions), 1),
        })

        print(f"  ep {ep+1:2d}: reward={ep_reward:.3f} | "
              f"t={avg_t:.2f}Mbps d={avg_d:.1f}ms loss={avg_l:.4f} u={avg_u:.4f}")

    env.close()

    # ── Per-episode CSV ────────────────────────────────────────────────────────
    ep_csv = EVAL_DIR / f"dqn_eval_{scenario.lower()}.csv"
    if episode_results:
        with open(ep_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=episode_results[0].keys())
            writer.writeheader()
            writer.writerows(episode_results)
    print(f"\n  Episode CSV: {ep_csv}")

    # ── Summary (mean across episodes) ────────────────────────────────────────
    mean_t = float(np.mean([r["throughput_mbps"] for r in episode_results]))
    mean_d = float(np.mean([r["avg_delay_ms"]     for r in episode_results]))
    mean_l = float(np.mean([r["loss_rate"]         for r in episode_results]))
    mean_u = float(np.mean([r["utility_score"]     for r in episode_results]))
    mean_r = float(np.mean([r["episode_reward"]    for r in episode_results]))
    total_acts = sum(action_counts.values())

    summary_row = {
        "scenario_id":       scenario,
        "method":            "DQN",
        "run_id":            "eval_mean",
        "seed":              seed,
        "throughput_mbps":   mean_t,
        "avg_delay_ms":      mean_d,
        "loss_rate":         mean_l,
        "utility_score":     mean_u,
        "episode_reward":    mean_r,
        "n_eval_episodes":   n_eval_episodes,
        "deterministic":     deterministic,
        "model_path":        model_path,
        "action_0_decrease_pct": action_counts[0] / max(total_acts, 1),
        "action_1_keep_pct":     action_counts[1] / max(total_acts, 1),
        "action_2_increase_pct": action_counts[2] / max(total_acts, 1),
        "notes": "delay_estimate_method:delaySum_per_packet; action=sender-side-rate-control",
    }

    # Append to dqn_summary.csv
    summ_csv = SUMM_DIR / "dqn_summary.csv"
    write_header = not summ_csv.exists()
    with open(summ_csv, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=summary_row.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(summary_row)

    print(f"  Summary CSV: {summ_csv}")
    print(f"\n  === DQN Mean Results (scenario={scenario}) ===")
    print(f"  Throughput:  {mean_t:.4f} Mbps")
    print(f"  Avg Delay:   {mean_d:.2f} ms")
    print(f"  Loss Rate:   {mean_l:.6f}")
    print(f"  Utility:     {mean_u:.4f}")
    print(f"  Ep Reward:   {mean_r:.4f}")
    print(f"  Actions:     decrease={action_counts[0]} keep={action_counts[1]} increase={action_counts[2]}")

    return summary_row


# ─────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Phase 4 DQN Evaluation")
    parser.add_argument("--model",    required=True, help="Path to .zip model file")
    parser.add_argument("--scenario", default="S1", choices=["S1", "S2"])
    parser.add_argument("--episodes", type=int, default=5)
    parser.add_argument("--seed",     type=int, default=42)
    parser.add_argument("--port",     type=int, default=5556)
    parser.add_argument("--verbose",  action="store_true")
    args = parser.parse_args()

    result = eval_dqn(
        model_path=args.model,
        scenario=args.scenario,
        n_eval_episodes=args.episodes,
        seed=args.seed,
        port=args.port,
        verbose=args.verbose,
    )

    print(f"\n✅ Evaluation complete for {args.scenario}")
    print(f"\nNext: python3 src/analysis/compare_dqn_baseline.py")


if __name__ == "__main__":
    main()
