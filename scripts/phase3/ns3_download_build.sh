#!/usr/bin/env bash
# =============================================================================
# Phase 3: ns-3.40 Download and Build Script
# Project: DRL for Congestion Control
# =============================================================================
# This script downloads ns-allinone-3.40 and builds ns-3.
# After build, it verifies TCP variant availability for baseline benchmark.
#
# PHASE 3 SCOPE:
#   - Build ns-3.40 only
#   - Verify NewReno / CUBIC / BBR TCP variants
#   - NO ns3-gym, NO DQN, NO PPO

set -e

NS3_ALLINONE="ns-allinone-3.40"
NS3_DIR="$HOME/${NS3_ALLINONE}"
NS3_SOURCE_URL="https://www.nsnam.org/releases/${NS3_ALLINONE}.tar.bz2"
NS3_VERSION="3.40"

# Windows mount path to project repo
PROJECT_WIN_PATH="/mnt/c/Users/donuop/Documents/grassland/ns3-drl-congestion-control"
METADATA_DIR="${PROJECT_WIN_PATH}/experiments/metadata"
mkdir -p "${METADATA_DIR}"

echo "=== Phase 3: ns-3.${NS3_VERSION} Download and Build ==="
echo "Target: ${NS3_DIR}"
echo ""

# ── Check if already downloaded ──────────────────────────────────────────────
if [ -d "${NS3_DIR}" ]; then
    echo "[INFO] ${NS3_DIR} already exists, skipping download."
else
    echo "[1/4] Downloading ns-${NS3_VERSION} source..."
    cd "$HOME"
    wget -c "${NS3_SOURCE_URL}" -O "${NS3_ALLINONE}.tar.bz2"
    echo "[2/4] Extracting..."
    tar -xjf "${NS3_ALLINONE}.tar.bz2"
    rm "${NS3_ALLINONE}.tar.bz2"
fi

# ── Build ns-3.40 ────────────────────────────────────────────────────────────
NS3_INNER="${NS3_DIR}/ns-${NS3_VERSION}"
if [ ! -f "${NS3_INNER}/ns3" ]; then
    echo "[3/4] Building ns-3.${NS3_VERSION} (this may take 10-20 minutes)..."
    cd "${NS3_INNER}"
    ./ns3 configure --enable-examples --disable-gtk --build-profile=optimized 2>&1 | tail -30
    ./ns3 build 2>&1 | tail -20
else
    echo "[INFO] ns-3.${NS3_VERSION} already built (ns3 binary found)."
fi

# ── Verify build and TCP variant availability ─────────────────────────────────
echo ""
echo "[4/4] Verifying toolchain..."
cd "${NS3_INNER}"

NS3_VER_OUTPUT=$(./ns3 --version 2>&1)
echo "  ns-3 version: ${NS3_VER_OUTPUT}"

# Check TCP variants via scratch example
echo "  Checking TCP variant availability..."
NEWTCP_AVAILABLE="UNKNOWN"
CUBIC_AVAILABLE="UNKNOWN"
BBR_AVAILABLE="UNKNOWN"

# Check source files for TCP variant headers
if ls src/internet/model/tcp-newreno.cc 2>/dev/null | head -1; then
    NEWTCP_AVAILABLE="YES"
fi
if ls src/internet/model/tcp-cubic.cc 2>/dev/null | head -1; then
    CUBIC_AVAILABLE="YES"
fi
if ls src/internet/model/tcp-bbr.cc 2>/dev/null | head -1; then
    BBR_AVAILABLE="YES"
else
    BBR_AVAILABLE="NOT_FOUND"
fi

echo ""
echo "=== Toolchain Verification Results ==="
echo "ns-3 version:     ${NS3_VER_OUTPUT}"
echo "NewReno:          ${NEWTCP_AVAILABLE}"
echo "CUBIC:            ${CUBIC_AVAILABLE}"
echo "BBR:              ${BBR_AVAILABLE}"
echo "FlowMonitor:      $(ls src/flow-monitor/model/*.cc 2>/dev/null | wc -l) files found"
echo "Build path:       ${NS3_INNER}"
echo ""

# ── Write metadata ─────────────────────────────────────────────────────────────
METADATA_FILE="${METADATA_DIR}/toolchain_metadata.yaml"
cat > "${METADATA_FILE}" << YAML
# Phase 3 Toolchain Metadata
# Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
phase: 3
step: A
ns3_version: "${NS3_VERSION}"
ns3_build_path: "${NS3_INNER}"
tcp_variants:
  NewReno: "${NEWTCP_AVAILABLE}"
  CUBIC: "${CUBIC_AVAILABLE}"
  BBR: "${BBR_AVAILABLE}"
flow_monitor: "$(ls src/flow-monitor/model/*.cc 2>/dev/null | wc -l) files"
python_version: "$(python3 --version 2>&1)"
gcc_version: "$(gcc --version 2>&1 | head -1)"
cmake_version: "$(cmake --version 2>&1 | head -1)"
generated_by: "phase3/ns3_download_build.sh"
YAML

echo "Toolchain metadata written to: ${METADATA_FILE}"
echo ""
echo "Next: Run baseline_runner.sh to execute NewReno / CUBIC / BBR scenarios."
