# Proposal: Change 05 reporting-figures-and-demo

## Why

Phase 4 has achieved Excellent Acceptance for the DQN MVP. The research, code implementation, baseline benchmark, and DQN results are all complete. However, the repository currently reflects an engineering/experimental state. We must now synthesize these Phase 0–4 outcomes into a cohesive, submittable final project package. Final deliverables require consistent narrative, figures, README, demo script, and PPTs. Without Change 05, the repository lacks the overarching story and exhibition package required for academic final evaluation.

## What Changes

Change 05 specifies the creation and governance of the Phase 5 package, which includes:
- Final report structure and contents
- Figure package selection, regeneration, and formatting
- Demo script and execution checklist
- PPT package (10-12 slides)
- README finalization rules (transforming from engineering repo to landing page)
- Final Artifact Manifest
- Result interpretation and presentation governance
- Final acceptance criteria

## What Does Not Change

- **No topic change:** The core MDP formulation and objectives remain identical.
- **No baseline changes:** Phase 3 baseline benchmark results are frozen.
- **No DQN model/training changes:** Phase 4 S1/S2 DQN results are frozen. No retraining.
- **No new experiments:** No additional data gathering.
- **No new protocols:** IPFS, QUIC, multi-agent, and multi-path routing remain out of scope.
- **No scope expansion:** PPO or continuous actions are not added.
- **No overclaiming:** We do NOT claim universal superiority of DRL over TCP.

## Impact

Change 05 will act as the single source of truth for all final reporting, demo, and presentation tasks. Future packaging implementations must strictly adhere to these specifications. The README, PPT, final report, and video script must be internally consistent and trace back to the artifacts established in this change.

## Dependencies

- Change 01 `project-charter` (Approved)
- Change 02 `ns3-baseline-benchmark` (Spec Approved, Phase 3 executed)
- Change 03 `opengym-env` (Spec Approved, Phase 4 implemented)
- Change 04 `dqn-mvp-agent` (Spec Approved, Phase 4 complete)
- Phase 3 baseline artifacts (Summaries, metadata, logs)
- Phase 4 DRL artifacts (DQN S1/S2 models, evaluations, summaries, comparison CSVs)

## Acceptance Criteria

- [ ] `final-report-package.md` spec complete
- [ ] `figure-package.md` spec complete
- [ ] `demo-script.md` spec complete
- [ ] `ppt-package.md` spec complete
- [ ] `readme-finalization.md` spec complete
- [ ] `artifact-manifest.md` spec complete
- [ ] `result-interpretation.md` rules complete
- [ ] `risk-register.md` complete
- [ ] No fake results specified or permitted
- [ ] No scope expansion specified
- [ ] OpenSpec strict validation passes (`openspec validate reporting-figures-and-demo --strict`)
