# Claude → Gemini Formal Handoff Document

**Handoff Author:** Antigravity (Claude Sonnet 4.6 Thinking)  
**Handoff Recipient:** Antigravity (Gemini Pro)  
**Handoff Date:** 2026-06-10  
**Project:** DRL-Based Congestion Control over a Bottleneck Link  
**Repo:** https://github.com/donuop35/ns3-drl-congestion-control  
**Status at Handoff:** Phase 4 Excellent Acceptance Complete / Change 05 Spec Created / Pending Phase 5 Approval

> ⚠️ **IMPORTANT FOR GEMINI:** This document is your onboarding source of truth. Read it completely before touching any file. Your first deliverable is a **Gemini Intake Understanding Report**, not code.

---

## 1. Executive Summary

This project implements Deep Reinforcement Learning (DRL) for TCP congestion control in a single-bottleneck ns-3 network environment. Phase 4 (DRL MVP Implementation) has been formally accepted by the Spec Owner at the "Excellent Acceptance" level, covering SB3 DQN training and evaluation for two scenarios (S1 Low Delay, S2 High Delay), real-ZMQ ns3-gym smoke tests, and a complete comparison against TCP baselines (NewReno, CUBIC, BBR).

Change 05 (`reporting-figures-and-demo`) has been created using the official OpenSpec workflow and the `openspec validate reporting-figures-and-demo --strict` command confirms the change is valid. The Change 05 spec defines the governance rules for the Phase 5 Final Package (Final Report, Figures, Demo, PPT, README finalization).

**The next step is NOT to begin Phase 5 implementation.** Before Phase 5, Gemini must: (1) read the full repo and this handoff, (2) submit an intake understanding report to the Spec Owner, (3) fix three specific Change 05 gaps after Spec Owner approval, and (4) await final approval before starting Phase 5 implementation.

---

## 2. Project Identity

| Field                | Value                                                                                                        |
| -------------------- | ------------------------------------------------------------------------------------------------------------ |
| **Repo URL**         | https://github.com/donuop35/ns3-drl-congestion-control                                                       |
| **Project Title**    | Deep Reinforcement Learning for Congestion Control and Throughput Optimization over a Single Bottleneck Link |
| **Chinese Title**    | 以深度強化學習進行單一瓶頸鏈路壅塞控制與吞吐量最佳化                                                         |
| **GitHub Repo Name** | ns3-drl-congestion-control                                                                                   |
| **Spec Owner**       | 使用者本人 — verifies, approves, and gates all phase transitions                                             |
| **Antigravity Role** | AI Coding Agent — implements per approved specs, never modifies experimental results                         |
| **OpenSpec Role**    | Official SDD workflow — `@fission-ai/openspec@1.4.1`, governs all changes                                    |
| **Current Phase**    | Phase 4 Excellent Acceptance Complete / Change 05 Spec Done                                                  |
| **Next Phase**       | Phase 5: Final Reporting / Demo / PPT Package (PENDING Spec Owner approval)                                  |

---

## 3. Official OpenSpec Status

| Item                          | Status                                                                                                                                           |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| OpenSpec version              | **1.4.1** (`@fission-ai/openspec@1.4.1`)                                                                                                         |
| Node.js version               | v20.20.2 (Windows, meets ≥ 20.19.0 requirement)                                                                                                  |
| Official OpenSpec initialized | ✅ YES — `openspec init` executed, `.openspec` config present                                                                                    |
| `.agent/skills/`              | ✅ EXISTS — contains 5 skills: `openspec-apply-change`, `openspec-archive-change`, `openspec-explore`, `openspec-propose`, `openspec-sync-specs` |
| `.agent/workflows/`           | ✅ EXISTS — contains 5 workflows: `opsx-apply.md`, `opsx-archive.md`, `opsx-explore.md`, `opsx-propose.md`, `opsx-sync.md`                       |
| `openspec-preview/`           | ⚠️ May exist as historical artifact — **NOT a source of truth**, do not use                                                                      |
| Change 05 official folder     | ✅ EXISTS — `openspec/changes/reporting-figures-and-demo/`                                                                                       |
| Validation command            | ✅ EXECUTED — `openspec validate reporting-figures-and-demo --strict`                                                                            |
| Validation result             | ✅ **PASSED** — `Change 'reporting-figures-and-demo' is valid`                                                                                   |

