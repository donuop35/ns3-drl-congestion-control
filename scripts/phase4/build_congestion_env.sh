#!/usr/bin/env bash
# Correctly build scratch/congestion-env in ns-3.40 CMake build system
set -e
NS3_DIR="$HOME/ns-allinone-3.40/ns-3.40"
SRC_CC="/mnt/c/Users/donuop/Documents/grassland/ns3-drl-congestion-control/src/ns3/opengym-congestion-env.cc"

echo "=== [1] Copy to ns-3 scratch root (not subdirectory) ==="
# ns-3.40 CMake build: scratch files should be directly in scratch/
# OR in a subdir with CMakeLists.txt
SCRATCH_SUBDIR="$NS3_DIR/scratch/congestion-env"
mkdir -p "$SCRATCH_SUBDIR"

# Copy C++ file
cp "$SRC_CC" "$SCRATCH_SUBDIR/congestion-env.cc"

# Create CMakeLists.txt for the scratch subdir
cat > "$SCRATCH_SUBDIR/CMakeLists.txt" << 'CMEOF'
build_lib_example(
  NAME congestion-env
  SOURCE_FILES congestion-env.cc
  LIBRARIES_TO_LINK
    ${libopengym}
    ${libpoint-to-point}
    ${libapplications}
    ${libflow-monitor}
    ${libinternet}
    ${libnetwork}
    ${libcore}
    ${libtraffic-control}
)
CMEOF

echo "Created scratch/congestion-env/CMakeLists.txt"
cat "$SCRATCH_SUBDIR/CMakeLists.txt"

echo ""
echo "=== [2] Reconfigure ns-3 to pick up new scratch ==="
cd "$NS3_DIR"
./ns3 configure --enable-examples --build-profile=optimized 2>&1 | grep -E "Configuring|Generating|Written|Scratch" | head -5

echo ""
echo "=== [3] Build congestion-env ==="
./ns3 build congestion-env 2>&1 | grep -E "Building|Linking|error:|Finished|FAILED" | tail -15

echo ""
echo "=== [4] Find binary ==="
find build/ -name "ns3*congestion*" -type f 2>/dev/null

echo "BUILD2_DONE"
