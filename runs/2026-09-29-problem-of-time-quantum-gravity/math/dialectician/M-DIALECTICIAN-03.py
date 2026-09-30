"""M-DIALECTICIAN-03: sharp relational evolution is unitary; Gaussian-blurred clock reading dephases as exp(-sigma^2 Delta^2/2).

Model (hbar = 1): clock H_C = diag(k - (d-1)/2), k = 0..63 (spacing 1 rad/s, d = 64); system H_S = diag(+Delta/2, -Delta/2),
Delta = 3 rad/s, psi0 = |+>. Constraint J = H_C x 1 + 1 x H_S. Clock states |t> = sum_k e^{-i eps_k t}|k> (norm^2 = d).
Sharp: psi(t) = <t|Psi> / norm must equal exp(-i H_S t) psi0 (fidelity 1).
Blurred: rho(t) = int g_sigma(t'-t) psi(t') psi(t')^dag dt' / trace, g Gaussian of std sigma (s).
Claim: |rho_01| = 0.5 exp(-sigma^2 Delta^2 / 2); 0.417635 (sigma = 0.2 s), 0.028067 (sigma = 0.8 s).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from math_checks import identity, limit, units, finish, Result, _done

def report(name, ok, note=""):
    _done(Result("pass" if ok else "fail", name, "numeric (numpy)", note=note), True)

d, Dl = 64, 3.0
eps = np.arange(d) - (d - 1) / 2
ES = np.array([Dl / 2, -Dl / 2])
J = np.add.outer(eps, ES)            # diagonal constraint in product energy basis, shape (d, 2)
psi0 = np.array([1, 1], complex) / np.sqrt(2)
# physical state: keep only resonant pairs eps = -E_s, with amplitudes psi0_s (group average of |t=0> x psi0)
Psi = np.where(np.abs(J) < 1e-12, 1.0, 0.0) * psi0[None, :]
print("resonant pairs:", int(np.sum(np.abs(J) < 1e-12)))

def cond(t):
    tv = np.exp(-1j * eps * t)
    v = tv.conj() @ Psi
    return v

fmin = 1.0
for t in np.linspace(0, 7, 29):
    v = cond(t)
    ref = np.exp(-1j * ES * t) * psi0
    f = abs(np.vdot(ref, v)) ** 2 / np.vdot(v, v).real
    fmin = min(fmin, f)
report("sharp conditional state = exp(-i H_S t) psi0 (fidelity)", 1 - fmin < 1e-12, f"min fidelity {fmin:.12f}")

for sig, quoted in [(0.05, None), (0.2, 0.417635), (0.5, None), (0.8, 0.028067)]:
    t = 1.3
    ts = np.linspace(t - 12 * sig, t + 12 * sig, 20001)
    g = np.exp(-(ts - t) ** 2 / (2 * sig**2))
    rho = np.zeros((2, 2), complex)
    for w, tp in zip(g, ts):
        v = cond(tp)
        rho += w * np.outer(v, v.conj())
    rho /= np.trace(rho)
    pred = 0.5 * np.exp(-sig**2 * Dl**2 / 2)
    note = f"|rho01| = {abs(rho[0,1]):.6f}, predicted {pred:.6f}"
    ok = abs(abs(rho[0, 1]) - pred) < 1e-6
    if quoted is not None:
        ok = ok and abs(pred - quoted) < 1e-6
        note += f", quoted {quoted}"
    report(f"blurred dephasing sigma = {sig} s", ok, note)

# symbolic: Gaussian characteristic function
x = sp.symbols("x", real=True)
s, D = sp.symbols("sigma Delta", positive=True)
cf = sp.integrate(sp.exp(-x**2 / (2 * s**2)) / (sp.sqrt(2 * sp.pi) * s) * sp.cos(D * x), (x, -sp.oo, sp.oo))
identity(cf, sp.exp(-s**2 * D**2 / 2))
limit(sp.exp(-s**2 * D**2 / 2), "sigma", 0, "1")          # sharp clock -> no dephasing (unitary limit)
units("(3 rad/s) * (0.2 s)", "dimensionless")
raise SystemExit(finish())
