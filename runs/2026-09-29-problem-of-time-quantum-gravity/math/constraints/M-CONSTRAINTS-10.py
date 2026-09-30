"""M-CONSTRAINTS-10: semiclassical (WKB) corrections (E/m_P)^2 with Kiefer's m_P = sqrt(3 pi hbar c/(2G)) (energy units).

Claims (F10): m_P = 2.650e19 GeV; (E/m_P)^2 = 4.5e-57 (Sr transition, E = h*429 THz), 2.6e-55 (hydrogen, 13.6 eV),
2.8e-31 (LHC 14 TeV), 1.4e-13 (1e13 GeV), 1.4e-11 (1e14 GeV). Cosmic variance sqrt(2/(2l+1)) = 0.63, 0.31, 0.18
at l = 2, 10, 30; 0.18/1.4e-11 >= 1e10; 7.6e-21 / 4.5e-57 ~ 1e36.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, units, limit, finish

quantity("(3*pi*hbar*c/(2*G))^0.5 * c^2", "2.650e19 GeV", rel_tol=2e-3)
units("(3*pi*hbar*c/(2*G))^0.5 * c^2", "energy")
mP = "((3*pi*hbar*c/(2*G))^0.5 * c^2)"
for E, ex in [("h_planck*429 THz", "4.5e-57"), ("13.6 eV", "2.6e-55"), ("14 TeV", "2.8e-31"),
              ("1e13 GeV", "1.4e-13"), ("1e14 GeV", "1.4e-11")]:
    quantity(f"(({E})/{mP})^2", ex, rel_tol=0.03)
for l, ex in [(2, 0.63), (10, 0.31), (30, 0.18)]:
    quantity(f"(2/(2*{l}+1))^0.5", f"{ex}", rel_tol=0.02)
quantity("(2/61)^0.5/1.42e-11", "1.3e10", rel_tol=0.03)
quantity("7.6e-21/4.48e-57", "1.7e36", rel_tol=0.02)
limit("sqrt(2/(2*l+1))", "l", "oo", "0")
raise SystemExit(finish())
