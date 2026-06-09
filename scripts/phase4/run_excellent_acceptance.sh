#!/usr/bin/env bash
# Phase 4 Excellent Acceptance: S2 DQN Training + Figure Generation
# Run inside WSL2 Ubuntu from project root
set -e

PROJECT_ROOT="/mnt/c/Users/donuop/Documents/grassland/ns3-drl-congestion-control"
cd "$PROJECT_ROOT"

export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
export PYTHONPATH="$PROJECT_ROOT/src:$PYTHONPATH"

echo "===================================================="
echo "  Phase 4 Excellent Acceptance Upgrade (WSL2)"
echo "===================================================="
echo "  Project: $PROJECT_ROOT"
echo "  Python: $(python3 --version)"
echo ""

# Quick env check
echo "Checking dependencies..."
python3 -c "from gym_env.ns3_congestion_env import HAS_NS3GYM; print('HAS_NS3GYM=' + str(HAS_NS3GYM))"
python3 -c "import stable_baselines3; print('SB3=' + stable_baselines3.__version__)"
python3 -c "import matplotlib; print('matplotlib=' + matplotlib.__version__)"

echo ""
echo "Starting excellent_acceptance_upgrade.py..."
echo "  (S2 training ~18 min, seed sensitivity after)"
echo ""

# Run upgrade: S2 training + eval + seed sens + all figures
python3 scripts/phase4/excellent_acceptance_upgrade.py \
    --s2-timesteps 30000 \
    --s2-seed 42 \
    --s2-port 5558 \
    --eval-port 5560 \
    --sens-port 5570 \
    --sens-seeds 42 43 44 \
    2>&1 | tee /tmp/excellent_acceptance_upgrade.log

echo ""
echo "Upgrade complete. Log: /tmp/excellent_acceptance_upgrade.log"
