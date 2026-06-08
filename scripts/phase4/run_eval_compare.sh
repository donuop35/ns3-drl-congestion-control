#!/usr/bin/env bash
# Phase 4 Step 5+6: Eval DQN S1 then compare with baseline
set -e

PROJ="/mnt/c/Users/donuop/Documents/grassland/ns3-drl-congestion-control"
MODEL="$PROJ/experiments/drl/models/dqn_s1_seed42.zip"

echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Phase 4 Step 5: DQN Evaluation (S1, deterministic)     ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo "  Model: $MODEL"

[ -f "$MODEL" ] || { echo "ERROR: model not found!"; exit 1; }

cd "$PROJ"
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
export PYTHONPATH="$PROJ/src:$PROJ"

echo ""
echo "=== Step 5: Evaluate S1 (5 episodes, deterministic) ==="
python3 src/agents/eval_dqn.py \
    --model "$MODEL" \
    --scenario S1 \
    --episodes 5 \
    --seed 42 \
    --port 5558 \
    --verbose \
    2>&1

echo ""
echo "=== Step 6: Generate DQN vs Baseline comparison ==="
python3 src/analysis/compare_dqn_baseline.py \
    --scenarios S1 \
    2>&1

echo "EVAL_COMPARE_DONE"
