#!/usr/bin/env bash
# Final fix: patch ns3env.py fully for gymnasium + add env var permanently
set -e

NS3GYM_PY="$HOME/ns3-gym-src/model/ns3gym/ns3gym"
SITE_NS3GYM="$HOME/.local/lib/python3.8/site-packages/ns3gym"

echo "=== Patch ns3env.py: gym → gymnasium ==="
# Replace all gym imports with gymnasium
sed -i \
    -e 's/^import gymnasium as gym$/import gymnasium as gym/' \
    -e 's/^try:$//' \
    -e 's/^    import gym$//' \
    -e 's/^except ImportError:$//' \
    -e 's/^    import gymnasium as gym$//' \
    -e 's/^from gym import spaces$/from gymnasium import spaces/' \
    -e 's/^from gym.utils import seeding$/try:\n    from gymnasium.utils import seeding\nexcept ImportError:\n    pass/' \
    "$NS3GYM_PY/ns3env.py"

# Also patch class definition: gym.Env → gymnasium.Env
sed -i 's/gym\.Env/gymnasium.Env/g' "$NS3GYM_PY/ns3env.py"

# Check patched file
echo "Patched imports:"
head -20 "$NS3GYM_PY/ns3env.py"

echo ""
echo "=== Recopy patched files to site-packages ==="
cp -r "$NS3GYM_PY" "$HOME/.local/lib/python3.8/site-packages/"
echo "Copied OK"

echo ""
echo "=== Create pth file for PROTOCOL_BUFFERS env var ==="
# Add env var to Python path via sitecustomize
SITE_PKG=$(python3 -m site --user-site)
cat > "$SITE_PKG/ns3gym_protobuf_fix.pth" << 'EOF'
import os; os.environ.setdefault('PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION', 'python')
EOF
echo "Created pth: $SITE_PKG/ns3gym_protobuf_fix.pth"

echo ""
echo "=== Final test ==="
python3 -c "
import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
import ns3gym
from ns3gym import ns3env
print('ns3gym OK')
print('Ns3Env:', ns3env.Ns3Env)
import gymnasium
print('gymnasium:', gymnasium.__version__)
print('All imports OK')
"

echo "FULL_FIX_COMPLETE"
