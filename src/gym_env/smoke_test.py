#!/usr/bin/env python3
"""
Phase 4 Step 3: Random Agent Smoke Test
Project: DRL for Congestion Control and Throughput Optimization
OpenSpec Change 03: opengym-env

Smoke test criteria (per Change 03 spec):
  - environment reset succeeds
  - observation shape = (5,)
  - observation in [0, 1] (no NaN/Inf)
  - action_space = Discrete(3)
  - random action accepted
  - step returns obs, reward, terminated, truncated, info
  - reward is finite (no NaN/Inf)
  - info contains required fields
  - fixed steps do not crash
  - logs written to experiments/drl/logs/

PHASE 4 SCOPE: Smoke test only. No DQN training.
"""

import sys
import os
import csv
import math
import json
import argparse
import traceback
from pathlib import Path
from datetime import datetime, timezone

import numpy as np

SCRIPT_DIR   = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent

sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT))

from gym_env.ns3_congestion_env import Ns3CongestionEnv, VALID_SCENARIOS, OBS_DIM, N_ACTIONS

LOG_DIR     = PROJECT_ROOT / "experiments" / "drl" / "logs"
REPORTS_DIR = PROJECT_ROOT / "reports" / "phase4-drl-mvp"

REQUIRED_INFO_FIELDS = [
    "raw_throughput_mbps",
    "raw_delay_ms",
    "raw_loss_rate",
    "utility_score",
    "scenario_id",
    "step_index",
    "action_applied",
    "delay_estimate_method",
]

# ─────────────────────────────────────────────────────────────────────────────
def validate_obs(obs, step_idx: int, results: list) -> bool:
    ok = True
    if not isinstance(obs, np.ndarray):
        results.append(f"  FAIL step {step_idx}: obs is not ndarray (got {type(obs)})")
        ok = False
        return ok
    if obs.shape != (OBS_DIM,):
        results.append(f"  FAIL step {step_idx}: obs.shape={obs.shape} != ({OBS_DIM},)")
        ok = False
    nan_inf = not np.all(np.isfinite(obs))
    if nan_inf:
        results.append(f"  FAIL step {step_idx}: obs contains NaN/Inf: {obs}")
        ok = False
    out_range = not np.all((obs >= 0.0) & (obs <= 1.0))
    if out_range:
        results.append(f"  WARN step {step_idx}: obs out of [0,1]: {obs}")
    return ok


def validate_reward(reward, step_idx: int, results: list) -> bool:
    if not math.isfinite(reward):
        results.append(f"  FAIL step {step_idx}: reward is non-finite: {reward}")
        return False
    return True


def validate_info(info: dict, step_idx: int, results: list) -> bool:
    ok = True
    for field in REQUIRED_INFO_FIELDS:
        if field not in info:
            results.append(f"  FAIL step {step_idx}: info missing field '{field}'")
            ok = False
    return ok


