#!/usr/bin/env python3
"""lens-constraints: Ford-Roman quantum inequality [D-04] applied to the Alcubierre bubble wall.

Units: geometric G = c = 1 with lengths in metres (hbar -> L_P^2), converted to SI at the end.

Method (the flat-space QI is only trusted for sampling times short compared with the local
curvature radius, so the bound is imposed at tau0 = alpha * r_c):
 1. Riemann tensor from gr_tensors' Christoffel symbols (the toolkit has no Riemann method);
    checked by contracting to Ricci and comparing with gr_tensors.ricci().
 2. Orthonormal Eulerian-frame components R_(abcd); r_c = max|R_(abcd)|^(-1/2).
 3. Scan wall points for C = |rho| * r_c^4 * sigma^2 (dimensionless; independent of sigma for sigma R >> 1).
 4. Lorentzian time-average of rho along the geodesic Eulerian worldline vs the local value.
 5. QI [D-04], N scalar-equivalent species:  |<rho>| <= N * 3 L_P^2 / (32 pi^2 tau0^4)
    -> sigma_min, Delta_max = 2/sigma_min, and the total energy of an R = 100 m bubble.
Run from the project root: python3 runs/smoke-constraints/calc/lens-constraints_qi_wall.py
"""
import math
import sys
import time

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from gr_tensors import C, G_NEWTON, HBAR, metrics, to_si

L_P = math.sqrt(HBAR * G_NEWTON / C**3)
M_SUN = 1.3271244e20 / G_NEWTON
print(__doc__.split("Method")[0])
print(f"L_P = {L_P:.5e} m, M_sun = {M_SUN:.5e} kg")

st, s = metrics.alcubierre()
t, x, y, z, v, R, sig, f = (s[k] for k in ("t", "x", "y", "z", "v", "R", "sigma", "f"))
top = metrics.alcubierre_top_hat(s)
X = st.coords
gam = st.christoffel()

t0 = time.time()
# R^a_{bcd} = d_c Gam^a_{db} - d_d Gam^a_{cb} + Gam^a_{ce} Gam^e_{db} - Gam^a_{de} Gam^e_{cb}  (same convention as gr_tensors' Ricci)
riem_up = {}
for a in range(4):
    for b in range(4):
        for c in range(4):
            for d in range(c + 1, 4):
                e_ = sp.diff(gam[a][d][b], X[c]) - sp.diff(gam[a][c][b], X[d])
                for e in range(4):
                    e_ += gam[a][c][e] * gam[e][d][b] - gam[a][d][e] * gam[e][c][b]
                riem_up[(a, b, c, d)] = e_
keys = list(riem_up)
print(f"Riemann (96 components) built symbolically in {time.time() - t0:.1f} s")


PARS = (v, R, sig)


def lam(expr):
    """Lambdify over (t,x,y,z,v,R,sigma) once; gr_tensors.compile() needs numeric params, which
    would force a fresh (slow) lambdify for every parameter set in a sweep."""
    e = sp.sympify(expr).subs(f, top).doit()
    return sp.lambdify(list(X) + list(PARS), e, "numpy", cse=True)


t0 = time.time()
F_RIEM = lam(sp.Matrix([riem_up[k] for k in keys]))
F_G = lam(st.g)
F_N = lam(st.eulerian_observer())
F_RHO = lam(st.energy_density())
F_RIC = lam(st.ricci())
print(f"lambdified Riemann, g, n, rho, Ricci once in {time.time() - t0:.1f} s")


def compile_all(p):
    pv = (p[v], p[R], p[sig])
    return ((lambda *c: F_RIEM(*c, *pv)), (lambda *c: F_G(*c, *pv)), (lambda *c: F_N(*c, *pv)),
            (lambda *c: F_RHO(*c, *pv)), (lambda *c: F_RIC(*c, *pv)), 0.0)


def frame_riemann(fr, fg, fn, pt):
    vals = np.array(fr(*pt), dtype=float).reshape(-1)
    Rup = np.zeros((4, 4, 4, 4))
    for val, (a, b, c, d) in zip(vals, keys):
        Rup[a, b, c, d] = val
        Rup[a, b, d, c] = -val
    gn = np.array(fg(*pt), dtype=float).reshape(4, 4)
    Rlow = np.einsum("ae,ebcd->abcd", gn, Rup)
    n = np.array(fn(*pt), dtype=float).reshape(4)
    n = n / math.sqrt(-n @ gn @ n)
    basis = [n]
    for i in range(1, 4):
        e = np.zeros(4)
        e[i] = 1.0
        e = e + (e @ gn @ n) * n
        for q in basis[1:]:
            e = e - (e @ gn @ q) * q
        basis.append(e / math.sqrt(e @ gn @ e))
    E = np.array(basis)  # rows: frame vectors
    Rhat = np.einsum("ia,jb,kc,ld,abcd->ijkl", E, E, E, E, Rlow)
    gi = np.linalg.inv(gn)
    kretsch = float(np.einsum("abcd,ae,bf,cg,dh,efgh->", Rlow, gi, gi, gi, gi, Rlow))
    return Rhat, Rup, kretsch


