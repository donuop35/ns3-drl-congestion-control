# Final Figure Source Map

| Figure | Path | Source CSV / Artifact | Generation Method | Caveat | Used In |
|--------|------|-----------------------|-------------------|--------|---------|
| baseline_utility_summary.png | `figures/final/baseline_utility_summary.png` | `experiments/summaries/baseline_summary.csv` | Matplotlib grouped bar | Provisional weights; BBR S2 anomaly preserved | Report / Slides |
| dqn_vs_baseline_utility_s1_s2.png | `figures/final/dqn_vs_baseline_utility_s1_s2.png` | `experiments/drl/summaries/dqn_vs_baseline_summary.csv` | Matplotlib subplot bar | Provisional weights | Report / Slides / Demo |
| dqn_vs_baseline_loss_s1_s2.png | `figures/final/dqn_vs_baseline_loss_s1_s2.png` | `experiments/drl/summaries/dqn_vs_baseline_summary.csv` | Matplotlib subplot bar | DQN S2 loss ≈5.54% | Report / Slides / Demo |
| dqn_action_distribution_s1_s2.png | `figures/final/dqn_action_distribution_s1_s2.png` | `experiments/drl/summaries/dqn_action_distribution_summary.csv` | Matplotlib grouped bar | S1 degenerate policy | Report / Slides |
| dqn_reward_curves_s1_s2.png | `figures/final/dqn_reward_curves_s1_s2.png` | `figures/drl/dqn_reward_curve_s*.png` | PIL merge | Training diagnostic only; not final performance | Slides |
| system_pipeline.png | `figures/final/system_pipeline.png` | `Conceptual` | Matplotlib flow diagram |  | Report / Slides |
| single_bottleneck_topology.png | `figures/final/single_bottleneck_topology.png` | `Conceptual` | Matplotlib node-link diagram |  | Report / Slides |
| mdp_formulation.png | `figures/final/mdp_formulation.png` | `Conceptual` | Matplotlib flow diagram |  | Report / Slides |
| key_findings_summary.png | `figures/final/key_findings_summary.png` | `Conceptual` | Matplotlib 4-card layout |  | Report / Slides |
