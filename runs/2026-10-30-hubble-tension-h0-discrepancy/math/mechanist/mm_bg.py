"""Independent flat-LCDM background written by the math checker (does not use the run's tools/).
Units: H in km/s/Mpc, distances in Mpc, c = 299792.458 km/s. Massless neutrinos, N_eff = 3.046,
T_CMB = 2.7255 K -> omega_gamma = 2.4728e-5. z_* from Hu & Sugiyama 1996; z_d from Eisenstein & Hu 1998.
"""
import math
from scipy.integrate import quad
from scipy.optimize import brentq

C = 299792.458
OG = 2.4728e-5
OR = OG * (1 + 0.2271 * 3.046)


def zstar(ob, om):
    g1 = 0.0783 * ob ** -0.238 / (1 + 39.5 * ob ** 0.763)
    g2 = 0.560 / (1 + 21.1 * ob ** 1.81)
    return 1048 * (1 + 0.00124 * ob ** -0.738) * (1 + g1 * om ** g2)


def zdrag(ob, om):
    b1 = 0.313 * om ** -0.419 * (1 + 0.607 * om ** 0.674)
    b2 = 0.238 * om ** 0.223
    return 1291 * om ** 0.251 / (1 + 0.659 * om ** 0.828) * (1 + b1 * ob ** b2)


def H(z, h, om):
    return 100 * math.sqrt(om * (1 + z) ** 3 + OR * (1 + z) ** 4 + (h * h - om - OR))


def sound_horizon(zx, h, ob, om):
    # integrate in a = 1/(1+z) to avoid the infinite range
    def f(a):
        z = 1 / a - 1
        R = 3 * ob / (4 * OG) * a
        cs = C / math.sqrt(3 * (1 + R))
        return cs / H(z, h, om) / a ** 2
    return quad(f, 1e-9, 1 / (1 + zx), epsabs=0, epsrel=1e-10, limit=400)[0]


def DM(zx, h, om):
    return quad(lambda z: C / H(z, h, om), 0, zx, epsabs=0, epsrel=1e-10, limit=400)[0]


def theta_star(h, ob, oc):
    om = ob + oc
    zs = zstar(ob, om)
    return sound_horizon(zs, h, ob, om) / DM(zs, h, om)


def h_from_theta(theta, ob, oc):
    return brentq(lambda h: theta_star(h, ob, oc) - theta, 0.4, 1.2, xtol=1e-13)


def rd(h, ob, om):
    return sound_horizon(zdrag(ob, om), h, ob, om)
