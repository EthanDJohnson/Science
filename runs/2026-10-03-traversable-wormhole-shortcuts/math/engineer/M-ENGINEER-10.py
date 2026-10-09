"""M-ENGINEER-10: CMB photons seen by an MM traveller; temperature limits; Lambda-era cooling; de Sitter floor.
Static metric ds^2 = -F dt^2 + H dx^2 (F, H > 0). Traveller with Killing energy per unit mass e (u_t = -e),
moving in +x; photon with Killing energy eps (k_t = -eps) moving in -x (head-on).
Energy seen: -u.k = (e eps/F)(1 + sqrt(1 - F/e^2)). At the throat F = 1/gamma^2, e = 1 (fell from rest):
-> 2 gamma^2 eps for gamma >> 1. Lens uses gamma^2.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, units, finish

F, H, e, eps, gam = sp.symbols("F H e eps gamma", positive=True)
ut = e / F
ux = sp.sqrt((e**2 / F - 1) / H)              # from -F ut^2 + H ux^2 = -1
kt = eps / F
kx = -eps / sp.sqrt(F * H)                     # null, moving in -x
identity(-F * kt**2 + H * kx**2, 0)
identity(-F * ut**2 + H * ux**2, -1)
Eobs = F * ut * kt - H * ux * kx                 # -g_ab u^a k^b
identity(Eobs, (e * eps / F) * (1 + sp.sqrt(1 - F / e**2)))
boost = sp.simplify((Eobs / eps).subs({e: 1, F: 1 / gam**2}))
limit(boost / gam**2, "gamma", "oo", "2")
# flat limit F = 1, e = 1 (traveller at rest): no boost
identity(Eobs.subs({F: 1, e: 1}), eps)

quantity("kB*2.725 K*(2e12)^2", "9.4e20 eV", rel_tol=1e-2)
quantity("1 eV/(kB*(2e12)^2)", "2.9e-21 K", rel_tol=1e-2)
quantity("1e-26 eV/kB", "1.16e-22 K", rel_tol=1e-2)
units("1 eV/kB", "temperature")
H0 = 67.4e3 / 3.0856775814913673e22
HL = H0 * math.sqrt(0.685)
t = math.log(2.725 / 2.9e-21) / HL / (365.25 * 86400)
TdS = 1.054571817e-34 * HL / (2 * math.pi * 1.380649e-23)
print(f"H_Lambda = {HL:.4e} 1/s; cooling time {t:.3e} yr; de Sitter T = {TdS:.3e} K")
print(f"orders: CMB/limit {math.log10(2.725/2.9e-21):.2f}, 38 pK/limit {math.log10(38e-12/2.9e-21):.2f}, 38 pK/dark {math.log10(38e-12/1.16e-22):.2f}")
quantity(f"{t} yr", "8.5e11 yr", rel_tol=1e-2)
quantity(f"{TdS} K", "2.2e-30 K", rel_tol=1e-2)
quantity("hbar*67.4 km/s/Mpc*0.685^0.5/(2*pi*kB)", "2.2e-30 K", rel_tol=1e-2)
raise SystemExit(finish())
