#!/usr/bin/env bash
# Phase 4 Step 3: Run smoke test with real ns3-gym connection
# Uses: src/gym_env/smoke_test.py
# Prerequisite: ns3.40-congestion-env-optimized binary built

set -e
PROJ="/mnt/c/Users/donuop/Documents/grassland/ns3-drl-congestion-control"
NS3_BIN="$HOME/ns-allinone-3.40/ns-3.40/build/scratch/congestion-env/ns3.40-congestion-env-optimized"

echo "=== Phase 4 Step 3: Smoke Test ==="
echo "Binary: $NS3_BIN"
if [ ! -f "$NS3_BIN" ]; then
    echo "ERROR: Binary not found. Run build_congestion_env.sh first."
    exit 1
fi
echo "Binary exists: OK"

echo ""
echo "=== Run binary --PrintHelp ==="
"$NS3_BIN" --PrintHelp 2>&1 | head -20

echo ""
echo "=== Run Python smoke test ==="
cd "$PROJ"
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
python3 src/gym_env/smoke_test.py \
    --scenarios S1 S2 \
    --n-steps 10 \
    --seed 42 \
    --port 5555 \
    --verbose \
    2>&1

echo "SMOKE_TEST_DONE"
