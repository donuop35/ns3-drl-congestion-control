# 老師閱讀導覽 — Teacher Navigation Map

本文件提供三條閱讀路線，讓評審者依據可用時間選擇最適合的驗收方式。

---

## 🚀 快速驗收路線 — 5 分鐘

適合快速確認專題完整性與核心結果。

| 步驟 | 閱讀內容 | 路徑 | 重點 |
|------|----------|------|------|
| 1 | Submission Guide | `SUBMISSION.md` | 專題概覽與交付物清單 |
| 2 | 一頁式摘要 | `reports/final/final-one-page-summary.md` | 研究問題、方法、核心結果 |
| 3 | Key Findings 圖 | `figures/final/key_findings_summary.png` | S1/S2 結果與限制一覽 |
| 4 | S1/S2 結果表 | `README.md` Results Summary 區段 | 效能排名與數值確認 |

---

## 📖 標準驗收路線 — 15 分鐘

適合完整理解研究內容與交付物品質。

| 步驟 | 閱讀內容 | 路徑 | 重點 |
|------|----------|------|------|
| 1 | README | `README.md` | 專題全貌、工具鏈、結果表 |
| 2 | 期末報告 | `reports/final/final-report.md` | Executive Summary、Results、Limitations |
| 3 | Final Figures | `figures/final/` | 9 張圖表（含 utility / loss / action dist / topology / pipeline） |
| 4 | Demo Script | `demo/demo-script.md` | 10 分鐘口頭報告流程 |
| 5 | Artifact Manifest | `reports/final/final-artifact-manifest.md` | 所有交付物索引 |
| 6 | 評分對齊矩陣 | `reports/final/grading-alignment-matrix.md` | 評分項目 ↔ 交付物對齊 |

---

## 🔬 深度驗收路線 — 30 分鐘以上

適合想深入檢視研究過程與可重現性的評審者。

| 步驟 | 閱讀內容 | 路徑 | 重點 |
|------|----------|------|------|
| 1-6 | 標準路線所有內容 | 同上 | — |
| 7 | OpenSpec Changes | `openspec/changes/` | 5 個 Change 的 proposal/specs/design/tasks |
| 8 | Phase 3 Baseline Report | `reports/phase3-baseline/phase3-baseline-report.md` | TCP baseline 實驗細節 |
| 9 | Phase 4 DRL Report | `reports/phase4-drl-mvp/phase4-drl-report.md` | DQN 訓練與評估細節 |
| 10 | Source CSV | `experiments/summaries/baseline_summary.csv`, `experiments/drl/summaries/dqn_vs_baseline_summary.csv` | 驗證圖表數據來源 |
| 11 | 訓練腳本 | `src/agents/train_dqn.py`, `src/agents/eval_dqn.py` | DQN 實作細節 |
| 12 | Reproducibility Guide | `reports/final/final-reproducibility-guide.md` | 重現步驟 |
| 13 | Claims Guardrail | `reports/final/final-claims-guardrail.md` | 可講 / 不可講的界線 |
