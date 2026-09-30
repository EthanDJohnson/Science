"""Engineer lens: required vs demonstrated, as orders of magnitude, for each negative-energy option.

Reference case (brief): flat ship region R = 100 m, v = 10c, wall Delta = 1 m or Delta at the
Pfenning-Ford QI limit Delta_QI = 100 v L_P.  SI units throughout unless marked geometric.
Formulas (geometric G = c = 1, v in c):
  Alcubierre tanh     |E| = v^2 R^2 / (18 Delta)            (brief; checked 3D in natario script)
  thick-wall floor    |E| = v^2 R (R + D) / (12 D)           (verified in natario script)
  Natario (same f)    |E| ~ 0.0056 v^2 R^4 sigma^3, sigma = 2/Delta   (our fit, natario script)
  peak |rho_alc|      = v^2 / (32 pi Delta^2)               (tanh, f'(R) ~ -sigma/2)
  SI: E[J] = E[m] * c^4/G ; M[kg] = E[m] * c^2/G
Demonstrated anchors (see engineer.md findings for sources):
  Casimir, largest parallel-plate test: Bressi 2002, A = 1.2 x 1.2 mm^2, gap 0.5 um (ideal plates)
  Casimir, smallest probed gap: Ederth 2000, 20 nm (ideal-plate density = upper bound)
  Squeezed vacuum: our order-of-magnitude estimate for a 15 dB, 1064 nm, ~100 MHz, 0.01 mm^2 beam
  World primary energy 2024: 592 EJ/yr.  QGP 14 GeV/fm^3.  Laser 1.1e23 W/cm^2.
"""
import math

G = 6.67430e-11
c = 299792458.0
hbar = 1.054571817e-34
lP = math.sqrt(hbar * G / c**3)
c4G = c**4 / G
c2G = c**2 / G
Msun, MJ = 1.989e30, 1.898e27
YR = 3.15576e7
L = lambda a, b: math.log10(abs(a) / abs(b))

R, v, D1 = 100.0, 10.0, 1.0
DQI = 100 * v * lP


def E_alc(v, R, D, k=18.0):  # J
    return v**2 * R**2 / (k * D) * c4G


def E_floor(v, R, D):  # J
    return v**2 * R * (R + D) / (12 * D) * c4G


def E_nat(v, R, D):  # J, thin-wall fit from natario script
    return 0.0056 * v**2 * R**4 * (2.0 / D) ** 3 * c4G


def kg(EJ):
    return EJ / c**2


def show(label, EJ):
    m = kg(EJ)
    print(f"  {label:58s} {EJ:9.2e} J = {m:9.2e} kg = {m/Msun:9.2e} Msun = {m/MJ:9.2e} MJ")


# ---------------- demonstrated anchors ----------------
casA = math.pi**2 * hbar * c / 720  # J m
u_cas = lambda a: casA / a**4  # |energy density| J/m^3
E_bressi = u_cas(0.5e-6) * 0.5e-6 * (1.2e-3) ** 2
u_ederth = u_cas(20e-9)
# squeezed vacuum (ours): |rho_-| ~ hbar w B (1 - e^{-2r})/2 / (A c)
lam, B, A_beam, dB = 1064e-9, 1e8, 1e-8, 15.0
w = 2 * math.pi * c / lam
sq = (1 - 10 ** (-dB / 10)) / 2
rho_sq = hbar * w * B * sq / (A_beam * c)
tau_sq = math.pi / (2 * w)  # length of each negative half-cycle of the 2w oscillation
E_world = 592e18  # J per year
P_world = E_world / YR
L_sun = 3.828e26
u_qgp = 14 * 1.602176634e-10 / 1e-45  # J/m^3
u_laser = 1.1e23 * 1e4 / c  # J/m^3
print("DEMONSTRATED ANCHORS (SI)")
print(f"  Casimir ideal energy, Bressi plates 1.44 mm^2 at 0.5 um: {E_bressi:.2e} J = {kg(E_bressi):.2e} kg")
print(f"  Casimir ideal |u| at 20 nm (Ederth gap, upper bound):     {u_ederth:.2e} J/m^3")
print(f"  Squeezed vacuum |rho_-| (ours, OOM): {rho_sq:.1e} J/m^3 for ~{tau_sq:.1e} s per half-cycle")
fr = 3 * hbar / (32 * math.pi**2 * c**3 * tau_sq**4)
print(f"    Ford-Roman bound at t0 = {tau_sq:.1e} s: {fr:.1e} J/m^3 (estimate lies {L(fr, rho_sq):.1f} orders inside)")
print(f"  World primary energy 2024: {E_world:.2e} J/yr = mass-energy {kg(E_world):.2e} kg/yr; mean power {P_world:.2e} W")
print(f"  QGP (LHC) {u_qgp:.2e} J/m^3 ; record laser I/c {u_laser:.2e} J/m^3")
print(f"  Planck length {lP:.3e} m ; Delta_QI(v=10) = {DQI:.2e} m")

