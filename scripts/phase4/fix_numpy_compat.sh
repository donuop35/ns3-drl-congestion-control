#!/usr/bin/env bash
# Fix np.float deprecated alias in ns3gym ns3env.py
set -e

NS3ENV="$HOME/.local/lib/python3.8/site-packages/ns3gym/ns3env.py"
NS3ENV_SRC="$HOME/ns3-gym-src/model/ns3gym/ns3gym/ns3env.py"

echo "=== Fix np.float → float in ns3env.py ==="

# Fix np.float in both locations
for f in "$NS3ENV" "$NS3ENV_SRC"; do
    if [ -f "$f" ]; then
        echo "Patching: $f"
        sed -i 's/np\.float\b/float/g' "$f"
        sed -i 's/np\.int\b/int/g' "$f"
        sed -i 's/np\.bool\b/bool/g' "$f"
        sed -i 's/np\.complex\b/complex/g' "$f"
        echo "Done."
    fi
done

echo ""
echo "=== Verify: grep remaining np.float occurrences ==="
grep -n 'np\.float\b' "$NS3ENV" 2>/dev/null || echo "No remaining np.float in site-packages ns3env.py"
grep -n 'np\.int\b' "$NS3ENV" 2>/dev/null || echo "No remaining np.int"

echo ""
echo "=== Quick import test ==="
python3 -c "
import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
from ns3gym import ns3env
print('ns3env import: OK')
import inspect
sig = inspect.signature(ns3env.Ns3Env.__init__)
print('Ns3Env signature:', sig)
print('FIX_DONE')
"

echo "NUMPY_FIX_DONE"
