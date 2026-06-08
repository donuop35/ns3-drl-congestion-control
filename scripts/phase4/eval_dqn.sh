#!/usr/bin/env bash
# Phase 4: DQN evaluation runner
set -e
PROJ="/mnt/c/Users/donuop/Documents/grassland/ns3-drl-congestion-control"
cd "$PROJ"
MODEL="${1:-experiments/drl/models/dqn_s1_seed42.zip}"
SCENARIO="${2:-S1}"
echo "[eval_dqn.sh] Evaluating DQN: model=$MODEL scenario=$SCENARIO"
python3 src/agents/eval_dqn.py \
    --model "$MODEL" \
    --scenario "$SCENARIO" \
    --episodes 5 \
    --seed 42 \
    "$@"
