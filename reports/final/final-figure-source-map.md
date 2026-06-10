# Final Figure Source Map

| Figure | Path | Source CSV / Artifact | Generation Method | Caveat | Used In |
|--------|------|-----------------------|-------------------|--------|---------|
| system_pipeline.png | `figures/final/system_pipeline.png` | `Conceptual` | Matplotlib text | Conceptual diagram | Slides/Report |
| single_bottleneck_topology.png | `figures/final/single_bottleneck_topology.png` | `Conceptual` | Matplotlib text | Conceptual diagram | Slides/Report |
| mdp_formulation.png | `figures/final/mdp_formulation.png` | `Conceptual` | Matplotlib text | Conceptual diagram | Slides/Report |
| key_findings_summary.png | `figures/final/key_findings_summary.png` | `Conceptual` | Matplotlib text | Conceptual diagram | Slides/Report |
| baseline_utility_summary.png | `figures/final/baseline_utility_summary.png` | `experiments/summaries/baseline_summary.csv` | Matplotlib bar chart | Provisional weights applied | Report/Slides |
| dqn_vs_baseline_utility_s1_s2.png | `figures/final/dqn_vs_baseline_utility_s1_s2.png` | `experiments/drl/summaries/dqn_vs_baseline_summary.csv` | Matplotlib grouped bar | Provisional weights applied | Report/Slides/Demo |
| dqn_vs_baseline_loss_s1_s2.png | `figures/final/dqn_vs_baseline_loss_s1_s2.png` | `experiments/drl/summaries/dqn_vs_baseline_summary.csv` | Matplotlib grouped bar | Exposes DQN S2 high loss anomaly | Report/Slides/Demo |
| dqn_action_distribution_s1_s2.png | `figures/final/dqn_action_distribution_s1_s2.png` | `experiments/drl/summaries/dqn_action_distribution_summary.csv` | Matplotlib bar chart | Shows S1 degenerate policy | Report/Slides |
| dqn_reward_curves_s1_s2.png | `figures/final/dqn_reward_curves_s1_s2.png` | `figures/drl/dqn_reward_curve_s*.png` | PIL merge | Training reward != performance | Slides |
