#!/usr/bin/env python3
"""Constraints lens: what each candidate explanation needs, in v~ = v_p/sqrt(G M/s) space.

Own numpy Kepler Monte Carlo (independent of the run's generator/estimator tools).
Units: G M = 1, a = 1 (v~ is dimensionless and scale-free); dN/da ~ a^-1.6 enters as the
weight w = (s/a)^0.6 for pairs selected in a narrow s bin (p(u|s) ~ u^(-beta-1) p(u), beta=-1.6).
Pseudo-Newtonian MOND: v~ scales as sqrt(gamma) (labelled approximation).

Sections
 A. weighted median v~ by eccentricity law; max v~; tail fractions under gamma
 B. tail-truncated median: weight MOND moves above sqrt(2), and naive vs consistent templates
 C. full-median contamination bound gamma_bias(f) = (Q(0.5/(1-f))/Q(0.5))^2 and the f needed
 D. triple perturbation of amplitude kappa = dv/v_c(s): bias of full median vs truncated medians
 E. measurement noise sigma_v~ (per axis): bias of the full median without noise-matched template
 F. eccentricity template mismatch: gamma_spurious(alpha_true; alpha_template), inversion
 G. hidden-companion mass underestimate M_true/M_est and its gamma bias (no velocity perturbation)
 H. statistical floor: sigma_gamma of a median estimator vs N
"""
import numpy as np

SEED = 7
N_MAIN = 600_000

def sample_e(kind, n, rng, alpha=None):
    if kind == "circular":
        return np.zeros(n)
    if kind == "power":
        return rng.uniform(0, 1, n) ** (1.0 / (alpha + 1.0)) * 0.999
    raise ValueError(kind)

def kepler_E(M, e):
    E = M + e * np.sin(M)
    for _ in range(60):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E

def rand_rot(n, rng):
    q = rng.normal(size=(n, 4)); q /= np.linalg.norm(q, axis=1)[:, None]
    w, x, y, z = q.T
    R = np.empty((n, 3, 3))
    R[:, 0, 0] = 1 - 2 * (y * y + z * z); R[:, 0, 1] = 2 * (x * y - z * w); R[:, 0, 2] = 2 * (x * z + y * w)
    R[:, 1, 0] = 2 * (x * y + z * w); R[:, 1, 1] = 1 - 2 * (x * x + z * z); R[:, 1, 2] = 2 * (y * z - x * w)
    R[:, 2, 0] = 2 * (x * z - y * w); R[:, 2, 1] = 2 * (y * z + x * w); R[:, 2, 2] = 1 - 2 * (x * x + y * y)
    return R

def population(kind, n, rng, alpha=None):
    """Returns v~ vector (2D sky components, in units of sqrt(GM/s)), s/a, weight."""
    e = sample_e(kind, n, rng, alpha)
    E = kepler_E(rng.uniform(0, 2 * np.pi, n), e)
    den = 1 - e * np.cos(E)
    pos = np.stack([np.cos(E) - e, np.sqrt(1 - e * e) * np.sin(E), np.zeros(n)], 1)
    vel = np.stack([-np.sin(E) / den, np.sqrt(1 - e * e) * np.cos(E) / den, np.zeros(n)], 1)
    R = rand_rot(n, rng)
    p = np.einsum("nij,nj->ni", R, pos); v = np.einsum("nij,nj->ni", R, vel)
    s = np.hypot(p[:, 0], p[:, 1])
    vt = v[:, :2] * np.sqrt(s)[:, None]
    return vt, s, s ** 0.6

def wquant(x, w, q):
    i = np.argsort(x); xs = x[i]; cw = np.cumsum(w[i]); cw /= cw[-1]
    return np.interp(q, cw, xs)

rng = np.random.default_rng(SEED)
LAWS = [("circular", None), ("uniform a=0", 0.0), ("a=0.5", 0.5), ("a=0.94", 0.94), ("thermal a=1", 1.0),
        ("a=1.17", 1.17), ("a=1.2", 1.2), ("a=1.3", 1.3), ("a=1.5", 1.5), ("a=2", 2.0)]
print("=== A. Newtonian v~ distribution (no noise, no contaminants), N = %d per law ===" % N_MAIN)
med = {}
pops = {}
for name, al in LAWS:
    kind = "circular" if al is None else "power"
    vt, s, w = population(kind, N_MAIN, rng, al)
    vm = np.hypot(vt[:, 0], vt[:, 1])
    med[name] = wquant(vm, w, 0.5)
    pops[name] = (vt, vm, w)
    # convergence: half sample
    h = N_MAIN // 2
    print("  %-12s median %.4f (half-sample %.4f) | max %.4f | P(v~>1) %.4f | P(v~>1.2) %.4f"
          % (name, med[name], wquant(vm[:h], w[:h], 0.5), vm.max(), np.average(vm > 1, weights=w),
             np.average(vm > 1.2, weights=w)))
