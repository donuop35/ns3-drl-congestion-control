# Change 01: Project Charter

## Why

本專案需要一份正式的 project charter 作為整學期的 **single source of truth**（唯一真相來源）。

若沒有 project charter：

- 研究方向需求散落在聊天紀錄，無法追蹤
- Antigravity 實作可能自行偏離成 IPFS、QUIC、multi-agent 等非 MVP 範疇
- 後續 OpenSpec changes 無法有明確的上游規格作為依據
- 容易在沒有完成 baseline 的情況下直接跳去做 DQN
- 期末驗收時無法確認「做了什麼、沒做什麼、為什麼這樣設計」

本 project charter 的存在，是為了讓整個學期的研究工作可以：

- 按照明確的 scope 推進，不跑偏
- 讓每一個後續 OpenSpec change 都有一個明確的上游依據
- 確保 Antigravity 只在被允許的範疇內執行任務
- 讓 spec owner 在任何時間點都能驗收當前進度

## What Changes

本 change 新增以下內容（僅限文件，不含任何程式實作）：

- **project title**（中文、英文、GitHub 簡版），正式凍結
- **project mission**（本專題使命說明）
- **project background**（研究背景，包含 TCP 壅塞控制歷史與 DRL 動機）
- **problem statement**（為何現有 TCP 演算法有改善空間）
- **proposed direction**（以 DRL 解決 congestion control 問題的核心策略）
- **scope**（本學期 MVP 必做清單）
- **non-scope**（明確不做的項目）
- **strict non-goals**（完全禁止的研究方向）
- **baseline freeze**（NewReno、CUBIC、BBR 固定）
- **metrics freeze**（throughput、RTT、loss、utility、reward curve）
- **MVP definition**（DQN first，PPO as future extension）
- **downstream change map**（change-02、03、04 的啟動條件與依賴）
- **risk register**（主要風險項目與降階方案）

## What Does Not Change

本 change **不包含**且**不允許**的任何事項：

- ❌ 不寫任何程式碼（Python、C++、shell script）
- ❌ 不建立 ns-3 simulation 或 topology
- ❌ 不安裝或使用 ns3-gym 作為實作步驟
- ❌ 不訓練任何 DRL agent（DQN、PPO）
- ❌ 不執行任何 baseline benchmark
- ❌ 不實作 IPFS
- ❌ 不實作 QUIC
- ❌ 不修改 Linux kernel TCP stack
- ❌ 不引入 multi-agent RL
- ❌ 不引入 multi-path routing
- ❌ 不宣稱已有實驗結果
- ❌ 不更改凍結後的研究題目

## Impact

本 change 對後續所有 OpenSpec changes 具有直接上游影響：

| 下游 Change | 依賴本 charter 的內容 |
|-------------|----------------------|
| **change-02-baseline-benchmark** | baseline 選擇（NewReno/CUBIC/BBR）、metrics 定義（throughput/RTT/loss/utility）、topology 邊界（single bottleneck）、scenario 設定 |
| **change-03-ns3gym-environment** | MDP 定義（state/action/reward/episode）、RL interface 選擇（ns3-gym）、observation space 邊界 |
| **change-04-dqn-mvp-agent** | MVP 演算法選擇（DQN first）、evaluation philosophy（honest comparison，不偽造結果）、success definition |

在本 charter 未經 spec owner 確認前，任何下游 change 均不得啟動。

## Dependencies

本 change 依賴以下前置工作（已完成或確認）：

- ✅ Phase 0 final topic decision（題目已凍結）
- ✅ Phase 1 proposal formulation（proposal 簡報已完成）
- ✅ Official OpenSpec v1.4.1 installed（`npm install -g @fission-ai/openspec@latest`）
- ✅ OpenSpec Antigravity integration updated（`openspec update --force`）
- 📖 ns-3 TCP model documentation（待 change-02 引用）
- 📖 ns3-gym official documentation（待 change-03 引用）
- 📖 Stable-Baselines3 DQN docs（待 change-04 引用）
- 📖 Aurora / Pantheon related work（已納入 docs/related_work.md）

## Acceptance Criteria

spec owner 驗收本 change 的條件（全部需完成）：

- [ ] 官方 OpenSpec v1.4.1 已安裝並驗證（`openspec --version` = 1.4.1）
- [ ] `.agent/skills/openspec-*/SKILL.md` 存在（官方 Antigravity integration）
- [ ] `.agent/workflows/opsx-*.md` 存在（官方 workflow 檔案）
- [ ] `openspec status --change "project-charter"` 顯示 `4/4 artifacts complete`
- [ ] 研究題目（中文、英文、GitHub 版）明確凍結在本 charter 中
- [ ] Scope（In / Out / Non-goals）邊界清楚定義
- [ ] Baseline（NewReno、CUBIC、BBR）正式凍結
- [ ] Metrics（throughput、RTT、loss、utility、reward curve）正式凍結
- [ ] MVP（DQN first，PPO as future extension）正式凍結
- [ ] MDP 初版定義（state、action、reward、episode）已記錄
- [ ] Risk register 涵蓋至少 12 個主要風險項目
- [ ] Downstream change map 清楚說明 change-02/03/04 的依賴
- [ ] 本 change 不包含任何程式碼、ns-3 實驗、ns3-gym 環境、DQN 訓練
- [ ] spec owner 簽核：「已確認方向，同意進入 change-02」
