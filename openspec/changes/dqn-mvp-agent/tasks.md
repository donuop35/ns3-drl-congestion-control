# Tasks: Change 04 DQN MVP Agent Specification

> ⚠️ 本 change 的所有 tasks 均為**規格任務**，不含 DQN training、ns-3 coding、benchmark execution 等 implementation 任務。
> 不得在 Spec Owner 驗收前執行 /opsx:apply 或進入任何 implementation。

---

## 0. Official OpenSpec Verification

- [x] 0.1 Confirm `@fission-ai/openspec@1.4.1` is installed (`openspec --version` → 1.4.1)
- [x] 0.2 Confirm repo is initialized with official OpenSpec (`openspec list --json` works)
- [x] 0.3 Confirm Change 04 is created under official OpenSpec (`openspec new change "dqn-mvp-agent"`)
- [x] 0.4 Confirm this is real OpenSpec, NOT `openspec-preview/`（all artifacts are under `openspec/changes/dqn-mvp-agent/`）
- [x] 0.5 Confirm no fake OpenSpec workflow was used

---

## 1. Specification Dependency Check

- [x] 1.1 Confirm dependency on Change 01 project-charter (✅ approved; title / scope / toolchain frozen)
- [x] 1.2 Confirm dependency on Change 02 ns3-baseline-benchmark (✅ approved; ns-3.40 frozen, metrics frozen)
- [x] 1.3 Confirm dependency on Change 03 opengym-env (✅ approved; MDP / observation / action / reward / smoke test frozen)
- [x] 1.4 Confirm no implementation is included in this change
- [x] 1.5 Confirm Phase 3 baseline must complete before Phase 4 DQN training

---

## 2. DQN MVP Boundary Specification

- [x] 2.1 Confirm DQN MVP uses Stable-Baselines3 DQN (in `specs/dqn-mvp-agent.md`)
- [x] 2.2 Confirm MlpPolicy is the default policy candidate
- [x] 2.3 Confirm observation inherits Change 03: shape [5], fixed field order
- [x] 2.4 Confirm action inherits Change 03: Discrete(3) {0: decrease, 1: keep, 2: increase}
- [x] 2.5 Confirm reward inherits Change 03 base concept: r = α·t_norm − β·d_norm − λ·l_norm
- [x] 2.6 Confirm initial reward weights are defined (α=1.0, β=0.1, λ=10.0, provisional)
- [x] 2.7 Confirm discount factor γ = 0.99 (consistent with Change 03)
- [x] 2.8 Confirm initial DQN hyperparameter starting points are documented in `design.md`
- [x] 2.9 Confirm PPO is explicitly excluded from Change 04 MVP
- [x] 2.10 Confirm continuous action is future extension only
- [x] 2.11 Confirm IPFS / QUIC / multi-agent / multi-path are not in scope

---

## 3. Training Protocol Specification

- [x] 3.1 Confirm smoke test gate is mandatory before training (in `specs/training-protocol.md`)
- [x] 3.2 Confirm baseline availability gate is required before training
- [x] 3.3 Confirm training_config.yaml must be completed before training starts
- [x] 3.4 Confirm training_log.csv schema (timestep, episode, reward, length, exploration_rate)
- [x] 3.5 Confirm episode_rewards.csv schema (per-episode summary with raw metrics from info dict)
- [x] 3.6 Confirm model checkpoint concept (SB3 .zip, fixed interval, evaluation input only)
- [x] 3.7 Confirm checkpoint ≠ success criterion
- [x] 3.8 Confirm reproducibility metadata requirements (seed + config + versions + timestamps)
- [x] 3.9 Confirm training non-goals (no hyperparameter tuning study, no ablation, no PPO)

---

## 4. Evaluation Protocol Specification

