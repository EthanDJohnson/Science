#!/usr/bin/env python3
"""Constraint audit, facet 4 (global time) and chronology, with gr_tensors.

Units: geometric G = c = 1. In Parts A-C lengths/times are in units of an arbitrary scale L
(scalar mass m in 1/L). Part D converts to SI (Gyr) with Planck-2018-like parameters.

Part A  Hamiltonian constraint of FRW (k = 0, +1) from gr_tensors: the Eulerian density
        rho = 3(adot^2 + k)/(8 pi a^2) is a CONSTRAINT (first order in time), and the
        4D Einstein route gives p = -(2 addot/a + (adot^2+k)/a^2)/(8 pi).
Part B  Minisuperspace trajectories (FRW + scalar field, V = m^2 phi^2/2). Count turning points
        of each candidate internal clock: volume a^3, scalar phi, York time K = -3H,
        unimodular 4-volume T = int a^3 dt (per unit comoving volume), and check energy
        conditions along the trajectory with gr_tensors.classify_stress_energy on the metric's
        own stress-energy. Convergence: RK4 with n and 1.5 n steps.
Part C  Goedel universe: all energy conditions hold, yet closed timelike curves pass through
        every point, so no global time function exists (chronology constraint).
Part D  Closed (k = +1) Lambda-CDM: York time (H) has a minimum at a* = 3 Om/(2|Ok|).
"""
import math
import sys
import time

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from gr_tensors import Spacetime, classify_stress_energy, _orthonormal_frame

t0_clock = time.time()
# ------------------------------------------------------------------ Part A
t, x, y, z = sp.symbols("t x y z", real=True)
k = sp.symbols("k", real=True)
A0, A1, A2 = sp.symbols("A0 A1 A2", real=True)   # a, adot, addot at t = 0
a = sp.Function("a")
r2 = x**2 + y**2 + z**2
Om = 1 / (1 + k * r2 / 4)
h = sp.diag(a(t)**2 * Om**2, a(t)**2 * Om**2, a(t)**2 * Om**2)
st = Spacetime.from_adm(1, [0, 0, 0], h, [t, x, y, z])
rho_adm = st.energy_density()
taylor = {a: sp.Lambda(t, A0 + A1 * t + A2 * t**2 / 2)}
rho_fn = st.compile(rho_adm, functions=taylor, free=[k, A0, A1, A2])
T_fn = st.compile(st.stress_energy(), functions=taylor, free=[k, A0, A1, A2])
g_fn = st.compile(st.g, functions=taylor, free=[k, A0, A1, A2])
u_fn = st.compile(st.eulerian_observer(), functions=taylor, free=[k, A0, A1, A2])
print("Part A: Hamiltonian constraint of FRW from gr_tensors (geometric units)")
rng = np.random.default_rng(1)
maxerr_rho = maxerr_p = 0.0
for _ in range(6):
    kk = float(rng.choice([0.0, 1.0]))
    a0, a1, a2 = 0.5 + rng.random(), rng.normal(), rng.normal()
    pt = (0.0, 0.3 * rng.normal(), 0.3 * rng.normal(), 0.3 * rng.normal())
    rho_num = float(rho_fn(*pt, kk, a0, a1, a2))
    rho_ref = 3 * (a1**2 + kk) / (8 * math.pi * a0**2)
    g = np.array(g_fn(*pt, kk, a0, a1, a2), float).reshape(4, 4)
    T = np.array(T_fn(*pt, kk, a0, a1, a2), float).reshape(4, 4)
    u = np.array(u_fn(*pt, kk, a0, a1, a2), float).reshape(4)
    e = _orthonormal_frame(g, u)
    Tf = e @ T @ e.T
    p_num = Tf[1, 1]
    p_ref = -(2 * a2 / a0 + (a1**2 + kk) / a0**2) / (8 * math.pi)
    maxerr_rho = max(maxerr_rho, abs(rho_num - rho_ref) / abs(rho_ref))
    maxerr_p = max(maxerr_p, abs(p_num - p_ref) / max(1e-12, abs(p_ref)))
print(f"  rho_Eulerian vs 3(adot^2+k)/(8 pi a^2): max rel err {maxerr_rho:.2e}")
print(f"  p (4D Einstein) vs -(2addot/a+(adot^2+k)/a^2)/(8pi): max rel err {maxerr_p:.2e}")
print(f"  (setup {time.time()-t0_clock:.1f} s)")


