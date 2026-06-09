# DRL-Based Congestion Control over a Bottleneck Link 🚀

> **以深度強化學習進行單一瓶頸鏈路壅塞控制與吞吐量最佳化**  
> **Deep Reinforcement Learning for Congestion Control and Throughput Optimization over a Single Bottleneck Link**
>
> **專案狀態:** 🟢 *Phase 4: DRL MVP Implementation — ✅ Excellent Acceptance Complete (2026-06-09) | Pending Spec Owner Review*  
> **DQN 訓練狀態:** ✅ S1 Complete (30k steps, ep_rew_mean=84.4) | ✅ S2 Complete (30k steps, ep_rew_mean=86.5) | Eval+Compare done | Pending Phase 5 approval

> 🎥 **Demo Video**: TODO — 正式 demo video 將在 Change 05 完成後補上。

---

## 📌 Research Motivation

Network congestion control is a fundamental problem in computer networking. Traditional TCP algorithms (NewReno, CUBIC, BBR) use hand-crafted rules to manage sending rates. Deep Reinforcement Learning (DRL) offers the potential to learn adaptive policies that optimize a richer utility function:

```
maximize: throughput
minimize: RTT (delay)
minimize: packet loss rate
```

This project formalizes single-bottleneck-link congestion control as an MDP, trains a DQN agent using Stable-Baselines3 on a reproducible ns-3 / ns3-gym simulation environment, and compares the DRL agent against TCP baselines.

**Thesis**: 本研究將單一瓶頸鏈路的壅塞控制建模為深度強化學習問題，透過 ns-3 / ns3-gym 建立可重現的網路模擬環境，讓 agent 學習在 throughput、RTT 與 packet loss 之間取得更好的控制折衷，並與傳統 TCP baseline 進行比較。

---

## 🚫 Scope and Non-Goals

### In Scope (MVP)
- Single bottleneck link: `sender → bottleneck → receiver`
- TCP baselines: NewReno, CUBIC (+ BBR if supported)
- DRL agent: Stable-Baselines3 DQN, discrete action space (3 actions)
- Metrics: throughput, RTT, packet loss, utility score, reward curve
- Scenarios: at least 2 (Scenario A: low-latency, Scenario B: high-latency)

### Out of Scope (Non-Goals)
- ❌ IPFS implementation (motivation/future work only)
- ❌ QUIC congestion control
- ❌ Linux kernel TCP stack modification
- ❌ Multi-agent RL
- ❌ Large-scale network topology (> sender + bottleneck + receiver)
- ❌ Multi-path transmission
- ❌ Real Internet deployment
- ❌ Production-grade TCP protocol
- ❌ Claiming DRL universally outperforms all TCP baselines

---

## 🔧 Official OpenSpec Setup Proof

This project uses **OpenSpec v1.4.1** for Spec-Driven Development.

```bash
# Installation verification
node -v               # v20.20.2 (Windows, meets OpenSpec ≥ 20.19.0 requirement)
npm list -g @fission-ai/openspec --depth=0  # @fission-ai/openspec@1.4.1
openspec --version    # 1.4.1

# Project initialization
openspec update --force   # Updated Antigravity (v1.4.1)
```

> ℹ️ **Node.js 版本**: 現在使用 Node.js **v20.20.2** (Windows) ≥ 官方要求的 20.19.0+。

**Generated files:**
```
.agent/skills/openspec-apply-change/SKILL.md
.agent/skills/openspec-archive-change/SKILL.md
.agent/skills/openspec-explore/SKILL.md
.agent/skills/openspec-propose/SKILL.md
.agent/skills/openspec-sync-specs/SKILL.md
.agent/workflows/opsx-apply.md
.agent/workflows/opsx-archive.md
.agent/workflows/opsx-explore.md
.agent/workflows/opsx-propose.md
.agent/workflows/opsx-sync.md
```

**Change 01 status** (verified by `openspec status --change "project-charter"`):
```
Progress: 4/4 artifacts complete
[x] proposal  [x] design  [x] specs  [x] tasks
```

---

## 🛠️ Toolchain

| Component | Tool | Version / Notes |
|-----------|------|------------------|
| Network Simulator | ns-3 | **3.40** (frozen per Change 02) |
| TCP NewReno | `ns3::TcpLinuxReno` | TcpNewReno superseded in ns-3.40 |
| TCP CUBIC | `ns3::TcpCubic` | Available in ns-3.40 |
| TCP BBR | `ns3::TcpBbr` | Available; S2 anomaly documented |
| Metrics | FlowMonitor | delaySum/rxPackets as delay proxy |
| **RL Interface** | **ns3-gym** | **✅ Installed** (tkn-tub/ns3-gym, commit cfff7f3) |
| **RL Framework** | **Stable-Baselines3** | **✅ v2.4.1** (Phase 4) |
| **RL Algorithm** | **DQN (SB3)** | **✅ Trained S1+S2** (30k steps each, S1 ep_rew_mean=84.4 / S2 ep_rew_mean=86.5, seed=42) |
| **PyTorch** | torch | **2.4.1+cu121** (CPU mode for training) |
| **Gymnasium** | gymnasium | **1.0.0** |
| Analysis | Python 3.8+ | numpy, matplotlib |
| Spec Management | OpenSpec | v1.4.1 |

