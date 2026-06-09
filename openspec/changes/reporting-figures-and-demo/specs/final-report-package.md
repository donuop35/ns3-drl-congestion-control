# Specification: Final Report Package

**Target Location:** `reports/final/final-report.md`

## ADDED Requirements

### Req 1: Define Final Report Structure
The final report must synthesize all project phases into a cohesive narrative.

#### Scenario: Authoring the report
Given the completed Phase 4 artifacts
When the author creates `reports/final/final-report.md`
Then it must contain the specified 14 sections.

## 2. Required Structure

### 1. Abstract
- **Purpose:** Provide a 200-word summary of the problem, method, and key findings.
- **Source Artifacts:** N/A (Synthesis)
- **Must NOT include:** Claims of DRL universality.

### 2. Introduction / Motivation
- **Purpose:** Explain the limitations of rule-based TCP and the motivation for DRL.
- **Source Artifacts:** `proposal.md` (Change 01)
- **Required Content:** Mention throughput, delay, and loss trade-offs.

### 3. Problem Statement
- **Purpose:** Define the single bottleneck link congestion control problem.
- **Source Artifacts:** `project-charter` specs
- **Required Content:** Clearly define the network topology.

### 4. Related Work / Background
- **Purpose:** Contextualize traditional TCP and RL.
- **Source Artifacts:** N/A (Literature review)
- **Required Content:** Brief mention of NewReno, CUBIC, BBR, and DQN basics.

### 5. System Design
- **Purpose:** Explain the ns-3 and ns3-gym integration.
- **Source Artifacts:** `README.md` Toolchain, `toolchain_metadata.yaml`
- **Required Content:** Architecture diagram. Mention of Fallback Option B (sender-side rate control abstraction).

### 6. MDP Formulation
- **Purpose:** Define state, action, and reward.
- **Source Artifacts:** `specs/opengym-env.md` (Change 03)
- **Required Content:** Observation space (shape 5), Action space (Discrete 3), Provisional Reward formula.

### 7. Baseline Benchmark
- **Purpose:** Present Phase 3 results.
- **Source Artifacts:** `baseline_summary.csv`, `phase3-baseline-report.md`
- **Required Content:** S1 and S2 baseline metrics. BBR S2 anomaly documentation.

### 8. DRL MVP Implementation
- **Purpose:** Explain DQN setup and training.
- **Source Artifacts:** `dqn_training_metadata_s1.yaml`, `dqn_training_metadata_s2.yaml`
- **Required Content:** SB3 usage, training duration (30k steps).

### 9. Results
- **Purpose:** Present DQN vs Baseline comparisons. MUST be split into S1 and S2 subsections.
- **Source Artifacts:** `dqn_summary.csv`, `dqn_vs_baseline_summary.csv`, Comparison Figures.
- **Required Content:** Throughput, delay proxy, loss, utility. Honest rankings (DQN 2nd in S1, 3rd in S2).

### 10. Discussion
- **Purpose:** Analyze the results and agent behavior.
- **Source Artifacts:** `dqn_action_distribution_summary.csv`
- **Required Content:** S1 degenerate policy (100% increase), S2 high loss trade-off.

### 11. Limitations
- **Purpose:** Transparently report system constraints.
- **Source Artifacts:** `phase4-excellent-acceptance-report.md`
- **Required Content:** Fallback Option B, Delay proxy vs true RTT, provisional utility weights, S1 near-capacity limitation, S2 high loss limitation.

### 12. Conclusion
- **Purpose:** Summarize the successful prototype and its boundaries.
- **Source Artifacts:** Synthesis
- **Must NOT include:** Claims that DRL completely outperforms TCP.

### 13. Reproducibility
- **Purpose:** Prove OpenSpec and artifact traceability.
- **Source Artifacts:** `artifact-index.md`
- **Required Content:** Mention seed sensitivity (std=0.000) and metadata YAMLs.

### 14. Appendix / Artifact Index
- **Purpose:** Link to raw logs, models, and code.
- **Source Artifacts:** `reports/final/final-artifact-manifest.md`

## 3. Governance
- No results may be manually invented.
- All numbers must trace back to Phase 3 or Phase 4 CSVs.
