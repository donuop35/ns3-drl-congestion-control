# Final Reproducibility Guide

本專案提供完整 source-of-truth artifacts、OpenSpec 規格紀錄與重現指令，以支撐主要結果與圖表的可追溯性。

## 1. Scope of Reproducibility
在相容工具鏈環境下，主要結果與 final figures 可由既有 CSV / scripts 重新產生。本指南分為「快速驗證路線」與「完整實驗重現路線」。

## 2. Environment Assumptions
- 作業系統：Ubuntu 20.04/22.04 LTS 或 WSL2
- 網路模擬器：`ns-3.40`
- Python 環境：`Python 3.8+`
- 套件：`ns3-gym`, `stable-baselines3`, `pandas`, `matplotlib`, `pyzmq`
- OpenSpec：`Node.js 20.19+`, `@fission-ai/openspec@1.4.1`

## 3. Source-of-Truth Artifacts
主要結果與圖表皆追溯至以下不可修改之 CSV 檔案：
- `experiments/summaries/baseline_summary.csv`
- `experiments/drl/summaries/dqn_vs_baseline_summary.csv`
- `experiments/drl/summaries/dqn_action_distribution_summary.csv`

## 4. Fast Verification Path (Recommended for Review)
此路線僅依賴既有 source-of-truth CSV，重新產生報告所需的圖表：
```bash
python3 scripts/phase5/generate_final_figures.py
```
*(圖表將輸出至 `figures/final/`。此指令執行速度快，不會重新跑 ns-3 模擬。)*

## 5. Optional Full Baseline Reproduction
此路線為耗時實驗，將重新執行 Phase 3 的所有傳統 TCP (NewReno, CUBIC, BBR) 模擬：
```bash
# 需在 WSL2 環境下執行
bash scripts/phase3/baseline_runner.sh
python3 scripts/phase3/analysis.py
```

## 6. Optional DQN Evaluation Reproduction
此路線評估 Phase 4 預先訓練好之模型（`dqn_s1_seed42.zip` 與 `dqn_s2_seed42.zip`），以驗證 DRL agent 的效能：
```bash
# S1 評估
bash scripts/phase4/eval_dqn.sh experiments/drl/models/dqn_s1_seed42.zip S1
# S2 評估
bash scripts/phase4/eval_dqn.sh experiments/drl/models/dqn_s2_seed42.zip S2
```

## 7. Final Figure Regeneration
若您想重新生成 Final figures，請執行：
```bash
python3 scripts/phase5/generate_final_figures.py
```

## 8. Commands Not Recommended for Live Demo
展演時，時間通常受限於 10 分鐘，因此**不建議** live 執行以下指令：
- `bash scripts/phase4/train_dqn.sh` (重訓 30,000 steps 會大幅超時)
- `bash scripts/phase3/baseline_runner.sh` (重新模擬所有 baseline 耗時)

## 9. Known Environment Caveats
- `ns-3` 必須編譯成功且位於上層目錄（相對於 `scripts/`）。
- `ns3-gym` 必須安裝正確的 pyzmq 版本。
- BBR 在高延遲 S2 場景的 anomaly 屬於 ns-3.40 已知現象，並記錄於報告中。

## 10. No-Manual-Editing Rule
主要 final figures 由既有 CSV 與 scripts 重新產生，避免手動改數字。請勿手動修改 `figures/final/` 內的圖片內容。
