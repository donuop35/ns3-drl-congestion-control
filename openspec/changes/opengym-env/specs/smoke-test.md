## Purpose

定義 Change 03 opengym-env 的 random agent smoke test 規格。

Smoke test 的目的是在 DQN training 開始前，驗證 ns3-gym environment 的 reset / step / observation / reward / info flow 是否正確運作。

**本 change 只定義 smoke test 規格，不執行 smoke test。** 實際執行在 Change 04 implementation 階段，作為 training 開始前的強制 gate。

---

## Smoke Test Mission

Smoke test = **Environment Correctness Check**（非 Agent Performance Check）

| 目的 | 說明 |
|------|------|
| **Environment 正確性驗證** | 確保 reset / step API 可正常運作，不 crash，不 hang |
| **Interface 一致性驗證** | 確保 observation shape、action space、info dict 與 spec 一致 |
| **Flow 完整性驗證** | 確保完整 episode（reset → N steps → terminated）可正確執行 |
| **Baseline metric 相容性驗證** | 確保 info dict 中的 raw metrics 與 Change 02 metrics 格式一致 |

---

## Smoke Test Requirements

Smoke test 必須驗證以下所有條件，**全部通過才算 PASS**：

### ST-01：Reset Returns Valid Observation

- **When**: `observation, info = env.reset()` 被呼叫
- **Then**: `observation` 必須是 shape `[5]`（或 `[4]` if `prev_action_norm` excluded）的 numeric array
- **Then**: `observation` 的所有值必須在 [0, 1] 範圍內（或允許微量超出後被 clip）
- **Then**: `info` 必須是 dict，且包含 `scenario_id` 欄位

### ST-02：Random Discrete Action Accepted

- **When**: `action = random.randint(0, 2)` 被採樣並傳入 `env.step(action)`
- **Then**: 不得 raise `ValueError` 或任何 action validation error
- **Then**: Environment 必須正確處理 {0, 1, 2} 的任意組合

### ST-03：Step Returns Valid Next Observation

- **When**: `env.step(action)` 被呼叫
- **Then**: 返回的 `next_observation` 必須是同形狀的 numeric array
- **Then**: 所有值仍在 [0, 1] 範圍內（或被 clip）

### ST-04：Reward is Finite Number

- **When**: `env.step(action)` 被呼叫
- **Then**: `reward` 必須是有限 float（`math.isfinite(reward)` == True）
- **Then**: `reward` 不得為 `NaN`、`Inf` 或 `-Inf`

### ST-05：Terminated / Truncated Defined

- **When**: Episode 執行至結束
- **Then**: `terminated` 或 `truncated` 必須在某個 step 為 `True`
- **Then**: `terminated` 和 `truncated` 不可同時為 `True`

### ST-06：Info Contains Required Fields

- **When**: `env.step(action)` 被呼叫
- **Then**: 返回的 `info` dict 必須包含以下所有欄位：
  - `raw_throughput_mbps`
  - `raw_delay_ms`
  - `raw_loss_rate`
  - `utility_score`
  - `scenario_id`
  - `step_index`
  - `action_applied`
  - `action_symbol`

### ST-07：No Crash for Fixed Number of Steps

- **When**: Random agent 執行 N steps（N 建議 = episode 的完整長度，或至少 10 steps）
- **Then**: Environment 不得 crash、hang 或 raise unhandled exception
- **Then**: ns-3 simulation process 不得意外退出

### ST-08：Log Format Compatible with Change 02 Metrics

- **When**: Smoke test 完成後，解析所有 step 的 `info` dict
- **Then**: `raw_throughput_mbps`、`raw_delay_ms`、`raw_loss_rate` 的單位與 Change 02 baseline CSV 相同（Mbps, ms, fraction [0,1]）
- **Then**: 可以用相同的 plotting script 畫出 DRL 與 baseline 的對比圖（conceptually）

### ST-09：Observation Feature Order Documented

- **When**: Smoke test 完成後
- **Then**: Observation index 0–4 對應的欄位必須有明確文件記錄（在 Change 04 implementation notes 中）

### ST-10：Action Applied Recorded

- **When**: 每個 `env.step(action)` 被呼叫
- **Then**: `info["action_applied"]` 必須等於傳入的 `action` 值
- **Then**: `info["action_symbol"]` 必須對應正確的 symbol（"decrease" / "keep" / "increase"）

---

## Smoke Test Non-Goals

Smoke test 明確**不驗證**以下事項：

> ⛔ **Agent performance** — Smoke test 使用 random agent，不評估策略品質  
> ⛔ **Reward improvement** — 不要求 cumulative reward 上升  
> ⛔ **Baseline outperformance** — Smoke test 不需要 DRL 比 NewReno / CUBIC 好  
> ⛔ **Final figures** — Smoke test 不產生論文品質的圖表  
> ⛔ **DQN training** — Smoke test 完全不涉及 DQN weight update  
> ⛔ **PPO** — Smoke test 不涉及任何 policy gradient  
> ⛔ **Long-run convergence** — 不需要評估 agent 是否收斂

---

## Smoke Test Acceptance Criteria（規格層級）

以下條件全部滿足，才代表 Change 03 smoke test **規格已就緒**（實際執行在 Change 04）：

- [ ] ST-01 ~ ST-10 的 WHEN / THEN 均已在本規格中明確定義
- [ ] Smoke test 的 non-goals 已明確記錄（不會被誤解為 performance test）
- [ ] Smoke test PASS 是 DQN training 開始前的強制 gate（已記錄在 Change 04 tasks.md 中）
- [ ] Smoke test 使用的 random agent 不包含任何 learned policy
- [ ] Smoke test 的結果（pass / fail）必須回報 Spec Owner（若 fail，必須停止並修復 environment）

---

## Smoke Test Flow（概念）

```
env = DrlCongestionControlEnv(scenario="scenario_a", seed=42)

obs, info = env.reset()
assert obs.shape == (5,)
assert all(0 <= x <= 1 for x in obs)

for step in range(N):
    action = random.randint(0, 2)
    obs, reward, terminated, truncated, info = env.step(action)

    assert obs.shape == (5,)
    assert math.isfinite(reward)
    assert "raw_throughput_mbps" in info
    assert "action_applied" in info
    assert info["action_applied"] == action

    if terminated or truncated:
        break

print("Smoke test PASSED")
```

> **Note**: 以上為概念性 pseudo-code，不含實際 ns3-gym / Python 實作。
