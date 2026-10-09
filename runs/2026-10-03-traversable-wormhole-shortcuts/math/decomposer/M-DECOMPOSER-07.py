"""M-DECOMPOSER-07: MM payload ratios m/|E_bin| with |E_bin| = 5e9 kg (quoted, Q-02)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, units, finish

for m, claim in [("1 kg", "2e-10"), ("70 kg", "1.4e-8"), ("1e3 kg", "2e-7")]:
    quantity(f"({m}) / (5e9 kg)", claim, rel_tol=1e-6)
units("(70 kg) / (5e9 kg)", "dimensionless")
# consistency of the quoted pair E_bin ~ -5e9 kg ~ -4.5e26 J: E = m c^2
quantity("5e9 kg * c^2", "4.5e26 J", rel_tol=1e-2)
raise SystemExit(finish())
