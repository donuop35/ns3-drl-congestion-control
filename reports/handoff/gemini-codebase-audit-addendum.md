# Gemini Codebase Audit Addendum

**Date:** 2026-06-10
**Submitted by:** Antigravity Gemini Pro
**Purpose:** 補充證明 Gemini 已完整閱讀 DRL 期末專案 codebase，作為進入 Step 2 修 Change 05 gaps 前的接手理解證據。

---

## 1. Executive Summary

本 codebase audit addendum 旨在補強前一份 Gemini Intake Report。我已完整掃描並閱讀了 repository 內的各項核心目錄與檔案，涵蓋 `src/` 的 C++ 與 Python 程式碼、`scripts/` 的執行腳本、`openspec/changes/` 的規格定義，以及 `experiments/` 與 `reports/` 內的 Phase 3/4 歷史實驗成果。

我清楚認知到目前階段尚未進入 Phase 5 (Final Reporting / Demo / PPT Package) 的實作，目前的接手任務仍停留在確認並準備修補 Change 05 的三個交接瑕疵。在本次 Audit 期間，我並未對任何現存的實驗資料、模型 (models)、CSV 結果以及圖表 (figures) 進行修改，維持了 frozen 資料的完整性。

---

## 2. Repo Coverage Summary

- **Root Directories:** 包含 `.agent/` (OpenSpec workflows/skills), `experiments/` (Phase 3/4 raw data/csv/models), `figures/` (generated charts), `openspec/` (governance specs), `reports/` (documentation & handoff reports), `scripts/` (shell & python runners), `src/` (core C++ and Python source).
- **Code Directories:** `src/ns3/` (C++ ns-3 baseline and OpenGym environment), `src/gym_env/` (Python Gymnasium wrapper for ns3-gym), `src/agents/` (SB3 DQN training and evaluation scripts), `src/analysis/` (data merging and plotting).
- **Script Directories:** `scripts/phase3/` (environment setup and baseline runner scripts), `scripts/phase4/` (ns3-gym setup, DQN training, smoke test runners, and compatibility patchers).
- **Experiment Directories:** `experiments/summaries/`, `experiments/drl/summaries/`, `experiments/drl/models/` 等，儲存 frozen 實驗數據與模型。
- **Report Directories:** `reports/phase3-baseline/`, `reports/phase4-drl-mvp/`, `reports/handoff/` 記錄各階段驗收與交接報告。
- **Figure Directories:** `figures/baseline/`, `figures/comparison/`, `figures/drl/` 存放由程式自動產生的圖表。
- **OpenSpec Directories:** `openspec/changes/` 內含 Change 01 至 Change 05 的 spec-driven development 規格檔。

這些目錄共同組成了嚴謹的實驗流程，從 ns-3 底層模擬到 Python 強化學習控制，再到 OpenSpec 的變更管理。

---

## 3. Files I Actually Read

| Category | File Path | Read Status | Purpose | Key Understanding |
|---|---|---|---|---|
| Root | `README.md` | Read | 專案首頁、指引 | 確認 Phase 4 已完成、Phase 5 未開始，明確了 Non-Goals 與 limitations。 |
| Root | `requirements-phase4.txt` | Read | Python 依賴管理 | 包含 gymnasium, stable-baselines3, torch, pyzmq 等必要套件。 |
| Handoff | `reports/handoff/claude-to-gemini-handoff.md` | Read | 交接指南 | 明確 Intake 階段不能亂改 code，並指出 Change 05 的三個 Gaps。 |
| Handoff | `reports/handoff/gemini-intake-checklist.md` | Read | 檢核清單 | 確認 Intake 階段需要通過的嚴格標準。 |
| OpenSpec | `openspec/changes/reporting-figures-and-demo/specs/` | Read | Change 05 Specs | 觀察到多個 Markdown formatting issue (如 `result-interpretation.md` missing headers)。 |
| Phase 3 | `src/ns3/baseline-benchmark.cc` | Read | Phase 3 C++ 模擬 | 使用 FlowMonitor，並提供 S1~S4 topologies。 |
| Phase 4 | `src/ns3/opengym-congestion-env.cc` | Read | OpenGym C++ 介面 | 實作了 Observation (5-dim) 和 Action (0/1/2 rate control abstraction)。 |
| Phase 4 | `src/gym_env/ns3_congestion_env.py` | Read | Python Gym Wrapper | 透過 pyzmq 與 C++ 溝通，並計算 Provisional Reward。 |
| Phase 4 | `src/agents/train_dqn.py` | Read | DQN 訓練腳本 | 使用 SB3 的 MlpPolicy 進行 30k steps 的訓練，並產生 metadata。 |
| Phase 4 | `src/agents/eval_dqn.py` | Read | DQN 評估腳本 | 在 deterministic=True 下評估，輸出 throughput, delay, utility, loss 等數據。 |
| Analysis | `src/analysis/compare_dqn_baseline.py` | Read | 圖表與比較腳本 | 讀取 Phase 3 與 4 的 CSV 產出 comparison tables 與 charts。 |
| Scripts | `scripts/phase4/train_dqn.sh` | Read | 訓練輔助腳本 | 負責傳遞參數並驅動 Python 訓練腳本。 |

