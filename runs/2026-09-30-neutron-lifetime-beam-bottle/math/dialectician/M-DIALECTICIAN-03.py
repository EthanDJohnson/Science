"""M-DIALECTICIAN-03: <m_e/E_e> over the neutron beta spectrum, dGamma/dW ∝ F(1,W) p W (W0 - W)^2,
W = E_e/m_e (total energy), p = sqrt(W^2 - 1), no recoil-order terms. Also the phase-space integral f.
Units: natural (m_e = 1); inputs in MeV."""
import sys
import mpmath as mp
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/dialectician")
from _common import *  # noqa

mp.mp.dps = 25
mn, mpr, me = mp.mpf("939.56542052"), mp.mpf("938.27208816"), mp.mpf("0.51099895")
alpha = 1 / mp.mpf("137.035999084")
W0_norecoil = (mn - mpr) / me
W0_recoil = (mn**2 - mpr**2 + me**2) / (2 * mn * me)
hbarc = mp.mpf("197.3269804")  # MeV fm
R = mp.mpf("0.8409") / hbarc * me  # proton charge radius in 1/m_e units (sensitivity is tiny)


def F_rel(W):
    p = mp.sqrt(W**2 - 1); eta = alpha * W / p; g = mp.sqrt(1 - alpha**2)
    return 2 * (1 + g) * (2 * p * R) ** (2 * (g - 1)) * mp.exp(mp.pi * eta) * abs(mp.gamma(g + 1j * eta)) ** 2 / mp.gamma(2 * g + 1) ** 2


def F_nr(W):
    p = mp.sqrt(W**2 - 1); y = 2 * mp.pi * alpha * W / p
    return y / (1 - mp.exp(-y))


def avg(F, W0):
    w = lambda W: F(W) * mp.sqrt(W**2 - 1) * W * (W0 - W) ** 2
    num_ = mp.quad(lambda W: w(W) / W, [1, W0]); den = mp.quad(w, [1, W0])
    return num_ / den, den


res = {}
for Wname, W0 in [("no recoil", W0_norecoil), ("recoil endpoint", W0_recoil)]:
    for Fname, F in [("rel Fermi", F_rel), ("nonrel Fermi", F_nr), ("no Fermi", lambda W: 1)]:
        a, f = avg(F, W0)
        res[(Wname, Fname)] = (a, f)
        print(f"W0 = {float(W0):.5f} ({Wname}), {Fname}: <m_e/E_e> = {float(a):.5f}, f = {float(f):.5f}")

num("<m/E>, Fermi on (rel, recoil endpoint)", res[("recoil endpoint", "rel Fermi")][0], 0.6553, unit="", abs_tol=0.0006)
num("<m/E>, Fermi off (recoil endpoint)", res[("recoil endpoint", "no Fermi")][0], 0.6540, unit="", abs_tol=0.0006)
# Limit check: with no Fermi function, the average must tend to 1 as W0 -> 1 (electron at rest)
aa, _ = avg(lambda W: 1, mp.mpf("1.0001"))
print(f"W0 -> 1 limit: <1/W> = {float(aa):.6f}")
num("W0->1 limit", aa, 1.0, unit="", abs_tol=1e-3)
# closed-form check: no-Fermi integrand; exact symbolic ratio at W0 = 2.5287 vs quadrature
import sympy as sp
Ws = sp.symbols("W", positive=True); W0s = sp.Rational(25287, 10000)
nsym = sp.integrate(sp.sqrt(Ws**2 - 1) * (W0s - Ws) ** 2, (Ws, 1, W0s))
dsym = sp.integrate(sp.sqrt(Ws**2 - 1) * Ws * (W0s - Ws) ** 2, (Ws, 1, W0s))
a_sym = float(nsym / dsym)
a_q, _ = avg(lambda W: 1, mp.mpf("2.5287"))
print(f"symbolic no-Fermi <1/W> at W0=2.5287: {a_sym:.6f}; quadrature {float(a_q):.6f}")
num("symbolic vs quadrature", a_q, a_sym, unit="", rel_tol=1e-8)
units("0.511 MeV / (1.0 MeV)", "dimensionless")
raise SystemExit(finish())
