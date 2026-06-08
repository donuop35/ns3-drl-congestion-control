# Tasks: Change 03 OpenGym Environment Specification

> ⚠️ 本 change 的所有 tasks 均為**規格任務**，不含 ns-3 coding、benchmark execution、DQN training 等 implementation 任務。
> 不得在 Spec Owner 驗收前執行 /opsx:apply 或進入任何 implementation。

---

## 0. Official OpenSpec Verification

- [x] 0.1 Confirm `@fission-ai/openspec` is installed (`openspec --version` → 1.4.1)
- [x] 0.2 Confirm repo is initialized with official OpenSpec (`openspec list --json` works)
- [x] 0.3 Confirm Change 03 is created under official OpenSpec (`openspec new change "opengym-env"`)
- [x] 0.4 Confirm Antigravity tool integration is enabled (`.agent/skills/openspec-*/` exists)
- [x] 0.5 Confirm no fake OpenSpec workflow was used; all artifacts are under `openspec/changes/opengym-env/`

---

## 1. Specification Dependency Check

- [x] 1.1 Confirm dependency on Change 01 project-charter (✅ approved, scope / non-goals / toolchain frozen)
- [x] 1.2 Confirm dependency on Change 02 ns3-baseline-benchmark (✅ approved, ns-3.40 frozen, metrics frozen)
- [x] 1.3 Confirm no implementation is included in this change
- [x] 1.4 Confirm ns-3 target version is ns-3.40 (inherited from Change 02, Spec Owner frozen)
- [x] 1.5 Confirm baseline metrics (throughput / RTT / loss / utility) are inherited from Change 02

---

## 2. MDP Interface Specification

- [x] 2.1 Confirm MDP interface M = (S, A, P, R, γ) is formally defined in `specs/mdp-interface.md`
- [x] 2.2 Confirm environment boundary is defined (ns-3 single bottleneck simulation abstraction)
- [x] 2.3 Confirm agent boundary is defined (sender-side only; no kernel-level TCP modification)
- [x] 2.4 Confirm transition dynamics P(s_{t+1}|s_t, a_t) is clarified as ns-3 determined
- [x] 2.5 Confirm discount factor γ = 0.99 is listed as initial recommendation (Change 04 may adjust)
- [x] 2.6 Confirm decision step concept is defined (fixed time interval per step)
- [x] 2.7 Confirm episode / horizon concept is defined (sim_duration / decision_interval)

---

## 3. Observation Space Specification

- [x] 3.1 Confirm MVP minimal observation has 5 fields with fixed index order (in `specs/observation-space.md`)
- [x] 3.2 Confirm `throughput_norm` (index 0) is defined with source and normalization
- [x] 3.3 Confirm `delay_norm` (index 1) is defined with source and normalization
- [x] 3.4 Confirm `loss_norm` (index 2) is defined with source and normalization
- [x] 3.5 Confirm `congestion_indicator` (index 3) is defined with derivation method
- [x] 3.6 Confirm `prev_action_norm` (index 4) is defined with normalization ({0→0.0, 1→0.5, 2→1.0})
- [x] 3.7 Confirm enhanced observation fields are listed as future extension only
- [x] 3.8 Confirm observation normalization rules are defined (all numeric, all normalizable, values bounded)
- [x] 3.9 Confirm observation fallback rules are defined (RTT → delay estimate, queue → delay proxy)

---

## 4. Action Space Specification

- [x] 4.1 Confirm discrete action space A = {0: decrease, 1: keep, 2: increase} (in `specs/action-space.md`)
- [x] 4.2 Confirm action semantics are defined for each of the 3 actions
- [x] 4.3 Confirm action safety rules are defined (no negative rate, bounded effect, action logged)
- [x] 4.4 Confirm no kernel-level TCP modification rule is stated
- [x] 4.5 Confirm continuous action is listed as future extension only (requires separate OpenSpec change)
- [x] 4.6 Confirm PPO is explicitly excluded from MVP (PPO exclusion rule in `action-space.md`)

---

## 5. Reward Function Specification

- [x] 5.1 Confirm base reward concept: `r_t = α·throughput_norm − β·delay_norm − λ·loss_norm` (in `specs/reward-function.md`)
- [x] 5.2 Confirm λ (lambda) is used for loss penalty (not γ, to avoid confusion with discount factor)
- [x] 5.3 Confirm reward weights α, β, λ are marked as provisional (Change 04 defines initial values)
- [x] 5.4 Confirm reward normalization philosophy is defined (all components normalized before weighting)
- [x] 5.5 Confirm reward failure modes are listed (throughput-only, over-penalized delay/loss, sparse reward)
- [x] 5.6 Confirm reward ablation plan is listed (throughput-only / +delay / full)
- [x] 5.7 Confirm relationship to Change 02 utility score is documented

---

## 6. Episode / Step / Reset Specification