**Active OpenSpec Changes:**

| Change ID                    | Folder                                         | Status                              |
| ---------------------------- | ---------------------------------------------- | ----------------------------------- |
| `project-charter`            | `openspec/changes/project-charter/`            | ✅ 4/4 artifacts, Approved          |
| `ns3-baseline-benchmark`     | `openspec/changes/ns3-baseline-benchmark/`     | ✅ 4/4 artifacts, Spec Approved     |
| `opengym-env`                | `openspec/changes/opengym-env/`                | ✅ 4/4 artifacts, Spec Approved     |
| `dqn-mvp-agent`              | `openspec/changes/dqn-mvp-agent/`              | ✅ 4/4 artifacts, Spec Approved     |
| `reporting-figures-and-demo` | `openspec/changes/reporting-figures-and-demo/` | ✅ Valid, Pending Spec Owner Review |

> ⚠️ **Validation Note for Gemini:** Although validation passed when Claude ran it before handoff, Gemini MUST independently re-run `openspec validate reporting-figures-and-demo --strict` upon taking over and record the result in `reports/handoff/change05-validation-note.md`. Do not assume the output is unchanged.

---

## 4. Phase Timeline and Acceptance Status

| Phase / Change      | Purpose                                                   | Status                             | Acceptance Level              | Key Artifacts                                                                                     | Notes                                    |
| ------------------- | --------------------------------------------------------- | ---------------------------------- | ----------------------------- | ------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| Phase 0 (Change 01) | Project charter, scope, non-goals, MDP definition         | ✅ Complete                        | Spec Owner Approved           | `openspec/changes/project-charter/`                                                               | Frozen — do not modify                   |
| Phase 1 (Change 02) | ns-3.40 baseline benchmark: topology, metrics, scenarios  | ✅ Spec Approved                   | Spec Owner Approved           | `openspec/changes/ns3-baseline-benchmark/`                                                        | Frozen                                   |
| Phase 2 (Change 03) | OpenGym env: MDP interface, obs/action/reward, smoke test | ✅ Spec Approved                   | Spec Owner Approved           | `openspec/changes/opengym-env/`                                                                   | Frozen                                   |
| Phase 3             | ns-3.40 TCP baseline execution (NewReno, CUBIC, BBR)      | ✅ Complete                        | Spec Owner Accepted           | `baseline_summary.csv`, `phase3-baseline-report.md`, `figures/baseline/`                          | Results FROZEN                           |
| Phase 4 (Change 04) | DQN MVP: ns3-gym + SB3 DQN training, eval, comparison     | ✅ Complete                        | **Excellent Acceptance**      | `dqn_summary.csv`, `dqn_vs_baseline_summary.csv`, models, `phase4-excellent-acceptance-report.md` | Results FROZEN                           |
| Change 05           | Final Package spec: Report, Figures, Demo, PPT, README    | ✅ Spec Created, Validation Passed | **Pending Spec Owner Review** | `openspec/changes/reporting-figures-and-demo/`                                                    | 3 gaps to fix before Phase 5             |
| Phase 5             | Final Reporting / Demo / PPT Package Implementation       | ⏳ NOT STARTED                     | Not Approved                  | N/A                                                                                               | Must not start until Spec Owner approves |

---

## 5. Source of Truth Map

Gemini MUST read these artifacts before taking any action:

