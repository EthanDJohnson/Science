#!/usr/bin/env python3
"""Sensitivity of each family's Newtonian bias (truth gamma = 1, f_triple = 0.2) to noise
underestimate, unbound comoving pairs, chance alignments, inner-binary period range, and the
RUWE-like cut. n_test = 6e4, n_cal = 4e4. Bin log10 g_N in [-11, -9.5] m s^-2."""
import importlib.util, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("inj", os.path.join(HERE, "lens-mechanist_injection.py"))
inj = importlib.util.module_from_spec(spec); spec.loader.exec_module(inj)
AU = inj.AU
t0 = time.time()
cases = [
    ("true PM noise 1.3x quoted (err_inflate=1.3)", dict(err_inflate=1.3)),
    ("unbound comoving pairs 5% of test zone (sigma 0.5 km/s)", dict(f_unbound=0.05)),
    ("chance alignments 2% (sigma 25 km/s)", dict(f_chance=0.02)),
    ("inner a_in up to 1000 au (longer inner periods)", dict(a_in_range=(0.1 * AU, 1000 * AU))),
    ("no RUWE-like wobble cut", dict(wob_cut=None)),
]
for lab, kw in cases:
    o = inj.run_case(0.2, 1.0, n_test=60000, n_cal=40000, seed=78, **kw)
    inj.fmt(o, "[Newton f_trip=0.2] " + lab)
print(f"elapsed {time.time() - t0:.1f} s")
