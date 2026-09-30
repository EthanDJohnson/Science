"""Constraints lens: Van Den Broeck (1999) pocket -- region II energy, the neck, NEC, QI. Geometric units (G = c = 1,
metres) with SI conversions.

Region II (R~ <= r < R~ + D~): f = 1, so in comoving coordinates xi = x - v t the metric is ultrastatic,
ds^2 = -dt^2 + B(r)^2 (dxi^2 + dy^2 + dz^2), independent of v. Then K_ij = 0, Eulerian rho = 3R/(16 pi) with
3R = -4 lap(B)/B^3 + 2 |grad B|^2/B^4 (conformally flat), and E_II = int rho B^3 4 pi r^2 dr.
Profile (Van Den Broeck 1999, as we recall it; tested below against the dossier's E_II numbers):
  B = 1 + alpha (-(n-1) w^n + n w^(n-1)),  w = (R~ + D~ - r)/D~,  alpha = 1e17, R~ = D~ = 1e-15 m.
Area radius A(r) = B r: a minimum of A outside the pocket is a throat (flare-out) => radial NEC violation in an
ultrastatic metric (rho + p_r = 3R_rr/(8 pi) < 0 there).
Region IV: Alcubierre wall of radius R = 3e-15 m at the QI-limited thickness Delta = 97.7 v L_P (alpha_QI = 0.1).
"""
import math
import sys

import mpmath as mp
import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from gr_tensors import Spacetime, metrics, to_si, PLANCK_LENGTH, qi  # noqa: E402

mp.mp.dps = 60
MSUN, MJ = 1.989e30, 1.898e27
KG_PER_M = to_si.mass_kg(1.0)


def region2(alpha, Rt, Dt, n, npts):
    alpha, Rt, Dt = mp.mpf(alpha), mp.mpf(Rt), mp.mpf(Dt)

    def B(r):
        w = (Rt + Dt - r) / Dt
        return 1 + alpha * (-(n - 1) * w**n + n * w ** (n - 1))

    def dB(r):  # dB/dr = -(1/Dt) dB/dw
        w = (Rt + Dt - r) / Dt
        return -(alpha / Dt) * n * (n - 1) * (w ** (n - 2) - w ** (n - 1))

    def d2B(r):
        w = (Rt + Dt - r) / Dt
        return (alpha / Dt**2) * n * (n - 1) * ((n - 2) * w ** (n - 3) - (n - 1) * w ** (n - 2))

    def rho(r):
        b, b1, b2 = B(r), dB(r), d2B(r)
        lap = b2 + 2 * b1 / r
        return (-4 * lap / b**3 + 2 * b1**2 / b**4) / (16 * mp.pi)

    def radial_ricci(r):  # 3R_(rr) orthonormal, conformally flat h = e^{2 om} delta, om = ln B
        b, b1, b2 = B(r), dB(r), d2B(r)
        om1 = b1 / b
        om2 = b2 / b - om1**2
        # R_ij = -(n-2)(om_ij - om_i om_j) - (lap om + (n-2)|grad om|^2) delta_ij, n = 3
        lap_om = om2 + 2 * om1 / r
        R_rr = -(om2 - om1**2) - (lap_om + om1**2)
        return R_rr / b**2

    rs = [Rt + Dt * mp.mpf(i + 0.5) / npts for i in range(npts)]
    h = Dt / npts
    neg = pos = mp.mpf(0)
    rmin_rho, min_rho, min_rrr, thr = None, mp.mpf(0), mp.mpf(0), None
    Aprev = None
    for r in rs:
        val = rho(r) * B(r) ** 3 * 4 * mp.pi * r**2 * h
        if val < 0:
            neg += val
        else:
            pos += val
        rv = rho(r)
        if rv < min_rho:
            min_rho, rmin_rho = rv, r
        rr_ = radial_ricci(r)
        if rr_ < min_rrr:
            min_rrr = rr_
        A = B(r) * r
        if Aprev is not None and thr is None and A > Aprev:
            thr = (r, A)
        Aprev = A
    return neg, pos, min_rho, rmin_rho, min_rrr, thr, B


