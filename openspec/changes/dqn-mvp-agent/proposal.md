## Why

Change 02 已建立可重現的 TCP baseline benchmark 規格；Change 03 已完整定義 ns3-gym MDP environment interface。在進入任何實作之前，必須先正式規格化 DQN MVP agent 的訓練、評估與比較協議，原因如下：

1. **DQN 必須承接 Change 03 environment**：observation shape、action space、reward concept、smoke test gate 均已在 Change 03 凍結，DQN agent 不得自行更改這些 interface
2. **DQN 必須承接 Change 02 baseline metrics**：throughput / RTT / loss / utility 是評估 DRL 有效性的唯一基準；reward curve 不能作為唯一成功指標
3. **不能在沒有訓練 / 評估規格的情況下進入實作**：若 training protocol、evaluation protocol、baseline comparison protocol 未先定義，DQN 實作會缺乏可驗收的完成標準
4. **DQN 不保證 outperform baseline**：必須先定義「DQN 輸給 baseline 也是 reportable」的規格，避免 training 結果無法解讀
5. **Phase 2 需要最後收束**：本 change 是 Phase 2「用 OpenSpec 建立專案真相來源」的最後一關；完成後才能進入 Phase 3 Baseline 先行

> 🔒 **OpenSpec 正式性要求**：本 change 使用官方 `@fission-ai/openspec@1.4.1` CLI。`openspec-preview/` 僅作為歷史參考，不是正式 OpenSpec source of truth。所有 artifacts 位於 `openspec/changes/dqn-mvp-agent/`。

**Upstream Reference**: 本 change 依據 Change 01（project-charter）、Change 02（ns3-baseline-benchmark）、Change 03（opengym-env）中已通過 Spec Owner 驗收的所有凍結規格。

---

## What Changes

本 change 新增以下規格（不含任何實作程式碼）：

- **DQN MVP Boundary**: 明確定義 DQN agent 使用的 algorithm（SB3 DQN）、policy（MlpPolicy）、action space（繼承 Change 03 Discrete(3)）、observation（繼承 Change 03 shape [5]）
- **Training Protocol**: 定義 training 前的 gate（smoke test）、required logging（episode reward / length / steps / seed / config）、checkpoint concept、reproducibility metadata
- **Evaluation Protocol**: 定義 training 與 evaluation 分離原則、evaluation metrics（throughput / RTT / loss / utility / episode reward）、MVP-required scenarios（S1 / S2）
- **Baseline Comparison Protocol**: 定義 DQN vs NewReno / CUBIC / BBR 的比較方式、metric alignment（繼承 Change 02）、DQN underperformance 的 interpretation rules
- **Output Artifacts**: 定義 logs / figures / tables / metadata / README section / PPT figure list / 10-minute video support
- **Success / Failure Criteria**: 定義 full success / partial success / failure but reportable / stop rules / fallback rules
- **Extension Rules**: 定義 reward ablation / observation ablation / PPO / continuous action 的 extension governance
- **DRL Risk Register**: 16 個 DRL 實作風險及 fallback

---

## What Does Not Change

本 change 嚴格禁止以下事項：

> ⛔ **不更改題目** — 題目在 Change 01 凍結  
> ⛔ **不更改 action space** — Discrete(3) 在 Change 03 凍結  
> ⛔ **不更改 baseline metrics** — throughput / RTT / loss / utility 在 Change 02 凍結  
> ⛔ **不導入 PPO 作為 MVP** — PPO 為 future extension  
> ⛔ **不使用 continuous action** — 需要另開 OpenSpec change  
> ⛔ **不做 IPFS / QUIC / multi-agent / multi-path** — 不在 scope  
> ⛔ **不修改 Linux kernel TCP** — 不在 scope  
> ⛔ **不宣稱已有實驗結果** — 本 change 只建立規格  
> ⛔ **不寫任何 Python / C++ / shell 程式碼**  
> ⛔ **不執行 ns-3 / ns3-gym / DQN training**

