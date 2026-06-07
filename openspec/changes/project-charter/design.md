## Context

本研究是大學 DRL 課程期末專題，主題為「以深度強化學習進行單一瓶頸鏈路壅塞控制與吞吐量最佳化」。目前尚無任何實作程式碼，需要在開始 coding 前建立方向凍結文件，防止範疇蔓延並確保整學期工作朝向可驗收方向前進。

**Stakeholders**:
- Spec Owner / Project Owner：使用者（最終驗收者）
- Implementation Agent：Antigravity（負責 coding、實驗執行、圖表產出）

**Current State**: 專案目錄已建立，OpenSpec v1.4.1 已安裝，`.agent/` integration 已更新。尚無 baseline code、RL environment 或訓練腳本。

**Constraints**:
- 本學期時間有限，必須以 MVP 為優先
- 執行環境為 Windows + WSL / Linux VM（ns-3 需要 Linux）
- 不得引入大型新依賴，除非 Spec Owner 明確批准

---

## Goals / Non-Goals

**Goals:**
- 凍結研究題目、thesis statement、MDP 初版定義，作為整學期不可動搖的方向文件
- 明確定義 MVP 必做清單（5 個 changes）與各 change 的啟動條件
- 建立可追蹤的 Risk Register 初版
- 定義明確的 Acceptance Criteria，使 Spec Owner 能在期末驗收時有具體標準
- 凍結工具鏈：ns-3、ns3-gym、Stable-Baselines3、DQN
- 凍結 Metrics：throughput、RTT、packet loss、utility score、reward curve

**Non-Goals:**
- 不做 IPFS 實作（僅可作為 motivation / future work 提及）
- 不做 QUIC congestion control 實作
- 不改 Linux kernel TCP stack
- 不做 multi-agent RL
- 不做大型網路拓樸（> 2 nodes with 1 bottleneck link）
- 不做多路徑傳輸
- 不做分散式節點系統
- 不做 production-grade TCP protocol
- 不做 real Internet deployment
- 不做 Pantheon 必裝依賴
- 不承諾 DRL 全面勝過所有 TCP 演算法

---

## Decisions

### D1：工具鏈選擇

**Decision**: ns-3 + ns3-gym + Stable-Baselines3 + DQN  
**Rationale**: 這是課程常見的 networking RL research stack，有公開文獻支持，且都有現成 example 可參考。  
**Alternatives Considered**:
- GNS3 / real testbed：成本高、不可重現、debug 困難 → 排除
- SUMO (traffic simulation)：與網路壅塞控制無關 → 排除
- OpenAI Gym custom env（純 Python）：可行，但缺乏真實 ns-3 packet dynamics → 保留為 ns3-gym fallback

### D2：第一版演算法為 DQN（離散 action）

**Decision**: MVP 使用 Stable-Baselines3 DQN，action space 離散（3 個動作）  
**Rationale**: 離散 action 易於驗收；DQN 是最基礎的 DRL 演算法；MVP 應先確保 pipeline 跑通，而非追求最先進演算法。  
**Alternatives Considered**:
- PPO with continuous action：更強但 debug 成本高 → 保留為加分 / v2
- SAC：連續 action，適合 rate control → 保留為 future work

### D3：MDP 定義初版

**Decision**: 第一版 observation 包含 {throughput, RTT, loss_rate, cwnd_signal}，action 為 {0=decrease, 1=keep, 2=increase}，reward = α·throughput - β·RTT - γ·loss  
**Rationale**: 簡潔且文獻常見；reward 不可只看 throughput 以防 agent 學會用犧牲 RTT 換 throughput  
**Note**: 具體 observation 實現方式（直接控制 cwnd vs. 控制 sending rate）待 Change 03 確認可行性後在 design.md 更新

### D4：Baseline 選擇

**Decision**: 必做 NewReno + CUBIC；BBR 為 strongly preferred 但非 blocking  
**Rationale**: NewReno 是最基礎的 TCP；CUBIC 是 Linux 預設；BBR 代表 delay-based 流派，有 BBR 更能說明比較的豐富度。若 BBR 整合困難，不得讓其阻塞 Change 02 進度。

### D5：Episode 設計

**Decision**: 第一版 episode 長度 60s，decision interval 500ms  
**Rationale**: 短 episode 降低訓練成本；500ms 是 RTT 可觀測的合理尺度；實際值待 smoke test 確認後可調整

### D6：Experiment Scenarios

**Decision**: 3 個情境（A: 低延遲穩定、B: 高延遲穩定、C: 動態變動）  
**Rationale**: 至少需要兩個對照情境才有比較意義；Scenario C 成本高則列為 optional  
**Constraint**: 每個情境固定 random seed，config 寫入 `experiments/configs/`

---

## Risks / Trade-offs

| Risk | Level | Mitigation | Fallback |
|------|-------|-----------|---------|
| ns3-gym 安裝失敗 | 高 | 固定 Linux 環境，先跑官方 example | 改用純 Python Gym bottleneck env |
| BBR baseline 整合困難 | 中高 | 先完成 NewReno/CUBIC；BBR 非 blocking | 移至 optional/future work |
| 無法直接控制 cwnd | 高 | 先確認 ns-3/ns3-gym 可控接口 | 改控 application sending rate |
| Reward 導致 agent 學歪 | 高 | 加入 RTT/loss penalty；保留 component log | 固定權重 + 降低 scenario 複雜度 |
| DQN 表現不佳 | 中高 | 先追求 pipeline 跑通；不追求 SOTA | 誠實報告 trade-off；不偽造結果 |
| 題目擴張到 IPFS/QUIC | 最高 | Non-goals 明確列入 charter | 立即停止，回到 charter 重審 |
| OpenSpec CLI 無法使用 | 最高 | 已確認 v1.4.1 安裝成功 | 無降階方案；必須回報並停止 |
| Node.js 版本不符（v20.11.1 < v20.19.0）| 中 | 目前 v1.4.1 WARN 但功能正常 | 需要時升級 Node.js |

---

## Open Questions

1. **ns3-gym 與最新 ns-3 版本的相容性**：待 Change 02 環境建置時確認；若不相容，需要在 Change 02 design.md 更新 fallback 方案。
2. **cwnd 控制層級**：是否能在 ns3-gym 中直接取得並設定 cwnd？待 Change 03 smoke test 確認。
3. **BBR 在目標 ns-3 版本的支援**：ns-3 >= 3.32 有 BBR，但需確認目標版本。
4. **Node.js 版本升級**：是否需要現在升級 Node.js 到 20.19.0+ 以完全符合 OpenSpec 要求？