print("=== Toolkit cross-check of the 1D region-II formula (alpha = 3, n = 4, R~ = D~ = 1, f = 1) ===")
st, s = metrics.van_den_broeck()
rr = sp.symbols("r", positive=True)
a_, n_ = 3, 4
w = (2 - rr) / 1
Bexpr = sp.Piecewise((1 + a_, rr < 1), (1 + a_ * (-(n_ - 1) * w**n_ + n_ * w ** (n_ - 1)), rr < 2), (1, True))
funcs = {s["f"]: sp.Lambda(rr, 1), s["B"]: sp.Lambda(rr, Bexpr)}
rho_sym = st.energy_density()
for n in (96, 144):
    parts = st.integrate_parts(rho_sym, 0.0, [(-2.2, 2.2)] * 3, n=n, params={s["v"]: 10.0}, functions=funcs)
    print(f"toolkit n={n}: E_neg {parts['negative']:+.5f}  E_pos {parts['positive']:+.5f}  total {parts['total']:+.5f} (m)")
neg, pos, *_ = region2(a_, 1, 1, n_, 4000)
print(f"1D mpmath:    E_neg {float(neg):+.5f}  E_pos {float(pos):+.5f}  total {float(neg+pos):+.5f} (m)")
# analytic: total = (1/2pi) int |grad psi|^2 d^3x with psi = sqrt(B) (boundary terms vanish) -> must be > 0

print("\n=== Van Den Broeck parameters: alpha = 1e17, R~ = D~ = 1e-15 m ===")
for n in (80,):
    for npts in (20000, 30000):
        neg, pos, min_rho, rmin, min_rrr, thr, B = region2(1e17, 1e-15, 1e-15, n, npts)
        print(f"n={n} npts={npts}: E_II- = {float(neg):.4e} m = {float(neg)*KG_PER_M:.3e} kg ({float(neg)*KG_PER_M/MSUN:.3f} Msun);"
              f" E_II+ = {float(pos)*KG_PER_M:.3e} kg ({float(pos)*KG_PER_M/MSUN:.3f} Msun); net {float(neg+pos)*KG_PER_M:.3e} kg")
    print(f"  pocket proper radius = alpha R~ = {1e17*1e-15:.0f} m ; min Eulerian rho = {float(min_rho):.3e} /m^2 = {float(min_rho)*KG_PER_M:.3e} kg/m^3 at r = {float(rmin):.6e} m")
    if thr:
        print(f"  throat (minimum of area radius B r) at r = {float(thr[0]):.6e} m, area radius {float(thr[1]):.3e} m = {float(thr[1])/PLANCK_LENGTH:.2e} L_P")
    print(f"  min 3R_(rr) (orthonormal) = {float(min_rrr):.3e} /m^2 -> rho + p_r = 3R_rr/(8 pi) = {float(min_rrr)/(8*math.pi):.3e} /m^2 < 0 : radial NEC violated")
    # curvature radius estimate and QI at the most negative point
    rc = 1 / math.sqrt(abs(float(min_rrr)))
    for aq in (0.1,):
        bound = qi.ford_roman_geometric(aq * rc)
        print(f"  curvature radius ~ 1/sqrt|3R_rr| = {rc:.3e} m = {rc/PLANCK_LENGTH:.2e} L_P ; FR bound at tau0 = {aq} r_c: {bound:.3e} /m^2 = {bound*KG_PER_M:.3e} kg/m^3 vs |rho_min| {abs(float(min_rho))*KG_PER_M:.3e} kg/m^3")

print("\n=== Region IV (outer Alcubierre wall, R = 3e-15 m) ===")
Rout = 3e-15
for v in (1.0, 10.0):
    Dq = 97.7 * v * PLANCK_LENGTH
    E_q = -(v**2) * Rout**2 / (18 * Dq)
    E_thick = -(v**2) * Rout**2 / (18 * 1e-15)
    print(f"v={v}c: QI-limited wall Delta = {Dq:.2e} m -> E_IV = {E_q*KG_PER_M:.3e} kg ({E_q*KG_PER_M/MSUN:.2f} Msun);"
          f" fm-thick wall (Delta = 1e-15 m, QI-violating) -> {E_thick*KG_PER_M:.3e} kg")
