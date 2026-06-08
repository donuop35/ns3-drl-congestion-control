## Purpose

定義 Change 03 opengym-env 的 reward function 規格，包含 reward philosophy、base reward concept、normalization philosophy、已知 failure modes 與 future ablation plan。

Reward 的具體 weight（α, β, λ）在本 change 不固定；Change 04 定義初始值，Change 05 可依 Spec Owner approval 調整。

---

## Base Reward Concept

```
r_t = α · throughput_norm_t − β · delay_norm_t − λ · loss_norm_t
```

> **⚠️ 重要符號說明**：Loss 懲罰使用 **λ（lambda）** 而非 γ，以避免與 RL discount factor γ（gamma）混淆。

### 符號解釋

| 符號 | 名稱 | 說明 |
|------|------|------|
| `r_t` | Step reward | 第 t 個 decision step 的即時 reward |
| `α` | Throughput weight | Throughput 的正向激勵權重；值越大，agent 越重視吞吐量提升 |
| `β` | Delay penalty weight | Delay 的懲罰強度；值越大，agent 越傾向降低延遲 |
| `λ` | Loss penalty weight | Packet loss 的懲罰強度；值越大，agent 越傾向避免封包丟失 |
| `throughput_norm_t` | 歸一化 throughput | `throughput_mbps / link_bw_mbps`，bounded to [0, 1] |
| `delay_norm_t` | 歸一化 delay | `avg_delay_ms / max_expected_delay_ms`，bounded to [0, 1] |
| `loss_norm_t` | 歸一化 loss | Packet loss rate [0, 1]，自然有界 |

---

## Weight Status（Provisional）

> **⚠️ α, β, λ 的數值在本 change 不固定。**

| 權重 | 本 change 的狀態 | 誰來定義 |
|------|-----------------|---------|
| α | **Provisional** | Change 04 定義初始值（e.g., α = 1.0） |
| β | **Provisional** | Change 04 定義初始值（e.g., β = 0.1） |
| λ | **Provisional** | Change 04 定義初始值（e.g., λ = 10.0）；與 Change 02 utility score 的 loss 係數參考對齊 |

Change 04 中定義的初始值可在 Change 05 中依 ablation study 結果調整，但**必須獲得 Spec Owner approval**。

---

## Normalization Philosophy

Reward 的三個 component 必須在相同 scale 上才能有意義地加權：

1. **Throughput / delay / loss 的量綱不同**（Mbps vs. ms vs. fraction），不能直接比較
2. **Normalization 是必要條件**：所有 component 必須歸一化後才能使用 α, β, λ 加權
3. **Weights are not fixed here**：本 change 定義 normalization 方式，不固定 weight 數值
4. **04-drl-mvp 定義初始 weights**：DQN training 開始時使用的 α, β, λ 在 Change 04 中記錄
5. **Evaluation with independent metrics**：最終 evaluation 仍需使用獨立的 throughput / RTT / loss 數值，不得只看 cumulative reward

---

## Reward Failure Modes

以下是已知的 reward design failure modes，必須在 Change 04 implementation 中避免：

### FM-01：Throughput-Only Reward

```
r_t = throughput_norm_t  ← FORBIDDEN
```

- **問題**: Agent 可能透過增加 retransmission 或忽略 delay / loss 來最大化 throughput
- **後果**: Agent 可能學到對網路有害的策略（e.g., buffer bloat）
- **防範**: Reward 必須包含 delay 和 loss component

### FM-02：Over-Penalized Delay

```
r_t = α · throughput_norm − 10.0 · delay_norm − ...  ← WARNING
```

- **問題**: 過大的 β 會使 agent 過度保守，throughput 嚴重下降
- **防範**: α, β, λ 的初始值在 Change 04 中調整；必須做 ablation study

### FM-03：Over-Penalized Loss

```
r_t = ... − 100.0 · loss_norm  ← WARNING
```

- **問題**: 過大的 λ 會使 agent 幾乎不發送任何封包（throughput ≈ 0）
- **防範**: Loss penalty 要有上限；初始 λ 建議在 1.0–20.0 之間

### FM-04：Unstable Reward Scale

- **問題**: 若 normalization 不一致，reward 範圍在不同 scenario 下差異極大，導致 DQN training 不穩定
- **防範**: 確保 normalization 公式在所有 scenario 下一致；考慮 reward clipping

### FM-05：Sparse Reward

- **問題**: 若 step 太短且 network effect 滯後，agent 難以關聯 action 與 reward
- **防範**: Decision interval 不得過短；至少 1 秒以上，讓 network effect 可觀測

---

## Relationship to Baseline Utility Score

Change 02 已定義 baseline utility score（provisional）：

```
utility_score = throughput_norm − 0.1 × rtt_norm − 10.0 × loss_rate
```

本 change 的 reward 概念與 utility score 有以下關係：

- **相同的 component**：throughput / delay / loss 三個維度
- **不同的用途**：utility score 是 baseline comparison 的 visualization metric；reward 是 training signal
- **Weights 可能不同**：Training 最佳的 α, β, λ 未必等於 utility score 的 0.1 和 10.0
- **不得直接用 utility_score 作為 reward**（除非 Change 04 明確決定並獲 Spec Owner 批准）

---

## Future Ablation Plan

Change 05（reporting）應包含 reward ablation study，比較以下設定：

| 設定名稱 | Reward formula | 目的 |
|---------|---------------|------|
| **Throughput-only** | `r = throughput_norm` | Ablation baseline（不推薦但需比較）|
| **Throughput + Delay** | `r = α·t_norm − β·d_norm` | 去除 loss penalty 後的效果 |
| **Full reward** | `r = α·t_norm − β·d_norm − λ·l_norm` | 推薦設定 |

> Note: Ablation study 在 Change 05 中執行，不在本 change 中執行。
