"""Examiner lens: small calculations that test hidden premises of the problem-of-time question.

Units: SI unless stated; the Page-Wootters part uses hbar = 1 with energies as angular frequencies (rad/s).
1. Is gravitational time dilation a curvature effect? Potential (g*dh/c^2) vs tidal (curvature) term over 1 mm.
2. QGEM phase read as a superposition of proper times: dtau = hbar*dphi/(m c^2).
3. Fractional time dilation produced by a superposed QGEM-scale source vs best clock precision.
4. Clock in a superposition of heights (Zych et al. 2011 witness): T*dh needed for zero visibility.
5. Kuchar's naive two-time probability vs the Giovannetti-Lloyd-Maccone memory construction.
6. Smith-Ahmadi clock-system gravitational coupling scale for rest-mass vs internal energies.
"""
import sys
import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import page_wootters as pw  # noqa: E402

G = 6.67430e-11      # m^3 kg^-1 s^-2
c = 2.99792458e8     # m/s
hbar = 1.054571817e-34  # J s
M_E = 5.972e24       # kg
R_E = 6.371e6        # m
g = G * M_E / R_E**2  # m/s^2

print("1. Potential vs curvature contribution to redshift over dh = 1 mm at Earth's surface")
dh = 1e-3
first = g * dh / c**2                       # uniform-field (Rindler-like) term, no curvature needed
tidal = 0.5 * (2 * G * M_E / R_E**3) * dh**2 / c**2  # second-order term set by the tidal tensor
print(f"   g = {g:.4f} m/s^2; g*dh/c^2 = {first:.3e} (dimensionless); tidal term = {tidal:.3e}; ratio = {tidal/first:.2e}")

print("2. QGEM entangling phase as a proper-time difference")
m = 1e-14
for dphi, tau in [(0.23, 1.0), (0.57, 2.5)]:
    dtau = hbar * dphi / (m * c**2)
    print(f"   dphi = {dphi} rad over {tau} s -> dtau = {dtau:.2e} s; fractional {dtau/tau:.2e}")

print("3. Time dilation sourced by a superposed QGEM mass vs Sr clock precision")
for d in [200e-6, 450e-6]:
    frac = G * m / (c**2 * d)
    print(f"   m = 1e-14 kg, d = {d*1e6:.0f} um: G m/(c^2 d) = {frac:.2e}; vs 7.6e-21 -> gap {7.6e-21/frac:.1e}")
for M, d in [(1e-3, 1e-3), (1.0, 1e-2)]:
    print(f"   classical-scale source M = {M} kg at {d} m: G M/(c^2 d) = {G*M/(c**2*d):.2e}")

print("4. Clock in a superposition of heights: T*dh for first visibility zero (dtau = pi/omega)")
for name, f in [("Sr optical 429 THz", 429e12), ("Cs microwave 9.19 GHz", 9.192631770e9)]:
    w = 2 * np.pi * f
    Tdh = np.pi * c**2 / (w * g)
    print(f"   {name}: T*dh = {Tdh:.2e} m s (e.g. dh = 1 m held {Tdh:.2e} s)")

print("5. Kuchar naive vs GLM two-time conditional probability (qubit, d = 8 clock, hbar = 1)")
d, w = 8, 1.0
HS = 0.5 * np.array([[0, 1], [1, 0]], dtype=complex)  # Rabi frequency 1 rad/s -> eigen +-0.5
# clock energies must cancel system energies: need -(+-0.5) in spec(H_C); equally spaced with k0 = -3.5
HC = pw.equally_spaced_clock(d, w, k0=-3.5)
model = pw.PWModel(HC, HS)
Psi = model.physical_state(np.array([1, 0]))
Pi0 = np.diag([1, 0]).astype(complex)
j1, j2 = 1, 3
times = 2 * np.pi * np.arange(d) / (d * w)
t1, t2 = times[j1], times[j2]
naive = pw.kuchar_naive(model, Psi, t1, t2, Pi0, Pi0)
glm = pw.glm_two_time(HS, np.array([1, 0]), d, w, j1, j2)["P_b_given_a"][0, 0]
E, V = np.linalg.eigh(HS)
U = V @ np.diag(np.exp(-1j * E * (t2 - t1))) @ V.conj().T
textbook = abs(U[0, 0])**2
print(f"   t1 = {t1:.4f} s, t2 = {t2:.4f} s; Kuchar naive P(0|0) = {naive:.6f}; GLM = {glm:.6f}; textbook |<0|U|0>|^2 = {textbook:.6f}")

print("6. Smith-Ahmadi coupling lam*E = G E/(c^4 x): rest-mass vs internal energy, x = 1 mm")
x = 1e-3
for name, E_J in [("optical photon 429 THz", hbar * 2 * np.pi * 429e12),
                  ("Sr-87 atom rest energy", 87 * 1.66054e-27 * c**2),
                  ("1 g clock rest energy", 1e-3 * c**2)]:
    print(f"   {name}: E = {E_J:.3e} J; lam*E = {G*E_J/(c**4*x):.2e}")
