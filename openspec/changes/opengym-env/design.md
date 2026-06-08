## Context

本 change 承接 Change 01 project-charter 與 Change 02 ns3-baseline-benchmark 的凍結規格：

- **Simulator**: ns-3.40（Spec Owner 正式凍結，OQ-02.01, 2026-06-08）
- **Baselines**: NewReno（required）、CUBIC（required）、BBR（strongly preferred, non-blocking）
- **Metrics**: throughput、RTT、packet loss rate、utility score（provisional）
- **Topology**: single bottleneck path（sender → router → receiver）
- **Scenarios**: S1（低延遲）、S2（高延遲）

本 change 的目標是將 Change 02 定義的 ns-3 simulation 抽象為可供 DQN 使用的 RL environment interface。

---

## Design Goal

1. 將 single bottleneck ns-3 simulation 抽象為形式化 RL environment（MDP）
2. 讓 DQN MVP 有穩定且可驗收的上游 interface 定義
3. 讓 Change 02 的 baseline metrics 能被 environment reward 與 evaluation 繼承
4. 確保 smoke test 在 DQN training 前可驗收 environment 正確性

---

## Environment Boundary

```
┌─────────────────────────────────────────────────────────┐
│                   ns-3 Simulation World                  │
│                                                         │
│  Sender ──[Access]──> Router ──[Bottleneck]──> Receiver │
│                        │                               │
│              (FlowMonitor / TracedValue)                │
│                        │                               │
│          ┌─────────────▼──────────────┐                │
│          │     OpenGym Environment    │                │
│          │   (ns3-gym bridge layer)   │                │
│          └─────────────┬──────────────┘                │
└────────────────────────│────────────────────────────────┘
                         │ observation / reward / info
                    ┌────▼────┐
                    │  Agent  │
                    │ (DQN)   │
                    └─────────┘
```

- Environment = single bottleneck ns-3 simulation 的 RL abstraction
- **Agent 不控制整個網路**；只控制 sender-side transmission behavior abstraction
- Network dynamics（queue, delay, loss）由 ns-3 simulation 決定
- Environment 不直接修改 kernel-level TCP

---

## MDP Interface

**M = (S, A, P, R, γ)**

| 符號 | 說明 |
|------|------|
| **S** | State / observation space：由 sender 可觀測的 network signal 組成（throughput, delay, loss, congestion indicator, previous action） |
| **A** | Action space：discrete set A = {0: decrease, 1: keep, 2: increase}，對應 sender-side transmission control abstraction |
| **P** | Transition dynamics P(s_{t+1} \| s_t, a_t)：由 ns-3 simulation 決定，agent 無法直接控制 |
| **R** | Reward function：r_t = α·throughput_norm − β·delay_norm − λ·loss_norm（α, β, λ provisional） |
| **γ** | Discount factor：建議初始值 γ = 0.99；Change 04 可調整 |

---

## Decisions

### D-03-01：Define Environment Before DQN

**Decision**: Change 03 必須在 Change 04 開始前完成 Spec Owner 驗收。  
**Rationale**: 若 DQN 在 environment interface 未固定前開始，observation shape、action mapping、reward signal 可能在 training 中途更改，導致 training 不可重現。  
**Rule**: Change 04 implementation 必須 depend on Change 03 specification。不得在本 change 中撰寫任何 DQN 程式碼。

### D-03-02：Minimal Observation for MVP

**Decision**: MVP observation 固定為 5 個欄位：`[throughput_norm, delay_norm, loss_norm, congestion_indicator, prev_action_norm]`。  
**Rationale**: 最小 observation 降低 training complexity，確保 MVP 可收斂；enhanced observation（queue occupancy、delay gradient 等）留為 future extension。  
**Fallback**: 若 RTT 不可直接取得，使用 `delaySum/rxPackets`（delay estimate），並在 info dict 中標記。

### D-03-03：Discrete Action for MVP

**Decision**: Action space 固定為 A = {0: decrease, 1: keep, 2: increase}（|A| = 3）。  
**Rationale**: Discrete action 簡化 DQN 實作，避免 policy gradient 複雜度；continuous action 與 PPO 留為 future extension。  
**Rule**: Change 04 不得自行改為 continuous action 或 PPO，除非另開 OpenSpec change 並獲 Spec Owner 批准。

