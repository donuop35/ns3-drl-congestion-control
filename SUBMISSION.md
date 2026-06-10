# 📋 Submission Guide — DRL-Based Congestion Control

## 1. 專題名稱

以深度強化學習進行單一瓶頸鏈路壅塞控制與吞吐量最佳化

## 2. 一句話論文主旨

本研究將單一瓶頸鏈路的壅塞控制建模為 MDP，透過 ns-3 / ns3-gym 環境訓練 DQN Agent，驗證 DRL 在 congestion control 領域的可行性與限制。

## 3. 建議優先閱讀

| 優先順序 | 文件 | 路徑 | 預計閱讀時間 |
|----------|------|------|-------------|
| 1 | 一頁式摘要 | `reports/final/final-one-page-summary.md` | 3 min |
| 2 | 老師閱讀導覽 | `reports/final/teacher-navigation-map.md` | 2 min |
| 3 | 完整期末報告 | `reports/final/final-report.md` | 10 min |
| 4 | 評分對齊矩陣 | `reports/final/grading-alignment-matrix.md` | 5 min |

## 4. 最終交付物一覽

| 交付物 | 路徑 | 狀態 |
|--------|------|------|
| 期末報告 | `reports/final/final-report.md` | ✅ |
| Final Figures | `figures/final/` | ✅ (9 張) |
| Demo Script | `demo/demo-script.md` | ✅ |
| 簡報大綱 | `slides/final/final-presentation-outline.md` | ✅ |
| Artifact Manifest | `reports/final/final-artifact-manifest.md` | ✅ |
| Reproducibility Guide | `reports/final/final-reproducibility-guide.md` | ✅ |
| 一頁式摘要 | `reports/final/final-one-page-summary.md` | ✅ |
| 評分對齊矩陣 | `reports/final/grading-alignment-matrix.md` | ✅ |
| 老師閱讀導覽 | `reports/final/teacher-navigation-map.md` | ✅ |
| Claims Guardrail | `reports/final/final-claims-guardrail.md` | ✅ |
| Phase 6 Extension Decision | `reports/final/phase6-extension-decision.md` | ✅ |

## 5. 核心結果摘要

### S1（低延遲瓶頸：10 Mbps, 10 ms）

DQN Utility 0.900，排名第 2（低於 BBR 0.947）。DQN 採取 100% Increase 退化策略，在低延遲環境中壓榨頻寬極限。

### S2（高延遲瓶頸：10 Mbps, 50 ms）

DQN Utility 0.757，排名第 3。DQN 丟包率 5.54%，暴露了粗粒度離散動作在高延遲環境下的限制。

## 6. 誠實揭露的限制

- Delay 為 FlowMonitor Proxy，非 true TCP RTT。
- Action 為 Sender-side Rate Abstraction（Fallback Option B），非 kernel-level TCP cwnd control。
- Utility 權重為 provisional。
- DQN 未全面勝過 TCP baselines。
- BBR S2 anomaly 為 ns-3.40 已知限制。
- Phase 6 已補回為 Conditional PPO Extension Decision Record：因 DQN Discrete(3) 動作限制，PPO / continuous action 是合理 future work，但本學期不實作，不影響 final result claims。

## 7. 如何重現圖表

```bash
python3 scripts/phase5/generate_final_figures.py
```

## 8. 如何驗證 Source Data

所有數據來自不可修改的凍結 CSV：

- `experiments/summaries/baseline_summary.csv`
- `experiments/drl/summaries/dqn_vs_baseline_summary.csv`

## 9. 本專題不宣稱

- 不宣稱 DQN 全面勝過 TCP。
- 不宣稱 production-ready。
- 不宣稱取代真實網路的 TCP 實作。
- 不宣稱 delay proxy 等同 true TCP RTT。
- 不宣稱 PPO 已實作或 PPO 一定反轉結果。

## 10. 建議評分路線

請參閱 `reports/final/teacher-navigation-map.md` 中的三條閱讀路線（5 分鐘 / 15 分鐘 / 30 分鐘）。
