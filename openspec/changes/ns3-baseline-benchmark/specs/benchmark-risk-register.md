## Purpose

管理 Change 02 ns3-baseline-benchmark 階段的實作風險，並為每個風險定義觸發條件與 fallback 處理。

---

## Risk Register

### R-02-01：ns-3 TCP algorithm name / version mismatch

| 屬性 | 說明 |
|------|------|
| **Trigger** | ns-3.40 內的 class name 與文件/範例不符（e.g., `TcpNewReno` vs `TcpLinuxReno`） |
| **Impact** | 高：baseline 無法正確執行 |
| **Mitigation** | 先執行 ns-3.40 內建 TCP examples 確認 class name；若不符，查 ns-3.40 `src/internet/model/tcp-*.h` 確認正確名稱 |
| **Fallback** | 以 ns-3.40 原始碼中確認的 class name 為準，不以文件猜測 |

### R-02-02：BBR availability issue in ns-3.40

| 屬性 | 說明 |
|------|------|
| **Trigger** | ns-3.40 中 `TcpBbr` class 不存在或不穩定 |
| **Impact** | 低：BBR 是 non-blocking；不影響 NewReno/CUBIC MVP |
| **Mitigation** | 在 implementation 開始前先確認 `TcpBbr` 可用性（D-04 decision gate） |
| **Fallback** | 創建 `experiments/results/BBR_SKIPPED.md`，記錄原因，繼續 MVP |

### R-02-03：FlowMonitor / logging cannot directly provide RTT or loss

| 屬性 | 說明 |
|------|------|
| **Trigger** | FlowMonitor XML 中無法直接讀取 RTT 欄位，或 loss 需要從 txPackets/rxPackets 推算 |
| **Impact** | 中：metrics 計算需要額外文件說明 |
| **Mitigation** | 使用 `delaySum / rxPackets` 作為 RTT 估計；使用 `(txPackets - rxPackets) / txPackets` 計算 loss；在 metadata 中記錄公式 |
| **Fallback** | 改用 ASCII trace + Python 後處理；在 spec 中記錄 ambiguity 處理方式 |

### R-02-04：Throughput calculation inconsistency

| 屬性 | 說明 |
|------|------|
| **Trigger** | 不同 baselines 的 throughput 計算方式不一致（e.g., goodput vs. link throughput） |
| **Impact** | 高：使比較結果失去公正性 |
| **Mitigation** | 統一使用 FlowMonitor 的 `rxBytes / simDuration` 作為 goodput；所有 baselines 使用相同公式 |
| **Fallback** | 在 metrics-logging.md 中明確記錄公式，並在所有 CSV 中加入計算方式欄位 |

### R-02-05：Scenario design too complex

| 屬性 | 說明 |
|------|------|
| **Trigger** | S3/S4 scenario 導致 topology 設計過於複雜，影響 MVP 交付時間 |
| **Impact** | 中：可能延遲 Change 02 完成 |
| **Mitigation** | S1/S2 先完成後，再考慮 S3/S4 |
| **Fallback** | S3/S4 降至 future work，不阻塞 MVP |

### R-02-06：Cross traffic makes MVP unstable

| 屬性 | 說明 |
|------|------|
| **Trigger** | S4 的 background flows 導致主 flow 結果不穩定、不可重現 |
| **Impact** | 中：S4 結果不可信 |
| **Mitigation** | 先在小規模 cross traffic（1 background flow）測試穩定性 |
| **Fallback** | S4 完全降至 optional / future work |

### R-02-07：Abnormal baseline result cannot be explained

| 屬性 | 說明 |
|------|------|
| **Trigger** | Throughput 接近 0 或 loss rate 接近 100%，但 topology 設定看起來正確 |
| **Impact** | 高：baseline 不可用 |
| **Mitigation** | 先以小規模（5 Mbps, 10s, seed=42）測試 topology 基本正確性；確認封包可達到 receiver |
| **Fallback** | 回報 Spec Owner，停止並重新檢查 topology 設計 |

### R-02-08：Antigravity jumps directly to DRL

| 屬性 | 說明 |
|------|------|
| **Trigger** | Antigravity 在 Change 02 未完成前開始撰寫 ns3-gym / DQN 相關程式碼 |
| **Impact** | 極高：違反 governance rules，Change 02 視為失敗 |
| **Mitigation** | 嚴格遵守 Non-Goals 列表；Change 02 僅允許 ns-3 baseline 相關工作 |
| **Fallback** | 立即停止，刪除 RL 相關程式碼，回報 Spec Owner |
| **⚠️ 強制規則** | 觸發此風險時，Antigravity 必須立即停止所有工作並回報，不得自行繼續 |

### R-02-09：Baseline figures insufficient for PPT / report

| 屬性 | 說明 |
|------|------|
| **Trigger** | 生成的圖表解析度過低、缺少標注、或視覺品質不符合學術報告標準 |
| **Impact** | 低（功能不影響，只影響呈現） |
| **Mitigation** | 所有圖表 >= 150 DPI；統一 color scheme；標記所有 axes 和 legend |
| **Fallback** | 在 Change 05 中補充更高品質圖表 |

### R-02-10：Pantheon mistaken as required tool

| 屬性 | 說明 |
|------|------|
| **Trigger** | 誤認為需要安裝 Pantheon 才能執行 baseline benchmark |
| **Impact** | 中：Pantheon 安裝複雜，會阻塞 MVP |
| **Mitigation** | 明確記錄：本 change 僅使用 ns-3.40 內建 TCP 模型；Pantheon 僅作為 benchmark 哲學參考，不作為依賴 |
| **Fallback** | 不安裝 Pantheon；若需要其 benchmark methodology，僅引用其 paper |

### R-02-11：Fake OpenSpec / simulated SDD workflow used

| 屬性 | 說明 |
|------|------|
| **Trigger** | 使用非官方 `@fission-ai/openspec` 的流程、自行模擬 SDD 或假 OpenSpec 資料夾 |
| **Impact** | 極高：本專案整體 governance 失效，所有 artifacts 無效 |
| **Mitigation** | 每次 change 開始前必須確認 `openspec --version` 輸出正確版本，且 `.agent/skills/` 和 `.agent/workflows/` 均由官方 CLI 產生 |
| **Fallback** | 立即停止，重新安裝官方 `@fission-ai/openspec@latest`，重新初始化 |
| **⚠️ 強制規則** | 發現任何假 OpenSpec 使用，必須立即停止並回報 Spec Owner，不得繼續任何 change |

---

## Fallback Principles

1. **NewReno + CUBIC = MVP 最低交付**，任何 risk 都不得阻塞此目標
2. **BBR non-blocking**：BBR 不可用時，以 `BBR_SKIPPED.md` 記錄並繼續
3. **S1 / S2 = 最低 scenario 交付**：S3/S4 為 optional
4. **Reproducibility tolerance**：相同 seed 下，metric 差異在 ±1% 以內視為 equivalent（具體 tolerance 在 metadata 中記錄）
5. **No fake OpenSpec**：任何假 OpenSpec 使用都是整個 change 的 critical failure
6. **No DRL before baseline approval**：在 Spec Owner 驗收 Change 02 前，不得開始 Change 03/04
