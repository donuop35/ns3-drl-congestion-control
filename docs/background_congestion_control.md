# Background: Congestion Control

## Overview

Congestion control is a fundamental mechanism in network communication that prevents senders from overwhelming the network with more data than it can handle. Without effective congestion control, packet queues fill up, packet loss increases, and throughput collapses — a phenomenon known as "congestion collapse."

## TCP Congestion Control Algorithms

### NewReno (RFC 6582)

NewReno is an extension of the original TCP Reno algorithm. It improves performance in scenarios where multiple packets are lost in a single window by distinguishing between partial and full acknowledgment. NewReno is the baseline "classic" TCP algorithm and is widely supported across all major operating systems.

Key characteristics:
- AIMD (Additive Increase, Multiplicative Decrease) window control
- Slow start → Congestion Avoidance → Fast Recovery phases
- Conservative approach; may underutilize bandwidth in high-RTT or high-loss paths

### CUBIC (RFC 8312)

CUBIC is the default TCP algorithm in Linux since kernel 2.6.19. It uses a cubic function to control window growth, making it more aggressive in high-bandwidth-delay-product (BDP) networks compared to NewReno.

Key characteristics:
- Cubic window growth function (does not depend on RTT for window growth)
- Better performance on high-BDP links
- Dominant TCP variant in real-world deployments

### BBR (Bottleneck Bandwidth and RTT)

BBR (developed by Google, 2016) takes a fundamentally different approach — it estimates the bottleneck bandwidth and min-RTT to directly model the network pipe, rather than reacting to packet loss as a congestion signal.

Key characteristics:
- Model-based (not loss-based) congestion control
- Explicitly probes for bandwidth and RTT
- Can achieve higher throughput with lower queuing delay
- Available in ns-3 >= 3.32

## Why Congestion Control is a Good DRL Problem

Traditional TCP algorithms use hand-crafted rules (AIMD, cubic curves, RTT estimation) that may be suboptimal for diverse network conditions. DRL offers:

1. **Adaptability**: An agent can learn to respond to complex, dynamic network states
2. **End-to-end optimization**: Directly optimizes a user-defined utility function (throughput - delay - loss)
3. **No manual tuning**: No need to hand-craft α, β, γ parameters for each scenario
4. **Generalization potential**: Trained policy may transfer to unseen network conditions

## Limitations

- DRL agents require training, which has sample efficiency challenges
- Interpretability is limited compared to traditional algorithms
- Safety concerns: an agent might learn to exploit the network in unintended ways
- Performance is only as good as the reward function design
