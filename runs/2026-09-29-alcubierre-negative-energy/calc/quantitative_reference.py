"""Reference-case numbers for the Alcubierre negative-energy question (SI units).

Alcubierre tanh bubble, Eulerian negative energy, geometric E = -v^2 R^2/(18 Delta) * (c^4/G) with v in units of c
(brief.md convention; Pfenning-Ford linear ramp uses 12 instead of 18; Lobo-Visser estimate ~ v^2 R^2 sigma).
Also: ideal Casimir energy density and Planck-length wall energy, for orders-of-magnitude gaps.
"""
import math

G = 6.67430e-11
c = 2.99792458e8
hbar = 1.054571817e-34
Msun = 1.989e30
MJ = 1.898e27
lP = math.sqrt(hbar * G / c**3)  # Planck length, m
c4G = c**4 / G  # N (Planck force scale)


def E_alc(v, R, D, k=18.0):
    """Magnitude of negative Eulerian energy in J; v in c."""
    return v**2 * R**2 / (k * D) * c4G


def show(label, E):
    m = E / c**2
    print(f"{label:52s} E = {E:.3e} J  M = {m:.3e} kg = {m/Msun:.3e} Msun = {m/MJ:.3e} MJ")


print("Planck length lP = %.4e m ; c^4/G = %.4e N" % (lP, c4G))
R = 100.0
for v in (1.0, 10.0):
    for D, name in ((1.0, "Delta=1 m"), (100 * v * lP, "Delta=100 v lP (Pfenning-Ford QI)")):
        show(f"tanh k=18, R=100 m, v={v:g}c, {name}", E_alc(v, R, D, 18.0))
        show(f"linear ramp k=12, R=100 m, v={v:g}c, {name}", E_alc(v, R, D, 12.0))
# Pfenning-Ford quoted 6.2e62 v kg
print("Pfenning-Ford quoted: 6.2e62 kg at v=1 -> ratio to k=12 calc: %.3f" % (6.2e62 / (E_alc(1, R, 100 * lP, 12) / c**2)))

# Thick-wall floor (brief): E_min = v^2/12 * R(R+D)/D ; D>>R limit -> v^2 R/12 * c^4/G
for v in (1.0, 10.0):
    show(f"thick-wall limit D->inf (v^2 R/12), R=100 m, v={v:g}c", v**2 * R / 12 * c4G)

# Bubble-size scaling: R=1 m, v=1c, Delta=1 m
show("tanh k=18, R=1 m, v=1c, Delta=1 m", E_alc(1.0, 1.0, 1.0))

# Van Den Broeck quoted values
for name, kg in (("VdB E_II,- (kg)", 1.4e30), ("VdB E_II,+ (kg)", 4.9e30), ("VdB E_IV (kg)", 6.3e29)):
    print(f"{name:20s} {kg:.2e} kg = {kg/Msun:.2f} Msun = {kg/MJ:.0f} MJ ; E = {kg*c**2:.2e} J")
print("VdB reduction vs 6.2e62 kg: %.2e" % (6.2e62 / 1.4e30))

# Fell-Heisenberg
E_FH = 9.25e43
print("Fell-Heisenberg 9.25e43 J = %.3e kg = %.3e MJ = %.3e Msun" % (E_FH / c**2, E_FH / c**2 / MJ, E_FH / c**2 / Msun))

# Casimir ideal parallel plates
def u_casimir(a):
    """Energy per volume (J/m^3), negative: -pi^2 hbar c /(720 a^4); energy per area = -pi^2 hbar c /(720 a^3)."""
    return math.pi**2 * hbar * c / (720 * a**4)

for a in (1e-9, 1e-7, 1e-6):
    u = u_casimir(a)
    print(f"Casimir a={a:.0e} m: |u| = {u:.3e} J/m^3 = {u/c**2:.3e} kg/m^3; pressure = {u:.3e}*(3) Pa (P=3|u|)")
a = 1e-9
A = 1e-4  # 1 cm^2
print("1 cm^2 plates at 1 nm ideal: |E| = %.3e J" % (u_casimir(a) * a * A))

# Required peak Eulerian density ~ for VdB QI-satisfying: 6.6e93 kg/m^3 => J/m^3
rho = 6.6e93
print("VdB peak |rho| 6.6e93 kg/m^3 = %.2e J/m^3 ; ratio to 1 nm Casimir |u|: 10^%.1f" % (rho * c**2, math.log10(rho * c**2 / u_casimir(a))))

# Energy density of Alcubierre wall (tanh) scale: |rho| ~ v^2 R^2... peak ~ (v^2/32 pi) (c^4/G) (rho_cyl^2/r^2)(f')^2, f' ~ 1/(2 Delta)*... order of magnitude
for D in (1.0, 100 * lP):
    fprime = 1.0 / D
    rho_pk = (1 / (32 * math.pi)) * c4G * fprime**2 / c**2  # kg/m^3 for v=1, rho_cyl~r
    print(f"Alcubierre wall peak |rho| ~ (1/32pi) (c^4/G)/Delta^2 (v=1c), Delta = {D:.3e} m -> {rho_pk:.3e} kg/m^3 = {rho_pk*c**2:.3e} J/m^3 ; ratio to 1nm Casimir 10^{{{math.log10(rho_pk*c**2/u_casimir(a)):.1f}}}")
