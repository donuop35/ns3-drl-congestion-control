## Purpose

定義 Change 04 dqn-mvp-agent 的 baseline comparison 規格，包含 required / strongly recommended / optional comparisons、metric alignment with Change 02 與 DQN underperformance interpretation rules。

---

## Required Comparisons

以下比較在 DQN evaluation 後**必須**完成：

| Comparison | Scenarios | Metrics |
|-----------|---------|--------|
| DQN vs NewReno | S1 + S2 | throughput / delay / loss / utility |
| DQN vs CUBIC | S1 + S2 | throughput / delay / loss / utility |

---

## Strongly Recommended Comparisons

| Comparison | Scenarios | Fallback |
|-----------|---------|--------|
| DQN vs BBR | S1 + S2 | If BBR unavailable in ns-3.40, create `BBR_SKIPPED.md` and skip this comparison（繼承 Change 02 R-02-01）|

---

## Optional Comparisons

| Comparison | Purpose |
|-----------|---------|
| DQN vs Random Agent | 作為最低基準（smoke test baseline）|
| DQN vs Heuristic Policy | 探索性比較，不影響 MVP success criteria |

---

## Metric Alignment with Change 02

DQN evaluation 必須與 Change 02 baseline 使用相同的 metric 定義：

| Metric | Change 02 source | DQN source | Required alignment |
|--------|-----------------|-----------|------------------|
| Throughput | `throughput_mbps` column in baseline CSV | `info["raw_throughput_mbps"]` | Same unit: Mbps |
| Delay | `rtt_ms` or `delay_ms` in baseline CSV | `info["raw_delay_ms"]` | Same unit: ms |
| Loss rate | `loss_rate` in baseline CSV | `info["raw_loss_rate"]` | Same unit: fraction [0,1] |
| Utility score | `utility_score` in baseline CSV | `info["utility_score"]` | Same formula（provisional）|

> ⚠️ 若計算方式有差異（e.g., delay 的定義不同），必須在 limitation 中明確說明。

---

## Comparison Scope Rules

1. **Same scenario**: DQN 和 baseline 的比較必須在相同 scenario（S1 / S2）下進行；不得跨 scenario 混用
2. **Same simulation duration**: DQN episode 的 simulation duration 必須與 Change 02 baseline scenario 相同（e.g., 60 秒）
3. **Same random seed（where applicable）**: 若 baseline 使用固定 seed（Change 02: seed = 42），DQN evaluation 也應使用相同 seed
4. **No mixing of training reward and baseline metrics**: 不得用 DQN 的 training episode reward 與 baseline 的 throughput 直接比較

---

## Comparison Output Format

### Required：Comparison Table（per scenario）

```
Scenario A (S1 - Low Latency)
─────────────────────────────────────────────────────────
Algorithm   | Throughput (Mbps) | Delay (ms) | Loss | Utility
────────────|───────────────────|────────────|──────|─────────
NewReno     |        X.X        |    XX.X    | X.XX |  X.XX
CUBIC       |        X.X        |    XX.X    | X.XX |  X.XX
BBR*        |        X.X        |    XX.X    | X.XX |  X.XX
DQN (ours)  |        X.X        |    XX.X    | X.XX |  X.XX
─────────────────────────────────────────────────────────
* BBR: if available; otherwise show N/A
```

### Required：Grouped Bar Charts（per metric）

- `figures/dqn_vs_baseline_throughput.png`：DQN + baselines，per scenario
- `figures/dqn_vs_baseline_delay.png`
- `figures/dqn_vs_baseline_loss.png`
- `figures/dqn_vs_baseline_utility.png`

---

## Interpretation Rules

### IF DQN ≥ NewReno AND DQN ≥ CUBIC on throughput（with acceptable delay / loss）
→ **Partial success or full success**（depends on all metrics）  
→ Present as positive contribution in final report

### IF DQN < NewReno AND DQN < CUBIC on most metrics
→ **Failure but reportable**（see `success-failure-criteria.md`）  
→ Do NOT hide results  
→ Analyze possible causes：reward design / exploration / convergence / training duration  
→ Present as limitation + future work  
→ DQN still provides valuable experimental findings（e.g., partial convergence, specific metric improvement）

### IF BBR is unavailable
→ Create `BBR_SKIPPED.md` with explanation  
→ Comparison table shows "N/A" for BBR  
→ This does NOT affect MVP success criteria  

### IF DQN outperforms BBR but not NewReno/CUBIC
→ Report honestly  
→ Partial success：DQN shows competitiveness with BBR  
→ Future work：improve NewReno/CUBIC comparison

### IF evaluation metrics diverge greatly across episodes（high std）
→ Report mean ± std  
→ Discuss possible causes（stochastic env, training instability）  
→ May indicate need for more training or seed averaging（future work）

---

## What to Do If DQN Loses

**DQN underperformance is NOT automatic failure.** The following steps apply:

1. **Record honest results**: Include all metrics in comparison table
2. **Analyze**: Document possible causes in final report（reward shaping, convergence, environment complexity）
3. **Present as limitation**: Frame underperformance as limitation and future work direction
4. **Do NOT re-train** without reporting to Spec Owner
5. **Do NOT cherry-pick** the best episode and present it as representative result without disclosing selection criteria
