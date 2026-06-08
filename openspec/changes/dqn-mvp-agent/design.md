## Context

本 change 承接三個已凍結的上游 changes：

| Change | 凍結內容 |
|--------|---------|
| Change 01 project-charter | 題目、scope、toolchain、baseline list、metrics、MVP definition |
| Change 02 ns3-baseline-benchmark | ns-3.40 凍結、NewReno/CUBIC/BBR roles、scenario matrix S1/S2、throughput/RTT/loss/utility |
| Change 03 opengym-env | MDP M=(S,A,P,R,γ)、observation [5]、Discrete(3) action、reward concept、smoke test ST-01~10、info dict |

---

## Design Goal

1. 將 Change 03 environment 與 SB3 DQN agent 的訓練 / 評估規格完整定義
2. 確保 DQN evaluation 可與 Change 02 baseline 做公正比較
3. 確保 DQN underperformance 有明確的 reportable fallback，不影響論文完整性
4. 確保 Phase 4 實作可直接遵循本 change 的 spec 而不需要再做設計決策

---

## DQN MVP Boundary

### Algorithm Selection

| 項目 | 決定 |
|------|------|
| **Algorithm** | Stable-Baselines3（SB3）DQN |
| **Policy** | `MlpPolicy`（預設候選；可在 Change 04 implementation 中評估其他 policy，但 MlpPolicy 為 baseline candidate）|
| **Observation** | 繼承 Change 03：shape [5]（throughput_norm / delay_norm / loss_norm / congestion_indicator / prev_action_norm）|
| **Action space** | 繼承 Change 03：Discrete(3)（0: decrease, 1: keep, 2: increase）|
| **Reward** | 繼承 Change 03：r = α·t_norm − β·d_norm − λ·l_norm（weights 在本 change 定義初始值）|
| **Framework** | Python；Stable-Baselines3；Gymnasium-compatible env wrapper |

### Initial Reward Weights（Change 04 定義，Change 05 可調整）

| 權重 | 初始建議值 | 說明 |
|------|-----------|------|
| α | 1.0 | Throughput 正向激勵 |
| β | 0.1 | Delay 懲罰（不過度保守）|
| λ | 10.0 | Loss 懲罰（與 Change 02 utility formula 參考對齊）|

> ⚠️ 以上為初始建議值，非固定值。Change 05 ablation study 可在 Spec Owner approval 下調整。

### DQN Hyperparameter Starting Point

| 超參數 | 初始建議值 | 說明 |
|-------|-----------|------|
| `learning_rate` | 1e-3 | Adam optimizer |
| `batch_size` | 32 | Replay buffer sample size |
| `buffer_size` | 50000 | Replay buffer capacity |
| `learning_starts` | 1000 | Steps before first gradient update |
| `target_update_interval` | 500 | Steps between target network updates |
| `exploration_fraction` | 0.1 | Fraction of training for ε-greedy decay |
| `exploration_final_eps` | 0.05 | Final ε value |
| `gamma` | 0.99 | Discount factor（與 Change 03 一致）|
| `train_freq` | 1 | Update every step |
| `gradient_steps` | 1 | Gradient steps per update |

> ⚠️ 以上為初始建議值。Change 04 實作可調整，但必須記錄所有超參數於 metadata。

---

## Decisions

### DR-04-01：Use DQN as MVP

**Decision**: MVP algorithm 固定為 SB3 DQN（Deep Q-Network）。  
**Rationale**: DQN 是最簡單可行的 value-based discrete-action RL algorithm；MlpPolicy 適合低維 observation space；SB3 提供可重現的 reference implementation。  
**Rule**: 不得改為 PPO、SAC、TD3 等 policy gradient 方法，除非另開 OpenSpec change 並獲 Spec Owner 批准。

### DR-04-02：Keep PPO as Future Extension

**Decision**: PPO 不在 Change 04 MVP scope 內。  
**Rationale**: PPO 通常用於 continuous action 或複雜 policy；本 MVP 使用 Discrete(3)，DQN 更直接；過早引入 PPO 會使 baseline comparison 複雜化。  
**Extension rule**: PPO 若在未來引入，必須另開 OpenSpec change，定義新的 action space 和 policy gradient 訓練規格。

### DR-04-03：Use Separate Evaluation

**Decision**: Training reward curve 不能作為唯一成功指標；必須有獨立的 evaluation pass。  
**Rationale**: Training reward 可能因 reward shaping 而高估 DQN 真實網路性能；獨立 evaluation 使用 raw metrics（throughput / RTT / loss / utility）才能與 baseline 公正比較。  
**Rule**: Evaluation 必須在 training 完成後進行，使用 deterministic policy（ε = 0 或最終 checkpoint），在 S1 / S2 各跑至少 1 個 evaluation episode。

### DR-04-04：Preserve Baseline-Compatible Metrics

