## Purpose

定義 Change 04 dqn-mvp-agent 的 DQN MVP scope、non-goals、non-negotiable constraints 與前置依賴。

本檔案是 Change 04 的核心邊界定義。Phase 4 implementation 必須嚴格遵循本規格。

---

## DQN MVP Scope

| 項目 | 規格 |
|------|------|
| **Algorithm** | Stable-Baselines3（SB3）DQN |
| **Policy** | `MlpPolicy`（default candidate）|
| **Observation** | shape [5]：throughput_norm / delay_norm / loss_norm / congestion_indicator / prev_action_norm |
| **Action** | Discrete(3)：{0: decrease, 1: keep, 2: increase} |
| **Reward** | r = α·t_norm − β·d_norm − λ·l_norm（α=1.0, β=0.1, λ=10.0 初始值）|
| **Scenarios** | S1（Required）、S2（Required）、S3/S4（Optional）|
| **Baselines** | NewReno（Required）、CUBIC（Required）、BBR（Strongly recommended）|
| **Simulator** | ns-3.40（Spec Owner frozen）|
| **Env bridge** | ns3-gym（ns3-gym / OpenGym）|
| **Framework** | Python + Stable-Baselines3 + Gymnasium-compatible env |

---

## DQN Non-Goals

以下明確**不在** Change 04 MVP scope 內：

| 非目標 | 說明 |
|--------|------|
| PPO | Future extension（另開 change）|
| SAC / TD3 / A3C | Future extension |
| Continuous action | Future extension（需另開 change）|
| Observation ablation | Future extension（Change 05）|
| Reward ablation | Future extension（Change 05）|
| IPFS / QUIC | 不在專題 scope 內 |
| Kernel-level TCP modification | 不在 scope |
| Multi-agent RL | 不在 scope |
| Multi-path routing | 不在 scope |
| Large-scale topology | 不在 scope |
| Hyperparameter tuning study | Optional enhancement，非 MVP |
| DQN vs Pantheon comparison | Pantheon 為 benchmark philosophy，非 required dependency |

---

## Non-Negotiable Constraints

以下約束在 Phase 4 implementation 中不得違反：

1. **Smoke test before training**: DQN training 開始前，Change 03 smoke test（ST-01~ST-10）必須全部通過
2. **Baseline before DRL**: Phase 3 baseline benchmark 必須先完成，才能進入 DQN training
3. **Discrete action only**: Action space 固定為 Discrete(3)；不得改為 continuous 而不另開 change
4. **Metric-compatible evaluation**: Evaluation metrics 必須與 Change 02 baseline 同單位、同計算方式
5. **Reproducible metadata**: 每次 training run 必須記錄完整 seed / config / hyperparameters
6. **Reportable failure**: DQN underperformance 必須誠實記錄，不得隱藏
7. **No PPO in MVP**: PPO 不得在 Change 04 實作中出現

---

## Dependencies on Change 03

| 依賴項目 | Change 03 artifact |
|---------|------------------|
| Observation shape [5] and field order | `specs/observation-space.md` |
| Action space Discrete(3) | `specs/action-space.md` |
| Reward concept (r = α·t − β·d − λ·l) | `specs/reward-function.md` |
| Reset / step / terminated / truncated / info dict | `specs/episode-step-reset.md` |
| Smoke test ST-01~ST-10 | `specs/smoke-test.md` |
| MDP interface M=(S,A,P,R,γ) | `specs/mdp-interface.md` |

---

## Dependencies on Change 02

| 依賴項目 | Change 02 artifact |
|---------|------------------|
| ns-3.40 version freeze | `design.md`（OQ-02.01 resolved）|
| Baseline methods（NewReno/CUBIC/BBR）| `specs/baseline-methods.md` |
| Topology（single bottleneck）| `specs/topology.md` |
| Metrics（throughput/RTT/loss/utility）| `specs/metrics-logging.md` |
| Scenario matrix S1/S2 | `specs/scenario-matrix.md` |
| BBR fallback rule | `specs/baseline-methods.md` + `specs/benchmark-risk-register.md` |

---

## Required Before Phase 4

Phase 4（DQN implementation）開始前，必須完成：

1. ✅ Change 01 Spec Owner approval（已完成）
2. ✅ Change 02 Spec Owner approval（specification phase 已完成；/opsx:apply 在 Phase 3）
3. ✅ Change 03 Spec Owner approval（已完成）
4. ✅ Change 04 Spec Owner approval（本 change）
5. ⏳ Phase 3 baseline benchmark 執行完成（Change 02 /opsx:apply）
6. ⏳ Smoke test ST-01~ST-10 通過（Change 03 實作 + 測試）
