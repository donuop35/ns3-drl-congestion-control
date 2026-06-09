# Specification: PPT Package

**Target Location:** `slides/final/final-presentation-outline.md` and `slides/final/speaker-notes.md`

## ADDED Requirements

### Req 1: Define PPT Package
The presentation must be timed for a 10-minute presentation and contain exactly 10-12 slides.

#### Scenario: Creating the slide deck
Given the finalized figures and project constraints
When the presenter creates the slide deck
Then it must adhere to the Slide-by-Slide Structure.

## 1. Slide Deck Requirements
- Each slide must focus on a single, clear message.
- Visuals must be drawn from the `figures/final/` package.
- The deck must prominently feature honest limitations and avoid any overclaiming of the DRL's performance.

## 2. Slide-by-Slide Structure

### Slide 1: Title
- **Objective:** Introduce the project.
- **Key Message:** Deep Reinforcement Learning for Congestion Control over a Single Bottleneck Link.
- **Visual:** Project logo / simple topology.
- **Forbidden:** Claims of "production-ready TCP" or "universal solution".

### Slide 2: Motivation
- **Objective:** Explain why this matters.
- **Key Message:** Traditional TCP uses hand-crafted rules; DRL offers an adaptive approach balancing throughput, delay, and loss.

### Slide 3: Research Question & Scope
- **Objective:** Define what we did and didn't do.
- **Key Message:** Single bottleneck link, DQN MVP, comparison against NewReno, CUBIC, BBR.
- **Forbidden:** IPFS, QUIC, multi-agent, multi-path.

### Slide 4: System Architecture
- **Objective:** Show the toolchain.
- **Key Message:** Integration of ns-3.40, ns3-gym, and Stable-Baselines3.
- **Visual:** `system_pipeline.png`

### Slide 5: MDP Formulation
- **Objective:** Explain the RL environment.
- **Key Message:** State (5 metrics), Action (Discrete 3: decrease/keep/increase), Reward (throughput vs delay/loss).
- **Visual:** `mdp_formulation.png`

### Slide 6: Baseline Benchmark
- **Objective:** Establish the performance floor.
- **Key Message:** Phase 3 baselines show how TCP behaves in S1 (low delay) and S2 (high delay).

### Slide 7: DRL MVP Implementation
- **Objective:** Prove the agent works.
- **Key Message:** Trained DQN for 30k steps. Real-ZMQ smoke tests passed.
- **Visual:** `dqn_reward_curves_s1_s2.png`

### Slide 8: Main Results — S1
- **Objective:** Show S1 performance.
- **Key Message:** In a low-delay environment, DQN achieves high utility (2nd place), finding a degenerate near-capacity policy (100% increase actions).
- **Visual:** `dqn_vs_baseline_utility_s1_s2.png` (S1 portion)
- **Forbidden:** "DQN beats TCP." Must say: "DQN utility ranks 2nd, below BBR."

### Slide 9: Main Results — S2
- **Objective:** Show S2 performance.
- **Key Message:** In a high-delay environment, DQN pursues throughput but suffers high loss (5.54%), ranking 3rd in utility.
- **Visual:** `dqn_vs_baseline_loss_s1_s2.png`
- **Forbidden:** Hiding the high loss rate or the 3rd place ranking.

### Slide 10: Findings and Limitations
- **Objective:** Honest appraisal of the MVP.
- **Key Message:** Delay is a proxy, Action is a sender-side abstraction (Fallback Option B), S2 loss is high.
- **Forbidden:** "True RTT", "kernel-level congestion control."

### Slide 11: Demo / Reproducibility
- **Objective:** Prove the work is real.
- **Key Message:** OpenSpec governed, 100% reproducible artifacts, seed sensitivity tested.

### Slide 12: Conclusion & Future Work
- **Objective:** Wrap up.
- **Key Message:** Feasibility proven. Future work includes PPO and continuous action spaces.