### D-03-04：Multi-Objective Reward

**Decision**: Reward 必須包含 throughput、delay、loss 三個 component。  
**Rationale**: Throughput-only reward 會誘導 agent 忽略 RTT 與 loss，不符合壅塞控制語意；utility score 在 Change 02 已定義為 provisional，此處繼承其哲學。  
**Weight status**: α, β, λ 在本 change 不固定；Change 04 定義初始值，Change 05 可調整。

### D-03-05：Smoke Test Before Training

**Decision**: 在 DQN training 開始前，必須先通過 random agent smoke test。  
**Rationale**: Smoke test 驗證 environment 的 reset / step / observation / reward / info flow 是否正確，避免 training 在 broken environment 上浪費資源。  
**Rule**: Smoke test 只驗證 environment correctness，不驗證 agent performance。

### D-03-06：PPO as Future Extension Only

**Decision**: PPO 不得在 Change 03 或 Change 04 中引入。  
**Rationale**: PPO 需要 continuous action 或特殊 policy 設計，超出 DQN MVP scope；若未來需要引入 PPO，必須另開 OpenSpec change。  
**Rule**: Change 04 的 MVP agent 必須是 DQN（或 Double DQN / Dueling DQN），不得改用 PPO。

### D-03-07：Official OpenSpec Workflow Only

**Decision**: 本 change 的所有 artifacts 必須在官方 `@fission-ai/openspec` CLI 產生的 `openspec/changes/opengym-env/` 目錄下建立。  
**Rule**: 不得自行模擬 OpenSpec workflow；不得在非官方 OpenSpec 結構下建立替代目錄。

---

## Observation Design

### MVP Minimal Observation（5 欄位，固定順序）

| Index | 欄位名稱 | 語意 | 來源 | Normalization | MVP status |
|-------|---------|------|------|---------------|-----------|
| 0 | `throughput_norm` | 當前 step 的 goodput（歸一化）| FlowMonitor rxBytes / step duration | 除以 link bandwidth 上限 | **Required** |
| 1 | `delay_norm` | 當前 step 的 average delay / RTT（歸一化）| FlowMonitor delaySum / rxPackets | 除以 max expected delay | **Required** |
| 2 | `loss_norm` | 當前 step 的 packet loss rate | (txPackets - rxPackets) / txPackets | [0, 1] 自然有界 | **Required** |
| 3 | `congestion_indicator` | 壅塞程度指示（loss / delay composite 或 binary）| 由 loss_norm 與 delay_norm 推導 | [0, 1] | **Required** |
| 4 | `prev_action_norm` | 上一步 action 的歸一化編碼 | Agent 自身記錄 | {0→0.0, 1→0.5, 2→1.0} | **Should-have** |

> **Fallback**: 若 `prev_action_norm` 在 ns3-gym interface 實作上有困難，可在 smoke test 中確認後再決定是否保留。

### Enhanced Observation（Future Extension Only）

| 欄位 | 語意 | 狀態 |
|------|------|------|
| `queue_occupancy` | 瓶頸佇列使用率 | Future extension |
| `delay_gradient` | delay 對時間的一階導數 | Future extension |
| `throughput_ma` | Throughput 移動平均 | Future extension |
| `estimated_bw` | 估計瓶頸頻寬 | Future extension |
| `cross_traffic_indicator` | Background traffic 強度 | Future extension |
| `ack_interarrival` | ACK 到達間隔 | Future extension |

> ⛔ Enhanced observation 不得阻塞 MVP。

---

## Action Design

**MVP Action Set**: A = {0, 1, 2}（|A| = 3）

| Action ID | Symbol | 語意 | 對 sender 的效果 |
|-----------|--------|------|-----------------|
| 0 | `decrease` | 降低 sender-side transmission intensity | 減少 sending rate 或 cwnd-like variable |
| 1 | `keep` | 維持目前控制強度 | 不改變 transmission parameter |
| 2 | `increase` | 提高 sender-side transmission intensity | 增加 sending rate 或 cwnd-like variable |