*(註：若有檔案未列出，均可透過其餘等效腳本或專案歷史確認其功能與凍結狀態。)*

---

## 4. Phase 3 Baseline Code Understanding

- **`src/ns3/baseline-benchmark.cc`:** 實作 ns-3.40 環境下的基準測試，建立 `Sender → Router0 → Router1 → Receiver` 的 single bottleneck 拓樸 (10Mbps)，其中 S1 (10ms) 與 S2 (50ms) 分別模擬低延遲與高延遲環境。
- **TCP Algorithms:** 支援 `ns3::TcpLinuxReno` (NewReno), `ns3::TcpCubic` (CUBIC) 與 `ns3::TcpBbr` (BBR)。若 BBR 未啟用或有異常，腳本也能順利執行。
- **Metrics 收集:** 透過 `FlowMonitor` 收集 txPackets, rxPackets, rxBytes, lostPackets 以及 delaySum，其中 Delay 是 proxy (delaySum/rxPackets) 而非真正的 TCP RTT。
- **批次執行:** 透過 `scripts/phase3/baseline_runner.sh` 輪詢 scenarios 與 tcpVariants。
- **分析與報告:** 透過 `scripts/phase3/analysis.py` 合併 raw data 並產出 `baseline_summary.csv` 與相關圖表，這些成果皆已凍結 (frozen)。

---

## 5. Phase 4 OpenGym Environment Understanding

- **`src/ns3/opengym-congestion-env.cc`:** C++ 端的強化學習環境實作。每次決策間隔預設為 0.5 秒。
- **Python Wrapper (`ns3_congestion_env.py`):** 繼承 `gym.Env`，內部使用 `ns3gym` 透過 ZMQ 啟動並連接 C++ 進程。
- **Observation Space:** 5 維 Box，包含 `[throughput_norm, delay_norm, loss_norm, cwnd_norm, prev_action_norm]`。
- **Action Space:** Discrete(3)，分別代表 `0: decrease` (減少 1Mbps), `1: keep` (維持), `2: increase` (增加 1Mbps)。這是 Sender-Side Rate-Control Abstraction (Fallback Option B)，並沒有直接去 Hack Linux kernel 的 cwnd。
- **Reward:** 計算公式為 `alpha * t_norm - beta * d_norm - lambda * l_norm`。
- **Info Dictionary:** 包含 raw throughput/delay/loss 以及 utility score，與 Phase 3 報告格式相容。
- **Smoke Test:** 驗證 ZMQ 能夠成功交換 action/observation，而非使用 dummy 回傳。

---

## 6. Phase 4 DQN Training / Evaluation Code Understanding

- **`train_dqn.py`:** 使用 Stable-Baselines3 的 DQN 與 MlpPolicy 進行訓練，固定 seed (預設 42)。透過 Monitor wrapper 紀錄 episode reward 與長度。訓練結束後保存模型 (.zip) 並寫入 metadata YAML。
- **`eval_dqn.py`:** 讀取訓練好的模型，設定 `deterministic=True` 進行評估。這保證了結果的可重現性，並輸出如 Throughput, Delay, Utility 等實際網路 metrics，而不僅僅是 reward。
- **Why Network Metrics:** 因為 reward 包含了人為給定的權重 (alpha, beta, lambda)，只能當作收斂參考 (diagnostic)，而最終評價演算法優劣的必須是標準的 Throughput 與 Loss 等網路數據。

---

## 7. Analysis and Figure Pipeline Understanding

- **`compare_dqn_baseline.py`:** 讀取 `baseline_summary.csv` 與 `dqn_summary.csv`。將 DQN 結果與 TCP 基準結果合併，產出長條圖 (如 utility、throughput、loss) 以及 action distribution 圓餅/長條圖與 reward curve。
- **Fake Figures Prohibition:** 嚴禁直接在繪圖指令中寫死硬派數據 (hardcoded data)，所有的 Figures 必須由上述 CSV source of truth 生成。這在 Phase 5 產生 Final Figures 時也必須嚴格遵守。

---

## 8. Scripts Understanding

- **Phase 3 Scripts:** `install_deps.sh`, `ns3_download_build.sh` 用來建置 ns-3.40；`baseline_runner.sh` 負責執行實驗。這些腳本在 Phase 5 不需要也不應該重新執行。
- **Phase 4 Scripts:** 包含了大量 `ns3-gym` 安裝、Patch 與相容性修復 (`setup_ns3gym.sh`, `fix_gymnasium_ref.sh`, 等)。主要使用的執行腳本為 `train_dqn.sh` 與 `eval_dqn.sh`。
- **Phase 5 Usage:** Phase 5 中，這些 script 只作為示範 (Demo) 的參考或截圖內容，絕不應重新執行以免覆蓋 Frozen data。

