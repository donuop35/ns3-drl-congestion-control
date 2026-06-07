## 1. OpenSpec Official Setup

- [x] 1.1 Confirm official OpenSpec installation: `npm list -g @fission-ai/openspec --depth=0`
- [x] 1.2 Confirm OpenSpec CLI version: `openspec --version` = 1.4.1
- [x] 1.3 Confirm Node.js version: `node -v` = v20.11.1 (WARN: < 20.19.0, functional)
- [x] 1.4 Confirm OpenSpec initialization: `openspec update --force` completed
- [x] 1.5 Confirm `.agent/skills/openspec-*/SKILL.md` exists (5 files)
- [x] 1.6 Confirm `.agent/workflows/opsx-*.md` exists (5 files)
- [x] 1.7 Confirm change-01 artifact path: `openspec/changes/project-charter/`
- [x] 1.8 Confirm `openspec status --change "project-charter"` shows `4/4 artifacts complete`

## 2. Project Identity Confirmation

- [x] 2.1 Confirm project title (Chinese): 以深度強化學習進行單一瓶頸鏈路壅塞控制與吞吐量最佳化
- [x] 2.2 Confirm project title (English): Deep Reinforcement Learning for Congestion Control and Throughput Optimization over a Single Bottleneck Link
- [x] 2.3 Confirm GitHub / README title: DRL-Based Congestion Control over a Bottleneck Link
- [x] 2.4 Confirm thesis statement is documented in spec.md
- [x] 2.5 Confirm project mission is documented in spec.md

## 3. Research Foundation Confirmation

- [x] 3.1 Confirm project background (TCP congestion control history and DRL motivation) is in spec.md
- [x] 3.2 Confirm problem statement (why hand-crafted TCP rules have limitations) is in proposal.md
- [x] 3.3 Confirm proposed direction (DRL + single bottleneck + ns-3/ns3-gym) is documented
- [x] 3.4 Confirm MDP initial definition (state / action / reward / episode) is in spec.md
- [x] 3.5 Confirm MDP definition includes Discrete(3) action space rationale
- [x] 3.6 Confirm reward function includes throughput reward AND delay/loss penalty (not throughput-only)

## 4. Scope Boundary Confirmation

- [x] 4.1 Confirm In Scope items are documented in scope.md
- [x] 4.2 Confirm Out of Scope items are documented in scope.md
- [x] 4.3 Confirm Strict Non-Goals are documented in scope.md (hard prohibitions)
- [x] 4.4 Confirm Expansion Rules are documented in scope.md
- [x] 4.5 Confirm IPFS is explicitly listed as out of scope
- [x] 4.6 Confirm QUIC is explicitly listed as out of scope
- [x] 4.7 Confirm Linux kernel modification is explicitly listed as out of scope
- [x] 4.8 Confirm multi-agent RL is explicitly listed as out of scope
- [x] 4.9 Confirm multi-path routing is explicitly listed as out of scope

## 5. Baseline and Metrics Confirmation

- [x] 5.1 Confirm baseline list: NewReno (required), CUBIC (required), BBR (strongly preferred)
- [x] 5.2 Confirm BBR is NOT a blocking dependency
- [x] 5.3 Confirm metric list: throughput, RTT, packet loss rate, utility score, reward curve, convergence behavior
- [x] 5.4 Confirm utility score formula is defined (composite: throughput - delay - loss)
- [x] 5.5 Confirm experiment scenarios: Scenario A (low-latency), Scenario B (high-latency), Scenario C (optional)
- [x] 5.6 Confirm all experiments use fixed random seeds

## 6. MVP Definition Confirmation

- [x] 6.1 Confirm MVP algorithm: Stable-Baselines3 DQN (discrete action)
- [x] 6.2 Confirm PPO is future extension ONLY, not MVP
- [x] 6.3 Confirm DQN action space: Discrete(3) = {decrease, keep, increase}
- [x] 6.4 Confirm success definition does NOT require DRL to outperform all baselines
- [x] 6.5 Confirm honest reporting is required even if DQN underperforms

## 7. Downstream Change Map Confirmation

