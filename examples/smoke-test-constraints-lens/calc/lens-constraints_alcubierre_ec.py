#!/usr/bin/env python3
"""lens-constraints: Alcubierre bubble -- energy conditions (NEC/WEC/SEC/DEC) and total energy.

Units: geometric, G = c = 1, all lengths in metres; energy density in 1/m^2, energy in m.
SI conversions use gr_tensors.to_si (c^4/G for energy and energy density, c^2/G for mass).

What it computes
 1. Eulerian energy density from gr_tensors vs the closed form quoted in [D-01].
 2. At chosen wall points and v in {0.1, 1, 2, 10}: Hawking-Ellis eigen-analysis of T^a_b and
    observer sampling (boosted observers) for NEC, WEC, SEC, DEC; toolkit scan as cross-check;
    Eulerian momentum density |J| vs |rho|.
 3. Total Eulerian energy on the t = 0 slice: 3D integral (n and 1.5n), 1D radial integral,
    and the thin-wall asymptotic E = -v^2 sigma R^2/36 - v^2 (pi^2-6)/(432 sigma) (derived here).
 4. SI scaling for R = 100 m, several wall thicknesses and speeds.
Run from the project root:  python3 runs/smoke-constraints/calc/lens-constraints_alcubierre_ec.py
"""
import math
import sys
import time

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from gr_tensors import C, G_NEWTON, HBAR, metrics, to_si

GM_SUN = 1.3271244e20            # m^3 s^-2, IAU 2015 nominal solar mass parameter (input constant)
M_SUN = GM_SUN / G_NEWTON        # kg
L_P = math.sqrt(HBAR * G_NEWTON / C**3)

print(__doc__.split("What it computes")[0])
print(f"constants: c={C} m/s, G={G_NEWTON} m^3/(kg s^2), hbar={HBAR} J s, L_P={L_P:.4e} m, M_sun={M_SUN:.5e} kg")

st, s = metrics.alcubierre()
t, x, y, z, v, R, sig, f, rs = (s[k] for k in ("t", "x", "y", "z", "v", "R", "sigma", "f", "r_s"))
rho = st.energy_density()
top = metrics.alcubierre_top_hat(s)
rr = sp.symbols("rr", positive=True)
fprime = sp.Lambda(rr, sp.diff(top(rr), rr))

# ---------------------------------------------------------------------------- 1
print("\n== 1. Eulerian rho: gr_tensors vs closed form [D-01]: rho = -v^2 (y^2+z^2) f'^2 / (32 pi r_s^2) (G=c=1)")
closed = -(v**2) * (y**2 + z**2) * fprime(rs) ** 2 / (32 * sp.pi * rs**2)
worst = 0.0
for vv in (0.5, 2.0, 10.0):
    p = {v: vv, R: 1.0, sig: 8.0}
    frho = st.compile(rho, p, {f: top})
    fcl = sp.lambdify((t, x, y, z), closed.subs(p).doit(), "numpy")
    for pt in [(0.0, 0.1, 0.95, 0.2), (0.0, -0.7, 0.6, 0.3), (0.3, 0.5 * vv * 0.3 + 0.9, 0.4, -0.2)]:
        a, b = float(frho(*pt)), float(fcl(*pt))
        worst = max(worst, abs(a - b) / max(abs(b), 1e-300))
print(f"   max relative difference over 9 points (v=0.5,2,10; R=1 m, sigma=8 /m): {worst:.1e}")


# ---------------------------------------------------------------------------- 2
def triad(gn, u):
    out = []
    for i in range(1, 4):
        e = np.zeros(4)
        e[i] = 1.0
        e = e + (e @ gn @ u) * u
        for q in out:
            e = e - (e @ gn @ q) * q
        out.append(e / math.sqrt(e @ gn @ e))
    return out


def fib_dirs(n):
    g = math.pi * (3 - math.sqrt(5))
    for i in range(n):
        zc = 1 - 2 * (i + 0.5) / n
        r = math.sqrt(1 - zc * zc)
        yield (r * math.cos(g * i), r * math.sin(g * i), zc)


