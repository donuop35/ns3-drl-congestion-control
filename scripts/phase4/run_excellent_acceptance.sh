#!/usr/bin/env bash
# Phase 4 Excellent Acceptance: S2 DQN Training + Figure Generation
# Run inside WSL2 Ubuntu from project root
set -e

PROJECT_ROOT="/mnt/c/Users/donuop/Documents/grassland/ns3-drl-congestion-control"
cd "$PROJECT_ROOT"

# ns3gym installed in donuop .local (since was installed as donuop user)
NS3GYM_PATH="/home/donuop/.local/lib/python3.8/site-packages"

# ns-3 binary built in donuop home (not root home)
NS3_HOME="/home/donuop/ns-allinone-3.40/ns-3.40"
NS3_BIN="$NS3_HOME/build/scratch/congestion-env/ns3.40-congestion-env-optimized"

export NS3_HOME
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
export PYTHONPATH="$NS3GYM_PATH:$PROJECT_ROOT/src:$PYTHONPATH"

echo "===================================================="
echo "  Phase 4 Excellent Acceptance Upgrade (WSL2)"
echo "  Running as: $(whoami)"
echo "===================================================="
echo "  Project: $PROJECT_ROOT"
echo "  NS3_HOME: $NS3_HOME"
echo "  NS3_BIN: $NS3_BIN"
echo "  Python: $(python3 --version)"
echo ""

# Check ns-3 binary exists
if [ ! -f "$NS3_BIN" ]; then
    echo "ERROR: ns-3 binary not found at $NS3_BIN"
    echo "Try: bash scripts/phase4/build_congestion_env.sh"
    echo ""
    echo "Searching for ns-3 binary..."
    find /home/donuop /root -name "ns3.40-congestion-env-optimized" 2>/dev/null || echo "Binary not found"
    exit 1
fi
echo "  ns-3 binary: OK ($NS3_BIN)"

# Quick env check
echo ""
echo "Checking dependencies..."
python3 -c "from ns3gym import ns3env; print('ns3gym OK')" 2>&1 | grep -v "Gym has been"
python3 -c "from gym_env.ns3_congestion_env import HAS_NS3GYM; print('HAS_NS3GYM=' + str(HAS_NS3GYM))" 2>&1 | grep -v "Gym has been"
python3 -c "import stable_baselines3; print('SB3=' + stable_baselines3.__version__)"
python3 -c "import matplotlib; print('matplotlib=' + matplotlib.__version__)"

echo ""
echo "Starting excellent_acceptance_upgrade.py..."
echo "  S2 training: 30k steps (~18 min)"
echo "  Then: seed sensitivity check (3 seeds x 2 scenarios x 3 eps each)"
echo "  Then: figure generation"
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
echo "======================================================="
echo "  Upgrade complete. Log: /tmp/excellent_acceptance_upgrade.log"
echo "======================================================="
