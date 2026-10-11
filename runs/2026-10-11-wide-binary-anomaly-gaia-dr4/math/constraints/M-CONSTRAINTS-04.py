"""M-CONSTRAINTS-04 (F4): projection statistics and physical scales (SI).

Isotropic projection: s/r = sin(psi), cos(psi) ~ U(0,1). <sin psi> = pi/4; median r/s = 2/sqrt(3).
Scales: r = sqrt(G M / g_N), v_c = (G M g_N)^(1/4), M = 1.5 Msun.
Proxy shift: at fixed proxy g_s = GM/s^2 the true g_N = g_s (s/r)^2 = g_s sin^2 psi.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-11-wide-binary-anomaly-gaia-dr4/math/constraints")
import mpmath as mp
from math_checks import identity, quantity, finish
from cklib import ef_state, sphere_boost, q, A0

identity("integrate(sqrt(1 - c**2), (c, 0, 1))", "pi/4")
identity("1/sqrt(1 - (1/2)**2)", "2/sqrt(3)")
q(2 / mp.sqrt(3), 1.155, 1e-3, "median r/s")
quantity("(G*1.5*Msun/(1e-8 m/s^2))^(1/2)", "943 au", rel_tol=2e-3)
quantity("(G*1.5*Msun/(3.16228e-10 m/s^2))^(1/2)", "5304 au", rel_tol=2e-3)
quantity("(G*1.5*Msun/(1e-10 m/s^2))^(1/2)", "9431 au", rel_tol=2e-3)
quantity("(G*1.5*Msun*1e-10 m/s^2)^(1/4)", "376 m/s", rel_tol=2e-3)
quantity("(G*1.5*Msun/(1.3729e-10 m/s^2))^(1/2)", "8050 au", rel_tol=2e-3)
# proxy shift (orientation-only average at fixed s, uniform in cos psi; lens weighting not stated)
mp.mp.dps = 15
gNe = ef_state("simple", mp.mpf("1.785"))[0]
for lgs, want_true, want_proxy in [(-9.5, 1.344, 1.276), (-10.0, 1.4193, 1.4159)]:
    gs = mp.mpf(10) ** lgs / A0
    avg = mp.quad(lambda c: sphere_boost("simple", gs * (1 - c * c), gNe), [0, 0.9, 0.99, 1 - 1e-9])
    print(f"proxy log g = {lgs}: orientation-avg true-r gamma = {float(avg):.4f} (lens {want_true}); at proxy = {float(sphere_boost('simple', gs, gNe)):.4f} (lens {want_proxy})")
    q(avg, want_true, 3e-3, f"true-r average at proxy {lgs}")
raise SystemExit(finish())
