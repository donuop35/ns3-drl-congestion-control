#!/usr/bin/env bash
# Phase 4: Check ZMQ/protobuf/pkg-config status without sudo
python3 -c "import zmq; print('zmq:', zmq.__version__)" 2>/dev/null || echo "zmq: NOT_INSTALLED"
python3 -c "import google.protobuf; print('protobuf:', google.protobuf.__version__)" 2>/dev/null || echo "protobuf: NOT_INSTALLED"
pkg-config --version 2>/dev/null && echo "pkg-config: OK" || echo "pkg-config: NOT_FOUND"
dpkg -l libzmq3-dev 2>/dev/null | grep -c "^ii" | xargs -I{} echo "libzmq3-dev: {} packages"
dpkg -l libprotobuf-dev 2>/dev/null | grep -c "^ii" | xargs -I{} echo "libprotobuf-dev: {} packages"
