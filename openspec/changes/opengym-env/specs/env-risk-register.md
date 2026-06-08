## Purpose

管理 Change 03 opengym-env 階段的環境設計與實作風險，並為每個風險定義觸發條件、預防措施與 fallback 處理原則。

---

## Risk Register

| Risk ID | Description | Probability | Impact | Prevention | Fallback | Owner | Trigger Condition |
|---------|-------------|-------------|--------|-----------|---------|-------|-------------------|
| R-03-01 | Observation 無法從 ns-3 / ns3-gym 直接取得 | High | High | 預先研究 FlowMonitor 與 ns3-gym `opengym` module 的 API；確認 `GetObs()` 可回傳自訂 observation | 使用 TracedValue / ASCII trace 作為 fallback；在 info dict 中標記取得方式 | Agent | 實作 `GetObs()` 時取得 empty 或 None |
| R-03-02 | RTT trace 無法從 ns-3 直接取得（只有 one-way delay）| High | Medium | 使用 `delaySum / rxPackets` 作為 delay estimate；在 observation-space.md fallback 規則中已定義 | 使用 delay estimate 取代 RTT；在 info dict 中標記 `delay_estimate_method` | Agent | FlowMonitor 無 RTT 欄位，只有 delay sum |
| R-03-03 | Queue occupancy 無法從 ns3-gym 取得 | Medium | Low | Queue occupancy 已標為 Enhanced observation（future extension）；MVP 不依賴此欄位 | 使用 `delay_norm` 作為壅塞代理信號；不阻塞 MVP | Agent | ns3-gym 無 queue trace API |
| R-03-04 | Action effect 難以映射到 sender-side control | High | High | 在 Change 04 implementation 中明確定義 action → cwnd/rate 的步長映射；本 change 只定義抽象語意 | 若直接控制 cwnd 有困難，改用 sending rate 抽象；若仍有困難，回報 Spec Owner | Agent | ns3-gym GetAction() 無法影響 TCP sending rate |
| R-03-05 | Reward scale 不穩（step-to-step 差異過大）| Medium | High | 確保所有 component 已正確 normalization；初始 α, β, λ 謹慎選擇；監控 reward 分佈 | 加入 reward clipping（e.g., clip to [-10, 10]）；回報 Spec Owner 並調整 weight | Agent | DQN training 中 Q-value 發散或 loss 爆炸 |
| R-03-06 | Throughput-only reward 誘導錯誤策略 | Medium | High | Reward 必須包含 delay 和 loss component（已在 reward-function.md 明確禁止 throughput-only）| 若發現 agent 行為異常（如 buffer bloat），立即停止 training 並回報 Spec Owner | Agent | Reward formula 只有 throughput_norm；或 β = λ = 0 |
| R-03-07 | Step interval 不一致導致 baseline / DRL 無法比較 | Medium | High | 在 Change 04 中固定 decision interval；info dict 中記錄 `episode_sim_time_s`；確保 DRL episode 與 baseline scenario 的 simulation duration 相同 | 若無法對齊，回報 Spec Owner；不得強行比較 | Agent | DRL episode 時長與 baseline scenario 時長不一致 |
| R-03-08 | Random agent smoke test 無法通過 | Medium | High | 按照 smoke-test.md 的 ST-01 ~ ST-10 逐一驗證；在 DQN training 開始前必須全部通過 | 若 smoke test fail，停止 Change 04 training，修復 environment 後重新測試；回報 Spec Owner | Agent | Smoke test 任一 ST condition fail |
| R-03-09 | Antigravity 直接寫 DQN training code 而跳過 smoke test | High | High | 在 tasks.md 中明確列出 smoke test 為 training 前的強制 gate；本 change 中明確禁止寫 training code | 若發現 DQN code，立即停止並刪除；回報 Spec Owner | Agent | Change 04 tasks.md 中 smoke test 尚未標記為 done 但 training code 已存在 |
| R-03-10 | PPO 被提前導入至 Change 03 或 Change 04 | Medium | High | design.md D-03-06 已明確禁止 PPO MVP；action-space.md 已記錄 PPO exclusion rule | 若發現 PPO code，立即停止並刪除；若需要 PPO 必須另開 change 並獲 Spec Owner 批准 | Agent | Change 04 中出現 PPO / ActorCritic / SAC 相關 code |
| R-03-11 | Environment spec 過度綁死 implementation 細節 | Low | Medium | 本 change 只定義 interface（observation shape / action space / reward concept），不定義具體 implementation 參數（step size / weight value）| 若 spec 過於嚴格導致 implementation 困難，另開 change revision 並獲 Spec Owner 批准 | Spec Owner | Change 04 implementation 因本 spec 的某條規格無法實現 |
| R-03-12 | Info dict 缺少 baseline-compatible metrics | Medium | High | episode-step-reset.md 已明確列出 info dict 的 required fields（含 `raw_*` metrics 和 `utility_score`）| 若 info dict 缺少欄位，DRL vs baseline 比較無法進行；必須補齊 info dict | Agent | Change 04 evaluation 無法提取 `raw_throughput_mbps` 等欄位 |
| R-03-13 | Antigravity 未使用官方 OpenSpec，而是自行模擬 workflow | High | High | 每個 change 開始前確認 `openspec --version` 與 `openspec list --json`；所有 artifacts 必須在官方 `openspec/changes/` 目錄下 | 若發現假 OpenSpec，立即停止所有 change；重新安裝官方 `@fission-ai/openspec@latest` 並重新初始化 | Agent | `openspec list` 找不到 change；或 `.agent/skills/` 目錄不存在 |

---

## Fallback Principles

1. **Smoke test MUST pass before DQN training**: 任何 risk 導致 smoke test fail，必須停止並回報 Spec Owner，不得繼續 training
2. **Observation fallback 已定義**: 若 RTT / queue occupancy 等無法取得，使用 observation-space.md 中定義的 fallback
3. **Reward provisional**: α, β, λ 的初始值在 Change 04 中調整，不在本 change 固定，降低 reward design risk
4. **PPO 和 continuous action 是嚴格 future extension**: 任何 PPO 或 continuous action 必須另開 change
5. **No DRL before baseline approval**: Change 02 specification 已通過，但 /opsx:apply 和 implementation 在 Phase 3 才開始
6. **Official OpenSpec only**: 任何假 OpenSpec 或模擬 workflow 都是整個 change 的 critical failure，必須立即停止
