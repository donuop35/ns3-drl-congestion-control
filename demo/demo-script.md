# Demo Script: DRL-Based Congestion Control

**Target Duration:** 10 分鐘
**Presenter:** Spec Owner

## 0:00–0:45 專題題目與研究問題
- **講稿:** 大家好，今天我要展示的專題是「以深度強化學習進行單一瓶頸鏈路擁塞控制」。我們探討的是，傳統 TCP（如 NewReno, CUBIC）依賴人工設計的規則，如果改用 DRL，Agent 能不能自己學會在吞吐量、延遲、與丟包之間取得平衡？我們做了一個 MVP。

## 0:45–1:45 OpenSpec SDD workflow 與 repo 結構
- **講稿:** 為了確保研究的嚴謹度，我們採用 OpenSpec 規格驅動開發（SDD）。所有實驗與變更都是由 `@fission-ai/openspec` 治理，保證 100% 可重現且沒有造假。
- **操作:** 秀出 repo 目錄結構，打開 `openspec/changes/`，展示 `Change 05` 裡面的 `specs/` 檔案。

## 1:45–2:45 Phase 3 baseline artifacts
- **講稿:** 實驗的第一步是建立 Baseline。我們跑了 NewReno, CUBIC, 與 BBR 在低延遲（S1, 10ms）與高延遲（S2, 50ms）的結果，這是我們比較的基準（Floor）。
- **操作:** 打開 `experiments/summaries/baseline_summary.csv`，證明數據來源真實存在。

## 2:45–3:45 Phase 4 ns3-gym + DQN artifacts
- **講稿:** 接著我們實作了 DQN Agent。我們透過 `ns3-gym` 橋接 `ns-3.40`，並使用 `Stable-Baselines3` 訓練了 30,000 steps。
- **操作:** 展示 `experiments/drl/models/` 內的 `.zip` 檔與 `dqn_summary.csv`。說明訓練已經完成，demo 不需 live 跑幾十分鐘的訓練。

## 3:45–4:45 S1 result
- **講稿:** 我們來看 Low Delay (S1) 的結果。DQN 達到了 9.88 Mbps 的吞吐量，Utility 排名第二（0.900），高於 CUBIC 與 NewReno。然而，我們發現 DQN 學到了一個 degenerate policy（100% Increase 動作），這代表它在簡單滿載環境下找到了局部最佳暴力解。
- **操作:** 秀出 `figures/final/dqn_vs_baseline_utility_s1_s2.png` 與 `figures/final/dqn_action_distribution_s1_s2.png`。

## 4:45–5:45 S2 result
- **講稿:** 到了 High Delay (S2)，情況變了。DQN 的丟包率飆升到 5.54%，Utility 降至排名第三。這顯示我們目前的 DQN MVP 在高延遲環境下，因為缺乏精細的隊列管理能力，選擇容忍丟包以換取吞吐量。
- **操作:** 秀出 `figures/final/dqn_vs_baseline_loss_s1_s2.png`。

## 5:45–6:45 Limitations and honest interpretation
- **講稿:** 我們必須誠實面對限制。首先，我們的動作是 Sender-side 的速率控制抽象化（Fallback Option B），不是直接改 Linux kernel 的 cwnd。其次，我們的延遲指標是 FlowMonitor 算出來的 Delay Proxy，不是 true TCP RTT。最後，DQN 並沒有全面打敗 TCP，這也不是 production-ready 的方案，而是一個證明「可行性」的雛形。

## 6:45–7:45 Reproducibility commands
- **講稿:** 這個專案最大的價值之一是「可重現性」。我們提供了一份完整的 Reproducibility Guide。
- **操作:** 在 terminal 執行 `python3 scripts/phase5/generate_final_figures.py`，證明所有的圖表都可以一鍵從 CSV 重新產生，絕無手動修圖。

## 7:45–8:45 Final report / figures / slides locations
- **講稿:** 所有的書面報告、最終圖表與投影片大綱，都妥善存放在 `reports/final/`, `figures/final/`, 與 `slides/final/`。我們也有一份 Artifact Manifest 來索引所有檔案。
- **操作:** 展示 GitHub Repo 的 README 中整理好的 Final Package Links。

## 8:45–10:00 Conclusion and future work
- **講稿:** 總結來說，我們成功建立了一個基於 ns-3 與 DRL 的擁塞控制實驗平台。雖然 DQN MVP 在複雜高延遲環境下有其極限，但這為未來的研究，如導入 PPO 演算法與連續動作空間，打下了堅實的基礎。謝謝大家。
