# Tasks: Change 05 reporting-figures-and-demo

> ⚠️ All tasks in this document are **specification tasks**, not implementation tasks. This change defines the requirements for Phase 5 (Final Reporting / Demo / PPT Package). No DRL training, no baseline execution, and no results manipulation are permitted.

---

## 0. Official OpenSpec Verification

- [ ] 0.1 Confirm official OpenSpec version (`openspec --version` is 1.4.1+)
- [ ] 0.2 Confirm Change 05 created by official OpenSpec workflow
- [ ] 0.3 Confirm not using `openspec-preview/`
- [ ] 0.4 Confirm strict validation target (`openspec validate reporting-figures-and-demo --strict`)

## 1. Upstream Artifact Audit

- [ ] 1.1 Audit Change 01 `project-charter`
- [ ] 1.2 Audit Change 02 `ns3-baseline-benchmark`
- [ ] 1.3 Audit Change 03 `opengym-env`
- [ ] 1.4 Audit Change 04 `dqn-mvp-agent`
- [ ] 1.5 Audit Phase 3 artifacts (`baseline_summary.csv`, figures, etc.)
- [ ] 1.6 Audit Phase 4 artifacts (`dqn_summary.csv`, reports, figures, models)
- [ ] 1.7 Identify stale README sections for finalization

## 2. Final Report Package Spec

- [ ] 2.1 Define final report structure (`specs/final-report-package.md`)
- [ ] 2.2 Define source artifacts per section
- [ ] 2.3 Define result interpretation rules (`specs/result-interpretation.md`)
- [ ] 2.4 Define limitations wording

## 3. Figure Package Spec

- [ ] 3.1 Define required final figures (`specs/figure-package.md`)
- [ ] 3.2 Define figure source mapping
- [ ] 3.3 Define PPT-ready visual rules
- [ ] 3.4 Define no-manual-number-editing rule

## 4. Demo Script Spec

- [ ] 4.1 Define demo flow (`specs/demo-script.md`)
- [ ] 4.2 Define demo commands
- [ ] 4.3 Define demo no-go statements
- [ ] 4.4 Define 10-minute timing

## 5. PPT Package Spec

- [ ] 5.1 Define 10–12 slide structure (`specs/ppt-package.md`)
- [ ] 5.2 Define key message per slide
- [ ] 5.3 Define figure per slide
- [ ] 5.4 Define speaker note direction
- [ ] 5.5 Define forbidden wording

## 6. README Finalization Spec

- [ ] 6.1 Define README final sections (`specs/readme-finalization.md`)
- [ ] 6.2 Define stale text cleanup
- [ ] 6.3 Define final artifact links
- [ ] 6.4 Define reproduction instructions

## 7. Artifact Manifest Spec

- [ ] 7.1 Define artifact groups (`specs/artifact-manifest.md`)
- [ ] 7.2 Define artifact table schema
- [ ] 7.3 Define source / usage / caveat mapping

## 8. Risk Register

- [ ] 8.1 Define reporting risks (`specs/risk-register.md`)
- [ ] 8.2 Define figure risks
- [ ] 8.3 Define demo risks
- [ ] 8.4 Define overclaiming risks
- [ ] 8.5 Define fallback rules

## 9. Review / Validation

- [ ] 9.1 Confirm no implementation included
- [ ] 9.2 Confirm no new experiment included
- [ ] 9.3 Confirm no fake result allowed
- [ ] 9.4 Confirm no PPO / IPFS / QUIC / multi-agent / multi-path
- [ ] 9.5 Run `openspec validate reporting-figures-and-demo --strict`
- [ ] 9.6 Stop and wait for Spec Owner review

---

## Change 05 Review Checklist (For Spec Owner)

- [ ] Are we using official OpenSpec?
- [ ] Have Phase 3 / Phase 4 artifacts been audited?
- [ ] Is this purely a reporting/demo/PPT specification change?
- [ ] Is retraining strictly prohibited?
- [ ] Is data manipulation strictly prohibited?
- [ ] Is the final report spec complete?
- [ ] Is the figure package spec complete?
- [ ] Is the demo script spec complete?
- [ ] Is the PPT package spec complete?
- [ ] Is the README finalization spec complete?
- [ ] Is the artifact manifest spec complete?
- [ ] Are result interpretation rules defined?
- [ ] Is there an explicit requirement to report honest DQN S1/S2 results?
- [ ] Is the delay proxy clearly marked?
- [ ] Is Fallback Option B clearly documented?
- [ ] Is overclaiming explicitly forbidden?
- [ ] Does this specification adequately support Phase 5 implementation?
