#!/usr/bin/env bash
# Deploy opengym-congestion-env.cc to ns-3.40 and build
set -e

NS3_DIR="$HOME/ns-allinone-3.40/ns-3.40"
SRC_CC="/mnt/c/Users/donuop/Documents/grassland/ns3-drl-congestion-control/src/ns3/opengym-congestion-env.cc"

echo "=== [1] Check opengym-congestion-env.cc ==="
if [ ! -f "$SRC_CC" ]; then
    echo "ERROR: Source file not found: $SRC_CC"
    exit 1
fi
echo "Source: $SRC_CC"
wc -l "$SRC_CC"

echo ""
echo "=== [2] Check contrib/opengym module structure ==="
ls "$NS3_DIR/contrib/opengym/examples/"
echo "opengym example sim.cc:"
head -5 "$NS3_DIR/contrib/opengym/examples/opengym/sim.cc" 2>/dev/null || echo "No sim.cc"

echo ""
echo "=== [3] Create opengym example directory for our env ==="
# ns-3 opengym expects scripts in ns-3 scratch/ or contrib/opengym/examples/
# Easiest: use scratch/ directory
SCRATCH_DIR="$NS3_DIR/scratch/congestion-env"
mkdir -p "$SCRATCH_DIR"
cp "$SRC_CC" "$SCRATCH_DIR/congestion-env.cc"
echo "Copied to scratch/congestion-env/"
ls "$SCRATCH_DIR/"

echo ""
echo "=== [4] Build the scratch example ==="
cd "$NS3_DIR"
./ns3 build scratch/congestion-env 2>&1 | grep -E "error:|warning:.*error|Built|Linking|Finished|FAILED" | tail -20
ls build/scratch/congestion-env/ 2>/dev/null | head -5

echo ""
echo "DEPLOY_DONE"
