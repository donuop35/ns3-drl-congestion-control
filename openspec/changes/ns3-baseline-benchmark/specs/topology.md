## Purpose

定義 Change 02 baseline benchmark 使用的 ns-3 single bottleneck network topology 規格。

---

## Minimal Topology（MVP-required）

MVP 僅限以下結構：

```
Sender ──[Access Link]──> Router ──[Bottleneck Link]──> Receiver
```

| 節點 | 數量 | 說明 |
|------|------|------|
| Sender | 1 | 傳送端，執行 TCP flow |
| Router | 1 | 中間節點，作為瓶頸（選用，可省略） |
| Receiver | 1 | 接收端，TCP sink |

**Bottleneck Link** 為限制整體 throughput 的鏈路，必須可配置：

| 參數 | 說明 | 型別 |
|------|------|------|
| `link_bandwidth` | 瓶頸鏈路頻寬（Mbps） | 整數 |
| `link_delay` | 瓶頸傳播延遲（e.g., `"10ms"`） | 字串 |
| `queue_size` | 瓶頸佇列大小（封包數） | 整數 |
| `queue_discipline` | 佇列紀律（DropTail 為預設） | 字串 |

Access Links（sender ↔ router, router ↔ receiver 端）使用比瓶頸高 5–10 倍的頻寬，確保瓶頸在 bottleneck link 上。

---

## Topology Diagram

```
           10× BW                Bottleneck BW
Sender ─────────────── Router ─────────────────── Receiver
         low delay              configurable delay
        (access link)           (bottleneck link)
```

> **ns-3 實作方式**：使用 `PointToPointHelper` 配置各段鏈路。Router node 可以是 `Node`，不需要複雜路由配置（point-to-point 自動路由即可）。

---

## Enhanced Topology（Optional，不得阻塞 MVP）

以下增強 topology 在 MVP 完成後方可考慮（需 Spec Owner 批准）：

| 增強項目 | 說明 | 優先序 |
|---------|------|------|
| Variable bandwidth | 瓶頸頻寬隨時間變化 | Should-have |
| High-delay path | 極高延遲（模擬衛星/洲際鏈路） | Should-have |
| Cross traffic | 額外 background flows 競爭瓶頸 | Optional |
| Multiple flows | 多個 TCP flow 同時競爭 | Optional |

---

## Non-Goals

以下絕對不得出現在本 change 的 topology 設計中：

> ⛔ **Large-scale topology** — 超出 single bottleneck path 所需  
> ⛔ **Multi-bottleneck topology** — MVP 只有一個瓶頸  
> ⛔ **Multi-path routing / ECMP** — 超出 single bottleneck path  
> ⛔ **Multiple sender/receiver groups** — 超出 single flow 設定  
> ⛔ **IPFS overlay network** — 不在 scope 內  
> ⛔ **QUIC transport** — 不在 scope 內  
> ⛔ **Multi-agent topology** — 不在 scope 內

---

## ns-3 Implementation Constraints

- **Target version**: ns-3.40（Spec Owner 正式凍結）
- **Allowed**: 合理的 ns-3 `PointToPointHelper` + router node 作為瓶頸的實作
- **Random seed**: 必須使用 `RngSeedManager::SetSeed(seed)` 固定；每次 run 必須記錄使用的 seed
- **Reproducibility**: 相同 config + 相同 seed 應產出 metric-equivalent 結果（within documented tolerance）