def audit(gn, tn, n_eul, n_dirs=64, etas=(0.0, 0.5, 1.0, 2.0, 3.0)):
    """Energy conditions at one point from numeric g_ab, T_ab and the Eulerian n^a."""
    scale = max(1e-300, float(np.max(np.abs(tn))))
    tol = 1e-10 * scale
    gi = np.linalg.inv(gn)
    trace = float(np.sum(gi * tn))
    tri = triad(gn, n_eul)
    wec_min = sec_min = nec_min = math.inf
    dec_ok = True
    for eta in etas:
        for d in fib_dirs(n_dirs):
            e = sum(c * q for c, q in zip(d, tri))
            u = math.cosh(eta) * n_eul + math.sinh(eta) * e
            k = n_eul + e
            wec_min = min(wec_min, float(u @ tn @ u) / math.cosh(eta) ** 2)
            sec_min = min(sec_min, float(u @ (tn - 0.5 * trace * gn) @ u) / math.cosh(eta) ** 2)
            nec_min = min(nec_min, float(k @ tn @ k))
            F = -(gi @ tn @ u)  # energy-flux 4-vector  F^a = -T^a_b u^b
            if float(u @ tn @ u) < -tol or float(F @ gn @ F) > tol or float(F @ gn @ n_eul) > tol:
                dec_ok = False
    # Hawking-Ellis type from eigen-analysis of T^a_b
    lam, vec = np.linalg.eig(gi @ tn)
    if np.max(np.abs(lam.imag)) > 1e-9 * scale:
        he = "IV (complex eigenvalues)"
        rest = None
    else:
        norms = [float(np.real(vec[:, i]) @ gn @ np.real(vec[:, i])) for i in range(4)]
        tl = [i for i in range(4) if norms[i] < -1e-12]
        if len(tl) == 1:
            i0 = tl[0]
            rho0 = -float(lam[i0].real)
            ps = sorted(float(lam[i].real) for i in range(4) if i != i0)
            he, rest = "I", (rho0, ps)
        else:
            he, rest = "II/III (no timelike eigenvector)", None
    return dict(nec_min=nec_min, wec_min=wec_min, sec_min=sec_min, dec_ok=dec_ok,
                nec=nec_min >= -tol, wec=wec_min >= -tol, sec=sec_min >= -tol, he=he, rest=rest, scale=scale)


print("\n== 2. Energy-condition audit (R = 1 m, sigma = 8 /m; bubble centre at origin, t = 0)")
print("   observers: Eulerian n plus boosts of rapidity 0.5,1,2,3 in 64 directions; NEC with k = n + e (64 dirs)")
points = {
    "equator wall (0,0,R,0)": (0.0, 0.0, 1.0, 0.0),
    "45deg wall": (0.0, 1 / math.sqrt(2), 1 / math.sqrt(2), 0.0),
    "front axis wall (0,R,0,0)": (0.0, 1.0, 0.0, 0.0),
    "inner wall edge (0,0,0.8R,0)": (0.0, 0.0, 0.8, 0.0),
    "interior (0,0.2,0.1,0)": (0.0, 0.2, 0.1, 0.0),
    "exterior (0,0,2.5R,0)": (0.0, 0.0, 2.5, 0.0),
}
T_sym, g_sym, n_sym = st.stress_energy(), st.g, st.eulerian_observer()
for vv in (0.1, 1.0, 2.0, 10.0):
    p = {v: vv, R: 1.0, sig: 8.0}
    t0 = time.time()
    fT = st.compile(T_sym, p, {f: top})
    fg = st.compile(g_sym, p, {f: top})
    fn = st.compile(n_sym, p, {f: top})
    print(f"\n   v = {vv} (units of c); compiled in {time.time() - t0:.1f} s")
    print(f"   {'point':30s} {'rho_Eul':>11s} {'|J|/|rho|':>9s} {'NECmin':>11s} {'WECmin':>11s} {'SECmin':>11s}  N W S D  HE-type  rest-frame rho0, p_i")
    for name, pt in points.items():
        tn = np.array(fT(*pt), dtype=float).reshape(4, 4)
        gn = np.array(fg(*pt), dtype=float).reshape(4, 4)
        nn = np.array(fn(*pt), dtype=float).reshape(4)
        nn = nn / math.sqrt(-nn @ gn @ nn)
        a = audit(gn, tn, nn)
        rho_e = float(nn @ tn @ nn)
        tri = triad(gn, nn)
        J = np.array([-(nn @ tn @ q) for q in tri])
        ratio = np.linalg.norm(J) / abs(rho_e) if abs(rho_e) > 1e-14 else float("nan")
        flags = " ".join("Y" if ok else "n" for ok in (a["nec"], a["wec"], a["sec"], a["dec_ok"]))
        rest = "" if a["rest"] is None else f"{a['rest'][0]:+.3e}, " + ", ".join(f"{q:+.2e}" for q in a["rest"][1])
        if a["scale"] < 1e-12:
            print(f"   {name:30s} T_ab ~ 0 (max |T| = {a['scale']:.1e} /m^2): vacuum, all conditions hold")
            continue
        print(f"   {name:30s} {rho_e:+.4e} {ratio:9.2f} {a['nec_min']:+.4e} {a['wec_min']:+.4e} {a['sec_min']:+.4e}  {flags}  {a['he']:8s} {rest}")
    if vv == 2.0:  # cross-check with the toolkit's own scan at the equatorial wall point
        sc = st.energy_condition_scan(points["equator wall (0,0,R,0)"], params=p, functions={f: top})
        print(f"   toolkit energy_condition_scan at equator wall: {sc}")

