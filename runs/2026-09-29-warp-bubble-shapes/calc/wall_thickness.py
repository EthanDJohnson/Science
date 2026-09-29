"""What wall thickness does to an Alcubierre bubble, beyond energy.

Run from the project root:
    python3 runs/2026-09-29-warp-bubble-shapes/calc/wall_thickness.py

Units: geometric (G = c = 1, lengths in metres) inside the calculations; SI in the printout.
Metric: ds^2 = -dt^2 + (dx - v f(r) dt)^2 + dy^2 + dz^2, r measured from the bubble centre.

1. Energy floor. For a spherical bubble, the Eulerian energy is exactly
       E = -(v^2/12) * integral f'(r)^2 r^2 dr.
   Minimising this with f = 1 in a flat interior r <= R and f = 0 at r >= R + D is the
   electrostatic problem of a spherical capacitor. The minimiser is f = C/r + const, and
       E_min(R, D) = -(v^2/12) * R (R + D) / D,
   which tends to -(v^2/12) R as D -> infinity (f = R/r, a 1/r tail reaching to infinity).
   So thickening has diminishing returns: no spherical profile beats v^2 R/12.
2. The largest Riemann component in the Eulerian frame, as a proxy for tides:
   (a) at the centre of a tanh bubble as its wall thickens inward;
   (b) around a bubble with the minimum-energy 1/r tail, versus a thin tanh wall.
   CORRECTION: this proxy is wrong for the ship. Inside the bubble the largest components are the
   "magnetic" part R_{0ijk}, which acts only on things moving relative to the ship, so section 2(a)
   overstates the stretch by up to many orders of magnitude (10 m wall, 2.3 m from the centre:
   3.6e6 g/m here against 0.04 g/m from the tidal tensor). interior_tides.py computes the tidal
   tensor properly, inside and outside the bubble; use its numbers.
3. Horizons at v = 2 for a thin tanh wall and the 1/r tail: position, surface gravity, and
   the share of the negative energy lying where the ship cannot send signals.
4. Quantum inequality: how the free-field bound scales with wall thickness.
"""
import math
import sys
import time

import numpy as np
import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from gr_tensors import C, G_NEWTON, HBAR, K_B, M_SUN, PLANCK_LENGTH, _orthonormal_frame, metrics

KG_PER_M = C**2 / G_NEWTON           # geometric length -> kg
M_JUP, M_EARTH = 1.89813e27, 5.9722e24
G0 = 9.80665


def mass_label(kg):
    kg = abs(kg)
    if kg >= 0.1 * M_SUN:
        return f"{kg / M_SUN:.2g} Suns"
    if kg >= 0.05 * M_JUP:
        return f"{kg / M_JUP:.2g} Jupiters"
    return f"{kg / M_EARTH:.2g} Earths"


def energy_tanh(R, D, v=1.0, n=400001):
    """Exact Eulerian energy (geometric) of Alcubierre's tanh profile, wall thickness D = 2/sigma."""
    s = 2.0 / D
    r = np.linspace(max(0.0, R - 40 * D), R + 40 * D, n)
    with np.errstate(over="ignore"):
        fp = s * (np.cosh(s * (r + R)) ** -2 - np.cosh(s * (r - R)) ** -2) / (2 * np.tanh(s * R))
    return -(v**2 / 12) * np.trapezoid(fp**2 * r**2, r)


def energy_capacitor(R, D, v=1.0):
    return -(v**2 / 12) * R * (R + D) / D


