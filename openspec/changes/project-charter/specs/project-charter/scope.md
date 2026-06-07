# Scope Specification

## In Scope

本學期 MVP 的正式納入範疇：

### 網路環境

- 單一瓶頸鏈路拓樸：`sender → bottleneck link → receiver`
- 可配置的瓶頸參數：bandwidth（Mbps）、propagation delay（ms）、queue size
- 固定 random seed 的實驗情境（Scenario A、B，optional C）

### 模擬工具

- **ns-3**（版本 >= 3.32）作為網路模擬器
- ns-3 TCP 模組用於 baseline benchmark
- ns3-gym 作為 RL 介面（將 ns-3 包裝成 Gym environment）

### Baseline

- **NewReno**（RFC 6582）— 必做
- **CUBIC**（RFC 8312）— 必做
- **BBR**（Google 2016）— Strongly preferred，非 blocking

### RL Environment

- Observation space（至少 4-dim：throughput、RTT、loss_rate、cwnd_signal）
- Action space（Discrete(3)：decrease / keep / increase）
- Reward function（throughput reward - RTT penalty - loss penalty）
- Episode reset / step / done / info 介面
- Random agent smoke test（至少 1 個 complete episode）

### DRL Agent（MVP）

- **Stable-Baselines3 DQN**（離散 action）
- Training script + evaluation script
- Training config（fixed hyperparameters）
- Trained model artifact（若合理儲存）

### 評估指標（Metrics）

- Average throughput（Mbps）
- Average RTT（ms）
- Packet loss rate（%）
- Utility score（composite：throughput - delay - loss penalty）
- Reward curve（training progress）
- Baseline comparison table

### 實驗情境

- **Scenario A**（必做）：穩定低延遲瓶頸，10 Mbps，RTT 20ms
- **Scenario B**（必做）：穩定高延遲瓶頸，10 Mbps，RTT 100ms
- **Scenario C**（optional）：動態/受干擾瓶頸

### 交付物

- GitHub repository（完整 README，可被第三方重現）
- Baseline benchmark CSV + figures
- ns3-gym smoke test log
- DQN reward curve figure
- DRL vs baseline comparison figure
- Final report outline
- PPT / slide assets
- 10 分鐘 demo script

---

## Out of Scope

本學期**不包含**以下項目（需 spec owner 明確批准才可加入）：

- IPFS 實作（僅可放 motivation / future work 章節提及）
- QUIC congestion control 實作
- Linux kernel TCP stack 修改
- 真實 Internet 部署
- Multi-agent RL（多個 agent 同時控制）
- Multi-path transmission（多路徑傳輸）
- Large-scale network topology（超過 sender + bottleneck + receiver 的拓樸）
- Pantheon 作為 MVP 必裝依賴
- PPO 作為 MVP 演算法（只作為加分 / future extension）
- Production-grade TCP protocol 實作
- Distributed node systems
- Adaptive Traffic Signal Control（ATSC）或其他非網路領域的 DRL 應用

---

## Strict Non-Goals

以下項目為**整學期硬性禁止**，不得以任何形式納入本專案任何 change 的實作：

> ⛔ **IPFS 實作** — 不得建立任何 IPFS node、不得修改 Bitswap、不得做 DHT 實驗
>
> ⛔ **QUIC 實作** — 不得實作任何 QUIC congestion control 演算法
>
> ⛔ **Linux kernel 修改** — 不得 patch 或修改 Linux kernel TCP 模組
>
> ⛔ **Multi-agent RL** — 不得引入多個 RL agent 同時競爭 / 協作
>
> ⛔ **Real Internet deployment** — 不得在任何真實 Internet 環境上執行實驗
>
> ⛔ **偽造實驗結果** — 若 DQN 不優於 baseline，必須誠實報告，不得捏造或誇大數字
>
> ⛔ **宣稱 DRL 全面勝過所有 baseline** — 本專案目標是公平比較，不是絕對勝負

---

## Expansion Rules

任何 scope 擴張必須遵守以下規則：

1. **任何 scope expansion 都必須另開一個新的 OpenSpec change。** 不得直接修改既有 change 的 tasks.md 偷偷加入新任務。

2. **IPFS / QUIC / multi-agent / multi-path 擴展，只能在所有 MVP changes（01–05）全部完成後討論。** 本學期內禁止作為實作範疇。

3. **Antigravity 不得自行新增研究方向。** 若 Antigravity 認為應加入某個新方向，必須停止並以明確文字向 spec owner 提出，等待批准後才能繼續。

4. **若實作中發現需要調整 scope，必須立即停止當前任務，回報 spec owner，並在 OpenSpec change 的 design.md 中記錄 Decision Record，等待確認後才能繼續。**

5. **Scope 爭議處理**：若對某項工作是否在 scope 內有疑義，預設為「不在 scope 內」，必須主動詢問 spec owner，不得自行認定。
