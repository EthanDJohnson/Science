#!/usr/bin/env python3
"""Constraints lens: gamma_MOND(g_N) with the Galactic external field effect (EFE), several
interpolating functions, and the exact bound on v~ for bound orbits in the EF-dominated
MOND potential.  SPECULATIVE physics (MOND), labelled.  SI units unless stated.

Independent formulas (not imported from the generator, which is used only for comparison):
  QUMOND nu-family:  nu_n(y) = [(1 + sqrt(1 + 4 y^-n))/2]^(1/n)   (n=1 simple, n=2 standard)
  MLS (McGaugh-Lelli-Schombert 2016): nu(y) = 1/(1 - exp(-sqrt(y)))
  Newtonian external field y_e from the TRUE external field x_e = g_ext/a0: y_e nu(y_e) = x_e.
  EF-dominated limit (point mass + test particle, uniform EF; exact solution of the linearised
  QUMOND equation, derived in this script's comments and checked against BZ18 Table 3):
      Phi = -(G M nu_e / r) (1 + K sin^2(theta)/2),  K = dln nu/dln y at y_e (K<0)
      radial-force boost eta(theta) = nu_e (1 + K sin^2 theta / 2), angle average nu_e (1 + K/3)
  AQUAL EF limit:  Phi = -G M / (mu_e r sqrt(1 + L sin^2 theta)),  L = dln mu/dln x at x_e.
  Bound orbit in a potential homogeneous of degree -1: E<0 => v^2 < 2 G M eta(theta)/r, and
  s <= r => v~^2 = v_p^2 s/(G M) <= 2 max_theta eta(theta).
  Transition regime (g_N ~ g_Ne): two approximations, (i) the 'algebraic' QUMOND field
  g = nu(|g_N|) g_N (curl part neglected) angle-averaged radial boost, (ii) the Chae 2024 eq.22
  form via the generator's gamma_mond(). An FFT QUMOND solve is in lens-constraints_qumond_fft.py.
"""
import sys
import numpy as np
sys.path.insert(0, ".claude/skills/conundrum/scripts")

A0 = 1.2e-10                      # m/s^2
KPC = 3.0856775814913673e19       # m
G = 6.67430e-11
MSUN = 1.3271244e20 / G
AU = 1.495978707e11
GEXT_BZ18 = (232.8e3) ** 2 / (8.2 * KPC)   # m/s^2, BZ18 sec 3.6

def nu_n(y, n):
    return ((1.0 + np.sqrt(1.0 + 4.0 * y ** (-n))) / 2.0) ** (1.0 / n)

def nu_mls(y):
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))

FUNCS = {"simple(n=1)": lambda y: nu_n(y, 1.0),
         "n=1.5": lambda y: nu_n(y, 1.5),
         "standard(n=2)": lambda y: nu_n(y, 2.0),
         "MLS": nu_mls}

def solve_ye(nu, x_e):
    lo, hi = 1e-6, 1e3
    for _ in range(200):
        mid = np.sqrt(lo * hi)
        if mid * nu(mid) < x_e:
            lo = mid
        else:
            hi = mid
    return np.sqrt(lo * hi)

def dlog(f, x, h=1e-6):
    return (np.log(f(x * (1 + h))) - np.log(f(x * (1 - h)))) / (np.log(1 + h) - np.log(1 - h))

def ef_limit(nu, x_e):
    y_e = solve_ye(nu, x_e)
    nue = nu(y_e)
    K = dlog(nu, y_e)
    # QUMOND: angle average and range
    th = np.linspace(0, np.pi, 20001)
    w = np.sin(th); w /= np.trapezoid(w, th)
    eta_q = nue * (1 + K * np.sin(th) ** 2 / 2)
    avg_q = np.trapezoid(eta_q * w, th)
    # AQUAL: mu(x) defined by x mu(x) = y, i.e. mu = 1/nu at the matching point; L = dln mu/dln x
    # with y = x mu(x): dln y = dln x (1 + L), and nu = x/y => dln nu = dln x - dln y = -L dln x
    # so K = dln nu/dln y = -L/(1+L)  =>  L = -K/(1+K)
    mue = 1.0 / nue
    L = -K / (1 + K)
    eta_a = 1.0 / (mue * np.sqrt(1 + L * np.sin(th) ** 2))
    avg_a = np.trapezoid(eta_a * w, th)
    return dict(y_e=y_e, nu_e=nue, K=K, L=L, q_avg=avg_q, q_min=eta_q.min(), q_max=eta_q.max(),
                a_avg=avg_a, a_min=eta_a.min(), a_max=eta_a.max())

