"""M-CONSTRAINTS-01: Alcubierre Eulerian slice energy (F1).

Geometric units G = c = 1, lengths in m. ds^2 = -dt^2 + (dx - v f(r) dt)^2 + dy^2 + dz^2 (N = 1,
flat slices). Hamiltonian constraint on flat slices: rho_E = (K^2 - K_ij K^ij)/(16 pi),
K_ij = (d_i b_j + d_j b_i)/2 (sign irrelevant for rho). Own derivation:
rho_E = -(v^2/(32 pi)) (y^2+z^2)/r^2 f'(r)^2, so E = -(v^2/12) int_0^inf f'^2 r^2 dr.
Thin wall tanh profile f = [tanh(s(r+R)) - tanh(s(r-R))]/(2 tanh(sR)), Delta = 2/s:
E -> -v^2 R^2 s/36 = -v^2 R^2/(18 Delta).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
import mpmath as mp
from math_checks import identity, limit, quantity, units, finish

x, y, z, t = sp.symbols("x y z t", real=True)
v = sp.symbols("v", positive=True)
F = sp.Function("F")
r = sp.sqrt(x**2 + y**2 + z**2)
b = [-v * F(r), 0, 0]
X = [x, y, z]
K = sp.Matrix(3, 3, lambda i, j: (sp.diff(b[j], X[i]) + sp.diff(b[i], X[j])) / 2)
rho = (K.trace()**2 - sum(K[i, j]**2 for i in range(3) for j in range(3))) / (16 * sp.pi)
rho_claim = -(v**2 / (32 * sp.pi)) * (y**2 + z**2) / r**2 * sp.diff(F(r), x).subs(x, x) * 0  # placeholder
# compare with explicit profile (Gaussian), to avoid Derivative-of-composite bookkeeping
rr = sp.symbols("rr", positive=True)
prof = sp.exp(-(rr - 2)**2)
rho_p = rho.subs(F(r), prof.subs(rr, r)).doit()
fp = sp.diff(prof, rr).subs(rr, r)
claim = -(v**2 / (32 * sp.pi)) * (y**2 + z**2) / r**2 * fp**2
identity(rho_p, claim, domain={"x": (-3, 3), "y": (-3, 3), "z": (-3, 3), "v": (0.1, 10)})

# Cross-check against the toolkit's 4D Einstein-tensor route at a numeric point (independent of lens scripts)
from gr_tensors import metrics
st, s = metrics.alcubierre()
f = s["f"]
lam = sp.Lambda(rr, sp.exp(-(rr - 2)**2))
u = st.eulerian_observer()
rho4 = st.contract(st.stress_energy(), u)
pt = (0.0, 1.3, 0.7, -0.4)
val4 = st.evaluate(rho4, pt, params={s["v"]: 3}, functions={f: lam})
valc = float(claim.subs({x: 1.3, y: 0.7, z: -0.4, v: 3}))
print("4D route", val4, "own formula", valc)
quantity(f"{val4}", f"{valc}", rel_tol=1e-8)

# Radial integral, own quadrature at high precision
def E(R, s_, vv):
    mp.mp.dps = 30
    fpr = lambda q: mp.diff(lambda w: (mp.tanh(s_ * (w + R)) - mp.tanh(s_ * (w - R))) / (2 * mp.tanh(s_ * R)), q)
    def fprime(q):
        return (s_ * mp.sech(s_ * (q + R))**2 - s_ * mp.sech(s_ * (q - R))**2) / (2 * mp.tanh(s_ * R))
    I = mp.quad(lambda q: fprime(q)**2 * q**2, [0, R - 10 / s_, R, R + 10 / s_, R + 60 / s_ + 10])
    return -(vv**2) / 12 * I

E_pl = E(1, 8, 1)
E_ref = E(100, 2, 10)
print("paper-like E (m) =", E_pl, " reference E (m) =", E_ref)
quantity(f"{float(E_pl)} m", "-0.22334 m", rel_tol=2e-4)
quantity(f"{float(E_ref)} m", "-5.5556e4 m", rel_tol=2e-4)
# closed-form thin-wall limit: E * 18 Delta/(v^2 R^2) -> -1 as Delta/R -> 0
Rs, ss = sp.symbols("R s", positive=True)
ratio = lambda R, s_: float(E(R, s_, 1) * 18 * (2 / s_) / R**2)
print("ratio at R*s = 16, 200, 2000:", ratio(1, 16), ratio(100, 2), ratio(1000, 2))
quantity(f"{ratio(1000, 2)}", "-1", rel_tol=1e-3)
# exact sech^4 integral used in the thin-wall limit: int sech^4 = 4/3
identity(sp.integrate(sp.sech(x)**4, (x, -sp.oo, sp.oo)), sp.Rational(4, 3))
limit("(v**2*R**2/(18*D))*D", "D", 0, "v**2*R**2/18")
# SI conversions: c^4/G per geometric metre of energy; c^2/G per metre of mass
quantity(f"{-float(E_ref)} m * c^4/G", "6.72e48 J", rel_tol=2e-3)
quantity(f"{-float(E_ref)} m * c^2/G", "7.48e31 kg", rel_tol=2e-3)
quantity(f"{-float(E_ref)} m * c^2/G", "37.6 Msun", rel_tol=2e-3)
quantity(f"{-float(E_pl)} m * c^2/G", "3.01e26 kg", rel_tol=2e-3)
units("1 m * c^4/G", "J")
raise SystemExit(finish())
