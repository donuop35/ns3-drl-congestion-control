# Phase 6 Extension Decision: PPO / Continuous Action as Future Work

## 1. Purpose

本文件記錄 Phase 6「條件式擴展階段」的正式決策。Phase 6 的定位是：

> 只有 DQN MVP 成功後，才考慮 PPO / continuous action 擴展。本學期不實作，作為 future-work 對比階段正式嵌入報告。

本文件是 **Decision Record**，不是 implementation report。

---

## 2. Why Phase 6 Exists

本專題的研究路線原始設計為：

1. Phase 0–2：題目定案、OpenSpec 規格建立
2. Phase 3：TCP Baseline Benchmark
3. Phase 4：DQN MVP Implementation
4. Phase 5：Final Reporting / Demo / PPT Package
5. **Phase 6：Conditional Extension（PPO / continuous action）**
6. Phase 7：High-Score Final Deliverable Packaging

Phase 6 的存在是因為：DQN 使用 Discrete(3) 動作空間，可能導致策略過於粗糙。如果 DQN MVP 成功完成，自然的下一步是嘗試支援 continuous action 的演算法（如 PPO），以改善粗粒度動作的限制。

Phase 6 不是一個「必須實作」的階段，而是一個「條件式考慮」的 decision point。

---

## 3. DQN MVP Completion Gate

Phase 6 的前置條件是 DQN MVP 必須成功完成。目前狀態：

| 前置條件 | 狀態 |
|----------|------|
| ns3-gym / OpenGym 環境建立 | ✅ Phase 4 Complete |
| DQN S1 訓練完成 (30k steps, seed=42) | ✅ ep_rew_mean=84.4 |
| DQN S2 訓練完成 (30k steps, seed=42) | ✅ ep_rew_mean=86.5 |
| DQN S1 評估完成 | ✅ Utility=0.900, Rank #2 |
| DQN S2 評估完成 | ✅ Utility=0.757, Rank #3 |
| DQN vs Baselines 比較完成 | ✅ 與 NewReno / CUBIC / BBR 完整比較 |
| Final Report 完成 | ✅ Phase 5 Complete |
| Final Figures 完成 | ✅ 9 張，QA 通過 |

**結論：DQN MVP Completion Gate 已通過。**

---

## 4. Evidence from Current DQN Results

DQN MVP 的結果顯示 DQN 沒有全面勝過 TCP baselines，但有限度的可行性：

### S1（低延遲瓶頸：10 Mbps, 10 ms）

| Algorithm | Utility | Rank |
|-----------|---------|------|
| BBR | 0.947 | #1 |
| **DQN** | **0.900** | **#2** |
| CUBIC | 0.884 | #3 |
| NewReno | 0.875 | #4 |

- DQN 排名第 2，高於 CUBIC / NewReno，但低於 BBR。
- DQN S1 採取 **100% Increase 退化策略（degenerate policy）**：Agent 在低延遲環境中發現壓榨頻寬極限即可獲得高 reward，不需要精細控制。
- 這反映了 Discrete(3) 動作空間的限制——Agent 沒有中間選項可微調發送速率。

### S2（高延遲瓶頸：10 Mbps, 50 ms）

| Algorithm | Utility | Loss Rate | Rank |
|-----------|---------|-----------|------|
| NewReno | 0.923 | 0.14% | #1 |
| CUBIC | 0.818 | 0.88% | #2 |
| **DQN** | **0.757** | **5.54%** | **#3** |
| BBR ⚠️ | -0.169 | 1.58% | #4 |

- DQN 排名第 3，輸給 NewReno / CUBIC。
- DQN 丟包率高達 **5.54%**，遠高於 NewReno 的 0.14%。
- 粗粒度的離散動作（只有 ↓ = ↑ 三選一）使 Agent 傾向暴力提高發送速率以追求 throughput reward，容忍丟包。

### DQN Discrete(3) Action 的根本限制

| 問題 | 說明 |
|------|------|
| S1 degenerate policy | 100% Increase，因為沒有更精細的「Increase by 5%」選項 |
| S2 high loss | ~87% Increase / ~13% Decrease，因為沒有 continuous rate adjustment |
| 粗粒度動作 | Discrete(3) = {↓, =, ↑} 無法表達精細的 sending-rate 調整 |
| Sender-side abstraction | 動作是應用層速率控制（Fallback Option B），非 kernel-level TCP cwnd |

---

## 5. What PPO / Extension Could Address

基於以上證據，PPO / continuous action 可能改善的方向：

### 5.1 Continuous Action Space

- **DQN 限制**：只支援 `Discrete` action（SB3 官方文件明確說明 DQN 不支援 `Box` continuous action）。
- **PPO 能力**：PPO 支援 `Discrete` 與 `Box` action space（SB3 官方文件確認）。
- **改善假說**：continuous action 可以表達「Increase by 3%」「Decrease by 7%」等精細調整，可能避免 S1 degenerate policy 與 S2 暴力提速造成的高丟包。

