# 10 分鐘口頭報告講稿 — Talk Track

## 開場（0:00–0:45）
大家好，今天我報告的題目是「以深度強化學習進行單一瓶頸鏈路壅塞控制」。傳統 TCP 如 NewReno、CUBIC 依賴人工規則控制發送速率，我們想探索 DRL Agent 能否在模擬環境中學會更好的速率控制策略。這是一個 MVP 等級的可行性驗證。

## OpenSpec 方法論（0:45–1:30）
我們採用 OpenSpec 規格驅動開發（SDD），每個階段的變更都有正式的 proposal、specs、design 與 tasks。這確保了研究過程的可追溯性。

## 系統架構（1:30–2:30）
（展示 system_pipeline.png）
整個系統分為六層：最上層是 OpenSpec 治理，然後是 Phase 3 的 Baseline Benchmark，中間是 ns-3.40 模擬環境與 ns3-gym ZMQ 介面，再來是 SB3 DQN Agent，最下層是 Evaluation Metrics。

## 網路拓撲（2:30–3:15）
（展示 single_bottleneck_topology.png）
我們使用最簡單的 Sender → Router → Receiver 單一瓶頸拓撲。瓶頸鏈路為 10 Mbps，S1 延遲 10ms、S2 延遲 50ms。

## MDP 建模（3:15–4:00）
（展示 mdp_formulation.png）
Agent 觀測 5 維狀態，包含 throughput、delay proxy、loss rate、congestion signal 與前一動作。動作空間是離散三選一：降低、維持、提高發送速率。注意，這是 Sender-side Rate Abstraction，不是直接控制 kernel TCP。

## Baseline 結果（4:00–4:45）
（展示 baseline_utility_summary.png）
Phase 3 我們完成了 NewReno、CUBIC、BBR 的 baseline benchmark。BBR 在 S1 表現最佳，但在 S2 出現 ns-3.40 的已知 anomaly。

## DQN vs Baselines — Utility（4:45–5:45）
（展示 dqn_vs_baseline_utility_s1_s2.png）
S1 場景中，DQN Utility 0.900 排名第 2，低於 BBR 的 0.947。S2 場景中，DQN 排名第 3，Utility 0.757。DQN 並沒有全面勝過 TCP baselines。

## DQN vs Baselines — Loss（5:45–6:30）
（展示 dqn_vs_baseline_loss_s1_s2.png）
特別看 S2，DQN 丟包率高達 5.54%，遠高於 NewReno 的 0.14%。這是因為粗粒度的離散動作讓 Agent 傾向暴力提高發送速率，容忍丟包。

## DQN Action Distribution（6:30–7:15）
（展示 dqn_action_distribution_s1_s2.png）
S1 中 DQN 100% 選擇 Increase——這是退化策略，不是複雜的 adaptive policy。S2 中約 87% Increase、13% Decrease。

## 限制與貢獻（7:15–8:15）
（展示 key_findings_summary.png）
誠實地說，DQN 的 delay 指標是 FlowMonitor proxy 而非 true RTT，動作是應用層速率控制而非 kernel TCP。但本專題的貢獻在於：建立了可重現的 DRL CC MVP 測試平台，並進行了誠實的限制揭露。

## 可重現性（8:15–8:45）
所有圖表都可以從凍結的 CSV 重新產生：`python3 scripts/phase5/generate_final_figures.py`。我們不會 live 重訓 30,000 steps。

## 結論與未來工作（8:45–9:30）
本 MVP 驗證了 DRL 在單一瓶頸鏈路擁塞控制的可行性。未來可嘗試 PPO 搭配連續動作空間。Phase 6 已由 Spec Owner 決定跳過，PPO 為 future work。

## 結尾（9:30–10:00）
感謝聆聽。所有的成果都在 GitHub repo 中，歡迎檢視。
