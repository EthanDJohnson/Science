#!/usr/bin/env python3
"""lens-constraints: Van Den Broeck geometry [D-09] -- where the energy goes, and what it costs.

Metric: ds^2 = -dt^2 + B(r_s)^2 [ (dx - v f(r_s) dt)^2 + dy^2 + dz^2 ]  (lapse 1, shift (-v f,0,0), h_ij = B^2 delta_ij).
Units: geometric G = c = 1, lengths in metres.

Derived here and checked numerically: where f = 1 (inside the Alcubierre wall) the slice data are just translated
by the shift, so K_ij = 0 and rho = 3R/(16 pi) = (1/8 pi)[ |grad B|^2/B^4 - 2 lap(B)/B^3 ].  With sqrt(h) = B^3 the
B-region energy is E_B = (1/8 pi) int |grad B|^2 / B d^3x = (1/2) int B'^2/B r^2 dr > 0 (the lap(B) term integrates to a
boundary term that vanishes), although rho < 0 in part of the transition.  Cauchy-Schwarz gives
E_B >= 2 r1^2 (sqrt(B_max) - 1)^2 / Delta_B for a transition between r1 and r1 + Delta_B.
 1. Toy bubble (v = 1, R_out = 1.2 m, sigma = 8 /m, B_max = 4, B transition at 0.4 m, s_B = 6 /m).
 2. Energy conditions in the B region and in the f wall (toolkit scan).
 3. Slice integrals (n and 1.5n): total, negative part, positive part; vs E_B (1D) + Alcubierre wall formula.
 4. Scaling to a microscopic outer bubble with QI-limited walls (numbers from lens-constraints_qi_wall.py).
Run: python3 runs/smoke-constraints/calc/lens-constraints_vdb.py
"""
import math
import sys
import time

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from gr_tensors import G_NEWTON, HBAR, C, Spacetime, metrics, to_si

L_P = math.sqrt(HBAR * G_NEWTON / C**3)
M_SUN = 1.3271244e20 / G_NEWTON
print(__doc__.split(" 1.")[0])

t, x, y, z = sp.symbols("t x y z", real=True)
v = sp.symbols("v", positive=True)
f, B = sp.Function("f"), sp.Function("B")
rs = sp.sqrt((x - v * t) ** 2 + y**2 + z**2)
t0 = time.time()
st = Spacetime.from_adm(1, [-v * f(rs), 0, 0], B(rs) ** 2 * sp.eye(3), [t, x, y, z])
rho = st.energy_density()
print(f"symbolic rho built in {time.time() - t0:.1f} s")

# toy profiles
R_OUT, SIG, BMAX, RB, SB = 1.2, 8.0, 4.0, 0.4, 6.0
_, s0 = metrics.alcubierre()
f_top = metrics.alcubierre_top_hat(s0)
q = sp.symbols("q", positive=True)
f_lam = sp.Lambda(q, f_top(q).subs({s0["R"]: R_OUT, s0["sigma"]: SIG}))
B_lam = sp.Lambda(q, 1 + (BMAX - 1) * (1 - sp.tanh(SB * (q - RB))) / 2)
fun = {f: f_lam, B: B_lam}
par = {v: 1.0}
print(f"toy: v = 1, R_out = {R_OUT} m, sigma = {SIG} /m, B_max = {BMAX} (B(0) = {float(B_lam(1e-9)):.4f}), "
      f"B transition at {RB} m with s_B = {SB} /m")

t0 = time.time()
f_rho = st.compile(rho, par, fun)
print(f"compiled rho in {time.time() - t0:.1f} s")

# closed form for the B region (K_ij = 0 there)
Bq = B_lam(q)
dB, d2B = sp.diff(Bq, q), sp.diff(Bq, q, 2)
rho_B = (dB**2 / Bq**4 - 2 * (d2B + 2 * dB / q) / Bq**3) / (8 * sp.pi)
f_rhoB = sp.lambdify(q, rho_B, "numpy")

print("\n== 1. Pointwise: gr_tensors rho vs (1/8 pi)[|grad B|^2/B^4 - 2 lap B/B^3] along the y axis (t = 0)")
rgrid = np.linspace(0.05, 1.9, 38)
vals = np.array([float(f_rho(0.0, 0.0, r, 0.0)) for r in rgrid])
for r, val in zip(rgrid[::3], vals[::3]):
    print(f"   r = {r:5.2f} m: rho = {val:+.5e} /m^2   B-region formula = {float(f_rhoB(r)):+.5e} /m^2   f = {float(f_lam(r)):.4f}")
