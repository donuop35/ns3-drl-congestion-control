# Gemini Intake Checklist

**Purpose:** This checklist is for the incoming Antigravity (Gemini Pro) agent to complete before taking any implementation action.

**Before you begin:** Read `reports/handoff/claude-to-gemini-handoff.md` in its entirety. Then read every file in the "Files Gemini Must Read" section below. Only then complete this checklist and produce the Intake Understanding Report.

---

## 1. Files Gemini Must Read

Complete these reads in order. Mark each done as you go.

### 1.1 Handoff and Meta

- [ ] `reports/handoff/claude-to-gemini-handoff.md` (this handoff document)
- [ ] `README.md`

### 1.2 OpenSpec Changes

- [ ] `openspec/changes/project-charter/proposal.md`
- [ ] `openspec/changes/ns3-baseline-benchmark/proposal.md`
- [ ] `openspec/changes/opengym-env/proposal.md`
- [ ] `openspec/changes/dqn-mvp-agent/proposal.md`
- [ ] `openspec/changes/dqn-mvp-agent/tasks.md` (especially Section 14)
- [ ] `openspec/changes/reporting-figures-and-demo/proposal.md`
- [ ] `openspec/changes/reporting-figures-and-demo/design.md`
- [ ] `openspec/changes/reporting-figures-and-demo/tasks.md`
- [ ] `openspec/changes/reporting-figures-and-demo/specs/final-report-package.md`
- [ ] `openspec/changes/reporting-figures-and-demo/specs/figure-package.md`
- [ ] `openspec/changes/reporting-figures-and-demo/specs/demo-script.md`
- [ ] `openspec/changes/reporting-figures-and-demo/specs/ppt-package.md`
- [ ] `openspec/changes/reporting-figures-and-demo/specs/readme-finalization.md`
- [ ] `openspec/changes/reporting-figures-and-demo/specs/artifact-manifest.md`
- [ ] `openspec/changes/reporting-figures-and-demo/specs/result-interpretation.md`
- [ ] `openspec/changes/reporting-figures-and-demo/specs/risk-register.md`

### 1.3 Phase 3 Artifacts

- [ ] `reports/phase3-baseline/phase3-baseline-report.md`
- [ ] `experiments/summaries/baseline_summary.csv`
- [ ] `experiments/metadata/toolchain_metadata.yaml`
- [ ] `experiments/metadata/phase3_run_metadata.yaml`

### 1.4 Phase 4 Artifacts

- [ ] `reports/phase4-drl-mvp/phase4-excellent-acceptance-report.md`
- [ ] `reports/phase4-drl-mvp/phase4-drl-report.md`
- [ ] `reports/phase4-drl-mvp/artifact-index.md`
- [ ] `reports/phase4-drl-mvp/smoke-test-report.md`
- [ ] `experiments/drl/summaries/dqn_summary.csv`
- [ ] `experiments/drl/summaries/dqn_vs_baseline_summary.csv`
- [ ] `experiments/drl/summaries/dqn_action_distribution_summary.csv`
- [ ] `experiments/drl/summaries/dqn_seed_sensitivity_summary.csv`

### 1.5 Git History

- [ ] Run `git log --oneline -20` and review recent history
- [ ] Run `git show 9ae8a2c --stat` to see what Change 05 added
- [ ] Run `git status` to confirm working tree is clean

### 1.6 OpenSpec Status

- [ ] Run `openspec --version`
- [ ] Run `openspec status`
- [ ] Run `openspec status --change "reporting-figures-and-demo"`
- [ ] Run `openspec validate reporting-figures-and-demo --strict`

---

## 2. Questions Gemini Must Answer Before Coding

Answer these questions in your Intake Understanding Report. Do not proceed if you cannot answer all of them accurately.

| #    | Question                                                  | Required Knowledge                                                 |
| ---- | --------------------------------------------------------- | ------------------------------------------------------------------ |
| 2.1  | What phase is the project currently in?                   | Phase 4 Complete / Change 05 Spec Done / Phase 5 Not Started       |
| 2.2  | What has the Spec Owner formally accepted?                | Phase 3 (baseline) and Phase 4 (Excellent Acceptance)              |
| 2.3  | What are the three Change 05 gaps to fix?                 | Validation note, tasks.md sync, markdown formatting                |
| 2.4  | What data must NOT be modified under any circumstances?   | All CSVs in `experiments/`, all figures in `figures/`              |
| 2.5  | What is the next approved action for you as Gemini?       | Read repo → submit intake report → wait for Spec Owner             |
| 2.6  | What claims are forbidden in all deliverables?            | "DQN beats TCP", "true RTT", "kernel cwnd", "production-ready"     |
| 2.7  | What algorithm is the DQN agent?                          | SB3 DQN Discrete(3) — NOT PPO, NOT A2C                             |
| 2.8  | What is Fallback Option B?                                | Sender-side rate-control abstraction — NOT kernel TCP modification |
| 2.9  | What is the delay metric?                                 | FlowMonitor delaySum/rxPackets proxy — NOT direct TCP RTT          |
| 2.10 | What is DQN S1 utility ranking?                           | 2nd (0.900) — below BBR (0.947), above CUBIC (0.884)               |
| 2.11 | What is DQN S2 utility ranking?                           | 3rd (0.757) — below NewReno (0.923) and CUBIC (0.818)              |
| 2.12 | What is DQN S2 loss rate?                                 | 5.54% — must be honestly disclosed                                 |
| 2.13 | May you start Phase 5 implementation now?                 | NO — must fix gaps and receive Spec Owner approval first           |
| 2.14 | Is the utility score final?                               | No — it is provisional (α=1.0, β=0.1, λ=10.0)                      |
| 2.15 | Which OpenSpec change is the source of truth for Phase 5? | `reporting-figures-and-demo`                                       |

