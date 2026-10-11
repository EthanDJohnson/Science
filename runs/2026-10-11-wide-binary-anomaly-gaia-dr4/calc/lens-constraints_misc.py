#!/usr/bin/env python3
"""Constraints lens, remaining checks (SI; MOND labelled SPECULATIVE):
 (a) size of GR (1PN) corrections in a wide binary;
 (b) perspective (projection) effect: kappa_p = theta * v_sys / v_c(s), and its full-median bias if
     uncorrected (magnitude model: Delta v_p = theta * v_sys with v_sys ~ 3D Gaussian, 25 km/s per
     axis, random sky direction; ASSUMED kinematics);
 (c) EF anisotropy as an observable: per-pair instantaneous boost eta(theta) = nu_e (1 + K sin^2 theta/2)
     (exact EF-limit QUMOND radial boost; applying it as a scalar per pair is an APPROXIMATION),
     for EF in the sky plane (pairs near l = 90/270 deg) vs EF along the line of sight (l = 0/180),
     and split by projected separation angle relative to the projected EF;
 (d) what Boufourou's quoted Delta lnL values imply for a quadratic likelihood, and how many sigma
     separate his E2/E3 values from the band of MOND predictions computed in lens-constraints_mond_gamma.py.
"""
import numpy as np

G = 6.67430e-11; MSUN = 1.3271244e20 / G; AU = 1.495978707e11; PC = 3.0856775814913673e16; C = 299792458.0
M = 1.5 * MSUN
rng = np.random.default_rng(31)

print("=== (a) GR corrections ===")
for s_au in [1000, 10000, 30000]:
    r = s_au * AU
    print("  r = %5d au: GM/(r c^2) = %.2e, v_c/c = %.2e  -> 1PN fractional correction to gamma ~ %.1e"
          % (s_au, G * M / (r * C ** 2), np.sqrt(G * M / r) / C, G * M / (r * C ** 2)))

# base Newtonian population, alpha = 1.3, dN/da ~ a^-1.6 weights (as in lens-constraints_vtilde.py)
def kepler_E(Mm, e):
    E = Mm + e * np.sin(Mm)
    for _ in range(50):
        E = E - (E - e * np.sin(E) - Mm) / (1 - e * np.cos(E))
    return E

def iso(n):
    v = rng.normal(size=(n, 3)); return v / np.linalg.norm(v, axis=1)[:, None]

def pop(n, alpha=1.3):
    e = rng.uniform(0, 1, n) ** (1 / (alpha + 1)) * 0.999
    E = kepler_E(rng.uniform(0, 2 * np.pi, n), e)
    den = 1 - e * np.cos(E)
    pos = np.stack([np.cos(E) - e, np.sqrt(1 - e * e) * np.sin(E), np.zeros(n)], 1)
    vel = np.stack([-np.sin(E) / den, np.sqrt(1 - e * e) * np.cos(E) / den, np.zeros(n)], 1)
    a = iso(n); b = iso(n); b -= (a * b).sum(1)[:, None] * a; b /= np.linalg.norm(b, axis=1)[:, None]
    c = np.cross(a, b); R = np.stack([a, b, c], 2)
    p = np.einsum("nij,nj->ni", R, pos); v = np.einsum("nij,nj->ni", R, vel)
    s = np.hypot(p[:, 0], p[:, 1]); r = np.linalg.norm(p, axis=1)
    return v[:, :2] * np.sqrt(s)[:, None], s ** 0.6, p / r[:, None]

def wq(x, w, q):
    i = np.argsort(x); cw = np.cumsum(w[i]); cw /= cw[-1]; return np.interp(q, cw, x[i])

N = 400_000
vt, w, nhat = pop(N)
vm = np.hypot(vt[:, 0], vt[:, 1]); m0 = wq(vm, w, 0.5)

