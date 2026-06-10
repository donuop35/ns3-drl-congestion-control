# Demo Checklist

## 展演前準備 (Pre-flight)
- [ ] 確認 `ns-3.40` 環境已編譯完成。
- [ ] 確認 Python 虛擬環境啟動，且 `pandas`, `matplotlib`, `stable-baselines3`, `openspec` 皆可用。
- [ ] 執行 `openspec validate reporting-figures-and-demo --strict` 確認規格無誤。
- [ ] 執行 `python3 scripts/phase5/generate_final_figures.py` 確保圖表可順利生成。
- [ ] 確認終端機（Terminal）字體夠大，且 IDE 畫面乾淨。

## 展演中防呆檢查 (No-Go Rules Check)
- [ ] **不可宣稱**：「DQN 全面打敗 TCP」。
- [ ] **不可宣稱**：「這是一個可以立刻部署的 production-ready TCP」。
- [ ] **不可宣稱**：「我們修改了 Kernel-level TCP cwnd」 (必須說明是 Fallback Option B)。
- [ ] **不可宣稱**：「這是 True TCP RTT」 (必須說明是 FlowMonitor Delay Proxy)。
- [ ] **不可執行**：Live 跑 30,000 steps 的 DQN 訓練，會超過 10 分鐘限制。

## 關鍵展示節點 (Key Deliverables to Show)
- [ ] `openspec/changes/reporting-figures-and-demo` (展示 SDD 工作流)
- [ ] `experiments/summaries/baseline_summary.csv` (展示 Baseline Source of Truth)
- [ ] `experiments/drl/summaries/dqn_summary.csv` (展示 DQN Source of Truth)
- [ ] `figures/final/dqn_vs_baseline_utility_s1_s2.png` (展示 S1 結果)
- [ ] `figures/final/dqn_vs_baseline_loss_s1_s2.png` (展示 S2 結果與高丟包限制)
- [ ] `reports/final/final-reproducibility-guide.md` (展示可重現性承諾)
