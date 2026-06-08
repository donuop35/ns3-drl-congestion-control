## Purpose

定義 Change 02 baseline benchmark 的 metrics 定義、logging 要求、與輸出 artifacts 規格。

---

## Required Metrics

以下四個 metrics 為 MVP-required，所有 baselines 均必須產出：

| Metric | 欄位名稱 | 單位 | 計算方式 |
|--------|---------|------|---------|
| **Average Throughput** | `throughput_mbps` | Mbps | 實驗期間 goodput 的時間平均值 |
| **Average RTT / Delay** | `rtt_ms` | ms | 流量統計中的平均 delay；若 FlowMonitor 無法直接提供 RTT，使用 `delaySum / rxPackets`，並在 metadata 中標記計算方式 |
| **Packet Loss Rate** | `loss_rate` | fraction [0, 1] | `(txPackets - rxPackets) / txPackets`，若有 drop 統計優先使用 |
| **Utility Score** | `utility_score` | dimensionless | **Preliminary / Provisional**（見下方） |

### Utility Score（Provisional）

> ⚠️ **此欄位為 preliminary baseline visualization metric**。  
> 公式：`utility_score = throughput_norm - 0.1 × rtt_norm - 10.0 × loss_rate`  
> 其中 `throughput_norm` 和 `rtt_norm` 為歸一化值（以所有情境最大值為基準）。  
> **此公式與權重為 provisional，不代表最終 reward function。**  
> 最終 reward / utility 權重將在 Change 04 / Change 05 經 Spec Owner approval 後調整。

---

## Required Logs（Raw）

從 ns-3 simulation 產出的原始 log：

| 項目 | 格式 | 說明 |
|------|------|------|
| FlowMonitor XML | `.xml` | ns-3 FlowMonitor 標準輸出；包含 per-flow packet events |
| 或 ASCII trace | `.tr` | FlowMonitor 不可用時的 fallback |
| Per-flow statistics | (含於 XML 或 CSV) | txPackets, rxPackets, txBytes, rxBytes, delaySum, jitterSum, lostPackets |
| Experiment metadata | `metadata.yaml` | scenario ID, algo, seed, ns-3 version, simulation duration |

**Ambiguity Rules（當 FlowMonitor 欄位不直接可用時）**：

1. **若 RTT 不可直接從 FlowMonitor 取得**：使用 `delaySum / rxPackets` 作為 mean one-way delay；在 metadata 中標記為「estimated delay (not RTT)」
2. **若 packet loss 不可直接取得**：使用 `(txPackets - rxPackets) / txPackets` 計算；在 metadata 中記錄公式
3. **所有 baselines 必須使用相同的 measurement window**（固定 simulation duration 內）
4. **所有 plots 必須使用相同的 scenario 命名**（`scenario_a`, `scenario_b`）

---

## Required Output Artifacts

| Artifact | 路徑 | 說明 |
|----------|------|------|
| Raw FlowMonitor log | `experiments/logs/<scenario>_<algo>_seed<seed>/` | ns-3 原始輸出 |
| Summary CSV | `experiments/results/<scenario>_<algo>_seed<seed>.csv` | 含 7 個必要欄位 |
| Per-scenario summary table | `experiments/results/summary_table.csv` | 所有演算法、所有情境的摘要 |
| Baseline comparison table | `experiments/results/baseline_comparison.md` | markdown 格式，便於 README 引用 |
| Throughput figure | `figures/baseline_throughput_comparison.png` | grouped bar chart，>= 150 DPI |
| RTT / Delay figure | `figures/baseline_rtt_comparison.png` | grouped bar chart，>= 150 DPI |
| Loss rate figure | `figures/baseline_loss_comparison.png` | grouped bar chart，>= 150 DPI |
| Utility figure | `figures/baseline_utility_comparison.png` | grouped bar chart，provisional，>= 150 DPI |
| Experiment metadata | `experiments/results/<scenario>_<algo>_seed<seed>_metadata.yaml` | 含 ns-3 version, seed, duration 等 |

---

## CSV Schema

`experiments/results/<scenario>_<algo>_seed<seed>.csv` 必須包含以下欄位：

```
throughput_mbps, rtt_ms, loss_rate, utility_score, algo, scenario, random_seed
```

---

## Figure Requirements

所有 figures 必須：

- 標記的 X/Y 軸（含單位）
- 圖例（legend）清楚標示演算法名稱
- 各演算法顏色在所有 figures 中保持一致
- 解析度 >= 150 DPI
- 若 BBR 不可用，圖中省略 BBR 並加 warning 標注
