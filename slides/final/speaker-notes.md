# Speaker Notes

**Slide 1: Title**
大家好，我是 Spec Owner，今天我要報告的專題是「以深度強化學習進行單一瓶頸鏈路擁塞控制」。這是一個 MVP 原型的實作與驗證。

**Slide 2: Motivation**
為什麼選擇這個題目？傳統的 TCP 擁塞控制大多依賴寫死的規則，很難在所有的網路情境下同時做到高吞吐、低延遲與低丟包。我們想知道，讓 AI (DRL) 控制發送速率，探索其在 ns-3 環境下的可行性與限制。

**Slide 3: Research Question & Scope**
我們的範圍非常明確：只有一條單一瓶頸鏈路。我們使用 DQN 演算法，只有三個簡單的離散動作。比較的對象是傳統的 NewReno, CUBIC, 以及 BBR。

**Slide 4: System Architecture**
要讓 RL 和網路模擬器對話，我們串接了 ns-3 作為網路環境，使用 ns3-gym 作為 ZMQ 橋樑，並使用 Stable-Baselines3 運行 DQN 代理。

**Slide 5: MDP Formulation**
在 RL 模型中，代理觀察到的狀態包含了吞吐量與延遲等 5 個維度。它能採取的動作是：增加、維持、減少發送速率（這是應用層的抽象控制）。我們給的獎勵函數會鼓勵高吞吐量，並懲罰高延遲與丟包。

**Slide 6: Baseline Benchmark**
在引入 AI 前，我們測量了傳統 TCP 作為基準。在低延遲 (S1) 時 BBR 最好；在高延遲 (S2) 時則是 NewReno 較好。

**Slide 7: DRL MVP Implementation**
我們成功讓 DQN 在這個環境中訓練了 30,000 步。圖中可以看到代理在 S1 與 S2 中都學會了如何提高它的 Reward。

**Slide 8: Main Results — S1**
在 S1 低延遲場景，DQN 表現亮眼，Utility 排名第二，僅次於 BBR。但我們分析動作分佈發現，它 100% 都在執行「增加」動作。這代表它在簡單環境下找到了暴力解，而不是真的學到了複雜的自適應策略。

**Slide 9: Main Results — S2**
在 S2 高延遲場景，DQN 的 Utility 降到第三名，且丟包率飆升到 5.54%。這顯示目前的 DQN MVP 太過追求吞吐量，缺乏處理長延遲佇列的精細控制能力。

**Slide 10: Findings and Limitations**
必須誠實說明限制：我們的 Delay 指標是 FlowMonitor 計算的 proxy，不是真正的 TCP RTT；動作控制也不是直接改 Linux Kernel。我們不宣稱 DQN 全面打敗 TCP。

**Slide 11: Demo / Reproducibility**
這個專案的重點是嚴謹。所有的變更都通過 OpenSpec 驗證，只要執行幾個腳本，任何人都可以在自己電腦上重現今天的圖表與數據。

**Slide 12: Conclusion & Future Work**
總結來說，這個 MVP 證明了用 RL 控制 ns-3 網路流量是可行的。未來我們希望能使用 PPO 搭配連續動作空間，讓控制更加平滑。謝謝大家。
