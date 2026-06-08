## Purpose

定義 Change 03 opengym-env 的 observation（state）space 規格，包含 MVP minimal observation、enhanced observation（future extension）、normalization rules 與 fallback rules。

Change 04 drl-mvp 的 DQN 實作必須完整遵循本規格中定義的 observation shape、欄位順序與 normalization 方式。

---

## MVP Minimal Observation

MVP observation 為長度 5 的向量，**欄位順序固定**：

```python
observation = [
    throughput_norm,        # index 0
    delay_norm,             # index 1
    loss_norm,              # index 2
    congestion_indicator,   # index 3
    prev_action_norm,       # index 4
]
```

### 欄位規格

#### Index 0：`throughput_norm`

| 屬性 | 說明 |
|------|------|
| **語意** | 當前 decision step 內的 sender→receiver goodput，歸一化後的值 |
| **預期來源** | FlowMonitor `rxBytes` / step duration，再除以 link bandwidth 上限 |
| **Normalization** | `throughput_norm = throughput_mbps / link_bw_mbps`，bounded to [0, 1] |
| **MVP status** | **Required** |
| **Fallback** | 若 FlowMonitor rxBytes 無法在 step 粒度取得，使用 step 期間的平均 goodput estimate |

#### Index 1：`delay_norm`

| 屬性 | 說明 |
|------|------|
| **語意** | 當前 step 的 average packet delay / RTT 估計，歸一化後的值 |
| **預期來源** | FlowMonitor `delaySum / rxPackets`（mean one-way delay；非直接 RTT） |
| **Normalization** | `delay_norm = avg_delay_ms / max_expected_delay_ms`，bounded to [0, 1] |
| **MVP status** | **Required** |
| **Fallback** | 若無法取得 delaySum，使用 ASCII trace 中的 delay-related 欄位；在 info dict 中標記為 `estimated_delay` |

#### Index 2：`loss_norm`

| 屬性 | 說明 |
|------|------|
| **語意** | 當前 step 的 packet loss rate |
| **預期來源** | `(txPackets - rxPackets) / txPackets`（若有 drop 統計則優先使用）|
| **Normalization** | 自然有界於 [0, 1]，無需額外歸一化 |
| **MVP status** | **Required** |
| **Fallback** | 若無法取得 drop 統計，使用 `(txPackets - rxPackets) / txPackets` 估算 |

#### Index 3：`congestion_indicator`

| 屬性 | 說明 |
|------|------|
| **語意** | 壅塞程度的複合指示，[0, 1] 範圍，值越大代表壅塞越嚴重 |
| **預期來源** | 由 `loss_norm` 與 `delay_norm` 推導（e.g., `0.5 * loss_norm + 0.5 * delay_norm`，具體公式在 Change 04 中定義）|
| **Normalization** | 由構成元素的 normalization 保證 [0, 1] |
| **MVP status** | **Required** |
| **Fallback** | 若計算複雜度過高，可使用 `loss_norm` 的二元版本（loss > threshold → 1，否則 0）作為簡化版 |

#### Index 4：`prev_action_norm`

| 屬性 | 說明 |
|------|------|
| **語意** | 上一個 step 中 agent 採取的 action，歸一化為連續值 |
| **預期來源** | Agent 自身記錄（不需要 ns-3 提供）|
| **Normalization** | `{0: decrease → 0.0, 1: keep → 0.5, 2: increase → 1.0}` |
| **MVP status** | **Should-have** |
| **Fallback** | 若在 ns3-gym interface 設計上有困難，可在 smoke test 後決定是否保留；若省略，observation shape 降為 [4] |

> ⚠️ **若 `prev_action_norm` 最終被省略**，必須在 Change 04 開始前向 Spec Owner 回報，並更新本 spec。

---

## Enhanced Observation（Future Extension Only）

以下欄位**不在 MVP scope 內**，不得阻塞 MVP 的完成：

| 欄位名稱 | 語意 | 來源 | 狀態 |
|---------|------|------|------|
| `queue_occupancy` | 瓶頸 router 佇列使用率 [0, 1] | ns-3 queue trace | Future extension |
| `delay_gradient` | delay 對時間的一階導數（delay 趨勢）| 由連續 delay 值計算 | Future extension |
| `throughput_ma` | Throughput 移動平均（smoothed）| 由多個 step 的 throughput 計算 | Future extension |
| `estimated_bw` | 估計的瓶頸可用頻寬 | Throughput + delay estimation | Future extension |
| `cross_traffic_indicator` | Background traffic 強度指示 | 需要 cross traffic trace | Future extension |
| `ack_interarrival` | ACK 到達間隔（BBR-style signal）| ns-3 ACK trace | Future extension |

> ⛔ Enhanced observation 需要另開 OpenSpec change 並獲 Spec Owner 批准，不得在 Change 04 中自行加入。

---

## Normalization Rules

所有 observation 欄位必須遵守以下規則：

1. **All observations MUST be numeric** — 不得使用字串、布林或 None 作為 observation 欄位值
2. **All observations MUST be normalizable** — 所有欄位必須有明確的歸一化公式或自然有界範圍
3. **Feature order MUST be documented** — observation vector 中每個 index 對應的欄位必須在 Change 04 實作中明確記錄
4. **Values MUST be bounded or scaled** — 所有欄位值必須 bounded to [0, 1] 或其他明確範圍；不得有 unbounded 欄位
5. **Normalization formula MUST be consistent** — 同一欄位在 training 與 evaluation 時必須使用相同的 normalization formula

---

## Fallback Rules

| 情境 | Fallback 處理方式 |
|------|-----------------|
| RTT trace 無法從 FlowMonitor 直接取得 | 使用 `delaySum / rxPackets` 作為 mean one-way delay estimate；在 info dict 中標記為 `delay_estimate_method: "delaySum_per_packet"` |
| Queue occupancy 無法取得（MVP）| 不加入 MVP observation；使用 `delay_norm` 作為壅塞代理信號 |
| Estimated bandwidth 無法取得（MVP）| 不加入 MVP observation；此欄位為 future extension |
| `prev_action_norm` 在 ns3-gym interface 有困難 | 在 smoke test 階段確認可行性；若不可行，observation shape 降為 [4]，並回報 Spec Owner |
| 任何欄位值超出 [0, 1] 範圍 | 使用 `clip(value, 0, 1)` 強制裁切，並在 info dict 中記錄 `clipped: true` |