# ---------------- required, reference case ----------------
print("\nREQUIRED at R = 100 m, v = 10c (magnitudes; Eulerian)")
req = {}
req["Alcubierre tanh, Delta = 1 m"] = E_alc(v, R, D1)
req["Alcubierre tanh, Delta = Delta_QI"] = E_alc(v, R, DQI)
req["Thick-wall floor, D = R"] = E_floor(v, R, R)
req["Thick-wall floor, D -> inf (v^2 R/12)"] = v**2 * R / 12 * c4G
req["Natario same profile, Delta = 1 m (ours)"] = E_nat(v, R, D1)
req["Bobrick-Martire flattened a_X=1+v^2, optimal profile /3"] = E_alc(v, R, D1) / (1 + v**2) / 3
req["Van Den Broeck region II, x v^2 (BM expectation)"] = 1.4e30 * v**2 * c**2
req["Van Den Broeck region II, v-independent (as published)"] = 1.4e30 * c**2
req["Lentz positive energy ~ v^2R^2/w (w = 1 m, C~1/18)"] = E_alc(v, R, D1)
req["Fell-Heisenberg example (positive Eulerian, own scale)"] = 9.25e43
req["Fuchs 2024 subluminal positive shell (v = 0.04c)"] = 4.49e27 * c**2
req["White oscillating [speculative], slide read by eye"] = 1e3 * c**2
for k_, E_ in req.items():
    show(k_, E_)

print("\nGAPS in total energy, log10(required / Bressi Casimir energy 5e-15 J) and vs world annual energy")
for k_, E_ in req.items():
    print(f"  {k_:58s} vs Casimir 10^{L(E_, E_bressi):5.1f} | vs world-year 10^{L(E_, E_world):5.1f}")

# ---------------- energy density ----------------
print("\nGAPS in energy density (peak Eulerian |rho|), SI")
for lab, D, vv in (("Alcubierre Delta=1 m, v=10", 1.0, 10), ("Alcubierre Delta=1 m, v=1", 1.0, 1), ("Alcubierre Delta_QI, v=10", DQI, 10)):
    rho = vv**2 / (32 * math.pi * D**2) * c4G
    print(f"  {lab:34s} |rho| = {rho:.1e} J/m^3 : vs Casimir 20 nm 10^{L(rho, u_ederth):.1f}, vs squeezed 10^{L(rho, rho_sq):.1f}, vs QGP (+ve) 10^{L(rho, u_qgp):.1f}")
rho_nat = (v**2 / (32 * math.pi)) * 0.8 * (R / D1) ** 2 / D1**2 * c4G
print(f"  Natario Delta=1 m, v=10 (~0.8 (R/D)^2 x Alcubierre, ours)  |rho| ~ {rho_nat:.1e} J/m^3 : vs Casimir 10^{L(rho_nat, u_ederth):.1f}")
rho_vdb = 6.6e93 * c**2
print(f"  Van Den Broeck peak 6.6e93 kg/m^3 = {rho_vdb:.1e} J/m^3 : vs Casimir 10^{L(rho_vdb, u_ederth):.1f}; vs QGP 10^{L(rho_vdb, u_qgp):.1f}")
M_lentz = kg(E_alc(v, R, D1))
rho_lentz = M_lentz / (4 * math.pi * R**2 * 1.0) * c**2
print(f"  Lentz-type positive shell (M = {M_lentz:.1e} kg in 4 pi R^2 x 1 m): {rho_lentz:.1e} J/m^3 vs QGP 10^{L(rho_lentz, u_qgp):.1f}")
rho_fuchs = 4.49e27 / (4 / 3 * math.pi * (20.0**3 - 10.0**3)) * c**2
print(f"  Fuchs shell (4.49e27 kg, 10-20 m): {rho_fuchs:.1e} J/m^3 vs QGP 10^{L(rho_fuchs, u_qgp):.1f}")

# self-gravity: Schwarzschild radius of the required |M|
print("\nSELF-GRAVITY of positive-energy shells: r_s = 2GM/c^2")
for lab, M, Rsh in (("Lentz-type, 7.5e31 kg, R = 100 m", M_lentz, 100.0), ("Fuchs, 4.49e27 kg, R2 = 20 m", 4.49e27, 20.0)):
    rs = 2 * G * M / c**2
    print(f"  {lab:36s} r_s = {rs:.2e} m ; r_s/R = {rs/Rsh:.2e}")

