## Purpose

定義 Change 04 dqn-mvp-agent 的 output artifacts 規格，包含 required logs、required figures、required tables、artifact naming philosophy 與 README / PPT / 10-minute video support 規格。

---

## Required Logs

```
experiments/
  logs/
    training/
      run_<run_id>_<scenario>_seed<seed>/
        training_config.yaml          # REQUIRED before training starts
        training_log.csv              # per-step / per-episode training data
        episode_rewards.csv           # per-episode summary
        dqn_checkpoint.zip            # SB3 model checkpoint (evaluation input)
        BBR_SKIPPED.md                # if BBR unavailable (optional)
  results/
    baseline/
      <scenario>_<algo>_seed<seed>.csv  # Change 02 baseline CSVs
    dqn/
      <scenario>_DQN_seed<seed>_run<id>.csv  # per-episode evaluation metrics
      evaluation_summary.csv                  # aggregated comparison
```

### Log File Requirements

| File | Required | Content |
|------|---------|---------|
| `training_config.yaml` | **Required** | All hyperparameters + reward weights + seed + versions |
| `training_log.csv` | **Required** | timestep, episode, episode_reward, episode_length, exploration_rate |
| `episode_rewards.csv` | **Required** | Per-episode summary with raw metrics from info dict |
| `dqn_checkpoint.zip` | **Required** | SB3 native format |
| `evaluation_summary.csv` | **Required** | Final comparison table（DQN + baselines, all metrics）|
| `BBR_SKIPPED.md` | If applicable | Reason BBR was skipped in ns-3.40 |

---

## Required Figures

All figures must meet：
- Resolution ≥ 150 DPI
- Labeled axes with units
- Legend identifying each algorithm
- Consistent algorithm color coding across figures

| Figure filename | Content | Required |
|----------------|---------|---------|
| `figures/dqn_training_reward_scenario_a.png` | Episode reward vs training steps, Scenario A (S1) | **Required** |
| `figures/dqn_training_reward_scenario_b.png` | Episode reward vs training steps, Scenario B (S2) | **Required** |
| `figures/dqn_vs_baseline_throughput.png` | Grouped bar chart：DQN + baselines, per scenario, throughput | **Required** |
| `figures/dqn_vs_baseline_delay.png` | Grouped bar chart：delay | **Required** |
| `figures/dqn_vs_baseline_loss.png` | Grouped bar chart：loss rate | **Required** |
| `figures/dqn_vs_baseline_utility.png` | Grouped bar chart：utility score | **Required** |
| `figures/baseline_throughput_comparison.png` | Baseline-only comparison（from Change 02）| Required（inherits）|
| `figures/baseline_rtt_comparison.png` | Baseline-only RTT（from Change 02）| Required（inherits）|
| `figures/baseline_loss_comparison.png` | Baseline-only loss（from Change 02）| Required（inherits）|

---

## Required Tables

### Table 1：DQN vs Baseline Comparison（Scenario S1）

| Algorithm | Throughput (Mbps) | Delay (ms) | Loss Rate | Utility Score |
|-----------|-------------------|------------|-----------|---------------|
| NewReno | | | | |
| CUBIC | | | | |
| BBR* | | | | |
| DQN（ours）| | | | |

### Table 2：DQN vs Baseline Comparison（Scenario S2）

（Same structure as Table 1）

### Table 3：DQN Training Configuration

| Parameter | Value |
|-----------|-------|
| Algorithm | SB3 DQN |
| Policy | MlpPolicy |
| α（reward weight）| |
| β（delay penalty）| |
| λ（loss penalty）| |
| learning_rate | |
| batch_size | |
| total_timesteps | |
| seed | |
| ns-3 version | 3.40 |

---

## Artifact Naming Philosophy

| Convention | Rule |
|------------|------|
| Scenario name | `scenario_a` = S1（low latency）, `scenario_b` = S2（high latency）|
| Algorithm name | `NewReno`, `CUBIC`, `BBR`, `DQN`（consistent capitalization）|
| Seed format | `seed42`（no underscore between seed and number）|
| Run ID format | `run_001`, `run_002`（zero-padded）|
| Figure naming | `dqn_vs_baseline_<metric>.png`（lowercase with underscores）|
| CSV naming | `<scenario>_<algorithm>_seed<seed>.csv` for baseline；`<scenario>_DQN_seed<seed>_run<id>.csv` for DQN |

---

## README Support

The project README must include a DQN Results section containing：

1. **Summary comparison table**（Table 1 + Table 2，or combined）
2. **At least one grouped bar figure**（e.g., `dqn_vs_baseline_utility.png`）
3. **Training configuration table**（Table 3）
4. **Brief interpretation**（2–4 sentences）：
   - What DQN achieved
   - How DQN compares to baselines
   - Limitations and future work

README must NOT：
- Claim DQN outperforms baseline without evidence
- Hide underperformance results
- Use training reward as the only performance metric

---

## PPT Support

PPT slides must include：

| Slide type | Content |
|-----------|---------|
| **Baseline results** | Change 02 baseline comparison charts |
| **DQN training progress** | Training reward curve（S1 + S2）|
| **DQN vs baseline** | 4 grouped bar charts（throughput / delay / loss / utility）|
| **Comparison table** | Summary table for S1 and S2 |
| **DQN interpretation** | What the results mean（success / partial success / limitation）|
| **Future work** | Reward ablation / PPO / advanced observation（as extension）|

---

## 10-Minute Video Support

The 10-minute demo / explanation video must cover：

1. **Problem statement** (1–2 min)：DRL for congestion control over single bottleneck
2. **Baseline benchmark** (1–2 min)：NewReno vs CUBIC vs BBR（Change 02 results）
3. **DRL environment** (1–2 min)：MDP interface, observation, action, reward（Change 03）
4. **DQN training** (1–2 min)：Training curve, convergence（or non-convergence explanation）
5. **DQN vs baseline** (2–3 min)：Comparison charts and interpretation
6. **Conclusion** (1 min)：Summary, limitations, future work

All figures shown in the video must be the same figures generated from the actual experiment（no mock-up or placeholder）.
