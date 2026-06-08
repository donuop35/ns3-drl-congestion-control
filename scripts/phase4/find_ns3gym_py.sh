#!/usr/bin/env bash
# Find and install ns3gym Python package
set -e

NS3GYM_SRC="$HOME/ns3-gym-src"

echo "=== Finding ns3gym Python package ==="
find "$NS3GYM_SRC" -name "setup.py" -o -name "pyproject.toml" 2>/dev/null
find "$NS3GYM_SRC" -name "*.py" | head -20

echo ""
echo "=== Repo root contents ==="
ls "$NS3GYM_SRC"

echo ""
echo "=== Check if ns3gym is just the Python client in examples ==="
find "$NS3GYM_SRC" -name "ns3gym" -type d 2>/dev/null
find "$NS3GYM_SRC" -name "*.py" -path "*ns3gym*" 2>/dev/null | head -10