def alg_boost(nu, y_int, y_e, nth=2001):
    """Angle-averaged radial boost of the algebraic QUMOND field nu(|g_N|) g_N minus the
    external part, for internal Newtonian field y_int (units a0) and Newtonian EF y_e."""
    th = np.linspace(0, np.pi, nth)
    w = np.sin(th); w /= np.trapezoid(w, th)
    # r_hat = (sin th, 0, cos th); EF along +z; internal Newtonian field = -y_int r_hat
    gx = -y_int * np.sin(th)
    gz = y_e - y_int * np.cos(th)
    mag = np.sqrt(gx ** 2 + gz ** 2)
    nv = nu(mag)
    fx = nv * gx
    fz = nv * gz - nu(y_e) * y_e
    radial = -(fx * np.sin(th) + fz * np.cos(th)) / y_int
    return np.trapezoid(radial * w, th)

print("=== 1. EF-dominated asymptotes (BZ18 framework), a0 = %.2e m/s^2 ===" % A0)
print("BZ18 g_ext = (232.8 km/s)^2/8.2 kpc = %.4e m/s^2 = %.4f a0" % (GEXT_BZ18, GEXT_BZ18 / A0))
print("Reference BZ18 Table 3 (dossier D-43): simple QUMOND 1.4228 / AQUAL 1.4056 / nu_ext 1.5602;"
      " standard 1.0726 / 1.0661 / 1.1462; MLS 1.3692 / 1.3508 / 1.5081")
for xe in [GEXT_BZ18 / A0, 1.8, 1.9, 2.0, 1.71, 2.09]:
    print("-- x_e = g_ext/a0 = %.3f (g_ext = %.3e m/s^2)" % (xe, xe * A0))
    for name, f in FUNCS.items():
        r = ef_limit(f, xe)
        print("  %-14s y_e=%.4f nu_e=%.4f K=%.4f | QUMOND avg %.4f [perp %.4f, par %.4f] | AQUAL avg %.4f [%.4f, %.4f]"
              " | v~max(bound) QUMOND %.4f AQUAL %.4f | Newton sqrt2 = 1.4142"
              % (name, r["y_e"], r["nu_e"], r["K"], r["q_avg"], r["q_min"], r["q_max"],
                 r["a_avg"], r["a_min"], r["a_max"], np.sqrt(2 * r["q_max"]), np.sqrt(2 * r["a_max"])))

print()
print("=== 2. Transition regime: gamma_MOND(g_N), g_N = internal Newtonian accel (m/s^2) ===")
try:
    import wide_binary_population as wbp
    have_wbp = True
except Exception as exc:  # pragma: no cover
    have_wbp = False
    print("generator import failed:", exc)
logg = np.arange(-11.0, -7.99, 0.25)
xe = GEXT_BZ18 / A0
hdr = "log10 gN | alg-simple | alg-n1.5 | alg-standard | alg-MLS | Chae-eq22(chae2024) | gen bz18_simple | gen bz18_standard"
print(hdr)
for lg in logg:
    y = 10 ** lg / A0
    row = []
    for name in ["simple(n=1)", "n=1.5", "standard(n=2)", "MLS"]:
        f = FUNCS[name]
        ye = solve_ye(f, xe)
        row.append(alg_boost(f, y, ye))
    if have_wbp:
        c = wbp.gamma_mond(10 ** lg, model="chae2024")
        bs = wbp.gamma_mond(10 ** lg, model="bz18_simple")
        bst = wbp.gamma_mond(10 ** lg, model="bz18_standard")
    else:
        c = bs = bst = float("nan")
    print("%7.2f | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f" % (lg, *row, c, bs, bst))

