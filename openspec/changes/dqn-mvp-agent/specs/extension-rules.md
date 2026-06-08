## Purpose

定義 Change 04 dqn-mvp-agent 的 extension governance 規格，確保所有 future extension 不會阻塞 DQN MVP 的完成，並且任何 extension 都需要另開 OpenSpec change 並獲 Spec Owner 批准。

---

## MVP Protection Rules

以下規則適用於所有 extension：

1. **Extension MUST NOT block MVP**: 任何 future extension 不得在未完成 DQN MVP 的情況下開始
2. **Extension MUST have Spec Owner approval**: 任何 extension 必須另開 OpenSpec change 並獲 Spec Owner 批准
3. **Extension MUST be documented in change artifacts**: 不得在未記錄的情況下悄悄引入 extension
4. **Extension MUST NOT change frozen interfaces**: 已在 Change 01-03 凍結的 observation / action / metric 定義不得在 extension 中悄悄更改
5. **PPO is NOT a DQN extension**: PPO 是一個完全不同的 algorithm，需要新的 MDP interface 審視

---

## Reward Ablation Rules

| 項目 | 規格 |
|------|------|
| **Status** | Future extension（Change 05 with Spec Owner approval）|
| **When** | 在 DQN MVP evaluation 完成後 |
| **Scope** | 比較不同 reward weight（α, β, λ）對 DQN performance 的影響 |
| **Non-negotiable** | Reward 必須仍包含 delay 和 loss component；純 throughput-only reward 只作 ablation baseline，不得成為 final reward |
| **Output** | 各 weight 配置的 evaluation metrics + comparison table |
| **Change required** | 若 ablation 改變 reward formula 結構（非只改 weight），必須另開 change |

---

## Observation Ablation Rules

| 項目 | 規格 |
|------|------|
| **Status** | Future extension（another OpenSpec change with Spec Owner approval）|
| **When** | 在 DQN MVP evaluation 完成後 |
| **Scope** | 比較 minimal observation（shape [5]）vs enhanced observation（加入 queue_occupancy 等）|
| **Non-negotiable** | MVP observation shape 不得改變而不另開 change；enhanced observation 不得阻塞 MVP |
| **Change required** | 加入 enhanced observation 必須另開 OpenSpec change，說明新的 observation shape 和 normalization |

---

## Algorithm Extension Rules

| Extension | Status | Requirements |
|-----------|--------|-------------|
| Double DQN | Optional enhancement within Change 04 | Must document in run metadata; does not require new change |
| Dueling DQN | Optional enhancement within Change 04 | Must document in run metadata |
| Prioritized Experience Replay | Optional enhancement within Change 04 | Must document in run metadata |
| **PPO** | **Future extension** | **Requires new OpenSpec change + Spec Owner approval** |
| SAC / TD3 | Future extension | Requires new OpenSpec change |
| A3C / A2C | Future extension | Requires new OpenSpec change |
| Multi-agent RL | Out of scope | Not in this project's scope |

> ⚠️ Double DQN / Dueling DQN / PER 可在 Change 04 implementation 中選擇性使用，但必須記錄在 training_config.yaml 中，且作為 DQN variant 而非全新 algorithm。

---

## PPO Governance

| 項目 | 規格 |
|------|------|
| **Status in MVP** | ⛔ EXCLUDED from Change 03 and Change 04 |
| **Why excluded** | PPO is a policy gradient method, typically used for continuous or complex action spaces; DQN MVP uses Discrete(3) and value-based learning |
| **Can it be introduced?** | Yes, but ONLY with a new OpenSpec change AND Spec Owner approval |
| **What the new change must define** | New policy interface; whether action space changes; new hyperparameter protocol; new evaluation comparison |
| **Trigger to consider PPO** | If DQN consistently fails to converge over multiple seeds after thorough debugging |
| **PPO NOT a shortcut** | PPO cannot be introduced as a "quick fix" for DQN underperformance without proper specification |

### PPO Introduction Process（if ever needed）

```
1. Document DQN failure in Change 04 final report
2. Create new OpenSpec change: change-04b-ppo-extension (or change-06-ppo)
3. Define new MDP interface considerations for PPO
4. Get Spec Owner approval
5. Implement PPO in separate branch
```

---

## Continuous Action Extension Rules

| 項目 | 規格 |
|------|------|
| **Status** | ⛔ EXCLUDED from Change 04 MVP |
| **Why excluded** | Continuous action requires a different DRL paradigm（policy gradient / actor-critic）; the current Discrete(3) interface is frozen in Change 03 |
| **Can it be introduced?** | Yes, with a new OpenSpec change that redefines action space and policy |
| **Impact of introducing** | Would require updating Change 03 action-space.md; not a small change |

---

## Extension Priority Order（After MVP completion）

If time and resources allow, extensions should be considered in this order:

1. **Double DQN / Dueling DQN** — Lowest overhead, within Change 04 scope
2. **Reward ablation（Change 05）** — High value for academic reporting
3. **S3 / S4 scenarios** — Additional scenario validation（if time allows）
4. **PPO（new change）** — Requires full new change and approval
5. **Observation ablation（new change）** — Requires new change and approval
6. **Continuous action（new change）** — Major architecture change, high risk

> ⛔ IPFS / QUIC / multi-agent / multi-path / kernel TCP modification are NOT extensions; they are out-of-scope features and must NOT be introduced under any circumstances.
