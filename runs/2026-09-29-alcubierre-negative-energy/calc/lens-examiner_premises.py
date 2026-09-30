"""Examiner lens: numerical checks on hidden premises.

1. Comoving-source fraction. In the Alcubierre metric ds^2 = -dt^2 + (dx - v f dt)^2 + dy^2 + dz^2
   (geometric units, G = c = 1), a worldline that rides with the bubble, x = x0 + v t, has
   ds^2 = (-1 + v^2 (1 - f)^2) dt^2, which is timelike only where f > 1 - 1/v.
   Where f < 1 - 1/v no material element can stay at fixed position relative to the bubble,
   so a source there cannot be "carried" by the ship. The same surface f = 1 - 1/v is the
   ship's forward horizon (forward photons have dx/dt - v = v f + 1 - v = 0).
   We compute the fraction of the Eulerian negative energy (density proportional to
   f'(r)^2 * sin^2(theta), same angular weight at every r) that lies where f < 1 - 1/v.
   Profiles: Alcubierre tanh (sigma R = 200, i.e. Delta ~ 1 m at R = 100 m, and sigma R -> inf),
   linear ramp, and Bobrick-Martire optimal f = min(r0/r, 1).
2. Free-field QI violation factor of a wall thicker than the Pfenning-Ford limit.
   Demand |rho| ~ v^2/Delta^2; QI bound ~ v^4/(alpha^4 Delta^4) (sampling time alpha*Delta/v),
   so demand/bound = (Delta/Delta_max)^2 with Delta_max = 1e2 v L_P (PF 1997 Eq. 23, alpha = 1/10).
3. Mean mass density of the QI-limited wall vs Planck density (SI).
4. Casimir plates: positive rest mass of the plates vs the |negative energy| in the gap
   (ideal conductors, T = 0; ideal formula is the most favourable case). SI.
"""
import math
import numpy as np

# ---------- 1. comoving-source fraction ----------
def frac_tanh(v, sigR, R=1.0, n=400001):
    sig = sigR / R
    r = np.linspace(max(0.0, R - 30 / sig), R + 30 / sig, n)
    f = (np.tanh(sig * (r + R)) - np.tanh(sig * (r - R))) / (2 * np.tanh(sig * R))
    fp = np.gradient(f, r)
    w = r**2 * fp**2
    mask = f < 1 - 1 / v
    return np.trapezoid(w * mask, r) / np.trapezoid(w, r)

def frac_tanh_thin(v):
    # sigma R -> inf: f ~ (1 - tanh x)/2, weight ~ sech^4 x, F(x) = tanh x - tanh^3 x / 3
    t0 = 1 - 2 * (1 - 1 / v)          # tanh x0 where f = 1 - 1/v
    F = lambda t: t - t**3 / 3
    return (F(1) - F(t0)) / (F(1) - F(-1))

def frac_linear(v):
    return 1 - 1 / v                   # f'^2 uniform in a thin wall

def frac_bm_optimal(v):
    return 1 - 1 / v                   # weight r0^2/r^2 from r0 to inf; f<1-1/v for r > r0/(1-1/v)

print("1. Fraction of Eulerian negative energy where no bubble-comoving timelike source can sit (f < 1 - 1/v)")
print(f"{'v/c':>6} {'tanh sR=200':>12} {'tanh thin':>10} {'linear':>8} {'BM opt':>8}")
for v in [1.0, 1.01, 1.5, 2, 5, 10, 100]:
    a = frac_tanh(v, 200.0) if v > 1 else 0.0
    b = frac_tanh_thin(v) if v > 1 else 0.0
    print(f"{v:6.2f} {a:12.4f} {b:10.4f} {frac_linear(v) if v>1 else 0:8.4f} {frac_bm_optimal(v) if v>1 else 0:8.4f}")

# ---------- 2. QI violation factor ----------
LP = 1.616255e-35  # m, Planck length (CODATA 2018)
print("\n2. Free-field QI (Pfenning-Ford, alpha = 1/10): Delta_max = 1e2 v L_P")
for v in [1, 10]:
    dmax = 1e2 * v * LP
    for D in [1.0, 1e-3, 1e-15]:
        print(f"  v = {v:>2}c  Delta = {D:.0e} m  Delta_max = {dmax:.2e} m  "
              f"demand/bound ~ (Delta/Delta_max)^2 = {(D/dmax)**2:.1e}  (10^{math.log10((D/dmax)**2):.1f})")

# ---------- 3. QI-limited wall density ----------
R = 100.0            # m
E_kg = 4.6e63        # kg, D-18, tanh at v = 10c, Delta = 100 v L_P
v = 10
dmax = 1e2 * v * LP
vol = 4 * math.pi * R**2 * dmax
rho_wall = E_kg / vol
G = 6.67430e-11; hbar = 1.054571817e-34; c = 2.99792458e8
rho_P = c**5 / (hbar * G**2)
print(f"\n3. QI wall at v = 10c: shell volume 4 pi R^2 Delta = {vol:.2e} m^3; mean |rho| = {rho_wall:.2e} kg/m^3;"
      f" Planck density = {rho_P:.2e} kg/m^3; ratio = {rho_wall/rho_P:.1e}")

# ---------- 4. Casimir plate mass vs gap energy deficit ----------
print("\n4. Casimir: plate rest mass per |negative gap energy| (ideal plates, T = 0), SI")
# assumed plate areal masses (illustrative inputs, not sourced): graphene monolayer 7.6e-7 kg/m^2 per sheet;
# gold 50 nm film (density 19300 kg/m^3) per plate.
plates = {"2 x graphene monolayer": 2 * 7.6e-7, "2 x 50 nm gold": 2 * 50e-9 * 19300}
for a in [1e-9, 1e-8, 1e-7, 1e-6]:
    EperA = math.pi**2 * hbar * c / (720 * a**3)   # J/m^2
    mdef = EperA / c**2                             # kg/m^2
    s = "  ".join(f"{k}: {m/mdef:.1e}" for k, m in plates.items())
    print(f"  gap {a:.0e} m: |E|/A = {EperA:.2e} J/m^2 = {mdef:.2e} kg/m^2 ; mass ratio  {s}")
