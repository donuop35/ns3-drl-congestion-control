# Phase 4 Smoke Test Report

**Generated**: 2026-06-08T16:27:44Z (initial)  
**Hardened**: 2026-06-09 (real-ZMQ enforcement + HAS_NS3GYM check)

> Phase 4 Scope: Smoke test only. No DQN training performed.

---

## 0. Environment Status

| Check | Value |
|-------|-------|
| HAS_NS3GYM | True |
| ns3gym import | ✅ SUCCESS |
| ZMQ mode | real |
| real-ZMQ enforcement | enabled (`allow_dummy=False` by default) |
| NS3_HOME | `/home/donuop/ns-allinone-3.40/ns-3.40` |
| ns-3 binary | ✅ Built (ns3.40-congestion-env-optimized) |
| Python | 3.8.10 (WSL2) |
| SB3 | 2.4.1 |

---

## 1. Summary

| Scenario | ZMQ Mode | Result | Steps | Avg Reward |
|----------|----------|--------|-------|------------|
| S1 (Low Delay, 10ms) | ✅ real | ✅ PASS | 9 | 0.4351 |
| S2 (High Delay, 50ms) | ✅ real | ✅ PASS | 9 | 0.4012 |

- **S1 ZMQ mode**: real
- **S2 ZMQ mode**: real

---

## 2. S1 Smoke Test Details

**Scenario:** S1 — Low Delay (10 Mbps, 10 ms)  
**Result**: ✅ PASS  
**ZMQ mode**: real

**Checks Passed** (9):
- ✅ HAS_NS3GYM = True
- ✅ ZMQ mode = real
- ✅ env construction
- ✅ action_space = Discrete(3)
- ✅ observation_space shape = (5,)
- ✅ reset() succeeds
- ✅ initial obs valid (shape, finite, [0,1])
- ✅ step loop ran 10 steps without crash
- ✅ reward finite (min=0.2986 max=0.6058)
- ✅ throughput non-zero (≥0.1 Mbps in ≥30% of steps)
- ✅ info fields complete

**Sample observation**: `[0.478, 0.134, 0.0, 0.5, 0.5]`  
**Sample reward range**: 0.40 – 0.61  
**Log CSV**: `experiments/drl/logs/smoke_test_s1.csv`

---

## 3. S2 Smoke Test Details

**Scenario:** S2 — High Delay (10 Mbps, 50 ms)  
**Result**: ✅ PASS  
**ZMQ mode**: real

**Checks Passed** (9):
- ✅ HAS_NS3GYM = True
- ✅ ZMQ mode = real
- ✅ env construction
- ✅ action_space = Discrete(3)
- ✅ observation_space shape = (5,)
- ✅ reset() succeeds
- ✅ initial obs valid (shape, finite, [0,1])
- ✅ step loop ran 10 steps without crash
- ✅ reward finite (min=0.3014 max=0.5568)
- ✅ throughput non-zero (≥0.1 Mbps in ≥30% of steps)
- ✅ info fields complete

**Sample observation**: `[0.202, 0.198, 0.0, 0.5, 0.5]`  
**Sample reward range**: 0.30 – 0.56  
**Log CSV**: `experiments/drl/logs/smoke_test_s2.csv`

---

## 4. Gate Decision

✅ **S1 smoke test PASSED** — DQN training on S1 is authorized.

✅ **S2 smoke test PASSED** — DQN training on S2 is authorized.

---

## 5. Real-ZMQ Hardening (Applied 2026-06-09)

- `allow_dummy=False` is the **default** for `Ns3CongestionEnv`
- `RuntimeError` raised if ns3gym is not importable and `allow_dummy=False`
- `RuntimeError` raised if ZMQ reset fails and `allow_dummy=False`
- Smoke test adds: **throughput-nonzero check** (≥0.1 Mbps in ≥30% of steps)
- Smoke test adds: **ZMQ mode assertion** (`zmq_mode=real` required)
- `--allow-dummy` flag available for debug/unit testing only (explicitly labeled as debug-only)
- `HAS_NS3GYM` and `zmq_mode` recorded in smoke test report

---

## 6. Limitations

- `delay_or_rtt_signal` = FlowMonitor delaySum/rxPackets proxy, NOT direct TCP RTT.
- Action is sender-side rate-control abstraction (Fallback Option B per Change 04).
- Formal smoke tests require real ns3-gym / ZMQ. Dummy fallback is disabled by default and only allowed for explicit debug/unit testing with `--allow-dummy`.