- [x] 7.1 Confirm change-02 depends on: baseline selection, metrics, topology, scenario configs
- [x] 7.2 Confirm change-03 depends on: MDP definition, RL interface, observation space
- [x] 7.3 Confirm change-04 depends on: MVP algorithm, evaluation philosophy, success definition
- [x] 7.4 Confirm change-05 depends on: all previous changes complete
- [x] 7.5 Confirm each change requires spec owner approval before next begins

## 8. Risk Register Confirmation

- [x] 8.1 Confirm R-01 (ns3-gym install failure) is documented with fallback
- [x] 8.2 Confirm R-02 (ns-3 logging incomplete) is documented with fallback
- [x] 8.3 Confirm R-03 (BBR version dependency) is documented with fallback
- [x] 8.4 Confirm R-04 (DQN non-convergence) is documented with fallback
- [x] 8.5 Confirm R-05 (reward design causes high throughput + high RTT) is documented
- [x] 8.6 Confirm R-06 (Antigravity self-scope-expansion) is documented
- [x] 8.7 Confirm R-07 (project misunderstood as IPFS) is documented
- [x] 8.8 Confirm R-08 (DRL underperforms baseline) is documented with honest reporting requirement
- [x] 8.9 Confirm R-09 (insufficient experiment figures) is documented
- [x] 8.10 Confirm R-10 (OpenSpec docs vs implementation mismatch) is documented
- [x] 8.11 Confirm R-11 (fake OpenSpec) is documented with strict handling procedure
- [x] 8.12 Confirm R-12 (claiming OpenSpec completion without CLI) is documented with strict handling

## 9. Document Review

- [x] 9.1 Review proposal.md: Why / What Changes / What Does Not Change / Impact / Dependencies / Acceptance Criteria
- [x] 9.2 Review design.md: Scope Boundary / Technical Direction / Governance Rules / DR-01 through DR-10
- [x] 9.3 Review specs/project-charter/spec.md: Mission / Title / Background / MDP / Success Definition / Governance Role
- [x] 9.4 Review specs/project-charter/scope.md: In Scope / Out of Scope / Strict Non-Goals / Expansion Rules
- [x] 9.5 Review specs/project-charter/risk-register.md: R-01 through R-12 with trigger conditions

## 10. Scope Compliance Check

- [x] 10.1 Confirm: no code written in this change
- [x] 10.2 Confirm: no ns-3 experiment created in this change
- [x] 10.3 Confirm: no ns3-gym environment created in this change
- [x] 10.4 Confirm: no DQN / PPO training started in this change
- [x] 10.5 Confirm: no IPFS / QUIC / multi-agent / multi-path expansion in this change
- [x] 10.6 Confirm: no experiment results claimed in this change

## 11. Spec Owner Review

- [x] 11.1 Submit change-01 artifacts for spec owner review
- [x] 11.2 Spec owner confirms: project title is correct and frozen ✅
- [x] 11.3 Spec owner confirms: scope boundary is acceptable ✅
- [x] 11.4 Spec owner confirms: MDP initial definition is acceptable ✅ (cwnd as cwnd-like abstraction; fallback rule added)
- [x] 11.5 Spec owner confirms: baseline selection is acceptable ✅ (NewReno+CUBIC required, BBR non-blocking)
- [x] 11.6 Spec owner confirms: risk register is adequate ✅ (R-01 ~ R-12 accepted)
- [x] 11.7 Spec owner signs off: "Direction confirmed, approved to start change-02" ✅ **2026-06-08**
- [ ] 11.8 (After Change 05 complete) Archive change-01 with `openspec archive change "project-charter"`

## 12. Post-Approval Revisions (Spec Owner Requested)

- [x] 12.1 Add Node.js v20.11.1 < 20.19.0 risk note to README and design.md
- [x] 12.2 Fix topology non-goal wording in design.md and scope.md (remove "> 2 nodes" phrasing; clarify ns-3 router-based bottleneck is allowed; prohibit multi-bottleneck/multi-path/multi-sender-receiver)
- [x] 12.3 Add cwnd fallback rule in spec.md, scope.md (cwnd_signal_norm OR sending_rate_signal_norm; fallback procedure defined)
- [x] 12.4 Remove YouTube embed from README (non-official video; replaced with TODO placeholder)
- [x] 12.5 Confirm proposal/ directory exists (3 files: PDF, PPTX, video-link.md) — already existed from previous work ✅
- [ ] 12.6 Spec owner final confirmation of revisions before entering Change 02 implementation

