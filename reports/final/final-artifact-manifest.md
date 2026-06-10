# Final Artifact Manifest

## 1. OpenSpec Artifacts
| Artifact | Path | Phase Source | Purpose | Used in Report | Used in Slides | Used in Demo | Caveat |
|----------|------|--------------|---------|----------------|----------------|--------------|--------|
| Change 05 Proposal | `openspec/changes/reporting-figures-and-demo/proposal.md` | Phase 5 | Define reporting goals | No | No | Yes | N/A |
| Change 05 Specs | `openspec/changes/reporting-figures-and-demo/specs/` | Phase 5 | Define strict constraints | Yes | Yes | Yes | OpenSpec rules |

## 2. Source Code Artifacts
| Artifact | Path | Phase Source | Purpose | Used in Report | Used in Slides | Used in Demo | Caveat |
|----------|------|--------------|---------|----------------|----------------|--------------|--------|
| Baseline Runner | `scripts/run_baseline.py` | Phase 3 | Execute TCP algorithms | No | No | No | N/A |
| DQN Agent | `src/drl_agent/dqn_agent.py` | Phase 4 | Train & evaluate DQN | No | No | No | Options B abstraction |

## 3. Baseline Data Artifacts
| Artifact | Path | Phase Source | Purpose | Used in Report | Used in Slides | Used in Demo | Caveat |
|----------|------|--------------|---------|----------------|----------------|--------------|--------|
| Baseline Summary | `experiments/summaries/baseline_summary.csv` | Phase 3 | Source of truth for TCP | Yes | Yes | Yes | Delay is a proxy |

## 4. DRL Data Artifacts
| Artifact | Path | Phase Source | Purpose | Used in Report | Used in Slides | Used in Demo | Caveat |
|----------|------|--------------|---------|----------------|----------------|--------------|--------|
| DQN Summary | `experiments/drl/summaries/dqn_summary.csv` | Phase 4 | Source of truth for DQN | Yes | Yes | Yes | Evaluated on Seed 42 |
| Comparison Summary | `experiments/drl/summaries/dqn_vs_baseline_summary.csv` | Phase 4 | Merged data for plotting | Yes | Yes | Yes | Utility is provisional |

## 5. Model Artifacts
| Artifact | Path | Phase Source | Purpose | Used in Report | Used in Slides | Used in Demo | Caveat |
|----------|------|--------------|---------|----------------|----------------|--------------|--------|
| DQN Model (S1) | `experiments/drl/models/dqn_s1_final.zip` | Phase 4 | S1 Agent Checkpoint | No | No | No | N/A |
| DQN Model (S2) | `experiments/drl/models/dqn_s2_final.zip` | Phase 4 | S2 Agent Checkpoint | No | No | No | N/A |

## 6. Figure Artifacts
| Artifact | Path | Phase Source | Purpose | Used in Report | Used in Slides | Used in Demo | Caveat |
|----------|------|--------------|---------|----------------|----------------|--------------|--------|
| Utility S1/S2 | `figures/final/dqn_vs_baseline_utility_s1_s2.png` | Phase 5 | Compare overall utility | Yes | Yes | Yes | Generated from CSV |
| Loss S1/S2 | `figures/final/dqn_vs_baseline_loss_s1_s2.png` | Phase 5 | Highlight S2 limitation | Yes | Yes | Yes | Exposes 5.54% loss |
| Action Dist | `figures/final/dqn_action_distribution_s1_s2.png` | Phase 5 | S1 degenerate policy | Yes | Yes | No | Generated from CSV |

## 7. Report Artifacts
| Artifact | Path | Phase Source | Purpose | Used in Report | Used in Slides | Used in Demo | Caveat |
|----------|------|--------------|---------|----------------|----------------|--------------|--------|
| Final Report | `reports/final/final-report.md` | Phase 5 | Complete academic summary | Yes | No | Yes | Honest limitations |
| Phase 5 Completion | `reports/final/phase5-completion-report.md` | Phase 5 | Record step completion | No | No | No | Handover only |

## 8. Demo Artifacts
| Artifact | Path | Phase Source | Purpose | Used in Report | Used in Slides | Used in Demo | Caveat |
|----------|------|--------------|---------|----------------|----------------|--------------|--------|
| Demo Script | `demo/demo-script.md` | Phase 5 | 10-minute speech outline | No | No | Yes | Time-boxed |
| Checklist | `demo/demo-checklist.md` | Phase 5 | Pre-flight sanity checks | No | No | Yes | No live training |

## 9. PPT / Slide Artifacts
| Artifact | Path | Phase Source | Purpose | Used in Report | Used in Slides | Used in Demo | Caveat |
|----------|------|--------------|---------|----------------|----------------|--------------|--------|
| Outline | `slides/final/final-presentation-outline.md` | Phase 5 | Deck structure | No | Yes | Yes | 12 slides max |
| Speaker Notes | `slides/final/speaker-notes.md` | Phase 5 | Practice script | No | Yes | Yes | N/A |