### 5.2 Actor-Critic Architecture

- **DQN**：value-based method，透過 Q-network 學習每個離散動作的 Q-value。
- **PPO**：actor-critic method，透過 clipping 限制 policy update 不離舊 policy 太遠。
- PPO 的 actor-critic 設計可能更適合 rate-control 問題，因為 rate control 本質上是連續的。

### 5.3 Reward Refinement

- 目前 reward 權重 α=1.0, β=0.1, λ=10.0 為 provisional。
- 未來可以進行 reward ablation study：增加 loss penalty（λ）可能抑制 S2 高丟包行為。
- 也可嘗試 delay-sensitive reward，對 delay proxy 給予更高懲罰。

### 5.4 Finer-Grained Rate Control

- continuous action 搭配 normalized rate adjustment (e.g., [-1.0, +1.0] → rate change percentage) 可能讓 Agent 學到更精細的 congestion control 策略。

---

## 6. What Phase 6 Does Not Claim

以下是本 decision record 明確不宣稱的內容：

| 不宣稱 | 原因 |
|--------|------|
| PPO 一定會反轉 DQN 的結果 | PPO 同樣面臨 exploration / reward design / environment fidelity 挑戰 |
| PPO 一定勝過 BBR / NewReno / CUBIC | TCP baselines 已經過數十年最佳化，PPO 未必能在所有場景超越 |
| PPO 已在本學期實作 | Phase 6 是 decision record，不是 implementation |
| PPO 有訓練結果可供參考 | 沒有任何 PPO 實驗數據 |
| Continuous action 一定解決問題 | continuous action 帶來更大的 exploration space，可能需要更多 training steps |
| DQN 結果因 PPO 而改變 | 所有 final results 仍基於 DQN MVP |

---

## 7. Why Phase 6 Is Deferred This Semester

| 理由 | 說明 |
|------|------|
| Scope control | 本學期已完成 Phase 0–5 + Phase 7，加上 PPO 會造成 scope creep |
| DQN MVP 已足夠 | DQN MVP 已驗證 DRL CC 的可行性與限制，達到期末專題的要求 |
| PPO 需要重新設計環境 | continuous action 需要修改 ns3-gym observation / action mapping |
| PPO 訓練時間未知 | PPO + continuous action 可能需要更多 training steps |
| 避免草率實作 | PPO 是另一套 actor-critic 設計，不應在期末最後階段被草率加成「已實作」 |
| Spec Owner 決定 | Phase 6 已由 Spec Owner 正式決定在本學期跳過，作為 deferred future work |

---

## 8. Suggested Future PPO Design

若未來要實作 Phase 6，建議的設計如下（僅供參考，不代表已實作）：

### Environment

- 沿用 ns-3.40 + ns3-gym + ZMQ 架構
- 修改 action space 從 `Discrete(3)` 改為 `Box(low=-1.0, high=1.0, shape=(1,))`
- action 映射為 sending rate 的百分比變化（e.g., -10% ~ +10%）

### Algorithm

- PPO（Stable-Baselines3 PPO）
- Default hyperparameters 作為起點
- 可能需要 learning rate scheduler

### Reward

- 維持 R = αT − βD − λL 結構
- 考慮增大 λ 以抑制 high-loss 行為
- 考慮 delay-sensitive reward adjustment

### Evaluation

- 與 DQN MVP 相同的 evaluation protocol
- 與 TCP baselines 使用相同 CSV source of truth 比較
- Seed 一致（seed=42）

### Expected Challenges

- continuous action space → larger exploration space → 可能需要更多 training steps
- PPO clipping → policy update 穩定但可能收斂較慢
- ns3-gym action mapping → 需要驗證 continuous rate adjustment 是否被 ns-3 正確接受

---

## 9. Expected Risks of PPO Extension

| 風險 | 說明 |
|------|------|
| PPO 可能仍輸 BBR | BBR 有 pacing mechanism，即使 continuous action 也未必能超越 |
| Training cost | PPO + continuous action 可能需要 50k+ steps |
| Environment compatibility | ns3-gym 的 continuous action handling 需要測試 |
| Reward sensitivity | continuous action + provisional reward weights 可能產生不穩定行為 |
| Overfitting | PPO 可能 overfit 到特定場景 (S1/S2)，不具泛化性 |

---

## 10. Final Decision

**Phase 6 正式決策：Deferred as Future Work。**

- DQN MVP 已成功完成，Phase 6 的前置條件已滿足。
- 實驗結果顯示 DQN Discrete(3) action 的粗粒度是主要限制因素。
- PPO / continuous action 是技術上合理的改進方向。
- 但本學期不實作 PPO，以避免 scope creep 與草率實作。
- Phase 6 的價值在於：研究路線補全、future work 合理化、以及對 DQN 限制的結構化分析。

> 本文件是 Decision Record，不是 Implementation Report。所有 final results 仍基於 DQN MVP。
