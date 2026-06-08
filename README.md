# DRL-Based Congestion Control over a Bottleneck Link 🚀

> **以深度強化學習進行單一瓶頸鏈路壅塞控制與吞吐量最佳化**  
> **Deep Reinforcement Learning for Congestion Control and Throughput Optimization over a Single Bottleneck Link**
>
> **專案狀態:** 🟢 *Phase 3: Baseline Benchmark — ✅ Completed（2026-06-08）| Pending Spec Owner Review*  
> **DQN 訓練狀態:** ⏳ Not started — Phase 4 will implement DQN MVP after Phase 3 approval

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
node -v               # v20.11.1
npm list -g @fission-ai/openspec --depth=0  # @fission-ai/openspec@1.4.1
openspec --version    # 1.4.1

# Project initialization
openspec update --force   # Updated Antigravity (v1.4.1)
```

> ⚠️ **Node.js 版本警告**：目前環境為 Node.js **v20.11.1**，低於 OpenSpec 官方要求的 **v20.19.0+**。目前功能正常（僅有 `EBADENGINE` WARN）。Change 02 implementation 開始前，建議使用 `nvm install 20.19.0 && nvm use 20.19.0` 升級，或由 Spec Owner 演出明確 waiver。

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
| RL Interface | ns3-gym | Phase 4 (not installed yet) |
| RL Framework | Stable-Baselines3 | Phase 4 (not installed yet) |
| MVP Algorithm | DQN | Phase 4 — NOT started |
| Analysis | Python 3.8+ | numpy, matplotlib |
| Spec Management | OpenSpec | v1.4.1 |

---

## 📦 Installation

> ⚠️ **ns-3 and ns3-gym require Linux.** Use WSL2 (Ubuntu 20.04+) or a Linux VM.

```bash
# 1. Clone repository
git clone <your-repo-url>
cd ns3-drl-congestion-control

# 2. Install ns-3 (see docs/ for detailed instructions - TODO: Change 02)
# 3. Install ns3-gym (see docs/ - TODO: Change 03)
# 4. Install Python dependencies (TODO: Change 04)
pip install stable-baselines3 gymnasium numpy pandas matplotlib
```

> Full installation instructions will be added in Changes 02 and 03.

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

## 🧪 How to Run ns3-gym Smoke Test

> **Status**: ⏳ TODO — will be implemented in Phase 4 (Change 03: opengym-env)  
> ⛔ **Do NOT install ns3-gym until Phase 3 is approved and Phase 4 begins.**

```bash
# Random agent smoke test — Phase 4 only
# python src/gym_env/smoke_test.py --episodes 1
```

---

## 🤖 How to Train DQN

> **Status**: ⏳ TODO — will be implemented in Phase 4 (Change 04: dqn-mvp-agent)  
> ⛔ **DQN has NOT been trained. Do NOT start Phase 4 without Spec Owner approval.**

```bash
# Train DQN agent — Phase 4 only
# python src/agents/train_dqn.py --timesteps 100000

