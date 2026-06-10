# Final Claims Guardrail — 主張界線指引

本文件列出本專題可以講、不能講、需要附帶條件講的內容，確保所有口頭報告、書面報告與 demo 都不會出現 overclaim。

| 主張類別 | 允許的措辭 | 禁止的措辭 | 證據來源 |
|----------|-----------|-----------|----------|
| DQN 整體表現 | DQN 在 S1 排名第 2，在 S2 排名第 3 | DQN beats TCP / DRL outperforms all baselines | `dqn_vs_baseline_summary.csv` |
| S1 結果 | DQN S1 Utility 0.900，低於 BBR (0.947)，高於 CUBIC / NewReno | DQN dominates in S1 | `dqn_vs_baseline_summary.csv` |
| S2 結果 | DQN S2 Utility 0.757，排名第 3，丟包率 5.54% 為主要限制 | DQN performs well in S2 / S2 丟包可忽略 | `dqn_vs_baseline_summary.csv` |
| S1 策略 | S1 DQN 採取 100% Increase 退化策略（degenerate policy） | DQN learned adaptive intelligent policy | `dqn_action_distribution_summary.csv` |
| Utility 排名 | Provisional utility (α=1.0, β=0.1, λ=10.0) | Definitive / optimal utility weights | `final-report.md` |
| Delay 指標 | FlowMonitor delay proxy (delaySum/rxPackets) | True RTT / direct TCP RTT | 整份專案 |
| Action 機制 | Sender-side rate abstraction (Fallback Option B) | Kernel-level TCP control / cwnd modification | `train_dqn.py` |
| BBR S2 | ns-3.40 TcpBbr 已知 anomaly，Utility -0.169 | BBR always works / ignore BBR S2 | `baseline_summary.csv` |
| 可重現性 | 提供 source-of-truth artifacts 與重現指令 | 100% 保證可重現 / 絕無造假 | `final-reproducibility-guide.md` |
| OpenSpec SDD | 採用 OpenSpec 規格驅動開發治理研究過程 | OpenSpec 保證研究正確性 | `openspec/` |
| 未來工作 | PPO + 連續動作空間為自然延伸；Phase 6 已由 Spec Owner 跳過 | PPO will definitely solve all problems | N/A |
| 部署狀態 | 本專題為 MVP prototype，運行於模擬環境 | Production-ready TCP / real Internet deployment | 整份專案 |
