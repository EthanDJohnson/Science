"""M-ENGINEER-02 (F5, F10, F13): independent re-implementation of the static 2024 shell
(Fuchs et al. eqs. 19-25 as defined in the run's brief/toolkit description; our own code):
constant density M = 4.49e27 kg on R1 = 10 m .. R2 = 20 m, SI TOV pressure with P(R2) = 0,
4-pass moving-average smoothing of P (span s) and rho (span 1.72 s), metric from the smoothed
profiles, tangential stress from div T = 0:  p_t = p_r + (r/2)(p_r' + (eps + p_r) a').
Lens claims at s = 1 m: lapse at centre 0.761, peak p_r 9.6e38 Pa, p_t in [-1.2e38, 3.9e39] Pa,
peak eps 1.38e40 J/m^3, max(|p|)/eps = 0.60; at s = 0.5 m max = 1.15 (DEC fails); at 2 m 0.32.
Limit: weak field, centre lapse -> 1 + Phi(0)/c^2, Phi(0) = -(3GM/2)(R2^2-R1^2)/(R2^3-R1^3)."""
import sys
import numpy as np
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/math/engineer")
from common import *
from math_checks import finish, units

R1, R2 = 10.0, 20.0


def build(M, span_P, dr=0.002, rmax=60.0, smooth=True, ratio=1.72):
    r = np.arange(0.0, rmax + dr / 2, dr)
    rho0 = 3 * M / (4 * math.pi * (R2**3 - R1**3))
    rho = np.where((r >= R1) & (r <= R2), rho0, 0.0)
    # TOV for P' with the unsmoothed, analytic m'(r); RK4 from R2 inward
    def mprime(x):
        return M * (max(x, R1)**3 - R1**3) / (R2**3 - R1**3)
    def dP(x, P):
        m = mprime(x)
        return -G * (rho0 + P / c**2) * (m + 4 * math.pi * x**3 * P / c**2) / (x**2 * (1 - 2 * G * m / (c**2 * x)))
    P = np.zeros_like(r)
    idx = np.where((r >= R1) & (r <= R2))[0][::-1]
    Pv = 0.0
    P[idx[0]] = 0.0
    for k in range(1, len(idx)):
        x0, x1 = r[idx[k - 1]], r[idx[k]]
        h = x1 - x0
        k1 = dP(x0, Pv); k2 = dP(x0 + h / 2, Pv + h * k1 / 2); k3 = dP(x0 + h / 2, Pv + h * k2 / 2); k4 = dP(x1, Pv + h * k3)
        Pv += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        P[idx[k]] = Pv
    P_R1 = Pv
    if smooth:
        def ma(y, span):
            n = int(round(span / dr))
            n += (n % 2 == 0)
            ker = np.ones(n) / n
            for _ in range(4):
                y = np.convolve(y, ker, mode="same")
            return y
        rho = ma(rho, ratio * span_P)
        P = ma(P, span_P)
    # mass function
    integrand = 4 * math.pi * r**2 * rho
    m = np.concatenate([[0.0], np.cumsum((integrand[1:] + integrand[:-1]) / 2 * dr)])
    Madm = m[-1]
    # a' and a, with a(rmax) = 0.5 ln(1 - 2 G Madm/(c^2 rmax))
    with np.errstate(divide="ignore", invalid="ignore"):
        ap = G * (m / (c**2 * r**2) + 4 * math.pi * r * P / c**4) / (1 - 2 * G * m / (c**2 * r))
    ap[0] = 0.0
    a = np.zeros_like(r)
    a[-1] = 0.5 * math.log(1 - 2 * G * Madm / (c**2 * rmax))
    a[:-1] = a[-1] - np.cumsum(((ap[1:] + ap[:-1]) / 2 * dr)[::-1])[::-1]
    eps = rho * c**2
    pr = P
    dpr = np.gradient(pr, dr)
    pt = pr + (r / 2) * (dpr + (eps + pr) * ap)
    return dict(r=r, eps=eps, pr=pr, pt=pt, lapse0=math.exp(a[0]), Madm=Madm, P_R1=P_R1)


def dec_ratio(s):
    mask = s["eps"] > 1e-6 * s["eps"].max()
    ratio = np.max(np.maximum(np.abs(s["pr"][mask]), np.abs(s["pt"][mask])) / s["eps"][mask])
    # any stress where eps is negligible is a DEC failure
    bad = (~mask) & ((np.abs(s["pr"]) > 1e-3 * s["pr"].max()) | (np.abs(s["pt"]) > 1e-3 * s["pr"].max()))
    return ratio, int(bad.sum())


M = 4.49e27
print("Unsmoothed (sharp) shell:")
s0 = build(M, 1.0, smooth=False)
print(f"  P'(R1) = {s0['P_R1']:.4g} Pa, centre lapse = {s0['lapse0']:.5f}, M_ADM = {s0['Madm']:.5g} kg")
for span in (0.5, 1.0, 2.0):
    for dr in (0.004, 0.002):
        s = build(M, span, dr=dr)
        rr, nbad = dec_ratio(s)
        print(f"span_P = {span} m, dr = {dr} m: lapse0 = {s['lapse0']:.5f}, M_ADM = {s['Madm']:.5g} kg, "
              f"C = {2*G*s['Madm']/(c**2*R2):.4f}, peak eps = {s['eps'].max():.4g}, peak p_r = {s['pr'].max():.4g}, "
              f"p_t in [{s['pt'].min():.4g}, {s['pt'].max():.4g}], max|p|/eps = {rr:.3f}, DEC-bad samples = {nbad}")
s1 = build(M, 1.0)
r1, _ = dec_ratio(s1)
rel("centre lapse, span 1 m", s1["lapse0"], 0.761, 3e-3)
rel("peak p_r, span 1 m (Pa)", s1["pr"].max(), 9.6e38, 0.05)
rel("peak p_t, span 1 m (Pa)", s1["pt"].max(), 3.9e39, 0.10)
rel("min p_t, span 1 m (Pa)", s1["pt"].min(), -1.2e38, 0.25)
rel("peak eps, span 1 m (J/m^3)", s1["eps"].max(), 1.38e40, 0.01)
near("max |p|/eps, span 1 m", r1, 0.60, 0.05)
rh, _ = dec_ratio(build(M, 0.5))
near("max |p|/eps, span 0.5 m", rh, 1.15, 0.10)
inequality(repr(float(rh)), ">", "1")   # DEC fails at 0.5 m
r2, _ = dec_ratio(build(M, 2.0))
near("max |p|/eps, span 2 m", r2, 0.32, 0.05)
# proper-time saving at the centre
near("1 - lapse0 (fractional ageing saving)", 1 - s1["lapse0"], 0.24, 0.01)
# weak-field limit of the centre lapse
Mw = 4.49e20
sw = build(Mw, 1.0, smooth=False)
Phi0 = -1.5 * G * Mw * (R2**2 - R1**2) / (R2**3 - R1**3)
rel("weak-field centre lapse - 1 vs Phi(0)/c^2", sw["lapse0"] - 1, Phi0 / c**2, 1e-3)
units("G*1 kg/(1 m)/c^2", "dimensionless")
units("G*(1 kg/m^3)^2*(1 m)^2", "Pa")
raise SystemExit(finish())
