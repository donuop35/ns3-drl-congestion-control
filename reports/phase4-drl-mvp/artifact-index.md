# Phase 4 Artifact Index

**Project:** DRL-Based Congestion Control over a Bottleneck Link  
**OpenSpec Change 04:** dqn-mvp-agent  
**Generated:** 2026-06-09  
**Phase:** Phase 4 Excellent Acceptance Upgrade

---

## 1. Models

| Artifact | Path | Status | Notes |
|----------|------|--------|-------|
| DQN S1 Final Model | `experiments/drl/models/dqn_s1_seed42.zip` | ✅ | 30k steps, seed=42 |
| DQN S1 Checkpoint 6k | `experiments/drl/models/dqn_s1_seed42_6000_steps.zip` | ✅ | Intermediate |
| DQN S1 Checkpoint 12k | `experiments/drl/models/dqn_s1_seed42_12000_steps.zip` | ✅ | Intermediate |
| DQN S1 Checkpoint 18k | `experiments/drl/models/dqn_s1_seed42_18000_steps.zip` | ✅ | Intermediate |
| DQN S1 Checkpoint 24k | `experiments/drl/models/dqn_s1_seed42_24000_steps.zip` | ✅ | Intermediate |
| DQN S1 Checkpoint 30k | `experiments/drl/models/dqn_s1_seed42_30000_steps.zip` | ✅ | Intermediate (= final) |
| DQN S2 Final Model | `experiments/drl/models/dqn_s2_seed42.zip` | 🔄 | Training in progress |

---

## 2. Training Logs

| Artifact | Path | Status | Notes |
|----------|------|--------|-------|
| S1 Monitor CSV | `experiments/drl/logs/dqn_train_s1_seed42.monitor.csv` | ✅ | SB3 Monitor episode log |
| S1 Episode CSVs | `experiments/drl/logs/env_episode_*_S1.csv` | ✅ | ~300 files |
| S2 Monitor CSV | `experiments/drl/logs/dqn_train_s2_seed42.monitor.csv` | 🔄 | Pending S2 training |
| S2 Episode CSVs | `experiments/drl/logs/env_episode_*_S2.csv` | 🔄 | Pending S2 training |

---

## 3. Evaluation CSVs

| Artifact | Path | Status | Notes |
|----------|------|--------|-------|
| S1 Per-Episode Eval | `experiments/drl/evaluations/dqn_eval_s1.csv` | ✅ | 5 episodes, deterministic |
| S2 Per-Episode Eval | `experiments/drl/evaluations/dqn_eval_s2.csv` | 🔄 | Pending S2 training |

---

## 4. Summary CSVs

| Artifact | Path | Status | Notes |
|----------|------|--------|-------|
| DQN Summary | `experiments/drl/summaries/dqn_summary.csv` | ✅+🔄 | S1 done; S2 row pending |
| DQN vs Baseline | `experiments/drl/summaries/dqn_vs_baseline_summary.csv` | ✅+🔄 | S1 comparison done; S2 pending |
| Seed Sensitivity | `experiments/drl/summaries/dqn_seed_sensitivity_summary.csv` | 🔄 | Pending excellent acceptance upgrade |
| Action Distribution | `experiments/drl/summaries/dqn_action_distribution_summary.csv` | 🔄 | Pending excellent acceptance upgrade |
| Phase 3 Baseline | `experiments/summaries/baseline_summary.csv` | ✅ | Phase 3; 10 rows (S1–S4, 3 algos) |

---

## 5. Metadata YAMLs

| Artifact | Path | Status | Notes |
|----------|------|--------|-------|
| S1 Training Metadata | `experiments/drl/metadata/dqn_training_metadata_s1.yaml` | ✅ | Seed, versions, hyperparams |
| S2 Training Metadata | `experiments/drl/metadata/dqn_training_metadata_s2.yaml` | 🔄 | Pending S2 training |
| Phase 3 Toolchain | `experiments/metadata/toolchain_metadata.yaml` | ✅ | ns-3.40 environment info |
| Phase 3 Run Config | `experiments/metadata/phase3_run_metadata.yaml` | ✅ | Baseline run configuration |

---

## 6. Figures

### 6.1 DRL-Specific Figures (`figures/drl/`)

| Artifact | Path | Status | Notes |
|----------|------|--------|-------|
| S1 Reward Curve | `figures/drl/dqn_reward_curve_s1.png` | ✅ | Diagnostic only |
| S2 Reward Curve | `figures/drl/dqn_reward_curve_s2.png` | 🔄 | Pending S2 training |
| S1 Action Distribution | `figures/drl/dqn_action_distribution_s1.png` | ✅ | 100% action 2 (increase) |
| S2 Action Distribution | `figures/drl/dqn_action_distribution_s2.png` | 🔄 | Pending S2 training |
| Seed Sensitivity | `figures/drl/dqn_seed_sensitivity.png` | 🔄 | Pending excellent acceptance upgrade |

### 6.2 Comparison Figures (`figures/comparison/`)