- [x] 6.1 Confirm reset concept flow is defined in `specs/episode-step-reset.md`
- [x] 6.2 Confirm step concept flow is defined (action → sender control → ns-3 advance → metrics → reward)
- [x] 6.3 Confirm terminated concept is defined (simulation duration reached)
- [x] 6.4 Confirm truncated concept is defined (time limit / fatal error)
- [x] 6.5 Confirm terminated and truncated cannot both be True simultaneously
- [x] 6.6 Confirm info dictionary requirements are fully specified (10+ required fields)
- [x] 6.7 Confirm info dict includes `raw_throughput_mbps`, `raw_delay_ms`, `raw_loss_rate`, `utility_score`
- [x] 6.8 Confirm info dict includes `scenario_id`, `step_index`, `action_applied`, `action_symbol`
- [x] 6.9 Confirm baseline metric compatibility rule is stated (units and calculation match Change 02)

---

## 7. Smoke Test Specification

- [x] 7.1 Confirm smoke test mission is defined (environment correctness, not agent performance)
- [x] 7.2 Confirm ST-01: reset returns valid observation (shape, range check)
- [x] 7.3 Confirm ST-02: random discrete action accepted (no ValueError)
- [x] 7.4 Confirm ST-03: step returns valid next observation
- [x] 7.5 Confirm ST-04: reward is finite (no NaN, Inf)
- [x] 7.6 Confirm ST-05: terminated / truncated defined correctly
- [x] 7.7 Confirm ST-06: info contains all required fields
- [x] 7.8 Confirm ST-07: no crash for fixed number of steps
- [x] 7.9 Confirm ST-08: log format compatible with Change 02 metrics
- [x] 7.10 Confirm ST-09: observation feature order documented
- [x] 7.11 Confirm ST-10: action applied recorded in info dict
- [x] 7.12 Confirm smoke test non-goals are listed (no performance expectation, no DQN training)
- [x] 7.13 Confirm smoke test PASS is a mandatory gate before DQN training (in Change 04 dependency)

---

## 8. Downstream Dependency Specification

- [x] 8.1 Confirm Change 04 must use the observation spec from this change (shape [5], fixed field order)
- [x] 8.2 Confirm Change 04 must use the action spec from this change (Discrete(3))
- [x] 8.3 Confirm Change 04 must use the reward concept from this change (multi-objective)
- [x] 8.4 Confirm Change 04 must pass smoke test before training
- [x] 8.5 Confirm Change 04 must NOT change to continuous action without a new OpenSpec change
- [x] 8.6 Confirm Change 04 must NOT introduce PPO as MVP
- [x] 8.7 Confirm Change 04 evaluation must compare DQN with Change 02 baseline (same scenario, same metrics)

---

## 9. Risk Register

- [x] 9.1 Confirm env-risk-register.md covers R-03-01 (observation not accessible from ns-3)
- [x] 9.2 Confirm R-03-02 (RTT trace difficult to obtain)
- [x] 9.3 Confirm R-03-03 (queue occupancy not available in MVP)
- [x] 9.4 Confirm R-03-04 (action effect hard to map to sender-side control)
- [x] 9.5 Confirm R-03-05 (reward scale instability)
- [x] 9.6 Confirm R-03-06 (throughput-only reward inducing wrong strategy)
- [x] 9.7 Confirm R-03-07 (step interval inconsistency affecting baseline comparison)
- [x] 9.8 Confirm R-03-08 (random agent smoke test cannot pass)
- [x] 9.9 Confirm R-03-09 (Antigravity jumps to DQN training without smoke test)
- [x] 9.10 Confirm R-03-10 (PPO introduced prematurely)
- [x] 9.11 Confirm R-03-11 (env spec over-constrains implementation)
- [x] 9.12 Confirm R-03-12 (info dict missing baseline-compatible metrics)
- [x] 9.13 Confirm R-03-13 (Antigravity uses fake OpenSpec instead of official CLI)

---

## 10. Anti-Implementation Review

- [x] 10.1 Review that no C++ code is included in this change
- [x] 10.2 Review that no Python code is included (pseudo-code in smoke-test.md is conceptual only)
- [x] 10.3 Review that no shell script for ns-3 / ns3-gym execution is included
- [x] 10.4 Review that no DQN training logic is included
- [x] 10.5 Review that PPO is not introduced as MVP in any artifact
- [x] 10.6 Review that IPFS / QUIC / multi-agent / multi-path are not introduced
- [x] 10.7 Review that no ns-3 simulation has been executed
- [x] 10.8 Review that no experiment results are claimed

---

## 11. Final Review

- [x] 11.1 Run `openspec status --change "opengym-env" --json` and confirm `isComplete: true` ✅ **confirmed** — `isComplete: true`, 4/4 artifacts `done`, 8 spec files recognized
- [x] 11.2 Run `openspec validate "opengym-env" --type change --strict --json` and confirm `valid: true, issues: []` ✅ **confirmed** — `valid: true, issues: [], passed: 1, failed: 0`
- [x] 11.3 Submit Change 03 to Spec Owner for review ✅ **submitted** — commit ce914a768d0766ca7d62e18343b5d4f5636182fe
- [x] 11.4 Spec Owner approval granted → approved to proceed to Change 04 proposal ✅ **approved** (Spec Owner, 2026-06-08) — proposal.md / design.md / tasks.md / specs all accepted
- [ ] 11.5 /opsx:apply for Change 03 — **Spec Owner approval for Change 03 specification is granted, but /opsx:apply is deferred until Phase 3: Baseline First. Do not apply until Phase 3 explicitly approved.**
