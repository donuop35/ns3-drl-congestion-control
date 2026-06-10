# Final Demo Runbook — 10 分鐘展演流程

## 開場（0:00–0:30）
- 開啟 GitHub repo 頁面
- 秀出 `SUBMISSION.md` 的交付物一覽
- 簡述專題目標

## Repo 導覽（0:30–1:30）
- 展示目錄結構：`openspec/`, `src/`, `experiments/`, `figures/`, `reports/`
- 點開 `openspec/changes/` 展示 5 個 Changes
- 強調 Spec-Driven Development

## OpenSpec 驗證（1:30–2:00）
- 在 terminal 執行：`openspec validate reporting-figures-and-demo --strict`
- 預期輸出：`Change 'reporting-figures-and-demo' is valid`

## Phase 3 Baseline（2:00–3:00）
- 開啟 `experiments/summaries/baseline_summary.csv`
- 展示 S1/S2 的 NewReno / CUBIC / BBR 數據
- 開啟 `figures/final/baseline_utility_summary.png`

## Phase 4 DQN 結果（3:00–5:00）
- 開啟 `experiments/drl/summaries/dqn_vs_baseline_summary.csv`
- 展示 `figures/final/dqn_vs_baseline_utility_s1_s2.png`
- 指出 S1 DQN 排名第 2、S2 排名第 3
- 展示 `figures/final/dqn_vs_baseline_loss_s1_s2.png`
- 指出 S2 DQN 丟包率 5.54%

## Action Distribution（5:00–5:30）
- 展示 `figures/final/dqn_action_distribution_s1_s2.png`
- 解釋 S1 degenerate policy

## 限制說明（5:30–6:30）
- 展示 `figures/final/key_findings_summary.png`
- 誠實說明：Delay Proxy, Sender-side Rate Abstraction, S2 高丟包
- 強調不宣稱 DQN 全面勝過 TCP

## Figure Regeneration Live Demo（6:30–7:30）
- 在 terminal 執行：`python scripts/phase5/generate_final_figures.py`
- 展示輸出：9 張圖全部 OK
- 展示 `figures/final/` 確認檔案存在

## Reproducibility（7:30–8:30）
- 開啟 `reports/final/final-reproducibility-guide.md`
- 說明快速驗證路線 vs 完整重現路線
- 強調不會 live 重訓 30,000 steps

## Final Report 巡覽（8:30–9:30）
- 開啟 `reports/final/final-report.md`
- 展示 Executive Summary、Results Tables、Limitations Table
- 開啟 `reports/final/final-artifact-manifest.md`

## 結尾（9:30–10:00）
- 總結貢獻：可重現的 DRL CC MVP
- 未來工作：PPO + 連續動作空間
- 感謝評審
