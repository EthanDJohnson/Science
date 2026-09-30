"""M-CONSTRAINTS-15: PQCG delta-kernel squeeze (SI). Lower bound D2 >= 1e-24 kg^2 s m^-3 (decoherence),
upper bound D2 <= 1e-41 kg^2 s m^-3 (torsion balance): the gap is lower/upper = 1e17 (F16)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, units, finish

units("(1e-24 kg^2 s/m^3)/(1e-41 kg^2 s/m^3)", "dimensionless")
quantity("(1e-24 kg^2 s/m^3)/(1e-41 kg^2 s/m^3)", "1e17", rel_tol=1e-9)
raise SystemExit(finish())
