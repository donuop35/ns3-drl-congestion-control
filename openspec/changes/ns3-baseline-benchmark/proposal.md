## Why

在正式訓練 DRL agent 之前，必須先建立可重現的 TCP baseline benchmark，作為後續 DRL 性能比較的參照基準。若沒有可信的 baseline 數據，DRL agent 的評估結果將缺乏比較基礎，無法判斷其壅塞控制策略是否有意義。本 change 的目標是在不碰任何 RL 程式碼的前提下，使用 ns-3 建立 single bottleneck link topology，並跑通 NewReno、CUBIC（+ BBR）baseline benchmark，產出可複現的 CSV log 與比較圖表。

**Upstream Reference**: 本 change 依據 Change 01 project-charter（已通過 Spec Owner 驗收，2026-06-08）中凍結的 baseline 選擇（NewReno/CUBIC/BBR）、metrics（throughput/RTT/loss/utility）與 topology 邊界（single bottleneck path）。

> 🔒 **ns-3 版本正式凍結（Spec Owner 决策 OQ-02.01, 2026-06-08）**: 本 change 使用 **ns-3.40** 作為目標版本。不得自行改用 ns-3.35、3.36 或最新穩定版。若 ns-3.40 無法穩定執行，必須停止並回報 Spec Owner。

## What Changes

本 change 新增以下功能（僅限 ns-3 baseline 相關，不含任何 RL 程式碼）：

- **ns-3 single bottleneck topology**：建立可配置的 `sender → (optional router) → receiver` topology，router 即為瓶頸節點；**目標版本凍結為 ns-3.40**
- **TCP baseline scripts**：ns-3 C++ 或 Python 腳本，執行 NewReno 和 CUBIC baseline；BBR 若 ns-3.40 版本支援則納入
- **Experiment configs**：`experiments/configs/scenario_a.yaml` 和 `scenario_b.yaml`（含固定 random seed）
- **Log parsing scripts**：從 ns-3 輸出提取 throughput / RTT / packet loss CSV
- **Baseline figures**：throughput comparison、RTT comparison、packet loss comparison 各一張
- **Baseline summary table**：各演算法各情境的 average throughput / RTT / loss / utility score

## Capabilities

### New Capabilities

- `ns3-topology`: ns-3 single bottleneck link topology 建立與參數配置（bandwidth、delay、queue size）
- `tcp-baseline`: TCP 壅塞控制演算法（NewReno、CUBIC、可選 BBR）在 bottleneck topology 下的 benchmark 執行
- `baseline-logging`: 從 ns-3 simulation 提取 throughput / RTT / packet loss 至 CSV 格式
- `baseline-figures`: 以 Python/matplotlib 產生 baseline 比較圖表（throughput、RTT、loss、utility）
- `experiment-configs`: YAML/JSON 格式的實驗情境設定檔（含 random seed、link 參數）

### Modified Capabilities

<!-- 無既有 spec 需要修改；本 change 建立全新能力 -->

## Impact

- **新增檔案**：`src/ns3/` 下的 topology + baseline 腳本、`experiments/configs/` 的情境設定、`experiments/results/` 的 CSV 輸出、`figures/` 的比較圖表
- **依賴安裝**（需在 Linux/WSL 環境）：ns-3（>= 3.32）、Python 3.9+、numpy、pandas、matplotlib
- **不影響**：任何 RL 相關程式碼（ns3-gym、Stable-Baselines3、DQN agent）
- **下游影響**：Change 03（ns3gym-environment）將使用本 change 建立的 topology 作為 RL environment 的基礎；Change 04/05 將使用本 change 的 CSV 結果作為 DRL vs baseline 比較的依據

## Dependencies

- ✅ Change 01 project-charter（已通過 Spec Owner 驗收）
- **ns-3.40**（正式凍結，不得自行改版）安裝於 Linux/WSL 環境（待驗證）
- BBR 模組可用性（ns-3.40 需確認；若不可用移至 optional）
- Python 3.9+ + numpy + pandas + matplotlib

## Acceptance Criteria

- [ ] ns-3.40 single bottleneck topology 可正確建立（至少 PointToPoint bottleneck 或 router-based 等效）
- [ ] TCP NewReno baseline 可在 Scenario A 和 Scenario B 執行完成並產出 log
- [ ] TCP CUBIC baseline 可在 Scenario A 和 Scenario B 執行完成並產出 log
- [ ] BBR baseline 執行成功，或有明確文件說明為何移至 optional
- [ ] `experiments/configs/scenario_a.yaml` 和 `scenario_b.yaml` 存在並含 random seed
- [ ] `experiments/results/` 含至少一份 CSV（throughput / RTT / loss 欄位）
- [ ] 至少 3 張 baseline 比較圖：throughput、RTT、packet loss
- [ ] README 有可執行的 baseline 重現指令
- [ ] 相同情境下使用相同 random seed，產出的量化指標（throughput / RTT / loss）應在文件記錄的容差範圍內相符（metric-equivalent within documented tolerance；不要求 FlowMonitor XML byte-for-byte identical）
- [ ] **utility_score 僅作為 baseline visualization metric（preliminary / provisional）**：公式與權重為 preliminary，最終 reward / utility 權重可於 Change 04 / Change 05 經 Spec Owner approval 後調整
- [ ] **不包含任何 RL / ns3-gym / DQN 相關程式碼**
- [ ] Spec Owner 驗收通過，才啟動 Change 03
