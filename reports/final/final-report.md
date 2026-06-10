# Final Report：DRL-Based Congestion Control over a Bottleneck Link

## Executive Summary
本專題探討在單一瓶頸鏈路（Single Bottleneck Link）上，應用深度強化學習（DRL, 具體為 DQN）進行擁塞控制（Congestion Control）之可行性。透過整合 `ns-3.40` 網路模擬器與 `Stable-Baselines3`，我們建立了一個受 OpenSpec 嚴格治理的重現環境。主要結果顯示，DQN 在低延遲（S1, 10ms）場景下可學到近乎滿載（near-capacity）的退化策略，獲得僅次於 BBR 的第二名效用表現（0.900）；但在高延遲（S2, 50ms）場景中，DQN 暴露出容忍高丟包（5.54%）以換取吞吐量的限制。本報告忠實呈現 MVP 的潛力與限制，**不宣稱** DQN 全面打敗 TCP。

## Contribution Summary
本研究之主要貢獻包含：
- 建立並驗證了受 OpenSpec 治理的 DRL 網路擁塞控制測試平台。
- 完成 ns-3 單一瓶頸鏈路的傳統 TCP (NewReno, CUBIC, BBR) 效能 benchmark。
- 成功實作 ns3-gym DQN MVP。
- 提供完整且可追溯的 final reproducibility package。
- 誠實報告與揭露 RL 在高延遲與簡單獎勵約束下之行為與限制（Honest limitation reporting）。

## OpenSpec SDD Methodology
為了確保研究過程的嚴謹與不可竄改性，本專題導入了 OpenSpec 規格驅動開發（Spec-Driven Development）。
- Phase 0 至 Phase 5 的每一步變更，皆由 `openspec` CLI 工具所產生的 `proposal`, `specs`, `design`, `tasks` 進行治理。
- 所有的 source-of-truth artifacts (如 CSV) 一旦凍結後即禁止手動竄改，避免「挑櫻桃」(cherry-picking) 數據。這保障了實驗結論的客觀可信度。

## Experiment Source Mapping
本報告內的所有數據皆來自不可修改的實驗記錄：
- Baseline results 來自：`experiments/summaries/baseline_summary.csv`
- DQN results 來自：`experiments/drl/summaries/dqn_summary.csv`
- DQN 與 Baseline 比較數據來自：`experiments/drl/summaries/dqn_vs_baseline_summary.csv`
- Final figures 皆由 `scripts/phase5/generate_final_figures.py` 讀取上述 CSV 動態產生，絕無手動繪圖或改數字。

## Results

### S1 Result Table (Low Delay Bottleneck: 10 Mbps, 10 ms)
| Scenario | Method | Throughput (Mbps) | Delay Proxy (ms) | Loss Rate | Utility | Rank | Notes |
|----------|--------|-------------------|------------------|-----------|---------|------|-------|
| S1 | BBR | 9.73 | 25.9 | 0.000000 | 0.947 | 1 | Best overall |
| S1 | DQN (ours) | 9.88 | 115.3 | 0.004040 | 0.900 | 2 | Degenerate policy (100% Increase) |
| S1 | CUBIC | 9.89 | 117.7 | 0.000504 | 0.884 | 3 | High throughput, moderate delay |
| S1 | NewReno | 9.82 | 105.4 | 0.000731 | 0.875 | 4 | |

### S2 Result Table (High Delay Bottleneck: 10 Mbps, 50 ms)
| Scenario | Method | Throughput (Mbps) | Delay Proxy (ms) | Loss Rate | Utility | Rank | Notes |
|----------|--------|-------------------|------------------|-----------|---------|------|-------|
| S2 | NewReno | 9.79 | 129.4 | 0.001363 | 0.923 | 1 | Best overall in S2 |
| S2 | CUBIC | 9.59 | 156.3 | 0.008848 | 0.818 | 2 | |
| S2 | DQN (ours) | 9.79 | 148.8 | 0.055440 | 0.757 | 3 | High loss rate limitation |
| S2 | BBR | 0.39 | 148.7 | 0.015816 | -0.169 | 4 | ns-3.40 TcpBbr anomaly |

*(註：Utility 權重為 provisional：α=1.0, β=0.1, λ=10.0。Delay Proxy 源自 FlowMonitor)*

