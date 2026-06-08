#!/usr/bin/env python3
"""
Phase 4 Step 4: DQN Training Script
Project: DRL for Congestion Control and Throughput Optimization
OpenSpec Change 04: dqn-mvp-agent

Requirements (per Change 04 spec):
  - Stable-Baselines3 DQN
  - MlpPolicy (default)
  - Discrete(3) action space
  - Observation shape (5,)
  - Reward from Change 03 (α=1.0, β=0.1, λ=10.0, provisional)
  - seed = 42
  - Log training to CSV (Monitor wrapper)
  - Save model checkpoint (.zip)
  - Record metadata YAML

GATE: Smoke test must have passed before running this script.
SCOPE: No PPO. No IPFS/QUIC/multi-agent/multi-path. No fake results.
"""

import sys
import os
import csv
import yaml
import argparse
import traceback
from pathlib import Path
from datetime import datetime, timezone

import numpy as np

SCRIPT_DIR   = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT))

# ── Check smoke test gate ──────────────────────────────────────────────────────
SMOKE_REPORT = PROJECT_ROOT / "reports" / "phase4-drl-mvp" / "smoke-test-report.md"

def check_smoke_gate():
    if not SMOKE_REPORT.exists():
        print("⛔ GATE BLOCKED: smoke-test-report.md not found.")
        print("   Run first: python3 src/gym_env/smoke_test.py")
        sys.exit(1)
    content = SMOKE_REPORT.read_text()
    if "S1 smoke test PASSED" not in content:
        print("⛔ GATE BLOCKED: S1 smoke test has not passed.")
        print(f"   See: {SMOKE_REPORT}")
        sys.exit(1)
    print("✅ Smoke test gate: PASSED — proceeding to DQN training")

# ── Paths ──────────────────────────────────────────────────────────────────────
MODELS_DIR   = PROJECT_ROOT / "experiments" / "drl" / "models"
LOGS_DIR     = PROJECT_ROOT / "experiments" / "drl" / "logs"
META_DIR     = PROJECT_ROOT / "experiments" / "drl" / "metadata"

