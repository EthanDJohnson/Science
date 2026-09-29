"""Tidal forces on a ship inside an Alcubierre bubble, and on objects it passes.

Run from the project root:
    python3 runs/2026-09-29-warp-bubble-shapes/calc/interior_tides.py

What is computed. A ship riding in the bubble is in free fall, so it feels no overall g-force.
What can hurt it is the tidal tensor, the difference in pull between neighbouring points. For an
observer with 4-velocity u, geodesic deviation gives the relative acceleration of two points a
separation xi apart as
    d^2 xi^i / d tau^2 = -E^i_j xi^j,   E_ij = R_{i0j0} in the observer's orthonormal frame.
Times c^2, E is an acceleration per metre of separation (1/s^2); divided by g it is "g per
metre". Negative eigenvalues stretch, positive ones squeeze.
- Inside the bubble the ship moves with the Eulerian observers, so their frame is the ship's.
- Outside, objects at rest relative to the distant stars are the static observers, u ~ d/dt.

Correction to wall_thickness.py. That script reported the largest Riemann component of any kind.
Inside the bubble the largest components are the "magnetic" part R_{0ijk}, which is first order in
the tiny deviation of the metric from flat, while the tidal tensor is second order. The magnetic
part acts only on things moving relative to the observer, so it overstated the stretch on the
ship by up to many orders of magnitude (section 5 shows both at the same point).

Precision. The tidal tensor is a near-cancellation of first-order terms, and float64 rounds
tanh(20) to exactly 1. Everything below, including the frame transformation, runs in mpmath with
enough digits, and only the final 3x3 tensor is converted to floats.

Units: geometric (G = c = 1, metres) in the curvature; SI in the printout.
"""
import math
import sys
import time

import mpmath
import numpy as np
import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from gr_tensors import C, _orthonormal_frame, metrics

G0 = 9.80665
EARTH_TIDE = 2 * 3.986e14 / 6.371e6**3 / G0          # Earth's own vertical tidal gradient at its surface, g/m
STEEL = {"density": 7800.0, "yield_pa": 2.5e8}       # structural steel
CARBON = {"density": 1600.0, "yield_pa": 3.5e9}      # carbon-fibre composite, along the fibres


def riemann_flat(st):
    rm = st.riemann()
    return sp.ImmutableMatrix([rm[a][b][c][d] for a in range(4) for b in range(4) for c in range(4) for d in range(4)])


def mp_tidal(r_up_flat, g, u):
    """E_ij for observer u, all in mpmath. The spatial triad is Gram-Schmidt on d/dx, d/dy, d/dz."""
    def dot(a, b):
        return sum(g[i][j] * a[i] * b[j] for i in range(4) for j in range(4))
    e0 = [x / mpmath.sqrt(-dot(u, u)) for x in u]
    triad = []
    for k in (1, 2, 3):
        e = [mpmath.mpf(1) if i == k else mpmath.mpf(0) for i in range(4)]
        e = [ei + dot(e, e0) * fi for ei, fi in zip(e, e0)]              # remove the e0 part (e0.e0 = -1)
        for f in triad:
            e = [ei - dot(e, f) * fi for ei, fi in zip(e, f)]
        norm = mpmath.sqrt(dot(e, e))
        triad.append([x / norm for x in e])
    R_up = [[[[r_up_flat[((a * 4 + b) * 4 + c) * 4 + d] for d in range(4)] for c in range(4)] for b in range(4)]
            for a in range(4)]
    R_low = [[[[sum(g[a][e] * R_up[e][b][c][d] for e in range(4)) for d in range(4)] for c in range(4)]
              for b in range(4)] for a in range(4)]
    E = np.zeros((3, 3))
    for i in range(3):
        for j in range(i, 3):
            val = mpmath.fsum(R_low[a][b][c][d] * triad[i][a] * e0[b] * triad[j][c] * e0[d]
                              for a in range(4) for b in range(4) for c in range(4) for d in range(4))
            E[i, j] = E[j, i] = float(val)
    return E


def worst(E):
    lam = np.linalg.eigvalsh(E)
    top = lam[np.argmax(np.abs(lam))]
    return abs(C**2 * top / G0), ("stretch" if top < 0 else "squeeze")


def show(val):
    return "~0" if val < 1e-6 else f"{val:.2g}"


