#!/usr/bin/env bash
# Diagnose ns3gym Python install issue
echo "=== ns3gym setup.py ==="
cat ~/ns3-gym-src/model/ns3gym/setup.py

echo ""
echo "=== Try pip install verbose ==="
pip3 install --user ~/ns3-gym-src/model/ns3gym/ -v 2>&1 | grep -E "error|Error|FAIL|Running|Building|Collected" | head -30

echo ""
echo "=== Try direct path install ==="
pip3 install --user "file:///home/donuop/ns3-gym-src/model/ns3gym" 2>&1 | tail -10

echo ""
echo "=== Fallback: manual copy to site-packages ==="
SITE_PKG=$(python3 -m site --user-site)
echo "site-packages: $SITE_PKG"
mkdir -p "$SITE_PKG"
# Just copy the ns3gym module directly
cp -r ~/ns3-gym-src/model/ns3gym/ns3gym "$SITE_PKG/"
echo "Copied ns3gym to $SITE_PKG"

echo ""
echo "=== Verify import ==="
python3 -c "import ns3gym; print('ns3gym import: OK'); from ns3gym import ns3env; print('ns3env: OK')"
