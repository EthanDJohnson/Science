"""Theory facet: helicity selection rule for tree-level g g -> gamma gamma, and a crossing cross-check.
Units: natural (hbar=c=1), G=1 (all amplitudes scale as G; cross sections as G^2 s).
Route 1: toolkit qft_second_order.helicity_amplitudes_cm (background-field Feynman-diagram calculation).
Route 2: Bjerrum-Bohr, Donoghue, Holstein, Planté, Vanhove (PRD 91, 064008, eq. 5.4) photon-graviton cross section
         dsigma/dt = 2 pi G^2 (s^4+u^4)/(s^2 t^2), crossed s<->t to g g -> gamma gamma.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import qft_second_order as q2

G = 1.0
s = 4.0
print("Inputs: s = %.3f (energy^2, natural units), G = %.1f" % (s, G))
for theta in (0.7, 1.0, math.pi/2, 2.2):
    amps = q2.helicity_amplitudes_cm(s=s, theta=theta, final="photon", G=G)
    t = -0.5*s*(1-math.cos(theta)); u = -0.5*s*(1+math.cos(theta))
    print("\ntheta = %.4f rad, t = %.4f, u = %.4f" % (theta, t, u))
    print("  predicted |M| = 8 pi G t^2/s = %.6f ; 8 pi G u^2/s = %.6f" % (8*math.pi*G*t*t/s, 8*math.pi*G*u*u/s))
    nz = {k: abs(v) for k, v in amps.items() if abs(v) > 1e-9}
    print("  nonzero (l1,l2,s1,s2) [physical helicities, each along own momentum]:")
    for k in sorted(nz): print("    ", k, "|M| = %.6f" % nz[k])
    print("  number nonzero: %d of %d" % (len(nz), len(amps)))
    same = [k for k in nz if k[0] == k[1]]
    print("  nonzero entries with SAME graviton helicity: %d ; with same photon helicity: %d" %
          (len(same), len([k for k in nz if k[2] == k[3]])))

# Route 2: total unpolarised sigma and sum rule
print("\nCross-check of unpolarised total cross section sigma(gg->gamma gamma) at s=%.2f" % s)
# crossing of Bjerrum-Bohr eq 5.4: sum over ALL helicities of |M|^2 for g gamma->g gamma = 2 (8 pi G)^2 (s^4+u^4)/t^2 * ... 
# From dsigma/dt = |M|^2_avg/(16 pi s^2), avg over 4 initial states: sum_all|M|^2 = 4*16 pi s^2 * 2 pi G^2 (s^4+u^4)/(s^2 t^2)
def sum_all_M2_gg(sv, tv, uv):
    # cross s<->t in 128 pi^2 G^2 (s^4+u^4)/t^2  -> 128 pi^2 G^2 (t^4+u^4)/s^2
    return 128*math.pi**2*G**2*(tv**4+uv**4)/sv**2
from numpy import linspace
ct = np.linspace(-1, 1, 200001)
tt = -0.5*s*(1-ct); uu = -0.5*s*(1+ct)
# dsigma/dcos = (1/2)*|M|^2_avg *(1/(32 pi s)) ... use dsigma/dt = Mavg/(16 pi s^2), dt = (s/2) dcos
Mavg = sum_all_M2_gg(s, tt, uu)/4.0
dsdt = Mavg/(16*math.pi*s*s)
sigma_cross = 0.5*np.trapezoid(dsdt*(s/2), ct)   # 1/2 identical photons
print("  Route 2 (crossed Bjerrum-Bohr eq 5.4): sigma_unpol = %.8f ; 2 pi G^2 s/5 = %.8f" % (sigma_cross, 2*math.pi*G**2*s/5))
print("  Route 1 (toolkit): sigma(R,L) = %.8f ; (4/5) pi G^2 s = %.8f ; unpolarised = half = %.8f" %
      (q2.sigma_total(s, "R", "L", final="photon", G=G), 0.8*math.pi*G**2*s, 0.5*q2.sigma_total(s, "R", "L", final="photon", G=G)))
print("  sigma(R,R) same-helicity (toolkit) = %.3e" % q2.sigma_total(s, "R", "R", final="photon", G=G))
