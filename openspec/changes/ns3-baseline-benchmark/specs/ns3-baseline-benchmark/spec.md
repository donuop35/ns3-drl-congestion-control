## ADDED Requirements

### Requirement: ns3-topology baseline topology setup

The system SHALL provide a configurable ns-3 single bottleneck network topology where:
- A sender node connects to an intermediate router node via a high-bandwidth access link
- The router node connects to a receiver node via a configurable bottleneck link
- The bottleneck link MUST be configurable: bandwidth (Mbps), propagation delay (ms), queue discipline (DropTail), queue size (packets)
- The topology SHALL support at least 2 scenarios with different bottleneck parameters
- Each experiment run MUST use a fixed random seed for reproducibility

#### Scenario: Scenario A topology setup

- **WHEN** `experiments/configs/scenario_a.yaml` is loaded with `link_bandwidth: 10`, `link_delay: 10ms`, `queue_size: 100`, `random_seed: 42`
- **THEN** ns-3 simulation SHALL create a sender → router → receiver topology with the specified parameters and the bottleneck link SHALL be the router → receiver link

#### Scenario: Scenario B topology setup

- **WHEN** `experiments/configs/scenario_b.yaml` is loaded with `link_bandwidth: 10`, `link_delay: 50ms`, `queue_size: 100`, `random_seed: 42`
- **THEN** ns-3 simulation SHALL create the same topology structure with higher propagation delay on the bottleneck link

#### Scenario: Reproducibility with fixed seed

- **WHEN** the same scenario config is run twice with the same `random_seed`
- **THEN** the ns-3 simulation SHOULD produce metric-equivalent outputs (throughput, RTT, loss) within documented tolerance. Note: byte-for-byte identical FlowMonitor XML is NOT required; only metric-level equivalence within tolerance is expected.

---

### Requirement: tcp-baseline benchmark execution

The system SHALL execute TCP congestion control baseline experiments where:
- TCP NewReno benchmark MUST run for all defined scenarios and produce output logs
- TCP CUBIC benchmark MUST run for all defined scenarios and produce output logs
- TCP BBR benchmark SHALL run if **ns-3.40** BBR module is available; otherwise MUST be documented as non-blocking optional
- Each experiment SHALL run for the full simulation duration specified in the config
- Experiments MUST NOT include any RL, ns3-gym, or DQN code

#### Scenario: NewReno baseline Scenario A

- **WHEN** baseline script is invoked with `--algo NewReno --config experiments/configs/scenario_a.yaml`
- **THEN** ns-3 simulation SHALL run to completion and write a FlowMonitor XML (or equivalent) log to `experiments/logs/`

#### Scenario: CUBIC baseline Scenario B

- **WHEN** baseline script is invoked with `--algo CUBIC --config experiments/configs/scenario_b.yaml`
- **THEN** ns-3 simulation SHALL run to completion and write output log to `experiments/logs/`

#### Scenario: BBR optional handling

- **WHEN** BBR is not available in the target ns-3 version
- **THEN** the system SHALL log a warning and skip BBR without failing the overall benchmark run; a `BBR_SKIPPED.md` note SHALL be created in `experiments/results/`

---

### Requirement: baseline-logging metric extraction

The system SHALL extract the following metrics from ns-3 simulation output into a standardized CSV format:

- `throughput_mbps`: average goodput over the experiment duration, in Mbps
- `rtt_ms`: average RTT over the experiment duration, in milliseconds
- `loss_rate`: packet loss rate as a fraction [0, 1]
- `utility_score`: **preliminary baseline visualization metric only**. The system SHALL compute and include a provisional composite score for visualization purposes. The formula (`throughput_norm - 0.1 * rtt_norm - 10.0 * loss_rate`) and weights are **provisional** and may be revised in Change 04 / Change 05 with Spec Owner approval. This field MUST NOT be treated as the final reward function definition.
- `algo`: TCP algorithm name (NewReno, CUBIC, BBR)
- `scenario`: scenario identifier (scenario_a, scenario_b)
- `random_seed`: the seed used for this run

The CSV SHALL be written to `experiments/results/<scenario>_<algo>_seed<seed>.csv`.

#### Scenario: CSV output for NewReno Scenario A

- **WHEN** `src/analysis/parse_baseline.py` is run against the ns-3 log for NewReno Scenario A
- **THEN** it SHALL produce `experiments/results/scenario_a_NewReno_seed42.csv` with all required columns

#### Scenario: Missing log file

- **WHEN** `parse_baseline.py` is invoked with a non-existent log path
- **THEN** it SHALL raise a clear error message and exit with non-zero status code

---

### Requirement: baseline-figures comparison figures

The system SHALL generate at least 3 comparison figures from baseline CSV results:

- **Figure 1**: `figures/baseline_throughput_comparison.png` — grouped bar chart, throughput per algo per scenario
- **Figure 2**: `figures/baseline_rtt_comparison.png` — grouped bar chart, RTT per algo per scenario
- **Figure 3**: `figures/baseline_loss_comparison.png` — grouped bar chart, loss rate per algo per scenario
- Each figure MUST include labeled axes, legend, and algorithm color coding consistent across all figures

#### Scenario: Generate throughput comparison figure

- **WHEN** `src/analysis/plot_baseline.py` is run with all required CSVs present
- **THEN** it SHALL produce `figures/baseline_throughput_comparison.png` at >= 150 DPI

#### Scenario: Missing CSV for one algorithm

- **WHEN** BBR CSV is absent (BBR skipped) but NewReno and CUBIC CSVs are present
- **THEN** the plot script SHALL generate figures for available algorithms and log a warning about missing BBR data

---

### Requirement: experiment-configs scenario configuration files

The system SHALL provide YAML configuration files for each scenario:

Each config MUST contain:
- `scenario_name`: unique identifier string
- `link_bandwidth`: bottleneck bandwidth in Mbps (integer)
- `link_delay`: bottleneck propagation delay string (e.g., `"10ms"`)
- `queue_size`: bottleneck queue size in packets (integer)
- `sim_duration`: simulation duration in seconds (integer)
- `random_seed`: integer seed for reproducibility
- `tcp_algorithms`: list of TCP algorithms to run (e.g., `[NewReno, CUBIC, BBR]`)

#### Scenario: Valid scenario config loading

- **WHEN** a Python script reads `experiments/configs/scenario_a.yaml`
- **THEN** it SHALL parse all required fields without error and `random_seed` SHALL be an integer

#### Scenario: Scenario B higher delay

- **WHEN** scenario_b.yaml is read
- **THEN** `link_delay` SHALL be >= 40ms (high-latency scenario)
