#!/usr/bin/env bash
# Phase 4: DQN training runner
set -e
PROJ="/mnt/c/Users/donuop/Documents/grassland/ns3-drl-congestion-control"
cd "$PROJ"
SCENARIO="${1:-S1}"
TIMESTEPS="${2:-50000}"
SEED="${3:-42}"
echo "[train_dqn.sh] Training DQN: scenario=$SCENARIO timesteps=$TIMESTEPS seed=$SEED"
python3 src/agents/train_dqn.py \
    --scenario "$SCENARIO" \
    --timesteps "$TIMESTEPS" \
    --seed "$SEED" \
    --verbose 1 \
    "$@"
