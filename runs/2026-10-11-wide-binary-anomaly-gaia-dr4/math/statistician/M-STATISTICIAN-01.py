"""M-STATISTICIAN-01: local significance of each DR3 signal (finding 1, Table 1).
gamma = G_eff/G (dimensionless); Gamma = log10 sqrt(gamma) (dimensionless).
z = (value - Newton)/sigma on the side facing Newton; stat+sys combined in quadrature.
Inputs from dossier D-20..D-26 (quoted, not checked here)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, limit, sign, finish
from _h import p2, report

allok = []
# Chae 2024b: gamma 1.37 +0.10-0.09 stat +0.16-0.09 sys; Gamma 0.068 +-0.015 stat +0.024-0.015 sys
allok.append(report("Chae24b stat z (gamma)", 0.37 / 0.09, 4.1, 0.05))
allok.append(report("Chae24b stat z (Gamma)", 0.068 / 0.015, 4.5, 0.05))
allok.append(report("Chae24b stat+sys z (gamma)", 0.37 / (0.09**2 + 0.09**2) ** 0.5, 2.9, 0.05))
zG = 0.068 / (0.015**2 + 0.015**2) ** 0.5
allok.append(report("Chae24b stat+sys z (Gamma)", zG, 3.21, 0.01))
allok.append(report("two-sided p at z=3.21", p2(zG), 1.3e-3, 0.05e-3))
allok.append(report("two-sided p at z=2.91", p2(0.37 / 0.09 / 2**0.5), 3.7e-3, 0.1e-3))
# others
allok.append(report("Yoon+25 1.32 -0.11", 0.32 / 0.11, 2.9, 0.05))
allok.append(report("Hernandez 1.5+-0.2", 0.5 / 0.2, 2.5, 0.01))
allok.append(report("Chae24a pure 1.49 -0.19", 0.49 / 0.19, 2.6, 0.05))
allok.append(report("Chae25 MOND 1.48 -0.23", 0.48 / 0.23, 2.1, 0.05))
allok.append(report("Chae25 +transition 1.34 -0.08", 0.34 / 0.08, 4.25, 0.01))
allok.append(report("Chae+26 1.60 -0.14", 0.60 / 0.14, 4.29, 0.01))
allok.append(report("Chae23 1.43+-0.06", 0.43 / 0.06, 7.2, 0.05))
allok.append(report("Chae23 re-analysed Gamma 0.059+-0.009", 0.059 / 0.009, 6.6, 0.05))
# Chae+26 without 2 systems: Gamma 0.042 -0.024, 0.057 -0.031, 0.085 -0.045
zs = [0.042 / 0.024, 0.057 / 0.031, 0.085 / 0.045]
print("Chae+26 w/o 2 systems z:", [round(z, 3) for z in zs], "(lens: 1.8-1.9)")
# Why gamma- and Gamma-units differ: the Gamma z ~ gamma z * (1 + correction); in small-boost limit they agree
# z_Gamma/z_gamma for symmetric small errors -> 1 as (gamma-1)->0 : log10 sqrt(g)/(dlogsqrt/dg) /(g-1)
limit("(log(g)/2/log(10)) / (1/(2*g*log(10))) / (g-1)", "g", 1, 1)
# gamma = 10^(2 Gamma) inverse of Gamma = log10 sqrt(gamma)
identity("log(sqrt(10**(2*G0)))/log(10)", "G0", domain={"G0": (-1, 1)})
# z increases when sys is removed (quadrature): s/sqrt(s^2+t^2) <= 1
sign("1 - s/sqrt(s**2+t**2)", "nonnegative", domain={"s": (0.001, 1), "t": (0, 1)})
print("ALL NUMERIC CHECKS OK" if all(allok) else "SOME NUMERIC CHECK DIFFERS")
raise SystemExit(finish())