---

## 3. Required Gemini Intake Report Format

After reading all files and answering all questions, submit the following report to the Spec Owner. Do not begin any code changes before receiving Spec Owner confirmation.

```markdown
# Gemini Intake Understanding Report

**Date:** [YYYY-MM-DD]
**Submitted by:** Antigravity (Gemini Pro)
**Re:** Handoff from Antigravity (Claude Sonnet 4.6 Thinking)

---

## 1. Repo State I Observed

- Current branch:
- Latest commit:
- Working tree state:
- OpenSpec version:
- OpenSpec validation result for Change 05:
- Directories present: [list key directories you confirmed]

## 2. OpenSpec State I Observed

- `.agent/skills/` present: YES/NO — list skills
- `.agent/workflows/` present: YES/NO — list workflows
- Active changes listed by `openspec status`:
- `openspec validate reporting-figures-and-demo --strict` output:

## 3. Phase 3 / Phase 4 Artifacts I Read

List every artifact you read, and for each state what it confirmed:

- `baseline_summary.csv`: confirmed [...]
- `dqn_vs_baseline_summary.csv`: confirmed [...]
- `phase4-excellent-acceptance-report.md`: confirmed [...]
- [etc.]

## 4. Change 05 Gaps I Confirmed

### Gap 1: Validation Proof

- File that needs creating: `reports/handoff/change05-validation-note.md`
- What I will put in it: [describe]
- Acceptance criteria I understand: [describe]

### Gap 2: tasks.md Completion Sync

- File: `openspec/changes/reporting-figures-and-demo/tasks.md`
- Current state: all tasks are `[ ]`
- Tasks I identify as already complete: [list them]
- Tasks I will leave unchecked (Phase 5 implementation): [list them]

### Gap 3: Markdown Formatting

- Files affected: [list affected spec files]
- Issues I confirmed: [describe per file]
- What I will fix: [describe]
- What I will NOT change: delta requirement blocks, metric values, spec content

## 5. What I Will Fix First

In strict order:

1. [Gap 1 fix]
2. [Gap 2 fix]
3. [Gap 3 fix]
   Then commit and wait for Spec Owner review.

## 6. What I Will Not Touch

- `experiments/summaries/baseline_summary.csv` — frozen Phase 3 data
- `experiments/drl/summaries/dqn_summary.csv` — frozen Phase 4 data
- `experiments/drl/summaries/dqn_vs_baseline_summary.csv` — frozen
- `experiments/drl/models/` — trained models, not to be retrained
- `figures/` — existing Phase 3/4 figures, not to be regenerated
- Any OpenSpec change for Change 01–04
- DQN training scripts (no retraining)
- No PPO, IPFS, QUIC, multi-agent, multi-path

## 7. Questions / Risks Before Proceeding

[List any genuine ambiguities or risks you have identified that need Spec Owner input before you proceed]

## 8. Ready for Spec Owner Confirmation

[ ] I have read the full repo
[ ] I have read the handoff document
[ ] I understand all three gaps to fix
[ ] I understand what must not be modified
[ ] I understand my first deliverable is this report, not code
[ ] I am waiting for Spec Owner confirmation before making any changes
```

---

## 4. Pass / Fail Criteria for Gemini Intake

The Spec Owner will use the following criteria to accept or reject the Gemini Intake Report:

### ✅ PASS criteria (all must be met)

| Criterion       | Required Response                                                                   |
| --------------- | ----------------------------------------------------------------------------------- |
| Phase awareness | Correctly states Phase 4 complete, Phase 5 not started                              |
| Gap 1 awareness | Correctly identifies `change05-validation-note.md` as missing artifact              |
| Gap 2 awareness | Correctly identifies that `tasks.md` is fully unchecked and needs sync              |
| Gap 3 awareness | Correctly identifies specific markdown formatting issues in spec files              |
| Data integrity  | Explicitly commits to not modifying any CSV files                                   |
| No retraining   | Explicitly commits to not running DQN training                                      |
| No overclaiming | Demonstrates understanding of forbidden wording (e.g., "true RTT", "DQN beats TCP") |
| Sequencing      | Explicitly states will fix gaps BEFORE Phase 5, not concurrently                    |
| Spec Owner gate | Explicitly states will wait for Spec Owner approval after gap fixes                 |

### ❌ FAIL criteria (any one is disqualifying)

| Criterion                | Disqualifying Behavior                                                    |
| ------------------------ | ------------------------------------------------------------------------- |
| Premature implementation | Begins Phase 5 (report/figures/demo/PPT) without approval                 |
| Data modification        | Proposes to modify any CSV, figure, or experimental result                |
| Retraining               | Proposes to retrain DQN or re-run baseline simulations                    |
| Scope expansion          | Proposes PPO, IPFS, QUIC, multi-agent, or multi-path                      |
| Overclaiming             | Uses forbidden wording in understanding report                            |
| Gap ignorance            | Does not identify all three gaps, or misidentifies what they are          |
| No wait                  | Does not indicate readiness to wait for Spec Owner confirmation           |
| Fabricated outputs       | Includes command outputs or validation results that were not actually run |

---

_Checklist produced by Antigravity (Claude Sonnet 4.6 Thinking) on 2026-06-10._
