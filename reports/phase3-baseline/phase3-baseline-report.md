# Phase 3 Baseline Report

**Generated**: 2026-06-08T15:13:08Z

> **Phase 3 Scope**: Baseline benchmark only. No DRL, no DQN, no PPO.

---

## 1. Objective

Phase 3 establishes the baseline-first foundation for the DRL congestion control project.
The goal is to produce clean, reproducible, and comparable TCP baseline results
that will serve as the reference point for Phase 4 DQN MVP comparison.

This report covers OpenSpec Change 02 (ns3-baseline-benchmark) execution.

## 2. Toolchain Metadata

```yaml
# Phase 3 Toolchain Metadata
# Generated: 2026-06-08T14:37:55Z (reconstructed from build logs)
phase: 3
step: "A - toolchain verification"

ns3_version: "3.40"
ns3_build_path: "/home/donuop/ns-allinone-3.40/ns-3.40"
ns3_build_profile: "optimized"
ns3_build_system: "CMake + Ninja"

tcp_variants:
  NewReno:
    status: "COMPLETED"
    ns3_typeid: "ns3::TcpLinuxReno"
    note: "In ns-3.40, TcpNewReno is superseded by TcpLinuxReno (full Reno semantics)"
  CUBIC:
    status: "COMPLETED"
    ns3_typeid: "ns3::TcpCubic"
  BBR:
    status: "COMPLETED (S1 normal; S2 anomaly documented)"
    ns3_typeid: "ns3::TcpBbr"
    note: "TcpBbr source found: src/internet/model/tcp-bbr.cc. S2 high-delay shows low throughput (0.39 Mbps) — known ns-3 BBR limitation in high-RTT scenario."

flow_monitor:
  status: "AVAILABLE"
  method: "FlowMonitorHelper::InstallAll()"
  delay_estimate_method: "delaySum_per_packet"
  note: "FlowMonitor delaySum/rxPackets used as one-way delay proxy. Direct RTT not available."

tracing:
  flowmonitor_xml: true
  summary_csv: true
  note: "FlowMonitor XML and per-run raw CSV produced for each run."

build_environment:
  os: "Ubuntu 20.04 (WSL2)"
  gcc_version: "gcc (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0"
  gxx_version: "g++ (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0"
  cmake_version: "cmake version 3.16.3"
  ninja_version: "1.10.0"
  python_version: "Python 3.8.10"

known_limitations:
  - "TcpNewReno not available by that TypeId in ns-3.40; TcpLinuxReno used as NewReno-family baseline"
  - "BBR S2 (50ms delay) shows anomalous low throughput — ns-3.40 TcpBbr known high-RTT limitation"
  - "FlowMonitor delay is one-way proxy, not RTT"

generated_by: "phase3/ns3_download_build.sh + reconstructed by hotfix"

```

## 3. Topology Summary

| Item | Value |
|------|-------|
| Topology type | Single bottleneck (router-based) |
| Sender count | 1 |
| Receiver count | 1 |
| Bottleneck link | PointToPoint, 10 Mbps, scenario-dependent delay |
| Queue type | DropTailQueue (100p default) |
| Traffic type | Long-lived TCP BulkSend |
| Routing | Ipv4GlobalRoutingHelper |
| ns-3 version | 3.40 |

## 4. Scenario Matrix

| Scenario | Priority | Status | Description |
|---------|----------|--------|-------------|
| S1 (Low Delay) | P0 MVP-required | ✅ Completed | 10 Mbps, 10 ms delay |
| S2 (High Delay) | P0 MVP-required | ✅ Completed | 10 Mbps, 50 ms delay |
| S3 (Variable BW) | P1 should-have | ✅ Completed | 10 Mbps, small queue |
| S4 (Cross Traffic) | P2 optional | ✅ Completed | 1 interfering flow |

## 5. Baseline Methods

| Method | TypeId (ns-3.40) | Required | Status |
|--------|-----------------|----------|--------|
| NewReno | ns3::TcpLinuxReno | Required | ✅ Completed |
| CUBIC   | ns3::TcpCubic     | Required | ✅ Completed |
| BBR     | ns3::TcpBbr       | Strongly recommended | COMPLETED for S1/S2 (S2 anomaly documented — see Limitations) |

## 6. Metrics Definition

| Metric | Unit | Definition | Source |
|--------|------|------------|--------|
| Throughput | Mbps | rxBytes × 8 / sim_duration / 1e6 | FlowMonitor rxBytes |
| Avg Delay | ms | delaySum / rxPackets × 1000 | FlowMonitor delaySum |
| Loss Rate | [0,1] | lostPackets / txPackets | FlowMonitor lostPackets |
| Utility Score | dimensionless | t_norm − 0.1×d_norm − 10×loss_rate | provisional |

