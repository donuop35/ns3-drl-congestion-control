## Why

在正式開始 DQN MVP（Change 04）之前，必須先將 ns-3 single bottleneck benchmark 環境抽象為一個形式化的 RL environment interface。

若沒有明確的 environment specification：

- DQN agent 的 observation input 沒有規格可遵循，training 結果不可解釋
- Action 的語意不明確，導致 sender-side behavior 無法對應到 network effect
- Reward function 若無先期定義，training 過程中可能誘導錯誤學習目標（如 throughput-only）
- Reset / step 流程若無規格，ns3-gym integration 無法驗收
- 若未先定義 smoke test 標準，DQN training 開始前無法判斷 environment 是否正確運作

本 change 是 Change 02 ns3-baseline-benchmark 與 Change 04 drl-mvp 的橋樑：

- **Change 02** 定義了 baseline metrics（throughput / RTT / loss / utility）與 scenario matrix
- **Change 03（本 change）** 將 baseline simulation 抽象為 MDP interface，繼承 baseline metrics 定義
- **Change 04** 依照本 change 的 observation / action / reward / episode spec 實作 DQN agent

> 🔒 **ns-3 版本凍結（繼承自 Change 02）**: ns-3.40。不得自行升降版本。

**Upstream Reference**: 本 change 依據 Change 01 project-charter 與 Change 02 ns3-baseline-benchmark（均已通過 Spec Owner 驗收）中凍結的 baseline 方法、metrics、topology 邊界與 scenario matrix。

---

## What Changes

本 change 新增以下規格（不含任何實作程式碼）：

- **MDP Interface**: 形式化定義 M = (S, A, P, R, γ)，指定 environment 與 agent 的邊界
- **Environment Boundary**: 明確說明 environment 為 ns-3 single bottleneck simulation 的 RL abstraction
- **Agent Boundary**: 明確說明 agent 只控制 sender-side transmission behavior abstraction
- **Observation Space**: 定義 MVP minimal observation（5 欄位）與 enhanced observation（future extension）
- **Action Space**: 固定 MVP discrete action A = {decrease, keep, increase}
- **Reward Function**: 定義 r_t = α·throughput_norm − β·delay_norm − λ·loss_norm（權重 provisional）
- **Episode / Horizon**: 定義 episode 的 reset / step / terminated / truncated 概念流程
- **Info Dictionary**: 定義 step 回傳的 info dict，包含 baseline-compatible metrics
- **Random Agent Smoke Test**: 定義 smoke test criteria（不執行，只定義規格）
- **Downstream Dependency**: 明確約束 Change 04 必須遵循本 change 的所有 interface 定義
- **Environment Risk Register**: 列出 13 個環境實作風險及 fallback

---

## What Does Not Change

本 change 嚴格禁止以下事項：

> ⛔ **不寫 C++ code** — ns-3 topology 實作留到 Phase 3  
> ⛔ **不寫 Python code** — ns3-gym wrapper 實作留到 Phase 3  
> ⛔ **不執行 ns-3** — 執行留到 Phase 3  
> ⛔ **不啟動 ns3-gym** — 啟動留到 Phase 3  
> ⛔ **不執行 smoke test** — 只定義規格，不執行  
> ⛔ **不訓練 DQN** — 訓練留到 Change 04 / Phase 3  
> ⛔ **不導入 PPO** — PPO 為 future extension，本 MVP 不引入  
> ⛔ **不接 IPFS / QUIC / kernel TCP** — 不在專題 scope 內  
> ⛔ **不做 multi-agent / multi-path** — 不在 MVP scope 內  
> ⛔ **不宣稱 environment 或 training 結果** — 本 change 只建立規格

---

## Capabilities

### New Capabilities

- `mdp-interface`: MDP 形式化定義，確立 environment 與 agent 之間的合約
- `observation-space`: MVP observation 5 欄位規格，含 normalization rules 與 fallback
- `action-space`: Discrete action A = {0: decrease, 1: keep, 2: increase} 規格
- `reward-function`: Multi-objective reward concept（throughput / delay / loss），權重 provisional
- `episode-step-reset`: Reset / step / terminated / truncated / info dict 概念流程
- `smoke-test`: Random agent smoke test 規格（不執行）

### Modified Capabilities

- **Inherits from Change 02**: throughput / RTT / loss / utility metrics 定義；scenario matrix S1/S2；ns-3.40 版本凍結

---

## Impact

本 change 建立的 interface specification 將直接約束：

- **Change 04 (drl-mvp)**: DQN observation input、action output、reward signal、episode logic 均必須符合本 change 規格
- **DQN implementation**: observation shape、action mapping、reward computation 均以本 change 為 source of truth
- **Smoke test before training**: 任何 DQN training 開始前必須先通過本 change 定義的 smoke test criteria
- **Baseline-compatible evaluation**: info dict 中的 metrics 必須與 Change 02 baseline 結果可對比

---

## Dependencies

- ✅ Change 01 project-charter（已通過 Spec Owner 驗收）
- ✅ Change 02 ns3-baseline-benchmark（已通過 Spec Owner 驗收，ns-3.40 凍結）
- 本 change 繼承 Change 02 的 scenario matrix（S1/S2）、metrics（throughput/RTT/loss/utility）、ns-3.40 版本凍結

---

## Acceptance Criteria

- [ ] MDP interface M = (S, A, P, R, γ) 已定義
- [ ] Environment boundary 已明確（ns-3 single bottleneck abstraction）
- [ ] Agent boundary 已明確（sender-side only，不直接控制 kernel TCP）
- [ ] Observation space 已定義（MVP: 5 欄位；enhanced: future extension）
- [ ] Action space 為 discrete（A = {decrease, keep, increase}）
- [ ] Reward function 包含 throughput / delay / loss（multi-objective）
- [ ] Reward 權重明確標為 provisional（不在本 change 固定）
- [ ] Reset / step 概念流程已定義
- [ ] Terminated / truncated 概念已定義
- [ ] Info dictionary 欄位已定義（含 baseline-compatible metrics）
- [ ] Random agent smoke test criteria 已定義（未執行）
- [ ] Downstream dependency to Change 04 明確（observation / action / reward / episode spec）
- [ ] PPO 未被導入為 MVP
- [ ] IPFS / QUIC / multi-agent / multi-path 未被引入
- [ ] 不含任何 C++ / Python / shell 程式碼
- [ ] 不含任何 training 結果或 experiment result 宣稱
- [ ] Spec Owner 驗收通過，才啟動 Change 04
