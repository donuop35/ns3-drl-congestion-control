# Deep Reinforcement Learning for Congestion Control 🚀

> **以深度強化學習進行單一瓶頸鏈路壅塞控制與吞吐量最佳化**
>
> **Project Status:** 📝 *Proposal Stage / OpenSpec Preview* (No implementation yet)

<div align="center">
  <a href="https://www.youtube.com/watch?v=3cu1WZz_k8M">
    <img src="https://img.youtube.com/vi/3cu1WZz_k8M/maxresdefault.jpg" alt="Proposal Presentation Video" width="800" style="border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
  </a>
  <br>
  <a href="https://www.youtube.com/watch?v=3cu1WZz_k8M">
    <img src="https://img.shields.io/badge/YouTube-Watch_Video-red?style=for-the-badge&logo=youtube" alt="Watch on YouTube">
  </a>
</div>

---

## 📌 Project Overview

This project aims to formalize network **Congestion Control** as a sequential decision-making problem using **Deep Reinforcement Learning (DRL)**. 

Instead of relying on rigid, rule-based heuristics (like traditional TCP algorithms such as NewReno or CUBIC), we introduce a DRL Agent. The agent dynamically adjusts transmission strategies at the sender side by observing real-time network states. Our core focus is not just maximizing throughput blindly—which often leads to severe bufferbloat—but finding the optimal dynamic **trade-off** between **Throughput**, **Round-Trip Time (RTT)**, and **Packet Loss**.

**Current Target Scope:** A single sender-to-receiver bottleneck link simulated in `ns-3`.

## 🧠 MDP Specification (Markov Decision Process)

To make congestion control learnable, we formulated the environment as an MDP $M = (S, A, P, R, \gamma)$:

- 👁️ **State Space ($S$)**: `[Throughput, RTT, Loss Rate, Congestion Indicator, Previous Action]`
- 🕹️ **Action Space ($A$)**: Discrete control choices: `{Decrease, Keep, Increase}` (adjusting sending rate or cwnd).
- 🏆 **Reward Function ($R$)**: $r_t = \alpha T_t - \beta RTT_t - \lambda L_t$ 
  *(Rewards high throughput $T_t$ while heavily penalizing latency spikes $RTT_t$ and packet drops $L_t$.)*
- 🌍 **Environment ($P$)**: Pure physical network dynamics handled by the `ns-3` network simulator via the `ns3-gym` interface.

## ⚙️ Spec-Driven Development Workflow

We refuse to jump straight from "idea" to "coding". This project strictly adheres to a **Spec-driven Development Pipeline**.

```text
PPT Proposal 
  ↓
NotebookLM PDR (Product Design Review) & Infographic
  ↓
OpenSpec Preview (Decomposing PDR into changes)
  ↓
task.md Draft (Actionable steps)
  ↓
🤖 Future Antigravity Implementation
```

**Core Principle:** `PLAN → APPLY → VERIFY`
Every upcoming phase must define the scope, apply the changes, and verify the outputs against baseline benchmarks (TCP NewReno, CUBIC, BBR) before advancing.

---

## 📂 Repository Structure & Deliverables

This repository currently holds the **Proposal Stage Materials**.

- **`proposal/`**: The origin of the idea. Contains the [Proposal Slides (PDF)📄](proposal/final-project-proposal-slides.pdf) and PPTX.
- **`pdr/`**: The formalized specification. Contains the [PDR Integrated Report 📘](pdr/PDR_integrated.pdf) detailing the experiment matrix and risk registers.
- **`openspec-preview/`**: The AI execution roadmap. Contains [OpenSpec Roadmap](openspec-preview/openspec-roadmap.md) and task drafts.
- **`docs/`**: Objective evidence and related work group analysis.
- **`assets/`**: System infographics and visual materials.

> [!WARNING]
> **Scope Note:** This repository currently contains proposal-stage materials only. Formal OpenSpec initialization, `ns-3` setup, and DQN model implementation will begin in **Phase 2**. 
> *IPFS, QUIC, multi-agent reinforcement learning, and real-internet deployments are explicitly out of scope for the current MVP.*