---

## 📦 Installation

> ⚠️ **ns-3 and ns3-gym require Linux.** Use WSL2 (Ubuntu 20.04+) or a Linux VM.

```bash
# 1. Clone repository
git clone <your-repo-url>
cd ns3-drl-congestion-control

# 2. Install ns-3.40 build dependencies (WSL2)
bash scripts/phase3/install_deps.sh
bash scripts/phase3/ns3_download_build.sh

# 3. Install ns3-gym (Phase 4)
bash scripts/phase4/setup_ns3gym.sh
bash scripts/phase4/build_opengym.sh

# 4. Install Python dependencies
pip install -r requirements-phase4.txt
# or: pip install stable-baselines3 gymnasium torch pyzmq numpy pandas matplotlib
```

---

## 🚀 How to Run Baseline (Phase 3)

> **Status**: ✅ Completed — ns-3.40 baseline benchmark executed

```bash
# Prerequisites: WSL2 Ubuntu 20.04+, build tools installed
# Step A: Install ns-3.40 build dependencies (one-time)
bash scripts/phase3/install_deps.sh

# Step A: Download and build ns-3.40 (one-time, ~15-20 min)
bash scripts/phase3/ns3_download_build.sh

# Steps C/D/E/F: Run NewReno + CUBIC + BBR baselines (S1/S2/S3/S4)
# Must run inside WSL2 as non-root user
bash scripts/phase3/baseline_runner.sh

# Step G: Analyze results and generate report + figures
# Can run from Windows or WSL2
python3 scripts/phase3/analysis.py

# Results will appear in:
#   experiments/summaries/baseline_summary.csv
#   figures/baseline/
#   reports/phase3-baseline/phase3-baseline-report.md
```

---

## 🧪 How to Run ns3-gym Smoke Test (Phase 4 Step 3)

> **Status**: ✅ Completed — Real ZMQ connection to ns-3.40 binary, S1 + S2 both PASS

```bash
# Prerequisites: ns3-gym installed, ns-3.40 binary built
# Run inside WSL2
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Step 1: Clone + install ns3-gym (one-time)
bash scripts/phase4/setup_ns3gym.sh
bash scripts/phase4/build_opengym.sh
python3 -c "from ns3gym import ns3env; print('ns3gym OK')"

# Step 2: Build ns-3 OpenGym environment
bash scripts/phase4/build_congestion_env.sh

# Step 3: Run smoke test (S1 + S2, 10 steps each)
bash scripts/phase4/run_smoke_test.sh
# → Report: reports/phase4-drl-mvp/smoke-test-report.md
```

**Smoke Test Results (2026-06-08):**

| Scenario | ZMQ | Result | Sample obs | Sample reward |
|----------|-----|--------|------------|---------------|
| S1 (Low Delay, 10ms) | ✅ Real | ✅ PASS | `[0.478, 0.134, 0.0, 0.5, 0.5]` | 0.40–0.61 |
| S2 (High Delay, 50ms) | ✅ Real | ✅ PASS | `[0.202, 0.198, 0.0, 0.5, 0.5]` | 0.30–0.56 |

---

## 🤖 How to Train DQN (Phase 4 Step 4)

> **Status**: ✅ Complete — S1 trained (30k steps, seed=42, ep_rew_mean=84.4)  
> **Model**: `experiments/drl/models/dqn_s1_seed42.zip`

```bash
# Train DQN agent (inside WSL2)
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
export PYTHONPATH=/path/to/ns3-drl-congestion-control/src:$PYTHONPATH

# Train S1 (30k steps for MVP)
bash scripts/phase4/train_dqn.sh S1 30000 42

# Evaluate trained model
export MODEL=experiments/drl/models/dqn_s1_seed42.zip
bash scripts/phase4/eval_dqn.sh "$MODEL" S1

# Generate DQN vs Baseline comparison figures
python3 src/analysis/compare_dqn_baseline.py --scenarios S1 S2
```