imin_B = int(np.argmin(np.where(rgrid < 0.8, vals, np.inf)))
imin_f = int(np.argmin(np.where(rgrid > 0.8, vals, np.inf)))
print(f"   most negative in B region: r = {rgrid[imin_B]:.3f} m, rho = {vals[imin_B]:+.4e}; in f wall: r = {rgrid[imin_f]:.3f} m, rho = {vals[imin_f]:+.4e}")

print("\n== 2. Energy-condition scans (toolkit)")
for label, r in (("B-region minimum", rgrid[imin_B]), ("f-wall minimum", rgrid[imin_f])):
    t0 = time.time()
    sc = st.energy_condition_scan((0.0, 0.0, float(r), 0.0), params=par, functions=fun)
    print(f"   {label} (0,0,{r:.3f},0): rho = {sc['rho']:+.4e}, min T(k,k) = {sc['nec_min']:+.4e}, "
          f"WEC ok = {sc['wec_ok']}, NEC ok = {sc['nec_ok']}  [{time.time() - t0:.1f} s]")

print("\n== 3. Slice integrals, box +-2.0 m")
f_dens = st.compile(rho * st.spatial_volume_element(), par, fun)
for n in (128, 192):
    t0 = time.time()
    E = st.integrate_on_slice(rho, 0.0, [(-2.0, 2.0)] * 3, n=n, params=par, functions=fun)
    h = 4.0 / n
    ax = -2.0 + h * (np.arange(n) + 0.5)
    yy, zz = np.meshgrid(ax, ax, indexing="ij")
    neg = pos = 0.0
    for xv in ax:
        d = np.broadcast_to(f_dens(0.0, np.full_like(yy, xv), yy, zz), yy.shape)
        neg += float(np.sum(np.minimum(d, 0.0)))
        pos += float(np.sum(np.maximum(d, 0.0)))
    print(f"   n = {n}: E_total = {E:+.6f} m; negative part = {neg * h**3:+.6f} m; positive part = {pos * h**3:+.6f} m  [{time.time() - t0:.1f} s]")
rr = np.linspace(1e-6, 3.0, 600001)
fB = sp.lambdify(q, dB**2 / Bq * q**2 / 2, "numpy")
E_B = np.trapezoid(fB(rr), rr)
E_f = -1.0 * SIG * R_OUT**2 / 36 - (math.pi**2 - 6) / (432 * SIG)
print(f"   1D: E_B = (1/2) int B'^2/B r^2 dr = {E_B:+.6f} m;  Alcubierre wall (thin-wall formula, R_out) E_f = {E_f:+.6f} m;"
      f"  sum = {E_B + E_f:+.6f} m")
print(f"   same interior proper radius with plain Alcubierre: R = B_max*RB = {BMAX * RB} m would need E_f = "
      f"{-SIG * (BMAX * RB) ** 2 / 36:+.4f} m if the wall stayed at sigma = {SIG}")

print("\n== 4. Scaling: microscopic outer bubble, QI-limited wall (alpha = 0.1, N = 1 from _qi_wall.py)")
qi = {1.0: 51.21, 2.0: 93.31, 10.0: 109.9}    # Delta_max / L_P
for R_out in (1e-15, 1e-12):
    for vv, dlp in qi.items():
        smin = 2.0 / (dlp * L_P)
        Ef = -vv**2 * smin * R_out**2 / 36
        print(f"   R_out = {R_out:.0e} m, v = {vv:4.1f}: sigma_min = {smin:.3e} /m, E_f = {Ef:+.3e} m = {to_si.mass_kg(Ef):+.3e} kg "
              f"= {to_si.mass_kg(Ef) / M_SUN:+.2e} M_sun")
print("   B-region lower bound E_B >= 2 r1^2 (sqrt(B_max)-1)^2 / Delta_B (illustrative parameters, not taken from [D-09]):")
for r1, Bm, dB_ in ((1e-15, 1e17, 1e-15), (1e-15, 1e17, 1e-13), (1e-15, 1e11, 1e-15)):
    EB = 2 * r1**2 * (math.sqrt(Bm) - 1) ** 2 / dB_
    print(f"   r1 = {r1:.0e} m, B_max = {Bm:.0e} (pocket radius ~ {Bm * r1:.0e} m), Delta_B = {dB_:.0e} m: "
          f"E_B >= {EB:+.3e} m = {to_si.mass_kg(EB):+.3e} kg = {to_si.mass_kg(EB) / M_SUN:+.2e} M_sun (positive)")

