# Specification: Demo Script

**Target Location:** `demo/demo-script.md` and `demo/demo-checklist.md`

## ADDED Requirements

### Req 1: Create Demo Script
The final demo video is constrained to a 10-minute presentation.

#### Scenario: Recording the demo
Given the 10-minute constraint
When the presenter executes the demo
Then the script must allocate time efficiently across the 10 sections.

## 1. Demo Flow and Structure

1. **Project Overview (1 min):** Briefly introduce the single bottleneck congestion control problem and the DRL objective.
2. **OpenSpec SDD Workflow Proof (1 min):** Show the `.agent/` directories and the `openspec status` output to prove specification-driven development.
3. **Phase 3 Baseline Artifacts (1 min):** Briefly show the generated baseline CSVs to establish the foundation.
4. **Phase 4 ns3-gym + DQN Artifacts (1 min):** Highlight the Python Gym wrapper and the SB3 DQN implementation.
5. **Smoke Test Result (1 min):** Show the real-ZMQ smoke test command and report, emphasizing the `allow_dummy=False` enforcement.
6. **DQN Training/Evaluation Result (1 min):** Briefly show the training logs, the 30k step models, and run a short evaluation command.
7. **DQN vs Baseline Comparison (2 mins):** Present the final generated figures (Utility and Loss). Honestly state the S1 2nd-place ranking and the S2 3rd-place ranking.
8. **Honest Limitations (1 min):** Explicitly discuss the Fallback Option B abstraction, the delay proxy, and the S1 degenerate policy.
9. **How to Reproduce (0.5 min):** Point to the README instructions for reviewers.
10. **Closing Statement (0.5 min):** Final summary of the MVP's feasibility.

## 2. Demo Constraints & No-Go Statements

To maintain academic integrity and adhere to project boundaries, the demo:
- **Must NOT** pretend to train the 30k-step model live (show the pre-trained artifacts).
- **Must NOT** claim DQN universally outperforms all baselines.
- **Must NOT** hide the DQN S2 high loss rate (5.54%).
- **Must NOT** hide Fallback Option B (must clarify it's sender-side rate control, not kernel `cwnd` modification).
- **Must NOT** refer to the delay proxy as "true RTT".

## 3. Demo Commands

The script should include verifiable commands that reviewers can execute:
- `openspec status`
- `bash scripts/phase4/run_smoke_test.sh` (to demonstrate real-ZMQ connectivity)
- `python3 src/agents/eval_dqn.py --scenario S1 --model experiments/drl/models/dqn_s1_seed42.zip --episodes 1` (quick eval proof)
- Python figure regeneration scripts.
