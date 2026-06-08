## ADDED Requirements

### Requirement: mdp-interface MDP Interface Definition

The system SHALL define a formal MDP interface for the DRL congestion control environment where:
- The MDP is specified as M = (S, A, P, R, γ) with each component formally documented
- The environment represents a single bottleneck ns-3.40 simulation abstracted as a RL environment
- The agent controls only sender-side transmission behavior abstraction
- The agent SHALL NOT directly modify kernel-level TCP parameters
- Network dynamics (queuing, delay, congestion) SHALL be determined by ns-3.40 simulation
- Transition dynamics P(s_{t+1}|s_t, a_t) SHALL be implicitly defined by ns-3.40 simulation
- The discount factor γ SHOULD be initialized to 0.99 (Change 04 may adjust with Spec Owner approval)

#### Scenario: MDP components are defined

- **WHEN** Change 03 specification artifacts are reviewed
- **THEN** M = (S, A, P, R, γ) SHALL have each component formally documented in `specs/mdp-interface.md`
- **THEN** environment boundary SHALL be defined (ns-3 single bottleneck abstraction)
- **THEN** agent boundary SHALL be defined (sender-side only)

#### Scenario: No kernel-level modification

- **WHEN** Change 04 implements the environment
- **THEN** the implementation SHALL NOT call kernel-level TCP modification commands (e.g., sysctl)
- **THEN** all agent control SHALL pass through the ns3-gym abstraction layer

---

### Requirement: observation-space MVP Observation Space

The system SHALL define an MVP observation space where:
- Observation vector has shape [5] with fixed field order
- All fields are numeric and normalizable to [0, 1]
- Observation index 0: `throughput_norm` (goodput / link_bw, bounded [0,1])
- Observation index 1: `delay_norm` (avg_delay_ms / max_expected_delay_ms, bounded [0,1])
- Observation index 2: `loss_norm` (packet loss rate, bounded [0,1])
- Observation index 3: `congestion_indicator` (derived from loss_norm and delay_norm)
- Observation index 4: `prev_action_norm` ({0→0.0, 1→0.5, 2→1.0}, should-have)
- Enhanced observation fields (queue occupancy, delay gradient, etc.) MUST be future extension only

#### Scenario: MVP observation shape and range

- **WHEN** `env.reset()` is called during smoke test
- **THEN** observation SHALL have shape [5] (or [4] if prev_action_norm excluded)
- **THEN** all values SHALL be in [0, 1] range (or clipped to [0, 1])

#### Scenario: RTT fallback

- **WHEN** direct RTT measurement is unavailable from FlowMonitor
- **THEN** the system SHALL use `delaySum / rxPackets` as delay estimate
- **THEN** the fallback method SHALL be documented in `info["delay_estimate_method"]`

---

### Requirement: action-space Discrete Action Space

The system SHALL define a discrete action space where:
- Action space is Discrete(3): A = {0: decrease, 1: keep, 2: increase}
- Action 0 (decrease) reduces sender-side transmission intensity
- Action 1 (keep) maintains current transmission parameter
- Action 2 (increase) raises sender-side transmission intensity
- No negative rate or cwnd-like variable SHALL be permitted
- Each action effect MUST be logged in the info dictionary
- Continuous action space MUST be marked as future extension only
- PPO MUST NOT be introduced in this change or Change 04 MVP

#### Scenario: Discrete action accepted

- **WHEN** random integer action ∈ {0, 1, 2} is passed to `env.step(action)`
- **THEN** the environment SHALL accept the action without raising ValueError
- **THEN** `info["action_applied"]` SHALL equal the action passed in

#### Scenario: Continuous action blocked

- **WHEN** any implementation attempts to introduce continuous action space
- **THEN** it SHALL be blocked and reported to Spec Owner
- **THEN** a separate OpenSpec change SHALL be required for continuous action

---

### Requirement: reward-function Multi-Objective Reward

The system SHALL define a multi-objective reward function where:
- Base reward concept: `r_t = α·throughput_norm_t − β·delay_norm_t − λ·loss_norm_t`
- Loss penalty uses λ (lambda), NOT γ (gamma) to avoid confusion with discount factor
- All components MUST be normalized before weighting
- Weights α, β, λ are provisional in this change; Change 04 SHALL define initial values
- Reward MUST NOT be throughput-only
- Reward SHALL be finite at every step (no NaN, Inf, -Inf)

#### Scenario: Reward is finite

- **WHEN** `env.step(action)` is called during smoke test
- **THEN** returned `reward` SHALL satisfy `math.isfinite(reward) == True`
- **THEN** reward SHALL NOT be NaN, Inf, or -Inf

#### Scenario: Multi-objective reward required

- **WHEN** Change 04 defines initial reward weights
- **THEN** both delay penalty (β > 0) and loss penalty (λ > 0) SHALL be included
- **THEN** throughput-only reward (β = 0, λ = 0) SHALL be documented as a failure mode to avoid

---

### Requirement: episode-step-reset Episode Flow Interface

The system SHALL define a complete episode flow interface where:
- `reset()` returns (observation, info) with observation shape [5] and info containing scenario_id
- `step(action)` returns (observation, reward, terminated, truncated, info)
- `terminated` is True when simulation duration is reached (natural episode end)
- `truncated` is True when time limit is exceeded or fatal error occurs
- `terminated` and `truncated` MUST NOT both be True simultaneously
- info dict MUST include: raw_throughput_mbps, raw_delay_ms, raw_loss_rate, utility_score, scenario_id, step_index, action_applied, action_symbol

#### Scenario: Complete reset/step/done flow

- **WHEN** random agent executes reset() → N steps → terminated
- **THEN** reset() SHALL return valid (observation, info)
- **THEN** each step() SHALL return (observation, reward, terminated, truncated, info)
- **THEN** info SHALL contain all required fields at every step

#### Scenario: Info dict baseline compatibility

- **WHEN** info dict fields are compared to Change 02 baseline CSV schema
- **THEN** raw_throughput_mbps SHALL be in same unit as Change 02 (Mbps)
- **THEN** raw_delay_ms SHALL be in same unit as Change 02 (ms)
- **THEN** raw_loss_rate SHALL be fraction [0, 1] as in Change 02

---

### Requirement: smoke-test Random Agent Smoke Test Criteria

The system SHALL define random agent smoke test criteria where:
- Smoke test verifies environment correctness, NOT agent performance
- ST-01: reset() returns valid observation (correct shape and range)
- ST-02: random discrete action {0, 1, 2} is accepted without error
- ST-03: step() returns valid next observation
- ST-04: reward is finite at every step
- ST-05: terminated/truncated are properly defined and mutually exclusive
- ST-06: info dict contains all required fields
- ST-07: no crash or unhandled exception for fixed number of steps
- ST-08: log format is compatible with Change 02 baseline metrics
- ST-09: observation feature order is documented
- ST-10: action applied is recorded in info dict
- Smoke test MUST PASS before DQN training begins in Change 04

#### Scenario: Smoke test PASS gate

- **WHEN** Change 04 is about to start DQN training
- **THEN** all ST-01 through ST-10 criteria SHALL be verified and passed
- **THEN** smoke test result (PASS/FAIL) SHALL be reported to Spec Owner
- **THEN** DQN training SHALL NOT begin if any ST criterion fails

#### Scenario: Smoke test non-goals respected

- **WHEN** smoke test is executed
- **THEN** no agent performance metric SHALL be collected or evaluated
- **THEN** no reward improvement trend SHALL be expected or measured
- **THEN** no baseline outperformance SHALL be claimed from smoke test results
