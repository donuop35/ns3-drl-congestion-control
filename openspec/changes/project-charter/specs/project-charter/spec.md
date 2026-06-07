# Project Charter

## Purpose

本文件是「DRL-Based Congestion Control over a Bottleneck Link」期末專題的 **single source of truth（唯一真相來源）**。

所有後續 OpenSpec changes 的 proposal.md、design.md、tasks.md 均必須以本 charter 作為上游規格依據。任何與本 charter 衝突的任務或決策，必須先回報 spec owner，取得明確批准後才能推進。

---

## Project Mission

> 本研究將單一瓶頸鏈路的壅塞控制建模為深度強化學習問題，透過 ns-3 / ns3-gym 建立可重現的網路模擬環境，讓 agent 學習在 throughput、RTT 與 packet loss 之間取得更好的控制折衷，並與傳統 TCP baseline 進行比較。

---

## Project Title（正式凍結）

| 版本 | 標題 |
|------|------|
| **中文正式題目** | 以深度強化學習進行單一瓶頸鏈路壅塞控制與吞吐量最佳化 |
| **英文正式題目** | Deep Reinforcement Learning for Congestion Control and Throughput Optimization over a Single Bottleneck Link |
| **GitHub / README 簡版** | DRL-Based Congestion Control over a Bottleneck Link |

上述題目**不得更改**，任何更改需要 spec owner 明確批准並新開 OpenSpec change。

---

## Research Background

### 網路壅塞控制的重要性

網路壅塞控制（Congestion Control）是確保網路穩定傳輸的核心機制。發送端必須動態調整傳輸速率，避免超過瓶頸鏈路的承載能力，否則將導致：

- 封包佇列溢出（Queue overflow）→ 封包遺失（Packet loss）
- RTT（Round-Trip Time）大幅上升（Bufferbloat 問題）
- 網路吞吐量崩潰（Congestion collapse）

### 傳統 TCP 演算法的限制

- **NewReno**（RFC 6582）：依靠 packet loss 作為壅塞信號，使用 AIMD 控制，保守但在高 BDP 網路效率低
- **CUBIC**（RFC 8312）：Linux 預設演算法，cubic growth function，更積極但仍是 loss-based
- **BBR**（Google 2016）：model-based 方法，估計 bottleneck bandwidth 和 min-RTT，但在高 loss 場景表現不穩定

傳統算法都使用**手刻規則（hand-crafted heuristics）**，難以適應複雜多變的網路條件。

### 為什麼 DRL 適合解決此問題

1. **DRL 可學習複雜決策策略**：不需手刻規則，agent 直接從網路狀態中學習最優控制策略
2. **端到端優化**：可直接優化一個複合 utility 函數（throughput - delay - loss），而非只關注某一個指標
3. **適應性**：訓練好的 policy 理論上可適應不同網路條件
4. **可解釋的 MDP 建模**：壅塞控制本身天然符合 MDP 結構（有狀態、有動作、有 reward）

---

## Research Target

本專題的核心研究目標包含：

1. **Single bottleneck congestion control**：在 `sender → bottleneck link → receiver` 的拓樸下建立可控的壅塞場景
2. **Sender-side control abstraction**：agent 控制傳送端的送率或 cwnd-like 控制訊號，不需修改 kernel
3. **DRL formulation**：將壅塞控制建模為 MDP，定義清楚的 state / action / reward / episode
4. **Baseline comparison**：與 NewReno、CUBIC（+ BBR）進行公平的 throughput / RTT / loss / utility 比較

---

## MDP 初版定義（凍結）

| 元素 | 定義 |
|------|------|
| **Environment** | ns-3 single bottleneck simulation |
| **Agent** | DRL congestion-control agent |
| **State space** | `[throughput_norm, rtt_norm, loss_rate, cwnd_or_rate_signal_norm]`（4-dim，待 Change 03 確認）<br>**cwnd fallback rule**：第 4 維優先使用 `cwnd_signal_norm`；若 Change 03 smoke test 驗證無法穩定取得或控制 cwnd，必須改為 `sending_rate_signal_norm`（或等效 congestion-control abstraction），並在 Change 03 design.md 中記錄 Decision Record，等待 Spec Owner 確認後才能繼續。 |
| **Action space** | `Discrete(3)`：{0: decrease, 1: keep, 2: increase}（語意：降低 / 維持 / 提高送率或 cwnd-like 控制訊號） |
| **Reward** | `r_t = α·throughput_t − β·RTT_t − γ·loss_t` |
| **Episode length** | 60 秒（初版，待 smoke test 後調整） |
| **Decision interval** | 500ms（初版，待 smoke test 後調整） |

---

## Success Definition

### 成功 = 以下條件均達成

- [x] 研究方向清楚，不偏離凍結題目（Change 01 ✅ 已通過 Spec Owner 驗收）
- [ ] Baseline（NewReno/CUBIC）可重現執行，產出 CSV log（Change 02 目標）
- [ ] ns3-gym environment 可 reset / step，random agent 可跑完 1 個 episode（Change 03 目標）
- [ ] DQN 訓練腳本可完成訓練，產出 reward curve（Change 04 目標）
- [ ] 至少有一張 DRL vs baseline comparison 圖表（Change 04/05 目標）
- [ ] GitHub repo 可被第三方依 README 重現主要流程（Change 05 目標）
- [ ] 10 分鐘 demo script 可說明：problem / baseline / DRL design / result / limitation（Change 05 目標）

### 成功 ≠ 以下條件

- ❌ DRL 全面打敗所有 TCP baseline（不要求，不偽造）
- ❌ 真實網路部署
- ❌ IPFS 實作
- ❌ QUIC 實作
- ❌ production-grade TCP protocol

---

## OpenSpec Governance Role

在本專案中，OpenSpec 扮演以下角色：

1. **規格中樞**：每一個開發 change 的 proposal / design / tasks / specs 都由 OpenSpec 管理
2. **Antigravity 的行動邊界**：Antigravity 只能在當前 OpenSpec change 的 tasks.md 所定義的範圍內執行任務
3. **驗收機制**：每個 change 完成後，必須等待 spec owner 驗收（確認 `openspec status` 顯示 complete），才能啟動下一個 change
4. **防偏軌機制**：OpenSpec specs 中的 Non-goals 和 Governance Rules 防止實作偏向 IPFS / QUIC / multi-agent 等非 MVP 範疇
5. **未驗收前禁止推進**：若 spec owner 尚未確認，Antigravity 不得自行進入下一個 change

---

## Downstream Change Map

| Change | 名稱 | 狀態 | 啟動條件 |
|--------|------|------|---------|
| 01 | project-charter（本 change） | ✅ Approved（Spec Owner 已驗收） | — |
| 02 | ns3-baseline-benchmark | 🟡 In Progress | ✅ Change 01 已通過 |
| 03 | ns3gym-environment | ⏳ Pending | Change 02 spec owner 確認 |
| 04 | dqn-mvp-agent | ⏳ Pending | Change 03 spec owner 確認 |
| 05 | reporting-figures-and-demo | ⏳ Pending | Change 04 spec owner 確認 |
