# Final Figures QA Report

## 1. 總結
本報告紀錄 Claude Model 接手 Gemini 產出之 Phase 5 交付物後，針對 final figures 所做的完整 QA 審核與修正。共發現並修正了 4 類圖表品質問題：空圖（scenario ID 大小寫不匹配）、baseline 圖缺少 method 標示、action distribution y-axis 尺度錯誤、以及 conceptual diagrams 品質過低。修正後所有 9 張 required figures 皆通過 QA 驗證。

## 2. Gemini Phase 5 Deliverables Audit
Claude 完整審查了以下 Gemini 產出物：
- `scripts/phase5/generate_final_figures.py`：發現 scenario ID 使用小寫 `s1`/`s2`，但 CSV 內為大寫 `S1`/`S2`，導致 DataFrame 過濾結果為空。
- `figures/final/*.png`：9 張圖中有 2 張空圖、1 張 y-axis 標示錯誤、4 張 conceptual diagrams 僅為文字框。
- `reports/final/final-figure-source-map.md`：需要因圖表重製而更新。
- `reports/final/final-artifact-manifest.md`：缺少 validation script 與部分 figure 條目。

## 3. Identified Figure Issues

### 3.1 `dqn_vs_baseline_utility_s1_s2.png` — 空圖
- **原因**：`generate_final_figures.py` 用 `'s1'`/`'s2'` 過濾，但 CSV 中 `scenario_id` 為 `'S1'`/`'S2'`。
- **影響**：圖表完全沒有 bar，只有空白座標軸。

### 3.2 `dqn_vs_baseline_loss_s1_s2.png` — 空圖
- **原因**：同上，scenario ID 大小寫不匹配。

### 3.3 `baseline_utility_summary.png` — 缺少 method 標示
- **原因**：原版使用 `set_index('scenario_id')` 後的簡單 bar chart，x-axis 只顯示重複的 S1/S2/S3/S4，無法辨識 NewReno/CUBIC/BBR。
- **影響**：讀者無法判讀各 bar 代表哪個 TCP 變體。且包含了 final report 不需要的 S3/S4 數據。

### 3.4 `dqn_action_distribution_s1_s2.png` — y-axis 尺度錯誤
- **原因**：原版 y-axis 標示 `Percentage (%)`，但資料值為 0–1 的 proportion（非百分比）。且 x-axis 標籤因旋轉變形顯示為 `t5`/`z5`。

### 3.5 Conceptual diagrams — 品質過低
- `system_pipeline.png`、`single_bottleneck_topology.png`、`mdp_formulation.png`、`key_findings_summary.png` 皆僅為灰色圓角矩形包裹純文字，不適合放入正式報告或簡報。

## 4. Fixes Applied

### 4.1 Scenario ID 修正
- 移除小寫 `s1`/`s2` 過濾，改為直接使用 CSV 中的大寫 `S1`/`S2`。
- 新增 fail-fast 檢查：若指定 scenario 在 DataFrame 中找不到任何列，立即 `sys.exit(1)`。

### 4.2 Baseline utility 升級為 grouped bar
- 只篩選 S1/S2。
- 使用 method 分組 (NewReno/CUBIC/BBR)，每個 scenario 內並排顯示。
- 對 BBR S2 anomaly 的負值加上紅字 annotation。

### 4.3 Action distribution 轉換為百分比
- 將 proportion (0–1) 乘以 100 後繪圖。
- y-axis 改為 `Action Share (%)`，範圍 0–110。
- 加上 S1 degenerate policy annotation。

### 4.4 Conceptual diagrams 全面升級
- `system_pipeline.png`：改為 6 層彩色 flow diagram，含箭頭連接。
- `single_bottleneck_topology.png`：改為 node-link diagram，含圓形節點與標示 delay scenario。
- `mdp_formulation.png`：改為 MDP loop diagram，含 Observation → Agent → Action → Environment 及 Reward 回饋箭頭。
- `key_findings_summary.png`：改為 2×2 彩色 insight cards。

### 4.5 Method label mapping
- 新增 `METHOD_LABELS` 字典，將 `ns3::TcpLinuxReno` 等映射為 `NewReno` 等 display label。
- 統一所有圖表的 method 名稱顯示。

### 4.6 Fail-fast 與 verify 機制
- `check_file()` 對 required files 執行 fail-fast。
- `verify_not_empty()` 確認產出檔案存在且不小於 1000 bytes。

## 5. Source Data Used
以下凍結 CSV 作為唯一數據來源（未修改）：
- `experiments/summaries/baseline_summary.csv`
- `experiments/drl/summaries/dqn_vs_baseline_summary.csv`
- `experiments/drl/summaries/dqn_action_distribution_summary.csv`

## 6. Regenerated Figures
所有 9 張 required figures 已重新產生：

| Figure | Size | Dimensions | Status |
|--------|------|------------|--------|
| `baseline_utility_summary.png` | 32,543 | 1200×750 | PASS |
| `dqn_vs_baseline_utility_s1_s2.png` | 44,028 | 1800×750 | PASS |
| `dqn_vs_baseline_loss_s1_s2.png` | 39,675 | 1800×750 | PASS |
| `dqn_action_distribution_s1_s2.png` | 36,716 | 1050×750 | PASS |
| `dqn_reward_curves_s1_s2.png` | 117,918 | 3000×600 | PASS |
| `system_pipeline.png` | 80,960 | 1500×1200 | PASS |
| `single_bottleneck_topology.png` | 61,776 | 1500×600 | PASS |
| `mdp_formulation.png` | 57,493 | 1200×1050 | PASS |
| `key_findings_summary.png` | 83,371 | 1500×900 | PASS |

## 7. Figure Validation Results
`validate_final_figures.py` 執行結果：QA RESULT: ALL PASS（9/9 通過）。

## 8. Documents Updated
- `scripts/phase5/generate_final_figures.py`：完整重寫。
- `scripts/phase5/validate_final_figures.py`：新增。
- `reports/final/final-figure-source-map.md`：自動更新。
- `reports/final/final-artifact-manifest.md`：補齊圖表與腳本條目。
- `openspec/changes/reporting-figures-and-demo/tasks.md`：新增 Section 11。

## 9. No-Go Compliance
- [x] 沒有重訓 DQN
- [x] 沒有重跑 baseline
- [x] 沒有修改 CSV
- [x] 沒有修改 model artifacts
- [x] 沒有 fake data
- [x] 沒有 fake figures
- [x] 沒有新增 PPO / IPFS / QUIC / multi-agent / multi-path
- [x] 沒有把 delay proxy 寫成 true RTT
- [x] 沒有把 rate abstraction 寫成 kernel-level cwnd control
- [x] 沒有宣稱 DQN 全面勝過 TCP
- [x] 沒有進入 Phase 7

## 10. Remaining Items
- `tasks.md` 中 `11.10 Wait for Spec Owner final figures QA review` 維持未勾選。

## 11. Ready for Spec Owner Final Figures QA Review
所有 9 張 required final figures 已通過 QA 驗證，品質達高分展示水準。等待 Spec Owner 審核放行。
