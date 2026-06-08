#!/usr/bin/env bash
# Phase 4 Step 1: Rebuild ns-3.40 with contrib/opengym
# Must be run AFTER setup_ns3gym.sh succeeds.
set -e

NS3_DIR="$HOME/ns-allinone-3.40/ns-3.40"
echo "=== [Build] ns-3.40 + contrib/opengym ==="
echo "NS3_DIR: $NS3_DIR"
cd "$NS3_DIR"

echo ""
echo "[1/3] Configure ns-3.40 (optimized, enable opengym)..."
./ns3 configure --enable-examples --build-profile=optimized 2>&1 | tail -5

echo ""
echo "[2/3] Build opengym module..."
./ns3 build opengym 2>&1 | tail -20

echo ""
echo "[3/3] Install ns3gym Python package..."
NS3GYM_SRC="$HOME/ns3-gym-src"

# Try to find setup.py in common locations
if [ -f "${NS3GYM_SRC}/src/ns3gym/setup.py" ]; then
    pip3 install --user "${NS3GYM_SRC}/src/ns3gym/"
elif [ -f "${NS3GYM_SRC}/setup.py" ]; then
    pip3 install --user "${NS3GYM_SRC}/"
else
    # Try pypi ns3gym package
    pip3 install --user ns3gym 2>/dev/null || echo "WARN: ns3gym pip install failed - may need manual install"
fi

# Verify
python3 -c "import ns3gym; print('ns3gym imported OK, version:', getattr(ns3gym, '__version__', 'unknown'))" 2>/dev/null \
    && echo "NS3GYM_PYTHON: OK" \
    || echo "NS3GYM_PYTHON: import failed (normal if pure C++ interface)"

echo ""
echo "BUILD_COMPLETE"
