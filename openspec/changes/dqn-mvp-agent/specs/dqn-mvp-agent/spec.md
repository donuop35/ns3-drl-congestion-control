## ADDED Requirements

### Requirement: dqn-agent DQN MVP Agent Boundary

The system SHALL define a DQN MVP agent using Stable-Baselines3 DQN where:
- Algorithm SHALL be SB3 DQN with MlpPolicy as default candidate
- Observation SHALL inherit Change 03 minimal observation: shape [5] with fixed field order
- Action SHALL inherit Change 03 Discrete(3): {0: decrease, 1: keep, 2: increase}
- Reward SHALL inherit Change 03 base reward: r = α·t_norm − β·d_norm − λ·loss_norm with initial weights α=1.0, β=0.1, λ=10.0 (provisional)
- Gamma SHALL be 0.99 (consistent with Change 03)
- PPO MUST NOT be introduced in Change 04 MVP
- Continuous action space MUST NOT be introduced without a new OpenSpec change
- IPFS / QUIC / multi-agent / multi-path MUST NOT be introduced

#### Scenario: DQN agent uses correct interface from Change 03

- **WHEN** Phase 4 implements DQN agent
- **THEN** observation input SHALL have shape [5] (or [4] if prev_action_norm excluded per Change 03 OQ-03.03)
- **THEN** action output SHALL be in {0, 1, 2} only
- **THEN** reward SHALL include throughput, delay, and loss components

#### Scenario: PPO and continuous action are blocked

- **WHEN** any implementation attempt introduces PPO or continuous action in Change 04
- **THEN** it SHALL be blocked and reported to Spec Owner immediately
- **THEN** a separate OpenSpec change SHALL be required before any algorithm change

---

### Requirement: training-gate Training Gate Before DQN Training

The system SHALL enforce a training gate where:
- Change 03 smoke test (ST-01 through ST-10) MUST all pass before DQN training begins
- Phase 3 baseline benchmark results (NewReno + CUBIC on S1 + S2) MUST be available
- training_config.yaml MUST be fully completed before training starts
- ns-3.40 MUST be verified as the simulator version
- Stable-Baselines3 MUST be installed and version recorded

#### Scenario: Training gate enforced

- **WHEN** DQN training is about to begin
- **THEN** all ST-01 through ST-10 smoke test criteria SHALL have been verified and passed
- **THEN** at least NewReno and CUBIC baseline CSV files SHALL exist for S1 and S2

#### Scenario: Training logging required

- **WHEN** DQN training runs
- **THEN** training_log.csv SHALL be written with at least: timestep, episode, episode_reward, episode_length, exploration_rate
- **THEN** training_config.yaml SHALL record all hyperparameters, reward weights, seed, and version information
- **THEN** dqn_checkpoint.zip SHALL be saved at fixed intervals and at training completion

---

### Requirement: evaluation-protocol Separate Evaluation Protocol

The system SHALL define a separate evaluation pass where:
- Training reward curve SHALL NOT be used as the sole success criterion
- Evaluation SHALL use deterministic policy (ε = 0) from trained checkpoint
- Evaluation metrics SHALL be extracted from info dict: raw_throughput_mbps, raw_delay_ms, raw_loss_rate, utility_score
- Evaluation SHALL cover both S1 (MVP-Required) and S2 (MVP-Required)
- Evaluation metrics SHALL use same units and calculation as Change 02 baseline CSV

#### Scenario: Evaluation uses raw metrics not training reward

- **WHEN** DQN evaluation phase runs
- **THEN** performance claims SHALL be based on raw_throughput_mbps, raw_delay_ms, raw_loss_rate from info dict
- **THEN** training episode_reward SHALL NOT be used as the primary performance metric in final report

#### Scenario: Evaluation covers both MVP scenarios

- **WHEN** evaluation phase completes
- **THEN** evaluation results SHALL include both S1 and S2
- **THEN** evaluation_summary.csv SHALL contain DQN metrics for both scenarios

---

### Requirement: baseline-comparison Baseline Comparison Protocol

The system SHALL define baseline comparison where:
- DQN vs NewReno on S1 and S2 SHALL be required
- DQN vs CUBIC on S1 and S2 SHALL be required
- DQN vs BBR SHALL be strongly recommended but non-blocking (inherits Change 02 BBR rule)
- Comparison SHALL use same metric unit as Change 02 baseline CSV
- DQN underperformance SHALL be reported honestly, not hidden

#### Scenario: Required comparison completed

- **WHEN** evaluation summary is produced
- **THEN** evaluation_summary.csv SHALL contain rows for DQN, NewReno, and CUBIC for both S1 and S2
- **THEN** all 4 metrics SHALL be present for each row

#### Scenario: DQN underperformance handled

- **WHEN** DQN performs worse than both NewReno and CUBIC on all metrics
- **THEN** results SHALL still be recorded and published in comparison table
- **THEN** failure SHALL be classified as "Failure but reportable" per success-failure-criteria.md
- **THEN** analysis of possible causes SHALL be included in final report

---

### Requirement: success-failure Success and Failure Criteria

The system SHALL define clear success and failure criteria where:
- Full success: DQN converges + throughput ≥ at least one baseline + delay/loss acceptable in both S1/S2
- Partial success: DQN converges in ≥ 1 scenario or improves ≥ 1 metric vs ≥ 1 baseline
- Failure but reportable: DQN converges to suboptimal policy but underperforms all baselines
- Stop condition: DQN reward is non-finite (NaN/Inf) or smoke test fails → immediate stop and report

#### Scenario: Stop condition triggered

- **WHEN** DQN training produces non-finite reward (NaN, Inf, -Inf) at any step
- **THEN** training SHALL stop immediately
- **THEN** Spec Owner SHALL be notified before any restart
- **THEN** reward computation and normalization SHALL be investigated

#### Scenario: Failure but reportable

- **WHEN** DQN converges but all evaluation metrics are worse than both NewReno and CUBIC
- **THEN** results SHALL be published honestly in all artifacts
- **THEN** limitation analysis SHALL be included in final report
- **THEN** the project SHALL NOT be considered automatically failed

---

### Requirement: output-artifacts Output Artifact Requirements

The system SHALL produce the following required artifacts:
- training_config.yaml: all hyperparameters, reward weights, seed, versions
- training_log.csv: per-step or per-episode training data
- episode_rewards.csv: per-episode summary with raw metrics
- dqn_checkpoint.zip: SB3 native model checkpoint
- evaluation_summary.csv: aggregated comparison table (DQN + baselines)
- dqn_training_reward_<scenario>.png: training reward curves (S1 + S2) at ≥ 150 DPI
- dqn_vs_baseline_<metric>.png: 4 grouped bar comparison figures (throughput/delay/loss/utility)

#### Scenario: All required artifacts present

- **WHEN** Phase 4 DQN implementation completes
- **THEN** all 7 required artifact types SHALL be present in correct directories
- **THEN** all figures SHALL be at ≥ 150 DPI with labeled axes and legend

#### Scenario: Artifact naming compliance

- **WHEN** DQN evaluation CSV files are generated
- **THEN** filenames SHALL follow pattern: <scenario>_DQN_seed<seed>_run<id>.csv
- **THEN** scenario names SHALL be consistent: "scenario_a" for S1, "scenario_b" for S2
