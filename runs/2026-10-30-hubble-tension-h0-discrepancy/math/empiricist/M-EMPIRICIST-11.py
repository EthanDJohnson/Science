"""M-EMPIRICIST-11: Wilson score interval for 0 successes in n = 12 trials, 95% (z = 1.959964):
upper = (p + z^2/2n + z sqrt(p(1-p)/n + z^2/4n^2)) / (1 + z^2/n); at p = 0 this is z^2/(n + z^2). Claim 0.24.
Tally (table C, 21 cases, 18 resolved): single-source resolved 12 with 0 new physics; multi-method resolved 6
with 3 new physics (solar ν, atmospheric ν, acceleration) and 1 mixed (age crisis, counted 0.5);
claims 3.5 of 6, and 14 of 18 'systematics, shared inputs or statistics'.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/empiricist")
from math_checks import identity, limit, finish
from _common import cmp

identity("(z**2/(2*n) + z*sqrt(z**2/(4*n**2)))/(1 + z**2/n)", "z**2/(n + z**2)")
limit("z**2/(n + z**2)", "n", "oo", "0")
z = 1.959963985
cmp("Wilson 95% upper bound, 0/12", z**2 / (12 + z**2), 0.24, 0.006)

# explicit case list as printed in table C (resolved = outcome given; unresolved = neutron lifetime, G spread, gallium)
cases = ["Hubble/Baade", "Sandage-dV", "age crisis", "solar nu", "atm nu", "acceleration", "proton radius",
         "muon g-2", "CDF W", "PTB G", "CODATA alpha", "reactor nu", "R_K", "OPERA", "BICEP2", "Pioneer",
         "Planck A_L", "S8", "neutron lifetime", "G spread", "gallium"]
unresolved = {"neutron lifetime", "G spread", "gallium"}
new_physics = {"solar nu": 1, "atm nu": 1, "acceleration": 1, "age crisis": 0.5}
resolved = [c for c in cases if c not in unresolved]
print(f"  cases {len(cases)}, resolved {len(resolved)}")
cmp("resolved count", len(resolved), 18, 0.01)
np_total = sum(new_physics.values())
pure_sys = sum(1 for c in resolved if c not in new_physics)
print(f"  new-physics weight {np_total}; purely non-new-physics {pure_sys}; mixed 1; 18 - 3.5 = {18 - np_total}")
cmp("purely systematics/shared input/statistics (mixed case excluded)", pure_sys, 14, 0.01)
raise SystemExit(finish())
