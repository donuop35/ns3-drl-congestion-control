## Purpose

定義 Change 02 baseline benchmark 的 scenario matrix，包含 MVP-required 與 optional 情境。

---

## Scenario Rules

- **S1 和 S2 足以完成 MVP**，是最低驗收標準
- **S3 和 S4 不得阻塞 MVP 的完成**
- 每個情境都必須使用相同的 required metrics（throughput / RTT / loss / utility provisional）
- 每個情境都必須使用固定 random seed（記錄在 config 檔中）
- **不得在未經 Spec Owner 批准的情況下新增情境**

---

## Required Scenarios（MVP-required）

### S1：Stable Low-Delay Bottleneck

| 屬性 | 值 |
|------|----|
| **Scenario ID** | `scenario_a` |
| **MVP-required** | ✅ Yes |
| **Purpose** | Basic sanity check；驗證 TCP 基礎行為、測量穩定狀態下的 throughput / RTT / loss |
| **Traffic** | 1 個 long-lived TCP flow（sender → receiver） |
| **Bottleneck bandwidth** | 10 Mbps（configurable） |
| **Bottleneck delay** | 10 ms（low-latency） |
| **Queue size** | 100 packets（DropTail） |
| **Simulation duration** | 60 seconds |
| **Random seed** | 42（固定） |
| **Baselines** | NewReno, CUBIC, BBR（if available） |

### S2：Stable High-Delay Bottleneck

| 屬性 | 值 |
|------|----|
| **Scenario ID** | `scenario_b` |
| **MVP-required** | ✅ Yes |
| **Purpose** | 觀察 delay-sensitive behavior；high BDP 下 TCP 演算法的 throughput 與 RTT 折衷 |
| **Traffic** | 1 個 long-lived TCP flow（sender → receiver） |
| **Bottleneck bandwidth** | 10 Mbps（configurable） |
| **Bottleneck delay** | 50 ms（high-latency） |
| **Queue size** | 100 packets（DropTail） |
| **Simulation duration** | 60 seconds |
| **Random seed** | 42（固定） |
| **Baselines** | NewReno, CUBIC, BBR（if available） |

---

## Optional Scenarios（Not MVP-required）

### S3：Variable Bandwidth Bottleneck

| 屬性 | 值 |
|------|----|
| **Scenario ID** | `scenario_c` |
| **MVP-required** | ❌ No |
| **Priority** | Should-have（強烈建議，但不阻塞 MVP） |
| **Purpose** | 觀察 TCP 演算法在頻寬動態變化下的適應行為 |
| **Traffic** | 1 個 long-lived TCP flow |
| **Bottleneck bandwidth** | 動態（e.g., 10 Mbps → 5 Mbps → 10 Mbps，每 20s 切換） |
| **Bottleneck delay** | 20 ms |
| **Random seed** | 42 |
| **Baselines** | NewReno, CUBIC, BBR（if available） |

### S4：Bottleneck with Cross Traffic

| 屬性 | 值 |
|------|----|
| **Scenario ID** | `scenario_d` |
| **MVP-required** | ❌ No |
| **Priority** | Optional / Future extension |
| **Purpose** | 觀察 TCP 演算法在 background traffic 干擾下的 robustness |
| **Traffic** | 1 main TCP flow + N background flows（N 待定） |
| **Risk** | Cross traffic 增加 topology 複雜度，可能使 MVP 不穩定 |
| **Constraint** | **若 S4 導致 MVP 實作困難，必須立即降至 future work，不得阻塞 S1/S2** |

---

## Downstream Dependency

| Change | 使用本 scenario matrix 的方式 |
|--------|----------------------------|
| **Change 03**（ns3gym-environment）| 必須使用相同的 S1 / S2 scenario 定義作為 RL environment 的 reset 條件 |
| **Change 04**（dqn-mvp-agent）| DQN 必須在相同的 scenario 設定下與 baseline 比較；不得更改 scenario 定義 |
| **Change 05**（reporting）| 所有 DRL vs baseline 的圖表必須基於本 scenario matrix |
