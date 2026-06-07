## 1. OpenSpec Environment Verification

- [x] 1.1 Verify OpenSpec CLI is installed (npm list -g @fission-ai/openspec)
- [x] 1.2 Upgrade OpenSpec to latest version (v1.4.1) and run openspec update --force
- [x] 1.3 Confirm .agent/skills/ contains openspec-* SKILL.md files
- [x] 1.4 Confirm .agent/workflows/ contains opsx-*.md workflow files
- [x] 1.5 Run openspec new change "project-charter" to create official change directory

## 2. Project Charter Artifacts

- [x] 2.1 Run openspec instructions proposal --change "project-charter" and create proposal.md
- [x] 2.2 Run openspec instructions design --change "project-charter" and create design.md (with Decisions, Risk Register, Open Questions)
- [x] 2.3 Run openspec instructions specs --change "project-charter" and create specs/project-charter/spec.md (with all requirements and scenarios)
- [x] 2.4 Run openspec instructions tasks --change "project-charter" and create this tasks.md
- [x] 2.5 Verify openspec status --change "project-charter" shows all artifacts as done

## 3. Project Directory Structure

- [x] 3.1 Create docs/ directory with placeholder files: background_congestion_control.md, methodology_mdp.md, related_work.md, risk_register.md
- [x] 3.2 Create src/ directory structure: src/ns3/, src/gym_env/, src/agents/, src/analysis/
- [x] 3.3 Create experiments/ directory structure: experiments/configs/, experiments/logs/, experiments/results/
- [x] 3.4 Create figures/ and slides/ and scripts/ directories
- [ ] 3.5 Create proposal/ directory with: phase0_decision.md, abstract_af.md, research_questions.md (already exists from previous work)

## 4. README Initial Version

- [x] 4.1 Update README.md with: project title (frozen), research motivation, scope and non-goals
- [x] 4.2 Add Official OpenSpec setup proof section to README (version, commands used)
- [x] 4.3 Add toolchain section to README (ns-3, ns3-gym, SB3, DQN)
- [x] 4.4 Add placeholder sections for: installation, how to run baseline, results summary, known limitations, future work
- [x] 4.5 Add Change sequence roadmap to README (Changes 01–05 with status)

## 5. Charter Validation

- [x] 5.1 Confirm project title is frozen and matches exactly in proposal.md, design.md, and README.md
- [x] 5.2 Confirm Non-goals list is complete and matches spec requirement "Non-goals are enforced throughout the project"
- [x] 5.3 Confirm MDP definition (observation, action, reward) is documented in design.md and spec.md
- [x] 5.4 Confirm Risk Register in design.md covers all 8 major risks
- [x] 5.5 Confirm Acceptance Criteria can be verified against spec.md scenarios
- [ ] 5.6 Present completed charter to Spec Owner for confirmation before starting Change 02
