#!/usr/bin/env bash
# =============================================================================
# Phase 3: ns-3.40 Build Dependency Installer
# Project: DRL for Congestion Control (ns3-drl-congestion-control)
# Change 02: ns3-baseline-benchmark
# =============================================================================
# IMPORTANT: This script ONLY installs ns-3.40 dependencies.
#   - NO ns3-gym installation
#   - NO DQN training
#   - NO PPO
#   - Only baseline benchmark prerequisites

set -e

NS3_VERSION="3.40"
NS3_DIR="$HOME/ns-allinone-3.${NS3_VERSION}"

echo "=== Phase 3: Step A — Toolchain Installation ==="
echo "ns-3 target version: ${NS3_VERSION}"
echo "Build dir: ${NS3_DIR}"
echo ""

echo "[1/5] Updating package lists..."
sudo apt-get update -y

echo "[2/5] Installing ns-3.40 build dependencies..."
sudo apt-get install -y \
    gcc g++ python3 python3-dev \
    cmake build-essential \
    pkg-config \
    libgsl-dev \
    libgtk2.0-dev \
    libsqlite3-dev \
    libxml2 libxml2-dev \
    libboost-all-dev \
    git wget curl \
    python3-pip \
    python3-setuptools \
    mercurial \
    ninja-build \
    ccache

echo "[3/5] Installing Python ns-3 dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install cppyy 2>/dev/null || echo "cppyy optional, skipping"

echo "[4/5] Verifying key tools..."
echo -n "  gcc: "; gcc --version | head -1
echo -n "  g++: "; g++ --version | head -1
echo -n "  cmake: "; cmake --version | head -1
echo -n "  python3: "; python3 --version
echo -n "  ninja: "; ninja --version 2>/dev/null || echo "not found (using waf instead)"

echo "[5/5] Done. Dependencies installed."
echo ""
echo "Next: Run ns3_download_build.sh to download and build ns-3.${NS3_VERSION}"