# ---------------------------------------------------------------- 1. energy floor
print("== 1. Energy against wall thickness, v = c (mass-energy of the negative-energy region, SI)")
for R in (5.0, 50.0):
    # numerical check of the capacitor minimum: integrate f = C/r + k between R and R + D
    D = R / 3
    rr = np.linspace(R, R + D, 200001)
    Cc = R * (R + D) / D
    num = -(1 / 12) * np.trapezoid((Cc / rr**2) ** 2 * rr**2, rr)
    assert abs(num / energy_capacitor(R, D) - 1) < 1e-6
    print(f"\n   flat ship region of radius R = {R:.0f} m ({2 * R:.0f} m across); best possible wall of thickness D")
    for D in (0.01, 1.0, R, 5 * R, 100 * R):
        b = energy_capacitor(R, D) * KG_PER_M
        print(f"   D = {D:>8.2f} m: {b:9.2e} kg  {mass_label(b)}")
    floor = -(1 / 12) * R * KG_PER_M
    print(f"   D = infinite  : {floor:9.2e} kg  {mass_label(floor)}  <- the floor, reached by f = R/r")
    tr = [(D, energy_tanh(R, D) * KG_PER_M) for D in (R / 5, R, 5 * R)]
    print("   Alcubierre's tanh wall (R = wall mid-radius) bottoms out near D ~ R and then rises again: "
          + ", ".join(f"D = {D:.0f} m -> {mass_label(e)}" for D, e in tr))
print("\n   All values are at v = c and scale as v^2. The tanh wall can dip below the floor only because")
print("   thickening it eats the flat interior (section 2a).")

# ---------------------------------------------------------------- 2. tidal gradients
print("\n== 2. Largest Riemann component (Eulerian frame, times c^2), v = c. NOT the tide on the ship:")
print("   inside the bubble this is the magnetic part, which overstates it; see interior_tides.py.")
st, s = metrics.alcubierre()
t, x, y, z, v = s["t"], s["x"], s["y"], s["z"], s["v"]
Rs, sig = s["R"], s["sigma"]
t0 = time.time()
rm = st.riemann()
flat = sp.ImmutableMatrix([rm[a][b][c][d] for a in range(4) for b in range(4) for c in range(4) for d in range(4)])
r_ = sp.symbols("r", positive=True)
shapes = {
    "tanh": metrics.alcubierre_top_hat(s),
    "inverse-r": sp.Lambda(r_, Rs / r_),
}
fns = {}
for name, lam in shapes.items():
    fns[name] = (st.compile(flat, functions={s["f"]: lam}, free=(v, Rs, sig)),
                 st.compile(st.g, functions={s["f"]: lam}, free=(v, Rs, sig)),
                 st.compile(st.eulerian_observer(), functions={s["f"]: lam}, free=(v, Rs, sig)))
# float64 rounds tanh(20) to exactly 1, which zeroes the exponentially small curvature inside and
# outside a thin tanh wall. Evaluate the tanh Riemann tensor in mpmath at enough digits instead.
rm_tanh_mp = st.compile(flat, functions={s["f"]: shapes["tanh"]}, free=(v, Rs, sig), modules="mpmath")
print(f"   (compiled the Riemann tensor for both shapes in {time.time() - t0:.0f} s)")


def riemann_components(shape, args):
    if shape != "tanh":
        return np.array(fns[shape][0](*args), dtype=float), None
    import mpmath
    rr = math.sqrt(sum(a * a for a in args[1:4]))
    mpmath.mp.dps = int(2 * args[6] * (rr + args[5]) / 2.302585) + 60   # digits to resolve 1 - tanh^2
    vals = [abs(c) for c in rm_tanh_mp(*[mpmath.mpf(a) for a in args])]
    top = max(vals)
    return np.array([float(c) for c in rm_tanh_mp(*[mpmath.mpf(a) for a in args])]), top


def peak_riemann(shape, point, vv, R, D):
    """Largest Riemann component in the Eulerian frame (1/m^2). Below float range, returns the
    largest coordinate component as an mpmath number (the frame is near-Minkowski there)."""
    _, g_fn, u_fn = fns[shape]
    args = (*point, vv, R, 2.0 / D)
    flat_vals, top = riemann_components(shape, args)
    if not np.any(flat_vals):
        return top
    g = np.array(g_fn(*args), dtype=float).reshape(4, 4)
    r_up = flat_vals.reshape(4, 4, 4, 4)
    r_low = np.einsum("ae,ebcd->abcd", g, r_up)
    e = _orthonormal_frame(g, np.array(u_fn(*args), dtype=float).reshape(4))
    frame = np.einsum("Aa,Bb,Cc,Dd,abcd->ABCD", e, e, e, e, r_low)
    return float(np.max(np.abs(frame)))    # 1/m^2


