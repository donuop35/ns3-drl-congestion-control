# Final Report：DRL-Based Congestion Control over a Bottleneck Link

## Abstract
本專題探討在單一瓶頸鏈路（Single Bottleneck Link）上，應用深度強化學習（Deep Reinforcement Learning, DRL）進行擁塞控制（Congestion Control）之可行性。透過整合 ns-3 網路模擬器與 Stable-Baselines3（SB3）的 DQN 演算法，我們建立了可重現的強化學習擁塞控制測試平台。實驗涵蓋低延遲（S1, 10ms）與高延遲（S2, 50ms）場景，並與傳統 TCP 變體（NewReno, CUBIC, BBR）進行比較。結果顯示，DQN 能在 S1 中學到近乎滿載（near-capacity）的退化策略（degenerate policy），在 utility 上排名第二；但在 S2 中則暴露出高丟包率（5.54%）的限制。本報告忠實呈現 DRL MVP 的潛力與限制。

## 1. Introduction / Motivation
傳統 TCP（如 NewReno, CUBIC）依賴人工設計的啟發式規則（hand-crafted rules）來因應網路擁塞，通常難以在吞吐量（throughput）、延遲（delay）與丟包率（loss）之間達到完美平衡。隨著 DRL 在複雜決策問題上展現潛力，探索 DRL 是否能自動學習出適應性強的擁塞控制策略，成為近年網路研究的熱點。

## 2. Problem Statement
在點對點的單一瓶頸網路中，發送端需決定封包發送速率，以最大化整體網路效用（Utility）。然而，發送端僅能觀察到延遲與丟包，無法得知瓶頸鏈路的真實狀態。本專題旨在驗證：一個基於 DQN 的 agent 是否能從這些受限觀察中，學會超越或持平傳統 TCP 的控制策略。

## 3. Background and Related Concepts
- **Congestion Control (CC):** 控制網路進入流量，避免路由器佇列溢滿。
- **Reinforcement Learning (RL):** 代理（Agent）透過與環境（Environment）互動，根據獎勵（Reward）最佳化長期決策。
- **DQN:** 結合深度神經網路與 Q-Learning 的演算法，適用於離散動作空間。

## 4. System Scope and Non-Goals
本專題為 Minimum Viable Product (MVP)，範圍嚴格限制於：
- **Scope:** 單一瓶頸鏈路（Single Bottleneck Topology），單一發送者對單一接收者。
- **Non-Goals:** 不涉及多代理（multi-agent）、多路徑（multi-path）、真實網際網路部署。不包含 IPFS 或 QUIC 實作。這**不是**一個 production-ready 的 TCP 方案。

## 5. System Design
本專題的工具鏈架構（Toolchain）整合如下：
- **環境（Environment）:** `ns-3.40` 負責網路模擬。
- **通訊橋樑:** `ns3-gym` 透過 ZMQ 提供 OpenAI Gym 介面。
- **代理（Agent）:** `Stable-Baselines3` 提供 DQN 演算法。
（參考：`figures/final/system_pipeline.png`）

## 6. MDP Formulation
我們將擁塞控制問題建模為馬可夫決策過程（MDP）：
- **State (Observation):** 包含吞吐量、Delay Proxy（FlowMonitor delaySum/rxPackets）、丟包率、Cwnd 狀態與重傳次數。
- **Action:** 離散的三個動作：減少（Decrease）、維持（Keep）、增加（Increase）。（註：此為發送端的 rate-control 抽象化，稱為 Fallback Option B，並非直接修改 Linux kernel 的 cwnd）。
- **Reward:** 結合吞吐量、延遲與丟包的組合函數：`Reward = (α * Throughput) - (β * Delay) - (λ * Loss)`。本專題使用的 provisional utility 權重為 α=1.0, β=0.1, λ=10.0。
（參考：`figures/final/mdp_formulation.png`）

