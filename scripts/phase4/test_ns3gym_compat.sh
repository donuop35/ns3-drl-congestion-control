#!/usr/bin/env bash
# Fix ns3gym protobuf compatibility: use pure Python implementation
set -e

SITE_PKG=$(python3 -m site --user-site)
NS3GYM_SRC="$HOME/ns3-gym-src"

echo "=== [1] Re-generate messages_pb2.py with newer protoc ==="
cd "$NS3GYM_SRC/model/ns3gym/ns3gym"
# Use PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python workaround
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

echo ""
echo "=== [2] Test with env var ==="
PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python python3 -c "
import ns3gym
print('ns3gym: OK')
from ns3gym import ns3env
print('ns3env: OK')
e = ns3env.Ns3Env.__doc__
print('Ns3Env available')
"

echo ""
echo "=== [3] Fix ns3env.py: patch ns3gym.Ns3Env to be standalone ==="
# Check ns3env.py for gym vs gymnasium
head -30 "$NS3GYM_SRC/model/ns3gym/ns3gym/ns3env.py"

echo "COMPAT_CHECK_DONE"
