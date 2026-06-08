#!/usr/bin/env bash
# =============================================================================
# Phase 3: Baseline Runner Script
# Project: DRL for Congestion Control
# OpenSpec Change 02: ns3-baseline-benchmark
#
# This script runs NewReno / CUBIC / BBR baseline benchmark for S1 and S2.
# Steps C + D + E of Phase 3.
#
# PHASE 3 SCOPE: Baseline only. NO ns3-gym. NO DQN. NO PPO.
# =============================================================================

set -e

NS3_ALLINONE="ns-allinone-3.40"
NS3_VERSION="3.40"
NS3_HOME="/home/donuop"
NS3_INNER="${NS3_HOME}/${NS3_ALLINONE}/ns-${NS3_VERSION}"
PROJECT_WIN_PATH="/mnt/c/Users/donuop/Documents/grassland/ns3-drl-congestion-control"

RAW_LOGS_DIR="${PROJECT_WIN_PATH}/experiments/raw_logs"
SUMMARIES_DIR="${PROJECT_WIN_PATH}/experiments/summaries"
METADATA_DIR="${PROJECT_WIN_PATH}/experiments/metadata"

mkdir -p "${RAW_LOGS_DIR}" "${SUMMARIES_DIR}" "${METADATA_DIR}"

SEED=42
SIM_DURATION=60.0

# ── Verify ns-3 build ─────────────────────────────────────────────────────────
if [ ! -f "${NS3_INNER}/ns3" ]; then
    echo "[ERROR] ns-3.${NS3_VERSION} not found at ${NS3_INNER}"
    echo "  Please run: bash scripts/phase3/ns3_download_build.sh first"
    exit 1
fi

# ── Copy scratch program ───────────────────────────────────────────────────────
SCRATCH_DIR="${NS3_INNER}/scratch"
mkdir -p "${SCRATCH_DIR}"
cp "${PROJECT_WIN_PATH}/src/ns3/baseline-benchmark.cc" "${SCRATCH_DIR}/baseline-benchmark.cc"
echo "[INFO] Copied baseline-benchmark.cc to scratch/"

# ── Build scratch program ──────────────────────────────────────────────────────
cd "${NS3_INNER}"
echo "[INFO] Building baseline-benchmark..."
./ns3 build scratch/baseline-benchmark 2>&1 | tail -10

# ── Helper: run one experiment ─────────────────────────────────────────────────
run_experiment() {
    local TCP_VARIANT="$1"
    local SCENARIO="$2"
    local RUN_ID="$3"

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Running: ${SCENARIO} + ${TCP_VARIANT} | Seed=${SEED} | ${RUN_ID}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    local EXIT_CODE=0
    ./ns3 run "scratch/baseline-benchmark \
        --tcpVariant=ns3::${TCP_VARIANT} \
        --scenario=${SCENARIO} \
        --simDuration=${SIM_DURATION} \
        --seed=${SEED} \
        --runId=${RUN_ID} \
        --outputDir=${RAW_LOGS_DIR}" \
        2>&1 || EXIT_CODE=$?

    if [ $EXIT_CODE -ne 0 ]; then
        echo "[WARN] Run exited with code ${EXIT_CODE}. Recording fallback note."
        echo "${SCENARIO},${TCP_VARIANT},${RUN_ID},${SEED},ERROR,ERROR,ERROR,ERROR,${SIM_DURATION},NO,run_failed_exit_${EXIT_CODE}" \
            >> "${SUMMARIES_DIR}/baseline_summary.csv"
    fi
    return 0
}

# ── Step C: NewReno (TcpLinuxReno in ns-3.40) Baseline ──────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Step C: NewReno (TcpLinuxReno) Baseline                 ║"
echo "╚══════════════════════════════════════════════════════════╝"
run_experiment "TcpLinuxReno" "S1" "run_001"
run_experiment "TcpLinuxReno" "S2" "run_001"

# ── Step D: CUBIC Baseline ────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Step D: CUBIC Baseline                                  ║"
echo "╚══════════════════════════════════════════════════════════╝"
run_experiment "TcpCubic" "S1" "run_001"
run_experiment "TcpCubic" "S2" "run_001"

