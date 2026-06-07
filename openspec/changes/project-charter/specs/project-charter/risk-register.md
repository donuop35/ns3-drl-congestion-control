# Risk Register

Last updated: 2026-06-08  
Change: 01-project-charter

---

## Risk Summary Table

| Risk ID | Description | Probability | Impact | Owner | Status |
|---------|-------------|-------------|--------|-------|--------|
| R-01 | ns3-gym 安裝失敗或版本不相容 | Medium | HIGH | Antigravity | ⏳ Pending（Change 03）|
| R-02 | ns-3 baseline logging 不完整 | Medium | HIGH | Antigravity | ⏳ Pending（Change 02）|
| R-03 | BBR baseline 版本相依問題 | Medium | MEDIUM | Antigravity | ⏳ Pending（Change 02）|
| R-04 | DQN 不收斂 | Medium | MEDIUM | Antigravity | ⏳ Pending（Change 04）|
| R-05 | Reward 設計導致高 throughput 但高 RTT / loss | Medium | HIGH | Antigravity | ⏳ Pending（Change 03）|
| R-06 | Antigravity 自行擴題 | Low | HIGHEST | Antigravity | 🔴 Actively Monitored |
| R-07 | 題目被誤解為 IPFS 實作 | Low | HIGHEST | Spec Owner | 🔴 Actively Monitored |
| R-08 | DRL 結果不優於 baseline | High | LOW | Antigravity | ⏳ Pending（Change 04）|
| R-09 | 實驗圖表不足以支撐簡報 | Medium | MEDIUM | Antigravity | ⏳ Pending（Change 05）|
| R-10 | OpenSpec 文件與實作脫節 | Low | MEDIUM | Antigravity | 🟡 Mitigated |
| R-11 | 使用假 OpenSpec / 模擬 OpenSpec workflow | Low | HIGHEST | Antigravity | 🟢 Verified（v1.4.1）|
| R-12 | 未使用官方 OpenSpec CLI 卻宣稱完成 OpenSpec change | Low | HIGHEST | Antigravity | 🟢 Verified（v1.4.1）|

---

## Detailed Risk Descriptions

### R-01: ns3-gym 安裝失敗或版本不相容

**Description**: ns3-gym 可能與目標 ns-3 版本不相容，或在 Windows/WSL 環境安裝困難。  
**Probability**: Medium  
**Impact**: HIGH — 若無法建立 RL environment，Change 03 完全阻塞  
**Prevention**:
- 先確認目標 ns-3 版本（>= 3.32）
- 先跑官方 ns3-gym example，確認基本功能正常
- 固定 Linux/Ubuntu 20.04 環境
- 將安裝步驟寫入 README，保留完整錯誤 log

**Fallback**:
1. 使用較舊但穩定的 ns-3 / ns3-gym 版本組合
2. 改用簡化 Python Gym bottleneck simulator（需 spec owner 批准）
3. 先完成 ns-3 baseline + DRL design proposal，等待環境問題解決

**Trigger Condition**: Change 03 中 `env.reset()` 或 `env.step()` 在 3 次修復嘗試後仍失敗  
**Owner**: Antigravity（須立即回報 spec owner）

---

### R-02: ns-3 baseline logging 不完整

**Description**: ns-3 可能無法直接輸出所需格式的 throughput / RTT / loss CSV，需要額外的 tracing 設定。  
**Probability**: Medium  
**Impact**: HIGH — 無法比較 baseline 與 DRL 結果  
**Prevention**:
- 研究 ns-3 的 FlowMonitor 和 tracing API
- 先以 small-scale 測試確認 log 可正確輸出
- 每個 scenario 都要先確認 CSV 格式

**Fallback**:
- 使用 ns-3 ASCII tracing / PCAP 後期解析
- 撰寫後處理 Python script 從 ns-3 output 提取所需 metrics

**Trigger Condition**: Change 02 的 baseline 跑完後，CSV 欄位缺失或格式異常  
**Owner**: Antigravity

---

### R-03: BBR baseline 版本相依問題

**Description**: BBR 支援需要 ns-3 >= 3.32，若目標版本較低或 BBR module 不完整，整合可能失敗。  
**Probability**: Medium  
**Impact**: MEDIUM — BBR 缺失降低比較豐富度，但不阻塞 MVP  
**Prevention**:
- 確認 ns-3 版本 >= 3.32
- 先確認 ns-3 BBR module 可正常運行
- BBR 設為 "strongly preferred" 而非 "required"

