# Design: Change 05 reporting-figures-and-demo

## Design Goal

The goal of Phase 5 is to consolidate the accomplishments of Phases 0–4 into a final project package that is easy for reviewers to understand, verify, and grade. This change ensures that the GitHub README, the final report, the presentation deck (PPT), and the demo video all share a cohesive, honest narrative regarding the DQN agent's successes and limitations.

## Final Narrative Design

The final project will follow this narrative arc:
1. **Problem Statement:** Traditional TCP congestion control relies on hand-crafted rules which struggle to balance competing goals across varying network conditions.
2. **Methodology:** We formulate the single-bottleneck congestion control problem as a Deep Reinforcement Learning (DRL) task (MDP).
3. **Foundation:** Phase 3 established robust baseline benchmarks for NewReno, CUBIC, and BBR in an ns-3.40 environment.
4. **Implementation:** Phase 4 successfully integrated ns3-gym and Stable-Baselines3 to train a DQN Minimum Viable Product (MVP).
5. **Results:** In Scenario 1 (Low Delay), DQN utility ranks 2nd (0.900), below BBR but above CUBIC/NewReno. In Scenario 2 (High Delay), DQN utility ranks 3rd (0.757), below NewReno/CUBIC but avoids the BBR anomaly.
6. **Key Findings:** DQN successfully learns a high-throughput policy but faces limitations in managing the delay/loss trade-off under high-RTT conditions, evident in its high loss rate (5.54% in S2).
7. **Conclusion:** The project successfully delivered a reproducible DRL-based congestion control prototype and an honest evaluation framework. We do not claim DRL universally outperforms TCP baselines, highlighting the challenges of the S2 environment.

## Figure Design

To support the narrative, we require the following figure types:
- Architecture / Pipeline figure (System level)
- Topology figure (Single bottleneck)
- Phase 3 baseline comparison summary
- DQN training reward convergence curves
- Action distribution visualizations
- S1 DQN vs baseline comparison (throughput, delay, loss, utility)
- S2 DQN vs baseline comparison (throughput, delay, loss, utility)
- Utility summary comparison figure
- Limitation / finding summary visual

## Demo Design

The demo must effectively communicate:
- The repository structure and OpenSpec SDD workflow changes.
- The existence and accessibility of Phase 3 baseline and Phase 4 DQN artifacts.
- Instructions to reproduce the real-ZMQ smoke test.
- Instructions to reproduce the DQN evaluation.
- Instructions to regenerate final figures from CSV data.
- The location of the final report.
- A strong emphasis on honest limitations (what not to claim).

## PPT Design

A 10–12 slide final presentation deck, designed for a 10-minute slot:
1. **Title / Research Question**
2. **Motivation and Problem**
3. **System Scope and Non-Goals**
4. **Method Overview:** ns-3 + ns3-gym + DQN
5. **MDP Formulation**
6. **Baseline Benchmark**
7. **OpenGym / DQN MVP Implementation**
8. **Main Results:** S1 (Low Delay)
9. **Main Results:** S2 (High Delay)
10. **Key Findings and Limitations**
11. **Demo / Reproducibility**
12. **Conclusion and Future Work**

Each slide must define its title, key message, suggested visual, speaker notes direction, and strictly forbidden wording.

## Governance Design

- The final report, README, PPT, and demo script must use exactly the same metric values.
- `artifact-index.md` must align perfectly with the final artifact manifest.
- All result claims must be directly traceable to a CSV summary, report, or figure.
- **Absolute prohibition** on manual editing of result numbers, fake figures, result inflation, or scope creep.
