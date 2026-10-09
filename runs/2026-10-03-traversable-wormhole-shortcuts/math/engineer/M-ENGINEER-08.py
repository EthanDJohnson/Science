"""M-ENGINEER-08: MM species requirement under |E_min| = N^2 g^2 hbar c/(256 pi r_e) (lens's N extension of
MMP 5.31, see M-ENGINEER-01) with g^2 N <= 1 and the payload criterion m c^2 <= |E_min|.
Then N >= 256 pi r_e m c^2/(hbar c). Also the N = 1 pure-4D value at r_e = 1.5e7 m: |E_min| <= hbar c/(256 pi r_e) for g <= 1.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, inequality, quantity, units, finish

Nn, x, r, m = sp.symbols("Nn x r m", positive=True)   # x = g^2 N in (0,1]
Emax = Nn / (256 * sp.pi * r)                           # natural units
Nreq = sp.solve(sp.Eq(Emax, m), Nn)[0]
identity(Nreq, 256 * sp.pi * r * m)
units("256*pi*(0.1 m)*(1 kg)*c^2/(hbar*c)", "dimensionless")
quantity("256*pi*(0.1 m)*(1 kg)*c^2/(hbar*c)", "2.29e44 m/m", rel_tol=5e-3)
quantity("256*pi*(1.5e7 m)*(70 kg)*c^2/(hbar*c)", "2.40e54 m/m", rel_tol=5e-3)
quantity("256*pi*(1.5e7 m)*(1000 kg)*c^2/(hbar*c)", "3.43e55 m/m", rel_tol=5e-3)
# MM quote N_f > 1e52 for r_e > 1e7 m, 1e3 kg: compare with and without the 256 pi factor
quantity("256*pi*(1e7 m)*(1000 kg)*c^2/(hbar*c)", "2.29e55 m/m", rel_tol=5e-3)
quantity("(1e7 m)*(1000 kg)*c^2/(hbar*c)", "2.84e52 m/m", rel_tol=5e-3)
for v, lab in ((2.29e44, "1 kg"), (2.40e54, "human"), (3.43e55, "ship")):
    print(f"{lab}: {math.log10(v) - 32:.1f} orders above the 1e32 cap")
# N = 1 pure 4D at r_e = 1.5e7 m: upper bound for g <= 1
quantity("hbar*c/(256*pi*1.5e7 m)", "2.62e-36 J", rel_tol=5e-3)
print("Lens value 9e-39 J would need g^2 =", 9e-39 / (1.054571817e-34 * 299792458.0 / (256 * math.pi * 1.5e7)))
# the lens value 9e-39 J is the N = 1 formula at the hypercharge g = 0.06
quantity("0.06^2*hbar*c/(256*pi*1.5e7 m)", "9e-39 J", rel_tol=0.06)
quantity("hbar*c/(256*pi*1.5e7 m)/(1 meV)", "1.64e-14 m/m", rel_tol=5e-2)
raise SystemExit(finish())
