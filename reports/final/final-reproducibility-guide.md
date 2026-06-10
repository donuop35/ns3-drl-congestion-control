# Final Reproducibility Guide

本專案所有的程式碼與實驗結果皆為 100% 可重現（100% Reproducible），且受到 `@fission-ai/openspec` 工作流的嚴格把關。

## 1. 系統先決條件 (System Prerequisites)
- 作業系統：Ubuntu 22.04 LTS 或 WSL2
- 網路模擬器：`ns-3.40`
- Python 環境：`Python 3.10+`
- 套件：`ns3-gym`, `stable-baselines3`, `pandas`, `matplotlib`, `pyzmq`
- OpenSpec：`Node.js 20.19+`, `@fission-ai/openspec@1.4.1`

## 2. 規格驗證 (OpenSpec Validation)
執行此指令以確保專案變更符合規格：
```bash
openspec validate reporting-figures-and-demo --strict
```
*(預期：Pass，確保所有檔案皆有遵守定義的規則)*

## 3. 重跑 Baseline 實驗 (Baseline Reproduction)
執行所有傳統 TCP (NewReno, CUBIC, BBR) 的測試：
```bash
python scripts/run_baseline.py
```
*(注意：此步驟較耗時，通常不需要在 Demo 時執行。既有的 CSV 已為 Source of Truth。)*

## 4. 執行 DRL 冒煙測試 (Smoke Test)
確認 ns3-gym ZMQ 連線與環境運作正常：
```bash
python src/drl_agent/smoke_test.py
```
*(預期：不報錯，且在幾秒內印出 step reward 與 episode completion 訊息)*

## 5. 評估已訓練的 DQN 模型 (DQN Evaluation)
讀取 Phase 4 預先訓練好的模型（存放於 `experiments/drl/models/`）並進行評估：
```bash
python src/drl_agent/evaluate_dqn.py --seed 42
```
*(注意：不建議在 Demo 時 Live 重訓 DQN 30,000 步。直接使用提供的 Evaluate 腳本即可確認模型表現。)*

## 6. 生成最終圖表 (Final Figure Generation)
使用既有的 CSV (Source of Truth) 重新產生報告與簡報中使用的所有圖片：
```bash
python scripts/phase5/generate_final_figures.py
```
*(預期：圖片會更新到 `figures/final/` 目錄內。)*

---
**核心原則：**
- 所有的 CSV (`experiments/summaries/baseline_summary.csv` 等) 是絕對的數據來源，請勿手動竄改。
- Demo 中不需要從零開始跑完整個 RL 訓練迴圈，這會超過 10 分鐘的展示限制。
