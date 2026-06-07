# Methodology: MDP Formulation

## Problem Formulation

We model single-bottleneck-link congestion control as a Markov Decision Process (MDP):

```
M = (S, A, R, P, γ)
```

where:
- **S**: State space (network observations)
- **A**: Action space (rate control decisions)
- **R**: Reward function (throughput-delay-loss trade-off)
- **P**: Transition probability (governed by ns-3 simulation)
- **γ**: Discount factor

## Environment

**Network Topology**:
```
Sender → [Bottleneck Link] → Receiver
```

The bottleneck link has configurable:
- Bandwidth (e.g., 10 Mbps)
- Propagation delay (e.g., 20ms or 100ms)
- Queue discipline (DropTail)
- Queue size (configurable)

## State Space (Observation)

Initial observation vector (4-dimensional):

| Index | Name | Unit | Source | Normalization |
|-------|------|------|--------|---------------|
| 0 | `throughput` | Mbps | ns3-gym measurement | / link_bandwidth |
| 1 | `rtt` | ms | ns3-gym measurement | / max_rtt |
| 2 | `loss_rate` | fraction [0,1] | ns3-gym measurement | already normalized |
| 3 | `cwnd_signal` | segments | ns-3 TCP state | / max_cwnd |

**Note**: Exact implementation of cwnd_signal (direct cwnd access vs. inferred) to be confirmed in Change 03 design.md.

## Action Space

Discrete(3):
- `0`: Decrease — reduce sending rate / cwnd-like signal
- `1`: Keep — maintain current rate
- `2`: Increase — increase sending rate / cwnd-like signal

**Note**: If direct cwnd control is unavailable, the action maps to application-level sending rate control.

## Reward Function

```
r_t = α · throughput_t − β · RTT_t − γ · loss_t
```

**Philosophy**: The agent must learn to transmit efficiently without causing excessive queue buildup (high RTT) or packet loss. Maximizing throughput at the cost of extreme RTT or loss is penalized.

**Initial weights** (subject to tuning after smoke test):
- α = 1.0 (throughput reward)
- β = 0.1 (RTT penalty)
- γ = 10.0 (loss penalty — loss is expensive)

## Episode Structure

- **Episode length**: 60 seconds (initial, may adjust after smoke test)
- **Decision interval**: 500ms (agent takes one action per interval)
- **Steps per episode**: 60s / 0.5s = 120 steps
- **Termination condition**: Simulation time elapsed

## Evaluation Metrics

For both baseline TCP and DRL agent:

1. **Average throughput** (Mbps) — higher is better
2. **Average RTT** (ms) — lower is better
3. **Packet loss rate** (%) — lower is better
4. **Utility score** = throughput_norm − β·RTT_norm − γ·loss_norm — higher is better
5. **Reward curve** (DRL only) — training convergence indicator

## Utility Score Definition

To enable fair comparison between baseline TCP and DRL agent:

```
utility = throughput_norm − 0.1 · rtt_norm − 10.0 · loss_rate
```

where `throughput_norm = throughput / link_bandwidth` and `rtt_norm = rtt / baseline_rtt`.

**Note**: Utility score formula must be finalized in Change 04 design.md before comparison plots are generated.
