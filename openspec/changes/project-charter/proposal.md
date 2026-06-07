## Why

本期末專題須在學期末前完成一套可重現、可驗收、可展示的深度強化學習 (DRL) 研究 pipeline，主題為「以 DRL 進行單一瓶頸鏈路壅塞控制與吞吐量最佳化」。目前專案尚缺乏凍結的研究方向文件、明確的 MVP 邊界、以及可供整學期遵循的工具鏈與驗收標準，需要在正式實作開始前先建立 project charter 作為唯一真相文件。

## What Changes

- 建立 `openspec/changes/project-charter/` 作為研究方向凍結的正式 OpenSpec change
- 凍結研究題目、研究目標、MDP 定義初版、工具鏈選擇、實驗情境
- 明確列出 MVP 必做清單與 Non-goals（不得在未經 Spec Owner 同意下納入的項目）
- 定義五個後續 OpenSpec changes 的順序與啟動條件
- 建立 Risk Register 初版
- 建立 Acceptance Criteria，作為整學期期末驗收依據

## Capabilities

### New Capabilities

- `project-charter`: 凍結本期末專案的研究方向、MVP 邊界、工具鏈、MDP 初版定義、實驗情境、Metrics、Risk Register 與 Acceptance Criteria；作為後續所有 OpenSpec changes 的基礎契約文件

### Modified Capabilities

<!-- 目前 openspec/specs/ 尚無既有 spec，無 modified capabilities -->

## Impact

- 影響後續所有 OpenSpec changes（02–05）的啟動條件與驗收標準
- 明確界定 ns-3、ns3-gym、Stable-Baselines3、DQN 為本學期核心工具鏈，其他工具需 Spec Owner 核准才能引入
- 明確排除 IPFS、QUIC、multi-agent RL、Linux kernel TCP、large-scale topology 等非 MVP 範疇
- 確立 Change 01 完成後才可啟動 Change 02（ns3-baseline-benchmark）