def ec_on_metric(kk, a0, a1, a2):
    """Energy conditions of the stress-energy the FRW metric requires, via gr_tensors."""
    pt = (0.0, 0.11, -0.07, 0.05)
    g = np.array(g_fn(*pt, kk, a0, a1, a2), float).reshape(4, 4)
    T = np.array(T_fn(*pt, kk, a0, a1, a2), float).reshape(4, 4)
    u = np.array(u_fn(*pt, kk, a0, a1, a2), float).reshape(4)
    e = _orthonormal_frame(g, u)
    return classify_stress_energy(e @ T @ e.T)


# ------------------------------------------------------------------ Part B
def rhs(s, kk, m):
    aa, ad, ph, pd, T4 = s
    V = 0.5 * m**2 * ph**2
    rho, p = 0.5 * pd**2 + V, 0.5 * pd**2 - V
    add = -(4 * math.pi / 3) * (rho + 3 * p) * aa
    H = ad / aa
    return np.array([ad, add, pd, -3 * H * pd - m**2 * ph, aa**3])


def run(kk, m, a_init, ph_init, pd_init, t_end, n):
    V = 0.5 * m**2 * ph_init**2
    rho = 0.5 * pd_init**2 + V
    ad2 = (8 * math.pi / 3) * rho * a_init**2 - kk
    if ad2 < 0:
        raise ValueError("constraint has no real adot")
    s = np.array([a_init, math.sqrt(ad2), ph_init, pd_init, 0.0])
    dt = t_end / n
    out = [np.r_[0.0, s]]
    tt = 0.0
    amax = a_init
    for _ in range(n):
        k1 = rhs(s, kk, m); k2 = rhs(s + dt / 2 * k1, kk, m)
        k3 = rhs(s + dt / 2 * k2, kk, m); k4 = rhs(s + dt * k3, kk, m)
        s = s + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        tt += dt
        out.append(np.r_[tt, s])
        amax = max(amax, s[0])
        if s[0] < 0.3 * amax and s[1] < 0:   # stop well before the crunch (stiff singular region)
            break
    return np.array(out)


def turning_points(v):
    d = np.diff(v)
    d = d[np.abs(d) > 1e-14 * max(1.0, np.abs(v).max())]
    return int(np.sum(np.sign(d[1:]) != np.sign(d[:-1])))


def audit(label, kk, m, a_init, ph_init, pd_init, t_end, n):
    res = {}
    for nn in (n, int(1.5 * n)):
        tr = run(kk, m, a_init, ph_init, pd_init, t_end, nn)
        tt, aa, ad, ph, pd, T4 = tr.T
        H = ad / aa
        V = 0.5 * m**2 * ph**2
        rho = 0.5 * pd**2 + V
        cons = np.max(np.abs(H**2 + kk / aa**2 - (8 * math.pi / 3) * rho) / ((8 * math.pi / 3) * rho))
        addot = -(4 * math.pi / 3) * (rho + 3 * (0.5 * pd**2 - V)) * aa
        res[nn] = dict(tp_vol=turning_points(aa**3), tp_phi=turning_points(ph), tp_H=turning_points(H),
                       tp_T4=turning_points(T4), cons=cons, t_last=tt[-1], sec_frac=float(np.mean(rho + 3 * (0.5 * pd**2 - V) < 0)),
                       sample=(aa, ad, addot))
    r1, r2_ = res[n], res[int(1.5 * n)]
    print(f"\n  {label}: k={kk}, m={m} (1/L); steps n={n} vs 1.5n={int(1.5*n)}")
    for key in ("tp_vol", "tp_phi", "tp_H", "tp_T4"):
        print(f"    turning points {key:7s}: {r1[key]:4d} | {r2_[key]:4d}")
    print(f"    max constraint residual |H^2+k/a^2-8pi rho/3|/(8pi rho/3): {r1['cons']:.1e} | {r2_['cons']:.1e}")
    print(f"    fraction of steps with SEC violated (rho+3p<0): {r1['sec_frac']:.3f} | {r2_['sec_frac']:.3f}; t_end reached {r1['t_last']:.2f} L")
    # gr_tensors energy-condition scan on ~40 points of the trajectory
    aa, ad, addot = r2_["sample"]
    idx = np.linspace(0, len(aa) - 1, 40).astype(int)
    viol = {"nec": 0, "wec": 0, "sec": 0, "dec": 0}
    types = set()
    for i in idx:
        c = ec_on_metric(kk, aa[i], ad[i], addot[i])
        types.add(c["type"])
        for key in viol:
            viol[key] += 0 if c[key] else 1
    print(f"    gr_tensors EC scan on 40 trajectory points: violations {viol}; Hawking-Ellis types {sorted(map(str, types))}")
    return r2_


