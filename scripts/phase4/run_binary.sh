#!/usr/bin/env bash
# Run built binary with --PrintHelp
set -e
NS3_DIR="$HOME/ns-allinone-3.40/ns-3.40"

echo "=== Find binary ==="
find "$NS3_DIR/build/scratch/congestion-env" -type f 2>/dev/null

echo ""
echo "=== Run PrintHelp ==="
BINARY=$(find "$NS3_DIR/build/scratch/congestion-env" -type f -name "ns3*" 2>/dev/null | head -1)
if [ -z "$BINARY" ]; then
    # Try without subdirectory
    BINARY=$(find "$NS3_DIR/build/scratch" -name "ns3*congestion*" -type f 2>/dev/null | head -1)
fi

if [ -n "$BINARY" ]; then
    echo "Binary: $BINARY"
    "$BINARY" --PrintHelp 2>&1 | head -30
else
    echo "Looking in build/scratch..."
    ls "$NS3_DIR/build/scratch/"
    ls "$NS3_DIR/build/scratch/congestion-env/" 2>/dev/null || echo "No subdirectory"
fi

echo "BINARY_CHECK_DONE"
