## Purpose

定義本專案的 MDP（Markov Decision Process）/ RL environment interface。
此檔案是 Change 03 opengym-env 的核心規格，Change 04 drl-mvp 必須完整遵循此規格建立 DQN agent。

---

## MDP Definition

本專案的 RL 問題形式化為：

**M = (S, A, P, R, γ)**

| 符號 | 名稱 | 說明 |
|------|------|------|
| **S** | State space（Observation space）| Agent 在每個 decision step 可觀測的 network signal 向量；詳見 `observation-space.md` |
| **A** | Action space | Discrete action set A = {0: decrease, 1: keep, 2: increase}；詳見 `action-space.md` |
| **P** | Transition dynamics | P(s_{t+1} \| s_t, a_t)：由 ns-3.40 simulation 決定，agent 無法直接控制；詳見下方 |
| **R** | Reward function | r_t = α·throughput_norm_t − β·delay_norm_t − λ·loss_norm_t（provisional weights）；詳見 `reward-function.md` |
| **γ** | Discount factor | 建議初始值 γ = 0.99；Change 04 可在 Spec Owner approval 下調整 |

---

## Environment Boundary

- **環境定義**: Environment 是 **ns-3.40 single bottleneck simulation 的 RL abstraction**
- **環境由 ns3-gym 橋接**: OpenGym / ns3-gym 負責連接 ns-3 simulation 與 Python RL agent
- **Agent 觀測範圍**: 僅限 sender 可感知的 network signal（throughput、delay、loss）；不直接觀測網路內部狀態（queue 長度等）
- **Network dynamics**: 所有 queuing、delay、congestion 行為由 ns-3.40 simulation 內部決定

```
ns-3 Simulation (ns-3.40)
  └── OpenGym socket bridge (ns3-gym)
        ├── observation ──→ RL agent (DQN)
        ├── ←── action ─── RL agent
        └── reward / done / info ──→ RL agent
```

---

## Agent Boundary

- **Agent 角色**: Agent 是 sender-side transmission behavior controller
- **Agent 可控制**: sender-side transmission intensity（透過 discrete action 間接影響）
- **Agent 不可控制**: 
  - 整個網路（router, bottleneck link, receiver）
  - kernel-level TCP parameters（不直接修改 TCP stack）
  - ns-3 simulation dynamics（queue, scheduler 等）
- **Abstraction layer**: Action → sender-side control parameter → ns-3 simulation → next state
- **Agent 不直接感知**: Router queue occupancy（MVP；此為 enhanced observation）

---

## Transition Assumption

- **Markovian assumption**: 假設 s_{t+1} 主要由 (s_t, a_t) 決定（近似 MDP；網路有 partial observability，但 MVP 以此近似處理）
- **Transition 由 ns-3 決定**: P(s_{t+1} | s_t, a_t) 無法解析式表示，由 ns-3.40 simulation dynamics 隱式定義
- **Decision interval**: 每個 step 推進固定時間（1–5 秒，具體值在 Change 04 中定義）
- **Action effect**: Action 只間接影響下一個 state（透過 sender-side control → network feedback）

---

## Downstream Constraints（Change 04 必須遵守）

Change 04 drl-mvp 在實作 DQN agent 時：

1. **必須使用本 change 定義的 observation space**（shape [5]，欄位固定順序）
2. **必須使用本 change 定義的 action space**（discrete，|A| = 3）
3. **必須使用本 change 定義的 reward concept**（multi-objective）
4. **必須通過 random agent smoke test**（依 `smoke-test.md` 規格）
5. **不得改變 MDP 的基本結構**（若需要改變，必須另開 OpenSpec change 並獲 Spec Owner 批准）
