#!/usr/bin/env bash
# Install ns3gym Python package and run smoke test
set -e

echo "=== [1] Install ns3gym Python package ==="
pip3 install --user ~/ns3-gym-src/model/ns3gym/ 2>&1 | tail -5

echo ""
echo "=== [2] Verify import ==="
python3 -c "import ns3gym; print('ns3gym OK, version:', getattr(ns3gym, '__version__', 'unknown'))"
python3 -c "from ns3gym import ns3env; print('ns3env: OK')"

echo ""
echo "=== [3] Check ns3gym example (opengym) ==="
ls ~/ns-allinone-3.40/ns-3.40/contrib/opengym/examples/opengym/ 2>/dev/null || echo "No opengym example dir"
ls ~/ns-allinone-3.40/ns-3.40/build/contrib/opengym/examples/ 2>/dev/null | head -5 || echo "Build dir check"
ls ~/ns-allinone-3.40/ns-3.40/build/lib/ | grep opengym || echo "No opengym in build/lib"

echo ""
echo "INSTALL_VERIFY_COMPLETE"
