# Specification: Risk Register

**Target Location:** `openspec/changes/reporting-figures-and-demo/specs/risk-register.md`

## ADDED Requirements

### Req 1: Define Risk Register
The risk register must track and mitigate reporting risks.

#### Scenario: Assessing risks
Given the Change 05 specification
When potential failure modes are analyzed
Then the following 14 risks must be tracked and mitigated.

## Change 05 Risk Register
| Risk ID | Description | Likelihood | Impact | Mitigation Strategy | Contingency Plan | Owner | Trigger |
|---------|-------------|-------------|--------|------------|----------|-------|-------------------|
| R-05-01 | README, report, and PPT results are mismatched. | Medium | High | Define result interpretation rules and centralize data source to Phase 4 CSVs. | Correct the inconsistent document to match the CSV source of truth. | Developer | Reviewer notices differing utility scores across docs. |
| R-05-02 | Figures are inconsistent with CSV data. | Low | High | Enforce programmatic generation of figures from CSVs. | Regenerate figures using analysis scripts. | Developer | Visual inspection shows chart bars not matching CSV values. |
| R-05-03 | Manual editing of result numbers. | Low | Critical | Strict OpenSpec governance prohibiting manual CSV/number edits. | Reject PR/change. Revert to original Phase 3/4 artifacts. | Spec Owner | Git diff shows manual modification of `dqn_summary.csv`. |
| R-05-04 | DQN result overclaiming (e.g., "beats TCP"). | High | High | Explicit forbidden wording lists in PPT and Report specs. | Edit documents to use honest ranking language. | Developer | Draft report uses marketing terminology. |
| R-05-05 | S2 high loss rate (5.54%) is hidden or obscured. | Medium | High | Require S2 loss to be explicitly mentioned in Limitations and Results sections. | Reject document until S2 loss is clearly stated. | Developer | S2 loss is missing from the Limitations slide/section. |
| R-05-06 | Delay proxy is described as true TCP RTT. | High | Medium | Enforce "delay proxy" terminology across all deliverables. | Search and replace "RTT" with "delay proxy" where applicable. | Developer | Use of "true RTT" found in the final report. |
| R-05-07 | Fallback Option B (sender-side abstraction) is omitted. | Medium | Medium | Require Option B to be stated in System Design and Limitations. | Add paragraph explaining the action space abstraction. | Developer | Implementation described as kernel modification. |
| R-05-08 | Demo script is too long for the 10-minute constraint. | High | Medium | Define rigid time allocations per section in `demo-script.md`. | Cut non-essential sections (e.g., live training) and use pre-recorded artifacts. | Developer | Dry run of demo exceeds 10 minutes. |
| R-05-09 | PPT is too technical and not aligned with the initial proposal. | Medium | Medium | Map PPT slides back to project charter objectives. | Simplify architecture slides; focus on problem, method, and results. | Developer | Reviewer feedback indicates the deck misses the big picture. |
| R-05-10 | Final report is too implementation-heavy, lacking analysis. | Medium | Medium | Require specific Discussion and Limitations sections in the report spec. | Expand analysis sections using `result-interpretation.md`. | Developer | Report lacks analysis of why S1 policy is degenerate. |
| R-05-11 | OpenSpec change is not validated prior to implementation. | Low | High | Add `openspec validate` to the final checklist. | Run validation and fix schema errors before proceeding. | Developer | Validation script fails. |
| R-05-12 | Stale TODOs remain in the finalized README. | Low | Low | Explicitly task the cleanup of "Change 05" and "Demo Video" TODOs. | Perform a grep for "TODO" and remove them. | Developer | "TODO" found in the main branch README. |
| R-05-13 | Artifact paths in the manifest are broken. | Low | Medium | Verify paths during manifest creation. | Fix relative paths in the markdown table. | Developer | Clicking a link in the manifest yields a 404/not found. |
| R-05-14 | Professor cannot find core results quickly. | Low | High | Ensure README has a clear "Key Result Summary" at the top level. | Move the summary table higher in the README. | Developer | Core metrics are buried deep in the appendix. |
