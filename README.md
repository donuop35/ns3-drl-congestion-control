# DRL-Based Congestion Control over a Bottleneck Link 🚀

> **以深度強化學習進行單一瓶頸鏈路壅塞控制與吞吐量最佳化**  
> **Deep Reinforcement Learning for Congestion Control and Throughput Optimization over a Single Bottleneck Link**
>
> **專案狀態:** 🟡 *Change 01: project-charter — ✅ Approved（2026-06-08）、Change 02: ns3-baseline-benchmark — In Progress*

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

| Component | Tool | Version |
|-----------|------|---------|
| Network Simulator | ns-3 | >= 3.32 |
| RL Interface | ns3-gym | Latest compatible |
| RL Framework | Stable-Baselines3 | >= 1.8.0 |
| MVP Algorithm | DQN | SB3 DQN |
| Analysis | Python 3.9+ | numpy, pandas, matplotlib |
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

## 🚀 How to Run Baseline

> **Status**: ⏳ TODO — will be implemented in Change 02 (ns3-baseline-benchmark)

```bash
# Run TCP NewReno baseline (Scenario A: low-latency bottleneck)
# python scripts/run_baseline.py --config experiments/configs/scenario_a.yaml --algo NewReno

# Run TCP CUBIC baseline
# python scripts/run_baseline.py --config experiments/configs/scenario_a.yaml --algo CUBIC
```

---

## 🧪 How to Run ns3-gym Smoke Test

> **Status**: ⏳ TODO — will be implemented in Change 03 (ns3-gym-environment)

```bash
# Random agent smoke test
# python src/gym_env/smoke_test.py --episodes 1 --config experiments/configs/scenario_a.yaml
```

---

## 🤖 How to Train DQN

> **Status**: ⏳ TODO — will be implemented in Change 04 (dqn-mvp-agent)

```bash
# Train DQN agent
# python src/agents/train_dqn.py --config experiments/configs/scenario_a.yaml --timesteps 100000

# Evaluate trained model
# python src/agents/eval_dqn.py --model experiments/results/dqn_model.zip --config experiments/configs/scenario_a.yaml
```

---

## 📊 How to Reproduce Figures

> **Status**: ⏳ TODO — will be implemented in Change 05 (reporting-figures-and-demo)

```bash
# Generate all comparison figures
# python src/analysis/plot_comparison.py --results experiments/results/
```

---

## 📈 Results Summary

> **Status**: ⏳ PENDING — experiments not yet run

| Metric | NewReno | CUBIC | BBR | DQN (ours) |
|--------|---------|-------|-----|------------|
| Avg Throughput (Mbps) | TBD | TBD | TBD | TBD |
| Avg RTT (ms) | TBD | TBD | TBD | TBD |
| Packet Loss (%) | TBD | TBD | TBD | TBD |
| Utility Score | TBD | TBD | TBD | TBD |

---

## 🗺️ Change Sequence Roadmap

| # | Change Name | Status | Description |
|---|-------------|--------|-------------|
| 01 | `project-charter` | 🟡 IN PROGRESS | Research direction freezing, MDP definition, charter document |
| 02 | `ns3-baseline-benchmark` | ⏳ PENDING | ns-3 single bottleneck TCP baselines (NewReno, CUBIC, BBR) |
| 03 | `ns3-gym-environment` | ⏳ PENDING | ns3-gym RL environment + random agent smoke test |
| 04 | `dqn-mvp-agent` | ⏳ PENDING | Stable-Baselines3 DQN training + evaluation |
| 05 | `reporting-figures-and-demo` | ⏳ PENDING | Final deliverables, figures, PPT assets, demo script |

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
│   ├── changes/
│   │   ├── project-charter/     # Change 01 (IN PROGRESS)
│   │   │   ├── proposal.md
│   │   │   ├── design.md
│   │   │   ├── tasks.md
│   │   │   └── specs/project-charter/spec.md
│   │   └── archive/
│   └── specs/
├── .agent/                      # OpenSpec Antigravity integration
│   ├── skills/                  # openspec-*/SKILL.md
│   └── workflows/               # opsx-*.md
├── docs/                        # Background docs
│   ├── background_congestion_control.md
│   ├── methodology_mdp.md
│   ├── related_work.md
│   └── risk_register.md
├── src/
│   ├── ns3/                     # ns-3 simulation scripts (Change 02)
│   ├── gym_env/                 # ns3-gym environment (Change 03)
│   ├── agents/                  # DQN agent (Change 04)
│   └── analysis/                # Analysis and plotting (Change 05)
├── experiments/
│   ├── configs/                 # Scenario configurations (with random seeds)
│   ├── logs/                    # Experiment logs
│   └── results/                 # CSV results and trained models
├── figures/                     # Generated figures
├── slides/                      # PPT assets
├── scripts/                     # Utility scripts
├── proposal/                    # Original proposal documents
└── pdr/                         # PDR documents
```