# ---------------------------------------------------------------- 0. sign convention check
print("== 0. Sign check: Schwarzschild, static observer at r = 10 M (expect -2M/r^3 radial, +M/r^3 sideways)")
sst, ss = metrics.schwarzschild()
pt = (0.0, 10.0, math.pi / 2, 0.0)
r_up = np.array(sst.compile(riemann_flat(sst), {ss["M"]: 1.0})(*pt), dtype=float).reshape(4, 4, 4, 4)
g = np.array(sst.compile(sst.g, {ss["M"]: 1.0})(*pt), dtype=float).reshape(4, 4)
u = np.array(sst.compile(sst.eulerian_observer(), {ss["M"]: 1.0})(*pt), dtype=float).reshape(4)
e = _orthonormal_frame(g, u)
E_s = np.einsum("Aa,Bb,Cc,Dd,abcd->ABCD", e, e, e, e, np.einsum("ae,ebcd->abcd", g, r_up))[1:, 0, 1:, 0]
print(f"   radial {E_s[0, 0]:+.6f}, sideways {E_s[1, 1]:+.6f} {E_s[2, 2]:+.6f}")
assert abs(E_s[0, 0] + 0.002) < 1e-9 and abs(E_s[1, 1] - 0.001) < 1e-9 and abs(E_s[2, 2] - 0.001) < 1e-9

# ---------------------------------------------------------------- set-up: two wall shapes
st, s = metrics.alcubierre()
v, Rs, sig = s["v"], s["R"], s["sigma"]
r_ = sp.symbols("r", positive=True)
SHAPES = {"tanh": metrics.alcubierre_top_hat(s), "inverse-r": sp.Lambda(r_, Rs / r_)}
t0 = time.time()
flat = riemann_flat(st)
fns = {}
for name, lam in SHAPES.items():
    fn = {s["f"]: lam}
    fns[name] = (st.compile(flat, functions=fn, free=(v, Rs, sig), modules="mpmath"),
                 st.compile(st.g, functions=fn, free=(v, Rs, sig), modules="mpmath"),
                 st.compile(st.eulerian_observer(), functions=fn, free=(v, Rs, sig), modules="mpmath"))
print(f"\n(compiled the Riemann tensor for both wall shapes in {time.time() - t0:.0f} s)")


def tide(shape, x, y, vv, R, D, observer="ship"):
    """Worst tidal gradient (g per metre) at (x, y, 0) at t = 0, for the ship (Eulerian) or a static object."""
    rm_fn, g_fn, u_fn = fns[shape]
    sigma = 2.0 / D
    rr = math.hypot(x, y)
    mpmath.mp.dps = (int(2 * sigma * (rr + R) / 2.302585) if shape == "tanh" else 0) + 50
    args = [mpmath.mpf(a) for a in (0.0, x, y, 0.0, vv, R, sigma)]
    r_up_flat = list(rm_fn(*args))
    gm = g_fn(*args)
    g = [[gm[i, j] for j in range(4)] for i in range(4)]
    if observer == "ship":
        um = u_fn(*args)
        u = [um[i] for i in range(4)]
    else:
        u = [mpmath.mpf(1), mpmath.mpf(0), mpmath.mpf(0), mpmath.mpf(0)]   # at rest relative to the stars
    return worst(mp_tidal(r_up_flat, g, u))


# ---------------------------------------------------------------- 1. inside the bubble
R, V = 50.0, 1.0
radii = [2.3, 5, 10, 15, 20, 25, 30, 35, 40, 45]
walls = [1.0, 2.0, 5.0, 10.0]
print(f"\n== 1. Tidal gradient on the ship, bubble radius R = {R:.0f} m, v = c (g per metre; ~0 means below 1e-6)")
print("   worst of the direction of travel and the perpendicular, at each distance from the centre")
t0 = time.time()
table = {}
for D in walls:
    for r in radii:
        table[(D, r)] = max(tide("tanh", r, 0.0, V, R, D), tide("tanh", 0.0, r, V, R, D))
print(f"   {'distance from centre':>22} " + " ".join(f"{f'wall {D:g} m':>11}" for D in walls))
for r in radii:
    print(f"   {r:>20.1f} m " + " ".join(f"{show(table[(D, r)][0]):>11}" for D in walls))
kinds = {k for (val, k) in table.values() if val >= 1e-6}
print(f"   (every non-negligible entry is a {'/'.join(sorted(kinds))}; {time.time() - t0:.0f} s)")

