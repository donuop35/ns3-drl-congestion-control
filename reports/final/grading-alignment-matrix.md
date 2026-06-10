# 評分對齊矩陣 — Grading Alignment Matrix

本矩陣將期末專題常見評分要求與本 repo 內的交付物對齊，讓評審者快速確認每項要求的滿足情況。

| 評分項目 | 本專題對應內容 | 證據路徑 | 備註 |
|----------|----------------|----------|------|
| 研究動機與背景 | README Research Motivation + Final Report Executive Summary | `README.md`, `reports/final/final-report.md` | 明確說明 TCP 擁塞控制的問題與 DRL 機會 |
| 問題定義與 MDP 建模 | MDP Formulation (State/Action/Reward) | `figures/final/mdp_formulation.png`, `reports/final/final-report.md` | 5 維觀測、3 離散動作、provisional 獎勵函數 |
| 相關工作 / 文獻回顧 | Proposal 內 related work + final report | `proposal/`, `reports/final/final-report.md` | 涵蓋 TCP CC 演進與 DRL CC 近年研究 |
| 系統設計與架構 | System Pipeline + Topology 圖 | `figures/final/system_pipeline.png`, `figures/final/single_bottleneck_topology.png` | ns-3 + ns3-gym + SB3 完整工具鏈 |
| Baseline 實驗 | Phase 3 Baseline Benchmark | `experiments/summaries/baseline_summary.csv`, `reports/phase3-baseline/phase3-baseline-report.md`, `figures/baseline/` | NewReno / CUBIC / BBR，S1-S4 |
| DRL 實作 | Phase 4 DQN MVP | `src/agents/train_dqn.py`, `src/agents/eval_dqn.py`, `experiments/drl/models/` | SB3 DQN，S1+S2 各 30k steps |
| 實驗結果與分析 | S1/S2 Result Tables + Final Figures | `reports/final/final-report.md`, `figures/final/dqn_vs_baseline_utility_s1_s2.png`, `figures/final/dqn_vs_baseline_loss_s1_s2.png` | 含 Rank / Utility / Loss 完整比較 |
| 規格治理 / 開發方法論 | OpenSpec SDD (5 Changes) | `openspec/changes/` | Spec-Driven Development，每個 change 含 proposal/specs/design/tasks |
| GitHub 交付物 | 完整 repo 結構 | 見 README Repository Structure | 含 src / scripts / experiments / figures / reports / openspec |
| 簡報 / 口頭報告 | Slides Outline + Speaker Notes + Talk Track | `slides/final/` | 12 頁以內，10 分鐘 |
| 可重現性 | Reproducibility Guide + Figure Generation Script | `reports/final/final-reproducibility-guide.md`, `scripts/phase5/generate_final_figures.py` | 提供快速驗證與完整重現路線 |
| 限制與未來工作 | Limitations Table + Future Work | `reports/final/final-report.md`, `reports/final/final-claims-guardrail.md` | 誠實揭露 Delay Proxy / Option B / S2 高丟包 |
| Demo / 影片 | Demo Script + Runbook + Checklist | `demo/demo-script.md`, `demo/final-demo-runbook.md` | 10 分鐘，含 fallback plan |
| PPO / 進階演算法 | Out of scope by design | N/A | Phase 6 已由 Spec Owner 決定跳過；PPO 列為 future work |
