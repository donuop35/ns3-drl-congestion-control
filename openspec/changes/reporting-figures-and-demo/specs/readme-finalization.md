# Specification: README Finalization

**Target Location:** `/README.md`

## ADDED Requirements

### Req 1: Finalize README
The README must transition from an active engineering work-in-progress document to a polished, final project landing page.

#### Scenario: Finalizing the README
Given the completion of Phase 5
When the developer updates the README
Then it must include the required final sections and remove stale content.

## 1. Overview
The final README must contain the following required sections:

## 2. Final Sections Required
1. **Project Overview:** High-level summary of the thesis.
2. **Phase Status:** Must explicitly state "Phase 5 Final Package Complete".
3. **OpenSpec SDD Proof:** Retain proof of governance.
4. **Toolchain:** Finalized list of all tools used across all phases.
5. **How to Run Baseline:** Instructions for Phase 3 reproduction.
6. **How to Run Smoke Test:** Instructions for Phase 4 environment verification.
7. **How to Evaluate DQN:** Instructions for Phase 4 agent evaluation.
8. **How to Reproduce Final Figures:** Instructions for Phase 5 figure generation.
9. **Key Result Summary:** The final table showing S1 and S2 metrics across all algorithms.
10. **Honest Limitations:** Explicit bullet points regarding system constraints.
11. **Final Artifacts:** Links to the Final Report, Demo Video, and PPT Package.
12. **Future Work:** Items beyond the scope of this semester.

## 3. Stale Text Cleanup
- **Remove** any `TODO` items regarding "Change 05", "Demo Video", or "How to Reproduce Figures" once Phase 5 is implemented.
- **Remove** any text implying Phase 4 is "pending", "in progress", or that results are "not available".
- **Ensure** the Repository Structure accurately reflects the final state, including the `reports/final/` and `slides/final/` directories.

## 4. Forbidden Elements
- The README **must not** adopt a marketing tone that exaggerates results.
- It **must not** hide the S2 high loss rate or the BBR S2 anomaly.
- It **must not** omit the Fallback Option B context.
- It **must not** misrepresent the delay proxy as true RTT.
