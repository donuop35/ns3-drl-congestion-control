## Context

本 change 是 Change 01 project-charter 的直接下游。根據 Change 01 凍結的技術路線：

- **Simulator**: **ns-3.40**（正式凍結，Spec Owner 决策 OQ-02.01, 2026-06-08）
  > ⚠️ 不得自行改用 ns-3.35、3.36 或最新穩定版。若 ns-3.40 無法穩定執行，必須停止並回報 Spec Owner。
  > 理由：ns3-gym 官方 README 直接示範使用 ns-allinone-3.40，搭配 app-ns-3.36+ branch；因此 ns-3.40 比最新穩定版更適合本專案的低風險路徑。
- **Baselines**: NewReno（required）、CUBIC（required）、BBR（strongly preferred, non-blocking）
- **Metrics**: throughput、RTT、packet loss rate、utility score（provisional）
- **Topology**: single bottleneck path（合理的 ns-3 router-based bottleneck topology 亦允許）
- **Scenarios**: Scenario A（低延遲）、Scenario B（高延遲）

目前 `src/ns3/`、`experiments/configs/`、`experiments/results/` 目錄已建立但為空。本 change 的任務是填充這些目錄，讓 baseline benchmark 可以重現執行。

**環境限制**：ns-3 必須在 Linux/WSL2（Ubuntu 20.04+）環境執行；所有 ns-3 相關腳本必須在該環境開發與驗證。

---

## Goals / Non-Goals

**Goals（本 change 必須完成）：**

- 在 ns-3 中建立 single bottleneck link topology（可配置）
- 執行 TCP NewReno baseline（Scenario A + B），產出 CSV log
- 執行 TCP CUBIC baseline（Scenario A + B），產出 CSV log
- 若 ns-3 >= 3.32 支援 BBR，執行 BBR baseline；否則文件說明並移至 optional
- 建立 YAML/JSON 格式的實驗設定檔（含 random seed）
- 撰寫 Python 腳本解析 ns-3 log 為 CSV（throughput / RTT / loss）
- 生成至少 3 張 baseline 比較圖（throughput、RTT、packet loss）
- 更新 README 的 baseline 執行指令

**Non-Goals（本 change 明確不做）：**

- ❌ 安裝或使用 ns3-gym（留到 Change 03）
- ❌ 建立 RL environment 或 Gym interface（留到 Change 03）
- ❌ 訓練任何 DRL agent（留到 Change 04）
- ❌ 評估 DRL vs baseline 的比較（留到 Change 05）
- ❌ BBR 整合若成本 > 1 個工作日，移至 optional（不得阻塞）
- ❌ Multi-bottleneck、multi-path、multi-sender/receiver 拓樸

---

## Decisions

### D-01: Topology Implementation Style

**Decision**: 使用 ns-3 PointToPoint 鏈路建立 bottleneck，可選用中間 router node 作為瓶頸節點。  
**Options considered**:
- Option A: Direct sender → receiver PointToPoint（最簡單）
- Option B: sender → router → receiver（更接近真實 topology，router 即為瓶頸）

**Chosen**: Option B（router-based），符合 Change 01 DR-01 規定的「合理 ns-3 router-based bottleneck topology」。  
**Rationale**: Router-based topology 讓瓶頸控制更清晰，且 ns3-gym 整合通常在 router 上加裝感應器，便於 Change 03 銜接。

### D-02: ns-3 Script Language

**Decision**: 優先使用 ns-3 C++ script（.cc 副檔名），放在 `src/ns3/`。  
**Rationale**: ns-3 官方範例大多以 C++ 為主，性能最佳，documentation 最完整。Python binding 可作為後選，若 C++ 開發遇到環境問題再轉換。  
**Fallback**: 若 C++ 編譯環境問題無法在 1 個工作日解決，改用 ns-3 Python binding（`waf` build 仍需，但 script 改 .py）。

### D-03: Metric Collection Method