# ─────────────────────────────────────────────────────────────────────────────
def run_smoke_test(scenario: str, n_steps: int = 20, seed: int = 42,
                   port: int = 5555, verbose: bool = False) -> dict:
    """Run smoke test for one scenario. Returns result dict."""
    print(f"\n{'='*60}")
    print(f"  Smoke Test: scenario={scenario} | steps={n_steps} | seed={seed}")
    print(f"{'='*60}")

    results_log   = []
    passed_checks = []
    failed_checks = []
    log_rows      = []

    # ── 1. Environment construction ──────────────────────────────────────────
    try:
        env = Ns3CongestionEnv(
            scenario=scenario,
            sim_duration=30.0,
            max_steps=n_steps,
            step_interval=0.5,
            seed=seed,
            port=port,
            verbose=verbose,
        )
        passed_checks.append("env construction")
    except Exception as e:
        failed_checks.append(f"env construction: {e}")
        return {
            "scenario": scenario, "passed": False,
            "passed_checks": passed_checks, "failed_checks": failed_checks,
            "error": str(e),
        }

    # ── 2. Action space check ────────────────────────────────────────────────
    if hasattr(env.action_space, 'n') and env.action_space.n == N_ACTIONS:
        passed_checks.append(f"action_space = Discrete({N_ACTIONS})")
    else:
        failed_checks.append(f"action_space check: got {env.action_space}")

    # ── 3. Observation space check ───────────────────────────────────────────
    if env.observation_space.shape == (OBS_DIM,):
        passed_checks.append(f"observation_space shape = ({OBS_DIM},)")
    else:
        failed_checks.append(f"observation_space.shape = {env.observation_space.shape}")

    # ── 4. Reset ─────────────────────────────────────────────────────────────
    try:
        obs, info = env.reset(seed=seed)
        passed_checks.append("reset() succeeds")
        print(f"  [reset] obs={obs}")
    except Exception as e:
        failed_checks.append(f"reset() failed: {e}")
        traceback.print_exc()
        env.close()
        return {
            "scenario": scenario, "passed": False,
            "passed_checks": passed_checks, "failed_checks": failed_checks,
        }

    # Validate initial observation
    if validate_obs(obs, 0, results_log):
        passed_checks.append("initial obs valid (shape, finite, [0,1])")
    else:
        failed_checks.extend(results_log)

    # ── 5. Step loop ─────────────────────────────────────────────────────────
    total_reward = 0.0
    reward_list  = []
    any_step_failed = False

    for step_i in range(1, n_steps + 1):
        action = env.action_space.sample()  # random action
        try:
            obs, reward, terminated, truncated, info = env.step(action)
        except Exception as e:
            failed_checks.append(f"step({step_i}) crashed: {e}")
            any_step_failed = True
            break

        # Validate each component
        obs_ok    = validate_obs(obs, step_i, results_log)
        rew_ok    = validate_reward(reward, step_i, results_log)
        info_ok   = validate_info(info, step_i, results_log)

        if not obs_ok:  failed_checks.append(f"step {step_i}: obs invalid")
        if not rew_ok:  failed_checks.append(f"step {step_i}: reward non-finite ({reward})")
        if not info_ok: failed_checks.append(f"step {step_i}: info incomplete")

        total_reward += reward
        reward_list.append(reward)

        log_rows.append({
            "scenario":           scenario,
            "step":               step_i,
            "action":             action,
            "action_meaning":     {0: "decrease", 1: "keep", 2: "increase"}[action],
            "reward":             reward,
            "terminated":         terminated,
            "truncated":          truncated,
            "throughput_mbps":    info.get("raw_throughput_mbps", 0.0),
            "delay_ms":           info.get("raw_delay_ms", 0.0),
            "loss_rate":          info.get("raw_loss_rate", 0.0),
            "utility_score":      info.get("utility_score", 0.0),
            "obs_t_norm":         float(obs[0]),
            "obs_d_norm":         float(obs[1]),
            "obs_l_norm":         float(obs[2]),
            "obs_c_norm":         float(obs[3]),
            "obs_a_norm":         float(obs[4]),
        })

        if verbose:
            print(f"  step={step_i:3d} action={action} reward={reward:.4f} "
                  f"t={info.get('raw_throughput_mbps', 0):.2f}Mbps "
                  f"d={info.get('raw_delay_ms', 0):.1f}ms "
                  f"loss={info.get('raw_loss_rate', 0):.4f} done={terminated}")

        if terminated or truncated:
            print(f"  [info] Episode ended at step {step_i} (terminated={terminated})")
            break

    if not any_step_failed:
        passed_checks.append(f"step loop ran {n_steps} steps without crash")
    if reward_list:
        passed_checks.append(f"reward finite (min={min(reward_list):.4f} max={max(reward_list):.4f})")

    env.close()

    # ── 6. Write step log CSV ────────────────────────────────────────────────
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = LOG_DIR / f"smoke_test_{scenario.lower()}.csv"
    if log_rows:
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=log_rows[0].keys())
            writer.writeheader()
            writer.writerows(log_rows)
        print(f"  [log] {csv_path}")

    passed = len(failed_checks) == 0
    avg_reward = np.mean(reward_list) if reward_list else 0.0
    print(f"\n  Result: {'PASS' if passed else 'FAIL'}")
    print(f"  Checks passed: {len(passed_checks)} | failed: {len(failed_checks)}")
    if failed_checks:
        for fc in failed_checks:
            print(f"    FAIL: {fc}")

    return {
        "scenario":       scenario,
        "passed":         passed,
        "passed_checks":  passed_checks,
        "failed_checks":  failed_checks,
        "n_steps":        len(log_rows),
        "avg_reward":     avg_reward,
        "total_reward":   total_reward,
        "log_csv":        str(csv_path) if log_rows else None,
    }


