#!/usr/bin/env bash
# Quick check: find ns3gym and fix PYTHONPATH
echo "=== ns3-gym-src contents ==="
ls ~/ns3-gym-src/ 2>/dev/null || echo "NOT FOUND at ~/ns3-gym-src"

echo ""
echo "=== Looking for ns3gym Python package ==="
find /root /home -name "ns3env.py" 2>/dev/null
find /usr -name "ns3env.py" 2>/dev/null

echo ""
echo "=== pip3 ns3gym ==="
pip3 show ns3gym 2>/dev/null || echo "not installed via pip"
pip3 list | grep -i ns3

echo ""
echo "=== Trying to import with common paths ==="
for path in /root/ns3-gym-src/gym_bridge /root/ns3-gym-src /home/$(whoami)/ns3-gym-src/gym_bridge; do
    if [ -d "$path" ]; then
        result=$(PYTHONPATH="$path:$PYTHONPATH" python3 -c "from ns3gym import ns3env; print('OK: ' + '$path')" 2>&1)
        echo "  $path: $result"
    fi
done

echo ""
echo "=== Current PYTHONPATH ==="
echo $PYTHONPATH

echo "=== Done ==="
