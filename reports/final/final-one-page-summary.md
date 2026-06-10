# 一頁式期末專題摘要

## 研究問題

傳統 TCP 擁塞控制（NewReno, CUBIC, BBR）依賴人工設計的規則，在不同的網路條件下難以同時最佳化吞吐量、延遲與丟包。本研究探討：在單一瓶頸鏈路上，以深度強化學習（DRL）訓練的 Agent 能否學習到有效的擁塞控制策略？

## 方法

將單一瓶頸鏈路的擁塞控制建模為 Markov Decision Process（MDP）。觀測空間包含吞吐量、延遲代理（delay proxy）、丟包率、擁塞信號與前一動作，共 5 維。動作空間為離散 3 選項：降低（↓）、維持（=）、提高（↑）發送速率。獎勵函數為 R = αT − βD − λL（α=1.0, β=0.1, λ=10.0，provisional）。

## 工具鏈

- 網路模擬器：ns-3.40
- RL 介面：ns3-gym（ZMQ 通訊）
- RL 框架：Stable-Baselines3 DQN
- 規格治理：OpenSpec v1.4.1

## Baseline（Phase 3）

在 S1（低延遲 10ms）與 S2（高延遲 50ms）兩個場景下，完成了 NewReno、CUBIC、BBR 的效能基準測試。

## DQN MVP（Phase 4）

以 Seed 42 訓練 30,000 steps，完成 S1/S2 兩場景的 DQN Agent 訓練與評估。

## 核心結果

### S1（低延遲）

DQN Utility **0.900**，排名第 2。低於 BBR（0.947），高於 CUBIC（0.884）與 NewReno（0.875）。DQN 採取 100% Increase 退化策略，在低延遲環境中壓榨頻寬極限。

### S2（高延遲）

DQN Utility **0.757**，排名第 3。低於 NewReno（0.923）與 CUBIC（0.818）。DQN 丟包率高達 **5.54%**，暴露了粗粒度離散動作在高延遲環境下的限制。

## 貢獻

1. 建立了受 OpenSpec 治理的可重現 DRL 擁塞控制 MVP 測試平台。
2. 完成了 ns-3 單一瓶頸鏈路的 TCP baseline benchmark。
3. 誠實報告 DQN 的潛力（S1 排名第 2）與限制（S2 高丟包）。

## 限制

- Delay 為 FlowMonitor Proxy，非 true TCP RTT。
- Action 為 Sender-side Rate Abstraction，非 kernel-level TCP control。
- Utility 權重為 provisional。
- DQN 未全面勝過 TCP baselines。

## 結語

本 MVP 驗證了 DRL 在單一瓶頸鏈路擁塞控制的可行性，並為未來連續動作空間（PPO）研究奠定了基礎。
