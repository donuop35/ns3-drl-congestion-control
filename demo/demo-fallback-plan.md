# Demo Fallback Plan — 應急方案

本文件提供 demo 過程中可能遇到的問題與應對方式。

## Fallback 1：Figure Regeneration 失敗
**問題**：`python scripts/phase5/generate_final_figures.py` 執行失敗。
**應對**：直接展示 `figures/final/` 中已存在的 9 張 PNG。向評審說明這些圖表是由之前成功執行的腳本所產生的，source data 均來自凍結的 CSV。

## Fallback 2：OpenSpec Validate 失敗
**問題**：`openspec validate` 回傳錯誤。
**應對**：確認 Node.js 版本是否 ≥ 20.19.0。若環境問題無法即時解決，展示 `reports/handoff/change05-validation-note.md` 中的歷史驗證紀錄。

## Fallback 3：被問到 PPO
**應對**：「Phase 6 已由 Spec Owner 決定在本學期跳過。PPO 搭配連續動作空間是本專題的自然延伸，已列入 future work。」

## Fallback 4：被問到 Real Internet Deployment
**應對**：「本專題為 MVP prototype，在 ns-3 模擬環境中運行。不宣稱 production-ready，也未進行 real Internet deployment。」

## Fallback 5：被問到為何 DQN 沒有贏 BBR
**應對**：「S1 中 BBR 的 delay 控制（25.9ms）遠優於 DQN（115.3ms），因為 BBR 有 pacing 機制。DQN 的 Sender-side Rate Abstraction 無法精細控制 sending rate，採取了 100% Increase 的退化策略。這是 MVP 的限制，不是失敗。」

## Fallback 6：被問到為何 S2 DQN 丟包這麼高
**應對**：「S2 高延遲環境中，DQN 的粗粒度離散動作（只有 ↓=↑ 三選一）使 Agent 傾向暴力提高發送速率以追求 throughput reward，導致 5.54% 的高丟包。這凸顯了離散動作空間的限制，也是我們建議未來使用 PPO + 連續動作空間的原因。」

## Fallback 7：網路斷線 / GitHub 無法存取
**應對**：事先準備 repo 的 local clone。所有展演內容都可在本地完成。