# ---------------------------------------------------------------- 2. what the numbers mean
print("\n== 2. How far from the centre each level holds")
levels = {0.1: "people barely notice", 1.0: "people feel a strong stretch", 100.0: "lethal to people"}
for D in walls:
    parts = []
    for lvl in levels:
        inside = [r for r in radii if table[(D, r)][0] < lvl]
        ok = max(inside) if inside and inside == radii[:len(inside)] else None
        parts.append(f"<{lvl:g} g/m out to {ok:g} m" if ok else f"<{lvl:g} g/m nowhere")
    print(f"   wall {D:>4g} m: " + "; ".join(parts))


def longest_rod(material, grad):
    """Longest uniform rod that survives a gradient: the stress at its middle is rho T L^2 / 8."""
    return math.sqrt(8 * material["yield_pa"] / (material["density"] * grad * G0))


print("\n   Longest uniform rod that survives, and the pull at the waist of a 70 kg, 1.8 m person:")
for grad in (0.1, 1.0, 100.0, 1e5):
    print(f"   {grad:>8.3g} g/m: steel {longest_rod(STEEL, grad):7.3g} m, carbon fibre {longest_rod(CARBON, grad):7.3g} m; "
          f"person pulled with {70 * grad * 1.8 / 8:8.3g} kgf")

# ---------------------------------------------------------------- 3. outside, on objects it passes
print(f"\n== 3. Tides on objects at rest that the bubble passes (R = {R:.0f} m, v = c, 45 deg off the path)")
print(f"   {'distance':>10} {'1/r tail (min energy)':>23} {'thin tanh wall, D = 1 m':>25}")
tail = {}
for dist in (100.0, 1e3, 1e4, 1e5, 1e6, 1e7):
    x = y = dist / math.sqrt(2)
    tail[dist] = tide("inverse-r", x, y, V, R, 1.0, observer="static")[0]
    thin = show(tide("tanh", x, y, V, R, 1.0, observer="static")[0]) if dist <= 1e3 else "~0"
    print(f"   {dist:>8.0e} m {tail[dist]:>19.2e} g/m {thin:>21} g/m")
slope = math.log(tail[1e7] / tail[1e6]) / math.log(10)
for label, level in (("100 g/m (lethal to people)", 100.0), ("Earth's own surface tide", EARTH_TIDE)):
    reach = 1e6 * (level / tail[1e6]) ** (1 / slope)
    print(f"   the 1/r tail exceeds {label} out to about {reach / 1e3:,.0f} km (falls as r^{slope:.2f})")

# ---------------------------------------------------------------- 4. speed scaling
print("\n== 4. Speed scaling of the tide on the ship (wall 10 m, 10 m from the centre)")
base = tide("tanh", 10.0, 0.0, 1.0, R, 10.0)[0]
for vv in (0.1, 1.0, 10.0):
    val = tide("tanh", 10.0, 0.0, vv, R, 10.0)[0]
    print(f"   v = {vv:>4g} c: {val:.3g} g/m  (x{val / base:.3g})")

# ---------------------------------------------------------------- 5. the earlier measure, for comparison
print("\n== 5. Earlier measure vs the tidal tensor, 2.3 m from the centre, v = c")
st_f, rm_float = st, st.compile(flat, functions={s["f"]: SHAPES["tanh"]}, free=(v, Rs, sig), modules="mpmath")
g_f = st.compile(st.g, functions={s["f"]: SHAPES["tanh"]}, free=(v, Rs, sig))
u_f = st.compile(st.eulerian_observer(), functions={s["f"]: SHAPES["tanh"]}, free=(v, Rs, sig))
for D in (5.0, 10.0):
    sigma = 2.0 / D
    args = (0.0, 2.0, 1.0, 0.5, 1.0, R, sigma)
    mpmath.mp.dps = int(2 * sigma * (2.3 + R) / 2.302585) + 50
    r_up = np.array([float(c) for c in rm_float(*[mpmath.mpf(a) for a in args])]).reshape(4, 4, 4, 4)
    g = np.array(g_f(*args), dtype=float).reshape(4, 4)
    e = _orthonormal_frame(g, np.array(u_f(*args), dtype=float).reshape(4))
    frame = np.einsum("Aa,Bb,Cc,Dd,abcd->ABCD", e, e, e, e, np.einsum("ae,ebcd->abcd", g, r_up))
    largest = C**2 * np.max(np.abs(frame)) / G0
    magnetic = C**2 * np.max(np.abs(frame[0, 1:, 1:, 1:])) / G0
    tidal = tide("tanh", 2.0, 1.0, 1.0, R, D)[0]
    print(f"   wall {D:>4g} m: largest component {largest:.2g} g/m (magnetic part {magnetic:.2g}); tidal tensor {show(tidal)} g/m")
