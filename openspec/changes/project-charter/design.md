# Design: Project Charter Governance

## Design Goal

本 design 的目標是建立本期末專題的 **project governance**（專案治理框架），而不是程式架構設計。

本 design 不包含任何程式實作決策，不包含 ns-3 參數設定，不包含 DQN 超參數選擇。
所有程式架構決策將在對應的下游 change（change-02、03、04）的 design.md 中定義。

---

## Project Scope Boundary

### In Scope（本學期 MVP 必做）

| 項目 | 說明 |
|------|------|
| Single bottleneck link topology | sender → bottleneck link → receiver，單一瓶頸鏈路 |
| ns-3 simulation | 使用 ns-3 建立可重現的網路模擬環境 |
| ns3-gym RL interface | 將 ns-3 simulation 包裝成 RL Gym environment |
| Sender-side congestion-control abstraction | agent 控制傳送端的送率或 cwnd-like 訊號 |
| DQN MVP | Stable-Baselines3 DQN，離散 action space，第一版演算法 |
| NewReno / CUBIC baseline | 必做；提供傳統 TCP 比較基準 |
| BBR baseline | Strongly preferred；若整合成本可控則納入 |
| Throughput / RTT / loss / utility evaluation | 四個主要 metrics，必須同時評估 |
| Reward curve / convergence behavior | DRL 訓練過程可視化 |
| Experiment scenarios A + B | Scenario A（低延遲穩定）+ Scenario B（高延遲穩定）|
| GitHub repo / README / PPT assets / demo script | 期末交付物 |
| Risk-honest reporting | 若 DQN 不贏 baseline，誠實報告 trade-off，不偽造 |

### Out of Scope（本學期不做）

| 項目 | 原因 |
|------|------|
| IPFS implementation | 與壅塞控制 DRL 研究無直接關聯；僅可放 motivation/future work |
| QUIC congestion control | 超出本學期 scope |
| Linux kernel TCP stack modification | 無法在模擬環境重現，風險極高 |
| Real Internet deployment | 不可重現，無法控制實驗條件 |
| Multi-agent RL | MVP 先解決 single agent 問題 |
| Multi-path routing | 超出 single bottleneck 設定 |
| Large-scale network topology | 超出 single bottleneck 設定 |
| Pantheon full integration as required dependency | 安裝複雜，非 MVP 必要 |
| PPO as MVP requirement | PPO 作為 future extension，不替代 DQN MVP 優先序 |
| Production-level congestion control protocol | 非學術研究目標 |
| Distributed node systems | 超出本學期 scope |

---

## Technical Direction

以下技術選型**正式凍結**，更改需要 spec owner 核准：

| 層級 | 選擇 | 版本限制 |
|------|------|---------|
| **Simulator** | ns-3 | >= 3.32（BBR 支援）|
| **RL Interface** | ns3-gym | 與目標 ns-3 版本相容的最新版 |
| **Training Framework** | Stable-Baselines3 | >= 1.8.0 |
| **MVP Algorithm** | DQN | SB3 DQN，離散 action |
| **Future Algorithm** | PPO | 加分 / v2，不替代 DQN MVP |
| **Required Baselines** | NewReno, CUBIC | 必做 |
| **Preferred Baseline** | BBR | Strongly preferred，非 blocking |
| **Evaluation Metrics** | throughput, RTT, packet loss, utility score, reward curve, convergence behavior | 全部必做 |
| **Spec Management** | OpenSpec v1.4.1 | 官方 `@fission-ai/openspec` |

---

## Governance Rules

以下治理規則在本學期全程有效：

1. **No implementation before project-charter approval.** 在 spec owner 確認本 charter 前，不得開始任何程式實作。
2. **Do not write code in change-01.** change-01 只包含文件任務，不含任何程式碼。
3. **Do not run ns-3 in change-01.** 不在本 change 中執行 ns-3。
4. **Do not create ns3-gym environment in change-01.** 不在本 change 中建立 RL environment。
5. **Do not start DQN / PPO in change-01.** 不在本 change 中訓練任何 DRL agent。
6. **Do not implement IPFS.** 整學期禁止實作 IPFS，無論在哪個 change。
7. **Do not implement QUIC.** 整學期禁止實作 QUIC。
8. **Do not modify kernel TCP.** 整學期禁止修改 Linux kernel TCP stack。
9. **Do not introduce multi-agent RL.** 整學期禁止多智慧體 RL（未經 spec owner 批准）。
10. **Do not introduce multi-path routing.** 整學期禁止多路徑傳輸（未經批准）。
11. **Do not optimize for throughput alone.** Reward function 必須包含延遲懲罰與丟包懲罰。
12. **All downstream work must reference this charter.** 所有下游 change 的 proposal.md 必須引用本 charter 作為上游依據。

---

## Downstream Change Dependency

```
change-01-project-charter  ←── 本 change（必須先完成）
         │
         ├──→ change-02-ns3-baseline-benchmark
         │         ├── 依賴：baseline 選擇（NewReno/CUBIC/BBR）
         │         ├── 依賴：metrics 定義（throughput/RTT/loss/utility）
         │         ├── 依賴：topology 邊界（single bottleneck）
         │         └── 依賴：scenario 設定（A/B/C）
         │
         ├──→ change-03-ns3gym-environment（需要 change-02 完成）
         │         ├── 依賴：MDP 定義（state/action/reward/episode）
         │         ├── 依賴：RL interface 選擇（ns3-gym）
         │         └── 依賴：observation space 邊界
         │
         └──→ change-04-dqn-mvp-agent（需要 change-03 完成）
                   ├── 依賴：MVP 演算法選擇（DQN first）
                   ├── 依賴：evaluation philosophy（honest comparison）
                   └── 依賴：success definition（非 DRL 必勝 baseline）
```

