#!/usr/bin/env bash
# Phase 4: Smoke test runner
set -e
PROJ="/mnt/c/Users/donuop/Documents/grassland/ns3-drl-congestion-control"
cd "$PROJ"
echo "[smoke_test.sh] Running Phase 4 random agent smoke test..."
python3 src/gym_env/smoke_test.py --scenarios S1 S2 --n-steps 20 --seed 42 --verbose "$@"
