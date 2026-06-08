#!/usr/bin/env bash
# =============================================================================
# Phase 4 Step 1: Install ns3-gym (tkn-tub/ns3-gym) for ns-3.40
# Project: DRL for Congestion Control
# OpenSpec Change 03: opengym-env
#
# Prerequisites: ns-3.40 built at ~/ns-allinone-3.40/ns-3.40/
# PHASE 4 SCOPE: ns3-gym installation only.
# =============================================================================

set -e

NS3_DIR="$HOME/ns-allinone-3.40/ns-3.40"
NS3GYM_REPO="https://github.com/tkn-tub/ns3-gym.git"
NS3GYM_DIR="$HOME/ns3-gym-src"
CONTRIB_DIR="${NS3_DIR}/contrib/opengym"
PROJECT_WIN_PATH="/mnt/c/Users/donuop/Documents/grassland/ns3-drl-congestion-control"
METADATA_DIR="${PROJECT_WIN_PATH}/experiments/drl/metadata"
REPORTS_DIR="${PROJECT_WIN_PATH}/reports/phase4-drl-mvp"

mkdir -p "${METADATA_DIR}" "${REPORTS_DIR}"

echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Phase 4 Step 1: ns3-gym Installation                   ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# ── 1. System dependencies ────────────────────────────────────────────────────
echo "[1/6] Installing ZMQ / protobuf / pkg-config system dependencies..."
sudo apt-get update -qq
sudo apt-get install -y \
    libzmq5 libzmq3-dev \
    libprotobuf-dev protobuf-compiler \
    pkg-config \
    2>&1 | grep -E 'Installing|Setting up|already' | head -20
echo "[1/6] System dependencies done."

# ── 2. Clone ns3-gym ──────────────────────────────────────────────────────────
echo ""
echo "[2/6] Cloning tkn-tub/ns3-gym..."
if [ -d "${NS3GYM_DIR}" ]; then
    echo "  Already cloned at ${NS3GYM_DIR}. Pulling latest..."
    cd "${NS3GYM_DIR}" && git pull --rebase 2>&1 | tail -3
else
    git clone --depth=1 "${NS3GYM_REPO}" "${NS3GYM_DIR}" 2>&1
fi
cd "${NS3GYM_DIR}"
NS3GYM_COMMIT=$(git rev-parse HEAD 2>/dev/null || echo "UNKNOWN")
NS3GYM_BRANCH=$(git branch --show-current 2>/dev/null || echo "UNKNOWN")
echo "  ns3-gym commit: ${NS3GYM_COMMIT}"
echo "  ns3-gym branch: ${NS3GYM_BRANCH}"

# ── 3. Check ns3-gym structure ────────────────────────────────────────────────
echo ""
echo "[3/6] Checking ns3-gym repo structure..."
ls -la "${NS3GYM_DIR}/" | head -15

OPENGYM_SUBDIR="${NS3GYM_DIR}/contrib/opengym"
MODEL_SUBDIR="${NS3GYM_DIR}/model"

if [ -d "${OPENGYM_SUBDIR}" ]; then
    echo "  Found: contrib/opengym/ structure"
    NS3GYM_SRC="${OPENGYM_SUBDIR}"
elif [ -d "${NS3GYM_DIR}/opengym" ]; then
    echo "  Found: opengym/ at root"
    NS3GYM_SRC="${NS3GYM_DIR}/opengym"
else
    echo "  Using repo root as opengym source"
    NS3GYM_SRC="${NS3GYM_DIR}"
fi

# ── 4. Install opengym into ns-3.40 contrib ───────────────────────────────────
echo ""
echo "[4/6] Installing opengym into ns-3.40 contrib/opengym..."
if [ -d "${CONTRIB_DIR}" ]; then
    echo "  contrib/opengym already exists, skipping copy"
