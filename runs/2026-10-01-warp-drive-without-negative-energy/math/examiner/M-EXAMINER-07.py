"""M-EXAMINER-07: cost arithmetic used in P10, O4 Q6/Q10 and EXAMINER-E.

SI. Shell mass M = 4.49e27 kg (quoted, not checked here). Payload m = 1e5 kg.
Photon rocket, constant proper acceleration a = 1 g, accelerate to midpoint then decelerate,
distance d = 4.37 ly. Rapidity at midpoint: cosh(phi) = 1 + a (d/2) / c^2.
Photon rocket: m_initial/m_final = exp(Delta rapidity), so the whole trip ratio = exp(2 phi).
Propellant energy = (ratio - 1) m c^2.
Claims: ratio 40.4; propellant energy 3.5e23 J; Mc^2 = 4.0e44 J; ratio of energies 1.1e21;
M/m = 4.5e22.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import math
import sympy as sp
from math_checks import identity, series, quantity, units, finish

c = 299792458.0
ly = c*365.25*86400
for a, lab in ((9.80665, "g0"), (9.81, "9.81")):
    d = 4.37*ly
    phi = math.acosh(1 + a*(d/2)/c**2)
    ratio = math.exp(2*phi)
    Ep = (ratio - 1)*1e5*c**2
    print(f"a = {lab} m/s^2: midpoint rapidity {phi:.4f}, mass ratio {ratio:.3f}, propellant energy {Ep:.4e} J, "
          f"Mc^2/Ep = {4.49e27*c**2/Ep:.3e}")
    ok = abs(ratio - 40.4) < 0.15
    print(("PASS" if ok else "FAIL") + f" photon-rocket mass ratio ({lab}) {ratio:.2f} vs claimed 40.4")
# photon rocket law: d(m)/m = -d(rapidity) for exhaust at c; check the small-rapidity limit gives classical dv/c
x = sp.Symbol("x", positive=True)
series("exp(x) - 1", "x", 0, 2, "x")       # Tsiolkovsky with u = c, small dv: dm/m = dv/c
quantity("4.49e27 kg * c^2", "4.035e44 J", rel_tol=1e-3)
quantity("39.4 * 1e5 kg * c^2", "3.54e23 J", rel_tol=2e-3)
units("4.49e27 kg * c^2", "energy")
quantity("4.035e44 J / (3.54e23 J)", "1.14e21 J / (1 J)", rel_tol=5e-3)
quantity("4.49e27 kg / (1e5 kg)", "4.49e22 kg / (1 kg)", rel_tol=1e-6)
raise SystemExit(finish())