| Priority    | File                                                            | What It Proves                                                       |
| ----------- | --------------------------------------------------------------- | -------------------------------------------------------------------- |
| 🔴 CRITICAL | `README.md`                                                     | Project status, toolchain, results summary, limitations, known TODOs |
| 🔴 CRITICAL | `openspec/changes/reporting-figures-and-demo/` (all files)      | Change 05 governance spec — the blueprint for Phase 5                |
| 🔴 CRITICAL | `reports/phase4-drl-mvp/phase4-excellent-acceptance-report.md`  | Phase 4 final acceptance record with real S1/S2 DQN numbers          |
| 🔴 CRITICAL | `experiments/drl/summaries/dqn_vs_baseline_summary.csv`         | The authoritative comparison data for all deliverables               |
| 🔴 CRITICAL | `experiments/drl/summaries/dqn_summary.csv`                     | S1 and S2 DQN training/eval summary                                  |
| 🟠 HIGH     | `reports/phase4-drl-mvp/artifact-index.md`                      | Complete inventory of Phase 4 artifacts                              |
| 🟠 HIGH     | `reports/phase3-baseline/phase3-baseline-report.md`             | Phase 3 baseline results and methodology                             |
| 🟠 HIGH     | `experiments/summaries/baseline_summary.csv`                    | Authoritative baseline CSV data                                      |
| 🟠 HIGH     | `reports/handoff/claude-to-gemini-handoff.md`                   | This document                                                        |
| 🟡 MEDIUM   | `reports/phase4-drl-mvp/smoke-test-report.md`                   | Real ZMQ smoke test proof                                            |
| 🟡 MEDIUM   | `experiments/drl/summaries/dqn_action_distribution_summary.csv` | DQN policy behavior data                                             |
| 🟡 MEDIUM   | `experiments/drl/summaries/dqn_seed_sensitivity_summary.csv`    | Determinism proof (std=0.000)                                        |
| 🟡 MEDIUM   | `figures/baseline/`, `figures/drl/`, `figures/comparison/`      | All existing generated figures                                       |
| 🟡 MEDIUM   | `openspec/changes/dqn-mvp-agent/tasks.md` (Section 14)          | Implementation status of Phase 4                                     |

---

## 6. Technical Architecture Summary

### 6.1 Network Simulation Layer (ns-3.40)

- **Simulator:** ns-3.40 (frozen per Change 02; do NOT use ns-3.35/3.36 or any "latest")
- **Topology:** Single bottleneck: `sender → bottleneck router → receiver`
- **Bottleneck:** 10 Mbps link; S1=10ms RTT, S2=50ms RTT
- **TCP Baselines:** `ns3::TcpLinuxReno` (NewReno), `ns3::TcpCubic` (CUBIC), `ns3::TcpBbr` (BBR)
- **Metrics collection:** FlowMonitor XML + CSV

### 6.2 RL Interface Layer (ns3-gym)

- **Library:** `tkn-tub/ns3-gym`, commit `cfff7f3`
- **Location (in WSL2):** `~/ns-allinone-3.40/ns-3.40/contrib/opengym`
- **C++ environment:** `src/congestion-env/` compiled to `ns3.40-congestion-env-optimized`
- **Python wrapper:** `src/gym_env/ns3_congestion_env.py` (451 lines, subprocess + ZMQ)
- **Compatibility patches:** `np.float` → `np.float32` (NumPy 1.24+), `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python`

### 6.3 RL Agent (SB3 DQN)

- **Algorithm:** `stable_baselines3.DQN` v2.4.1 — **NOT PPO**, **NOT A2C**, **NOT SAC**
- **Observation Space:** `Box(5,)` — `[throughput_normalized, delay_normalized, loss_normalized, action_0_ratio, action_1_ratio]`
- **Action Space:** `Discrete(3)` — `{0: decrease rate, 1: keep rate, 2: increase rate}`
- **Action Abstraction:** Fallback Option B — **sender-side rate-control abstraction** — does NOT directly modify Linux kernel TCP `cwnd`. This is a critical limitation to disclose.
- **Reward:** `r = α·throughput_norm - β·delay_norm - λ·loss_norm` with `α=1.0, β=0.1, λ=10.0` (provisional weights)
- **Training:** 30,000 steps, seed=42, ~18 min on CPU
- **Evaluation:** 5 episodes, deterministic=True

### 6.4 Metrics Definitions

| Metric     | Definition                                              | Important Caveat                              |
| ---------- | ------------------------------------------------------- | --------------------------------------------- |
| Throughput | FlowMonitor `rxBytes / simDuration` (Mbps)              | Reliable                                      |
| Delay      | `FlowMonitor delaySum / rxPackets` (ms)                 | **PROXY only — NOT direct TCP RTT**           |
| Loss Rate  | `(txPackets - rxPackets) / txPackets`                   | Reliable                                      |
| Utility    | `α·(tput/max_tput) - β·(delay/max_delay) - λ·loss_rate` | **PROVISIONAL** — weights subject to revision |

