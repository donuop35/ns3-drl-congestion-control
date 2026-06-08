## Purpose

定義 Change 02 baseline benchmark 使用的 TCP congestion control methods 及其角色與 fallback 規則。

---

## Required Baselines

以下兩個演算法為 **MVP-required**，在任何情況下均必須完成：

| Baseline | RFC | 角色 | 狀態 |
|---------|-----|------|------|
| **NewReno** | RFC 6582 | Loss-based AIMD，保守基準 | Required |
| **CUBIC** | RFC 8312 | Linux 預設，cubic growth，loss-based | Required |

---

## Strongly Recommended Baseline

| Baseline | 來源 | 角色 | 狀態 |
|---------|------|------|------|
| **BBR** | Google 2016 | Model-based，bandwidth + min-RTT estimation | Strongly preferred，non-blocking |

BBR 的引入條件（per D-04）：
1. ns-3.40 中 `TcpBbr` class 可用且可編譯
2. 整合成本 ≤ 0.5 個工作日

---

## Optional Baselines

以下演算法**不在 MVP 範圍內**，需要 Spec Owner 明確批准才能加入：

- Vegas
- Westwood
- DCTCP
- LEDBAT

---

## Exclusion Rules

以下絕對不得作為本 change 的 baseline：

> ⛔ **QUIC congestion control** — 不在本專題 scope 內  
> ⛔ **IPFS traffic pattern** — 無直接關聯  
> ⛔ **Pantheon full integration** — 安裝複雜，非 MVP 必要；僅可參考其 benchmark 哲學  
> ⛔ **Production transport protocols** — 非學術研究目標  
> ⛔ **任何額外 baseline（未經 Spec Owner 批准）**

---

## BBR Fallback Rule

若 BBR 在 ns-3.40 中不可用或整合成本超過 0.5 工作日：

1. MVP 以 **NewReno + CUBIC** 完成，不得等待 BBR
2. 必須建立 `experiments/results/BBR_SKIPPED.md`，記錄：
   - ns-3.40 BBR 不可用的原因
   - 是否可在 future work 中補充
3. 所有 figures 和 tables 只顯示可用的演算法，並標註 BBR 缺席原因
4. 不得因 BBR 缺席而宣告 Change 02 失敗

---

## ns-3 Implementation Note

> **目標版本**：ns-3.40（Spec Owner 正式凍結，OQ-02.01, 2026-06-08）  
> **TCP 模組**：ns-3 內建 `TcpNewReno`、`TcpCubic`、`TcpBbr`（需確認版本可用）  
> **不得修改 ns-3 kernel**：所有 TCP 演算法必須使用 ns-3 內建實作，不得 patch kernel TCP
