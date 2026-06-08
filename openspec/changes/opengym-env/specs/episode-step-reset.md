## Purpose

定義 Change 03 opengym-env 的 episode / step / reset 規格，包含 episode 結構、reset 概念流程、step 概念流程、terminated / truncated 定義，以及 info dictionary 欄位規格。

本檔案的規格適用於 OpenAI Gym / Gymnasium interface（`env.reset()` / `env.step(action)`）。

---

## Episode Structure

| 概念 | 說明 |
|------|------|
| **Episode** | 對應一次完整的 ns-3 scenario simulation（e.g., scenario S1 或 S2）|
| **Decision interval** | 每個 step 推進的 simulation 時間（1–5 秒；具體值在 Change 04 中定義）|
| **Episode length** | `sim_duration / decision_interval`（e.g., 60s / 2s = 30 steps per episode）|
| **Episode start** | 呼叫 `reset()` 時，ns-3 simulation 重新初始化並從 t=0 開始 |
| **Episode end** | `terminated = True`（simulation duration 達到）或 `truncated = True`（time limit / error）|

---

## Reset Concept

`reset()` 的概念流程（不含具體程式碼）：

```
reset() concept:
1. Select scenario config (S1 or S2; random seed fixed)
2. Initialize ns-3 simulation parameters
   - topology: sender → router → receiver (ns-3.40, PointToPoint)
   - TCP algorithm: baseline-compatible (but under agent control in DRL)
   - link_bandwidth, link_delay, queue_size from scenario_*.yaml
3. Initialize flow (start long-lived TCP flow from sender to receiver)
4. Initialize metrics buffer (clear all accumulated throughput / delay / loss)
5. Initialize previous action = 1 (keep, neutral starting state)
6. Advance simulation by one decision interval (warm-up)
7. Collect initial observation from FlowMonitor / TracedValue
8. Return: (observation, info)
```

**Reset 必須返回**：
- `observation`: shape [5]（或 [4] if `prev_action_norm` excluded）
- `info`: dict（含 scenario ID, step_index = 0, 基本 metadata）

---

## Step Concept

`step(action)` 的概念流程（不含具體程式碼）：

```
step(action) concept:
1. Receive action (int, ∈ {0, 1, 2})
2. Validate action is in action space
3. Map action to sender-side control abstraction:
   - 0 (decrease): reduce sender-side transmission parameter
   - 1 (keep):     maintain current parameter
   - 2 (increase): increase sender-side transmission parameter
4. Send control signal to ns-3 via ns3-gym socket
5. Advance ns-3 simulation by one decision interval
6. Collect metrics from FlowMonitor / TracedValue:
   - throughput_mbps (rxBytes in interval / interval duration)
   - delay_ms (delaySum / rxPackets, or estimate)
   - loss_rate ((txPackets - rxPackets) / txPackets)
7. Compute observation:
   - throughput_norm, delay_norm, loss_norm, congestion_indicator, prev_action_norm
8. Compute reward:
   - r_t = α·throughput_norm − β·delay_norm − λ·loss_norm
   (weights provisional; defined in Change 04)
9. Determine terminated / truncated (see below)
10. Compose info dict (see below)
11. Update previous action = action
12. Return: (observation, reward, terminated, truncated, info)
```

---

## Terminated / Truncated

遵循 Gymnasium（新版 Gym）的 `terminated` / `truncated` 分離規範：

| 狀態 | 觸發條件 | 說明 |
|------|---------|------|
| `terminated = True` | Simulation duration 達到（自然結束）| Episode 正常完成；agent 應接收到完整 episode 的 reward |
| `truncated = True` | Step 數超過 max_steps 但未自然結束 | Time limit 達到；或 environment fatal error |
| `terminated = False, truncated = False` | Episode 仍在進行中 | 正常 step |

**Fatal error 情境**（導致 `truncated = True`）：

- ns-3 simulation process 意外退出
- ns3-gym socket 連線斷開
- Observation 取得失敗（全部 fallback 均失效）

**Episode boundary 規則**：

- `terminated` 和 `truncated` 不可同時為 True
- 若 episode 正常結束後呼叫 `step()`，必須 raise error 並要求 `reset()`

---

## Info Dictionary Requirements

每個 `step()` 回傳的 `info` dict 必須包含以下欄位：

```python
info = {
    # === Raw Metrics（baseline-compatible）===
    "raw_throughput_mbps":  float,   # 本 step 的 goodput (Mbps)
    "raw_delay_ms":         float,   # 本 step 的 avg delay (ms)
    "raw_loss_rate":        float,   # 本 step 的 packet loss rate [0, 1]
    "utility_score":        float,   # provisional utility (same formula as Change 02)

    # === Normalization Metadata ===
    "delay_estimate_method": str,    # "direct_rtt" or "delaySum_per_packet"
    "observation_clipped":   bool,   # True if any observation value was clipped to [0, 1]

    # === Episode / Step Context ===
    "scenario_id":          str,    # "scenario_a" or "scenario_b"
    "step_index":           int,    # 從 0 開始的 step 計數
    "episode_sim_time_s":   float,  # 目前 simulation time (秒)

    # === Action Metadata ===
    "action_applied":       int,    # 實際執行的 action id (0, 1, 2)
    "action_symbol":        str,    # "decrease", "keep", "increase"
    "sender_param_before":  float,  # action 前的 sender-side parameter
    "sender_param_after":   float,  # action 後的 sender-side parameter
}
```

**Info dict 規則**：

1. 所有欄位必須在每個 step 都存在（不得缺席）
2. `utility_score` 使用 Change 02 的 provisional formula（baseline-compatible）
3. `raw_*` 欄位不需要 normalization，但必須有明確單位
4. `delay_estimate_method` 必須在每個 step 記錄，以便後處理時知道 RTT 計算方式

---

## Baseline Metric Compatibility

Info dict 中的 `raw_throughput_mbps`、`raw_delay_ms`、`raw_loss_rate` 和 `utility_score`，
必須與 Change 02 baseline 結果的相同欄位**單位與計算方式一致**，以確保 DRL vs. baseline 比較的公正性。

Change 04 evaluation 時，應提取每個 episode 的 info dict，計算：
- Mean throughput（Mbps）
- Mean delay（ms）
- Mean loss rate
- Mean utility score

並與 Change 02 baseline 的同一 scenario 的對應值比較。
