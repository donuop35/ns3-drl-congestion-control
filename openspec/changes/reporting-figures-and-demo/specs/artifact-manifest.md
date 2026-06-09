# Specification: Artifact Manifest

**Target Location:** `reports/final/final-artifact-manifest.md`

## ADDED Requirements

### Req 1: Define Artifact Manifest
The Final Artifact Manifest serves as the ultimate inventory of the project's deliverables.

#### Scenario: Listing the deliverables
Given the artifacts from Phases 0-5
When the manifest is generated
Then it must organize the files into the 9 required categories.

## 1. Purpose
The manifest must organize files into the following categories:

1. **OpenSpec Artifacts:** `.agent/` directories, `changes/` specs.
2. **Source Code Artifacts:** C++ environment, Python wrapper, DQN agent scripts, analysis scripts.
3. **Baseline Data Artifacts:** Phase 3 CSV summaries and metadata.
4. **DRL Data Artifacts:** Phase 4 logs, evaluation CSVs, summary CSVs.
5. **Model Artifacts:** Final `dqn_s1_seed42.zip` and `dqn_s2_seed42.zip`.
6. **Figure Artifacts:** The finalized images in `figures/final/`.
7. **Report Artifacts:** Phase 3 report, Phase 4 reports, Final Phase 5 report.
8. **Demo Artifacts:** Demo script, video link.
9. **PPT Artifacts:** Final slide deck outline and notes.

## 3. Artifact Table Schema
For each artifact listed, the following fields must be provided:
- **Path:** Repository-relative path to the file.
- **Purpose:** Brief description of what the artifact proves or provides.
- **Phase Source:** Which phase (0-5) produced it.
- **Status:** Must be ✅ Complete.
- **Used in Final Report:** Yes/No.
- **Used in PPT:** Yes/No.
- **Used in Demo:** Yes/No.
- **Caveat:** Any limitations (e.g., "delay proxy", "utility is provisional").
