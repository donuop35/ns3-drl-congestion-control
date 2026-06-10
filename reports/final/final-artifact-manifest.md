# Final Artifact Manifest

## 1. OpenSpec Artifacts
| Artifact | Path | Exists | Phase Source | Purpose | Used in Report | Used in Slides | Used in Demo | Caveat |
|----------|------|--------|--------------|---------|----------------|----------------|--------------|--------|
| Change 05 Proposal | `openspec/changes/reporting-figures-and-demo/proposal.md` | Yes | Phase 5 | Define reporting goals | No | No | Yes | N/A |
| Change 05 Specs | `openspec/changes/reporting-figures-and-demo/specs/` | Yes | Phase 5 | Define strict constraints | Yes | Yes | Yes | OpenSpec rules |

## 2. Source Code Artifacts
| Artifact | Path | Exists | Phase Source | Purpose | Used in Report | Used in Slides | Used in Demo | Caveat |
|----------|------|--------|--------------|---------|----------------|----------------|--------------|--------|
| Baseline Runner | `scripts/phase3/baseline_runner.sh` | Yes | Phase 3 | Execute TCP algorithms | No | No | No | Optional / expensive |
| Smoke Test | `src/gym_env/smoke_test.py` | Yes | Phase 4 | ZMQ connection sanity check | No | No | No | Requires ns3-gym |
| Train DQN | `src/agents/train_dqn.py` | Yes | Phase 4 | Train DQN model | No | No | No | Option B abstraction |
| Evaluate DQN | `src/agents/eval_dqn.py` | Yes | Phase 4 | Evaluate trained DQN model | No | No | No | Seed 42 |

## 3. Baseline Data Artifacts
| Artifact | Path | Exists | Phase Source | Purpose | Used in Report | Used in Slides | Used in Demo | Caveat |
|----------|------|--------|--------------|---------|----------------|----------------|--------------|--------|
| Baseline Summary | `experiments/summaries/baseline_summary.csv` | Yes | Phase 3 | Source of truth for TCP | Yes | Yes | Yes | Delay is a proxy |

## 4. DRL Data Artifacts
| Artifact | Path | Exists | Phase Source | Purpose | Used in Report | Used in Slides | Used in Demo | Caveat |
|----------|------|--------|--------------|---------|----------------|----------------|--------------|--------|
| DQN Summary | `experiments/drl/summaries/dqn_summary.csv` | Yes | Phase 4 | Source of truth for DQN | Yes | Yes | Yes | Evaluated on Seed 42 |
| Comparison Summary | `experiments/drl/summaries/dqn_vs_baseline_summary.csv` | Yes | Phase 4 | Merged data for plotting | Yes | Yes | Yes | Utility is provisional |

## 5. Model Artifacts
| Artifact | Path | Exists | Phase Source | Purpose | Used in Report | Used in Slides | Used in Demo | Caveat |
|----------|------|--------|--------------|---------|----------------|----------------|--------------|--------|
| DQN Model (S1) | `experiments/drl/models/dqn_s1_seed42.zip` | Yes | Phase 4 | S1 Agent Checkpoint | No | No | No | S1 only |
| DQN Model (S2) | `experiments/drl/models/dqn_s2_seed42.zip` | Yes | Phase 4 | S2 Agent Checkpoint | No | No | No | S2 only |

## 6. Figure Artifacts
| Artifact | Path | Exists | Phase Source | Purpose | Used in Report | Used in Slides | Used in Demo | Caveat |
|----------|------|--------|--------------|---------|----------------|----------------|--------------|--------|
| Generate Script | `scripts/phase5/generate_final_figures.py` | Yes | Phase 5 | High-score figure generator | No | No | No | Fail-fast on missing CSV |
| Validate Script | `scripts/phase5/validate_final_figures.py` | Yes | Phase 5 | Figure QA checker | No | No | No | Checks size + dimensions |
| Figure Source Map | `reports/final/final-figure-source-map.md` | Yes | Phase 5 | Figure to CSV mapping | Yes | No | No | N/A |
| Baseline Utility | `figures/final/baseline_utility_summary.png` | Yes | Phase 5 | S1/S2 baseline grouped bar | Yes | Yes | No | BBR S2 anomaly annotated |
| Utility S1/S2 | `figures/final/dqn_vs_baseline_utility_s1_s2.png` | Yes | Phase 5 | Compare overall utility | Yes | Yes | Yes | Generated from CSV |
| Loss S1/S2 | `figures/final/dqn_vs_baseline_loss_s1_s2.png` | Yes | Phase 5 | Highlight S2 limitation | Yes | Yes | Yes | DQN S2 loss 5.54% |
| Action Dist | `figures/final/dqn_action_distribution_s1_s2.png` | Yes | Phase 5 | S1 degenerate policy | Yes | Yes | No | Percentage scale 0-100 |
| System Pipeline | `figures/final/system_pipeline.png` | Yes | Phase 5 | Architecture flow diagram | Yes | Yes | No | Conceptual |
| Bottleneck Topology | `figures/final/single_bottleneck_topology.png` | Yes | Phase 5 | Network topology | Yes | Yes | No | Conceptual |
| MDP Formulation | `figures/final/mdp_formulation.png` | Yes | Phase 5 | MDP loop diagram | Yes | Yes | No | Conceptual |
| Key Findings | `figures/final/key_findings_summary.png` | Yes | Phase 5 | 4-card insight summary | Yes | Yes | No | Conceptual |
| Reward Curves | `figures/final/dqn_reward_curves_s1_s2.png` | Yes | Phase 5 | Training diagnostic | No | Yes | No | Not final performance |

## 7. Report Artifacts
| Artifact | Path | Exists | Phase Source | Purpose | Used in Report | Used in Slides | Used in Demo | Caveat |
|----------|------|--------|--------------|---------|----------------|----------------|--------------|--------|
| Final Report | `reports/final/final-report.md` | Yes | Phase 5 | Complete academic summary | Yes | No | Yes | Honest limitations |
| High-Score Report | `reports/final/phase5-high-score-acceptance-report.md` | Yes | Phase 5 | Acceptance validation proof | No | No | No | N/A |
| Figures QA Report | `reports/final/final-figures-qa-report.md` | Yes | Phase 5 | Figure QA audit trail | No | No | No | N/A |

## 8. Demo Artifacts
| Artifact | Path | Exists | Phase Source | Purpose | Used in Report | Used in Slides | Used in Demo | Caveat |
|----------|------|--------|--------------|---------|----------------|----------------|--------------|--------|
| Demo Script | `demo/demo-script.md` | Yes | Phase 5 | 10-minute speech outline | No | No | Yes | Time-boxed |
| Checklist | `demo/demo-checklist.md` | Yes | Phase 5 | Pre-flight sanity checks | No | No | Yes | No live training |

## 9. PPT / Slide Artifacts
| Artifact | Path | Exists | Phase Source | Purpose | Used in Report | Used in Slides | Used in Demo | Caveat |
|----------|------|--------|--------------|---------|----------------|----------------|--------------|--------|
| Outline | `slides/final/final-presentation-outline.md` | Yes | Phase 5 | Deck structure | No | Yes | Yes | 12 slides max |
| Speaker Notes | `slides/final/speaker-notes.md` | Yes | Phase 5 | Practice script | No | Yes | Yes | N/A |
