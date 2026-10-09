"""Falsifier C7-2 (scale): can an MM wormhole's mouth clock offset reach Delta_s = T_thru - d
within MM's own survival conditions?  SI units unless stated.

MM conditions (arXiv:2008.06618, p.7 and App. B, quoted in verdict):
  (a) mouth orbital angular velocity Omega << 1/ell (energy gap, c = 1), so radiation and
      Unruh quanta do not disrupt the throat  ->  Omega*ell/c << 1,
      and by the same Unruh logic a proper acceleration with a/(2 pi c) << c/ell;
  (b) U(1) radiation dE/dt = (2/3) r_e^2 d^2 Omega^4 (geometric), lifetime ~ (3/4) d^3/r_e^2.
"""
import math

c = 2.99792458e8
G = 6.674e-11
yr = 3.15576e7
ly = c * yr
Msun = 1.989e30
c5G = c**5 / G  # W

ell = 3e3 * ly          # MM eq. 3.27 (dossier Q-02)
r_e = 1.5e7             # m (Q-01)
M = 2.0e34              # kg (Q-04)
E_bin = 5e9 * c**2      # J (Q-02)
T_thru = math.pi * ell / c
d = 1e3 * ly
Ds = T_thru - d / c
Dctc = T_thru + d / c
gap = c / ell           # s^-1, energy gap 1/ell as an angular frequency
a_unruh = 2 * math.pi * c**2 / ell  # acceleration whose Unruh frequency a/(2 pi c) equals c/ell
print(f"T_thru = {T_thru/yr:.4g} yr; Delta_s = {Ds/yr:.4g} yr; Delta_CTC = {Dctc/yr:.4g} yr (d = 1000 ly)")
print(f"energy gap c/ell = {gap:.3g} s^-1; Unruh-equality acceleration 2 pi c^2/ell = {a_unruh:.3g} m/s^2")

def circling(beta, R, label):
    v = beta * c
    gam = 1 / math.sqrt(1 - beta**2)
    Om = v / R
    a = gam**2 * v**2 / R   # proper acceleration of circular motion
    eps = 1 - 1 / gam
    t_s = Ds / eps
    t_c = Dctc / eps
    # U(1) radiation, geometric: P = (2/3) r_e^2 R^2 (Om/c)^4  [dimensionless] * c^5/G
    P = (2 / 3) * r_e**2 * R**2 * (Om / c)**4 * c5G
    F = gam * M * v**2 / R
    Mc = v**2 * R / G
    E_photon = F * t_s * c
    print(f"[{label}] beta={beta}, R={R/ly:.4g} ly: Omega*ell/c = {Om*ell/c:.3g}; a/(2pi c^2/ell) = {a/a_unruh:.3g}; "
          f"eps = {eps:.4g}; t(Delta_s) = {t_s/yr:.3g} yr; t(Delta_CTC) = {t_c/yr:.3g} yr")
    print(f"    force = {F:.3g} N; central mass for a gravitational orbit = {Mc:.3g} kg = {Mc/Msun:.3g} Msun; "
          f"photon-rocket energy to supply it to Delta_s = {E_photon:.3g} J = {E_photon/(M*c**2):.3g} mouth rest energies")
    print(f"    dark-U(1) power = {P:.3g} W; radiated to Delta_s = {P*t_s:.3g} J = {P*t_s/(M*c**2):.3g} Mc^2")

circling(0.1, d, "candidate 0.1c circling")
circling(0.9, d, "0.9c circling within d")
circling(0.01, d, "gentle circling")
circling(0.03, d, "gentle circling")

# MM lifetime for Keplerian pair (App. B, B.34): T = (3/4) d^3 / r_e^2 (geometric, length) / c
for dd in (0.5 * ly, d):
    T = 0.75 * dd**3 / r_e**2 / c
    print(f"MM Keplerian lifetime at d = {dd/ly:.3g} ly: {T/yr:.3g} yr")

# Straight-line MTY trip at 0.9c with turnaround at acceleration a = 0.1 * a_unruh
beta = 0.9
gam = 1 / math.sqrt(1 - beta**2)
a = 0.1 * a_unruh
# hyperbolic motion: rapidity change 2*artanh(beta) for reversal, proper time tau = c*drap/a
drap = 2 * math.atanh(beta)
tau = c * drap / a
t_coord = 2 * (c / a) * math.sinh(drap / 2)
x_turn = (c**2 / a) * (math.cosh(drap / 2) - 1)
print(f"0.9c reversal at a = {a:.3g} m/s^2: proper time {tau/yr:.3g} yr, coordinate time {t_coord/yr:.3g} yr, "
      f"overshoot distance {x_turn/ly:.3g} ly (vs cruise time 1.5e4 yr)")

# Sgr A* ISCO parking (candidate route)
Mbh = 4.3e6 * Msun
GMc3 = G * Mbh / c**3
r_isco = 6 * G * Mbh / c**2
Om_isco = math.sqrt(G * Mbh / r_isco**3)
q = M / Mbh
eta = M * Mbh / (M + Mbh)**2
x = G * (Mbh + M) / (r_isco * c**2)
P_gw = (32 / 5) * eta**2 * x**5 * c5G
t_gw_from_isco = (5 / 256) * GMc3 * (1 + q)**2 / q / x**4  # leading-order quadrupole time to coalescence from r=6M
eps_isco = 1 - math.sqrt(1 - 3 / 6)
t_park = Ds / eps_isco
print(f"Sgr A* ISCO: period {2*math.pi/Om_isco:.4g} s; Omega*ell/c = {Om_isco*ell/c:.3g}; "
      f"quadrupole inspiral time from r=6M {t_gw_from_isco:.3g} s = {t_gw_from_isco/86400:.3g} d; "
      f"GW power {P_gw:.3g} W; GW energy over {t_park/yr:.3g} yr parking = {P_gw*t_park:.3g} J = {P_gw*t_park/(M*c**2):.3g} mouth rest energies")
print(f"E_bin = {E_bin:.3g} J for reference")