else
    if [ -d "${OPENGYM_SUBDIR}" ]; then
        cp -r "${OPENGYM_SUBDIR}" "${CONTRIB_DIR}"
        echo "  Copied contrib/opengym → ${CONTRIB_DIR}"
    else
        # Fallback: copy whole repo content if structured differently
        mkdir -p "${CONTRIB_DIR}"
        # Look for CMakeLists.txt or wscript to identify source
        if ls "${NS3GYM_DIR}/"*/CMakeLists.txt 2>/dev/null; then
            cp -r "${NS3GYM_DIR}/"*/ "${CONTRIB_DIR}/" 2>/dev/null || true
        else
            cp -r "${NS3GYM_DIR}/." "${CONTRIB_DIR}/"
        fi
        echo "  Fallback copy to ${CONTRIB_DIR}"
    fi
fi

echo "  Contents of ${CONTRIB_DIR}:"
ls "${CONTRIB_DIR}/" | head -10

# ── 5. Rebuild ns-3.40 with contrib/opengym ───────────────────────────────────
echo ""
echo "[5/6] Rebuilding ns-3.40 with contrib/opengym (this may take 5-10 min)..."
cd "${NS3_DIR}"
./ns3 configure --enable-examples --disable-gtk --build-profile=optimized 2>&1 | tail -3
./ns3 build opengym 2>&1 | grep -E 'error:|warning:|Linking|FAILED|Finished|Building' | tail -15
echo "[5/6] ns-3.40 + opengym build complete (or see errors above)"

# ── 6. Install Python ns3gym package ─────────────────────────────────────────
echo ""
echo "[6/6] Installing Python ns3gym package..."
# Try pip install from ns3-gym repo
if [ -f "${NS3GYM_DIR}/src/ns3gym/setup.py" ]; then
    pip3 install --user "${NS3GYM_DIR}/src/ns3gym/" 2>&1 | tail -5
elif [ -f "${NS3GYM_DIR}/setup.py" ]; then
    pip3 install --user "${NS3GYM_DIR}/" 2>&1 | tail -5
else
    pip3 install --user ns3gym 2>&1 | tail -5
fi
echo "[6/6] ns3gym Python package installation complete"

# ── Verify ─────────────────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Verification                                            ║"
echo "╚══════════════════════════════════════════════════════════╝"
NS3GYM_VERSION=$(python3 -c "import ns3gym; print(getattr(ns3gym, '__version__', 'installed-no-version'))" 2>/dev/null || echo "IMPORT_FAILED")
echo "  ns3gym Python import: ${NS3GYM_VERSION}"

ZMQ_CHECK=$(python3 -c "import zmq; print('zmq', zmq.__version__)" 2>/dev/null || echo "ZMQ_NOT_AVAILABLE")
echo "  zmq: ${ZMQ_CHECK}"

PROTO_CHECK=$(python3 -c "import google.protobuf; print('protobuf', google.protobuf.__version__)" 2>/dev/null || echo "PROTOBUF_NOT_AVAILABLE")
echo "  protobuf: ${PROTO_CHECK}"

# ── Write metadata ─────────────────────────────────────────────────────────────
cat > "${METADATA_DIR}/ns3gym_toolchain_metadata.yaml" << YAML
# ns3-gym Toolchain Metadata — Phase 4 Step 1
# Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
ns3gym:
  repo: "${NS3GYM_REPO}"
  commit: "${NS3GYM_COMMIT}"
  branch: "${NS3GYM_BRANCH}"
  python_import_status: "${NS3GYM_VERSION}"
  contrib_opengym_path: "${CONTRIB_DIR}"
ns3:
  version: "3.40"
  dir: "${NS3_DIR}"
dependencies:
  zmq: "${ZMQ_CHECK}"
  protobuf: "${PROTO_CHECK}"
generated_by: "scripts/phase4/install_ns3gym.sh"
YAML

echo ""
echo "  Metadata: ${METADATA_DIR}/ns3gym_toolchain_metadata.yaml"
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Step 1 Complete. Check output for any errors.          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo "Next: Run scripts/phase4/build_opengym_env.sh"