### 6.5 Comparison Logic

- Source: `experiments/drl/summaries/dqn_vs_baseline_summary.csv`
- Script: `src/analysis/compare_dqn_baseline.py`
- Outputs: `figures/comparison/dqn_vs_baseline_{metric}_{scenario}.png`

---

## 7. Current Results Summary

### 7.1 Phase 3 Baseline — Frozen Ground Truth

**Scenario S1 (10 Mbps, 10ms RTT, 60s, seed=42):**

| Algorithm | Throughput (Mbps) | Avg Delay (ms)† | Loss Rate | Utility‡  |
| --------- | :---------------: | :-------------: | :-------: | :-------: |
| BBR       |     **9.727**     |    **25.9**     | 0.000000  | **0.947** |
| CUBIC     |       9.894       |      117.7      | 0.000504  |   0.884   |
| NewReno   |       9.824       |      105.4      | 0.000731  |   0.875   |

**Scenario S2 (10 Mbps, 50ms RTT, 60s, seed=42):**

| Algorithm | Throughput (Mbps) | Avg Delay (ms)† | Loss Rate | Utility‡  |
| --------- | :---------------: | :-------------: | :-------: | :-------: |
| NewReno   |     **9.794**     |      129.4      | 0.001363  | **0.923** |
| CUBIC     |       9.588       |      156.3      | 0.008848  |   0.818   |
| BBR ⚠️    |       0.385       |      148.7      | 0.015816  |  -0.169   |

> ⚠️ BBR S2 anomaly: Known ns-3.40 TcpBbr bug in high-RTT scenario. Documented limitation.  
> † Delay is FlowMonitor proxy, NOT direct TCP RTT.  
> ‡ Utility is provisional.

**S3 and S4 are supplementary (NewReno/CUBIC only; optional for final reporting).**

---

### 7.2 Phase 4 DQN S1 — Frozen

| Metric               | Value                                                          |
| -------------------- | -------------------------------------------------------------- |
| Training steps       | 30,000 (seed=42)                                               |
| ep_rew_mean at end   | 84.4                                                           |
| Throughput           | 9.877 Mbps                                                     |
| Avg Delay            | 115.3 ms (proxy)                                               |
| Loss Rate            | 0.40%                                                          |
| **Utility**          | **0.900 — Ranks 2nd (below BBR 0.947, above CUBIC 0.884)**     |
| Action distribution  | 100% increase (Action 2) — **degenerate near-capacity policy** |
| Eval episodes        | 5 (seeds 42–46)                                                |
| Seed sensitivity std | **0.000** (deterministic policy in deterministic simulator)    |
| Model artifact       | `experiments/drl/models/dqn_s1_seed42.zip`                     |

### 7.3 Phase 4 DQN S2 — Frozen

| Metric               | Value                                                                 |
| -------------------- | --------------------------------------------------------------------- |
| Training steps       | 30,000 (seed=42)                                                      |
| ep_rew_mean at end   | 86.5                                                                  |
| Throughput           | 9.786 Mbps                                                            |
| Avg Delay            | 148.8 ms (proxy)                                                      |
| Loss Rate            | **5.54%** ← Must disclose honestly                                    |
| **Utility**          | **0.757 — Ranks 3rd (below NewReno 0.923, below CUBIC 0.818)**        |
| Action distribution  | 86.87% increase, 13.13% decrease — does not degenerate as badly as S1 |
| Eval episodes        | 5 (seeds 42–46)                                                       |
| Seed sensitivity std | **0.000** (deterministic)                                             |
| Model artifact       | `experiments/drl/models/dqn_s2_seed42.zip`                            |

### 7.4 Key Findings (Mandatory Disclosures)

1. **DQN does NOT universally outperform TCP.** S2 DQN ranks 3rd.
2. **S1 policy is degenerate** — 100% "increase" action is near-capacity behavior, not adaptive control.
3. **S2 has high loss (5.54%)** — DQN over-prioritizes throughput in high-RTT conditions.
4. **Delay metric is a proxy**, not direct TCP RTT. Do not call it "true RTT" anywhere.
5. **DQN uses Fallback Option B** (sender-side rate abstraction), not kernel TCP `cwnd` modification.
6. **Utility score is provisional** — weights α=1.0, β=0.1, λ=10.0 may be revised.
7. **BBR S2 anomaly** — BBR near-zero throughput in S2 is a known ns-3.40 limitation.

