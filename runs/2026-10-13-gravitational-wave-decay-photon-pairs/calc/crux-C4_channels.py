"""Crux C4: re-check the linear-channel vs fusion numbers the verdicts use, and
estimate the h1-h2 interference overlap for a Gaussian-band GW150914-like burst.

Units: SI for inputs; results are pair numbers (dimensionless).
Inputs: B&O GW150914 anchors (D-27): E = 2 Msun c^2, f = 150 Hz, sigma_w = 200 rad/s;
LVK E = 3 Msun c^2 (D-28). k_lin = 0.03385 (verdicts C4-0/1/2, calc files there).
"""
import math

G = 6.67430e-11       # m^3 kg^-1 s^-2
c = 2.99792458e8      # m/s
Msun = 1.98892e30     # kg
w = 2 * math.pi * 150.0   # rad/s (GW angular frequency, B&O w_s)
sigma = 200.0         # rad/s
k_lin = 67 / (630 * math.pi)

print(f"k_lin = 67/(630 pi) = {k_lin:.5f}")
for Emsun in (2.0, 3.0):
    E = Emsun * Msun * c**2
    x = G * E * w / c**5            # dimensionless G E w / c^5
    y = G * E * sigma / c**5
    N_lin = k_lin * x
    P_BO = (4 / 25) * x * y         # B&O eq.8 x T_eff (top hat), = (4/25) G^2 N^2 w^3 sigma
    print(f"E = {Emsun} Msun c^2: G E w/c^5 = {x:.4e}; N_lin = {N_lin:.3e} pairs; "
          f"P_BO = {P_BO:.3e} pairs; N_lin/P_BO = {N_lin / P_BO:.1f}")
    # Fusion share needed for fusion to match the linear channel
    print(f"   fusion would need a factor {N_lin / P_BO:.0f} above B&O to equal N_lin")

# Interference h1-h2: h1 spectrum centred at q0 = w (width sigma), the fusion (h1*h1)
# piece centred at q0 = 2w with width sqrt(2) sigma (Gaussian convolution).
# Normalised amplitude overlap of two Gaussians in q0 (power widths s1, s2):
#   O = Int A1 A2 / sqrt(Int A1^2 Int A2^2), A_i ~ exp(-(q0-m_i)^2/(4 s_i^2)) for
#   power ~ exp(-(q0-m)^2/(2 s^2)).
def overlap(m1, s1, m2, s2):
    # amplitudes a_i(q) = exp(-(q-m_i)^2/(4 s_i^2)); |a_i|^2 has rms width s_i
    a = 1 / (4 * s1**2) + 1 / (4 * s2**2)
    num = math.sqrt(math.pi / a) * math.exp(-(m1 - m2)**2 / (4 * (s1**2 + s2**2)))
    den = math.sqrt(math.sqrt(2 * math.pi) * s1 * math.sqrt(2 * math.pi) * s2)
    return num / den

O = overlap(w, sigma, 2 * w, math.sqrt(2) * sigma)
print(f"Gaussian q0-overlap of h1 (w, sigma) and h1*h1 (2w, sqrt2 sigma) amplitudes: {O:.3e}")
for ratio in (72.0, 107.0):
    bound = 2 * math.sqrt(ratio) * O
    print(f"  interference / fusion <= 2 sqrt(N_lin/P_fus) x O = {bound:.3f} (N_lin/P_fus = {ratio})")
# sharper (narrower) band check at sigma/w = 0.1
O2 = overlap(w, 0.1 * w, 2 * w, math.sqrt(2) * 0.1 * w)
print(f"same overlap at sigma/w = 0.1: {O2:.3e}")
