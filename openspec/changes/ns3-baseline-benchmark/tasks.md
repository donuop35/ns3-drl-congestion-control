## 1. Pre-Implementation Environment Check

- [ ] 1.1 Confirm ns-3 is installed in Linux/WSL2 environment: run `ns3 --version` or `./waf --version`
- [ ] 1.2 Confirm ns-3 version is >= 3.32 (required for BBR module)
- [ ] 1.3 Confirm BBR module availability: check if `TcpBbr` class exists in ns-3 TCP module
- [ ] 1.4 Confirm Python 3.9+ is available: `python3 --version`
- [ ] 1.5 Install Python dependencies: `pip install numpy pandas matplotlib pyyaml`
- [ ] 1.6 Confirm node -v and openspec --version are available (Node.js version note: v20.11.1, < 20.19.0 — consider upgrading before implementation)
- [ ] 1.7 Run ns-3 tutorial example to confirm basic ns-3 functionality: `./waf --run first` or equivalent

## 2. Experiment Configuration Files

- [ ] 2.1 Create `experiments/configs/scenario_a.yaml` with: `link_bandwidth: 10`, `link_delay: "10ms"`, `queue_size: 100`, `sim_duration: 60`, `random_seed: 42`, `tcp_algorithms: [NewReno, CUBIC, BBR]`, `scenario_name: scenario_a`
- [ ] 2.2 Create `experiments/configs/scenario_b.yaml` with: `link_bandwidth: 10`, `link_delay: "50ms"`, `queue_size: 100`, `sim_duration: 60`, `random_seed: 42`, `tcp_algorithms: [NewReno, CUBIC, BBR]`, `scenario_name: scenario_b`
- [ ] 2.3 Validate YAML files can be parsed: `python3 -c "import yaml; yaml.safe_load(open('experiments/configs/scenario_a.yaml'))"`
- [ ] 2.4 Confirm all required fields are present in both config files

## 3. ns-3 Topology Script

- [ ] 3.1 Create `src/ns3/bottleneck_topology.cc` (or `.py` if using Python binding): sender → router → receiver topology
- [ ] 3.2 Implement configurable bottleneck link: read bandwidth, delay, queue size from command-line args or config
- [ ] 3.3 Add FlowMonitor instrumentation to collect per-flow throughput, RTT, packet loss
- [ ] 3.4 Configure ns-3 random seed: `ns3::RngSeedManager::SetSeed(seed)` and `SetRun(run)`
- [ ] 3.5 Test topology with small simulation: 5 Mbps, 5s, verify FlowMonitor output is non-empty
- [ ] 3.6 Verify reproducibility: run same config twice and confirm identical FlowMonitor output

## 4. TCP Baseline Scripts

- [ ] 4.1 Create `scripts/run_baseline.sh` (or `run_baseline.py`) to: load scenario config, invoke ns-3 with specified TCP algorithm, save output log to `experiments/logs/`
- [ ] 4.2 Run NewReno baseline on Scenario A: confirm log is produced in `experiments/logs/scenario_a_NewReno_seed42/`
- [ ] 4.3 Run NewReno baseline on Scenario B: confirm log is produced
- [ ] 4.4 Run CUBIC baseline on Scenario A: confirm log is produced
- [ ] 4.5 Run CUBIC baseline on Scenario B: confirm log is produced
- [ ] 4.6 Assess BBR availability (per D-04 decision gate):
  - If BBR available and cost <= 0.5 days: run BBR baseline on Scenario A and B
  - If BBR unavailable or cost > 0.5 days: create `experiments/results/BBR_SKIPPED.md` with explanation; continue without BBR

## 5. Log Parsing and CSV Generation

- [ ] 5.1 Create `src/analysis/parse_baseline.py`: parse FlowMonitor XML output and extract throughput_mbps, rtt_ms, loss_rate
- [ ] 5.2 Implement utility score calculation: `utility = throughput_norm - 0.1 * rtt_norm - 10.0 * loss_rate`
- [ ] 5.3 Output CSV to `experiments/results/<scenario>_<algo>_seed<seed>.csv` with all required columns
- [ ] 5.4 Parse and validate NewReno Scenario A log: confirm CSV has correct columns and non-trivial values
- [ ] 5.5 Parse and validate NewReno Scenario B log
- [ ] 5.6 Parse and validate CUBIC Scenario A log
- [ ] 5.7 Parse and validate CUBIC Scenario B log
- [ ] 5.8 Parse BBR logs if available; skip gracefully if `BBR_SKIPPED.md` exists
- [ ] 5.9 Add error handling: exit with non-zero code and clear message if log file is missing

## 6. Baseline Comparison Figures

- [ ] 6.1 Create `src/analysis/plot_baseline.py`: read all CSVs in `experiments/results/`, generate comparison figures
- [ ] 6.2 Generate `figures/baseline_throughput_comparison.png`: grouped bar chart, algorithms as groups, scenarios as x-axis
- [ ] 6.3 Generate `figures/baseline_rtt_comparison.png`: same format
- [ ] 6.4 Generate `figures/baseline_loss_comparison.png`: same format
- [ ] 6.5 Verify all figures: labeled axes, legend, >= 150 DPI, consistent algorithm color coding
- [ ] 6.6 Handle missing BBR gracefully: figures show available algorithms without error

## 7. README and Documentation Update

- [ ] 7.1 Update `README.md` "How to Run Baseline" section with actual working commands (replace TODO placeholder)
- [ ] 7.2 Add ns-3 installation instructions or link to `docs/` for Linux/WSL2 setup
- [ ] 7.3 Document BBR status (available or skipped) in README
- [ ] 7.4 Verify README commands are tested and reproducible from a clean checkout

## 8. Spec Owner Review

- [ ] 8.1 Confirm all required baseline CSVs are present
- [ ] 8.2 Confirm all 3 comparison figures are generated and legible
- [ ] 8.3 Confirm no RL / ns3-gym / DQN code was introduced in this change
- [ ] 8.4 Confirm random seeds are fixed and results are reproducible
- [ ] 8.5 Submit change-02 for spec owner review
- [ ] 8.6 Spec owner confirms: baseline benchmark is acceptable → approved to start Change 03
