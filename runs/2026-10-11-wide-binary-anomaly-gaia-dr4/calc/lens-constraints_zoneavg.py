#!/usr/bin/env python3
"""Constraints lens: MOND (SPECULATIVE) prediction averaged over a separation zone, as a
median-based test would see it, vs the constant gamma = 1.4 often used as 'the MOND value'.

Pairs: projected s log-distributed with dN/ds ~ s^-1.6 in [s_lo, s_hi]; total mass M ~ U(1.0, 2.0) Msun;
3D r from isotropic projection (r = s/sin i, cos i ~ U(0,1)), circular-orbit snapshot for r/s only;
gamma_i = exact QUMOND sphere-averaged boost at g_N = G M / r^2 (simple and standard nu,
g_ext = 1.785 a0; formula as in lens-constraints_mond_gamma.py); v~_i = sqrt(gamma_i) v~_N,i with v~_N
drawn from the alpha = 1.3 Newtonian Kepler population. Zone gamma = (median v~ / median v~_N)^2.
SI units.
"""
import numpy as np

G = 6.67430e-11; MSUN = 1.3271244e20 / G; AU = 1.495978707e11; KPC = 3.0856775814913673e19
A0 = 1.2e-10; XE = (232.8e3) ** 2 / (8.2 * KPC) / A0
rng = np.random.default_rng(41)

def nu_n(y, n):
    return ((1 + np.sqrt(1 + 4 * y ** (-n))) / 2) ** (1 / n)

def solve_ye(n):
    lo, hi = 1e-6, 1e3
    for _ in range(200):
        mid = np.sqrt(lo * hi)
        if mid * nu_n(mid, n) < XE: lo = mid
        else: hi = mid
    return mid

def boost(y, n, ye, nth=801):
    th = np.linspace(0, np.pi, nth); wt = np.sin(th); wt /= np.trapezoid(wt, th)
    gx = -y * np.sin(th); gz = ye - y * np.cos(th)
    nv = nu_n(np.hypot(gx, gz), n)
    rad = -(nv * gx * np.sin(th) + (nv * gz - nu_n(ye, n) * ye) * np.cos(th)) / y
    return np.trapezoid(rad * wt, th)

tab_l = np.linspace(-13.5, -7.0, 261)
TAB = {}
for n in [1.0, 2.0]:
    ye = solve_ye(n)
    TAB[n] = np.array([boost(10 ** t / A0, n, ye) for t in tab_l])

def kepler_E(Mm, e):
    E = Mm + e * np.sin(Mm)
    for _ in range(50):
        E = E - (E - e * np.sin(E) - Mm) / (1 - e * np.cos(E))
    return E

def newton_vt(n, alpha=1.3):
    e = rng.uniform(0, 1, n) ** (1 / (alpha + 1)) * 0.999
    E = kepler_E(rng.uniform(0, 2 * np.pi, n), e)
    den = 1 - e * np.cos(E)
    pos = np.stack([np.cos(E) - e, np.sqrt(1 - e * e) * np.sin(E), np.zeros(n)], 1)
    vel = np.stack([-np.sin(E) / den, np.sqrt(1 - e * e) * np.cos(E) / den, np.zeros(n)], 1)
    v1 = rng.normal(size=(n, 3)); v1 /= np.linalg.norm(v1, axis=1)[:, None]
    v2 = rng.normal(size=(n, 3)); v2 -= (v1 * v2).sum(1)[:, None] * v1; v2 /= np.linalg.norm(v2, axis=1)[:, None]
    R = np.stack([v1, v2, np.cross(v1, v2)], 2)
    p = np.einsum("nij,nj->ni", R, pos); v = np.einsum("nij,nj->ni", R, vel)
    s = np.hypot(p[:, 0], p[:, 1]); r = np.linalg.norm(p, axis=1)
    return np.hypot(v[:, 0], v[:, 1]) * np.sqrt(s), s / r, s ** 0.6

def zone(s_lo, s_hi, n_mc):
    vtN, u, w = newton_vt(n_mc)
    # assign physical s by drawing from dN/ds ~ s^-1.6 (the weight w already encodes a-selection at fixed s)
    x = rng.uniform(size=n_mc)
    s = (s_lo ** -0.6 + x * (s_hi ** -0.6 - s_lo ** -0.6)) ** (-1 / 0.6) * AU
    Mt = rng.uniform(1.0, 2.0, n_mc) * MSUN
    r = s / u
    lg = np.log10(G * Mt / r ** 2)
    out = {}
    def wq(xx, ww, q):
        i = np.argsort(xx); cw = np.cumsum(ww[i]); cw /= cw[-1]; return np.interp(q, cw, xx[i])
    m0 = wq(vtN, w, 0.5)
    for n in [1.0, 2.0]:
        gam = np.interp(lg, tab_l, TAB[n])
        out[n] = ((wq(vtN * np.sqrt(gam), w, 0.5) / m0) ** 2, np.average(gam, weights=w))
    gs = np.log10(G * Mt / s ** 2)
    return out, np.percentile(lg, [10, 50, 90]), np.percentile(gs, [10, 50, 90])

for (lo, hi, name) in [(2000, 30000, "Boufourou test zone / Banik+24 range 2-30 kau"),
                       (5000, 30000, "Chae 2024b-like s >~ 5 kau"),
                       (1000, 30000, "Cookson+26 range 1-30 kau")]:
    for nmc in [200_000, 300_000]:
        out, pr, ps = zone(lo, hi, nmc)
        print("%-46s N=%d: median-inferred gamma simple %.4f (mean %.4f), standard %.4f (mean %.4f); log10 g_N(r) 10/50/90%% = %.2f/%.2f/%.2f; g_N(s) %.2f/%.2f/%.2f"
              % (name, nmc, out[1.0][0], out[1.0][1], out[2.0][0], out[2.0][1], *pr, *ps))

# scoring bin built from s: pairs whose g_N(s) proxy lies in [10^-10.5, 10^-9.5]
vtN, u, w = newton_vt(300_000)
x = rng.uniform(size=len(u))
s = (1000 ** -0.6 + x * (60000 ** -0.6 - 1000 ** -0.6)) ** (-1 / 0.6) * AU
Mt = rng.uniform(1.0, 2.0, len(u)) * MSUN
gs = np.log10(G * Mt / s ** 2); gr = np.log10(G * Mt / (s / u) ** 2)
sel = (gs > -10.5) & (gs < -9.5)
def wq(xx, ww, q):
    i = np.argsort(xx); cw = np.cumsum(ww[i]); cw /= cw[-1]; return np.interp(q, cw, xx[i])
m0 = wq(vtN[sel], w[sel], 0.5)
for n in [1.0, 2.0]:
    gam = np.interp(gr[sel], tab_l, TAB[n])
    print("scoring bin via s-proxy [10^-10.5, 10^-9.5]: nu n=%.0f median-inferred gamma %.4f (N_sel=%d)"
          % (n, (wq(vtN[sel] * np.sqrt(gam), w[sel], 0.5) / m0) ** 2, sel.sum()))