- [x] 4.1 Confirm separate evaluation principle: training reward ≠ success criterion (in `specs/evaluation-protocol.md`)
- [x] 4.2 Confirm evaluation uses deterministic policy (ε = 0 or exploration disabled)
- [x] 4.3 Confirm evaluation metrics: raw_throughput_mbps / raw_delay_ms / raw_loss_rate / utility_score / episode_reward
- [x] 4.4 Confirm S1 is MVP-required evaluation scenario
- [x] 4.5 Confirm S2 is MVP-required evaluation scenario
- [x] 4.6 Confirm evaluation output artifacts: per-episode CSV + evaluation_summary.csv
- [x] 4.7 Confirm evaluation_summary.csv schema (algorithm, scenario, 4 metrics, seed, run_id)
- [x] 4.8 Confirm evaluation interpretation rules (5 rules in spec)

---

## 5. Baseline Comparison Protocol Specification

- [x] 5.1 Confirm DQN vs NewReno is required comparison (in `specs/baseline-comparison.md`)
- [x] 5.2 Confirm DQN vs CUBIC is required comparison
- [x] 5.3 Confirm DQN vs BBR is strongly recommended but non-blocking
- [x] 5.4 Confirm metric alignment with Change 02 (same unit: Mbps / ms / fraction / dimensionless)
- [x] 5.5 Confirm comparison must be within same scenario (no cross-scenario mixing)
- [x] 5.6 Confirm DQN underperformance interpretation rules (5 rules in spec)
- [x] 5.7 Confirm "what to do if DQN loses" is documented (honest reporting + limitation analysis)

---

## 6. Output Artifact Specification

- [x] 6.1 Confirm required logs directory structure (in `specs/output-artifacts.md`)
- [x] 6.2 Confirm training_config.yaml is required
- [x] 6.3 Confirm training_log.csv is required
- [x] 6.4 Confirm episode_rewards.csv is required
- [x] 6.5 Confirm dqn_checkpoint.zip is required
- [x] 6.6 Confirm evaluation_summary.csv is required
- [x] 6.7 Confirm dqn_training_reward_<scenario>.png is required (S1 + S2)
- [x] 6.8 Confirm 4 grouped bar comparison figures are required (throughput / delay / loss / utility)
- [x] 6.9 Confirm all figures must be ≥ 150 DPI with labeled axes and legend
- [x] 6.10 Confirm artifact naming convention (scenario_a / scenario_b / seed<N> / run_<id>)
- [x] 6.11 Confirm README DQN results section requirements
- [x] 6.12 Confirm PPT required slides list
- [x] 6.13 Confirm 10-minute video content structure

---

## 7. Reproducibility Metadata Specification

- [x] 7.1 Confirm all random seeds must be fixed and recorded (Python / NumPy / PyTorch / SB3 / ns-3)
- [x] 7.2 Confirm ns-3.40 version freeze is inherited (Change 02)
- [x] 7.3 Confirm SB3 version must be recorded
- [x] 7.4 Confirm reproducibility criterion: metric-equivalent (not bit-for-bit; inherits Change 02 philosophy)

---

## 8. Success / Failure Criteria Specification

- [x] 8.1 Confirm full success criteria are defined (in `specs/success-failure-criteria.md`)
- [x] 8.2 Confirm partial success criteria are defined
- [x] 8.3 Confirm "failure but reportable" criteria are defined
- [x] 8.4 Confirm stop rules are defined (6 stop conditions in table)
- [x] 8.5 Confirm fallback rules are defined (6 fallback scenarios)
- [x] 8.6 Confirm evaluation result reporting rules (5 rules in spec)
- [x] 8.7 Confirm success criteria summary table is present (4 levels × 5 dimensions)

---

## 9. Extension Rules Specification

- [x] 9.1 Confirm 5 MVP protection rules are stated (in `specs/extension-rules.md`)
- [x] 9.2 Confirm reward ablation rules (Change 05 with Spec Owner approval)
- [x] 9.3 Confirm observation ablation rules (separate OpenSpec change required)
- [x] 9.4 Confirm algorithm extension table (Double DQN within scope; PPO / SAC / TD3 future extension)
- [x] 9.5 Confirm PPO governance rules (introduction process defined)
- [x] 9.6 Confirm continuous action extension rules
- [x] 9.7 Confirm extension priority order is documented
- [x] 9.8 Confirm IPFS / QUIC / multi-agent / multi-path are NOT extensions but out-of-scope