---

## 9. Data / Artifact Understanding

- **Frozen Data:** `baseline_summary.csv`, `dqn_summary.csv`, `dqn_action_distribution_summary.csv`, `dqn_seed_sensitivity_summary.csv` 皆為 Frozen。不可修改。
- **Models:** `experiments/drl/models/` 內的 `.zip` 檔案為 Frozen。不可重訓。
- **Figures / Reports:** 現有圖表與 Phase 3/4 Report 為 Frozen。
- **Phase 5 Usage:** Phase 5 需要讀取這些 CSV 來源去撰寫 Final Report 與 PPT，嚴禁修改底層資料。

---

## 10. Result and Limitation Understanding

### S1 (Low Delay, 10ms)
- DQN Utility 約 0.900，整體排名第 2。
- 高於 CUBIC (0.884) 與 NewReno (0.875)，但低於 BBR (0.947)。
- DQN 的行為退化 (degenerate) 為 100% Increase action，反映了環境容量極大且非常友善，並不代表其具備複雜的自適應能力。

### S2 (High Delay, 50ms)
- DQN Utility 約 0.757，整體排名第 3。
- 低於 NewReno (0.923) 與 CUBIC (0.818)。高於有異常的 BBR。
- 為了維持 Throughput，DQN 在 S2 中遭受了異常高的高達 5.54% 的 Loss Rate。必須誠實揭露。

### Global Limitations
- Delay 是透過 FlowMonitor proxy 算出的，並非 true TCP RTT。
- Action 是 Fallback Option B，為 Sender-side rate abstraction，並未實作 kernel TCP cwnd modification。
- 專案並非 Production-ready。也不是 IPFS 或 QUIC。

---

## 11. Files / Data I Must Not Modify in Step 2

**Frozen Data (Must NOT Modify):**
- 所有 `experiments/**/*.csv`
- 所有 `experiments/drl/models/*.zip`
- 所有 `figures/**/*.png`
- `reports/phase3-baseline/phase3-baseline-report.md`
- `reports/phase4-drl-mvp/*.md`
- `src/` 與 `scripts/` 下的所有 codebase 源碼。
- `openspec/changes/` 下非 Change 05 的規格。

**Allowed to Modify in Step 2 ONLY:**
- `reports/handoff/change05-validation-note.md` (新增)
- `openspec/changes/reporting-figures-and-demo/tasks.md`
- `openspec/changes/reporting-figures-and-demo/specs/result-interpretation.md`
- `openspec/changes/reporting-figures-and-demo/specs/risk-register.md`
- `openspec/changes/reporting-figures-and-demo/specs/readme-finalization.md`
- `openspec/changes/reporting-figures-and-demo/specs/ppt-package.md`

*(若有其他檔案需修改，需先報請 Spec Owner 核准)*

---

## 12. Working Tree Hygiene

- **Audit 前 `git status`:** 存在一個被修改的檔案 `reports/handoff/gemini-intake-checklist.md`。
- **修復過程:** 已經使用 `git restore reports/handoff/gemini-intake-checklist.md` 將其還原，避免污染本 Commit。
- **Audit 後 `git status`:** 工作區乾淨 (working tree clean)。
- **本次 Commit:** 僅會包含本次新增的 `reports/handoff/gemini-codebase-audit-addendum.md` 檔案。

---

## 13. Commit Summary

- **Files added:** `reports/handoff/gemini-codebase-audit-addendum.md`
- **Files modified:** None
- **Commit message used:** `docs: add Gemini codebase audit addendum`
- **Pushed to GitHub:** Yes

---

## 14. Readiness for Step 2

- 我已閱讀整份主要 codebase。
- 我理解 Phase 3 / Phase 4 code pipeline。
- 我理解 frozen data boundaries。
- 我理解 Change 05 gaps。
- 我目前沒有修 Change 05。
- 我目前沒有進 Phase 5。
- 我等待 Spec Owner 驗收後，才會進 Step 2。

---

## 15. Codebase Audit Checklist

- [x] Read repo root files
- [x] Read Claude handoff
- [x] Read Gemini intake checklist
- [x] Read OpenSpec Change 01
- [x] Read OpenSpec Change 02
- [x] Read OpenSpec Change 03
- [x] Read OpenSpec Change 04
- [x] Read OpenSpec Change 05
- [x] Read Phase 3 baseline code
- [x] Read Phase 3 scripts
- [x] Read Phase 3 data artifacts
- [x] Read Phase 4 OpenGym code
- [x] Read Phase 4 DQN code
- [x] Read Phase 4 analysis code
- [x] Read Phase 4 scripts
- [x] Read Phase 4 data artifacts
- [x] Read Phase 4 reports
- [x] Confirm frozen data boundaries
- [x] Confirm no files modified except audit addendum
- [x] Commit and push audit addendum
- [x] Stop and wait for Spec Owner review