# convergence of the angular quadrature
f = FUNCS["simple(n=1)"]; ye = solve_ye(f, xe)
print("quadrature check alg-simple at 1e-10: nth=2001 -> %.6f, nth=3001 -> %.6f"
      % (alg_boost(f, 1e-10 / A0, ye, 2001), alg_boost(f, 1e-10 / A0, ye, 3001)))
print("limit checks: alg-simple at y=1e4 -> %.6f (Newton 1); at y=1e-4 -> %.4f (EF-limit avg %.4f)"
      % (alg_boost(f, 1e4, ye), alg_boost(f, 1e-4, ye), ef_limit(f, xe)["q_avg"]))

print()
print("=== 3. Scoring bin: log-uniform average over [10^-10.5, 10^-9.5] and at 1e-10 ===")
grid = np.linspace(-10.5, -9.5, 41)
for name in ["simple(n=1)", "standard(n=2)", "MLS"]:
    f = FUNCS[name]; ye = solve_ye(f, xe)
    vals = np.array([alg_boost(f, 10 ** g / A0, ye) for g in grid])
    print("  alg %-14s at 1e-10: %.4f ; bin-avg: %.4f ; at 10^-9.5: %.4f ; at 10^-10.5: %.4f"
          % (name, alg_boost(f, 1e-10 / A0, ye), vals.mean(), vals[-1], vals[0]))
if have_wbp:
    for m in ["chae2024", "bz18_simple", "bz18_standard"]:
        vals = wbp.gamma_mond(10 ** grid, model=m)
        print("  gen %-14s at 1e-10: %.4f ; bin-avg: %.4f" % (m, wbp.gamma_mond(1e-10, model=m), vals.mean()))

print()
print("=== 4. Projected-separation g_N proxy: g_N(s) = G M/s^2 vs g_N(r) = G M/r^2 ===")
# isotropic orientation, circular orbit snapshot: u = s/r has pdf u/sqrt(1-u^2) on [0,1]
rng = np.random.default_rng(1)
cth = rng.uniform(-1, 1, 400000)
u = np.sqrt(1 - cth ** 2)
print("  <s/r> = %.4f (pi/4 = %.4f); median r/s = %.4f; <(s/r)^2> = %.4f" %
      (u.mean(), np.pi / 4, np.median(1 / u), (u ** 2).mean()))
f = FUNCS["simple(n=1)"]; ye = solve_ye(f, xe)
for gs in [10 ** -9.5, 1e-10, 10 ** -10.5]:
    gr = gs * u ** 2       # true g_N(r) for pairs whose s-based proxy is gs
    lg = np.log10(gr)
    # tabulate alg boost on a grid then interpolate
    tab_l = np.linspace(-13, -8, 201)
    tab_g = np.array([alg_boost(f, 10 ** t / A0, ye, 801) for t in tab_l])
    gam = np.interp(lg, tab_l, tab_g)
    print("  s-proxy g_N=%.2e: alg-simple gamma at proxy %.4f, averaged over true r: %.4f"
          % (gs, alg_boost(f, gs / A0, ye), gam.mean()))

print()
print("=== 5. Physical scales for M_tot = 1.5 Msun ===")
M = 1.5 * MSUN
for lg in [-8.0, -9.0, -9.5, -10.0, -10.5, -11.0]:
    r = np.sqrt(G * M / 10 ** lg)
    print("  g_N = 1e%.1f m/s^2 -> r = %.0f au, v_c(r) = %.0f m/s" % (lg, r / AU, np.sqrt(G * M / r)))
ye_s = solve_ye(FUNCS["simple(n=1)"], xe)
print("  Newtonian external field (simple) g_Ne = y_e a0 = %.3e m/s^2 -> internal = external at r = %.0f au (1.5 Msun)"
      % (ye_s * A0, np.sqrt(G * M / (ye_s * A0)) / AU))