---

## 10. Risk Register

- [x] 10.1 Confirm R-04-01: smoke test not passed (ENV)
- [x] 10.2 Confirm R-04-02: DQN reward non-finite (TRN)
- [x] 10.3 Confirm R-04-03: DQN reward diverges (TRN)
- [x] 10.4 Confirm R-04-04: DQN not converging (TRN)
- [x] 10.5 Confirm R-04-05: DQN learns conservative policy (TRN)
- [x] 10.6 Confirm R-04-06: DQN chases throughput only, RTT/loss increases (TRN)
- [x] 10.7 Confirm R-04-07: training reward up but evaluation metrics down (EVL)
- [x] 10.8 Confirm R-04-08: DQN loses to CUBIC / BBR on all metrics (EVL)
- [x] 10.9 Confirm R-04-09: BBR unavailable in ns-3.40 (ENV)
- [x] 10.10 Confirm R-04-10: S3/S4 scenarios too hard (SCP)
- [x] 10.11 Confirm R-04-11: artifact logging incomplete (ART)
- [x] 10.12 Confirm R-04-12: PPO or continuous action prematurely introduced (SCP)
- [x] 10.13 Confirm R-04-13: action space changed without new change (SCP)
- [x] 10.14 Confirm R-04-14: final PPT cannot explain results (ART)
- [x] 10.15 Confirm R-04-15: DQN config / seed / metadata missing (OPS)
- [x] 10.16 Confirm R-04-16: official OpenSpec not initialized / openspec-preview used (OPS)

---

## 11. Anti-Implementation Review

- [x] 11.1 Review that no DQN training script is included in this change
- [x] 11.2 Review that no Python implementation code is included
- [x] 11.3 Review that no C++ ns-3 code is included
- [x] 11.4 Review that no shell command implementation script is included
- [x] 11.5 Review that no ns-3 simulation has been executed
- [x] 11.6 Review that no ns3-gym has been launched
- [x] 11.7 Review that no benchmark has been run
- [x] 11.8 Review that no DQN training has been performed
- [x] 11.9 Review that no reward curve or experiment result has been generated
- [x] 11.10 Review that PPO is not introduced as MVP in any artifact
- [x] 11.11 Review that IPFS / QUIC / multi-agent / multi-path are not introduced
- [x] 11.12 Review that `openspec-preview/` is not used as formal spec source

---

## 12. Scope Correction Notes Review

- [x] 12.1 Confirm Final Specification Closure Note #1: Official OpenSpec Requirement (in proposal.md)
- [x] 12.2 Confirm Note #2: openspec-preview Demotion
- [x] 12.3 Confirm Note #3: Baseline Before DRL
- [x] 12.4 Confirm Note #4: DQN MVP Protection
- [x] 12.5 Confirm Note #5: Evaluation Over Reward Curve
- [x] 12.6 Confirm Note #6: Reportable Failure Rule
- [x] 12.7 Confirm Note #7: No Scope Expansion

---

## 13. Final Review

- [ ] 13.1 Run `openspec status --change "dqn-mvp-agent" --json` and confirm `isComplete: true`
- [ ] 13.2 Run `openspec validate "dqn-mvp-agent" --type change --strict --json` and confirm `valid: true, issues: []`
- [x] 13.3 Submit Change 04 to Spec Owner for review ✅ **submitted** — commit 2411e57
- [x] 13.4 Spec Owner approval granted → approved to proceed to Phase 3: Baseline First ✅ **approved** (Spec Owner, 2026-06-08) — all artifacts accepted; Phase 3 authorized
- [ ] 13.5 /opsx:apply for Change 04 — **Spec Owner approval for Change 04 specification is granted, but /opsx:apply is deferred. ALL changes (/opsx:apply for Change 02, 03, 04) are deferred until Spec Owner explicitly approves per-change. Phase 3 baseline execution is now underway.**

---

## 14. Implementation Status (Phase 4 Execution)

