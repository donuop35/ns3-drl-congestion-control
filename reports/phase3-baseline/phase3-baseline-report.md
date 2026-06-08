# Phase 3 Baseline Report

**Generated**: 2026-06-08T14:38:46Z

> **Phase 3 Scope**: Baseline benchmark only. No DRL, no DQN, no PPO.

---

## 1. Objective

Phase 3 establishes the baseline-first foundation for the DRL congestion control project.
The goal is to produce clean, reproducible, and comparable TCP baseline results
that will serve as the reference point for Phase 4 DQN MVP comparison.

This report covers OpenSpec Change 02 (ns3-baseline-benchmark) execution.

## 2. Toolchain Metadata

| Item | Status |
|------|--------|
| ns-3 version | 3.40 (target) |
| NewReno | See raw logs |
| CUBIC | See raw logs |
| BBR | NOT_AVAILABLE |

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

| Method | Required | Status |
|--------|----------|--------|
| NewReno | Required | ⏳ |
| CUBIC | Required | ⏳ |
| BBR | Strongly recommended | NOT_AVAILABLE |

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

- **Delay measurement**: Using FlowMonitor `delaySum/rxPackets` as one-way delay estimate. Direct RTT not available. Marked as `delay_estimate_method: delaySum_per_packet` in logs.
- **BBR**: NOT_AVAILABLE. MVP is not blocked.
- **Utility score**: Provisional. Weights (0.1 for delay, 10 for loss) are subject to revision in Change 04/05 with Spec Owner approval.
- **S3/S4**: Variable BW and cross traffic scenarios may have higher result variability. Results marked as optional/non-blocking.
- **Single run**: Only 1 run per configuration (seed=42). Multiple seeds are recommended for final evaluation (Phase 4+).

## 10. Next Step to Phase 4

Phase 4 (DQN MVP implementation) can only begin after:

1. ✅ Phase 3 baseline artifacts verified by Spec Owner
2. ✅ S1 + NewReno + CUBIC completed
3. ✅ S2 + NewReno + CUBIC completed
4. ✅ Summary CSV and figures available
5. ✅ BBR fallback documented (if BBR unavailable)
6. ⏳ Spec Owner approval to proceed to Phase 4

> **Phase 4 will implement the ns3-gym DRL environment (Change 03) and DQN MVP agent (Change 04). DQN evaluation will be compared against the baseline artifacts produced in this Phase 3 report.**