**Decision**: DQN evaluation 的 metrics 必須與 Change 02 baseline 的 metrics 使用相同單位和計算方式。  
**Rationale**: 若 DQN evaluation metrics 與 baseline metrics 量綱不同，比較結果無效。  
**Rule**: DQN evaluation 的 `raw_throughput_mbps`、`raw_delay_ms`、`raw_loss_rate`、`utility_score` 必須從 info dict 提取，與 Change 02 CSV schema 對齊。

### DR-04-05：DQN Underperformance is Reportable

**Decision**: DQN 不收斂、不穩定、或輸給 NewReno / CUBIC / BBR 均不是自動失敗。  
**Rationale**: 網路壅塞控制是困難的 RL 問題；DQN 的 partial success 或 failure 可以作為 limitation / future work，並提供有價值的實驗發現。  
**Rule**: Final report 必須誠實記錄 DQN 的 evaluation results，不得隱藏 underperformance；stop rule（見 `success-failure-criteria.md`）定義何時必須停止 training 並回報。

### DR-04-06：Official OpenSpec Only

**Decision**: 本 change 的所有 artifacts 必須在官方 `@fission-ai/openspec@1.4.1` CLI 產生的 `openspec/changes/dqn-mvp-agent/` 目錄下建立。  
**Rule**: `openspec-preview/` 只作為歷史參考，不得視為正式規格。不得自行模擬 OpenSpec workflow。

---

## Training Protocol Design

### Training Gate

在 DQN training 開始前，必須滿足：

1. **Change 03 smoke test PASSED**（ST-01 ~ ST-10 全部通過）
2. **Change 02 baseline results available**（至少 NewReno + CUBIC on S1 + S2）
3. **Training config recorded**（seed / scenario / reward weights / DQN hyperparameters）

### Training Logging Requirements

每次 training run 必須記錄：

```
logs/training/
  run_<run_id>_<scenario>_seed<seed>/
    training_log.csv          # step, episode, reward, length
    training_config.yaml      # all hyperparameters + reward weights + seed
    episode_rewards.csv       # episode_num, total_reward, episode_length
    dqn_checkpoint.zip        # SB3 model checkpoint (evaluation input only)
    BBR_SKIPPED.md            # if BBR unavailable (inherits from Change 02)
```

### Model Checkpoint Concept

- Checkpoint 是 evaluation 的 input，不是 final success 的宣告
- Checkpoint 在 Change 04 實作中按固定 interval 儲存（e.g., every 10000 steps）
- Final checkpoint = training 完成時的最後一個 checkpoint
- Checkpoint format：SB3 native `.zip`（包含 policy weights + optimizer state）

### Reproducibility Metadata

每次 run 的 metadata 必須記錄：

```yaml
run_id: "run_001"
scenario: "scenario_a"          # S1
random_seed: 42
ns3_version: "3.40"
sb3_version: "<actual version>"
python_version: "<actual version>"
reward_weights:
  alpha: 1.0
  beta: 0.1
  lambda: 10.0
dqn_config:
  learning_rate: 1e-3
  batch_size: 32
  ...
training_start_time: "<ISO8601>"
training_end_time: "<ISO8601>"
total_timesteps: <int>
```

---

## Evaluation Protocol Design

### Separate Evaluation Principle

```
Training Phase          Evaluation Phase
─────────────           ─────────────────
DQN trains              DQN checkpoint loaded
ε-greedy explore        ε = 0 (deterministic)
reward ← training       metrics ← raw FlowMonitor
checkpoint saved        → comparison table
                        → figures
```

- Training 和 Evaluation 必須是兩個獨立的 pass
- Evaluation 使用 deterministic policy（不探索）
- Evaluation metrics 從 info dict 提取 raw values

### Evaluation Metrics（每 scenario 每 run）

| Metric | Source | Unit |
|--------|--------|------|
| Mean throughput | `info["raw_throughput_mbps"]` | Mbps |
| Mean delay | `info["raw_delay_ms"]` | ms |
| Mean loss rate | `info["raw_loss_rate"]` | fraction [0,1] |
| Mean utility | `info["utility_score"]` | dimensionless |
| Mean episode reward | Sum of r_t / episode length | dimensionless |

### MVP-Required Evaluation Scenarios

| Scenario | Status |
|---------|--------|
| S1（低延遲，10 Mbps BW，10 ms delay）| **Required** |
| S2（高延遲，10 Mbps BW，50 ms delay）| **Required** |
| S3, S4 | Optional（同 Change 02 scenario-matrix.md）|

---

## Baseline Comparison Design

### Required Comparisons

| Comparison | Status |
|-----------|--------|
| DQN vs NewReno | **Required** |
| DQN vs CUBIC | **Required** |

### Strongly Recommended

| Comparison | Status |
|-----------|--------|
| DQN vs BBR | **Strongly recommended**（if ns-3.40 BBR available；non-blocking）|