> This section records **implementation execution status**, NOT specification tasks.
> Specification tasks are in sections 0-13. Updated: 2026-06-09 (Excellent Acceptance upgrade).

### 14.A Environment Setup
- [x] ns3-gym installed (tkn-tub/ns3-gym, commit cfff7f3)
- [x] ns3-gym patched for Gymnasium 1.0.0 + NumPy 1.24+ + Protobuf 5.x
- [x] C++ OpenGym env built (ns3.40-congestion-env-optimized)
- [x] Python wrapper ns3_congestion_env.py (Gymnasium + ZMQ + subprocess)
- [x] allow_dummy=False enforcement: dummy fallback raises RuntimeError by default

### 14.B Smoke Test
- [x] S1 smoke test PASS -- real ZMQ, obs=[0.478, 0.134, 0.0, 0.5, 0.5], reward=0.40-0.61
- [x] S2 smoke test PASS -- real ZMQ, obs=[0.202, 0.198, 0.0, 0.5, 0.5], reward=0.30-0.56
- [x] Hardened: throughput-nonzero check (>= 0.1 Mbps in >= 30% steps required)
- [x] Hardened: zmq_mode=real assertion; --allow-dummy flag for debug-only

### 14.C DQN Training
- [x] S1 DQN COMPLETE -- 30k steps, seed=42, ep_rew_mean: 62.9->84.4 (+34%), ~18 min CPU
- [x] S1 checkpoints saved: 6k/12k/18k/24k/30k steps + final model
- [x] S1 training metadata YAML + Monitor log + ~300 episode CSVs
- [ ] S2 DQN PENDING -- smoke test gate PASSED; training not yet executed

### 14.D DQN Evaluation
- [x] S1 eval COMPLETE -- 5 eps, deterministic, seed=42-46
- [x] S1: Throughput=9.877 Mbps, Delay=115.3 ms (proxy), Loss=0.0040, Utility=0.900
- [x] S1: Action distribution 100% action 2 (increase) -- near-capacity S1 behavior
- [x] S1 eval CSV + summary row in dqn_summary.csv
- [ ] S2 eval PENDING -- depends on S2 training

### 14.E Comparison vs Baseline (S1)
- [x] DQN vs NewReno S1: DQN utility 0.900 > NewReno 0.875
- [x] DQN vs CUBIC S1: DQN utility 0.900 > CUBIC 0.884
- [x] DQN vs BBR S1: DQN utility 0.900 < BBR 0.947 (honest result, not hidden)
- [x] S1 comparison row in dqn_vs_baseline_summary.csv
- [ ] S2 comparison -- pending S2 training/eval

### 14.F Figures
- [x] S1 reward curve: figures/drl/dqn_reward_curve_s1.png
- [x] S1 action distribution: figures/drl/dqn_action_distribution_s1.png
- [x] S1 comparison figures (x4): figures/comparison/dqn_vs_baseline_*_s1.png
- [ ] S2 reward curve / action distribution / comparison figures -- pending
- [ ] Robustness/seed sensitivity figure -- pending

### 14.G Reports
- [x] smoke-test-report.md (hardened, ZMQ metadata added)
- [x] phase4-drl-report.md
- [x] excellent-acceptance-audit.md
- [ ] artifact-index.md -- pending
- [ ] phase4-excellent-acceptance-report.md -- pending

### 14.H Scope Enforcement
- [x] No PPO, no IPFS/QUIC/multi-agent/multi-path, no fake data
- [x] DQN vs BBR honestly documented (DQN ranks 2nd on utility)
- [x] delay proxy clearly disclosed (not true RTT)
- [x] /opsx:apply deferred until Spec Owner explicit approval per-change

### 14.I Non-Blocking Future Work (Phase 5 / Change 05)
- [ ] S2 DQN training/eval (in progress via this upgrade)
- [ ] Repeated-seed robustness study (full multi-training version)
- [ ] Reward weight ablation (requires Change 05 Spec Owner approval)
- [ ] Demo video + PPT package (Change 05)