---

## 8. Current Git / Commit State

**As of 2026-06-10T02:31 UTC:**

| Field         | Value                                                                    |
| ------------- | ------------------------------------------------------------------------ |
| Branch        | `main`                                                                   |
| Latest commit | `9ae8a2c` — `openspec: create Change 05 reporting-figures-and-demo spec` |
| Working tree  | ✅ Clean — `nothing to commit, working tree clean`                       |

**Recent commit history (latest 15):**

```
9ae8a2c openspec: create Change 05 reporting-figures-and-demo spec
900f4cb phase4: final excellent acceptance cleanup and artifact sync
465959e Phase 4 Excellent Acceptance COMPLETE (Step 3-6: S2 DQN + all figures)
2e3b253 Phase 4 Excellent Acceptance Upgrade (Step 0-2, 7-9)
abe8fe5 phase4: COMPLETE - DQN training+eval+comparison done (commit final)
211bf2b phase4: README update - Phase 4 in progress, smoke test results, DQN training instructions
f054657 phase4: fix SB3 Monitor compatibility (episode→ep_num), progress_bar=False, train_dqn.sh update
5598a67 phase4: Step 3 SMOKE TEST PASSED (real ZMQ) - S1+S2 both PASS
197c703 phase4: ns3gym install+compat fixes; all Python deps OK; deploy/build scripts
6bad551 phase4: add setup_ns3gym.sh + build_opengym.sh; all Python deps installed (SB3 2.4.1, torch 2.4.1, gymnasium 1.0.0)
6c4c87f phase4: Step 1-6 code artifacts complete
eab5765 phase4: Step 0 preflight audit complete (GO); Phase 4 dir structure + install_ns3gym.sh created
507496e phase3: fix baseline report status and README after spec-owner review
604af3e phase3: ALL STEPS COMPLETE - baseline_summary.csv (10 runs), 4 figures, phase3-baseline-report.md; S1/S2 NewReno+CUBIC+BBR, S3/S4 NewReno+CUBIC
8c5bdc8 phase3: fix baseline-benchmark.cc (IsEmpty→GetN, TcpLinuxReno, flow-monitor-module); fix baseline_runner.sh (TypeId names, NS3_HOME path)
```

**Files added by latest commit `9ae8a2c` (Change 05):**

```
openspec/changes/reporting-figures-and-demo/.openspec.yaml
openspec/changes/reporting-figures-and-demo/design.md
openspec/changes/reporting-figures-and-demo/proposal.md
openspec/changes/reporting-figures-and-demo/specs/artifact-manifest.md
openspec/changes/reporting-figures-and-demo/specs/demo-script.md
openspec/changes/reporting-figures-and-demo/specs/figure-package.md
openspec/changes/reporting-figures-and-demo/specs/final-report-package.md
openspec/changes/reporting-figures-and-demo/specs/ppt-package.md
openspec/changes/reporting-figures-and-demo/specs/readme-finalization.md
openspec/changes/reporting-figures-and-demo/specs/reporting-figures-and-demo/spec.md
openspec/changes/reporting-figures-and-demo/specs/result-interpretation.md
openspec/changes/reporting-figures-and-demo/specs/risk-register.md
openspec/changes/reporting-figures-and-demo/tasks.md
```

---

## 9. Known Change 05 Gaps To Fix Before Phase 5

These three gaps must be addressed by Gemini **before** Phase 5 implementation may begin. They are minor governance/documentation fixes, not technical or experimental changes.

---

### Gap 1: OpenSpec Validation Proof Not Yet Recorded in Repo

**File:** `reports/handoff/change05-validation-note.md` (does not yet exist)

**Problem:** Although Claude executed `openspec validate reporting-figures-and-demo --strict` and it passed, the output was not committed as a formal artifact. The repo contains no written record of this validation run.

**Why it matters:** The Spec Owner requires formal proof that validation passed. Without this file, the governance chain has a gap between "validation occurred" and "validation is documented".

**Exact fix expected from Gemini:**

