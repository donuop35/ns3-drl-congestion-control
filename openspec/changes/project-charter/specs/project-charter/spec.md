## ADDED Requirements

### Requirement: Project Title and Research Goal are frozen
The system (this project) SHALL be identified by the following fixed title and research goal for the entire semester. No change to the title, thesis, or core research direction is permitted without explicit Spec Owner approval.

**Project Title (Chinese)**: 以深度強化學習進行單一瓶頸鏈路壅塞控制與吞吐量最佳化  
**Project Title (English)**: Deep Reinforcement Learning for Congestion Control and Throughput Optimization over a Single Bottleneck Link  
**GitHub Title**: DRL-Based Congestion Control over a Bottleneck Link  
**Thesis Statement**: 本研究將單一瓶頸鏈路的壅塞控制建模為深度強化學習問題，透過 ns-3 / ns3-gym 建立可重現的網路模擬環境，讓 agent 學習在 throughput、RTT 與 packet loss 之間取得更好的控制折衷，並與傳統 TCP baseline 進行比較。

#### Scenario: Title is referenced in all deliverables
- **WHEN** any deliverable (README, PPT, report, figure) is created
- **THEN** it MUST use the frozen project title as defined above without modification

---

### Requirement: MVP scope is defined and frozen
The project SHALL complete exactly the following five OpenSpec changes in order. Additional changes require Spec Owner approval.

**Change sequence**:
1. `project-charter` — Research direction freezing and charter document (**this change**)
2. `ns3-baseline-benchmark` — ns-3 single bottleneck TCP baseline (NewReno, CUBIC, optional BBR)
3. `ns3-gym-environment` — ns3-gym RL environment with smoke test
4. `dqn-mvp-agent` — Stable-Baselines3 DQN training and evaluation
5. `reporting-figures-and-demo` — Final deliverables, figures, README, PPT assets

#### Scenario: Change execution order is enforced
- **WHEN** a new change is proposed
- **THEN** it MUST only begin after the preceding change is complete and confirmed by Spec Owner

#### Scenario: Non-MVP work is blocked
- **WHEN** any task involves IPFS, QUIC, multi-agent RL, Linux kernel modification, large topology, or real Internet deployment
- **THEN** the implementation agent MUST stop and report to Spec Owner before proceeding

---

### Requirement: Toolchain is frozen
The project SHALL use the following toolchain. No alternatives may be substituted without Spec Owner approval.

| Component | Tool | Version Constraint |
|-----------|------|-------------------|
| Simulator | ns-3 | >= 3.32 (BBR support) |
| RL Interface | ns3-gym | Latest compatible with target ns-3 |
| RL Framework | Stable-Baselines3 | >= 1.8.0 |
| MVP Algorithm | DQN | Stable-Baselines3 DQN |
| Analysis | Python 3.9+ | numpy, pandas, matplotlib |
| Spec Management | OpenSpec | v1.4.1 (installed) |

#### Scenario: Alternative tool is proposed
- **WHEN** the implementation agent proposes using a tool not in the frozen toolchain
- **THEN** it MUST present the proposal to Spec Owner and wait for approval before installing or using it

---

### Requirement: MDP formulation initial version is defined
The project SHALL model congestion control as an MDP with the following initial definition. Changes to MDP structure require design.md update and Spec Owner confirmation.

**Environment**: Single bottleneck link: `sender → bottleneck link → receiver`  
**Agent**: DRL congestion-control agent selecting discrete rate-control actions  
**Observation (initial)**: `[throughput_norm, rtt_norm, loss_rate, cwnd_signal_norm]` (4-dimensional)  
**Action space**: Discrete(3) — {0: decrease, 1: keep, 2: increase}  
**Reward**: `r_t = α·throughput_t − β·RTT_t − γ·loss_t` (α, β, γ TBD by smoke test)  
**Episode length**: 60s (initial, may adjust after smoke test)  
**Decision interval**: 500ms (initial, may adjust after smoke test)

#### Scenario: Observation definition matches design
- **WHEN** the ns3-gym environment is implemented
- **THEN** each observation dimension MUST be documented in Change 03 design.md with: name, unit, source, sampling interval, normalization method

#### Scenario: Action space remains discrete for MVP
- **WHEN** implementing the DQN agent
- **THEN** the action space MUST remain Discrete(3) unless Spec Owner explicitly approves a continuous action space

