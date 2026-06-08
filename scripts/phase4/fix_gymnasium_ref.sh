#!/usr/bin/env bash
# Targeted fix: revert gymnasium.Env to gym.Env (since we aliased gym=gymnasium)
set -e

NS3GYM_SITE="$HOME/.local/lib/python3.8/site-packages/ns3gym"
NS3GYM_SRC="$HOME/ns3-gym-src/model/ns3gym/ns3gym"

echo "=== Fix gymnasium.Env → gym.Env (gym is aliased to gymnasium) ==="
sed -i 's/gymnasium\.Env/gym.Env/g' "$NS3GYM_SITE/ns3env.py"
sed -i 's/gymnasium\.Env/gym.Env/g' "$NS3GYM_SRC/ns3env.py"

# Also check for gymnasium.spaces → spaces (already from gymnasium import spaces)
sed -i 's/gymnasium\.spaces/spaces/g' "$NS3GYM_SITE/ns3env.py"
sed -i 's/gymnasium\.spaces/spaces/g' "$NS3GYM_SRC/ns3env.py"

echo "Fixed."
echo ""
echo "=== Final import test ==="
python3 -c "
import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
import ns3gym
from ns3gym import ns3env
print('ns3gym OK')
print('Ns3Env:', ns3env.Ns3Env)
import gymnasium
print('gymnasium:', gymnasium.__version__)
print('ALL_IMPORTS_OK')
"

echo "FINAL_FIX_DONE"
