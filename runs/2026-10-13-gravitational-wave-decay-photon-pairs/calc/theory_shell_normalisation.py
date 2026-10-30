"""Theory facet: what angular distribution does B&O's top-hat f_s(k) (Theta = sqrt(2 pi^2 N/(omega_s sigma_omega))) imply?
Units: natural (hbar = c = 1). B&O commutator [a(k),a^dag(k')] = (2 pi)^3 2k delta^3(k-k'), so
N = sum_lambda Int d^3k /((2 pi)^3 2k) |f_lambda(k)|^2.
Test: f_lambda = Theta for k in [w - s/2, w + s/2], over solid angle dOmega, for n_hel helicities.
"""
import math

def theta_sq(N, w, sig, solid_angle, n_hel):
    # N = n_hel * Theta^2 * (solid_angle * Int k^2 dk /((2pi)^3 2k)) = n_hel*Theta^2*solid_angle*w*sig/(2*(2pi)^3)
    return N / (n_hel * solid_angle * w * sig / (2 * (2 * math.pi) ** 3))

N, w, sig = 1.0, 1.0, 1.0
B_O = 2 * math.pi ** 2 * N / (w * sig)
print("Inputs: N = %.1f, omega_s = %.1f, sigma_omega = %.1f (natural units, arbitrary energy unit; ratio only)" % (N, w, sig))
print("B&O Theta^2 = 2 pi^2 N/(omega_s sigma_omega) = %.8f" % B_O)
for name, om, nh in [("full sphere, 2 helicities", 4 * math.pi, 2),
                     ("full sphere, 1 helicity", 4 * math.pi, 1),
                     ("hemisphere, 2 helicities", 2 * math.pi, 2),
                     ("beam half-angle 0.1 rad, 2 helicities", 2 * math.pi * (1 - math.cos(0.1)), 2)]:
    print("  %-40s Theta^2 = %.8f  ratio to B&O = %.6f" % (name, theta_sq(N, w, sig, om, nh), theta_sq(N, w, sig, om, nh) / B_O))
print("Verification: full sphere + 2 helicities reproduces B&O's Theta^2 to", abs(theta_sq(N, w, sig, 4*math.pi, 2) - B_O) / B_O)
# Kinematics: s = 2 w^2 (1 - cos(psi)) for two gravitons of energy w with opening angle psi; K = |k1+k2| = 2 w cos(psi/2); s = 4w^2 - K^2
print("\nRelation s = 4 w^2 - K^2 (B&O S6): opening angle psi vs s/(4 w^2)")
for psi in (math.pi, math.pi/2, 1.0, 0.1, 0.01, 1e-3):
    s = 2 * w * w * (1 - math.cos(psi))
    K = 2 * w * math.cos(psi / 2)
    print("  psi = %.4g rad: s/(4w^2) = %.4g ; check 4w^2-K^2 -> %.4g" % (psi, s / (4 * w * w), (4 * w * w - K * K) / (4 * w * w)))
