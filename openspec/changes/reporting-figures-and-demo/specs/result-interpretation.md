# Specification: Result Interpretation Rules

**Target Location:** Internal reference for all Phase 5 reporting (applied across README, PPT, Report, and Demo).

## ADDED Requirements

### Req 1: Define Result Interpretation
All results must be presented honestly, without exaggeration.

#### Scenario: Interpreting the results
Given the final metrics
When the results are described in deliverables
Then the interpretation must follow the S1 and S2 rules.

## 1. Core Principle
Results must be interpreted accurately without overclaiming adaptiveness or performance.

## 2. S1 Interpretation (Low Delay, 10ms)
- **Observations:** DQN achieves near-maximum throughput (9.88 Mbps). Its utility (0.900) ranks 2nd overall.
- **Comparisons:** DQN beats CUBIC (0.884) and NewReno (0.875) on utility. DQN does **not** beat BBR (0.947).
- **Behavior:** The agent learned a degenerate policy (100% "increase" actions).
- **Required Wording:** This must be interpreted as the agent finding a locally optimal policy for a highly benign, near-capacity environment, rather than demonstrating complex adaptive behavior. Do not overclaim adaptiveness.

## 3. S2 Interpretation (High Delay, 50ms)
- **Observations:** DQN maintains high throughput (9.79 Mbps) but suffers a significantly higher loss rate (5.54%). Its utility (0.757) ranks 3rd overall.
- **Comparisons:** DQN loses to NewReno (0.923) and CUBIC (0.818) on utility.
- **Behavior:** The high loss rate indicates the DQN MVP over-prioritizes throughput at the expense of queue management in high-RTT conditions.
- **Required Wording:** This result is a valuable limitation finding. It proves the environment is challenging and highlights the limitations of the current simple reward function and discrete action space.

## 4. Global Interpretation Rules
- **Feasibility:** The DQN MVP proves feasibility; it is not production-ready.
- **Utility:** The Utility Score is explicitly **provisional**.
- **Delay:** The delay metric is a **proxy** (FlowMonitor delaySum/rxPackets), not true RTT.
- **Action Abstraction:** DQN uses Fallback Option B (sender-side rate-control abstraction), it does not directly hack Linux kernel `cwnd`.
- **Contribution:** The project's main contribution is the reproducible ns-3/ns3-gym pipeline and the honest baseline comparison framework, paving the way for future advanced algorithms (e.g., PPO).