**執行規則**：每個 change 完成後必須等待 spec owner 確認，才能啟動下一個 change。禁止同時進行多個 change（除非 spec owner 明確批准）。

---

## Decision Records

### DR-01: Use single bottleneck link topology

**Decision**: 第一版 topology 為 `sender → bottleneck link → receiver`，只有單一瓶頸。  
**Rationale**: 問題最簡單、最易重現、最易驗收。先解決 single bottleneck 才能推廣到複雜拓樸。  
**Alternatives**: Multi-hop topology → 排除（過於複雜，MVP 不需要）。

### DR-02: Use ns-3 as simulator

**Decision**: 使用 ns-3 網路模擬器。  
**Rationale**: 業界標準學術模擬器，有完整 TCP 模型（NewReno/CUBIC/BBR），且有 ns3-gym 整合。可重現、可控制、文獻基礎強。  
**Alternatives**: GNS3 / real testbed → 排除（不可重現）；Pure Python simulator → 排除（缺乏真實 TCP dynamics）。

### DR-03: Use ns3-gym as RL interface

**Decision**: 使用 ns3-gym 將 ns-3 包裝成 OpenAI Gym 介面。  
**Rationale**: 官方文獻已發表，有現成 example，可讓 Python DRL agent 與 ns-3 互動，無需重造輪子。  
**Alternatives**: 自寫 socket bridge → 排除（開發成本高，風險大）。

### DR-04: Use Stable-Baselines3 as training framework

**Decision**: 使用 Stable-Baselines3（SB3）進行 DRL 訓練。  
**Rationale**: 高品質、有文獻支持的 DRL 實作；支援 DQN、PPO 等主流演算法；有良好的 logging 和評估 API。  
**Alternatives**: RLlib → 排除（較複雜，對 MVP 過於重量級）；自實作 DQN → 排除（開發成本高）。

### DR-05: Use DQN for MVP

**Decision**: 第一版 DRL agent 使用 DQN（離散 action space）。  
**Rationale**: DQN 適合離散 action；離散 action 易於驗收（3 個明確選擇）；可先確保 pipeline 跑通，再考慮進階演算法。  
**Alternatives**: PPO with continuous action → 排除（更複雜，先驗證 pipeline）。

### DR-06: Keep PPO as future extension only

**Decision**: PPO 僅作為 change-04 之後的加分項目，不得取代 DQN 的 MVP 優先序。  
**Rationale**: 避免在未完成基礎 pipeline 時就跑向進階演算法。  
**Constraint**: 若 DQN MVP 完成前 PPO 相關任務出現，Antigravity 必須停止並回報。

### DR-07: Do not implement IPFS

**Decision**: IPFS 不在本學期任何 change 的實作範疇內。  
**Rationale**: 本專題是 DRL networking，IPFS 是 decentralized storage，無直接關聯。IPFS 只可放 motivation/future work。  
**Constraint**: 任何 IPFS 實作任務出現，Antigravity 必須立即停止並回報 spec owner。

### DR-08: Do not implement QUIC

**Decision**: QUIC congestion control 不在本學期任何 change 的實作範疇內。  
**Rationale**: QUIC 是另一個研究問題，超出 ns-3 + ns3-gym 的本學期工具鏈。  
**Constraint**: 同 DR-07。

### DR-09: Do not optimize for throughput alone

**Decision**: Reward function 必須包含 delay penalty 和 loss penalty，不得只最大化 throughput。  
**Rationale**: 純 throughput 最大化會導致 agent 學會用犧牲 RTT / 丟包換取吞吐量，這不是「好的壅塞控制」。  
**Implementation**: `r_t = α·throughput - β·RTT - γ·loss`，α, β, γ 待 change-03 smoke test 後確認。

### DR-10: Use official OpenSpec package, not simulated OpenSpec

**Decision**: 本專案必須使用官方 `@fission-ai/openspec` npm 套件，且必須可驗證。  
**Rationale**: 使用官方工具確保 SDD workflow 的一致性、可追蹤性，並防止「假 OpenSpec」問題。  
**Verification**: `openspec --version` 必須回報正確版本；`.agent/skills/` 和 `.agent/workflows/` 必須包含官方產生的檔案。  
**Constraint**: 若發現使用假 OpenSpec 或模擬 OpenSpec，必須立即停止，重新安裝官方套件。

---

## Open Questions（待 spec owner 決策）

| # | 問題 | 影響 | 狀態 |
|---|------|------|------|
| OQ-01 | Node.js v20.11.1 < 20.19.0（OpenSpec 要求）。功能目前正常（有 WARN），是否需要升級？ | 低（目前不影響功能） | ⏳ 待決策 |
| OQ-02 | ns3-gym 與最新 ns-3 版本的相容性確認 | 高（Change 03 的基礎）| ⏳ 待 Change 02 |
| OQ-03 | BBR 是否在目標 ns-3 版本支援（需要 >= 3.32）| 中（Change 02 決策）| ⏳ 待 Change 02 |
| OQ-04 | cwnd 是否可在 ns3-gym 中直接讀寫？ | 高（影響 action design）| ⏳ 待 Change 03 |