for d in [MODELS_DIR, LOGS_DIR, META_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
def train_dqn(
    scenario: str = "S1",
    total_timesteps: int = 50_000,
    seed: int = 42,
    port: int = 5555,
    learning_rate: float = 1e-4,
    batch_size: int = 64,
    buffer_size: int = 10_000,
    learning_starts: int = 1000,
    gamma: float = 0.99,
    target_update_interval: int = 500,
    exploration_fraction: float = 0.3,
    exploration_final_eps: float = 0.05,
    max_steps: int = 100,
    verbose: int = 1,
):
    """Train SB3 DQN on the ns3-gym congestion control environment."""
    # Imports here so they fail gracefully if SB3 not installed
    try:
        import stable_baselines3 as sb3
        from stable_baselines3 import DQN
        from stable_baselines3.common.monitor import Monitor
        from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback
        SB3_VERSION = sb3.__version__
    except ImportError as e:
        print(f"⛔ stable_baselines3 not installed: {e}")
        print("   Install: pip3 install stable-baselines3")
        sys.exit(1)

    try:
        import torch
        TORCH_VERSION = torch.__version__
        # Fix seed
        torch.manual_seed(seed)
    except ImportError:
        TORCH_VERSION = "NOT_INSTALLED"

    from gym_env.ns3_congestion_env import Ns3CongestionEnv

    print("╔══════════════════════════════════════════════════════════╗")
    print("║  Phase 4 Step 4: DQN Training                           ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"  Scenario:        {scenario}")
    print(f"  Timesteps:       {total_timesteps:,}")
    print(f"  Seed:            {seed}")
    print(f"  SB3 version:     {SB3_VERSION}")
    print(f"  PyTorch:         {TORCH_VERSION}")
    print()

    # ── Environment ────────────────────────────────────────────────────────────
    np.random.seed(seed)

    raw_env = Ns3CongestionEnv(
        scenario=scenario,
        sim_duration=60.0,
        max_steps=max_steps,
        seed=seed,
        port=port,
        verbose=False,
    )

    log_file = str(LOGS_DIR / f"dqn_train_{scenario.lower()}_seed{seed}")
    env = Monitor(raw_env, filename=log_file)

    # ── DQN model ──────────────────────────────────────────────────────────────
    model = DQN(
        policy="MlpPolicy",
        env=env,
        learning_rate=learning_rate,
        batch_size=batch_size,
        buffer_size=buffer_size,
        learning_starts=learning_starts,
        gamma=gamma,
        target_update_interval=target_update_interval,
        exploration_fraction=exploration_fraction,
        exploration_final_eps=exploration_final_eps,
        verbose=verbose,
        seed=seed,
        device="cpu",
    )

    print(f"  Model policy:    MlpPolicy")
    print(f"  Action space:    {env.action_space}")
    print(f"  Obs space:       {env.observation_space}")
    print()

    # ── Checkpoint callback ────────────────────────────────────────────────────
    checkpoint_path = str(MODELS_DIR)
    checkpoint_cb = CheckpointCallback(
        save_freq=max(total_timesteps // 5, 1000),
        save_path=checkpoint_path,
        name_prefix=f"dqn_{scenario.lower()}_seed{seed}",
        verbose=1,
    )

    # ── Training ───────────────────────────────────────────────────────────────
    ts_start = datetime.now(timezone.utc)
    print(f"  Training started: {ts_start.strftime('%Y-%m-%dT%H:%M:%SZ')}")
    print()

    try:
        model.learn(
            total_timesteps=total_timesteps,
            callback=checkpoint_cb,
            reset_num_timesteps=True,
            progress_bar=True,
        )
    except KeyboardInterrupt:
        print("\n[WARN] Training interrupted by user. Saving partial model...")
    except Exception as e:
        print(f"\n[ERROR] Training failed: {e}")
        traceback.print_exc()
        # Save partial model for diagnostic
        partial_path = str(MODELS_DIR / f"dqn_{scenario.lower()}_seed{seed}_PARTIAL.zip")
        model.save(partial_path)
        print(f"  Partial model saved: {partial_path}")
        raise

    ts_end = datetime.now(timezone.utc)
    duration_s = (ts_end - ts_start).total_seconds()
    print(f"\n  Training ended:  {ts_end.strftime('%Y-%m-%dT%H:%M:%SZ')}")
    print(f"  Duration:        {duration_s:.1f}s")

    # ── Save final model ───────────────────────────────────────────────────────
    model_path = str(MODELS_DIR / f"dqn_{scenario.lower()}_seed{seed}")
    model.save(model_path)
    print(f"  Model saved:     {model_path}.zip")

    # ── Save training metadata ────────────────────────────────────────────────
    meta = {
        "phase":           "Phase 4 DRL MVP",
        "algorithm":       "DQN",
        "policy":          "MlpPolicy",
        "scenario":        scenario,
        "seed":            seed,
        "total_timesteps": total_timesteps,
        "model_path":      f"{model_path}.zip",
        "log_file":        f"{log_file}.monitor.csv",
        "hyperparameters": {
            "learning_rate":            learning_rate,
            "batch_size":               batch_size,
            "buffer_size":              buffer_size,
            "learning_starts":          learning_starts,
            "gamma":                    gamma,
            "target_update_interval":   target_update_interval,
            "exploration_fraction":     exploration_fraction,
            "exploration_final_eps":    exploration_final_eps,
        },
        "reward_weights": {
            "alpha":  1.0,
            "beta":   0.1,
            "lambda": 10.0,
            "note":   "Provisional weights per Change 03/04. Subject to revision in Change 05.",
        },
        "obs_fields": [
            "throughput_norm", "delay_norm", "loss_norm",
            "cwnd_norm", "prev_action_norm",
        ],
        "action_space": "Discrete(3) {0=decrease, 1=keep, 2=increase}",
        "action_note":  "Fallback Option B: sender-side rate-control abstraction",
        "delay_note":   "delay_or_rtt_signal = delaySum/rxPackets proxy, not direct RTT",
        "sb3_version":  SB3_VERSION,
        "torch_version": TORCH_VERSION,
        "training_start": ts_start.isoformat(),
        "training_end":   ts_end.isoformat(),
        "training_duration_s": duration_s,
    }

    meta_path = META_DIR / f"dqn_training_metadata_{scenario.lower()}.yaml"
    with open(meta_path, "w") as f:
        yaml.dump(meta, f, default_flow_style=False, allow_unicode=True)
    print(f"  Metadata saved:  {meta_path}")

    env.close()

    return model_path + ".zip", meta


# ─────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Phase 4 DQN Training")
    parser.add_argument("--scenario",      default="S1",   choices=["S1", "S2"])
    parser.add_argument("--timesteps",     type=int, default=50_000,
                        help="Total training timesteps (start small for MVP)")
    parser.add_argument("--seed",          type=int, default=42)
    parser.add_argument("--port",          type=int, default=5555)
    parser.add_argument("--lr",            type=float, default=1e-4,
                        dest="learning_rate")
    parser.add_argument("--skip-gate",     action="store_true",
                        help="Skip smoke test gate check (for debug only)")
    parser.add_argument("--verbose",       type=int, default=1)
    args = parser.parse_args()

    if not args.skip_gate:
        check_smoke_gate()

    model_path, meta = train_dqn(
        scenario=args.scenario,
        total_timesteps=args.timesteps,
        seed=args.seed,
        port=args.port,
        learning_rate=args.learning_rate,
        verbose=args.verbose,
    )

    print(f"\n✅ DQN training complete for {args.scenario}")
    print(f"   Model: {model_path}")
    print(f"\nNext: python3 src/agents/eval_dqn.py --scenario {args.scenario} --model {model_path}")


if __name__ == "__main__":
    main()