### Optional

| Comparison | Status |
|-----------|--------|
| DQN vs Random Agent | Optional（smoke test baseline）|
| DQN vs Heuristic Policy | Optional |

### Metric Alignment with Change 02

DQN evaluation metrics 必須與 Change 02 baseline 在相同 scenario（S1 / S2）、相同 random seed、相同 ns-3.40 simulation duration 下比較。若有差異，必須在 limitation 中說明。

### DQN Underperformance Interpretation

| DQN result vs baseline | Interpretation |
|------------------------|---------------|
| DQN ≥ baseline on all metrics | Full success |
| DQN ≥ baseline on throughput + acceptable delay/loss | Partial success |
| DQN < baseline on all metrics | Failure but reportable → limitation + future work |
| DQN converges but underperforms BBR only | Partial success（BBR 非 required）|

---

## Artifact Design

### Required Logs

```
experiments/
  results/dqn/
    <scenario>_DQN_seed<seed>.csv       # evaluation metrics per episode
  logs/training/
    run_<id>_<scenario>_seed<seed>/
      training_log.csv
      training_config.yaml
      dqn_checkpoint.zip
```

### Required Figures

| Figure | Description |
|--------|-------------|
| `figures/dqn_training_reward_<scenario>.png` | Episode reward vs training steps |
| `figures/dqn_vs_baseline_throughput.png` | Grouped bar: DQN + baselines, per scenario |
| `figures/dqn_vs_baseline_delay.png` | Grouped bar: delay comparison |
| `figures/dqn_vs_baseline_loss.png` | Grouped bar: loss rate comparison |
| `figures/dqn_vs_baseline_utility.png` | Grouped bar: utility score comparison |

### Required Tables

| Table | Description |
|-------|-------------|
| Summary comparison table | DQN vs NewReno vs CUBIC vs BBR（if available），per scenario, all 4 metrics |
| Training configuration table | All hyperparameters + reward weights |

### README / PPT / Video Support

- **README**: 必須包含 DQN results section（使用 summary table + 至少一張 figure）
- **PPT**: 每個 metric 一張 grouped bar chart；training reward curve；comparison table
- **10-minute video**: Figures 必須可在 video 中清楚呈現；narration 必須解釋 DQN 結果（含 underperformance）

---

## Success / Failure Design

詳見 `specs/success-failure-criteria.md`。摘要：

| Level | 條件 |
|-------|------|
| **Full Success** | DQN converges + ≥ baseline on throughput + acceptable delay/loss in both S1 + S2 |
| **Partial Success** | DQN converges in ≥ 1 scenario or ≥ 1 metric improvement over at least 1 baseline |
| **Failure but Reportable** | DQN converges but underperforms all baselines → report as limitation |
| **Stop Rule** | DQN reward diverges / non-finite OR smoke test fails → stop and report to Spec Owner |

---

## Extension Governance

| Extension | Status | Requirement to unlock |
|-----------|--------|----------------------|
| Reward ablation study | Future extension | Change 05 with Spec Owner approval |
| Observation ablation | Future extension | Separate OpenSpec change |
| PPO | Future extension | Separate OpenSpec change |
| Continuous action | Future extension | Separate OpenSpec change |
| Double DQN / Dueling DQN | Optional enhancement within Change 04 | Must document in run metadata |
| S3 / S4 scenarios | Optional | Must not block S1/S2 MVP |

> ⛔ All extensions MUST NOT block MVP completion.

---

## Risks / Trade-offs

詳見 `specs/drl-risk-register.md`。主要風險摘要：

| Risk | Mitigation |
|------|-----------|
| DQN 不收斂 | Stop rule + reportable fallback |
| Reward 爆炸（非有限）| Reward clipping + stop rule |
| Smoke test fail | 修復 environment 後才繼續 |
| DQN 輸給所有 baseline | Reportable limitation，不是自動失敗 |
| PPO 被提前導入 | DR-04-02 明確禁止 |
| Training / evaluation metrics 不對齊 | DR-04-04 規定 metric alignment |

---

## Open Questions

| # | 問題 | 狀態 |
|---|------|------|
| OQ-04.01 | MlpPolicy 的具體 hidden layer size（e.g., [64, 64] vs [256, 256]）| ⏳ Change 04 implementation 開始時確認 |
| OQ-04.02 | Training timesteps 的具體數量（e.g., 100k vs 500k）| ⏳ 依環境收斂速度調整，在 implementation 中記錄 |
| OQ-04.03 | Decision interval 的具體長度（OQ-03.01 繼承）| ⏳ Smoke test 後確認 |
| OQ-04.04 | 是否需要 Double DQN 或 Dueling DQN 作為 MVP 增強 | ⏳ 可選；若採用必須在 run metadata 中記錄 |