**Fallback**:
- 若 BBR 整合超過 1 個工作日仍失敗，移至 optional/future work
- 在 README 和 report 中說明原因，不列為 MVP 失敗

**Trigger Condition**: Change 02 中 BBR baseline 安裝時間 > 1 個工作日  
**Owner**: Antigravity

---

### R-04: DQN 不收斂

**Description**: DQN agent 訓練後 reward curve 平坦，或無法學到有意義的策略。  
**Probability**: Medium  
**Impact**: MEDIUM — 不影響 pipeline 完整性，但影響 final report 說服力  
**Prevention**:
- Action space 保持簡單（Discrete(3)）
- Scenario 先用最簡單的情境（Scenario A）
- 先用 random agent 做 smoke test，確認 environment 正常
- 先追求 pipeline 跑通，不追求 SOTA 性能

**Fallback**:
- 分析 reward curve 趨勢（即使未收斂，可討論學習行為）
- 誠實報告 trade-off：分析 throughput / RTT / loss 各自的變化
- 強化 report 中的「limitation 與 future work」section
- **不偽造結果**

**Trigger Condition**: Change 04 的訓練完成後，reward curve 無明顯上升趨勢  
**Owner**: Antigravity（須誠實報告，不得偽造）

---

### R-05: Reward 設計導致高 throughput 但高 RTT / loss

**Description**: Agent 學會用犧牲 RTT 和 loss 換取高 throughput，違反壅塞控制目標。  
**Probability**: Medium  
**Impact**: HIGH — 結果不具壅塞控制意義，report 說服力低  
**Prevention**:
- Reward 必須包含 delay penalty（β·RTT）和 loss penalty（γ·loss）
- 保留每個 reward component 的獨立 log（throughput_reward, rtt_penalty, loss_penalty）
- 比較 utility score 而非只看 throughput

**Fallback**:
- 調整 β、γ 權重（增加懲罰力度）
- 降低 episode 長度，減少 agent 找到 exploitative 策略的機會
- 在 report 中分析 reward component 分解

**Trigger Condition**: Change 04 evaluation 顯示 DQN throughput 高但 RTT 異常（> 2x baseline）  
**Owner**: Antigravity

---

### R-06: Antigravity 自行擴題

**Description**: Antigravity 在未獲 spec owner 批准的情況下，自行新增 IPFS、QUIC、multi-agent、large topology 等研究方向。  
**Probability**: Low（有 OpenSpec governance 管控）  
**Impact**: HIGHEST — 浪費學期時間，偏離驗收目標  
**Prevention**:
- 本 charter 明確列出 Non-goals 和 Strict Non-Goals
- 每個 change 的 tasks.md 只能包含該 change 範圍內的任務
- Antigravity 必須在每次回報中確認 Scope Compliance

**Fallback**:
- 立即停止偏軌的任務
- 回到本 charter 重審 scope boundary
- 刪除或 revert 不在 scope 內的工作

**Trigger Condition**: 任何 task 出現 IPFS/QUIC/multi-agent/multi-path 相關實作  
**Owner**: Antigravity（自我管控）/ Spec Owner（最終決策）

---

### R-07: 題目被誤解為 IPFS 實作

**Description**: 由於背景知識或上下文混淆，任務被誤解為 IPFS 去中心化儲存實作。  
**Probability**: Low（有明確凍結題目）  
**Impact**: HIGHEST — 整學期方向錯誤  
**Prevention**:
- 本 charter 明確寫出「不做 IPFS」
- README 明確列出 Non-goals
- Proposal.md 明確說明 IPFS 只在 motivation/future work 中提及

**Fallback**:
- 立即停止，回到本 charter 確認凍結題目
- 告知 spec owner，確認是否需要澄清說明

**Trigger Condition**: 任何 change 的 tasks 中出現 IPFS、Bitswap、DHT 等字眼  
**Owner**: Spec Owner

---

### R-08: DRL 結果不優於 baseline

**Description**: DQN agent 的 throughput / RTT / utility 全面不優於 NewReno / CUBIC。  
**Probability**: High（DRL 在簡單場景不一定優於精心設計的 TCP）  
**Impact**: LOW — 只要 pipeline 完整、比較誠實，仍是合格的 final project  
**Prevention**:
- 設定合理的 success definition（不要求 DRL 必勝）
- 設計 reward 讓 agent 能學到有意義的 trade-off
- 先確保 pipeline 完整，再談性能