# ---------------------------------------------------------------- 1. validate Riemann via Ricci
print("\n== 1. Riemann check: contraction R^a_{bad} vs gr_tensors.ricci()")
p = {v: 2.0, R: 1.0, sig: 8.0}
fr, fg, fn, frho, fric, dt = compile_all(p)
for pt in [(0.0, 0.0, 1.0, 0.0), (0.0, 0.6, 0.7, 0.2)]:
    _, Rup, _ = frame_riemann(fr, fg, fn, pt)
    ric_mine = np.einsum("abad->bd", Rup)
    ric_tool = np.array(fric(*pt), dtype=float).reshape(4, 4)
    print(f"   point {pt}: max |Ricci_mine - Ricci_toolkit| = {np.max(np.abs(ric_mine - ric_tool)):.2e} "
          f"(max |Ricci| = {np.max(np.abs(ric_tool)):.2e})")

# ---------------------------------------------------------------- 2-3. curvature radius and C = |rho| r_c^4 sigma^2
print("\n== 2-3. Curvature radius r_c and C = |rho| r_c^4 sigma^2 over wall points (R = 1 m)")
results = {}
SIG = {0.01: (4.0e4, 8.0e4), 0.1: (32.0, 64.0), 1.0: (32.0, 64.0), 2.0: (32.0, 64.0), 10.0: (32.0, 64.0)}
print("   (thin-wall regime needs sigma R >> 1/v, so v = 0.01 uses sigma R = 4e4, 8e4)")
for vv in (0.01, 0.1, 1.0, 2.0, 10.0):
    for sv in SIG[vv]:
        p = {v: vv, R: 1.0, sig: sv}
        fr, fg, fn, frho, fric, dt = compile_all(p)
        best = (0.0, None, None, None)
        rc_eq = rho_eq = None
        for th in np.linspace(0.05, math.pi / 2, 12):          # polar angle from +x (direction of motion)
            for u in np.linspace(-3.0, 3.0, 25):               # r = R + u/sigma across the wall
                r = 1.0 + u / sv
                for sgn in (+1, -1):                           # front and back hemispheres
                    pt = (0.0, sgn * r * math.cos(th), r * math.sin(th), 0.0)
                    Rhat, _, _ = frame_riemann(fr, fg, fn, pt)
                    rc = 1.0 / math.sqrt(np.max(np.abs(Rhat)))
                    rh = float(frho(*pt))
                    Cval = abs(rh) * rc**4 * sv**2
                    if Cval > best[0]:
                        best = (Cval, pt, rc, rh)
        pt_eq = (0.0, 0.0, 1.0, 0.0)
        Rhat, _, K = frame_riemann(fr, fg, fn, pt_eq)
        rc_eq = 1.0 / math.sqrt(np.max(np.abs(Rhat)))
        rho_eq = float(frho(*pt_eq))
        results[(vv, sv)] = dict(C=best[0], pt=best[1], rc=best[2], rho=best[3], rc_eq=rc_eq, rho_eq=rho_eq, K=K)
        print(f"   v={vv:5.2f} sigma={sv:4.0f}/m: equator wall rho={rho_eq:+.4e}/m^2, r_c*sigma={rc_eq * sv:.4f}, "
              f"Kretschmann={K:.3e}/m^4; max C={best[0]:.4e} at (x,y)=({best[1][1]:+.3f},{best[1][2]:.3f}) m")

print("   sigma-independence of C (thin-wall scaling check): ratio C(2 sigma)/C(sigma):")
for vv in (0.01, 0.1, 1.0, 2.0, 10.0):
    s1, s2 = SIG[vv]
    print(f"     v={vv:5.2f}: {results[(vv, s2)]['C'] / results[(vv, s1)]['C']:.4f}")