print("\n== 5. B-region split (1D, valid where f = 1): r^2/2 (B'^2/B - 2B'' - 4B'/r) integrates to E_B")
dens1d = sp.lambdify(q, q**2 / 2 * (dB**2 / Bq - 2 * d2B - 4 * dB / q), "numpy")
vals1d = dens1d(rr)
print(f"   E_B negative part = {np.trapezoid(np.minimum(vals1d, 0), rr):+.6f} m, positive part = "
      f"{np.trapezoid(np.maximum(vals1d, 0), rr):+.6f} m, sum = {np.trapezoid(vals1d, rr):+.6f} m (E_B above {E_B:+.6f} m)")

print("\n== 6. QI in the B region: C = |rho| r_c^4 at points with rho < 0 vs proper scale l = B(r)/s_B")
print("   (co-moving Eulerian observers see a static rho there, so no time-averaging factor; f = 1 so v drops out)")
Bm, sBs, RBs, Ro, sgs = sp.symbols("Bm sBs RBs Ro sgs", positive=True)
f_sym = sp.Lambda(q, f_top(q).subs({s0["R"]: Ro, s0["sigma"]: sgs}))
B_sym = sp.Lambda(q, 1 + (Bm - 1) * (1 - sp.tanh(sBs * (q - RBs))) / 2)
X = st.coords
gam = st.christoffel()
t0 = time.time()
keys = [(a, b, c, d) for a in range(4) for b in range(4) for c in range(4) for d in range(c + 1, 4)]
riem = []
for (a, b, c, d) in keys:
    e_ = sp.diff(gam[a][d][b], X[c]) - sp.diff(gam[a][c][b], X[d])
    for e in range(4):
        e_ += gam[a][c][e] * gam[e][d][b] - gam[a][d][e] * gam[e][c][b]
    riem.append(e_)
args = list(X) + [v, Ro, sgs, Bm, sBs, RBs]


def lam(expr):
    return sp.lambdify(args, sp.sympify(expr).subs({f: f_sym, B: B_sym}).doit(), "numpy", cse=True)


F_R, F_G, F_N, F_RHO = lam(sp.Matrix(riem)), lam(st.g), lam(st.eulerian_observer()), lam(rho)
print(f"   VdB Riemann (96 comps) built and lambdified with parameters in {time.time() - t0:.1f} s")
print("   rho in the B region is FIRST order in (B - 1) (from lap B), and so is the curvature, so C = |rho| r_c^4 need not")
print("   stay bounded: tabulate C/l^2 along the transition, u = s_B (r - R_B), l = B/s_B = local proper scale.")
deep, edge = [], []
for bm, sb in ((1e4, 6.0), (1e4, 12.0), (1e3, 6.0), (4.0, 6.0)):
    pv = (1.0, 3.0, 8.0, bm, sb, 0.5)      # v, R_out, sigma, B_max, s_B, R_B: f = 1 throughout the B region
    line = []
    for u in (0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0):
        r = 0.5 + u / sb
        pt = (0.0, 0.0, float(r), 0.0)
        rh = float(F_RHO(*pt, *pv))
        Bv = 1 + (bm - 1) * (1 - math.tanh(sb * (r - 0.5))) / 2
        if rh >= 0:
            line.append(f"u={u:g}: rho>=0")
            continue
        vals_ = np.array(F_R(*pt, *pv), dtype=float).reshape(-1)
        Rup = np.zeros((4, 4, 4, 4))
        for val, (a, b, c, d) in zip(vals_, keys):
            Rup[a, b, c, d], Rup[a, b, d, c] = val, -val
        gn = np.array(F_G(*pt, *pv), dtype=float).reshape(4, 4)
        Rlow = np.einsum("ae,ebcd->abcd", gn, Rup)
        nn = np.array(F_N(*pt, *pv), dtype=float).reshape(4)
        nn = nn / math.sqrt(-nn @ gn @ nn)
        basis = [nn]
        for i in range(1, 4):
            e = np.zeros(4)
            e[i] = 1.0
            e = e + (e @ gn @ nn) * nn
            for qq in basis[1:]:
                e = e - (e @ gn @ qq) * qq
            basis.append(e / math.sqrt(e @ gn @ e))
        E4 = np.array(basis)
        Rhat = np.einsum("ia,jb,kc,ld,abcd->ijkl", E4, E4, E4, E4, Rlow)
        rc = 1.0 / math.sqrt(np.max(np.abs(Rhat)))
        ratio = abs(rh) * rc**4 / (Bv / sb) ** 2
        line.append(f"u={u:g}: B-1={Bv - 1:.2e} C/l^2={ratio:.3e} (C/l^2)(B-1)={ratio * (Bv - 1):.3e}")
        if Bv - 1 > 100:
            deep.append(ratio)
        if Bv - 1 < 0.1:
            edge.append(ratio * (Bv - 1))
    print(f"   B_max = {bm:8.0e}, s_B = {sb:4.0f} /m:")
    for item in line:
        print(f"      {item}")