> **Limitations**:
> - Action = sender-side rate-control abstraction (Fallback Option B). Does NOT directly modify kernel TCP.
> - delay metric = FlowMonitor delaySum/rxPackets proxy, not direct RTT.
> - Reward weights (α=1.0, β=0.1, λ=10.0) are provisional; may be revised in Change 05.

**DQN S1 Results (2026-06-08, deterministic eval, 5 episodes):**

| Algorithm | Throughput (Mbps) | Delay (ms) | Loss Rate | Utility |
|-----------|:-----------------:|:----------:|:---------:|:-------:|
| BBR | 9.727 | **25.9** | 0.000 | **0.947** |
| **DQN (ours)** | **9.877** | 115.3 | 0.004 | **0.900** |
| CUBIC | 9.894 | 117.7 | 0.001 | 0.884 |
| NewReno | 9.824 | 105.4 | 0.001 | 0.875 |

> Honest result: DQN ranks 2nd on utility (better than CUBIC/NewReno, below BBR). See `reports/phase4-drl-mvp/phase4-drl-report.md`.

---

## 📊 How to Reproduce Figures

> **Status**: ⏳ TODO — will be implemented in Change 05 (reporting-figures-and-demo)

```bash
# Generate all comparison figures
# python src/analysis/plot_comparison.py --results experiments/results/
```

---

## 📈 Results Summary — Phase 3 Baseline (ns-3.40, seed=42, 60s)

> **Phase 3 baseline completed. Phase 4 DQN S1 + S2 comparison complete.**  
> All baseline values from `experiments/summaries/baseline_summary.csv`.  
> DQN values from `experiments/drl/summaries/dqn_summary.csv`.  
> See `reports/phase3-baseline/` and `reports/phase4-drl-mvp/` for full reports.

### Scenario S1 — Low Delay Bottleneck (10 Mbps, 10 ms)

| Algorithm | TypeId | Throughput (Mbps) | Avg Delay (ms) | Loss Rate | Utility† |
|-----------|--------|:-----------------:|:--------------:|:---------:|:--------:|
| **BBR** | ns3::TcpBbr | **9.73** | **25.9** | 0.000000 | **0.947** |
| **DQN (ours)** | SB3 DQN | 9.88 | 115.3‡ | 0.004040 | 0.900 |
| CUBIC | ns3::TcpCubic | 9.89 | 117.7 | 0.000504 | 0.884 |
| NewReno | ns3::TcpLinuxReno | 9.82 | 105.4 | 0.000731 | 0.875 |

### Scenario S2 — High Delay Bottleneck (10 Mbps, 50 ms)

| Algorithm | TypeId | Throughput (Mbps) | Avg Delay (ms) | Loss Rate | Utility† |
|-----------|--------|:-----------------:|:--------------:|:---------:|:--------:|
| **NewReno** | ns3::TcpLinuxReno | **9.79** | 129.4 | 0.001363 | **0.923** |
| CUBIC | ns3::TcpCubic | 9.59 | 156.3 | 0.008848 | 0.818 |
| **DQN (ours)** | SB3 DQN | 9.79 | 148.8‡ | 0.055440 | 0.757 |
| BBR ⚠️ | ns3::TcpBbr | 0.39 | 148.7 | 0.015816 | -0.169 |

> † Utility score is **provisional** (α=1.0, β=0.1, λ=10.0). Subject to revision in Phase 5.  
> ⚠️ BBR S2 anomaly: known ns-3.40 TcpBbr limitation in high-RTT scenario. MVP not blocked.  
> ‡ DQN delay uses FlowMonitor delaySum/rxPackets proxy, NOT direct TCP RTT.  
> DQN S1 result: ranks 2nd on utility (better than CUBIC/NewReno, below BBR). Honest result.  
> DQN S2 result: ranks 3rd on utility (high loss=5.5% reflects near-maximum-rate policy under high-RTT conditions). Honest result.  
> DQN is Fallback Option B (sender-side rate-control). Results are **preliminary MVP**, not a claim of universal superiority.

---

## 🗺️ Change Sequence Roadmap

| # | Change Name | Status | Description |
|---|-------------|--------|-------------|
| 01 | `project-charter` | ✅ **APPROVED** | Research direction, MDP definition, charter |
| 02 | `ns3-baseline-benchmark` | ✅ **SPEC APPROVED** / 🟢 **Phase 3 Executed** | ns-3.40 TCP baselines — pending Spec Owner review |
| 03 | `opengym-env` | ✅ **SPEC APPROVED** / ✅ **Phase 4 Implemented** | ns3-gym RL environment + ZMQ smoke test S1+S2 PASS |
| 04 | `dqn-mvp-agent` | ✅ **SPEC APPROVED** / ✅ **Phase 4 Complete** | S1+S2 DQN: ✅ Trained+Eval+Compare | Excellent Acceptance ✅ |
| 05 | `reporting-figures-and-demo` | ⏳ PENDING | Final deliverables, PPT assets, demo script |