# ---------------- Casimir: net energy including plates ----------------
print("\nCASIMIR STACK: rest energy of plates vs Casimir deficit, per unit area of one cell")
for a, t, rho_p, lab in ((20e-9, 20e-9, 19300.0, "gold, a = t = 20 nm"), (0.5e-6, 1e-6, 7190.0, "Cr-like, a = 0.5 um, t = 1 um"),
                         (1e-9, 0.3e-9, 2200.0, "graphene-like t = 0.3 nm, a = 1 nm (ideal formula, optimistic)")):
    neg = u_cas(a) * a
    pos = rho_p * t * c**2
    net = (pos - neg) / (a + t)
    print(f"  {lab:60s} plate/deficit = 10^{L(pos, neg):.1f}; net stack density = +{net:.1e} J/m^3 (positive)")

# ---------------- wall thickness / fabrication ----------------
print("\nWALL THICKNESS vs demonstrated length control")
for lab, Lreq in (("Delta_QI at v=10c", DQI), ("Van Den Broeck curvature radius ~10 L_P", 10 * lP), ("Van Den Broeck neck 3e-15 m", 3e-15)):
    print(f"  {lab:40s} {Lreq:.1e} m : vs atomic 1e-10 m 10^{L(1e-10, Lreq):.1f}; vs LHC-probed ~1.5e-20 m 10^{L(1.5e-20, Lreq):.1f}")

# ---------------- duration ----------------
t_trip = 4.37 / v * YR
print(f"\nDURATION: trip at 10c lasts {t_trip:.2e} s; squeezed negative half-cycle {tau_sq:.1e} s -> 10^{L(t_trip, tau_sq):.1f}")

# ---------------- power and cost ----------------
print("\nPOWER to assemble the Delta = 1 m Alcubierre requirement")
Ereq = E_alc(v, R, D1)
for T, lab in ((1.0, "1 s"), (YR, "1 yr"), (100 * YR, "100 yr")):
    P = Ereq / T
    print(f"  over {lab:6s}: {P:.1e} W : vs world 10^{L(P, P_world):.1f}, vs Sun luminosity 10^{L(P, L_sun):.1f}")
print(f"  years of world energy: {Ereq/E_world:.1e} yr ; at $0.05/kWh: ${Ereq/3.6e6*0.05:.1e}")

# ---------------- which parameters shrink the gap ----------------
print("\nSCALING: radius R that a given energy budget can support (thick-wall floor, D -> inf, v = 1 and 10)")
for lab, E_ in (("Bressi Casimir 5e-15 J", E_bressi), ("world energy 1 yr", E_world), ("world energy to 2100 (75 yr)", 75 * E_world),
                ("Jupiter rest energy", MJ * c**2), ("Sun rest energy", Msun * c**2)):
    for vv in (1.0, 10.0):
        Rmax = 12 * E_ / (vv**2 * c4G)
        print(f"  {lab:30s} v = {vv:4.1f}c : R_max = {Rmax:.1e} m ({Rmax/lP:.1e} L_P)")
print("  and at the QI wall (tanh, Delta = 100 v L_P): R_max = sqrt(18 E Delta_QI/(v^2 c^4/G))")
for lab, E_ in (("world energy to 2100", 75 * E_world), ("Sun rest energy", Msun * c**2)):
    for vv in (1.0, 10.0):
        Rq = math.sqrt(18 * E_ * 100 * vv * lP / (vv**2 * c4G))
        print(f"  {lab:30s} v = {vv:4.1f}c : R_max = {Rq:.1e} m")
print("\nParameter elasticities of |E| (Alcubierre fixed Delta): dlogE/dlogv = 2, dlogE/dlogR = 2, dlogE/dlogDelta = -1;")
print("floor: dlogE/dlogR -> 1 as D/R -> inf; QI wall: dlogE/dlogv = 1, dlogE/dlogR = 2")
for lab, EJ in (("v 10c -> 1c", E_alc(1, R, D1)), ("R 100 m -> 1 m", E_alc(v, 1.0, D1)), ("Delta 1 m -> 100 m (floor D=R)", E_floor(v, R, R)),
                ("all three: v=1, R=1 m, D=R", E_floor(1, 1.0, 1.0)), ("probe: v=1, R=1 mm, D=R", E_floor(1, 1e-3, 1e-3))):
    print(f"  {lab:36s} |E| = {EJ:.1e} J = {kg(EJ):.1e} kg ; gap vs Casimir 10^{L(EJ, E_bressi):.1f}; vs world-year 10^{L(EJ, E_world):.1f}")