#### Scenario: Reward does not optimize throughput alone
- **WHEN** the reward function is implemented
- **THEN** it MUST include at least one delay or loss penalty term, and MUST NOT be a pure throughput maximization objective

---

### Requirement: Baselines are defined and must be run before DRL
The project SHALL complete TCP baseline benchmarks BEFORE any RL environment or DRL training begins.

**Required baselines**: NewReno, CUBIC  
**Strongly preferred**: BBR (if ns-3 version supports it and integration cost is acceptable)  
**Blocking rule**: BBR MUST NOT block Change 02 completion if integration takes > 1 working day

#### Scenario: Baselines produce reproducible output
- **WHEN** baseline benchmarks are run
- **THEN** they MUST produce CSV logs for throughput, RTT, and packet loss; and MUST use fixed random seeds specified in `experiments/configs/`

#### Scenario: BBR is optional
- **WHEN** BBR integration fails after 1 working day of effort
- **THEN** BBR MUST be moved to optional/future work and documented in Change 02 README

---

### Requirement: Metrics are defined and must be produced
The project SHALL produce the following metrics for both baseline and DRL evaluation.

**Required metrics**:
1. Average throughput (Mbps)
2. Average RTT (ms)
3. Packet loss rate (%)
4. Utility score (composite metric)
5. Reward curve (DRL training)
6. Baseline comparison table

**Optional metrics**: Queue occupancy, Jain's fairness index, convergence stability

#### Scenario: Utility score is defined before comparison
- **WHEN** producing baseline vs. DRL comparison
- **THEN** utility score formula MUST be defined in design.md and applied consistently to both baseline and DRL results

---

### Requirement: Experiment scenarios are defined
The project SHALL run experiments in at least 2 of the following 3 scenarios.

**Scenario A (required)**: Stable low-latency bottleneck — baseline bandwidth 10 Mbps, RTT 20ms, no background traffic  
**Scenario B (required)**: Stable high-latency bottleneck — baseline bandwidth 10 Mbps, RTT 100ms, no background traffic  
**Scenario C (optional)**: Dynamic/disturbed bottleneck — varying background traffic or link capacity changes  

#### Scenario: All experiments use fixed random seeds
- **WHEN** any experiment (baseline or DRL) is run
- **THEN** the random seed MUST be fixed and recorded in `experiments/configs/<scenario-name>.yaml`

#### Scenario: Scenario C does not block MVP
- **WHEN** Scenario C integration cost is high
- **THEN** it MUST be deferred to optional/future work without blocking Changes 02–05

---

### Requirement: Final deliverables are defined
The project SHALL produce the following final deliverables to be considered complete.

**Required deliverables**:
1. GitHub repository with complete README (reproducible by third party)
2. Baseline benchmark results (CSV + figures)
3. ns3-gym smoke test log
4. DQN training reward curve
5. DRL vs. baseline comparison figure
6. Throughput / RTT / loss / utility comparison table
7. Network topology diagram
8. MDP diagram (state / action / reward)
9. Final report outline
10. PPT/slide assets
11. 10-minute demo script

#### Scenario: DRL underperforms baseline
- **WHEN** DQN results do not outperform TCP baselines
- **THEN** the agent MUST produce honest trade-off analysis and MUST NOT fabricate or exaggerate results

#### Scenario: Repository is reproducible
- **WHEN** a third party follows the README
- **THEN** they MUST be able to reproduce the baseline benchmark and DQN smoke test without additional undocumented steps

---

### Requirement: Non-goals are enforced throughout the project
The project MUST NOT include the following in any change implementation without explicit Spec Owner approval.

**Forbidden without approval**:
- IPFS implementation
- Bitswap modification
- DHT experiments
- libp2p node experiments
- Blockchain network protocol
- QUIC congestion control
- Linux kernel TCP stack modification
- Real Internet deployment
- Multi-agent RL
- Large-scale topology (> sender + bottleneck + receiver)
- Multi-path transmission
- Distributed node systems
- Pantheon as mandatory dependency
- Claiming DRL universally outperforms all TCP baselines

#### Scenario: Forbidden item is proposed
- **WHEN** any forbidden item appears in a task or is proposed for implementation
- **THEN** the implementation agent MUST stop immediately and report to Spec Owner before any action
