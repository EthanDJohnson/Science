#!/usr/bin/env python3
"""Timing probe: how long is one closed-loop run_course on the lens's plant?"""
import os
import sys
import time
from importlib import import_module

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
M = import_module("lens-simulator_model")
from quadrotor import platform_sun2022  # noqa: E402

q = platform_sun2022()
c = M.Slalom(tol=0.2)
ctl = M.Cascade(q)
for U in (10.0, 15.0):
    t0 = time.time()
    r = M.run_course(q, ctl, c, U, dt=2e-3)
    print(f"U={U}: ok={r['ok']} err={r['worst_gate_err']:.4f} mode={r['failure_mode']} "
          f"wall={time.time()-t0:.2f} s")
