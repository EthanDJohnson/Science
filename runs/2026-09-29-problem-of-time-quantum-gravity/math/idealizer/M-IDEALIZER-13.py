"""M-IDEALIZER-13 (F13): arithmetic of the Planck-suppression numbers (SI and GeV).
lam = hbar G/(c^4 x) at x = 1 mm: 8.7e-76 s; lam*omega_Sr = 2.4e-60 (dimensionless).
(E/m_P)^2 with the lens's quoted m_P = 2.65e19 GeV (value from [Q-17], not checked here):
1.77 eV -> 4.5e-57; 14 TeV -> 2.8e-31; 1e16 GeV -> 1.4e-7. Also the same numbers with the standard
Planck energy sqrt(hbar c^5/G) = 1.22e19 GeV, to show the convention's effect (factor (2.65/1.22)^2 = 4.7).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, units, finish

quantity("hbar * G / (c^4 * 1 mm)", "8.7e-76 s", rel_tol=0.01)
units("hbar * G / (c^4 * 1 mm) * 2*pi*429.2e12 Hz", "1")
quantity("hbar * G / (c^4 * 1 mm) * 2*pi*429.2e12 Hz", "2.4e-60", rel_tol=0.03)
quantity("(1.77 eV / (2.65e19 GeV))^2", "4.5e-57", rel_tol=0.01)
quantity("(14 TeV / (2.65e19 GeV))^2", "2.8e-31", rel_tol=0.01)
quantity("(1e16 GeV / (2.65e19 GeV))^2", "1.4e-7", rel_tol=0.02)
# convention check: standard Planck energy
quantity("(hbar * c^5 / G)^0.5", "1.2209e19 GeV", rel_tol=1e-3)
quantity("(2.65e19 GeV / (hbar * c^5 / G)^0.5)^2", "4.71", rel_tol=0.01)
raise SystemExit(finish())
