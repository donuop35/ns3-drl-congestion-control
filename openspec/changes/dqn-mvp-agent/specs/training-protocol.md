## Purpose

定義 Change 04 dqn-mvp-agent 的 DQN training protocol 規格，包含 training gate、training logging、model checkpoint concept、reproducibility metadata 與 training non-goals。

本檔案不含任何 training script 或程式碼；實際 training 在 Phase 4 執行。

---

## Training Mission

DQN training 的目標是讓 agent 學習在 ns-3.40 single bottleneck environment 中，透過 discrete action（decrease / keep / increase）控制 sender-side transmission intensity，以最大化 multi-objective reward（throughput ↑, delay ↓, loss ↓）。

Training 的直接輸出是：
1. **Model checkpoint**（evaluation input）
2. **Training logs**（training diagnostic）
3. **Training metadata**（reproducibility record）

Training reward curve 是 training diagnostic，**不是 final success criterion**。

---

## Training Environment Requirements

DQN training 開始前，以下條件必須全部滿足：

| Gate | 說明 | 驗收方式 |
|------|------|---------|
| **Smoke test PASSED** | Change 03 ST-01~ST-10 全部通過 | smoke test log 顯示 PASS |
| **Baseline available** | Phase 3 NewReno + CUBIC on S1 + S2 已完成 | Change 02 CSV 存在且非空 |
| **Config recorded** | training_config.yaml 已填寫（seed + scenario + reward weights + DQN hyperparams）| 檔案存在且完整 |
| **ns-3.40 verified** | ns-3 版本為 3.40 | `./ns3 --version` 輸出 3.40 |
| **SB3 installed** | Stable-Baselines3 已安裝 | `import stable_baselines3; print(stable_baselines3.__version__)` 成功 |

---

## Training Logging Requirements

每次 training run 必須產生以下 logs（路徑在 Phase 4 的 config 中確認）：

### training_log.csv

| 欄位 | 說明 | 記錄頻率 |
|------|------|---------|
| `timestep` | 全局 training step 計數 | Every step |
| `episode` | Episode 計數 | Per episode |
| `episode_reward` | 本 episode 的累積 reward | Per episode |
| `episode_length` | 本 episode 的 step 數 | Per episode |
| `exploration_rate` | 當前 ε 值 | Per episode |

### training_config.yaml

必須記錄（在 training 開始前填寫）：

```yaml
run_id: "<unique run identifier>"
scenario: "<scenario_a or scenario_b>"
random_seed: <int>
ns3_version: "3.40"
sb3_version: "<SB3 version>"
python_version: "<Python version>"
reward_weights:
  alpha: <float>
  beta: <float>
  lambda: <float>
dqn_hyperparameters:
  policy: "MlpPolicy"
  learning_rate: <float>
  batch_size: <int>
  buffer_size: <int>
  learning_starts: <int>
  target_update_interval: <int>
  exploration_fraction: <float>
  exploration_final_eps: <float>
  gamma: <float>
  train_freq: <int>
  gradient_steps: <int>
  total_timesteps: <int>
training_start_time: "<ISO8601>"
training_end_time: "<ISO8601>"
```

### episode_rewards.csv

| 欄位 | 說明 |
|------|------|
| `episode_num` | Episode 序號（從 0 開始）|
| `total_reward` | 本 episode 累積 reward |
| `episode_length` | 本 episode step 數 |
| `mean_throughput_mbps` | 本 episode 平均 throughput（from info dict）|
| `mean_delay_ms` | 本 episode 平均 delay |
| `mean_loss_rate` | 本 episode 平均 loss rate |
| `mean_utility_score` | 本 episode 平均 utility |

---

## Model Checkpoint Concept

| 概念 | 說明 |
|------|------|
| **Format** | SB3 native `.zip`（包含 policy weights + replay buffer state + optimizer state）|
| **Frequency** | 每固定 timestep interval 儲存一次（e.g., every 10,000 steps）；具體值在 Phase 4 確認 |
| **Final checkpoint** | Training 完成時的最後一個 checkpoint，作為 evaluation 的 input |
| **Checkpoint ≠ success** | Checkpoint 的存在不代表 DQN 訓練成功；success 由 evaluation metrics 決定 |
| **Path** | `experiments/logs/training/run_<id>_<scenario>_seed<seed>/dqn_checkpoint.zip` |

---

## Reproducibility Metadata

以下 metadata 必須確保在相同配置下可重現訓練結果：

1. **Fixed random seed**: Python random、NumPy、PyTorch seed 均設為相同值
2. **Fixed ns-3 seed**: `ns3::RngSeedManager::SetSeed(seed)` and `SetRun(run)`（繼承 Change 03）
3. **Fixed SB3 seed**: SB3 `DQN(seed=<seed>)`
4. **Frozen ns-3.40**: Simulator 版本固定（繼承 Change 02）
5. **Recorded config**: training_config.yaml 記錄所有超參數和環境配置

> ⚠️ **Reproducibility criterion**: 相同 seed + config 下，重複 training 的 episode reward 曲線應 metric-equivalent（不要求 bit-for-bit identical；繼承 Change 02 的 reproducibility philosophy）

---

## Training Non-Goals

以下事項明確**不在** training protocol 範圍內：

> ⛔ **不做 hyperparameter tuning study** — 初始值按 design.md 設定；tuning 留 Change 05  
> ⛔ **不做 ablation study** — reward / observation ablation 留 Change 05  
> ⛔ **不訓練 PPO** — PPO 為 future extension  
> ⛔ **不用 training reward curve 作為 final success criterion** — 必須有獨立 evaluation  
> ⛔ **不在 training 中做 DQN vs baseline 比較** — 比較在 evaluation 後進行  
> ⛔ **不在 training 中產生 final figures** — figures 在 evaluation + Change 05 中產生