| Artifact | Path | Status | Notes |
|----------|------|--------|-------|
| S1 Throughput | `figures/comparison/dqn_vs_baseline_throughput_s1.png` | ✅ | 4 algorithms |
| S1 Avg Delay | `figures/comparison/dqn_vs_baseline_avg_delay_s1.png` | ✅ | delay proxy noted |
| S1 Loss Rate | `figures/comparison/dqn_vs_baseline_loss_s1.png` | ✅ | |
| S1 Utility Score | `figures/comparison/dqn_vs_baseline_utility_score_s1.png` | ✅ | DQN=0.900, BBR=0.947 |
| S2 Throughput | `figures/comparison/dqn_vs_baseline_throughput_s2.png` | 🔄 | Pending S2 |
| S2 Avg Delay | `figures/comparison/dqn_vs_baseline_avg_delay_s2.png` | 🔄 | |
| S2 Loss Rate | `figures/comparison/dqn_vs_baseline_loss_s2.png` | 🔄 | |
| S2 Utility Score | `figures/comparison/dqn_vs_baseline_utility_score_s2.png` | 🔄 | |

### 6.3 Phase 3 Baseline Figures (`figures/baseline/`)

| Artifact | Path | Status | Notes |
|----------|------|--------|-------|
| Baseline Throughput | `figures/baseline/throughput_comparison.png` | ✅ | Phase 3 |
| Baseline Delay | `figures/baseline/delay_comparison.png` | ✅ | Phase 3 |
| Baseline Loss | `figures/baseline/loss_comparison.png` | ✅ | Phase 3 |
| Baseline Utility | `figures/baseline/utility_score_comparison.png` | ✅ | Phase 3 |

---

## 7. Reports

| Artifact | Path | Status | Notes |
|----------|------|--------|-------|
| Phase 3 Baseline Report | `reports/phase3-baseline/phase3-baseline-report.md` | ✅ | NewReno/CUBIC/BBR S1–S4 |
| Phase 4 Preflight Audit | `reports/phase4-drl-mvp/preflight-audit.md` | ✅ | Pre-implementation checklist |
| Phase 4 Smoke Test Report | `reports/phase4-drl-mvp/smoke-test-report.md` | ✅ | S1+S2 real ZMQ PASS (hardened) |
| Phase 4 DRL Report | `reports/phase4-drl-mvp/phase4-drl-report.md` | ✅ | S1 DQN results |
| Phase 4 Audit | `reports/phase4-drl-mvp/excellent-acceptance-audit.md` | ✅ | This upgrade gap analysis |
| Artifact Index | `reports/phase4-drl-mvp/artifact-index.md` | ✅ | This file |
| Excellent Acceptance Report | `reports/phase4-drl-mvp/phase4-excellent-acceptance-report.md` | 🔄 | Pending S2 + upgrade completion |

---

## 8. Source Code

| Artifact | Path | Status | Notes |
|----------|------|--------|-------|
| C++ OpenGym Env | `src/ns3/congestion-env.cc` | ✅ | ns-3.40 OpenGym wrapper |
| Python Gym Wrapper | `src/gym_env/ns3_congestion_env.py` | ✅ | Gymnasium + ZMQ + subprocess |
| Smoke Test | `src/gym_env/smoke_test.py` | ✅ | Hardened real-ZMQ enforcement |
| DQN Training | `src/agents/train_dqn.py` | ✅ | SB3 DQN + Monitor |
| DQN Evaluation | `src/agents/eval_dqn.py` | ✅ | Deterministic eval |
| DQN vs Baseline | `src/analysis/compare_dqn_baseline.py` | ✅ | Comparison + figures |
| Excellent Acceptance Upgrade | `scripts/phase4/excellent_acceptance_upgrade.py` | ✅ | S2 training + all figures |

---

## 9. Smoke Test CSVs

| Artifact | Path | Status | Notes |
|----------|------|--------|-------|
| S1 Smoke Steps | `experiments/drl/logs/smoke_test_s1.csv` | ✅ | 10 steps, real ZMQ |
| S2 Smoke Steps | `experiments/drl/logs/smoke_test_s2.csv` | ✅ | 10 steps, real ZMQ |

---

## 10. Status Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Complete and verified |
| 🔄 | In progress (pending S2 training + excellent acceptance upgrade) |
| ⏳ | Planned for Phase 5 / Change 05 |

---

## 11. Key Result Summary (Current)

| Algorithm | Scenario | Throughput (Mbps) | Delay (ms)† | Loss Rate | Utility‡ |
|-----------|----------|:-----------------:|:-----------:|:---------:|:--------:|
| BBR | S1 | 9.727 | **25.9** | 0.000 | **0.947** |
| **DQN (ours)** | S1 | **9.877** | 115.3 | 0.004 | **0.900** |
| CUBIC | S1 | 9.894 | 117.7 | 0.001 | 0.884 |
| NewReno | S1 | 9.824 | 105.4 | 0.001 | 0.875 |
| NewReno | S2 | **9.794** | 129.4 | 0.001 | **0.923** |
| CUBIC | S2 | 9.588 | 156.3 | 0.009 | 0.818 |
| BBR ⚠️ | S2 | 0.385 | 148.7 | 0.016 | -0.169 |
| **DQN (ours)** | S2 | 🔄 | 🔄 | 🔄 | 🔄 |

> † delay proxy: FlowMonitor delaySum/rxPackets, NOT direct TCP RTT  
> ‡ Utility score is provisional (α=1.0, β=0.1, λ=10.0)  
> ⚠️ BBR S2 anomaly: known ns-3.40 TcpBbr limitation in high-RTT scenarios  
> S1 DQN honest result: ranks 2nd on utility (better than CUBIC/NewReno, below BBR)

---

*Last updated: 2026-06-09 | Phase 4 Excellent Acceptance Upgrade in progress*