---

## Impact

本 change 建立的規格將直接成為：

- **Phase 3 Baseline 先行 / Phase 4 DQN implementation 的上游規格**: 所有實作必須符合本 change 定義的 training / evaluation / comparison protocol
- **Final GitHub README 的依據**: README 中的 DQN results section 必須按本 change 的 artifact requirements 組織
- **Final PPT 與 10 分鐘影片的圖表與敘事依據**: 本 change 定義了 required figures 與 comparison tables
- **DQN success / failure interpretation 的依據**: 本 change 明確定義「DQN 輸給 baseline 也是 reportable」，不得在 presentation 中隱藏 underperformance

---

## Dependencies

- ✅ Change 01 project-charter（已通過 Spec Owner 驗收）
- ✅ Change 02 ns3-baseline-benchmark（已通過 Spec Owner 驗收，ns-3.40 凍結）
- ✅ Change 03 opengym-env（已通過 Spec Owner 驗收，MDP interface 凍結）
- Stable-Baselines3 DQN（Python package，實際安裝在 Phase 3 / Phase 4）

---

## Acceptance Criteria

- [ ] DQN MVP boundary 已明確（SB3 DQN + MlpPolicy + Change 03 observation/action/reward）
- [ ] DQN 使用 discrete action（Change 03 Discrete(3)）；未改為 continuous
- [ ] PPO 明確標為 future extension only
- [ ] Training protocol 已定義（smoke test gate + logging + checkpoint + reproducibility）
- [ ] Evaluation protocol 已定義（training/evaluation 分離 + metrics + S1/S2 MVP-required）
- [ ] Baseline comparison protocol 已定義（DQN vs NewReno / CUBIC / BBR if available）
- [ ] Output artifacts 已定義（logs / figures / tables / metadata / README / PPT）
- [ ] Failure fallback 已定義（DQN underperformance = reportable，不是自動失敗）
- [ ] DRL risk register 已建立（16 個風險）
- [ ] Extension rules 已建立（所有 extension 不得阻塞 MVP）
- [ ] 不含任何 DQN / ns-3 / ns3-gym 實作程式碼
- [ ] 無 scope drift（無 IPFS / QUIC / PPO MVP / multi-agent / multi-path）
- [ ] Spec Owner 驗收通過，才進入 Phase 3 Baseline 先行

---

## Final Specification Closure Notes

### 1. Official OpenSpec Requirement
本專案使用官方 OpenSpec CLI（`@fission-ai/openspec@1.4.1`）。不接受任何仿製 workflow。所有 change artifacts 位於 `openspec/changes/` 下。

### 2. openspec-preview Demotion
`openspec-preview/`（若存在）只能作為歷史預覽參考，不是正式 OpenSpec source of truth。正式規格以 `openspec/changes/` 為準。

### 3. Baseline Before DRL
Phase 3 必須先執行 baseline benchmark（Change 02 /opsx:apply），確認 NewReno / CUBIC 結果後，才能進入 DQN training。不得直接從規格跳到 DQN training。

### 4. DQN MVP Protection
DQN MVP 只使用 Discrete(3) action space。不導入 PPO、不使用 continuous action。任何 algorithm 變更必須另開 OpenSpec change 並獲 Spec Owner 批准。

### 5. Evaluation Over Reward Curve
Training reward curve 只作為 training diagnostic（監控收斂）。Final evaluation 必須使用獨立的 throughput / RTT / loss / utility 指標，並與 baseline 比較。

### 6. Reportable Failure Rule
DQN 不收斂、不穩定、或輸給 baseline 均不是自動失敗。這些情境必須轉成 limitation / future work 並在 final report 中誠實記錄。

### 7. No Scope Expansion
不得引入 IPFS、QUIC、multi-agent、multi-path、large topology。任何 scope 變更必須另開 OpenSpec change 並獲 Spec Owner 批准。
