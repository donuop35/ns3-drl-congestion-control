# OpenSpec Roadmap

## Project

**Deep Reinforcement Learning for Congestion Control and Throughput Optimization over a Single Bottleneck Link**

中文題目：**以深度強化學習進行單一瓶頸鏈路壅塞控制與吞吐量最佳化**

---

## Purpose

This document summarizes how the proposal-stage PDR will be converted into an OpenSpec-driven implementation workflow.

This is an **OpenSpec preview**, not the formal `openspec/` directory. Formal OpenSpec initialization will begin in **Phase 2** after proposal submission.

本文件用途是讓教授、助教與後續 Antigravity 實作流程能快速理解：本專題如何從 Proposal PPT 與 PDR，轉換為後續可執行、可驗收、可追蹤的 Spec-driven Development pipeline。

---

## Workflow Overview

```text
Proposal PPT
  ↓
NotebookLM PDR / Infographic
  ↓
OpenSpec Preview
  ↓
task.md Draft
  ↓
Future Antigravity Implementation
```

核心原則：

```text
PLAN → APPLY → VERIFY
```

本專題不會直接從概念跳到 code，而是先透過 PDR 凍結研究範圍、方法設計、MDP 規格、baseline、metrics、experiment matrix 與風險控管，再於 Phase 2 轉入 OpenSpec changes。

---

## Professor Whiteboard Workflow Mapping

| Professor Workflow | Project Mapping | Current Status |
|---|---|---|
| PPT → PDF | Final Proposal PPT exported as PDF | Completed |
| PDF → NotebookLM | NotebookLM used to generate PDR and infographic | Completed |
| NotebookLM → PDR report / charts | PDR report, objective evidence table, experiment matrix, risk register | Completed |
| PDR → OpenSpec | PDR will be decomposed into OpenSpec changes | Preview completed |
| OpenSpec → task.md | Each change will produce a task checklist | Draft completed |
| task.md → code | Antigravity will implement after specs are approved | Future work |
| PLAN → APPLY → VERIFY | Every implementation step must follow spec-first workflow | Required |

---

## Planned OpenSpec Changes

| Change ID | Purpose | Main Output | Status |
|---|---|---|---|
| `01-project-charter` | Freeze topic, scope, non-goals, risks, and project boundaries | project charter / scope rules | Preview |
| `02-ns3-baseline-benchmark` | Build single bottleneck ns-3 baseline with TCP variants | baseline logs / figures | Future |
| `03-ns3-gym-environment` | Build RL environment interface between ns-3 and Gym | observation / action / reward interface | Future |
| `04-dqn-mvp-agent` | Train and evaluate a discrete-action DQN MVP agent | reward curve / action logs / evaluation outputs | Future |
| `05-reporting-figures-demo` | Produce final figures, README, demo materials, and report artifacts | final reporting package | Future |

---

## Change Dependency Order

```text
01-project-charter
  ↓
02-ns3-baseline-benchmark
  ↓
03-ns3-gym-environment
  ↓
04-dqn-mvp-agent
  ↓
05-reporting-figures-demo
```

Dependency rule:

- `01-project-charter` must be completed before any implementation-oriented change.
- `02-ns3-baseline-benchmark` must be completed before RL environment and DQN work.
- `03-ns3-gym-environment` must define observation, action, reward, and environment stepping behavior before `04-dqn-mvp-agent` starts.
- `04-dqn-mvp-agent` must not claim outperforming TCP baselines by default; it should output logs and figures for analysis.
- `05-reporting-figures-demo` depends on all prior outputs.

---

## Change 01 — Project Charter

### Purpose

Freeze the project direction before implementation begins.

### Scope

- Confirm final project title.
- Confirm single bottleneck link as the only MVP scenario.
- Confirm proposal-stage status.
- Confirm baseline, metrics, risk boundaries, and future work.

### Main Outputs

- Project charter.
- Scope and non-scope rules.
- Risk boundary.
- Acceptance criteria for proceeding to baseline work.

### Verification

- The project remains about DRL congestion control over a single bottleneck link.
- No implementation work starts before scope is approved.

---

## Change 02 — ns-3 Baseline Benchmark

### Purpose

Establish reproducible TCP baseline evaluation before introducing DRL.

### Planned Baselines

- NewReno
- CUBIC
- BBR, if supported by the selected ns-3 version and configuration

### Planned Metrics

- Average throughput
- Average RTT
- Packet loss rate
- Utility score
- Baseline logs and figures

### Verification

- Baseline simulations can generate analyzable logs.
- At least NewReno and CUBIC should be treated as required baselines.
- BBR may remain a strong optional baseline if version/configuration risk is high.

---

## Change 03 — ns3-gym Environment

### Purpose

Expose the ns-3 single bottleneck simulation as an RL environment.

### Planned Environment Design

- Observation/state: recent throughput, RTT, loss signal, congestion indicator, previous action.
- Action: decrease / keep / increase sending rate or cwnd-like control.
- Reward: balance throughput, RTT, and loss.
- Transition: determined by ns-3 network dynamics.

### Verification

- Environment reset and step behavior are defined.
- A random or simple policy can interact with the environment.
- Logs are sufficient for later training and debugging.

---

## Change 04 — DQN MVP Agent

### Purpose

Implement a minimal discrete-action DRL agent for congestion-control behavior analysis.

### Planned Agent

- Stable-Baselines3 DQN.
- Discrete actions: decrease / keep / increase.
- Reward function:

```text
r_t = αT_t − βRTT_t − λL_t
```

### Verification

- Future implementation should complete train/eval pipeline and output reward curve, action logs, and evaluation logs.
- Whether the agent converges or outperforms baselines must be treated as an evaluation result, not a proposal-stage promise.

---

## Change 05 — Reporting, Figures, and Demo

### Purpose

Convert experimental outputs into final report artifacts.

### Planned Outputs

- Final figures.
- Result summary tables.
- README update.
- Demo / presentation materials.
- GitHub documentation.

### Verification

- All figures must be traceable to logged outputs.
- Results should analyze throughput–RTT–loss trade-off rather than claiming DRL is always superior.

---

## Scope Boundary

This proposal does **not** implement the following in the MVP:

- IPFS implementation
- QUIC implementation
- kernel-level TCP modification
- multi-agent reinforcement learning
- multi-path routing
- real Internet deployment

These directions may be treated as future work after the single bottleneck ns-3 DRL prototype is validated.

---

## Repository Placement

During proposal submission, this file should be placed at:

```text
openspec-preview/openspec-roadmap.md
```

It should not be placed under the formal `openspec/` directory yet.

Recommended related files:

```text
pdr/PDR_integrated.md
pdr/PDR_integrated.pdf
openspec-preview/task-md-draft.md
openspec-preview/antigravity-instruction-draft.md
```

---

## Notes for Antigravity

Antigravity should treat this roadmap as a planning document only. It must not start coding directly from this file.

Implementation must begin only after formal OpenSpec initialization in Phase 2. All changes must follow:

```text
PLAN → APPLY → VERIFY
```

Any scope change must return to the spec owner before implementation proceeds.
