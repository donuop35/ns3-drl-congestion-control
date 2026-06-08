## 0. Pre-Apply Cleanup (Spec Owner Required, 2026-06-08)

> ❗ 以下任務必須在 /opsx:apply 前完成。未完成前不得進入 implementation。

- [x] 0.1 Node.js upgrade to v20.19.0+ — Spec Owner 授權直接升級（本次不授予 waiver）
- [x] 0.2 Confirm `node -v` 輸出 >= 20.19.0 後回報
- [x] 0.3 Confirm `openspec --version` 升級後仍可正常執行
- [x] 0.4 Confirm 升級後無 EBADENGINE warning
- [x] 0.5 Validate specs/baseline-methods.md against Change 02 acceptance criteria
- [x] 0.6 Validate specs/topology.md against router-based single bottleneck constraints
- [x] 0.7 Validate specs/metrics-logging.md against metric-equivalent reproducibility and provisional utility_score rules
- [x] 0.8 Validate specs/scenario-matrix.md against MVP-required / optional scenario boundaries
- [x] 0.9 Validate specs/benchmark-risk-register.md against required risk and fallback coverage
- [x] 0.10 Run `openspec status --change "ns3-baseline-benchmark" --json` 後回報，確認仍為 isComplete: true ✅ **confirmed** — `isComplete: true`，4/4 artifacts `status: done`，6 spec files recognized；`openspec validate --strict --json` → `valid: true, issues: [], passed: 1, failed: 0`
- [ ] 0.11 Spec Owner 再次驗收通過，才可執行 /opsx:apply

## 1. Pre-Implementation Environment Check

- [ ] 1.1 Confirm **ns-3.40** is installed in Linux/WSL2 environment: run `./ns3 --version` and verify output is `3.40`
- [ ] 1.2 Confirm ns-3.40 specifically (NOT 3.35, 3.36, or latest stable) — Spec Owner frozen version
- [ ] 1.3 Confirm BBR module availability in ns-3.40: check if `TcpBbr` class exists in `src/internet/model/tcp-bbr.h`
- [ ] 1.4 Confirm Python 3.9+ is available: `python3 --version`
- [ ] 1.5 Install Python dependencies: `pip install numpy pandas matplotlib pyyaml`
- [x] 1.6 Node.js upgraded to v20.19.0+ (pre-apply cleanup task 0.1); `openspec --version` confirmed working
- [ ] 1.7 Run ns-3.40 tutorial example to confirm basic ns-3 functionality: `./ns3 run first` or `./waf --run first`

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
- [ ] 3.6 Verify reproducibility: run same config twice with same seed and confirm metric-equivalent outputs (throughput / RTT / loss within documented tolerance; byte-for-byte FlowMonitor XML identity is NOT required)

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
- [ ] 5.2 Implement utility score calculation: `utility = throughput_norm - 0.1 * rtt_norm - 10.0 * loss_rate` (**provisional formula** — weights are not final; may be revised in Change 04/05 with Spec Owner approval)
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