**Action Safety Rules**:
- 不允許 sender-side rate / cwnd-like variable 降至負值
- Action effect 的幅度有界（步長在 Change 04 implementation 中定義）
- 每個 action 必須在 info dict 中記錄
- 不直接修改 kernel-level TCP
- 維持 abstraction layer（action → sender control → ns-3 effect）

---

## Reward Design

**Base reward concept**:

```
r_t = α · throughput_norm_t − β · delay_norm_t − λ · loss_norm_t
```

| 符號 | 說明 | 數值 |
|------|------|------|
| `throughput_norm_t` | 當前 step goodput / link BW 上限 | [0, 1] |
| `delay_norm_t` | 當前 step avg delay / max expected delay | [0, 1] |
| `loss_norm_t` | 當前 step packet loss rate | [0, 1] |
| `α` | Throughput 正向權重 | **provisional**（初始值由 Change 04 定義） |
| `β` | Delay 懲罰權重 | **provisional** |
| `λ` | Loss 懲罰權重（用 λ 而非 γ，避免與 discount factor 混淆）| **provisional** |

> ⚠️ **Reward weights are provisional**：α, β, λ 在本 change 不固定；Change 04 定義初始值；Change 05 可依 Spec Owner approval 調整。

---

## Episode / Horizon

| 概念 | 說明 |
|------|------|
| **Decision interval** | 每個 step 對應一個固定時間窗口的 ns-3 simulation（e.g., 1–5 秒，具體值在 Change 04 中定義） |
| **Episode length** | 對應一個完整的 scenario duration（e.g., 60 秒 → ~12–60 steps，依 decision interval 而定）|
| **Terminated** | Episode 自然結束（simulation duration 達到）|
| **Truncated** | Time limit 達到但 episode 未自然結束，或 environment fatal error |
| **Max steps per episode** | 在 Change 04 中依 scenario config 確定 |

---

## Downstream Usage

Change 04（drl-mvp）**必須遵循**本 change 的所有規格：

| 項目 | Change 03 定義 | Change 04 必須遵守 |
|------|--------------|-----------------|
| Observation shape | `[5]`（MVP minimal）| 不得自行更改 shape |
| Observation fields | 5 個欄位，固定順序 | 必須按本 change 的 index mapping |
| Action space | Discrete, `|A| = 3` | 不得改為 continuous |
| Reward | Multi-objective（throughput/delay/loss）| 不得改為 throughput-only |
| Episode flow | reset / step / terminated / truncated / info | 必須實作完整流程 |
| Smoke test | Random agent smoke test before training | 必須先通過 |
| Info dict | 含 baseline-compatible metrics | 不得省略 |

Change 04 不得自行：
- 改為 PPO MVP
- 引入 continuous action 而不另開 change
- 使用 throughput-only reward
- 加入 IPFS / QUIC / multi-agent / multi-path

---

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| Observation 無法從 ns-3 直接取得 | 預先研究 FlowMonitor / TracedValue API；定義 fallback rule（見 observation-space.md）|
| RTT trace 不易取得 | 使用 `delaySum/rxPackets` 作為 delay estimate；在 info dict 中標記 |
| Action effect 難以映射到 sender-side control | 在 Change 04 implementation 中明確定義 step size；此處只定義 abstraction |
| Reward scale 不穩 | Reward normalization 是必要條件；Change 04 需要調整初始 weight |
| Smoke test 無法通過 | 若 smoke test 失敗，必須停止並回報 Spec Owner，不得繼續 DQN training |

---

## Open Questions

| # | 問題 | 狀態 |
|---|------|------|
| OQ-03.01 | Decision interval 的具體長度（e.g., 1s, 2s, 5s per step）| ⏳ Change 04 implementation 開始時定義 |
| OQ-03.02 | α, β, λ 的初始數值 | ⏳ Change 04 中定義初始值；Change 05 可調整 |
| OQ-03.03 | `prev_action_norm` 在 ns3-gym interface 是否可取得 | ⏳ Smoke test 中確認；若不可得，降為 should-have |
| OQ-03.04 | Max steps per episode（依 scenario duration / decision interval）| ⏳ Change 04 中依 scenario config 確定 |
