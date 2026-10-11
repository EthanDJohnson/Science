#!/usr/bin/env python3
"""Timing / smoke test of lens-mechanist_injection.run_case (Newtonian truth, f_triple = 0.2, small N)."""
import importlib.util
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("inj", os.path.join(HERE, "lens-mechanist_injection.py"))
inj = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inj)

t0 = time.time()
o = inj.run_case(0.2, 1.0, n_test=30000, n_cal=20000)
inj.fmt(o, "quick f_triple=0.2 gamma_inj=1.0 (n_test=3e4)")
print(f"elapsed {time.time() - t0:.1f} s")