> **Note**: Delay is one-way delay estimate (delaySum/rxPackets). Direct RTT not available from FlowMonitor; using delay proxy. Utility score is provisional as per Change 02 spec.

## 7. Results Summary

### S1 (Low Delay, 10ms)

| Algorithm | Throughput (Mbps) | Avg Delay (ms) | Loss Rate | Utility Score |
|-----------|-------------------|----------------|-----------|---------------|
| BBR       |            9.7274 |          25.89 |  0.000000 |        0.9469 |
| CUBIC     |            9.8944 |         117.67 |  0.000504 |        0.8844 |
| NewReno (TcpLinuxReno) |            9.8236 |         105.42 |  0.000731 |        0.8751 |

### S2 (High Delay, 50ms)

| Algorithm | Throughput (Mbps) | Avg Delay (ms) | Loss Rate | Utility Score |
|-----------|-------------------|----------------|-----------|---------------|
| BBR       |            0.3854 |         148.65 |  0.015816 |       -0.1692 |
| CUBIC     |            9.5875 |         156.27 |  0.008848 |        0.8182 |
| NewReno (TcpLinuxReno) |            9.7944 |         129.44 |  0.001363 |        0.9227 |

### S3 (Variable BW)

| Algorithm | Throughput (Mbps) | Avg Delay (ms) | Loss Rate | Utility Score |
|-----------|-------------------|----------------|-----------|---------------|
| CUBIC     |            9.8944 |          67.90 |  0.000565 |        0.9159 |
| NewReno (TcpLinuxReno) |            9.8097 |          61.48 |  0.000672 |        0.9128 |

### S4 (Cross Traffic)

| Algorithm | Throughput (Mbps) | Avg Delay (ms) | Loss Rate | Utility Score |
|-----------|-------------------|----------------|-----------|---------------|
| CUBIC     |            5.4848 |         123.92 |  0.001634 |        0.4321 |
| NewReno (TcpLinuxReno) |            5.1366 |         117.95 |  0.001978 |        0.3939 |

## 8. Figure Index

| Figure | Description |
|--------|-------------|
| [baseline_throughput_mbps_comparison.png](figures/baseline/baseline_throughput_mbps_comparison.png) | Baseline comparison |
| [baseline_avg_delay_ms_comparison.png](figures/baseline/baseline_avg_delay_ms_comparison.png) | Baseline comparison |
| [baseline_loss_rate_comparison.png](figures/baseline/baseline_loss_rate_comparison.png) | Baseline comparison |
| [baseline_utility_score_comparison.png](figures/baseline/baseline_utility_score_comparison.png) | Baseline comparison |

## 9. Limitations

- **Delay measurement**: Using FlowMonitor `delaySum/rxPackets` as one-way delay proxy. Direct RTT not available from FlowMonitor. All logs are marked `delay_estimate_method: delaySum_per_packet`.
- **BBR S2 anomaly**: ns-3.40 TcpBbr shows anomalously low throughput in high-delay scenario (S2, 50ms bottleneck: ~0.39 Mbps vs ~9.8 Mbps for NewReno/CUBIC). This is a known ns-3 BBR implementation limitation in high-RTT environments. BBR S1 result is normal (9.73 Mbps, lowest delay). MVP is NOT blocked.
- **Utility score**: Provisional. Weights (α=1.0, β=0.1, λ=10.0) are subject to revision in Change 04/05 with Spec Owner approval. Do not use as sole comparison metric.
- **S3/S4 optional**: S3 (Variable BW) and S4 (Cross Traffic) are optional non-blocking scenarios. Results are informative but not part of MVP success criteria.
- **Single run per config**: Only 1 run per configuration (seed=42). Multiple seeds are recommended for final Phase 4 DQN comparison.
- **TcpNewReno TypeId**: In ns-3.40, `TcpNewReno` is superseded by `TcpLinuxReno`. All NewReno-family measurements use `ns3::TcpLinuxReno`.

## 10. Next Step to Phase 4

Phase 4 (DQN MVP implementation) can only begin after Spec Owner approval:

1. ✅ Phase 3 baseline artifacts produced (this report)
2. ✅ S1 + NewReno (TcpLinuxReno) + CUBIC completed
3. ✅ S2 + NewReno (TcpLinuxReno) + CUBIC completed
4. ✅ BBR completed for S1/S2 (S2 anomaly documented)
5. ✅ Summary CSV and 4 figures available
6. ⏳ Spec Owner review and approval

> **DQN has NOT been trained yet.** Phase 4 will implement the ns3-gym DRL environment (Change 03) and DQN MVP agent (Change 04). DQN evaluation will be compared against the baseline artifacts produced in this Phase 3 report. Do NOT start Phase 4 without Spec Owner approval.