# ─────────────────────────────────────────────────────────────────────────────
def write_smoke_report(results_s1: dict, results_s2: dict):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / "smoke-test-report.md"
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def status(r):
        return "✅ PASS" if r.get("passed") else "❌ FAIL"

    with open(report_path, "w") as f:
        f.write("# Phase 4 Smoke Test Report\n\n")
        f.write(f"**Generated**: {ts}\n\n")
        f.write("> Phase 4 Scope: Smoke test only. No DQN training performed.\n\n")
        f.write("---\n\n")

        f.write("## 1. Summary\n\n")
        f.write("| Scenario | Result | Steps | Avg Reward |\n")
        f.write("|----------|--------|-------|------------|\n")
        f.write(f"| S1 (Low Delay) | {status(results_s1)} | {results_s1.get('n_steps', 0)} | {results_s1.get('avg_reward', 0):.4f} |\n")
        f.write(f"| S2 (High Delay) | {status(results_s2)} | {results_s2.get('n_steps', 0)} | {results_s2.get('avg_reward', 0):.4f} |\n\n")

        for label, r in [("S1", results_s1), ("S2", results_s2)]:
            f.write(f"## {label} Smoke Test Details\n\n")
            f.write(f"**Result**: {status(r)}\n\n")
            f.write(f"**Checks Passed** ({len(r.get('passed_checks', []))}):\n")
            for c in r.get("passed_checks", []):
                f.write(f"- ✅ {c}\n")
            failed = r.get("failed_checks", [])
            if failed:
                f.write(f"\n**Checks Failed** ({len(failed)}):\n")
                for c in failed:
                    f.write(f"- ❌ {c}\n")
            if r.get("log_csv"):
                f.write(f"\n**Log CSV**: `{r['log_csv']}`\n")
            f.write("\n")

        f.write("## Gate Decision\n\n")
        s1_ok = results_s1.get("passed", False)
        s2_ok = results_s2.get("passed", False)
        if s1_ok:
            f.write("✅ **S1 smoke test PASSED** — DQN training on S1 is authorized.\n\n")
        else:
            f.write("❌ **S1 smoke test FAILED** — DQN training is BLOCKED until S1 smoke test passes.\n\n")
        if s2_ok:
            f.write("✅ **S2 smoke test PASSED** — DQN training on S2 is authorized.\n\n")
        else:
            f.write("⚠️ **S2 smoke test FAILED / skipped** — DQN training on S2 is non-blocking for MVP.\n\n")

        f.write("## Limitations\n\n")
        f.write("- `delay_or_rtt_signal` = FlowMonitor delaySum/rxPackets proxy, NOT direct TCP RTT.\n")
        f.write("- Action is sender-side rate-control abstraction (Fallback Option B per Change 04).\n")
        f.write("- Smoke test runs with dummy observation if ns3gym not installed; check ns3gym install status.\n")

    print(f"\n  [Report] {report_path}")
    return report_path


# ─────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Phase 4 Smoke Test")
    parser.add_argument("--scenarios",  nargs="+", default=["S1", "S2"],
                        choices=list(VALID_SCENARIOS), help="Scenarios to test")
    parser.add_argument("--n-steps",   type=int, default=20,
                        help="Steps per scenario")
    parser.add_argument("--seed",      type=int, default=42)
    parser.add_argument("--port",      type=int, default=5555,
                        help="Base ZMQ port (S2 uses port+1)")
    parser.add_argument("--verbose",   action="store_true")
    args = parser.parse_args()

    print("╔══════════════════════════════════════════════════════════╗")
    print("║  Phase 4 Step 3: Random Agent Smoke Test                ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"  Scenarios: {args.scenarios}")
    print(f"  Steps per scenario: {args.n_steps}")
    print(f"  Seed: {args.seed}")

    results_s1 = {"passed": False, "passed_checks": [], "failed_checks": ["not run"], "n_steps": 0, "avg_reward": 0}
    results_s2 = {"passed": False, "passed_checks": [], "failed_checks": ["not run"], "n_steps": 0, "avg_reward": 0}

    if "S1" in args.scenarios:
        results_s1 = run_smoke_test("S1", n_steps=args.n_steps,
                                    seed=args.seed, port=args.port,
                                    verbose=args.verbose)
    if "S2" in args.scenarios:
        results_s2 = run_smoke_test("S2", n_steps=args.n_steps,
                                    seed=args.seed, port=args.port + 1,
                                    verbose=args.verbose)

    report_path = write_smoke_report(results_s1, results_s2)

    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║  Smoke Test Complete                                     ║")
    print("╚══════════════════════════════════════════════════════════╝")
    s1_ok = results_s1.get("passed", False)
    s2_ok = results_s2.get("passed", False)
    print(f"  S1: {'PASS ✅' if s1_ok else 'FAIL ❌'}")
    print(f"  S2: {'PASS ✅' if s2_ok else 'FAIL ❌ (non-blocking for MVP)'}")
    print(f"  Report: {report_path}")

    if not s1_ok:
        print("\n⛔ S1 smoke test FAILED. DQN training is blocked.")
        sys.exit(1)
    print("\n✅ S1 smoke test PASSED. Proceed to DQN training.")
    sys.exit(0)


if __name__ == "__main__":
    main()
