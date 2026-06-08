#!/usr/bin/env bash
# Phase 4 Step 4: DQN Training
# Gate: smoke test must have passed (smoke-test-report.md must contain "S1 smoke test PASSED")
set -e

PROJ="/mnt/c/Users/donuop/Documents/grassland/ns3-drl-congestion-control"
SCENARIO="${1:-S1}"
TIMESTEPS="${2:-30000}"
SEED="${3:-42}"

echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Phase 4 Step 4: DQN Training                           ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo "  Scenario:  $SCENARIO"
echo "  Timesteps: $TIMESTEPS"
echo "  Seed:      $SEED"
echo ""

cd "$PROJ"
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
export PYTHONPATH="$PROJ/src:$PROJ"

python3 src/agents/train_dqn.py \
    --scenario "$SCENARIO" \
    --timesteps "$TIMESTEPS" \
    --seed "$SEED" \
    --port 5557 \
    --verbose 1 \
    2>&1

echo "TRAINING_DONE"