print("  reference D-48 (a^-1.6 MC): circular 0.6925, uniform 0.5896, thermal 0.5269, alpha=1.3 0.5134, alpha=2 0.4880")

print()
print("=== B. Pseudo-Newtonian gamma: fraction of pairs above cuts, tail-truncated medians ===")
for name in ["thermal a=1", "a=1.3"]:
    vt, vm, w = pops[name]
    m0 = med[name]
    for g in [1.0, 1.2, 1.37, 1.4228]:
        vg = vm * np.sqrt(g)
        out = []
        for cut in [np.sqrt(2), 1.6, 2.0, 2.5]:
            out.append(np.average(vg > cut, weights=w))
        sel = vg < np.sqrt(2)
        mt = wquant(vg[sel], w[sel], 0.5)
        # naive: compare truncated median with untruncated Newtonian template median
        g_naive = (mt / m0) ** 2
        print("  %-11s gamma_true %.4f: P(v~>sqrt2) %.4f, P(>1.6) %.4f, P(>2) %.4f, P(>2.5) %.4f | trunc-median %.4f -> naive gamma %.4f (consistent template: exact by construction)"
              % (name, g, *out, mt, g_naive))

print()
print("=== C. Full-median contamination bound (all contaminants above the clean median) ===")
for name in ["thermal a=1", "a=1.3"]:
    vt, vm, w = pops[name]
    m0 = med[name]
    fs = np.array([0.02, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4])
    gb = [(wquant(vm, w, 0.5 / (1 - f)) / m0) ** 2 for f in fs]
    print("  %-11s f -> gamma_bias_max: " % name + ", ".join("%.2f->%.3f" % (f, g) for f, g in zip(fs, gb)))
    fgrid = np.linspace(0, 0.45, 451)
    ggrid = np.array([(wquant(vm, w, 0.5 / (1 - f)) / m0) ** 2 for f in fgrid])
    for target in [1.05, 1.1, 1.2, 1.37, 1.5]:
        print("     uncalibrated contaminant fraction needed for gamma = %.2f: f >= %.3f" % (target, np.interp(target, ggrid, fgrid)))

print()
print("=== D. Triple perturbation (f = 0.2, kappa = |dv|/v_c(s), isotropic 3D kick projected) ===")
vt, vm, w = pops["a=1.3"]
m0 = med["a=1.3"]
n = len(vm)
rng2 = np.random.default_rng(11)
is_t = rng2.uniform(size=n) < 0.2
d3 = rng2.normal(size=(n, 3)); d3 /= np.linalg.norm(d3, axis=1)[:, None]
for kappa in [0.1, 0.2, 0.3, 0.5, 0.75, 1.0, 1.5, 2.0, 4.0]:
    vo = vt.copy()
    vo[is_t] += kappa * d3[is_t, :2]
    vmo = np.hypot(vo[:, 0], vo[:, 1])
    g_full = (wquant(vmo, w, 0.5) / m0) ** 2
    res = []
    for cut in [np.sqrt(2), 2.5]:
        sel = vmo < cut
        res.append((wquant(vmo[sel], w[sel], 0.5) / m0) ** 2)
        res.append(np.average(sel & is_t, weights=w) / np.average(is_t, weights=w))
    print("  kappa %.2f: full-median gamma %.3f | trunc<sqrt2 gamma %.3f (triples kept %.2f) | trunc<2.5 gamma %.3f (kept %.2f)"
          % (kappa, g_full, *res))

print()
print("=== E. Measurement noise (per-axis Gaussian sigma in v~ units), Newtonian truth, alpha = 1.3 ===")
rng3 = np.random.default_rng(13)
nz = rng3.normal(size=(n, 2))
for sig in [0.02, 0.05, 0.1, 0.15, 0.2, 0.3]:
    vmo = np.hypot(vt[:, 0] + sig * nz[:, 0], vt[:, 1] + sig * nz[:, 1])
    g_full = (wquant(vmo, w, 0.5) / m0) ** 2
    sel = vmo < np.sqrt(2)
    g_tr = (wquant(vmo[sel], w[sel], 0.5) / m0) ** 2
    print("  sigma_v~ %.2f: full-median gamma (noise-free template) %.4f; trunc<sqrt2 %.4f" % (sig, g_full, g_tr))
print("  scaling: sigma_v~ = 4.74 km/s * d[kpc] * sigma_mu,rel[mas/yr] / sqrt(G M/s) grows as s^0.5 at fixed d, M")

