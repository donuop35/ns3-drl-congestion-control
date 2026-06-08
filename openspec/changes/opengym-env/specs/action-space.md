## Purpose

定義 Change 03 opengym-env 的 action space 規格，包含 MVP discrete action set、action 語意、action safety rules 與 continuous action 的 future extension 規則。

Change 04 drl-mvp 的 DQN 實作必須使用本規格定義的 discrete action space，不得自行改為 continuous action 或 PPO。

---

## MVP Discrete Action Set

**A = {0, 1, 2}**（|A| = 3）

固定為 **Discrete(3)** action space（相容於 OpenAI Gym / Gymnasium `Discrete` space）。

| Action ID | Symbol | 語意 | 對 sender-side 的概念效果 |
|-----------|--------|------|--------------------------|
| **0** | `decrease` | 降低 sender-side transmission intensity | 減少 sending rate 或 cwnd-like variable（步長在 Change 04 中定義）|
| **1** | `keep` | 維持目前控制強度 | 不改變 transmission parameter；觀察 network 反應 |
| **2** | `increase` | 提高 sender-side transmission intensity | 增加 sending rate 或 cwnd-like variable（步長在 Change 04 中定義）|

> **Note**: Action 的具體映射（e.g., `decrease` 對應 cwnd × 0.5 還是 rate − 1 Mbps）在 Change 04 implementation 中定義。本 change 只定義 abstract 語意。

---

## Action Mapping Abstraction

```
Agent Action (discrete)
     ↓
Sender-side Control Abstraction
     ↓
ns3-gym socket → ns-3 simulation
     ↓
Network Effect (throughput / delay / loss change)
     ↓
Next Observation
```

- Action 影響的是 **sender-side transmission behavior 的抽象參數**
- 實際的 cwnd / sending rate 操作在 ns3-gym implementation 中定義
- Agent 不直接存取或修改 ns-3 內部 TCP 狀態

---

## Action Safety Rules

以下規則在 Change 04 implementation 中必須強制執行：

1. **No negative parameter**: `decrease` action 不得使 sender-side rate 或 cwnd-like variable 降至負值或零以下；必須有下界保護
2. **Bounded action effect**: 每次 action 的效果有固定步長上限；不得允許一次 action 導致 rate 驟升至 link bandwidth 上限
3. **Action effect MUST be logged**: 每個 step 採取的 action 及其對 sender-side parameter 的效果，必須記錄在 info dict 中
4. **No kernel-level TCP modification**: Action 不得直接修改 Linux kernel TCP 參數（e.g., 不得呼叫 `sysctl`）
5. **Maintain abstraction layer**: Action 必須透過 ns3-gym interface 作用，不得繞過 environment abstraction 直接操作 ns-3 C++ 物件

---

## Action Recording Requirements

每個 step 的 info dict 中必須包含：

```python
info = {
    "action_applied": int,           # 實際執行的 action id (0, 1, 2)
    "action_symbol": str,            # "decrease", "keep", "increase"
    "sender_param_before": float,    # action 前的 sender-side parameter
    "sender_param_after": float,     # action 後的 sender-side parameter
    ...
}
```

---

## Continuous Action（Future Extension Only）

> ⛔ **Continuous action 不在 MVP scope 內。**

若未來需要引入 continuous action（e.g., 直接控制 sending rate 為連續值）：

1. 必須另開一個新的 OpenSpec change
2. 必須獲得 Spec Owner 明確批准
3. 引入 continuous action 通常伴隨 PPO / SAC 等 policy gradient 方法，需要重新審視整個 MDP interface
4. **Change 04 不得自行改為 continuous action 而不另開 change**

---

## PPO Exclusion Rule

> ⛔ **PPO 不得在 Change 03 或 Change 04 中引入。**

- PPO 通常用於 continuous action space 或大型 discrete action space，與本 MVP 的 DQN + Discrete(3) 設計不符
- 若 Change 04 過程中認為 PPO 更合適，必須：
  1. 停止 Change 04 implementation
  2. 另開 OpenSpec change（e.g., change-04b-ppo-extension）
  3. 獲得 Spec Owner 批准後才能繼續

---

## Relationship to Baseline Comparison

- DQN agent 的 action 透過 environment 影響 throughput / RTT / loss
- 這些 metrics 需要與 Change 02 baseline（NewReno / CUBIC / BBR）的相同 metrics 可比較
- **Change 04 evaluation 必須在相同 scenario（S1 / S2）下，使用相同 metrics 比較 DQN 與 baseline**
- Action 設計必須讓 agent 在 congestion 時有 decrease 選項，在 underutilization 時有 increase 選項，以便 agent 有機會比 baseline 表現更好