def tidal(p):                               # 1/m^2 -> (m/s^2) per metre
    return C**2 * p


def g_per_m(p):
    val = tidal(p) / G0
    try:
        return f"{float(val):9.2e}" if float(val) > 0 else f"~1e{int(__import__('mpmath').log10(val))}"
    except (OverflowError, ValueError):
        return f"~1e{int(__import__('mpmath').log10(val))}"


R = 50.0
print(f"\n   (a) At the ship's position (bubble centre), tanh profile, R = {R:.0f} m.")
print(f"       Offset 2 m from the exact centre, where symmetry would hide the gradient.")
for D in (1.0, 5.0, 10.0, 25.0, 50.0):
    p = peak_riemann("tanh", (0.0, 2.0, 1.0, 0.5), 1.0, R, D)
    print(f"       wall D = {D:>5.1f} m: {g_per_m(p):>9} g per metre")

print(f"\n   (b) Outside the bubble, R = {R:.0f} m, at 45 degrees off the direction of travel:")
print(f"       {'distance':>10} {'1/r tail (min energy)':>24} {'thin tanh wall, D = 1 m':>26}")
for dist in (100.0, 1e3, 1e4, 1e5, 1e6, 1e7):
    pt = (0.0, dist / math.sqrt(2), dist / math.sqrt(2), 0.0)
    a = tidal(peak_riemann("inverse-r", pt, 1.0, R, 1.0)) / G0
    b_txt = g_per_m(peak_riemann("tanh", pt, 1.0, R, 1.0)) if dist <= 1e3 else "smaller still"
    print(f"       {dist:>8.0e} m {a:>20.2e} g/m {b_txt:>22} g/m")
earth = 2 * 3.986e14 / 6.371e6**3
print(f"       For scale: Earth's own tidal gradient at its surface is {earth:.1e} (m/s^2)/m = {earth / G0:.1e} g/m.")

# ---------------------------------------------------------------- 3. horizons at v = 2
print("\n== 3. Horizons at v = 2 (forward light from the ship stalls where v(1 - f) = 1)")
vv = 2.0
for name, D in (("thin tanh wall", 1.0), ("1/r tail", None)):
    if D:
        sgm = 2.0 / D
        kappa = 2 * sgm * (1 - 1 / vv)
        r_h = R  # at v = 2 the horizon sits where f = 1/2, the middle of a thin tanh wall
        share = "~(D/R)^2, a few millionths (smoke-test scan: 3.0e-6 for R = 100 m)"
    else:
        r_h = R * vv / (vv - 1)
        kappa = (vv - 1) ** 2 / (vv * R)
        share = f">= {3 / 16 * (vv - 1) / vv:.0%} (everything ahead of the horizon)"
    temp = HBAR * C * kappa / (2 * math.pi * K_B)
    print(f"   {name:<15}: horizon at r = {r_h:6.1f} m, surface gravity {kappa:.3g} /m, "
          f"Hawking T = {temp:.1e} K, 1/(c kappa) = {1 / (C * kappa):.1e} s")
    print(f"   {'':<15}  share of the negative energy the ship cannot signal: {share}")

# ---------------------------------------------------------------- 4. quantum inequality
print("\n== 4. Free-field quantum inequality against wall thickness, v = c")
print("   Required |rho| ~ 1/D^2 (from section 1's integrand); the bound allows ~1/tau^4 with the")
print("   sampling time tau ~ 0.1 x curvature radius ~ D, so the mismatch grows as D^2.")
base = 65.9   # log10(required/allowed) at D = 1 m, from examples/.../lens-constraints_sources.py
for D in (1.0, 10.0, 50.0, 1e3):
    print(f"   wall D = {D:>6.0f} m: requirement exceeds the bound by 10^{base + 2 * math.log10(D):.1f}")
print(f"   The bound is met only for D <~ 51 Planck lengths = {51 * PLANCK_LENGTH:.1e} m at v = c (smoke test, qi_wall).")