## 7. Baseline Benchmark
在 Phase 3，我們建立 Baseline，評估 NewReno、CUBIC 與 BBR 在 S1（10ms）與 S2（50ms）的表現。
- 這些數據來自 `experiments/summaries/baseline_summary.csv`。
（參考：`figures/final/baseline_utility_summary.png`）

## 8. DRL MVP Implementation
Phase 4 中，我們成功將 DQN 與 ns-3 介接，並進行了 30,000 steps 的訓練。
- 透過 Real-ZMQ smoke test 驗證。
- 模型與日誌保存於 `experiments/drl/models/` 與 `logs/`。
（參考：`figures/final/dqn_reward_curves_s1_s2.png`）

## 9. Results

### 9.1 Scenario S1：Low Delay
- **表現:** DQN 達到極高的吞吐量（9.88 Mbps），Provisional Utility 為 0.900，整體排名第 2。
- **比較:** DQN 效用高於 CUBIC（0.884）與 NewReno（0.875），但低於 BBR（0.947）。
- **策略:** 代理學習到了 degenerate policy（100% Increase），在低延遲、近滿載的 benign 環境下，這是一個局部最佳解。

### 9.2 Scenario S2：High Delay
- **表現:** DQN 維持了不錯的吞吐量，但付出了高昂的丟包代價（Loss Rate: 5.54%）。Provisional Utility 為 0.757，整體排名第 3。
- **比較:** DQN 效用低於 NewReno（0.923）與 CUBIC（0.818），僅高於遭遇高延遲異常（anomaly）的 BBR（0.316）。

### 9.3 Summary Across Scenarios
DQN 在簡單場景下能快速壓榨頻寬，但在高延遲場景下，目前 MVP 的離散動作空間與簡單 reward 設計難以應付佇列管理（queue management），導致明顯的丟包懲罰。
（參考：`figures/final/dqn_vs_baseline_utility_s1_s2.png` 及 `figures/final/dqn_action_distribution_s1_s2.png`）

## 10. Discussion
本專題成功驗證了「使用 DRL 進行 ns-3 網路模擬擁塞控制」的基礎可行性（Feasibility）。DQN 在 S1 中發現了發送端的最佳暴力解，這符合我們對 RL 在簡單約束下行為的預期。然而，S2 的高丟包率提醒我們，RL 容易「鑽漏洞」：為了拿到吞吐量獎勵，它選擇容忍丟包懲罰。

## 11. Limitations
必須誠實揭露以下系統限制：
- **Delay Proxy:** 本專題的 Delay 來自 FlowMonitor 統計，是 Proxy 而非 true TCP RTT。
- **Action Abstraction:** 動作為 Fallback Option B（發送端 application-level rate control），並非真實的 kernel-level TCP control。
- **Loss Behavior:** S2 中的高丟包率（5.54%）顯示目前代理缺乏細緻的預測能力。
- **Not Production Ready:** 本專題並未宣稱 DQN beats TCP，這僅為學術原型的 MVP。

## 12. Reproducibility
所有產出皆符合 OpenSpec SDD 規範。
我們提供 `reports/final/final-reproducibility-guide.md`，說明如何使用指令重現從 baseline、smoke test 到 DQN 評估與圖表生成的所有步驟，且所有結果均以 CSV 作為 Source of Truth。

## 13. Conclusion
本專題成功建立了基於 ns-3、ns3-gym 與 SB3 的單一瓶頸鏈路 DRL 擁塞控制測試平台。DQN MVP 在低延遲場景下展現出逼近極限吞吐量的潛力，同時也誠實揭露了其在高延遲下因離散動作與簡單獎勵造成的限制。這為未來導入更進階的演算法（如 PPO）與連續動作空間奠定了堅實基礎。

## 14. Appendix：Artifact Index
請參閱 `reports/final/final-artifact-manifest.md`，其中羅列了本專題所有的程式碼、數據、圖表與文件產出清單。
