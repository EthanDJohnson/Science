#!/usr/bin/env python3
"""Constraints lens: quantum-inequality wall limit and horizons for the Alcubierre reference case,
and momentum / proper-time bookkeeping for the positive-energy shell.

Units: geometric (G = c = 1, metres) for curvature and densities, converted to SI with to_si.
1. Alcubierre, R = 100 m, v = 10, tanh wall with Delta = 2/sigma. At the wall point of largest
   |rho_E| (on the y axis, r = R): Eulerian rho, curvature radius r_c (gr_tensors.curvature_at),
   Ford-Roman bound with tau0 = alpha r_c (alpha = 0.1). Scaling rho ~ sigma^2, r_c ~ 1/sigma
   (checked at two sigmas) then gives the largest wall thickness Delta_QI that the free-field QI
   allows, and the Eulerian energy E = -v^2 R^2/(18 Delta) there.
2. Horizons of the v = 10 bubble on its axis (comoving 1+1 river u(xi) = -v(1 - f)), surface
   gravities and Hawking temperatures.
3. Positive-energy shell (published M): momentum to reach v and stop, ideal photon-rocket mass
   ratio, versus a bare 1e5 kg payload; interior clock rate and the equivalent rocket speed.
"""
import math
import sys

import numpy as np
import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from gr_tensors import metrics, qi, horizons_1p1, to_si, PLANCK_LENGTH  # noqa: E402

C = 299792458.0
MSUN = 1.989e30


def alc_wall(Rv, sg, vv):
    st, s = metrics.alcubierre()
    top = metrics.alcubierre_top_hat(s)
    params = {s["v"]: vv, s["R"]: Rv, s["sigma"]: sg}
    rho_fn = st.compile(st.energy_density(), params, {s["f"]: top})
    ys = np.linspace(Rv - 2 / sg, Rv + 2 / sg, 4001)
    vals = np.array([float(rho_fn(0.0, 0.0, y, 0.0)) for y in ys])
    i = int(np.argmin(vals))
    p = (0.0, 0.0, float(ys[i]), 0.0)
    cur = st.curvature_at(p, params, {s["f"]: top})
    pc = st.precision_check(st.energy_density(), [p], params, {s["f"]: top})
    return vals[i], cur["curvature_radius"], p, pc


def main():
    Rv, vv, alpha = 100.0, 10.0, 0.1
    out = []
    for sg in (2.0, 4.0):
        rho, rc, p, pc = alc_wall(Rv, sg, vv)
        out.append((sg, rho, rc))
        print(f"Alcubierre R = 100 m, v = 10, sigma = {sg} /m (Delta = {2/sg} m): min Eulerian rho = {rho:.5e} 1/m^2"
              f" = {to_si.energy_density_j_per_m3(rho):.3e} J/m^3 at y = {p[2]:.4f} m; curvature radius r_c = {rc:.4e} m;"
              f" precision_check {pc}")
        tau0 = alpha * rc
        bound = qi.ford_roman_geometric(tau0)
        print(f"   Ford-Roman bound with tau0 = {alpha} r_c = {tau0:.3e} m: rho >= {bound:.3e} 1/m^2"
              f" ({qi.ford_roman_si(tau0 / C):.3e} J/m^3); violation factor |rho|/|bound| = {abs(rho)/abs(bound):.3e}")
    (s1, r1, c1), (s2, r2, c2) = out
    k_rho = math.log(r2 / r1) / math.log(s2 / s1)
    k_rc = math.log(c2 / c1) / math.log(s2 / s1)
    print(f"   scaling exponents: rho ~ sigma^{k_rho:.4f}, r_c ~ sigma^{k_rc:.4f}")
    # |rho(sig)| = |r1| (sig/s1)^k_rho ; bound(sig) = 3 Lp^2 / (32 pi^2 (alpha c1 (sig/s1)^k_rc)^4)
    A = 3 * PLANCK_LENGTH ** 2 / (32 * math.pi ** 2 * (alpha * c1) ** 4)
    # |r1| x^k_rho = A x^(-4 k_rc)  ->  x = (A/|r1|)^(1/(k_rho + 4 k_rc))
    x = (A / abs(r1)) ** (1.0 / (k_rho + 4 * k_rc))
    sig_qi = s1 * x
    Dqi = 2 / sig_qi
    E = -vv ** 2 * Rv ** 2 / (18 * Dqi)
    print(f"   QI-limited wall: sigma = {sig_qi:.3e} /m, Delta_QI = {Dqi:.3e} m = {Dqi/PLANCK_LENGTH:.1f} L_Planck"
          f" (= {Dqi/(vv*PLANCK_LENGTH):.1f} v L_P); E = -v^2R^2/(18 Delta) = {E:.3e} m = {to_si.mass_kg(E):.3e} kg"
          f" = {to_si.mass_kg(E)/MSUN:.3e} M_sun")
    # horizons on the axis, comoving coordinate xi
    sg = 2.0
    T = math.tanh(sg * Rv)

    def f(r):
        return (np.tanh(sg * (r + Rv)) - np.tanh(sg * (r - Rv))) / (2 * T)

    xs = np.linspace(0.0, Rv + 20, 200001)
    hz = horizons_1p1(lambda xi: -vv * (1 - f(np.abs(xi))), xs)
    for h in hz:
        print(f"Alcubierre v = 10 horizon at |xi| = {h['x']:.4f} m: kappa = {h['kappa']:.4e} 1/m, T_H = {to_si.hawking_temperature_k(h['kappa']):.4e} K")
    # shell momentum / proper time
    M = 4.511e27
    for beta in (0.0244, 0.04, 0.1):
        g = 1 / math.sqrt(1 - beta ** 2)
        P = g * M * beta * C
        mr = (1 + beta) / (1 - beta)          # ideal photon rocket, accelerate + brake
        print(f"shell to v = {beta}c and back: momentum to supply/eject each way {P:.3e} kg m/s; ideal photon-rocket"
              f" start-stop mass ratio {mr:.4f} -> radiated mass {M*(1-1/mr):.3e} kg = {M*(1-1/mr)*C**2:.3e} J;"
              f" bare 1e5 kg payload: radiated {1e5*(mr-1):.3e} kg (initial mass {1e5*mr:.4e} kg)")
    lapse = 0.7611845
    for beta in (0.0244, 0.04, 0.1):
        g = 1 / math.sqrt(1 - beta ** 2)
        geq = g / lapse
        veq = math.sqrt(1 - 1 / geq ** 2)
        print(f"interior clock at shell speed {beta}c runs at lapse/gamma = {lapse/g:.4f} of exterior time;"
              f" a rocket gets the same slowing at v = {veq:.4f}c")
    d = 4.37  # ly
    print(f"alpha Cen (4.37 ly) at 0.0244c: {d/0.0244:.1f} yr exterior, {d/0.0244*lapse*math.sqrt(1-0.0244**2):.1f} yr inside the shell")
    return 0


if __name__ == "__main__":
    sys.exit(main())
