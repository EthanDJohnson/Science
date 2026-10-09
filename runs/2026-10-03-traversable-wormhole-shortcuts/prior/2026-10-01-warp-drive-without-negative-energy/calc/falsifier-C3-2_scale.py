"""Falsifier C3-2 (scale angle): is the photon rocket the floor for starting/stopping
a positive-energy shell, and at what scale do the alternatives sit?
Units: SI throughout. M = 4.511e27 kg (toolkit M_ADM, taken as input), R2 = 20 m.
"""
import math

c = 2.99792458e8          # m/s
G = 6.67430e-11           # m^3 kg^-1 s^-2
M = 4.511e27              # kg, shell ADM mass (toolkit rebuild)
R2 = 20.0                 # m, outer radius
Rs1 = 10.0                # m, inner radius
yr = 3.15576e7            # s
WORLD_YR = 6.0e20         # J, assumed world primary energy per year (~600 EJ)
L_SUN = 3.828e26          # W
M_SUN = 1.98892e30        # kg
P_SHELL = 3.87e39         # Pa, max tangential stress of the rebuilt shell (M-CONSTRAINTS-12)

def gamma(b):
    return 1.0 / math.sqrt(1 - b * b)

print("=== (1) Self-contained rocket: mass-ratio floor over exhaust speed ===")
# Isolated system, rest mass M_i -> shell M_f at speed b plus exhaust.
# Exact bound from E, p conservation with E_ex >= |p_ex| c: M_i/M_f >= gamma(1+b).
for b in (0.0239, 0.04):
    floor = gamma(b) * (1 + b)
    print(f"b = {b}: photon floor one leg gamma(1+b) = {floor:.6f}; sqrt((1+b)/(1-b)) = {math.sqrt((1+b)/(1-b)):.6f}")
    # relativistic rocket with exhaust speed u: M_i/M_f = exp(atanh(b)/u)
    for u in (1.0, 0.5, 0.1, 0.03):
        mr = math.exp(math.atanh(b) / u)
        print(f"   exhaust speed u = {u} c: one-leg mass ratio {mr:.6f}  (>= photon floor: {mr >= floor - 1e-12})")

print()
print("=== (2) Energy accounting at b = 0.04 (start + stop) ===")
b = 0.04
g = gamma(b)
p_leg = g * M * b * c
ke = (g - 1) * M * c**2
mr2 = (1 + b) / (1 - b)
E_photon = M * (mr2 - 1) * c**2     # M taken as final mass after both legs
print(f"momentum per leg gamma M v = {p_leg:.4e} kg m/s")
print(f"photon rocket start+stop: mass ratio {mr2:.5f}; exhaust energy {E_photon:.4e} J = {E_photon/WORLD_YR:.3e} world-years")
print(f"kinetic energy per leg (gamma-1)Mc^2 = {ke:.4e} J; 2KE = {2*ke:.4e} J = {2*ke/WORLD_YR:.3e} world-years")
print(f"ratio photon-exhaust/2KE = {E_photon/(2*ke):.2f}; log10(2KE/world-year) = {math.log10(2*ke/WORLD_YR):.2f}")

print()
print("=== (3) Beamed push on the shell (external momentum, shell mass ratio 1) ===")
# Perfect reflector, low speed: p = 2E/c per bounce (Doppler loss ignored at 4%)
E_beam_1 = p_leg * c / 2
for t_years in (10.0, 100.0):
    P = E_beam_1 / (t_years * yr)
    A = math.pi * R2**2
    I = P / A
    p_rad = 2 * I / c
    print(f"single-bounce beam, per leg over {t_years:.0f} yr: E = {E_beam_1:.3e} J, P = {P:.3e} W = {P/L_SUN:.2f} L_sun, "
          f"I on pi R2^2 = {I:.3e} W/m^2, radiation pressure {p_rad:.3e} Pa = {p_rad/P_SHELL:.2e} of shell stress")
for N in (10, 100, 1000):
    E = p_leg * c / (2 * N)
    print(f"   recycled N = {N} bounces: beam energy per leg >= max({E:.3e} J, KE {ke:.3e} J)")

print()
print("=== (4) Gravity assist (no exhaust, no energy spent by the shell) ===")
# Lab-frame Delta v <= 2 U for a deflector moving at U; need U >= b c / 2 to reach b from rest (ideal).
U_need = b * c / 2
print(f"deflector speed needed for b = 0.04 from rest (ideal head-on 2U): U >= {U_need/1e3:.0f} km/s")
# Hyperbolic deflection in deflector frame: tan(theta/2) = G Mb / (b_imp v^2); grazing b_imp = Rb.
for name, Mb, Rb in (("Sun-like star", M_SUN, 6.957e8), ("white dwarf 1 Msun", M_SUN, 5.8e6),
                     ("neutron star 1.4 Msun", 1.4 * M_SUN, 1.2e4)):
    v_rel = U_need
    t = G * Mb / (Rb * v_rel**2)
    theta = 2 * math.atan(t)
    dv = 2 * v_rel * math.sin(theta / 2)
    tidal = 2 * G * Mb / Rb**3 * R2
    selfg = G * M / R2**2
    print(f"{name}: grazing deflection {math.degrees(theta):.2f} deg, Delta v_max (deflector frame turn) {dv/1e3:.0f} km/s "
          f"of {2*v_rel/1e3:.0f} needed; tidal accel across shell {tidal:.2e} m/s^2 vs shell surface gravity {selfg:.2e} m/s^2")

print()
print("=== (5) Braking by interstellar drag (magsail-type, no exhaust) ===")
rho_ism = 1.6726e-21   # kg/m^3, 1 proton per cm^3
ly = 9.4607e15
for x_ly in (1.0, 10.0):
    x = x_ly * ly
    A = M * math.log(100.0) / (rho_ism * x)   # v -> v/100, full momentum coupling
    print(f"slow 0.04 c -> 4e-4 c over {x_ly:.0f} ly: effective area {A:.3e} m^2, radius {math.sqrt(A/math.pi):.3e} m "
          f"= {math.sqrt(A/math.pi)/1.496e11:.2e} AU")

print()
print("=== (6) Is the self-propelled GW-rocket level plausible in scale? ===")
# Bound: GW momentum flux <= GW energy flux / c, so Delta M_GW >= gamma M_f b (1+...) same as photons.
print(f"GW rocket start+stop radiated fraction of initial mass >= {1 - 1/mr2:.4f}")
