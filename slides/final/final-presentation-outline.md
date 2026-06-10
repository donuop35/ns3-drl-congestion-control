# Final Presentation Outline

**總投影片數:** 12 頁
**預計時間:** 10 分鐘

## Slide 1: Title
- **Main Message:** Deep Reinforcement Learning for Congestion Control over a Single Bottleneck Link.
- **Key Bullets:** 
  - 探討 DRL 應用於單一瓶頸鏈路擁塞控制之可行性。
  - MVP 實作與 Baseline 比較。
- **Suggested Visual:** `figures/final/single_bottleneck_topology.png`
- **Data Source:** N/A
- **Speaker Note Summary:** 大家好，今天我要報告的專題是...
- **Forbidden Wording:** "production-ready TCP", "universal solution".

## Slide 2: Motivation
- **Main Message:** 傳統 TCP 使用人工啟發式規則，DRL 提供潛在的自適應平衡方案。
- **Key Bullets:**
  - 傳統 TCP 難以完美平衡 Throughput, Delay, 與 Loss。
  - DRL 具備從經驗中自動學習最佳策略的潛力。
- **Suggested Visual:** 無（文字為主）
- **Data Source:** N/A
- **Speaker Note Summary:** 為什麼我們要做這個題目？傳統 TCP...

## Slide 3: Research Question & Scope
- **Main Message:** 範圍限制在單一瓶頸鏈路與 DQN MVP，並與 NewReno, CUBIC, BBR 進行比較。
- **Key Bullets:**
  - Scope: Single bottleneck link.
  - Agent: DQN (Discrete Action Space).
  - Baseline: NewReno, CUBIC, BBR.
- **Suggested Visual:** 無
- **Data Source:** N/A
- **Speaker Note Summary:** 本研究的範圍非常明確，我們不做多路徑也不做 IPFS...
- **Forbidden Wording:** IPFS, QUIC, multi-agent, multi-path.

## Slide 4: System Architecture
- **Main Message:** 結合 ns-3.40, ns3-gym, 與 Stable-Baselines3 的工具鏈。
- **Key Bullets:**
  - Environment: ns-3.40.
  - Bridge: ns3-gym (ZMQ).
  - RL Algorithm: SB3 DQN.
- **Suggested Visual:** `figures/final/system_pipeline.png`
- **Data Source:** N/A
- **Speaker Note Summary:** 我們的系統架構包含三個核心組件...

## Slide 5: MDP Formulation
- **Main Message:** 定義 State, Action, 與 Reward。
- **Key Bullets:**
  - State (5 metrics): Throughput, Delay Proxy, Loss Rate, Cwnd, Rtx.
  - Action (3 discrete): Decrease, Keep, Increase (Fallback Option B).
  - Reward: 結合吞吐量、延遲與丟包。
- **Suggested Visual:** `figures/final/mdp_formulation.png`
- **Data Source:** N/A
- **Speaker Note Summary:** 我們將問題建模為 MDP，特別注意動作是 Sender-side 的抽象化...

## Slide 6: Baseline Benchmark
- **Main Message:** Phase 3 Baseline 確立了 S1 與 S2 的效能基準。
- **Key Bullets:**
  - S1 (10ms): BBR 表現最佳。
  - S2 (50ms): NewReno 表現較佳，BBR 出現異常。
- **Suggested Visual:** `figures/final/baseline_utility_summary.png`
- **Data Source:** `baseline_summary.csv`
- **Speaker Note Summary:** 比較前，我們先看傳統 TCP 的基準線...

## Slide 7: DRL MVP Implementation
- **Main Message:** 成功訓練 DQN 30k steps 且通過 Smoke Test。
- **Key Bullets:**
  - 訓練過程穩定。
  - Training reward is diagnostic, not final performance。
- **Suggested Visual:** `figures/final/dqn_reward_curves_s1_s2.png`
- **Data Source:** `dqn_training logs`
- **Speaker Note Summary:** 這張圖展示了 DQN 訓練過程中的 Reward 變化...

## Slide 8: Main Results — S1
- **Main Message:** 在低延遲環境中，DQN 效用排名第 2，學習到滿載退化策略。
- **Key Bullets:**
  - Utility: 0.900 (2nd place).
  - Policy: 100% Increase (Degenerate near-capacity policy).
- **Suggested Visual:** `figures/final/dqn_vs_baseline_utility_s1_s2.png` (S1)
- **Data Source:** `dqn_vs_baseline_summary.csv`
- **Speaker Note Summary:** 在 S1 低延遲場景下，DQN 表現很好，但主要是找到了簡單的暴力解...
- **Forbidden Wording:** "DQN beats TCP."

## Slide 9: Main Results — S2
- **Main Message:** 在高延遲環境中，DQN 盲目追求吞吐量導致高丟包率。
- **Key Bullets:**
  - Utility: 0.757 (3rd place).
  - Loss Rate: 5.54%.
- **Suggested Visual:** `figures/final/dqn_vs_baseline_loss_s1_s2.png` (S2)
- **Data Source:** `dqn_vs_baseline_summary.csv`
- **Speaker Note Summary:** S2 高延遲場景暴露了目前 MVP 的限制，丟包率顯著偏高...
- **Forbidden Wording:** 隱藏 high loss rate 或 3rd place ranking.

## Slide 10: Findings and Limitations
- **Main Message:** 誠實評估 MVP 的侷限性。
- **Key Bullets:**
  - Delay 只是 Proxy。
  - Action 是 Sender-side abstraction。
  - S2 丟包率偏高。
- **Suggested Visual:** `figures/final/key_findings_summary.png`
- **Data Source:** N/A
- **Speaker Note Summary:** 總結我們的發現與限制，我們沒有直接修改 Kernel...
- **Forbidden Wording:** "True RTT", "kernel-level congestion control."

## Slide 11: Demo / Reproducibility
- **Main Message:** 專案受到 OpenSpec 治理，主要結果可追溯。
- **Key Bullets:**
  - Provide Reproducibility Guide.
  - Figure generation scripts provided.
- **Suggested Visual:** GitHub Repo Screenshot or Logo.
- **Data Source:** N/A
- **Speaker Note Summary:** 如果教授想驗證，只要跑這幾個腳本...

## Slide 12: Conclusion & Future Work
- **Main Message:** 驗證了可行性，未來可朝連續動作空間發展。
- **Key Bullets:**
  - Feasibility proven.
  - Future Work: PPO, Continuous Action Spaces.
  - Phase 6 skipped by Spec Owner; PPO is future work only.
- **Suggested Visual:** 無
- **Data Source:** N/A
- **Speaker Note Summary:** 結論是本 MVP 證明了可行性，未來可以嘗試 PPO...
