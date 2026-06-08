#!/usr/bin/env bash
# Fix ns3gym: generate protobuf, patch gym→gymnasium, install
set -e

NS3GYM_SRC="$HOME/ns3-gym-src"
NS3_DIR="$HOME/ns-allinone-3.40/ns-3.40"
SITE_PKG=$(python3 -m site --user-site)

echo "=== [1] Generate messages_pb2.py from protobuf ==="
cd "$NS3GYM_SRC/model/ns3gym/ns3gym"
PROTO_SRC="$NS3GYM_SRC/model/messages.proto"
if [ -f "$PROTO_SRC" ]; then
    protoc --proto_path="$NS3GYM_SRC/model" --python_out=. "$PROTO_SRC"
    echo "Generated messages_pb2.py"
    ls messages_pb2.py
else
    echo "WARN: messages.proto not found at $PROTO_SRC"
    find "$NS3GYM_SRC" -name "*.proto" | head -3
fi

echo ""
echo "=== [2] Fix ns3gym __init__.py: gym → gymnasium ==="
cd "$NS3GYM_SRC/model/ns3gym"

# Check original __init__.py
echo "Original __init__.py:"
cat ns3gym/__init__.py

# Patch: replace 'gym.envs.registration' with gymnasium equivalent
sed -i 's/from gym.envs.registration import register/try:\n    from gymnasium.envs.registration import register\nexcept ImportError:\n    from gym.envs.registration import register/' ns3gym/__init__.py 2>/dev/null || true

# Also patch ns3env.py which uses gym.Env
if grep -q "import gym" ns3gym/ns3env.py 2>/dev/null; then
    echo "Patching ns3env.py to use gymnasium..."
    sed -i 's/import gym$/import gymnasium as gym\ntry:\n    import gym\nexcept ImportError:\n    import gymnasium as gym/' ns3gym/ns3env.py || true
fi

echo ""
echo "=== [3] Direct copy patched ns3gym to site-packages ==="
cp -r "$NS3GYM_SRC/model/ns3gym/ns3gym" "$SITE_PKG/"
echo "Copied ns3gym to $SITE_PKG"
ls "$SITE_PKG/ns3gym/"

echo ""
echo "=== [4] Also install gym compatibility shim ==="
pip3 install --user gym 2>&1 | tail -5 || echo "gym install info above"

echo ""
echo "=== [5] Verify import ==="
python3 -c "import ns3gym; print('ns3gym import: OK')" || echo "ns3gym import still failing"
python3 -c "from ns3gym import ns3env; print('ns3env: OK')" || echo "ns3env import failing"

echo "NSGY_FIX_COMPLETE"