print()
print("=== (b) Perspective effect, uncorrected (magnitude model) ===")
vsys = rng.normal(0, 25e3, size=(N, 3))
vsys_mag = np.linalg.norm(vsys, axis=1)
ang = rng.uniform(0, 2 * np.pi, N)
for d_pc in [50, 100, 200]:
    row = []
    for s_au in [2000, 5000, 10000, 20000, 30000]:
        theta = s_au * AU / (d_pc * PC)
        vc = np.sqrt(G * M / (s_au * AU))
        kp = theta * vsys_mag / vc
        vo = vt + np.stack([kp * np.cos(ang), kp * np.sin(ang)], 1)
        g = (wq(np.hypot(vo[:, 0], vo[:, 1]), w, 0.5) / m0) ** 2
        row.append("s=%dk: median kappa_p %.3f, gamma %.4f" % (s_au // 1000, np.median(kp), g))
    print("  d = %3d pc: %s" % (d_pc, "; ".join(row)))

print()
print("=== (c) EF anisotropy as an observable (simple nu, g_ext = 1.785 a0: nu_e = 1.5602, K = -0.2642) ===")
nu_e, K = 1.5602, -0.2642
def eta(cth):
    return nu_e * (1 + K * (1 - cth ** 2) / 2)
# EF in sky plane along x
g_sky = eta(nhat[:, 0])
v_sky = vm * np.sqrt(g_sky)
# EF along line of sight z
g_los = eta(nhat[:, 2])
v_los = vm * np.sqrt(g_los)
print("  angle-average check: <eta> over isotropic pairs = %.4f (exact 1.4228); weighted by s^0.6: %.4f"
      % (np.mean(g_sky), np.average(g_sky, weights=w)))
print("  median-inferred gamma, EF in sky plane: %.4f ; EF along line of sight: %.4f ; contrast %.4f"
      % ((wq(v_sky, w, 0.5) / m0) ** 2, (wq(v_los, w, 0.5) / m0) ** 2,
         (wq(v_sky, w, 0.5) / m0) ** 2 - (wq(v_los, w, 0.5) / m0) ** 2))
phi = np.arctan2(nhat[:, 1], nhat[:, 0])
par = np.abs(np.cos(phi)) > np.cos(np.pi / 6)
perp = np.abs(np.cos(phi)) < np.sin(np.pi / 6)
gp = (wq(v_sky[par], w[par], 0.5) / wq(vm[par], w[par], 0.5)) ** 2
gq = (wq(v_sky[perp], w[perp], 0.5) / wq(vm[perp], w[perp], 0.5)) ** 2
print("  EF in sky plane, split by projected separation angle: parallel (<30 deg) gamma %.4f (%.1f%% of pairs), perpendicular (>60 deg) %.4f (%.1f%%), contrast %.4f"
      % (gp, 100 * par.mean(), gq, 100 * perp.mean(), gp - gq))
for Nb in [1000, 3000, 10000, 30000]:
    sig = 1.39 * 1.42 / np.sqrt(Nb / 3)    # each third-subsample, median floor (lens-constraints_vtilde.py H)
    print("  N_bin = %5d: sigma(gamma) per split ~ %.3f -> contrast/sigma_diff = %.1f" % (Nb, sig, (gp - gq) / (np.sqrt(2) * sig)))

print()
print("=== (d) Boufourou's Delta lnL as a quadratic likelihood vs the MOND band ===")
g_hat = 1.05
for g_alt, dlnL in [(1.4, 129.0), (1.0, 4.8)]:
    sig = abs(g_alt - g_hat) / np.sqrt(2 * dlnL)
    print("  Delta lnL(%.2f) = %.1f -> implied sigma = %.4f" % (g_alt, dlnL, sig))
sig_lo, sig_hi = abs(1.0 - g_hat) / np.sqrt(2 * 4.8), abs(1.4 - g_hat) / np.sqrt(2 * 129.0)
for name, gm in [("standard n=2 bin-avg", 1.073), ("n=1.5 asymptote", 1.167), ("two-body QUMOND low (D-45)", 1.20),
                 ("two-body QUMOND high", 1.30), ("Chae eq.22 bin-avg", 1.321), ("MLS bin-avg", 1.341),
                 ("simple bin-avg (exact sphere avg)", 1.393), ("simple EF asymptote", 1.4228)]:
    z = (gm - g_hat) / sig_hi
    print("  %-34s gamma %.3f: (gamma - 1.05)/sigma_stat = %.1f sigma (stat only, sigma=%.4f); with E2 f(e) band half-width 0.055 added in quadrature: %.1f sigma"
          % (name, gm, z, sig_hi, (gm - g_hat) / np.hypot(sig_hi, 0.055)))
print("  deep bin (D-31): 1.11 +- 0.07 vs simple 1.42: %.1f sigma; vs two-body 1.25: %.1f sigma; vs standard 1.07: %.1f sigma"
      % ((1.4228 - 1.11) / 0.07, (1.25 - 1.11) / 0.07, (1.11 - 1.073) / 0.07))
