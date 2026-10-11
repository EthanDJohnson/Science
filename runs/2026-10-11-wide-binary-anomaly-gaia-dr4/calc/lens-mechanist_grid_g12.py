#!/usr/bin/env python3
"""Injection-recovery grid row: gamma_inj = 1.2, f_triple in {0, 0.1, 0.2, 0.3}; n_test = 1e5, n_cal = 6e4.
Scoring bin log10 g_N in [-11, -9.5] (g_N in m s^-2). See lens-mechanist_injection.py for the design."""
import importlib.util, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("inj", os.path.join(HERE, "lens-mechanist_injection.py"))
inj = importlib.util.module_from_spec(spec); spec.loader.exec_module(inj)
t0 = time.time()
g = 1.2
for f in (0.0, 0.1, 0.2, 0.3):
    o = inj.run_case(f, g, seed=int(100 * f + 10 * g))
    inj.fmt(o, f"f_triple={f:.1f} gamma_inj={g:.1f}")
print(f"elapsed {time.time() - t0:.1f} s")
