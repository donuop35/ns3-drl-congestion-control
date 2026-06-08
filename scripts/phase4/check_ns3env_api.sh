#!/usr/bin/env bash
# Check ns3gym Ns3Env signature to fix simFileName issue
python3 -c "
import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
from ns3gym import ns3env
import inspect
print('Ns3Env.__init__ signature:')
print(inspect.signature(ns3env.Ns3Env.__init__))
print()
print('start_sim_script signature:')
from ns3gym.start_sim import start_sim_script
print(inspect.signature(start_sim_script))
"