**Fallback**:
- 誠實報告：分析 DQN 在哪些維度接近或優於 baseline
- 在哪些情境（如高 RTT / 高 loss）DQN 可能有相對優勢
- 將「誠實比較 trade-off」作為 report 的核心貢獻之一
- **不偽造結果，不誇大性能**

**Trigger Condition**: Change 04 evaluation 顯示 DQN 在所有 metrics 上均不如 baseline  
**Owner**: Antigravity

---

### R-09: 實驗圖表不足以支撐簡報

**Description**: 產出的圖表數量或品質不足，無法清楚說明實驗結果。  
**Probability**: Medium  
**Impact**: MEDIUM — 簡報評分受影響  
**Prevention**:
- 預先定義至少 8 張必要圖表（見 proposal 規格）
- 每個 change 的 tasks.md 包含圖表產出任務
- 使用 matplotlib / seaborn 產出高品質圖表

**Fallback**:
- 即使 DRL 結果不佳，仍可用 baseline 比較圖、MDP diagram、topology diagram 填充簡報
- 增加 qualitative analysis（文字分析）補充量化圖表不足

**Trigger Condition**: Change 05 完成後，圖表數量 < 6 或圖表解析度 / 標注不符標準  
**Owner**: Antigravity

---

### R-10: OpenSpec 文件與實作脫節

**Description**: OpenSpec 的 tasks.md 顯示完成，但實際程式碼不符合 spec.md 的要求。  
**Probability**: Low  
**Impact**: MEDIUM — 導致驗收困難  
**Prevention**:
- 每個 task 完成後立即用 `openspec status` 確認
- spec.md 中的 Acceptance Criteria 必須逐項驗證
- 不得在未完成的情況下勾選 `[x]`

**Fallback**:
- 回到 tasks.md，重新確認每個已勾選的 task
- 更新 tasks.md 反映實際狀態

**Trigger Condition**: spec owner 驗收時發現 task 標記 [x] 但實際輸出不符合  
**Owner**: Antigravity

---

### R-11: 使用假 OpenSpec / 模擬 OpenSpec workflow

**Description**: 未安裝官方 `@fission-ai/openspec` 套件，而是自行建立類似 OpenSpec 的資料夾結構，宣稱已使用 OpenSpec。  
**Probability**: Low（已驗證）  
**Impact**: HIGHEST — 整個 SDD workflow 失去可信度，違反本專案的最高優先規則

**⚠️ 嚴格處理程序**：

若發現此情況：
1. **立即停止所有實作任務**
2. **向 spec owner 明確回報**：「本專案發現使用假 OpenSpec，尚未真正完成 OpenSpec setup」
3. **重新執行官方安裝**：`npm install -g @fission-ai/openspec@latest`
4. **重新初始化**：`openspec init --tools antigravity`
5. **驗證**：`openspec --version`、`.agent/skills/` 和 `.agent/workflows/` 必須存在
6. **等待 spec owner 確認後才能繼續**

**Current Status**: 🟢 **MITIGATED** — 已確認使用官方 `@fission-ai/openspec@1.4.1`，`openspec status` 顯示 4/4 artifacts complete  
**Owner**: Antigravity（自我審查）/ Spec Owner（最終確認）

---

### R-12: 未使用官方 OpenSpec CLI 卻宣稱完成 OpenSpec change

**Description**: 未執行 `openspec new change`、`openspec instructions`、`openspec status` 等官方 CLI 指令，僅手動建立檔案，宣稱已完成 OpenSpec change。  
**Probability**: Low（已驗證）  
**Impact**: HIGHEST — 與 R-11 同等嚴重，違反本專案的核心原則

**⚠️ 嚴格處理程序**：同 R-11

**Verification Evidence（已可驗證）**:
- `openspec --version` → `1.4.1`
- `npm list -g @fission-ai/openspec --depth=0` → `@fission-ai/openspec@1.4.1`
- `openspec new change "project-charter"` → 官方 CLI 建立 change 目錄
- `openspec instructions proposal/design/specs/tasks` → 官方 CLI 提供 artifact 建立指引
- `openspec status --change "project-charter"` → `4/4 artifacts complete`
- `.agent/skills/openspec-*/SKILL.md` → 5 個官方 Antigravity skill 檔案
- `.agent/workflows/opsx-*.md` → 5 個官方 workflow 檔案（含 v1.4.1 新增的 opsx-sync.md）

**Current Status**: 🟢 **VERIFIED** — 所有官方 CLI 指令均已執行並可驗證  
**Owner**: Antigravity（自我審查）/ Spec Owner（最終確認）
