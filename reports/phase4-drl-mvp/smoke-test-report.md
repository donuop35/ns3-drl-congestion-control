# Phase 4 Smoke Test Report

**Generated**: 2026-06-08T16:27:44Z

> Phase 4 Scope: Smoke test only. No DQN training performed.

---

## 1. Summary

| Scenario | Result | Steps | Avg Reward |
|----------|--------|-------|------------|
| S1 (Low Delay) | ✅ PASS | 9 | 0.4351 |
| S2 (High Delay) | ✅ PASS | 9 | 0.4012 |

## S1 Smoke Test Details

**Result**: ✅ PASS

**Checks Passed** (7):
- ✅ env construction
- ✅ action_space = Discrete(3)
- ✅ observation_space shape = (5,)
- ✅ reset() succeeds
- ✅ initial obs valid (shape, finite, [0,1])
- ✅ step loop ran 10 steps without crash
- ✅ reward finite (min=0.2986 max=0.6058)

**Log CSV**: `experiments/drl/logs/smoke_test_s1.csv`

## S2 Smoke Test Details

**Result**: ✅ PASS

**Checks Passed** (7):
- ✅ env construction
- ✅ action_space = Discrete(3)
- ✅ observation_space shape = (5,)
- ✅ reset() succeeds
- ✅ initial obs valid (shape, finite, [0,1])
- ✅ step loop ran 10 steps without crash
- ✅ reward finite (min=0.3014 max=0.5568)

**Log CSV**: `experiments/drl/logs/smoke_test_s2.csv`

## Gate Decision

✅ **S1 smoke test PASSED** — DQN training on S1 is authorized.

✅ **S2 smoke test PASSED** — DQN training on S2 is authorized.

## Limitations

- `delay_or_rtt_signal` = FlowMonitor delaySum/rxPackets proxy, NOT direct TCP RTT.
- Action is sender-side rate-control abstraction (Fallback Option B per Change 04).
- Smoke test runs with dummy observation if ns3gym not installed; check ns3gym install status.
