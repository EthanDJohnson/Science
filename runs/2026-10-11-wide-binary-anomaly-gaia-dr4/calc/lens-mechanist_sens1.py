#!/usr/bin/env python3
"""Sensitivity of each family's Newtonian bias (truth gamma = 1, f_triple = 0.2) to eccentricity
truth/template mismatch and mass bias. n_test = 6e4, n_cal = 4e4. Bin log10 g_N in [-11, -9.5] m s^-2."""
import importlib.util, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("inj", os.path.join(HERE, "lens-mechanist_injection.py"))
inj = importlib.util.module_from_spec(spec); spec.loader.exec_module(inj)
t0 = time.time()
cases = [
    ("baseline htz truth, alpha_e=1.3 template", {}),
    ("truth thermal (alpha=1), template 1.3", dict(ecc="thermal")),
    ("truth uniform e, template 1.3", dict(ecc="uniform")),
    ("truth htz, template thermal (1.0)", dict(tmpl_alpha=1.0)),
    ("mass_bias 0.9 in BOTH zones", dict(mass_bias=0.9)),
    ("mass_bias 0.9 in LOW zone only (separation-dependent)", dict(mass_bias=1.0, mass_bias_low=0.9)),
]
for lab, kw in cases:
    o = inj.run_case(0.2, 1.0, n_test=60000, n_cal=40000, seed=77, **kw)
    inj.fmt(o, "[Newton f_trip=0.2] " + lab)
print(f"elapsed {time.time() - t0:.1f} s")
