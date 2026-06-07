# Risk Register

Last updated: 2026-06-08

## Risk Summary Table

| ID | Risk | Level | Mitigation | Fallback | Owner |
|----|------|-------|-----------|---------|-------|
| R1 | OpenSpec CLI fails | HIGHEST | Verified v1.4.1 installed | No fallback; must stop and report | Antigravity |
| R2 | ns3-gym install fails | HIGH | Pin Linux env, run official example first | Pure Python Gym bottleneck env | Antigravity |
| R3 | BBR baseline integration difficult | MED-HIGH | NewReno+CUBIC first; BBR optional | Move to optional/future work | Antigravity |
| R4 | Cannot directly control cwnd | HIGH | Confirm ns-3/ns3-gym control interface | Application sending rate control | Antigravity |
| R5 | Reward causes wrong agent behavior | HIGH | Include RTT+loss penalty; log components | Fix weights; reduce scenario complexity | Antigravity |
| R6 | DQN performs poorly | MED-HIGH | Simple action space; smoke test first | Honest trade-off analysis | Antigravity |
| R7 | Scope expands to IPFS/QUIC/multi-agent | HIGHEST | Non-goals in charter; check each change | Stop change; return to charter review | Spec Owner |
| R8 | Node.js version warning (v20.11.1 < 20.19.0) | LOW | v1.4.1 works with WARN; upgrade if needed | Upgrade Node.js to 20.19.0+ | Antigravity |

## Detailed Risk Descriptions

### R1: OpenSpec CLI unavailable

**Status**: ✅ MITIGATED — OpenSpec v1.4.1 installed and verified  
**Trigger**: `openspec --version` fails or Antigravity integration missing  
**Response**: Stop all work immediately; report to Spec Owner; do NOT use fake OpenSpec

### R2: ns3-gym installation failure

**Status**: ⏳ PENDING — not yet attempted  
**Trigger**: `openai_gym.reset()` or `step()` fails after 3 repair attempts  
**Response**:
1. Report detailed error log
2. Propose fallback: simplified Python Gym bottleneck simulator
3. Wait for Spec Owner approval before switching

### R3: BBR baseline integration

**Status**: ⏳ PENDING — to be assessed in Change 02  
**Trigger**: BBR integration takes > 1 working day  
**Response**: Move BBR to optional; complete NewReno+CUBIC; document reason in Change 02 README

### R4: cwnd control interface

**Status**: ⏳ PENDING — to be confirmed in Change 03  
**Trigger**: ns-3/ns3-gym does not expose writable cwnd  
**Response**: Use application-level sending rate as proxy; update design.md; get Spec Owner confirmation

### R5: Reward function design

**Status**: ⏳ PENDING — to be validated in Change 03 smoke test  
**Trigger**: Agent learns to maximize throughput by flooding queue (high RTT, high loss)  
**Response**: Add stronger loss penalty; log reward components separately; reduce episode length

### R6: DQN convergence

**Status**: ⏳ PENDING — to be observed in Change 04  
**Trigger**: Reward curve shows no improvement after reasonable training  
**Response**: Analyze reward components; compare utility vs. baseline honestly; do NOT fabricate results

### R7: Scope expansion

**Status**: 🔴 HIGHEST priority enforcement  
**Trigger**: Any task involving IPFS, QUIC, Linux kernel, multi-agent, large topology appears  
**Response**: Immediate stop; report to Spec Owner; no implementation until approval

### R8: Node.js version

**Status**: 🟡 LOW — WARN only, functionality not impacted  
**Trigger**: OpenSpec features break due to Node.js v20.11.1  
**Response**: Upgrade Node.js to 20.19.0+ using nvm or official installer
