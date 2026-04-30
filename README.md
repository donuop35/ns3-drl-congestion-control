# Deep Reinforcement Learning for Congestion Control 🚀

> **以深度強化學習進行單一瓶頸鏈路壅塞控制與吞吐量最佳化**
>
> **專案狀態:** 📝 *提案階段 (Proposal Stage) / OpenSpec 預覽* (尚未開始程式實作)

<div align="center">
  <a href="https://www.youtube.com/watch?v=3cu1WZz_k8M">
    <img src="https://img.youtube.com/vi/3cu1WZz_k8M/maxresdefault.jpg" alt="Proposal Presentation Video" width="800" style="border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
  </a>
  <br>
  <a href="https://www.youtube.com/watch?v=3cu1WZz_k8M">
    <img src="https://img.shields.io/badge/YouTube-觀看簡報影片-red?style=for-the-badge&logo=youtube" alt="Watch on YouTube">
  </a>
</div>

---

## 📌 專案概述 (Project Overview)

本專案旨在將網路傳輸中的**壅塞控制 (Congestion Control)** 形式化為一個**深度強化學習 (Deep Reinforcement Learning, DRL)** 的序列決策問題。

有別於傳統依賴固定規則或啟發式邏輯的 TCP 演算法 (如 NewReno 或 CUBIC)，我們在此引入了 DRL 智慧體 (Agent)。該智慧體會根據即時觀測到的網路狀態，動態調整傳送端的傳輸策略。我們的核心目標並非盲目地最大化吞吐量 (這往往會導致嚴重的緩衝區滿載 Bufferbloat)，而是要在**吞吐量 (Throughput)**、**往返延遲 (RTT)** 與**封包遺失率 (Packet Loss)** 之間，找出最佳的動態**權衡 (Trade-off)**。

**目前的目標範圍：** 於 `ns-3` 模擬環境中建立單一傳送端至接收端的瓶頸鏈路 (Single bottleneck link)。

## 🧠 MDP 規格 (Markov Decision Process)

為了讓壅塞控制具備可學習性，我們將環境建模為馬可夫決策過程 (MDP) $M = (S, A, P, R, \gamma)$：

- 👁️ **狀態空間 (State Space, $S$)**: `[近期吞吐量, 往返延遲 (RTT), 丟包訊號, 壅塞指標, 上一步的動作]`
- 🕹️ **動作空間 (Action Space, $A$)**: 離散控制選擇：`{減少 (Decrease), 維持 (Keep), 增加 (Increase)}` (用於調整傳送速率或壅塞視窗)。
- 🏆 **獎勵函數 (Reward Function, $R$)**: $r_t = \alpha T_t - \beta RTT_t - \lambda L_t$ 
  *(給予高吞吐量 $T_t$ 正向獎勵，同時針對高延遲 $RTT_t$ 與網路丟包 $L_t$ 施加嚴厲懲罰。)*
- 🌍 **環境動態 (Environment, $P$)**: 實體的網路動態由 `ns-3` 網路模擬器處理，並透過 `ns3-gym` 介面與智慧體互動。

## ⚙️ 規格驅動開發工作流 (Spec-Driven Workflow)

我們拒絕從「概念」直接跳入「撰寫程式碼」。本專案嚴格遵循**規格驅動開發 (Spec-driven Development)** 的流程。

```text
PPT 概念提案 
  ↓
NotebookLM PDR (產品設計規格書) 與 資訊圖表
  ↓
OpenSpec 預覽 (將 PDR 拆解為具體的變更任務)
  ↓
task.md 任務草案 (可執行的開發步驟)
  ↓
🤖 未來交由 Antigravity 進行實作
```

**核心原則：** `PLAN (計畫) → APPLY (實作) → VERIFY (驗證)`
在未來的每一個開發階段，都必須先定義範圍、實作變更，並在進入下一階段前，確實與基礎基準線 (TCP NewReno, CUBIC, BBR) 進行成效驗證。

---

## 📂 Repository 目錄結構與交付物

本 Repository 目前存放的是**提案階段 (Proposal Stage)** 的相關文件。

- **`proposal/`**: 概念提案的起源。包含 [Proposal 簡報 PDF📄](proposal/final-project-proposal-slides.pdf) 與 PPTX 原始檔。
- **`pdr/`**: 形式化的規格書。包含 [PDR 整合報告 📘](pdr/PDR_integrated.pdf) (詳細說明實驗矩陣與風險評估)。
- **`openspec-preview/`**: AI 執行的路線圖草案。包含 [OpenSpec Roadmap](openspec-preview/openspec-roadmap.md) 與工作清單草案。
- **`docs/`**: 客觀證據對照表與相關研究群組分析。
- **`assets/`**: 系統資訊圖表與視覺資源。

> [!WARNING]
> **範圍邊界聲明 (Scope Note)：**
> 本 Repository 目前僅包含提案階段的素材。正式的 OpenSpec 初始化、`ns-3` 環境建置與 DQN 模型實作將於 **Phase 2** 展開。
> *IPFS、QUIC、多智慧體強化學習 (Multi-agent RL) 以及真實網際網路部署，已明確排除於本次的 MVP 實作範圍之外。*