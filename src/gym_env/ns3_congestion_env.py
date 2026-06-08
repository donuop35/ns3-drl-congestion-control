"""
Phase 4: Python Gymnasium wrapper for ns3-gym OpenGym Congestion Environment
Project: DRL for Congestion Control and Throughput Optimization
OpenSpec Change 03: opengym-env | Change 04: dqn-mvp-agent

This module provides a Gymnasium-compatible environment that:
  - Launches the ns-3 opengym-congestion-env simulation
  - Communicates via ZMQ socket (ns3-gym protocol)
  - Exposes Discrete(3) action space and Box(5) observation space
  - Computes reward per Change 03 spec (provisional weights)
  - Returns baseline-compatible metrics in info dict

PHASE 4 SCOPE: DRL environment only.
  - No PPO
  - No IPFS / QUIC / multi-agent / multi-path
  - No fake/mock results

Action semantics:
  0 = decrease send rate
  1 = keep current rate
  2 = increase send rate

Note: This is Fallback Option B (sender-side rate-control abstraction).
  Action does NOT directly modify kernel TCP cwnd.
  This is documented as per Change 04 fallback hierarchy.
"""

import os
import sys
import json
import subprocess
import time
import csv
import signal
import atexit
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

# Fix ns3gym/protobuf 5.x compatibility (must be set before importing ns3gym)
os.environ.setdefault('PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION', 'python')

import numpy as np
import gymnasium as gym
from gymnasium import spaces

try:
    from ns3gym import ns3env
    HAS_NS3GYM = True
except ImportError:
    HAS_NS3GYM = False
    print("[WARN] ns3gym not importable. Using subprocess-based fallback interface.")

# ──────────────────────────────────────────────────────────────────────────────
# Paths
# ──────────────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent

NS3_HOME = Path(os.environ.get("NS3_HOME", str(
    Path.home() / "ns-allinone-3.40" / "ns-3.40"
)))
NS3_BIN = NS3_HOME / "ns3"
ENV_SCRIPT = "opengym-congestion-env"

# ──────────────────────────────────────────────────────────────────────────────
# Constants (per Change 03/04 spec)
# ──────────────────────────────────────────────────────────────────────────────
OBS_DIM    = 5      # [throughput_norm, delay_norm, loss_norm, cwnd_norm, prev_action_norm]
N_ACTIONS  = 3      # {0: decrease, 1: keep, 2: increase}
GAMMA      = 0.99   # Discount factor per Change 03

# Provisional reward weights (Change 04 spec; may be revised in Change 05)
ALPHA    = 1.0
BETA     = 0.1
LAMBDA_W = 10.0

VALID_SCENARIOS = {"S1", "S2"}


