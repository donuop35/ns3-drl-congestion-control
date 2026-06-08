#!/usr/bin/env bash
# Verify ns-3 scratch build and check binary
set -e
NS3_DIR="$HOME/ns-allinone-3.40/ns-3.40"
cd "$NS3_DIR"

echo "=== Build congestion-env (verbose) ==="
./ns3 build scratch/congestion-env 2>&1 | tail -15

echo ""
echo "=== Check built binary ==="
find build/ -name "*congestion*" 2>/dev/null | head -5

echo ""
echo "=== Run with --PrintHelp to confirm binary works ==="
NS3BIN=$(find build/ -name "ns3.40-congestion-env-*" 2>/dev/null | head -1)
if [ -n "$NS3BIN" ]; then
    echo "Binary: $NS3BIN"
    "$NS3BIN" --PrintHelp 2>&1 | head -20
else
    echo "Binary not found in build/. Checking scratch path..."
    ls build/scratch/ 2>/dev/null | grep congestion || echo "Not in build/scratch"
    ./ns3 run "scratch/congestion-env --PrintHelp" 2>&1 | head -20
fi

echo "BUILD_VERIFY_DONE"