1. Re-run `openspec validate reporting-figures-and-demo --strict` independently.
2. Create `reports/handoff/change05-validation-note.md` containing:
   - The exact command run
   - The exact output
   - Timestamp of execution
   - Confirmation of pass/fail status
3. Commit this file.

**Acceptance criteria:** The file exists, contains the actual command output, and is committed to `main`.

**What NOT to change:** Do not modify any `openspec/changes/reporting-figures-and-demo/` spec files as part of this fix. This is purely a documentation artifact.

---

### Gap 2: Change 05 `tasks.md` Has All Tasks Unchecked

**File:** `openspec/changes/reporting-figures-and-demo/tasks.md`

**Problem:** All 35+ tasks in `tasks.md` are currently `[ ]` (unchecked), including tasks that are already **factually complete** as of the specification phase. For example:

- Task 0.1–0.4 (OpenSpec verification) — Claude already performed these
- Tasks 2.1–2.4, 3.1–3.4, 4.1–4.4, 5.1–5.5, 6.1–6.4, 7.1–7.3, 8.1–8.5 — spec files already created
- Tasks 9.1–9.5 (scope review and validation) — already completed

**Why it matters:** A fully unchecked `tasks.md` gives the false impression that no specification work has been done, undermining the governance record.

**Exact fix expected from Gemini:**

1. Read each task carefully.
2. Mark `[x]` for tasks whose corresponding artifact or action is already complete.
3. Leave `[ ]` for tasks that require Phase 5 implementation (e.g., actual README finalization, final report writing, demo video recording).
4. Do NOT check off tasks that require live Phase 5 implementation work.
5. Specifically: Section 9.6 ("Stop and wait for Spec Owner review") should reflect current status.

**Acceptance criteria:** The tasks.md reflects the real state — specification tasks done are checked, implementation tasks are not.

**What NOT to change:** Do not alter the task descriptions, task IDs, or section structure. Only change `[ ]` to `[x]` for completed items.

---

### Gap 3: Markdown Formatting and Readability in Change 05 Spec Files

**Files:** All `.md` files in `openspec/changes/reporting-figures-and-demo/specs/`

**Problem:** Several Change 05 spec files have minor formatting issues introduced during the OpenSpec validation compliance edits:

- `result-interpretation.md`: The `## 1. Core Principle` section and `## 2. S1 Interpretation` section lost their natural paragraph structure when delta headers were prepended — the content runs together without clear section breaks.
- `risk-register.md`: The table header row `| Risk ID | Description | ...` was accidentally removed during the delta edit; the table may render without proper headers.
- `readme-finalization.md`: The `## 2. Final Sections Required` header was removed during the delta edit, causing the numbered list to appear directly under `## 1. Overview`.
- `ppt-package.md`: The bullet list `- The presentation must contain exactly 10–12 slides. / - It must be timed...` was accidentally condensed.

**Why it matters:** These are spec documents that the Spec Owner and future Gemini must rely on. Poor formatting degrades readability and may cause misinterpretation.

**Exact fix expected from Gemini:**

1. Read each affected spec file.
2. Restore missing section headers (e.g., `## 2. S1 Interpretation`, `## 2. Final Sections Required`, table header row in risk-register).
3. Ensure the `risk-register.md` table has a proper header row.
4. Do NOT change any spec content, conclusions, metric values, or scope boundaries.
5. Do NOT remove the `## ADDED Requirements` / `### Requirement:` / `#### Scenario:` blocks — these are required by OpenSpec and must remain.

**Acceptance criteria:** All spec files render cleanly as Markdown. Section structure is intact. `openspec validate reporting-figures-and-demo --strict` still passes after the cleanup.

**What NOT to change:** Do not alter metric values, interpretation rules, forbidden wording lists, or the delta requirement blocks.

---

## 10. Gemini First Task After Handoff

**Strict sequencing — no exceptions:**

1. **Read the full repo.** Use `git log`, `dir`, file reads. Do not skip any critical artifact.
2. **Read this handoff document** from top to bottom.
3. **Read the latest `git diff`** (`git show 9ae8a2c --stat` and key diffs).
4. **Output a Gemini Intake Understanding Report** using the format in `gemini-intake-checklist.md`.
5. **Wait for Spec Owner confirmation** that your understanding is correct.
6. **Fix the three Change 05 gaps** (after approval):
   - Gap 1: Create `change05-validation-note.md`
   - Gap 2: Sync `tasks.md` checked/unchecked status
   - Gap 3: Formatting cleanup in spec files
