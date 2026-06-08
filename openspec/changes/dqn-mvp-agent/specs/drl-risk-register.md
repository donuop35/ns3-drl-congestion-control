## Purpose

管理 Change 04 dqn-mvp-agent 的 DRL 訓練、評估與實作風險，並為每個風險定義觸發條件、預防措施與 fallback 處理原則。

---

## Risk Categories

- **ENV**: Environment / ns3-gym related risks
- **TRN**: Training related risks
- **EVL**: Evaluation related risks
- **SCP**: Scope drift / governance risks
- **ART**: Artifact / logging risks
- **OPS**: Operational / toolchain risks

---

## Risk Register

| Risk ID | Category | Description | Probability | Impact | Prevention | Fallback | Owner | Trigger Condition |
|---------|----------|-------------|-------------|--------|-----------|---------|-------|-------------------|
| R-04-01 | ENV | Smoke test（ST-01~ST-10）未通過 | Medium | **Critical** | 在 training 開始前完整執行 smoke test；fix environment before training | 修復 environment 後重新執行 smoke test；不得在 smoke test fail 時強行開始 training | Agent | Any ST criterion returns FAIL |
| R-04-02 | TRN | DQN reward 非有限（NaN / Inf / -Inf）| Medium | High | 確保所有 observation 欄位有 clip to [0,1]；reward clipping（e.g., clip to [-10, 10]）| 立即停止 training；回報 Spec Owner；檢查 normalization 和 reward formula | Agent | `math.isfinite(reward) == False` at any step |
| R-04-03 | TRN | DQN reward 發散（unbounded growth）| Low | High | 監控 training reward 趨勢；設置 reward clipping | 立即停止；調整 reward weights；回報 Spec Owner | Agent | Episode reward grows without bound over training |
| R-04-04 | TRN | DQN 不收斂（reward 不穩定或持平在低值）| High | Medium | 選擇合適 learning rate 和 batch size；足夠 timesteps；確認 environment 穩定 | Reportable failure（見 success-failure-criteria.md）；record as limitation；do NOT silently increase timesteps without reporting | Agent | After 50% of total_timesteps, reward shows no improvement trend |
| R-04-05 | TRN | DQN 只學會保守策略（always action 1: keep）| Medium | Medium | 確保 ε-greedy exploration 設定合理（不過小）；確保 reward 有足夠 signal | Record as "conservative policy convergence"；analyze reward signal；report as limitation | Agent | > 90% of actions are action 1 (keep) in evaluation |
| R-04-06 | TRN | DQN 只追 throughput，RTT / loss 上升 | Medium | High | 確保 β > 0 和 λ > 0（非 throughput-only reward）；DR-04-04 明確要求 | 調整 β / λ（with Spec Owner approval）；document as reward design limitation | Agent | Evaluation: throughput improves but delay/loss significantly worse than baseline |
| R-04-07 | EVL | Training reward 上升但 evaluation metrics 變差 | Medium | High | Training / evaluation 嚴格分離（DR-04-03）；evaluation 使用 deterministic policy | Investigate overfitting or reward misalignment；report as limitation | Agent | Training reward converges but evaluation throughput/utility < baseline |
| R-04-08 | EVL | DQN 輸給 CUBIC / BBR 在所有 metrics | High | Medium | Reportable failure 定義已處理此情境（見 success-failure-criteria.md）| Report honestly；analysis in limitation section；frame as future work | Agent | All 4 evaluation metrics worse than both NewReno and CUBIC |
| R-04-09 | ENV | BBR 在 ns-3.40 不可用 | Medium | Low | 繼承 Change 02 BBR fallback rule；BBR 是 strongly recommended but non-blocking | Create `BBR_SKIPPED.md`；continue without BBR comparison | Agent | ns-3.40 TcpBbr module unavailable or unstable |
| R-04-10 | SCP | S3 / S4 scenario 太難導致 DQN 無法收斂 | Low | Low | S1 / S2 是 MVP-required；S3/S4 是 optional（見 Change 02 scenario-matrix.md）| Skip S3/S4；focus on S1/S2；document as "Optional scenarios not evaluated" | Agent | DQN training fails on S3/S4 scenarios |
| R-04-11 | ART | Artifact logging 不完整（缺少 training_config / checkpoint / evaluation CSV）| Medium | High | training_config.yaml 在 training 開始前填寫；checkpoint 設置固定 save interval | 重新 training（若 config 記錄完整）；若 config 丟失，需重新設計 run | Agent | After training: training_config.yaml missing, or evaluation_summary.csv missing |
| R-04-12 | SCP | Antigravity 提前導入 PPO 或 continuous action | Medium | High | DR-04-01 / DR-04-02 明確禁止；extension-rules.md 規定需另開 change | 立即停止並刪除 PPO / continuous action code；回報 Spec Owner | Agent | PPO / SAC / TD3 / continuous action code appears in Change 04 implementation |
| R-04-13 | SCP | Antigravity 改 action space 而不另開 change | Low | High | Change 03 action space 凍結（Discrete(3)）；任何更改必須另開 change | 立即停止；回報 Spec Owner；revert action space change | Agent | Action space changed from Discrete(3) without new OpenSpec change |
| R-04-14 | ART | Final PPT 無法解釋 DQN 結果（缺圖或數字矛盾）| Medium | High | output-artifacts.md 明確定義 required figures 和 tables；在 implementation 時同步建立圖表 | 補充缺失圖表；若數字矛盾，重新 evaluation | Agent | PPT figures and comparison table numbers are inconsistent |
| R-04-15 | OPS | DQN config / seed / metadata 缺失導致無法重現 | Medium | High | training-protocol.md 明確定義 reproducibility metadata；training_config.yaml 必須在 training 前填寫 | 若 metadata 不完整，重新 training 並正確記錄；document as limitation if impossible | Agent | Cannot reproduce training results from saved config |
| R-04-16 | OPS | 官方 OpenSpec 未正確初始化 / 使用 openspec-preview 代替 | High | High | 每次 change 開始前確認 `openspec --version` 和 `openspec list --json`；proposal.md 正式說明 openspec-preview 降級 | 若發現 openspec-preview 被誤用，立即停止；重新初始化官方 OpenSpec；回報 Spec Owner | Agent | `openspec list` 找不到 change-04 / dqn-mvp-agent；或 `.agent/skills/` 目錄不存在 |

---

## Fallback Principles

1. **Smoke test MUST pass before training**: R-04-01 是最高優先 stop rule
2. **Non-finite reward = immediate stop**: R-04-02 必須立即停止，不得繼續 training
3. **DQN underperformance is reportable, not catastrophic**: R-04-04, R-04-08 有明確 reportable fallback
4. **PPO and continuous action are strict exclusions**: R-04-12, R-04-13 是 governance risk，必須立即回報
5. **Metadata completeness is mandatory**: R-04-15 的預防比 fallback 更重要；在 training 前填寫所有 metadata
6. **Official OpenSpec is non-negotiable**: R-04-16 是 foundational risk；任何假 OpenSpec 都是 critical failure