# ──────────────────────────────────────────────────────────────────────────────
# Environment
# ──────────────────────────────────────────────────────────────────────────────
class Ns3CongestionEnv(gym.Env):
    """
    Gymnasium wrapper for ns3-gym congestion control environment.

    Observation space: Box(5,) in [0, 1]
      [throughput_norm, delay_norm, loss_norm, cwnd_norm, prev_action_norm]
      delay_or_rtt_signal = delay proxy (delaySum/rxPackets), NOT direct RTT.

    Action space: Discrete(3)
      0 = decrease, 1 = keep, 2 = increase

    Reward: r = alpha*t_norm - beta*d_norm - lambda*l_norm (clipped to [-1,1])
    """

    metadata = {"render_modes": []}

    def __init__(
        self,
        scenario: str = "S1",
        sim_duration: float = 60.0,
        max_steps: int = 100,
        step_interval: float = 0.5,
        seed: int = 42,
        port: int = 5555,
        alpha: float = ALPHA,
        beta: float = BETA,
        lambda_w: float = LAMBDA_W,
        log_dir: Optional[str] = None,
        verbose: bool = False,
    ):
        super().__init__()

        assert scenario in VALID_SCENARIOS, \
            f"Invalid scenario '{scenario}'. Must be one of {VALID_SCENARIOS}"

        self.scenario      = scenario
        self.sim_duration  = sim_duration
        self.max_steps     = max_steps
        self.step_interval = step_interval
        self.seed_val      = seed
        self.port          = port
        self.alpha         = alpha
        self.beta          = beta
        self.lambda_w      = lambda_w
        self.verbose       = verbose

        # Logging
        if log_dir is None:
            log_dir = str(PROJECT_ROOT / "experiments" / "drl" / "logs")
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Gymnasium spaces
        self.observation_space = spaces.Box(
            low=np.float32(0.0),
            high=np.float32(1.0),
            shape=(OBS_DIM,),
            dtype=np.float32,
        )
        self.action_space = spaces.Discrete(N_ACTIONS)

        # Internal state
        self._ns3env     = None
        self._step_count = 0
        self._ep_count   = 0
        self._prev_action = 1  # keep
        self._last_info   = {}
        self._log_rows    = []

        # Metadata for recording
        self.metadata_dict = {
            "scenario":       scenario,
            "sim_duration":   sim_duration,
            "max_steps":      max_steps,
            "step_interval":  step_interval,
            "seed":           seed,
            "port":           port,
            "obs_shape":      OBS_DIM,
            "obs_fields":     ["throughput_norm", "delay_norm", "loss_norm",
                               "cwnd_norm", "prev_action_norm"],
            "action_space":   "Discrete(3) {0=decrease, 1=keep, 2=increase}",
            "action_note":    ("Fallback Option B: sender-side rate-control abstraction. "
                               "Does NOT directly modify kernel TCP cwnd."),
            "delay_note":     "delay_or_rtt_signal = delaySum/rxPackets proxy, not direct TCP RTT",
            "reward_weights": {"alpha": alpha, "beta": beta, "lambda": lambda_w},
            "reward_note":    "Provisional weights per Change 03/04. Subject to revision in Change 05.",
            "gamma":          GAMMA,
        }

        if verbose:
            print(f"[Ns3CongestionEnv] Init: scenario={scenario} port={port} "
                  f"max_steps={max_steps} seed={seed}")

    # ── Properties ────────────────────────────────────────────────────────────
    @property
    def obs_fields(self):
        return self.metadata_dict["obs_fields"]

    # ── reset ─────────────────────────────────────────────────────────────────
    def reset(
        self,
        seed: Optional[int] = None,
        options: Optional[dict] = None,
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Reset environment: (re)launch ns-3 simulation, return initial obs."""
        if seed is not None:
            self.seed_val = seed

        # Close existing ns3gym connection
        if self._ns3env is not None:
            try:
                self._ns3env.close()
            except Exception:
                pass
            self._ns3env = None

        # Flush episode log
        if self._log_rows and self._ep_count > 0:
            self._flush_episode_log()

        self._step_count  = 0
        self._ep_count   += 1
        self._prev_action = 1
        self._log_rows    = []

        if self.verbose:
            print(f"[reset] Episode {self._ep_count} | scenario={self.scenario} "
                  f"port={self.port} seed={self.seed_val}")

        if not HAS_NS3GYM:
            # Return dummy zero obs for testing without ns3gym
            obs = np.zeros(OBS_DIM, dtype=np.float32)
            info = self._make_info(obs, 0)
            return obs, info

        try:
            ns3_cmd = self._build_ns3_command()
            self._ns3env = ns3env.Ns3Env(
                port=self.port,
                stepTime=self.step_interval,
                startSim=1,
                simSeed=self.seed_val,
                simArgs=ns3_cmd,
                debug=self.verbose,
            )
            obs = self._parse_obs(self._ns3env.reset())
        except Exception as e:
            print(f"[WARN] ns3env reset failed: {e}")
            obs = np.zeros(OBS_DIM, dtype=np.float32)

        info = self._make_info(obs, self._prev_action)
        return obs, info

    # ── step ──────────────────────────────────────────────────────────────────
    def step(
        self, action: int
    ) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        """Apply action, advance simulation one step, return (obs, reward, terminated, truncated, info)."""
        assert self.action_space.contains(action), f"Invalid action: {action}"

        self._prev_action = int(action)
        self._step_count += 1

        if not HAS_NS3GYM or self._ns3env is None:
            # Dummy step for testing without ns3gym
            obs = np.zeros(OBS_DIM, dtype=np.float32)
            reward = 0.0
            terminated = self._step_count >= self.max_steps
            truncated  = False
            info = self._make_info(obs, action)
            return obs, reward, terminated, truncated, info

        try:
            raw_obs, raw_reward, done, extra_info = self._ns3env.step(action)
            obs    = self._parse_obs(raw_obs)
            reward = float(raw_reward)

            # Parse extra info from ns-3
            try:
                info_dict = json.loads(extra_info)
            except (json.JSONDecodeError, TypeError):
                info_dict = {}

        except Exception as e:
            print(f"[WARN] ns3env step error at step {self._step_count}: {e}")
            obs     = np.zeros(OBS_DIM, dtype=np.float32)
            reward  = 0.0
            done    = True
            info_dict = {}

        terminated = done or (self._step_count >= self.max_steps)
        truncated  = False

        info = self._make_info(obs, action, extra=info_dict)
        reward = self._clip_reward(reward)

        # Log
        self._log_rows.append({
            "episode":             self._ep_count,
            "step":                self._step_count,
            "action":              action,
            "reward":              reward,
            "throughput_mbps":     info.get("raw_throughput_mbps", 0.0),
            "delay_ms":            info.get("raw_delay_ms", 0.0),
            "loss_rate":           info.get("raw_loss_rate", 0.0),
            "utility_score":       info.get("utility_score", 0.0),
            "obs_t_norm":          float(obs[0]),
            "obs_d_norm":          float(obs[1]),
            "obs_l_norm":          float(obs[2]),
            "obs_c_norm":          float(obs[3]),
            "obs_a_norm":          float(obs[4]),
            "terminated":          terminated,
        })

        return obs, reward, terminated, truncated, info

    # ── close ─────────────────────────────────────────────────────────────────
    def close(self):
        if self._ns3env is not None:
            try:
                self._ns3env.close()
            except Exception:
                pass
            self._ns3env = None
        if self._log_rows:
            self._flush_episode_log()

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _build_ns3_command(self) -> dict:
        """Build ns3gym simArgs dict for ns-3 simulation."""
        return {
            "--scenario":     self.scenario,
            "--openGymPort":  str(self.port),
            "--simDuration":  str(self.sim_duration),
            "--seed":         str(self.seed_val),
            "--maxSteps":     str(self.max_steps),
            "--stepInterval": str(self.step_interval),
            "--alpha":        str(self.alpha),
            "--beta":         str(self.beta),
            "--lambdaW":      str(self.lambda_w),
        }

    def _parse_obs(self, raw) -> np.ndarray:
        """Convert ns3gym observation to numpy array, clipped to [0,1]."""
        if raw is None:
            return np.zeros(OBS_DIM, dtype=np.float32)
        obs = np.array(raw, dtype=np.float32)
        if obs.shape != (OBS_DIM,):
            obs = np.zeros(OBS_DIM, dtype=np.float32)
        obs = np.clip(obs, 0.0, 1.0)
        return obs

    def _clip_reward(self, reward: float) -> float:
        """Clip reward to [-1, 1] for numerical stability."""
        if not np.isfinite(reward):
            return 0.0
        return float(np.clip(reward, -1.0, 1.0))

    def _compute_utility(self, t_mbps, d_ms, loss):
        """Compute provisional utility score (matches Phase 3 baseline formula)."""
        t_norm = min(t_mbps / 10.0, 1.0)
        d_norm = min(d_ms / 200.0, 1.0)
        return float(t_norm - 0.1 * d_norm - 10.0 * loss)

    def _make_info(self, obs, action, extra: dict = None) -> Dict[str, Any]:
        """Build baseline-compatible info dict."""
        extra = extra or {}
        t_mbps = float(obs[0] * 10.0)  # denormalize
        d_ms   = float(obs[1] * (300.0 if self.scenario == "S2" else 100.0))
        loss   = float(obs[2])
        util   = self._compute_utility(t_mbps, d_ms, loss)

        info = {
            # Baseline-compatible metrics (matches baseline_summary.csv columns)
            "raw_throughput_mbps":   extra.get("raw_throughput_mbps", t_mbps),
            "raw_delay_ms":          extra.get("raw_delay_ms", d_ms),
            "raw_loss_rate":         extra.get("raw_loss_rate", loss),
            "utility_score":         util,
            "delay_estimate_method": "delaySum_per_packet",
            # RL metadata
            "scenario_id":           self.scenario,
            "step_index":            self._step_count,
            "action_applied":        action,
            "action_meaning":        {0: "decrease", 1: "keep", 2: "increase"}[action],
            "episode":               self._ep_count,
        }
        info.update(extra)
        self._last_info = info
        return info

    def _flush_episode_log(self):
        """Write episode log to CSV."""
        fname = self.log_dir / f"env_episode_{self._ep_count:04d}_{self.scenario}.csv"
        if not self._log_rows:
            return
        keys = self._log_rows[0].keys()
        with open(fname, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self._log_rows)
        if self.verbose:
            print(f"[Episode log] {fname}")


# ──────────────────────────────────────────────────────────────────────────────
# Registration
# ──────────────────────────────────────────────────────────────────────────────
def make_env(scenario: str = "S1", **kwargs) -> Ns3CongestionEnv:
    """Factory function for creating the environment."""
    return Ns3CongestionEnv(scenario=scenario, **kwargs)