# ── Step E: BBR Baseline ───────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Step E: BBR Baseline (non-blocking; fallback if fail)  ║"
echo "╚══════════════════════════════════════════════════════════╝"

# Check BBR availability (tcp-bbr.cc confirmed present in ns-3.40)
BBR_STATUS="NOT_FOUND"
if [ -f "${NS3_INNER}/src/internet/model/tcp-bbr.cc" ]; then
    BBR_STATUS="FOUND"
fi
echo "[INFO] BBR source availability: ${BBR_STATUS}"

if [ "${BBR_STATUS}" = "FOUND" ]; then
    run_experiment "TcpBbr" "S1" "run_001" || echo "[WARN] BBR S1 failed, continuing (non-blocking)"
    run_experiment "TcpBbr" "S2" "run_001" || echo "[WARN] BBR S2 failed, continuing (non-blocking)"
else
    echo "[FALLBACK] BBR not available in ns-3.${NS3_VERSION}. Creating BBR_SKIPPED.md..."
    cat > "${PROJECT_WIN_PATH}/experiments/raw_logs/BBR_SKIPPED.md" << 'BBRSKIP'
# BBR Baseline Skipped

**Reason**: TcpBbr implementation not found in ns-3.40.

This is a known limitation. BBR was introduced in ns-3 but may require additional
module configuration or may not be present in the current build.

**Impact**: MVP is NOT blocked. Change 02 specifies BBR as "strongly recommended
but non-blocking". NewReno + CUBIC are the required baselines.

**Fallback**: NewReno + CUBIC baselines provide the required baseline reference
for Phase 4 DQN MVP comparison.

**Resolution options (future)**:
- Check if ns3::TcpBbr is available in a newer ns-3 patch
- Alternatively, use ns-3.36+ which has better BBR support
- This limitation must be documented in Phase 3 baseline report

Generated by: scripts/phase3/baseline_runner.sh
BBRSKIP
    echo "[INFO] BBR_SKIPPED.md created."
fi

# ── Optional Step F: S3 / S4 (non-blocking) ──────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Step F: S3/S4 Optional Scenarios (non-blocking)        ║"
echo "╚══════════════════════════════════════════════════════════╝"

echo "[INFO] Attempting S3 (should-have, non-blocking)..."
run_experiment "TcpLinuxReno" "S3" "run_001" || echo "[WARN] S3 TcpLinuxReno failed (non-blocking)"
run_experiment "TcpCubic"     "S3" "run_001" || echo "[WARN] S3 CUBIC failed (non-blocking)"

echo "[INFO] Attempting S4 (optional, non-blocking)..."
run_experiment "TcpLinuxReno" "S4" "run_001" || echo "[WARN] S4 TcpLinuxReno failed (non-blocking)"
run_experiment "TcpCubic"     "S4" "run_001" || echo "[WARN] S4 CUBIC failed (non-blocking)"

# ── Write run metadata ─────────────────────────────────────────────────────────
METADATA_FILE="${METADATA_DIR}/phase3_run_metadata.yaml"
cat > "${METADATA_FILE}" << YAML
# Phase 3 Baseline Run Metadata
# Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
phase: 3
steps_completed:
  - "C: NewReno baseline (S1+S2)"
  - "D: CUBIC baseline (S1+S2)"
  - "E: BBR baseline (${BBR_STATUS})"
  - "F: S3/S4 optional (attempted)"
ns3_version: "3.40"
seed: ${SEED}
sim_duration_s: ${SIM_DURATION}
tcp_variants_attempted:
  - TcpNewReno
  - TcpCubic
  - TcpBbr (${BBR_STATUS})
scenarios_attempted:
  - S1 (MVP-required)
  - S2 (MVP-required)
  - S3 (should-have, non-blocking)
  - S4 (optional, non-blocking)
output:
  raw_logs: "${RAW_LOGS_DIR}"
  summaries: "${SUMMARIES_DIR}"
generated_by: "scripts/phase3/baseline_runner.sh"
YAML

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Phase 3 Steps C/D/E/F complete                         ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Summary CSV: ${SUMMARIES_DIR}/baseline_summary.csv"
echo "Raw logs:    ${RAW_LOGS_DIR}/"
echo "Metadata:    ${METADATA_FILE}"
echo ""
echo "Next: Run scripts/phase3/analysis.py to produce figures and report."