7. **Commit the gap fixes** and submit for Spec Owner review.
8. **Wait for Spec Owner approval** before Phase 5 implementation.
9. **Only then** may you begin Phase 5 (Final Reporting / Demo / PPT Package implementation).

---

## 11. Strict No-Go Rules

The following are **permanently prohibited** throughout Phase 5:

| Rule                     | Prohibition                                                                                       |
| ------------------------ | ------------------------------------------------------------------------------------------------- |
| No retraining            | Never re-run `train_dqn.sh` or `train_dqn.py`                                                     |
| No baseline re-execution | Never re-run `baseline_runner.sh` or `analysis.py` (unless fixing a bug with Spec Owner approval) |
| No CSV modification      | Never manually edit any `.csv` file in `experiments/`                                             |
| No fake figures          | Never generate figures from random data or hardcoded values                                       |
| No result inflation      | Never claim DQN universally beats TCP; never hide S2 loss=5.54%                                   |
| No PPO                   | Never introduce PPO, A2C, SAC, or any other RL algorithm                                          |
| No IPFS                  | Never implement IPFS-related networking                                                           |
| No QUIC                  | Never implement QUIC congestion control                                                           |
| No multi-agent           | Never expand beyond a single DQN agent                                                            |
| No multi-path            | Never expand beyond the single bottleneck topology                                                |
| No archive               | Never run `openspec archive` on any change                                                        |
| No direct Phase 5        | Never start Phase 5 implementation before gap fixes are accepted                                  |
| No overclaiming          | Never write "DRL beats TCP", "true RTT", "kernel-level control", "production-ready"               |
| No fake commands         | Never fabricate command outputs in reports                                                        |

---

## 12. Recommended Gemini Prompt Sequence

The Spec Owner will issue prompts to Gemini in this order. These are reference titles only:

1. **"Gemini Intake Report Prompt"** — Purpose: Confirm Gemini has read the repo and handoff, and understands the project state, gaps, and constraints before taking any action. Gemini must submit an intake report in the specified format.

2. **"Change 05 Gap Fix Prompt"** — Purpose: Instruct Gemini to fix the three specific gaps (validation note, tasks.md sync, markdown cleanup) after the intake report is accepted. Gemini commits the fixes and waits for review.

3. **"Phase 5 Implementation Prompt"** — Purpose: Once gap fixes are accepted by Spec Owner, authorize Gemini to proceed with Phase 5 (Final Reporting / Demo / PPT Package) implementation following the Change 05 spec as source of truth.

---

## 13. Handoff Acceptance Checklist

The Spec Owner should verify this checklist before accepting the handoff:

- [ ] Repo state (current branch, clean working tree, latest commit) is clearly documented
- [ ] OpenSpec version and validation result are recorded
- [ ] `.agent/skills` and `.agent/workflows` are confirmed present
- [ ] All active OpenSpec changes are listed with their status
- [ ] Phase 3 baseline results are correctly summarized (S1/S2/S3/S4, NewReno/CUBIC/BBR)
- [ ] Phase 4 DQN S1 results are correctly summarized (utility 0.900, ranks 2nd)
- [ ] Phase 4 DQN S2 results are correctly summarized (utility 0.757, ranks 3rd, loss 5.54%)
- [ ] Phase 4 honest limitations are explicitly stated (delay proxy, Fallback Option B, degenerate S1 policy)
- [ ] Change 05 purpose and scope are correctly described
- [ ] All three Change 05 gaps are specifically described with fix instructions
- [ ] Gemini's first task (intake report) is clearly stated
- [ ] No-go rules are clearly enumerated
- [ ] No fake results or fabricated data present in this document
- [ ] No scope expansion (PPO/IPFS/QUIC/multi-agent/multi-path) present in this document
- [ ] This document does not instruct Gemini to begin Phase 5 directly

---

_Document produced by Antigravity (Claude Sonnet 4.6 Thinking) on 2026-06-10 as the formal handoff package for Antigravity (Gemini Pro)._
