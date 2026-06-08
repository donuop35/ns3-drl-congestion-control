## Purpose

定義 Change 04 dqn-mvp-agent 的 DQN evaluation protocol 規格，包含 training / evaluation 分離原則、evaluation metrics、evaluation scenarios、comparison targets 與 interpretation rules。

本檔案不含任何 evaluation script；實際 evaluation 在 Phase 4 執行。

---

## Separate Evaluation Principle

**Training reward curve ≠ DQN success criterion。**

DQN evaluation 必須是獨立的 pass，使用：
- 固定的 deterministic policy（ε = 0，或 exploration disabled）
- Trained checkpoint（Final model）
- Raw metrics from info dict（不是 training reward）
- 與 Change 02 baseline 對齊的 metrics

```
┌─────────────────────────────────────────────────────────┐
│  Training Phase             │  Evaluation Phase          │
│  ─────────────────          │  ──────────────────        │
│  ε-greedy exploration       │  Deterministic policy      │
│  Reward accumulates         │  Raw metrics extracted     │
│  Checkpoint saved           │  Checkpoint loaded         │
│  training_log.csv           │  evaluation_results.csv    │
│  Diagnostic only            │  Success criteria applied  │
└─────────────────────────────────────────────────────────┘
```

---

## Evaluation Mission

1. **Quantify DQN network performance** under Change 02 scenarios（S1 / S2）
2. **Compare with baseline** NewReno / CUBIC（Required）and BBR（if available）
3. **Produce baseline-compatible metrics** for final report / PPT / README

---

## Evaluation Metrics

每個 evaluation episode 必須提取以下 metrics（從 info dict）：

| Metric | Source field | Unit | Aggregation |
|--------|-------------|------|-------------|
| Throughput | `info["raw_throughput_mbps"]` | Mbps | Mean over episode |
| Delay | `info["raw_delay_ms"]` | ms | Mean over episode |
| Loss rate | `info["raw_loss_rate"]` | fraction [0,1] | Mean over episode |
| Utility score | `info["utility_score"]` | dimensionless | Mean over episode |
| Episode reward | Sum of r_t | dimensionless | Sum per episode |

### Aggregation Across Episodes

若評估多個 episode（建議 ≥ 3 episodes per scenario per run）：
- 報告 mean ± std（均值與標準差）
- 若只評估 1 episode，必須在 limitation 中說明

---

## Evaluation Scenarios

| Scenario | Status | Description |
|---------|--------|-------------|
| **S1** | **MVP-Required** | Low latency：10 Mbps BW，10 ms delay，60s duration，seed 42 |
| **S2** | **MVP-Required** | High latency：10 Mbps BW，50 ms delay，60s duration，seed 42 |
| S3, S4 | Optional | 繼承 Change 02 scenario-matrix.md；不得阻塞 S1/S2 |

---

## Comparison Targets

| Target | Status | Metric source |
|--------|--------|--------------|
| NewReno | **Required** | Change 02 baseline CSV |
| CUBIC | **Required** | Change 02 baseline CSV |
| BBR | Strongly recommended（non-blocking）| Change 02 baseline CSV（or BBR_SKIPPED.md）|
| Random agent | Optional | Smoke test baseline |
| Heuristic policy | Optional | Ad-hoc comparison |

---

## Evaluation Output Artifacts

```
experiments/results/dqn/
  <scenario>_DQN_seed<seed>_run<id>.csv     # per-episode evaluation metrics
  evaluation_summary.csv                     # aggregated comparison table
```

### evaluation_summary.csv Schema

| 欄位 | 說明 |
|------|------|
| `algorithm` | "DQN" / "NewReno" / "CUBIC" / "BBR" |
| `scenario` | "scenario_a" / "scenario_b" |
| `mean_throughput_mbps` | 平均 throughput |
| `mean_delay_ms` | 平均 delay |
| `mean_loss_rate` | 平均 loss rate |
| `mean_utility_score` | 平均 utility |
| `mean_episode_reward` | 平均 episode reward（DQN only）|
| `std_throughput_mbps` | Throughput 標準差（若多 episodes）|
| `run_id` | DQN run identifier |
| `seed` | Random seed |

---

## Interpretation Rules

### Rule 1：Always Use Raw Metrics

最終評估**必須**使用 `raw_throughput_mbps`、`raw_delay_ms`、`raw_loss_rate`、`utility_score`。不得只使用 `episode_reward` 作為 DQN 優越性的依據。

### Rule 2：Scenario-Level Comparison

比較 DQN 與 baseline 時，必須在相同 scenario（S1 / S2）下比較，不得跨 scenario 混用。

### Rule 3：Acknowledge Underperformance

若 DQN 在某個 metric 或 scenario 中輸給 baseline：
- **必須誠實記錄**，不得省略
- 轉換為 limitation / future work
- 可能的原因分析（e.g., reward shaping、exploration、convergence）

### Rule 4：BBR Non-Blocking

若 BBR 在 ns-3.40 不可用，DQN evaluation 仍可完成。BBR 只作為 strongly recommended comparison。

### Rule 5：Evaluation Before Final Report

Final GitHub README / PPT / video 中的 DQN performance 數字，**必須**來自本 evaluation protocol 的結果，不得使用 training log 中的 reward 數字作為 performance 宣稱。