# ---------------------------------------------------------------- 4. Lorentzian average along the Eulerian geodesic
print("\n== 4. Lorentzian-sampled rho along the Eulerian worldline through the max-C point (larger sigma of each pair, R = 1 m)")
avg_factor = {}
for vv in (0.01, 0.1, 1.0, 2.0, 10.0):
    sv = SIG[vv][1]
    res = results[(vv, sv)]
    p = {v: vv, R: 1.0, sig: sv}
    frho = compile_all(p)[3]
    rq = sp.symbols("rq", positive=True)
    ff = sp.lambdify(rq, top(rq).subs({R: 1.0, sig: sv}), "numpy")
    x0, y0 = res["pt"][1], res["pt"][2]

    def xdot(tt, xx):
        return vv * ff(math.sqrt((xx - vv * tt) ** 2 + y0**2))

    out = []
    for alpha in (0.01, 0.1, 0.5):
        tau0 = alpha * res["rc"]
        T = 60 * tau0 + 20.0 / (sv * vv)
        nstep = 40000
        h = T / nstep
        ts, xs = [0.0], [x0]
        for direction in (+1, -1):          # RK4 forward and backward from t = 0
            tt, xx = 0.0, x0
            for _ in range(nstep):
                hh = direction * h
                k1 = xdot(tt, xx)
                k2 = xdot(tt + hh / 2, xx + hh * k1 / 2)
                k3 = xdot(tt + hh / 2, xx + hh * k2 / 2)
                k4 = xdot(tt + hh, xx + hh * k3)
                xx += hh * (k1 + 2 * k2 + 2 * k3 + k4) / 6
                tt += hh
                ts.append(tt)
                xs.append(xx)
        order = np.argsort(ts)
        ts, xs = np.array(ts)[order], np.array(xs)[order]
        rhos = np.array(frho(ts, xs, np.full_like(ts, y0), np.zeros_like(ts)), dtype=float)
        w = (tau0 / math.pi) / (ts**2 + tau0**2)
        mean = np.trapezoid(rhos * w, ts)   # rho ~ 0 outside the window (wall has passed), so this is the full average
        out.append((alpha, mean / res["rho"], np.trapezoid(w, ts)))
    avg_factor[vv] = out
    print(f"   v={vv:5.2f}: " + "; ".join(f"alpha={a}: <rho>/rho_local={r:.4f} (weight captured {wsum:.4f})" for a, r, wsum in out))

# ---------------------------------------------------------------- 5. QI bound -> wall thickness and energy
print("\n== 5. QI [D-04] |<rho>| <= N*3 L_P^2/(32 pi^2 tau0^4), tau0 = alpha r_c  =>  Delta_max = 2/sigma_min")
print("   C_eff = max C * (<rho>/rho_local at alpha); sigma_min = alpha^2 sqrt(32 pi^2 C_eff/(3N)) / L_P")
RHO_PLANCK = C**7 / (HBAR * G_NEWTON**2)
print(f"   Planck energy density c^7/(hbar G^2) = {RHO_PLANCK:.3e} J/m^3")
print(f"   {'v':>5s} {'alpha':>5s} {'N':>4s} {'C_eff':>9s} {'Delta_max/L_P':>13s} {'Delta_max (m)':>13s} {'r_c/L_P':>8s} {'E(R=100 m) J':>12s} {'M (kg)':>10s} {'M/M_sun':>9s} {'peak|rho| J/m^3':>15s} {'rho/rho_P':>9s}")
table = []
for vv in (0.01, 0.1, 1.0, 2.0, 10.0):
    for alpha, ratio, _ in avg_factor[vv]:
        Ceff = results[(vv, SIG[vv][1])]["C"] * ratio
        rcs = results[(vv, SIG[vv][1])]["rc_eq"] * SIG[vv][1]   # r_c * sigma at the equator wall
        for N in (1, 100):
            smin = alpha**2 * math.sqrt(32 * math.pi**2 * Ceff / (3 * N)) / L_P
            dmax = 2.0 / smin
            E = -vv**2 * smin * 100.0**2 / 36.0
            rho_pk = vv**2 * smin**2 / (128 * math.pi)
            table.append((vv, alpha, N, dmax / L_P))
            print(f"   {vv:5.2f} {alpha:5.2f} {N:4d} {Ceff:9.3e} {dmax / L_P:13.3e} {dmax:13.3e} {rcs / smin / L_P:8.1f} {to_si.energy_joules(E):+12.3e} "
                  f"{to_si.mass_kg(E):+10.3e} {to_si.mass_kg(E) / M_SUN:+9.2e} {to_si.energy_density_j_per_m3(rho_pk):15.3e} "
                  f"{to_si.energy_density_j_per_m3(rho_pk) / RHO_PLANCK:9.1e}")
