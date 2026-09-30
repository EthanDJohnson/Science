"""M-DIALECTICIAN-06: Leggett-Garg K3 with Gaussian clock-reading errors.

Qubit H = Omega sigma_x/2 (hbar = 1), dichotomic Q = sigma_z, projective sequential measurements at true times
t_i + e_i where the clock reads t_i = i tau (i = 1,2,3), e_i iid N(0, sigma^2).
Sharp correlator C(t, t') = cos(Omega (t' - t)) (state independent for this precession).
Claim: K3 = <C12> + <C23> - <C13> = e^{-Omega^2 sigma^2} (2 cos(Omega tau) - cos(2 Omega tau)); max 1.5 e^{-Omega^2 sigma^2};
violation (K3 > 1) lost at Omega sigma = sqrt(ln 1.5) = 0.6368. Ex: Omega sigma = 0.4 -> 1.2782.
GPP clock at T = 1 s for Omega = 2 pi 429 THz: Omega * dT = 3.8e-14.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import math
import numpy as np
import sympy as sp
from math_checks import identity, limit, finish, Result, _done

def report(name, ok, note=""):
    _done(Result("pass" if ok else "fail", name, "numeric", note=note), True)

# (i) sharp two-time correlator from first principles (Luders rule), random initial state
Om = 1.0
sx = np.array([[0, 1], [1, 0]], complex); sz = np.diag([1.0, -1.0]).astype(complex)
def U(t):
    return np.cos(Om * t / 2) * np.eye(2) - 1j * np.sin(Om * t / 2) * sx
P = [np.diag([1, 0]).astype(complex), np.diag([0, 1]).astype(complex)]
rng = np.random.default_rng(7)
v = rng.normal(size=2) + 1j * rng.normal(size=2); v /= np.linalg.norm(v)
rho0 = np.outer(v, v.conj())
def corr(t1, t2):
    tot = 0.0
    for a, qa in ((0, 1), (1, -1)):
        r1 = U(t1) @ rho0 @ U(t1).conj().T
        pa = P[a] @ r1 @ P[a]
        r2 = U(t2 - t1) @ pa @ U(t2 - t1).conj().T
        for b, qb in ((0, 1), (1, -1)):
            tot += qa * qb * np.trace(P[b] @ r2).real
    return tot
err = max(abs(corr(t1, t1 + dt) - math.cos(Om * dt)) for t1 in (0.1, 0.7) for dt in (0.3, 1.1, 2.5))
report("sharp C(t,t') = cos(Omega (t'-t)) for a random state", err < 1e-12, f"max err {err:.1e}")

# (ii) Monte Carlo over clock errors with first-principles correlator
tau = math.pi / 3
for xs in (0.4, 0.8):
    sig = xs / Om
    N = 40000
    e = rng.normal(0, sig, size=(N, 3))
    tt = np.array([1, 2, 3]) * tau + e
    c = lambda i, j: np.cos(Om * (tt[:, j] - tt[:, i]))  # sampled sharp correlator (verified in (i))
    K3 = np.mean(c(0, 1) + c(1, 2) - c(0, 2))
    pred = 1.5 * math.exp(-xs**2)
    report(f"MC K3 at Omega sigma = {xs}", abs(K3 - pred) < 0.01, f"MC {K3:.4f} vs {pred:.4f}")
report("quoted 1.2782 at Omega sigma = 0.4", abs(1.5 * math.exp(-0.16) - 1.2782) < 5e-5, f"{1.5*math.exp(-0.16):.5f}")

# (iii) symbolic: E[cos(Om(Dt + e_j - e_i))] with e_j - e_i ~ N(0, 2 sigma^2)
x = sp.symbols("x", real=True)
Omg, s, dt = sp.symbols("Omega sigma tau", positive=True)
avg = sp.integrate(sp.exp(-x**2 / (4 * s**2)) / (sp.sqrt(4 * sp.pi) * s) * sp.cos(Omg * x), (x, -sp.oo, sp.oo))
identity(avg, sp.exp(-Omg**2 * s**2))
K = 2 * sp.cos(Omg * dt) - sp.cos(2 * Omg * dt)
crit = sp.solve(sp.diff(K.subs(Omg, 1), dt), dt)
kmax = max(float(K.subs(Omg, 1).subs(dt, cr)) for cr in crit if cr.is_real)
report("max over tau of 2cos - cos2 = 1.5", abs(kmax - 1.5) < 1e-12, f"{kmax}; critical points {crit}")
thr = math.sqrt(math.log(1.5))
report("threshold Omega sigma = sqrt(ln 1.5) = 0.6368", abs(thr - 0.6368) < 5e-5, f"{thr:.5f}")
limit(1.5 * sp.exp(-(Omg * s) ** 2), "sigma", 0, "3/2")   # sharp clock recovers the Luders maximum 3/2

# (iv) GPP clock number
hbar, G, c = 1.054571817e-34, 6.67430e-11, 299792458.0
tp = math.sqrt(hbar * G / c**5)
dT = tp ** (2 / 3)
Oopt = 2 * math.pi * 429e12
report("Omega * dT_GPP(1 s) = 3.8e-14 (sigma = dT)", abs(Oopt * dT / 3.8e-14 - 1) < 0.02, f"{Oopt*dT:.3e}; with sigma = sqrt3 dT: {Oopt*dT*math.sqrt(3):.3e}")
raise SystemExit(finish())