# Peak |rho| scaling check: rho_eq(r=R) = -v^2 f'(R)^2/(32 pi), f'(R) = -sigma/2 * [1 - tanh^2(2 sigma R)]/tanh(sigma R) ~ -sigma/2
print("\n   peak Eulerian |rho| at equator wall vs thin-wall estimate v^2 sigma^2/(128 pi):")
for vv, ss in ((1.0, 8.0), (1.0, 16.0), (2.0, 16.0)):
    p = {v: vv, R: 1.0, sig: ss}
    val = st.evaluate(rho, (0.0, 0.0, 1.0, 0.0), p, {f: top})
    print(f"   v={vv}, sigma={ss}/m: rho={val:+.6e} /m^2; estimate {-vv**2 * ss**2 / (128 * math.pi):+.6e} /m^2")

# ---------------------------------------------------------------------------- 3
print("\n== 3. Total Eulerian energy on the t = 0 slice (v = 1)")


def e_radial(Rv, sv, vv=1.0, npts=400001):
    fp = sp.lambdify(rr, fprime(rr).subs({R: Rv, sig: sv}), "numpy")
    r = np.linspace(1e-9, Rv + 40.0 / sv, npts)
    return -(vv**2 / 12.0) * np.trapezoid(fp(r) ** 2 * r**2, r)


def e_asym(Rv, sv, vv=1.0):
    return -vv**2 * sv * Rv**2 / 36.0 - vv**2 * (math.pi**2 - 6) / (432.0 * sv)


for Rv, sv, half, n1 in ((1.0, 4.0, 2.4, 64), (1.0, 8.0, 1.8, 96)):
    p = {v: 1.0, R: Rv, sig: sv}
    res = []
    for n in (n1, int(round(1.5 * n1))):
        t0 = time.time()
        E = st.integrate_on_slice(rho, 0.0, [(-half, half)] * 3, n=n, params=p, functions={f: top})
        res.append(E)
        print(f"   R={Rv} m, sigma={sv} /m, box +-{half} m, n={n:3d} (spacing {2 * half / n:.4f} m): E3D = {E:+.6f} m  [{time.time() - t0:.1f} s]")
    print(f"   convergence |E(n)-E(1.5n)|/|E| = {abs(res[0] - res[1]) / abs(res[1]):.1e}")
    print(f"   1D radial -(v^2/12) int f'^2 r^2 dr = {e_radial(Rv, sv):+.6f} m ; thin-wall asymptotic = {e_asym(Rv, sv):+.6f} m")

print("   v^2 scaling (R=1, sigma=8, n=64): ", end="")
e1 = st.integrate_on_slice(rho, 0.0, [(-1.8, 1.8)] * 3, n=64, params={v: 1.0, R: 1.0, sig: 8.0}, functions={f: top})
e3 = st.integrate_on_slice(rho, 0.0, [(-1.8, 1.8)] * 3, n=64, params={v: 3.0, R: 1.0, sig: 8.0}, functions={f: top})
print(f"E(v=3)/E(v=1) = {e3 / e1:.6f} (expect 9)")

# thin-wall regime check of the asymptotic formula with the 1D integral at large sigma R
for sv in (50.0, 200.0):
    print(f"   sigma R = {sv:.0f}: 1D {e_radial(1.0, sv, npts=2000001):+.6f} m vs asymptotic {e_asym(1.0, sv):+.6f} m")

# ---------------------------------------------------------------------------- 4
print("\n== 4. SI requirements for a macroscopic bubble, R = 100 m (thin-wall formula validated above)")
print("   wall thickness Delta := 2/sigma (f falls from 0.88 to 0.12 across it)")
print(f"   {'v':>5s} {'Delta':>10s} {'E (geom, m)':>12s} {'E (J)':>11s} {'M (kg)':>11s} {'M/M_sun':>10s} {'peak |rho| (J/m^3)':>18s}")
for vv in (0.1, 1.0, 2.0, 10.0):
    for delta in (1.0, 1e-3):
        sv = 2.0 / delta
        E = e_asym(100.0, sv, vv)
        rho_pk = vv**2 * sv**2 / (128 * math.pi)
        print(f"   {vv:5.1f} {delta:8.0e} m {E:+12.4e} {to_si.energy_joules(E):+11.3e} {to_si.mass_kg(E):+11.3e} "
              f"{to_si.mass_kg(E) / M_SUN:+10.3e} {to_si.energy_density_j_per_m3(rho_pk):18.3e}")
print("   (QI-limited walls are handled in lens-constraints_qi_wall.py)")