print("\n   Only one worldline per v is tested; the QI must hold for every inertial observer, so the true")
print("   Delta_max is <= the tabulated value (the table is generous to the warp drive).")
print("   Sensitivity: Delta_max scales as alpha^-2 and N^(1/2); E(R) scales as v^2 R^2 / Delta_max.")
print("   Compare [D-05]: 'Wall thickness allowed by QIs for a macroscopic bubble ~ hundreds of Planck lengths'.")

# ---------------------------------------------------------------- 6. static (co-moving) observers in the outer tail
print("\n== 6. Observers at rest in the bubble frame, u ~ (1, v, 0, 0), in the outer tail of a SUBLUMINAL wall")
print("   (they exist where v (1 - f) < 1; they see a static T_ab, so <rho> = local rho; acceleration")
print("    a = |grad ln sqrt(1 - v^2 (1-f)^2)| -> 0 in the tail, so the inertial QI applies there when a*tau0 << 1)")
F_T = lam(st.stress_energy())
rq6 = sp.symbols("rq6", positive=True)
for vv in (0.1, 0.5, 0.9):
    sv = 8.0
    pv = (vv, 1.0, sv)
    fprof = sp.lambdify(rq6, top(rq6).subs({R: 1.0, sig: sv}), "numpy")
    dfprof = sp.lambdify(rq6, sp.diff(top(rq6), rq6).subs({R: 1.0, sig: sv}), "numpy")
    print(f"   v = {vv}, R = 1 m, sigma = {sv} /m, polar angle 1.1 deg from the +x (front) axis:")
    for r in (1.3, 1.6, 2.0, 2.5, 3.0):
        th = math.radians(1.1)
        pt = (0.0, r * math.cos(th), r * math.sin(th), 0.0)
        T_ = np.array(F_T(*pt, *pv), dtype=float).reshape(4, 4)
        g_ = np.array(F_G(*pt, *pv), dtype=float).reshape(4, 4)
        u_ = np.array([1.0, vv, 0.0, 0.0])
        u_ = u_ / math.sqrt(-u_ @ g_ @ u_)
        rho_c = float(u_ @ T_ @ u_)
        vals = np.array(F_RIEM(*pt, *pv), dtype=float).reshape(-1)
        Rup = np.zeros((4, 4, 4, 4))
        for val, (a, b, c, d) in zip(vals, keys):
            Rup[a, b, c, d], Rup[a, b, d, c] = val, -val
        Rlow = np.einsum("ae,ebcd->abcd", g_, Rup)
        basis = [u_]
        for i in range(1, 4):
            e = np.zeros(4)
            e[i] = 1.0
            e = e + (e @ g_ @ u_) * u_
            for qq in basis[1:]:
                e = e - (e @ g_ @ qq) * qq
            basis.append(e / math.sqrt(e @ g_ @ e))
        E4 = np.array(basis)
        rc = 1.0 / math.sqrt(np.max(np.abs(np.einsum("ia,jb,kc,ld,abcd->ijkl", E4, E4, E4, E4, Rlow))))
        fv, dfv = float(fprof(r)), float(dfprof(r))
        acc = vv**2 * (1 - fv) * abs(dfv) / (1 - vv**2 * (1 - fv) ** 2)
        Cc = abs(rho_c) * rc**4 * sv**2
        print(f"      r = {r:3.1f} m: f = {fv:.2e}, rho_c = {rho_c:+.3e} /m^2 (rho_c/f = {rho_c / fv:+.3f}), r_c*sigma = {rc * sv:.3e}, "
              f"C_c = |rho_c| r_c^4 sigma^2 = {Cc:.3e} (C_c*f = {Cc * fv:.3e}), a*(0.1 r_c) = {acc * 0.1 * rc:.1e}")
print("   C_c*f ~ constant => C_c ~ 1/f diverges in the tail: for free-field sources the QI fails in the far front tail")
print("   of a subluminal wall whatever sigma is (zone f <~ C_c*f * 32 pi^2 alpha^4/(3 N (L_P sigma)^2)).")
for alpha, N in ((0.1, 1), (0.01, 100)):
    for smin_lp in (1 / 50.0, 1 / 5.0e4):     # sigma in units of 1/L_P spanning the table above
        print(f"   alpha = {alpha}, N = {N}, sigma = {smin_lp:.0e}/L_P: violation zone f < "
              f"{0.05 * 32 * math.pi**2 * alpha**4 / (3 * N * smin_lp**2):.2e} x (C_c*f/0.05)")
