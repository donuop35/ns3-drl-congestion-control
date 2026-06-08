## Purpose

定義 Change 04 dqn-mvp-agent 的 DQN training / evaluation 成功標準、失敗定義、stop rules 與 fallback rules。

本檔案是判斷 DQN MVP 是否可進入 final report 的 decision framework。

---

## Full Success

DQN 達到 **full success** 的條件：

所有以下條件均滿足：

- [ ] Smoke test ST-01~ST-10 PASSED（pre-training gate）
- [ ] DQN training converges（episode reward 呈上升趨勢且穩定；不需要 monotonic）
- [ ] DQN evaluation S1 throughput ≥ NewReno or CUBIC throughput（at least one baseline）
- [ ] DQN evaluation S1 delay and loss rate are NOT significantly worse than baseline（within ±20% relative）
- [ ] DQN evaluation S2 achieves similar result on at least one metric
- [ ] All required output artifacts are present（logs + figures + tables）
- [ ] Evaluation metrics are baseline-compatible（same unit and calculation）

**Interpretation**: DQN shows competitive or superior performance to classical baselines in the congestion control task. Present as main contribution.

---

## Partial Success

DQN 達到 **partial success** 的條件（以下任一組合）：

- DQN converges in S1 but not S2（or vice versa）
- DQN improves throughput but has higher delay or loss than baseline
- DQN outperforms NewReno but not CUBIC
- DQN shows convergence trend but did not complete enough timesteps for full evaluation
- DQN utility score improves over baseline, even if individual metrics are mixed

**Interpretation**: DQN shows promise but has limitations. Present as "DQN achieves partial improvement" with analysis of trade-offs. Include in final report as main result with clear limitation statement.

---

## Failure but Reportable

DQN 達到 **failure but reportable** 的條件：

- DQN converges（episode reward stabilizes）but ALL evaluation metrics are worse than NewReno AND CUBIC
- DQN converges to a conservative strategy（always action 1: keep）with no performance improvement

**This is NOT automatic project failure.** Required actions:

1. **Record all evaluation results honestly** in comparison tables and figures
2. **Analyze possible causes**：
   - Reward function may be poorly shaped（e.g., β or λ too large）
   - Observation may be insufficient（e.g., missing queue occupancy）
   - Training timesteps may be insufficient for convergence
   - Decision interval may be too coarse for effective control
3. **Present as limitation and future work** in final report, PPT, and video
4. **Do NOT re-train without reporting to Spec Owner**

**Interpretation**: DQN provides valuable experimental data about the difficulty of applying DRL to this problem. The limitation analysis itself is a scientific contribution.

---

## Stop Rules（Mandatory）

The following conditions require **immediate stop and report to Spec Owner**：

| Stop Condition | Action |
|---------------|--------|
| Smoke test FAIL（any ST condition）| Stop DQN training; fix environment first |
| Training reward is non-finite（NaN / Inf / -Inf）at any step | Stop training; investigate reward computation |
| Training reward diverges（unbounded increase）| Stop training; investigate reward scaling |
| ns-3.40 simulation crashes during training | Stop; attempt restart; if persistent, report |
| ns3-gym socket disconnects repeatedly | Stop; investigate environment stability |
| DQN checkpoint cannot be loaded for evaluation | Stop; re-run training with same config |
| Evaluation metrics are completely undefined（all NaN）| Stop; investigate info dict |

**After stopping**: Do NOT silently restart with different config. Report stop condition and config to Spec Owner before any adjustment.

---

## Fallback Rules

| Situation | Fallback |
|-----------|---------|
| BBR unavailable in ns-3.40 | Create `BBR_SKIPPED.md`; continue without BBR comparison |
| S2 evaluation fails（environment issue）| Report S1 only; document S2 as limitation |
| DQN does not converge in allocated timesteps | Report partial results; increase timesteps（with Spec Owner approval）or document as limitation |
| Training reward stabilizes at low value | Report as "DQN converges to suboptimal policy"; analysis in limitation section |
| `prev_action_norm` excluded from observation（Change 03 OQ-03.03）| Confirm observation shape [4]; update training config; re-run smoke test |
| Model checkpoint corrupted | Re-run training with same config; document in limitation |

---

## Evaluation Result Reporting Rules

1. **Always report all 4 metrics**：throughput / delay / loss / utility（per scenario）
2. **Always include training reward curve**：as diagnostic（not success criterion）
3. **Always include comparison table**：DQN vs NewReno vs CUBIC（vs BBR if available）
4. **Never cherry-pick episodes**：use mean（+ std if multiple episodes）over full evaluation
5. **Never hide underperformance**：if DQN loses on any metric, report it with analysis

---

## Success Criteria Summary Table

| Level | DQN convergence | vs NewReno | vs CUBIC | Artifacts | Interpretation |
|-------|----------------|-----------|---------|-----------|---------------|
| **Full Success** | ✅ Converges | ≥ on throughput + acceptable d/l | ≥ on throughput + acceptable d/l | ✅ Complete | Main contribution |
| **Partial Success** | ✅ Converges | Improves ≥ 1 metric | Mixed | ✅ Complete | Promising with limitation |
| **Failure but Reportable** | ✅ Converges（to suboptimal）| < all metrics | < all metrics | ✅ Complete | Limitation + future work |
| **Stop（Non-reportable）**| ❌ Non-finite / diverge | N/A | N/A | ❌ Incomplete | Stop + report Spec Owner |
