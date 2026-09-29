"""Falsifier C8-0: check the reframe's numbers and stress-test "more than 20 orders closer".

SI units throughout. Warp figures are Eulerian negative-energy magnitudes from
calc/lens-engineer_gaps.py (reference case R = 100 m, v = 10c) and the thick-wall floor
|E| >= v^2 R (R + D) / (12 D) (geometric G = c = 1) -> v^2 R / 12 as D -> inf.

Checks:
 1. 1 g accelerate/brake trip to 4.37 ly: ship time, mass ratio, energy per kg (photon rocket),
    and the same profile with realistic annihilation exhaust speeds (pion rocket ve = 0.33c, 0.58c).
 2. Energy for a 1e5 kg payload vs world primary energy (592 EJ/yr, engineer lens anchor).
 3. Like-for-like "demonstrated supply": antimatter fuel vs total antiprotons ever made
    (~16 ng, search-summary: Fermilab ~15 ng + CERN ~1 ng); warp negative energy vs Bressi
    Casimir energy 5.0e-15 J.
 4. Fuchs shell (4.49e27 kg at 0.04c): minimum kinetic energy to accelerate and brake it by
    external means (no self-acceleration is known), and trip time at 0.04c.
 5. Smallest superluminal warp: how small R must be (v -> 1, thick-wall floor) before the
    warp's need approaches a 1e5 kg rocket's.
"""
import math

G = 6.67430e-11
c = 299792458.0
YR = 3.15576e7
LY = 9.4607304725808e15
g0 = 9.80665
c4G = c**4 / G
E_world = 592e18  # J/yr
E_casimir = 4.99e-15  # J, Bressi plates (ideal), from engineer lens
m_pbar_ever = 16e-12  # kg (~16 ng), ACCESS: search-summary
lg = math.log10

d = 4.37 * LY
payload = 1e5  # kg

# 1. trip kinematics, accelerate to midpoint then brake
phi_half = math.acosh(1 + g0 * (d / 2) / c**2)  # rapidity at midpoint
tau = 2 * (c / g0) * phi_half / YR
t_earth = 2 * (c / g0) * math.sinh(phi_half) / YR
vpk = math.tanh(phi_half)
print(f"1 g trip to 4.37 ly: ship time {tau:.3f} yr, Earth time {t_earth:.3f} yr, peak {vpk:.4f} c, total rapidity {2*phi_half:.4f}")

print("\nRocket energy for a 1e5 kg payload (all fuel rest energy spent: (MR - 1) m c^2)")
rows = {}
for ve, lab in ((1.0, "photon rocket ve = c"), (0.58, "pion rocket ve = 0.58c (ideal nozzle)"), (0.33, "pion rocket ve = 0.33c (beamed core)")):
    MR = math.exp(2 * phi_half / ve)
    E = (MR - 1) * payload * c**2
    rows[lab] = E
    print(f"  {lab:40s} MR = {MR:9.3e}  E = {E:9.2e} J = 10^{lg(E/E_world):5.2f} world-years ; antimatter = {E/(2*c**2):.2e} kg")

# warp side (engineer lens, Eulerian negative energy)
warp = {
    "Bobrick-Martire flattened, optimal profile, Delta = 1 m (cheapest, lens)": 2.22e46,
    "thick-wall floor D -> inf, v^2 R / 12, R = 100 m, v = 10c": 10**2 * 100 / 12 * c4G,
    "thick-wall floor, v = 1c, R = 100 m (no flattening)": 1 * 100 / 12 * c4G,
    "White oscillating [speculative, brane-world], read by eye": 1e3 * c**2,
}
print("\nWarp Eulerian |E_-| (J) and world-years")
for k, E in warp.items():
    print(f"  {k:72s} {E:9.2e} J = 10^{lg(E/E_world):6.2f} world-years")

print("\nGap difference, energy vs world supply (warp gap minus rocket gap, orders)")
Ew_cheap = warp["Bobrick-Martire flattened, optimal profile, Delta = 1 m (cheapest, lens)"]
Ew_floor = warp["thick-wall floor D -> inf, v^2 R / 12, R = 100 m, v = 10c"]
for lab, Er in rows.items():
    print(f"  {lab:40s} vs cheapest warp: {lg(Ew_cheap/Er):5.2f} ; vs thick-wall floor: {lg(Ew_floor/Er):5.2f}")
Ewhite = warp["White oscillating [speculative, brane-world], read by eye"]
print(f"  photon rocket vs White [speculative]: {lg(Ewhite/rows['photon rocket ve = c']):5.2f} (negative = warp claim is CHEAPER)")

print("\nLike-for-like supply gaps (required / demonstrated of the same kind)")
for lab, Er in rows.items():
    m_anti = Er / (2 * c**2)
    print(f"  {lab:40s} antimatter {m_anti:.2e} kg vs ~16 ng ever: 10^{lg(m_anti/m_pbar_ever):5.1f}")
print(f"  cheapest warp negative energy vs Bressi Casimir energy: 10^{lg(Ew_cheap/E_casimir):5.1f}")
print(f"  -> difference (photon rocket): {lg(Ew_cheap/E_casimir) - lg(rows['photon rocket ve = c']/(2*c**2)/m_pbar_ever):5.1f} orders")
print(f"  -> difference (pion 0.33c):    {lg(Ew_cheap/E_casimir) - lg(rows['pion rocket ve = 0.33c (beamed core)']/(2*c**2)/m_pbar_ever):5.1f} orders")

# 4. Fuchs shell as a transport system
M, v = 4.49e27, 0.04 * c
gam = 1 / math.sqrt(1 - (v / c) ** 2)
KE = (gam - 1) * M * c**2
t_trip = 4.37 / 0.04
print(f"\nFuchs shell: M = {M:.2e} kg, v = 0.04c: kinetic energy {KE:.2e} J; accelerate + brake >= {2*KE:.2e} J = 10^{lg(2*KE/E_world):.2f} world-years")
print(f"  vs photon rocket 1e5 kg: 10^{lg(2*KE/rows['photon rocket ve = c']):.2f} times more; trip to 4.37 ly at 0.04c: {t_trip:.0f} yr (vs 3.58 yr ship time)")
MR_f = math.exp(2 * math.atanh(0.04))
print(f"  if accelerated by an onboard photon rocket: MR = {MR_f:.4f}, fuel energy {(MR_f-1)*M*c**2:.2e} J = 10^{lg((MR_f-1)*M*c**2/E_world):.2f} world-years")
print(f"  Fuchs shell rest energy {M*c**2:.2e} J = 10^{lg(M*c**2/E_world):.2f} world-years")

# 5. smallest superluminal bubble whose floor matches the photon rocket's need
Er = rows["photon rocket ve = c"]
R_eq = 12 * Er / c4G  # v = 1, thick-wall floor
print(f"\nThick-wall floor at v = 1c equals the 1e5 kg photon rocket's 3.5e23 J only for R = {R_eq:.1e} m")
for R in (100.0, 1.0, 1e-2):
    E = R / 12 * c4G
    print(f"  R = {R:7.2e} m, v = 1c floor: {E:.2e} J -> {lg(E/Er):5.1f} orders above the photon rocket")