print("\nPart B: minisuperspace clock audit (geometric units, scale L)")
audit("(i) closed, massless scalar", 1.0, 0.0, 1.0, 0.0, 0.5, 60.0, 60000)
audit("(ii) flat, massive scalar", 0.0, 1.0, 1.0, 1.0, 0.0, 60.0, 60000)
audit("(iii) closed, massive scalar", 1.0, 1.0, 1.0, 1.0, 0.0, 60.0, 60000)

# ------------------------------------------------------------------ Part C: Goedel
tg, rg, yg, fg = sp.symbols("t r y phi", real=True)
ag = sp.symbols("a_G", positive=True)
sh = sp.sinh(rg)
gG = 4 * ag**2 * sp.Matrix([[-1, 0, 0, -sp.sqrt(2) * sh**2],
                            [0, 1, 0, 0], [0, 0, 1, 0],
                            [-sp.sqrt(2) * sh**2, 0, 0, sh**2 - sh**4]])
godel = Spacetime(gG, [tg, rg, yg, fg], simplify=True)
obs = sp.Matrix([1 / (2 * ag), 0, 0, 0])      # static observer u = d_t / (2a), g_tt = -4a^2
pts = [(0.0, float(r), 0.0, 0.3) for r in np.linspace(0.1, 2.5, 25)]
scan = godel.scan_energy_conditions(pts, params={ag: 1.0}, observer=obs)
one = godel.energy_conditions((0.0, 1.2, 0.0, 0.3), params={ag: 1.0}, observer=obs)
r_ctc = math.asinh(1.0)
print("\nPart C: Goedel universe (a_G = 1 L), effective source including Lambda")
print(f"  scan over r in [0.1, 2.5]: points {scan['points']}, violations {scan['violations']}")
print(f"  at r = 1.2: type {one['type']}, NEC {one['nec']}, WEC {one['wec']}, SEC {one['sec']}, DEC {one['dec']}, rho_obs = {one['rho_observer']:.5f} /L^2")
print(f"  g_phiphi = 4a^2 (sinh^2 r - sinh^4 r) < 0 for r > asinh(1) = {r_ctc:.4f}: phi-circles are closed timelike curves")
for r in (0.5, r_ctc, 1.2):
    print(f"    r = {r:.4f}: g_phiphi/(4a^2) = {math.sinh(r)**2 - math.sinh(r)**4:+.4f}")

# ------------------------------------------------------------------ Part D: closed LCDM York time
print("\nPart D: closed Lambda-CDM, York time K = -3H (SI)")
H0 = 67.4e3 / 3.0857e22          # s^-1
Om_m, Gyr = 0.315, 3.15576e16
for Ok in (-0.001, -0.01, -0.05):
    OL = 1 - Om_m - Ok
    astar = 3 * Om_m / (2 * abs(Ok))
    def Hs(aa):
        return H0 * math.sqrt(Om_m / aa**3 + Ok / aa**2 + OL)
    for n in (20000, 30000):     # t(a*) = int_0^a* da/(a H) in ln a, n vs 1.5 n
        lna = np.linspace(math.log(1e-8), math.log(astar), n)
        integrand = np.array([1 / Hs(math.exp(v)) for v in lna])
        tstar = np.trapezoid(integrand, lna) / Gyr if hasattr(np, "trapezoid") else np.trapz(integrand, lna) / Gyr
        print(f"  Ok = {Ok:+.3f}: a* = {astar:8.2f}, H_min/H0 = {Hs(astar)/H0:.5f}, sqrt(OL) = {math.sqrt(OL):.5f}, t(a*) = {tstar:9.2f} Gyr (n={n})")
print(f"\n(total {time.time()-t0_clock:.1f} s)")