**Decision**: 使用 ns-3 `FlowMonitor` 模組收集每個 flow 的 throughput / RTT / packet loss 統計；補充使用 `ns3::TracedValue` 追蹤 cwnd 隨時間變化（為 Change 03 預做準備）。  
**Rationale**: FlowMonitor 是 ns-3 官方支援的高層統計 API，輸出穩定且可直接解析。  
**Fallback**: 若 FlowMonitor 輸出格式有問題，改用 ASCII tracing + Python 後處理。

### D-04: BBR Integration Decision Gate

**Decision**: 在開始 Change 02 implementation 時，先確認 **ns-3.40** BBR module 是否可用。若可用且整合成本 <= 0.5 工作日，則納入 BBR baseline；否則以「non-blocking optional」記錄並跳過。  
**Rationale**: BBR 是 strongly preferred（非 required）；不得讓 BBR 阻塞 NewReno/CUBIC 的基礎交付。  
**ns-3 version**: 目標版本為 **ns-3.40**（Spec Owner 正式凍結）；不得自行改用其他版本。

### D-05: Experiment Config Format

**Decision**: 使用 YAML 格式的實驗設定檔，存於 `experiments/configs/scenario_a.yaml` 等。  
**Rationale**: YAML 人類可讀、Python 易解析（`pyyaml`）；後續 Change 03/04 的 RL experiment config 可沿用相同格式。  
**Config fields**: `link_bandwidth`, `link_delay`, `queue_size`, `sim_duration`, `random_seed`, `tcp_algorithm`（list）, `scenario_name`

### D-06: Python Analysis Script Structure

**Decision**: 撰寫 `src/analysis/parse_baseline.py` 和 `src/analysis/plot_baseline.py`。  
**Rationale**: 分離 parsing 和 plotting 邏輯，便於 Change 05 復用 plotting 腳本產生 DRL vs baseline 比較圖。

---

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| ns-3 安裝失敗或環境問題（WSL/Ubuntu） | 先跑 `examples/tutorial/first.cc`；確認基本 ns-3 功能後再做 bottleneck topology |
| BBR module 在目標 ns-3 版本不可用 | 確認 ns-3 版本 >= 3.32；若不可用，以 Non-blocking optional 記錄，繼續做 NewReno/CUBIC |
| FlowMonitor 輸出解析困難 | 預先研究 FlowMonitor XML output 格式；準備 fallback ASCII tracing |
| ns-3 C++ 編譯時間過長 | 只編譯所需模組（`--enable-modules`）；允許使用 Python binding 作為 fallback |
| Scenario 參數設定導致 unrealistic 結果（throughput = 0 或 loss = 100%）| 先以小規模（5 Mbps, 10s）測試 topology 是否正常，再設定正式情境參數 |
| Node.js v20.11.1 < 20.19.0 | OpenSpec CLI 目前功能正常；若升級到 20.19.0+ 則在此 change 前或 change implementation 前完成 |

---

## Open Questions

| # | 問題 | 影響 | 决策時間 |
|---|------|------|---------|
| OQ-02.01 | ns-3 目標版本？ | 高 | ✅ **Spec Owner 正式决策 2026-06-08**：使用 **ns-3.40**。理由：ns3-gym 官方 README 直接示範使用 ns-allinone-3.40，搭配 app-ns-3.36+ branch；這是本專案的低風險路徑。 |
| OQ-02.02 | ns3-gym 與哪個 ns-3 版本相容？（需要 Change 03 銅接規劃）| 中 | ✅ 不阻塞 change-02，ns3-gym 與 ns-3.40 相容性留到 change-03 為第一步驗證 |
| OQ-02.03 | ns-3 C++ script 還是 Python binding？（D-02 已有 default，但視環境而定）| 低 | ⏳ Change 02 implementation 開始時確認 |
| OQ-02.04 | Scenario 參數是否需要更多情境？（目前 A + B + optional C）| 低 | ⏳ 可在 implementation 中調整，不需 spec owner 另外批准 |