print()
print("=== F. Eccentricity template mismatch (full median): gamma_spurious = (med_true/med_template)^2 ===")
names = [nm for nm, _ in LAWS]
for tmpl in ["thermal a=1", "a=1.2", "a=1.3"]:
    row = ", ".join("%s:%.3f" % (nm, (med[nm] / med[tmpl]) ** 2) for nm in names)
    print("  template %-11s -> %s" % (tmpl, row))
al = np.array([0.0, 0.5, 0.94, 1.0, 1.17, 1.2, 1.3, 1.5, 2.0])
mm = np.array([med["uniform a=0"], med["a=0.5"], med["a=0.94"], med["thermal a=1"], med["a=1.17"], med["a=1.2"],
               med["a=1.3"], med["a=1.5"], med["a=2"]])
for tmpl_med, tn in [(med["a=1.2"], "1.2"), (med["a=1.3"], "1.3")]:
    gs = (mm / tmpl_med) ** 2
    # gs decreasing in alpha; invert
    for target in [1.1, 1.2, 1.37]:
        a_need = np.interp(target, gs[::-1], al[::-1])
        print("  template alpha=%s: true alpha needed for gamma_spurious=%.2f: %.2f (circular gives %.3f)"
              % (tn, target, a_need, (med["circular"] / tmpl_med) ** 2))
print("  observed (Hwang+22, D-41): alpha = 1.30 at 1-3 kau, 1.32 +0.09-0.08 at 3-10 kau, 1.17 +0.14-0.15 at 10-30 kau")

print()
print("=== G. Hidden-companion mass underestimate (no velocity perturbation) ===")
rng4 = np.random.default_rng(17)
for aL in [3.5, 4.0]:
    for qlo in [0.1, 0.5]:
        q = rng4.uniform(qlo, 1.0, 400000)
        mB = rng4.uniform(0.5, 1.0, 400000)   # m_B/m_A, a mild spread
        Mt = (1 + q) + mB
        Me = (1 + q ** aL) ** (1 / aL) + mB
        mu = Mt / Me
        print("  L~m^%.1f, q_in~U(%.1f,1): mean M_true/M_est %.4f, median %.4f, max %.4f" % (aL, qlo, mu.mean(), np.median(mu), mu.max()))
# effect on full median and truncated median for f=0.2 triples with mass term only
q = rng4.uniform(0.1, 1.0, n); mB = rng4.uniform(0.5, 1.0, n)
mu = ((1 + q) + mB) / ((1 + q ** 3.5) ** (1 / 3.5) + mB)
fac = np.where(is_t, np.sqrt(mu), 1.0)
vmo = vm * fac
sel = vmo < np.sqrt(2)
print("  f=0.2, L~m^3.5, q_in~U(0.1,1), mass term only: full-median gamma %.4f, trunc<sqrt2 gamma %.4f"
      % ((wquant(vmo, w, 0.5) / m0) ** 2, (wquant(vmo[sel], w[sel], 0.5) / m0) ** 2))
for fm in [0.1, 0.3, 0.5]:
    it = rng4.uniform(size=n) < fm
    vmo = vm * np.where(it, np.sqrt(mu), 1.0)
    print("  f=%.1f mass term only: full-median gamma %.4f" % (fm, (wquant(vmo, w, 0.5) / m0) ** 2))

print()
print("=== H. Statistical floor of a median estimator (thermal-ish alpha=1.3, Newton) ===")
vt, vm, w = pops["a=1.3"]
m0 = med["a=1.3"]
dq = 0.01
fm = 2 * dq / (wquant(vm, w, 0.5 + dq) - wquant(vm, w, 0.5 - dq))
c = 1.0 / (fm * m0)   # sigma_gamma = gamma * c / sqrt(N)
print("  pdf at median f(m) = %.4f, median m = %.4f -> sigma_gamma/gamma = %.3f/sqrt(N) (weights ignored in N)" % (fm, m0, c))
for N in [61, 341, 1000, 3000, 6389, 10000, 30000, 50000, 100000]:
    print("  N = %6d: sigma_gamma(gamma=1) = %.4f, (gamma=1.4) = %.4f" % (N, c / np.sqrt(N), 1.4 * c / np.sqrt(N)))
for tgt in [0.005, 0.01, 0.02]:
    print("  N needed for sigma_gamma = %.3f at gamma=1: %d" % (tgt, int((c / tgt) ** 2)))
# empirical check by subsampling
rs = np.random.default_rng(19)
for N in [341, 3000]:
    gs = []
    for _ in range(400):
        idx = rs.integers(0, len(vm), N)
        gs.append((wquant(vm[idx], w[idx], 0.5) / m0) ** 2)
    print("  bootstrap check N=%d: sd(gamma) = %.4f (analytic %.4f; weights add variance)" % (N, np.std(gs), c / np.sqrt(N)))
