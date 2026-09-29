"""Falsifier C5-0: can lab negative-energy phenomena supply a warp wall?

Units: SI throughout (J, kg, m, s). Wall demand figures are taken from the
candidate/dossier (peak |rho| = 1.2e44 J/m^3 for tanh, R = 100 m, Delta = 1 m,
v = 10c; cruise 1.38e7 s; E_- = 7.5e31 kg at Delta = 1 m, 10c).

A. Casimir per-cell energy balance.
   Ideal perfect-conductor energy per area |E/A| = pi^2 hbar c / (720 a^3).
   For any passive material the Lifshitz integrand ln(1 - r^2 exp(-2 q a))
   is monotone in r^2 <= 1 (imaginary-frequency reflection coefficients),
   so the ideal value is an UPPER bound on |E/A| for real plates.
   The plate mass per area is bounded below by (i) graphene, one atom thick;
   (ii) a generic floor: at least one electron + one proton per a^2
   (a mirror for wavelengths ~a needs carriers spaced <= a).
B. Squeezed vacuum / free EM field: Ford-Roman Lorentzian QI in Minkowski,
   rho_hat >= -3 hbar / (16 pi^2 c^3 tau^4) (EM = 2 x massless scalar 3/(32 pi^2)).
C. Negative-effective-mass BEC: T_00 = n (m c^2 + e_kin + e_int) > 0.
"""
import math

hbar = 1.054571817e-34      # J s
c = 2.99792458e8            # m/s
G = 6.67430e-11
me = 9.1093837015e-31       # kg
mp = 1.67262192369e-27      # kg
u = 1.66053906660e-27       # kg
LP = 1.616255e-35           # m
Msun = 1.989e30

def casimir_EA(a):
    """ideal |E/A| in J/m^2 (upper bound for real materials)"""
    return math.pi**2 * hbar * c / (720 * a**3)

print("=== A. Casimir per-cell balance (SI) ===")
# graphene areal mass: 2 C atoms per hexagonal cell, C-C bond 0.142 nm
acc = 0.142e-9
cell = 3 * math.sqrt(3) / 2 * acc**2
sigma_g = 2 * 12.011 * u / cell
print(f"graphene areal mass = {sigma_g:.3e} kg/m^2; rest energy = {sigma_g*c**2:.3e} J/m^2")
t_g = 0.335e-9  # effective thickness (graphite interlayer), m
for a in [0.335e-9, 1e-9, 20e-9, 100e-9, 0.5e-6]:
    EA = casimir_EA(a)
    ratio = sigma_g * c**2 / EA          # one plate per gap in an infinite stack
    net = (sigma_g * c**2 - EA) / (a + t_g)
    rho_gap = EA / a
    print(f"a = {a:.3e} m: ideal |E/A| = {EA:.3e} J/m^2, gap density -{rho_gap:.3e} J/m^3; "
          f"plate rest/deficit = {ratio:.3e}; stack net = +{net:.3e} J/m^3")

# gold plates 100 nm thick (typical experiment) at 100 nm gap
sig_au = 19300 * 100e-9
print(f"gold 100 nm film at 100 nm gap: rest/deficit = {sig_au*c**2/casimir_EA(100e-9):.3e}")

# generic floor: one electron (+ proton) per a^2 per plate
k = 720 / math.pi**2 / (hbar * c)
a_e = 1 / (k * me * c**2)
a_ep = 1 / (k * (me + mp) * c**2)
print(f"generic floor ratio = 720 m c^2 a /(pi^2 hbar c): <1 only for a < {a_e:.3e} m (electrons only), "
      f"a < {a_ep:.3e} m (electron+proton)")
for a in [1e-9, 1e-12, 1e-15]:
    print(f"   a = {a:.0e} m: floor ratio (e+p) = {k*(me+mp)*c**2*a:.3e}")

rho_wall = 1.2e44  # J/m^3, tanh R=100 m Delta=1 m v=10c (candidate figure)
a_need = (math.pi**2 * hbar * c / (720 * rho_wall))**0.25
print(f"gap for ideal Casimir density = {rho_wall:.1e} J/m^3: a = {a_need:.3e} m "
      f"(= {a_need/LP:.2e} L_P; proton radius 8.4e-16 m)")
print(f"   at that gap the e+p floor ratio = {k*(me+mp)*c**2*a_need:.3f}")
# NB below ~1e-15 m 'plates' would have to be nuclear matter; nuclear density
rho_nuc = 2.3e17  # kg/m^3
sig_nuc = rho_nuc * a_need   # plate at least as thick as the gap
print(f"   nuclear-density plate as thick as the gap: rest/deficit = "
      f"{sig_nuc*c**2/casimir_EA(a_need):.3e}")

E_minus = 7.5e31  # kg, Delta = 1 m, 10c (D-17)
# area of ideal 0.335 nm graphene cells needed and their positive mass
A_need = E_minus * c**2 / casimir_EA(0.335e-9)
print(f"cells to hold |E_-| = {E_minus:.1e} kg at a = 0.335 nm: area {A_need:.3e} m^2, "
      f"plate mass {A_need*sigma_g:.3e} kg = {A_need*sigma_g/Msun:.3e} M_sun "
      f"(Schwarzschild radius {2*G*A_need*sigma_g/c**2:.3e} m)")

print("\n=== B. Free-field EM quantum inequality (Minkowski, Lorentzian sampling) ===")
def qi_em(tau):
    return 3 * hbar / (16 * math.pi**2 * c**3 * tau**4)
for label, tau in [("1 fs", 1e-15), ("wall crossing at 10c, Delta=1 m: Delta/(v c)", 1.0/(10*c)),
                   ("wall light-crossing Delta/c", 1.0/c), ("cruise 1.38e7 s", 1.38e7)]:
    b = qi_em(tau)
    print(f"tau = {tau:.3e} s ({label}): |rho| allowed <= {b:.3e} J/m^3; "
          f"demand/allowed = {rho_wall/b:.3e} (10^{math.log10(rho_wall/b):.1f})")
tau_max = (3 * hbar / (16 * math.pi**2 * c**3 * rho_wall))**0.25
print(f"1.2e44 J/m^3 allowed only for tau <= {tau_max:.3e} s")
print(f"validity check at Delta = 1 m, 10c: c*tau = {c/(10*c):.2f} m vs curvature scale ~Delta = 1 m "
      f"(tau0 = 0.1 x that -> {0.01:.2f} m): flat-space QI regime applies")
tau01 = 0.1 * 1.0 / (10 * c)
print(f"with tau0 = 0.1 Delta/(v c) = {tau01:.3e} s: allowed {qi_em(tau01):.3e} J/m^3, "
      f"ratio 10^{math.log10(rho_wall/qi_em(tau01)):.1f}")

print("\n=== C. 'Negative effective mass' BEC (87Rb) ===")
m_rb = 86.909 * u
n = 1e20   # m^-3, typical peak BEC density (order of magnitude)
e_rest = m_rb * c**2
e_kin = hbar * 2 * math.pi * 1e3   # ~ h x 1 kHz per atom, generous upper scale of SOC band energies
print(f"rest energy/atom {e_rest:.3e} J; band/kinetic energy scale {e_kin:.3e} J; ratio {e_kin/e_rest:.1e}")
print(f"T_00 = n (m c^2 +/- band) = {n*(e_rest - e_kin):.3e} J/m^3 > 0 (mass density {n*m_rb:.2e} kg/m^3)")
