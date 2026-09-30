"""M-IDEALIZER-15 (F12 parenthetical): "The dossier's 0.23/0.57 rad [Q-10] uses a different geometric convention,
G m^2/d with d = 450 um". Test: phi = G m^2 t/(hbar d), m = 1e-14 kg, d = 450 um, t = 1 s and 2.5 s (SI).
Alternative convention tested: Bose et al. geometry with d = 450 um, dx = 250 um, closest/farthest separations
d - dx = 200 um and d + dx = 700 um: phi = G m^2 t (1/(200 um) - 1/(700 um))/hbar.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, finish

quantity("G * (1e-14 kg)^2 * 1 s / (hbar * 450 um)", "0.23", rel_tol=0.05)       # lens's stated convention
quantity("G * (1e-14 kg)^2 * 2.5 s / (hbar * 450 um)", "0.57", rel_tol=0.05)
quantity("G * (1e-14 kg)^2 * 1 s / (hbar * 450 um)", "0.1406", rel_tol=2e-3)      # what that convention gives
quantity("G * (1e-14 kg)^2 * 1 s * (1/(200 um) - 1/(700 um)) / hbar", "0.23", rel_tol=0.03)
quantity("G * (1e-14 kg)^2 * 2.5 s * (1/(200 um) - 1/(700 um)) / hbar", "0.57", rel_tol=0.03)
raise SystemExit(finish())