## Figure Reference Table
| Figure | Path | Source Data | Used For | Caveat |
|--------|------|-------------|----------|--------|
| System Pipeline | `figures/final/system_pipeline.png` | Conceptual | 說明工具鏈 | |
| Single Bottleneck | `figures/final/single_bottleneck_topology.png` | Conceptual | 說明網路拓撲 | |
| MDP Formulation | `figures/final/mdp_formulation.png` | Conceptual | 定義 RL State/Action/Reward | |
| Baseline Utility | `figures/final/baseline_utility_summary.png` | `baseline_summary.csv` | Phase 3 TCP 效能 | |
| DQN vs Baseline Utility | `figures/final/dqn_vs_baseline_utility_s1_s2.png` | `dqn_vs_baseline_summary.csv` | 呈現整體效用比較 | |
| DQN vs Baseline Loss | `figures/final/dqn_vs_baseline_loss_s1_s2.png` | `dqn_vs_baseline_summary.csv` | 凸顯 S2 DQN 高丟包率 | |
| DQN Action Dist. | `figures/final/dqn_action_distribution_s1_s2.png` | `dqn_action_distribution_summary.csv` | S1 degenerate policy 洞察 | |
| DQN Reward Curves | `figures/final/dqn_reward_curves_s1_s2.png` | Log merging | DQN 訓練過程穩定性 | Training reward != performance |
| Key Findings | `figures/final/key_findings_summary.png` | Conceptual | 結論與發現總結 | |

## Limitations Table
| Limitation | Impact | How This Report Handles It |
|------------|--------|----------------------------|
| **Delay Proxy** | 未能直接反映 TCP kernel RTT | 於報告與圖表中明確標示為 "Delay Proxy" (由 FlowMonitor 計算)，不稱其為 true RTT。 |
| **Fallback Option B** | Action 只是 Sender-side 應用層速率控制 | 清楚聲明本 MVP 為 rate abstraction，非 kernel-level TCP control。 |
| **Discrete Action Space** | 動作受限於 +, -, =，控制粒度粗 | 承認這是造成 S2 丟包的部分原因，並將連續動作列入未來工作。 |
| **S1 Degenerate Policy** | DQN 在低延遲只學到單一策略 | 誠實揭露 DQN 發現暴力解，並未過度解讀其「智慧」。 |
| **S2 High Loss** | 代理選擇容忍丟包以追求吞吐量 | 圖表 (`dqn_vs_baseline_loss`) 與內文明確指出 5.54% 的高丟包率，不避諱排名第三。 |
| **Provisional Utility** | 權重 (1, 0.1, 10) 影響總分 | 備註權重之隨機性，不宣稱 DQN 在絕對意義上勝過 TCP。 |
| **BBR S2 Anomaly** | ns-3.40 TcpBbr 表現異常 | 列入表格附註為已知問題，MVP 不受阻礙。 |
| **No Real-World Deployment** | 環境僅在模擬器中運行 | 明確宣告不追求 production-ready。 |

## Future Work and Skipped Phase 6
本專題的下一步自然延伸為：
- 使用 PPO 演算法搭配連續動作空間（Continuous Action Space），以達成更精細的發送速率控制。
- 探索更多樣化、多資料流（Multi-flow）的網路拓撲場景。

**Phase 6 說明**：為了確保最終交付（Phase 5）的品質與專注度，並避免擴充題目帶來的時程風險，Spec Owner 已決定**本期末專題跳過 Phase 6**（不實作 PPO）。因此，PPO 與進階擴展僅列為 Future Work，而非本專題的未完成缺口。

## Conclusion
本專題成功建立了可重現的單一瓶頸鏈路 DRL 擁塞控制 MVP prototype。我們驗證了：
1. DQN 在低延遲（S1）環境下，可發掘出壓榨頻寬極限的暴力策略，表現出不俗的吞吐量與效用（排名第二）。
2. 在高延遲（S2）環境下，因粗粒度的離散動作控制，代理傾向容忍丟包，曝露了 MVP 的限制。
本研究的最終貢獻在於，建構了一套嚴謹可驗證的測試環境（prototype），並示範了基於 OpenSpec 治理的客觀評估（evaluation discipline）與誠實的限制揭露（honest limitations），為未來的連續控制研究奠定了堅實的基礎。