# Evaluate trained model — Phase 4 only
# python src/agents/eval_dqn.py --model experiments/results/dqn/dqn_checkpoint.zip
```

---

## 📊 How to Reproduce Figures

> **Status**: ⏳ TODO — will be implemented in Change 05 (reporting-figures-and-demo)

```bash
# Generate all comparison figures
# python src/analysis/plot_comparison.py --results experiments/results/
```

---

## 📈 Results Summary — Phase 3 Baseline (ns-3.40, seed=42, 60s)

> **Phase 3 baseline completed.** DQN comparison pending Phase 4 — **DRL results NOT available yet.**  
> All values from `experiments/summaries/baseline_summary.csv`. See `reports/phase3-baseline/` for full report.

### Scenario S1 — Low Delay Bottleneck (10 Mbps, 10 ms)

| Algorithm | TypeId | Throughput (Mbps) | Avg Delay (ms) | Loss Rate | Utility† |
|-----------|--------|:-----------------:|:--------------:|:---------:|:--------:|
| **BBR** | ns3::TcpBbr | **9.73** | **25.89** | 0.000000 | **0.947** |
| CUBIC | ns3::TcpCubic | 9.89 | 117.67 | 0.000504 | 0.884 |
| NewReno | ns3::TcpLinuxReno | 9.82 | 105.42 | 0.000731 | 0.875 |

### Scenario S2 — High Delay Bottleneck (10 Mbps, 50 ms)

| Algorithm | TypeId | Throughput (Mbps) | Avg Delay (ms) | Loss Rate | Utility† |
|-----------|--------|:-----------------:|:--------------:|:---------:|:--------:|
| **NewReno** | ns3::TcpLinuxReno | **9.79** | 129.44 | 0.001363 | **0.923** |
| CUBIC | ns3::TcpCubic | 9.59 | 156.27 | 0.008848 | 0.818 |
| BBR ⚠️ | ns3::TcpBbr | 0.39 | 148.65 | 0.015816 | -0.169 |

> † Utility score is **provisional** (α=1.0, β=0.1, λ=10.0). Subject to revision in Phase 4.  
> ⚠️ BBR S2 anomaly: known ns-3.40 TcpBbr limitation in high-RTT scenario. MVP not blocked.  
> **DQN column intentionally omitted** — DQN has not been trained. Phase 4 will add DQN results.

---

## 🗺️ Change Sequence Roadmap

| # | Change Name | Status | Description |
|---|-------------|--------|-------------|
| 01 | `project-charter` | ✅ **APPROVED** | Research direction, MDP definition, charter |
| 02 | `ns3-baseline-benchmark` | ✅ **SPEC APPROVED** / 🟢 **Phase 3 Executed** | ns-3.40 TCP baselines — pending Spec Owner review |
| 03 | `opengym-env` | ✅ **SPEC APPROVED** / ⏳ Phase 4 pending | ns3-gym RL environment + random agent smoke test |
| 04 | `dqn-mvp-agent` | ✅ **SPEC APPROVED** / ⏳ Phase 4 pending | Stable-Baselines3 DQN training + evaluation |
| 05 | `reporting-figures-and-demo` | ⏳ PENDING | Final deliverables, PPT assets, demo script |

---

## ⚠️ Known Limitations

- ns3-gym compatibility with the latest ns-3 version TBD (Change 02)
- Direct cwnd control feasibility TBD (Change 03)
- BBR baseline support depends on ns-3 version (Change 02)
- DQN may not outperform TCP baselines — honest trade-off analysis will be provided

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
│   ├── gym_env/                 # ⏳ Phase 4: ns3-gym environment
│   └── agents/                  # ⏳ Phase 4: DQN agent
├── scripts/
│   └── phase3/
│       ├── install_deps.sh      # ✅ Step A: build dependency installer
│       ├── ns3_download_build.sh # ✅ Step A: ns-3.40 downloader/builder
│       ├── baseline_runner.sh   # ✅ Steps C-F: NewReno/CUBIC/BBR runner
│       └── analysis.py          # ✅ Step G: figures + report generator
├── experiments/
│   ├── raw_logs/                # ✅ 10 CSV + 10 FlowMonitor XML
│   ├── summaries/
│   │   └── baseline_summary.csv # ✅ Phase 3 results
│   └── metadata/
│       ├── toolchain_metadata.yaml   # ✅ ns-3.40 environment info
│       └── phase3_run_metadata.yaml  # ✅ run configuration
├── figures/
│   └── baseline/               # ✅ 4 comparison figures
├── reports/
│   └── phase3-baseline/
│       └── phase3-baseline-report.md  # ✅ Phase 3 baseline report
├── docs/                        # Background docs
├── slides/                      # PPT assets
├── proposal/                    # Original proposal documents
└── pdr/                         # PDR documents
```