---

## ⚠️ Known Limitations

- **ns3-gym**: patched for Gymnasium 1.0 + protobuf 5.x + NumPy 1.24+ compatibility
- **DQN Fallback Option B**: action = sender-side rate-control abstraction, NOT direct kernel TCP cwnd modification
- **Delay proxy**: FlowMonitor delaySum/rxPackets, NOT direct TCP RTT
- **DQN S1 behavior**: 100% increase actions — reflects near-capacity S1 environment, not a general adaptive policy
- **DQN S2 behavior**: high loss rate (5.5%) — agent pursues throughput at expense of loss in high-RTT scenario
- **BBR S2 anomaly**: known ns-3.40 TcpBbr limitation in high-RTT scenario (documented in Phase 3)
- **Seed sensitivity**: DQN utility std=0.000 across eval seeds 42/43/44 — deterministic policy in deterministic simulator

---

## 🔮 Future Work

- PPO with continuous action space for finer-grained rate control
- Multi-flow scenarios (Jain's fairness index analysis)
- Generalization across different network scenarios
- IPFS / decentralized network motivation (not in this semester's scope)
- QUIC congestion control adaptation (not in this semester's scope)

---

## 📂 Repository Structure

```
ns3-drl-congestion-control/
├── README.md                    # This file
├── openspec/                    # Official OpenSpec (v1.4.1)
│   └── changes/
│       ├── project-charter/     # Change 01 ✅ Approved
│       ├── ns3-baseline-benchmark/  # Change 02 ✅ Spec Approved
│       ├── opengym-env/         # Change 03 ✅ Spec Approved
│       └── dqn-mvp-agent/       # Change 04 ✅ Spec Approved
├── src/
│   ├── ns3/
│   │   └── baseline-benchmark.cc  # ✅ Phase 3: ns-3.40 simulation
│   ├── gym_env/                 # ✅ Phase 4: ns3-gym Gymnasium wrapper
│   │   ├── ns3_congestion_env.py  # ✅ Gymnasium env (ZMQ + subprocess)
│   │   └── smoke_test.py        # ✅ Real-ZMQ smoke test S1+S2 PASS
│   └── agents/                  # ✅ Phase 4: DQN agent
│       ├── train_dqn.py         # ✅ S1+S2 complete
│       └── eval_dqn.py          # ✅ S1+S2 complete
├── scripts/
│   └── phase3/
│       ├── install_deps.sh      # ✅ Step A: build dependency installer
│       ├── ns3_download_build.sh # ✅ Step A: ns-3.40 downloader/builder
│       ├── baseline_runner.sh   # ✅ Steps C-F: NewReno/CUBIC/BBR runner
│       └── analysis.py          # ✅ Step G: figures + report generator
├── experiments/
│   ├── raw_logs/                # ✅ 10 CSV + 10 FlowMonitor XML (Phase 3)
│   ├── summaries/
│   │   └── baseline_summary.csv # ✅ Phase 3 baseline (S1-S4, 3 algos)
│   ├── drl/
│   │   ├── models/              # ✅ dqn_s1_seed42.zip + dqn_s2_seed42.zip
│   │   ├── evaluations/         # ✅ dqn_eval_s1.csv + dqn_eval_s2.csv
│   │   ├── summaries/           # ✅ dqn_summary.csv + vs_baseline + seed_sens
│   │   ├── logs/                # ✅ Monitor CSV + ~300+ episode CSVs
│   │   └── metadata/            # ✅ Training metadata YAMLs S1+S2
│   └── metadata/              # ✅ Phase 3 toolchain + run metadata
├── figures/
│   ├── baseline/               # ✅ 4 comparison figures (Phase 3)
│   ├── comparison/             # ✅ 8 DQN vs baseline figures (S1+S2 ×4)
│   └── drl/                    # ✅ Reward curves S1+S2, action dist S1+S2, seed sensitivity
├── reports/
│   ├── phase3-baseline/
│   │   └── phase3-baseline-report.md  # ✅ Phase 3 baseline report
│   └── phase4-drl-mvp/
│       ├── smoke-test-report.md       # ✅ Real-ZMQ hardened S1+S2 PASS
│       ├── phase4-drl-report.md       # ✅ S1+S2 DQN results
│       ├── artifact-index.md          # ✅ Complete artifact directory
│       └── phase4-excellent-acceptance-report.md  # ✅ Excellent Acceptance
├── docs/                        # Background docs
├── slides/                      # PPT assets
├── proposal/                    # Original proposal documents
└── pdr/                         # PDR documents
```