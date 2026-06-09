# Specification: Figure Package

**Target Location:** `figures/final/`

## ADDED Requirements

### Req 1: Generate Final Figures
The final package must compile and format the required figures.

#### Scenario: Compiling figures
Given the Phase 3 and Phase 4 CSV artifacts
When the analysis scripts are run
Then the 9 required figures must be generated in `figures/final/`.

## 1. Required Final Figures

1. `system_pipeline.png` (Architecture/Pipeline)
2. `single_bottleneck_topology.png` (Topology)
3. `mdp_formulation.png` (Visual representation of state/action/reward)
4. `baseline_utility_summary.png` (Phase 3 baseline performance)
5. `dqn_reward_curves_s1_s2.png` (Combined or side-by-side training convergence)
6. `dqn_action_distribution_s1_s2.png` (S1 100% increase vs S2 distribution)
7. `dqn_vs_baseline_utility_s1_s2.png` (Utility score comparison)
8. `dqn_vs_baseline_loss_s1_s2.png` (Loss rate comparison, highlighting S2 DQN loss)
9. `key_findings_summary.png` (Visual summary of limitations and honest results)

## 2. Figure Generation Rules

All final figures must adhere to the following rules:
- **Clarity:** Clear titles, axis labels, and legends.
- **Context:** Must explicitly state the Scenario (e.g., S1: Low Delay, 10ms).
- **Units:** Must explicitly state units (Mbps, ms, %).
- **Transparency:** The Delay axis must be labeled as "Delay Proxy" (not true RTT). Utility must be labeled "Provisional Utility".
- **Naming:** Follow the standardized `snake_case` naming convention listed above.
- **Integrity:** Figures must be generated programmatically from existing CSV artifacts (`dqn_vs_baseline_summary.csv`, etc.). Manual editing of data points is strictly prohibited.
- **Format:** High resolution (≥ 150 DPI), PPT-ready layout.

## 3. Figure Source Mapping

| Figure Name | Source Artifact | Purpose | Used In | Caveat |
|-------------|-----------------|---------|---------|--------|
| `system_pipeline.png` | Manual creation / Drawing | Illustrate ns3-gym interaction | README, PPT, Report | Conceptual only |
| `single_bottleneck_topology.png` | Manual creation / Drawing | Illustrate sender-bottleneck-receiver | PPT, Report | Conceptual only |
| `mdp_formulation.png` | Manual creation / Drawing | Visual aid for RL loop | PPT | Conceptual only |
| `baseline_utility_summary.png` | `baseline_summary.csv` | Show baseline bounds | Report | Utility is provisional |
| `dqn_reward_curves_s1_s2.png` | `dqn_train_s*_seed42.monitor.csv` | Prove training convergence | Report | Y-axis is episode reward, not throughput |
| `dqn_action_distribution_s1_s2.png` | `dqn_action_distribution_summary.csv` | Illustrate policy differences | PPT, Report | S1 is degenerate |
| `dqn_vs_baseline_utility_s1_s2.png` | `dqn_vs_baseline_summary.csv` | Core performance metric | README, PPT, Report | DQN ranks 2nd in S1, 3rd in S2 |
| `dqn_vs_baseline_loss_s1_s2.png` | `dqn_vs_baseline_summary.csv` | Highlight S2 limitation | PPT, Report | DQN S2 loss is 5.54% |
| `key_findings_summary.png` | Synthesis | Executive summary | PPT, Video | Must include honest limitations |
