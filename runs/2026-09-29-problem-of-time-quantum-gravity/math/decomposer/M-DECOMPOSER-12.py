# M-DECOMPOSER-12: semiclassical correction size (E/m_P)^2 at LHC energy.
# The dossier (Q-18) uses m_P = 2.65e19 GeV, which is sqrt(3*pi/2) * sqrt(hbar c^5/G) (Kiefer-style convention).
import sys, math; sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, units, finish
units("14 TeV / (m_P * c^2)", "dimensionless")
quantity("(3*pi/2)^(1/2) * m_P * c^2", "2.65e19 GeV", rel_tol=5e-3)          # the convention
quantity("(14 TeV / ((3*pi/2)^(1/2) * m_P * c^2))^2", "3e-31", rel_tol=0.1)   # lens / Q-18 value
# With the conventional Planck energy 1.22e19 GeV the same ratio is 4.7x larger:
quantity("(14 TeV / (m_P * c^2))^2", "1.3e-30", rel_tol=0.05)
raise SystemExit(finish())
