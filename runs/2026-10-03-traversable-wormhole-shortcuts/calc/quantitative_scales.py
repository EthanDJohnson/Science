"""Scale arithmetic for the Maldacena-Milekhin 2020 wormhole and Ford-Roman bound (SI units).
Inputs are quoted from arXiv:2008.06618 eq. (3.26)-(3.27) and arXiv:gr-qc/9510071."""
G = 6.67430e-11      # m^3 kg^-1 s^-2
c = 2.99792458e8     # m/s
hbar = 1.054571817e-34
Msun = 1.98847e30    # kg
ly = 9.4607e15       # m
yr = 3.15576e7       # s
g0 = 9.8             # m/s^2

l_planck = (hbar * G / c**3) ** 0.5
print("Planck length (m):", l_planck)

# MM 2020 tidal criterion: a ~ size / r_e^2 < 20 g, size ~0.5 m (their units c=1: a ~ size*c^2/r_e^2)
size = 0.5
r_e_min = (size * c**2 / (20 * g0)) ** 0.5
print("r_e_min from size*c^2/r_e^2 < 20 g (m):", r_e_min, " (paper: 1.5e7 m, 0.05 s)")
print("r_e_min in light-seconds:", r_e_min / c)

# Extremal mass M_e = r_e c^2 / G  (eq. 2.5, M_e = r_e/G_4 with c=1)
r_e = 1.5e7
M_e = r_e * c**2 / G
print("M_e for r_e=1.5e7 m (kg):", M_e, " = ", M_e / Msun, "solar masses")

# |E_bin| ~ 5e9 kg -> energy
E_bin_kg = 5e9
print("|E_bin| in J:", E_bin_kg * c**2, " ratio to M_e:", E_bin_kg / M_e)

# ell ~ 3e3 ly, gamma = ell/r_e
ell = 3e3 * ly
print("gamma = ell/r_e:", ell / r_e, " (paper 2e12)")
print("outside travel time pi*ell/c (years):", 3.14159 * ell / c / yr)
print("proper time pi*r_e/c (s):", 3.14159 * r_e / c)

# Ford-Roman: r0 <~ l_p/(2 f^2) * ... per quoted eq.(51): r0 <~ l_p / (2 f^2)? text: for f=0.01 -> 1e4 l_p = 1e-31 m
f = 0.01
print("1e4 l_p (m):", 1e4 * l_planck, " paper: 1e-31 m")

# Hypothetical magnetic charge from r_e = sqrt(pi q) l_p / g4, with g4 ~ O(1)? -> q = g^2 r_e^2/(pi l_p^2) (g undetermined, e.g. 0.3)
for g4 in (0.1, 0.3, 1.0):
    q = g4**2 * r_e**2 / (3.14159 * l_planck**2)
    print(f"q (g4={g4}): {q:.2e} magnetic flux quanta (needs g4 to be fixed by the model; illustrative)")
