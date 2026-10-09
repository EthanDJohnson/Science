"""M-DECOMPOSER-04: MTY mouth motion and gravitational parking for the MM shortcut lag.

Definitions: a mouth moving at constant speed v (exterior frame) for exterior time T has its
clock lag behind the static mouth by T(1 - 1/gamma), gamma = 1/sqrt(1 - v^2/c^2) (turnarounds
neglected). A mouth parked at lapse alpha for exterior time T lags by T(1 - alpha).
Kinetic energy of one mouth of mass M: (gamma - 1) M c^2.
Inputs: lag needed = 8425 yr (shortcut lag, M-DECOMPOSER-03); M = 2e34 kg (dossier Q-04, quoted).
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, series, quantity, units, finish

v, cc = sp.symbols("v c", positive=True)
gam = 1 / sp.sqrt(1 - v**2 / cc**2)
# small-speed limit: lag fraction 1 - 1/gamma ~ v^2/(2c^2); KE ~ M v^2/2 (Newtonian limit)
series(1 - 1 / gam, "v", 0, 4, v**2 / (2 * cc**2), domain={"v": (0.01, 0.5), "c": (1, 1)})
series(gam - 1, "v", 0, 4, v**2 / (2 * cc**2), domain={"v": (0.01, 0.5), "c": (1, 1)})

lag_short = (math.pi * 3e3 - 1e3)  # yr
lag_ctc = (math.pi * 3e3 + 1e3)    # yr
M = 2e34
for beta, trip_claim, ke_claim, msun_claim in [(0.1, "1.68e6 yr", "9.1e48 J", 50.7), (0.9, "1.49e4 yr", "2.3e51 J", 1.3e4)]:  # claims carry 2-3 sig figs
    g = 1 / math.sqrt(1 - beta**2)
    frac = 1 - 1 / g
    trip = lag_short / frac
    print(f"beta={beta}: gamma={g:.6f}, lag fraction={frac:.6f}, trip for shortcut lag={trip:.4e} yr, "
          f"trip for CTC lag={lag_ctc/frac:.4e} yr, distance covered={beta*trip:.3e} ly")
    quantity(f"{trip} yr", trip_claim, rel_tol=5e-3)
    ke = f"({g} - 1) * {M} kg * c^2"
    quantity(ke, ke_claim, rel_tol=2.2e-2)  # 2.3e51 is a 2-sig-fig rounding
    units(ke, "energy")
    quantity(f"({g} - 1) * {M} kg * c^2 / (Msun * c^2)", f"{msun_claim}", rel_tol=1e-2)
# parking at lapse alpha = 0.5
alpha = 0.5
quantity(f"{lag_short / (1 - alpha)} yr", "1.69e4 yr", rel_tol=5e-3)
raise SystemExit(finish())