K_deep, K_edge = max(deep), max(edge)
L_P = math.sqrt(HBAR * G_NEWTON / C**3)
print(f"   deep part (B - 1 > 100): C/l^2 -> {min(deep):.3e} .. {K_deep:.3e} (bounded); outer edge (B - 1 < 0.1): "
      f"(C/l^2)(B - 1) -> {min(edge):.3e} .. {K_edge:.3e}, i.e. C ~ K_e/(s_B^2 (B - 1)) grows without bound as B -> 1")
print("   QI [D-04] with tau0 = alpha r_c (static rho for these geodesic observers):  C <= 3 N L_P^2/(32 pi^2 alpha^4)")
for alpha, N in ((0.1, 1), (0.01, 100)):
    q_ = 3 * N / (32 * math.pi**2 * alpha**4)
    lmax = math.sqrt(q_ / K_deep) * L_P
    print(f"   alpha = {alpha}, N = {N}: deep part needs l = B/s_B <= {lmax / L_P:.2e} L_P; outer edge violates wherever "
          f"(B - 1) < {K_edge / q_:.2e} (L_P s_B)^-2 -- a non-empty zone for every s_B (smooth tanh-type tails)")
    EB = 100.0**2 / (6 * lmax)
    print(f"      tanh profile: rho < 0 wherever B <~ B_max/3 (derived), so s_B >~ B_max/(3 l_max) and "
          f"E_B >~ L_pocket^2/(6 l_max) = {EB:.2e} m = {to_si.mass_kg(EB):.2e} kg = {to_si.mass_kg(EB) / M_SUN:.1e} M_sun for L_pocket = 100 m")
print("   Not tested: B profiles whose outer edge keeps rho >= 0 (e.g. a harmonic 1/r tail ending in a thin shell).")

print("\n== 7. Precision check: toolkit rho (unsimplified, float64) vs the B-region closed form at 50 digits (mpmath)")
import mpmath
mpmath.mp.dps = 50
for bm in (1e4, 1e6):
    fun_b = {f: sp.Lambda(q, f_top(q).subs({s0["R"]: 3.0, s0["sigma"]: 8.0})),
             B: sp.Lambda(q, 1 + (bm - 1) * (1 - sp.tanh(6.0 * (q - 0.5))) / 2)}
    fr_b = st.compile(rho, {v: 1.0}, fun_b)
    Bq_b = fun_b[B](q)
    ex = sp.lambdify(q, (sp.diff(Bq_b, q)**2 / Bq_b**4 - 2 * (sp.diff(Bq_b, q, 2) + 2 * sp.diff(Bq_b, q) / q) / Bq_b**3) / (8 * sp.pi), "mpmath")
    row = "; ".join(f"u={u}: {float(fr_b(0.0, 0.0, 0.5 + u / 6.0, 0.0)):+.3e} vs {float(ex(mpmath.mpf(0.5 + u / 6.0))):+.3e}" for u in (1, 2, 3, 5))
    print(f"   B_max = {bm:.0e}: {row}")
print("   -> float64 evaluation of the unsimplified expression is unreliable for B_max >~ 1e6 (cancellation);")
print("      section 6 therefore uses B_max <= 1e4, where toolkit and exact values agree to <= 3e-4.")
