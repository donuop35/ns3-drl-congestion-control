#!/usr/bin/env bash
# Phase 4 Step 1: Setup ns3-gym as contrib/opengym for ns-3.40
set -e

NS3_DIR="$HOME/ns-allinone-3.40/ns-3.40"
CONTRIB_DIR="${NS3_DIR}/contrib/opengym"

echo "=== [Step A] Clone ns3-gym ==="
if [ -d "$HOME/ns3-gym-src" ]; then
    echo "Already exists at ~/ns3-gym-src"
else
    git clone --depth=1 https://github.com/tkn-tub/ns3-gym.git "$HOME/ns3-gym-src"
fi
cd "$HOME/ns3-gym-src"
NS3GYM_COMMIT=$(git rev-parse HEAD)
echo "commit: $NS3GYM_COMMIT"

echo ""
echo "=== [Step B] Copy to contrib/opengym ==="
if [ -d "$CONTRIB_DIR" ]; then
    echo "Already installed at $CONTRIB_DIR"
else
    cp -r "$HOME/ns3-gym-src" "$CONTRIB_DIR"
    echo "Copied OK"
fi
echo "Contents of contrib/opengym:"
ls "$CONTRIB_DIR" | head -10

echo ""
echo "=== [Step C] Check deps ==="
pkg-config --modversion libzmq && echo "libzmq: OK" || echo "libzmq: NOT FOUND"
python3 -m zmq --version 2>/dev/null || python3 -c "import zmq; print('zmq version:', zmq.__version__)"
protoc --version 2>/dev/null || echo "protoc: checking..."
dpkg -l libprotobuf-dev 2>/dev/null | grep "^ii" | awk '{print "libprotobuf-dev:", $3}' || echo "libprotobuf-dev: check dpkg"

echo ""
echo "PREP_COMPLETE"
