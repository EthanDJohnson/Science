"""M-IDEALIZER-06: NEC cap on the shift at the 2024 parameters (F6). Geometric units.
R1 = 10 m, R2 = 20 m, M = 4.49e27 kg -> G M/c^2 = 3.334 m. Linear theory, M*beta cross terms dropped.
(a) NEC for a type-I block [[rho, j], [j, p]] with isotropic p: rho + p + 2 j cos(alpha) >= 0 for all
    null directions <=> |j| <= (rho + p)/2.
(b) Uniform wall, p = 0: beta_max = 8 pi rho / max|V|. Claims 0.0272 sigmoid, 0.0476 cubic, 0.0439 quintic.
(c) p = 0.1 rho raises the cap by 10%.
(d) Shaped wall: 0.084 (sigmoid) to 0.107 (cubic).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/math/idealizer")
import sympy as sp
from math_checks import identity, inequality, quantity, units, limit, finish
from profiles import caps, KG_TO_M

rho, p, j, al = sp.symbols("rho p j alpha", real=True)
# null k = (1, cos al, sin al, 0) in the orthonormal frame; T_00 = rho, T_0x = j, T_ij = p delta
Tkk = rho + 2*j*sp.cos(al) + p*(sp.cos(al)**2 + sp.sin(al)**2)
identity(sp.simplify(Tkk), rho + p + 2*j*sp.cos(al))
print("min over alpha of T_kk =", "rho + p - 2|j|  (cos alpha = -sign j)")
identity(Tkk.subs(al, sp.pi), rho + p - 2*j)
units("1 kg * 6.6743e-11 m^3/(kg s^2) / (2.99792458e8 m/s)^2", "m")
Mg = 4.49e27*KG_TO_M
print(f"M = {Mg:.4f} m (geometric)")
quantity(f"{Mg}", "3.334", rel_tol=1e-3)
claims = {"sigmoid": (0.0272, 0.084), "cubic": (0.0476, 0.107), "quintic": (0.0439, None)}
for kind, (cu, cs) in claims.items():
    b1 = caps(kind, Mg, 10.0, 20.0, nr=10000)
    b2 = caps(kind, Mg, 10.0, 20.0, nr=20000)
    b01 = caps(kind, Mg, 10.0, 20.0, nr=20000, p_over_rho=0.1)
    print(f"{kind}: uniform {b1[0]:.5f} -> {b2[0]:.5f}; shaped spherical {b2[1]:.4f}; shaped pointwise {b2[2]:.4f}; p=0.1rho {b01[0]:.5f} (x{b01[0]/b2[0]:.3f})")
    quantity(f"{b2[0]}", f"{cu}", rel_tol=0.005)
    quantity(f"{b01[0]/b2[0]}", "1.1", rel_tol=1e-9)
    if cs is not None:
        print(f"   claim shaped {cs}: spherical {b2[1]:.4f}, pointwise {b2[2]:.4f}")
        quantity(f"{b2[2]}", f"{cs}", rel_tol=0.02)   # pointwise rho = 2|T_0i| reproduces the claim
# limit: M -> 0 gives cap -> 0 (linear in M)
quantity(f"{caps('cubic', 1e-6*Mg, 10.0, 20.0)[0]/caps('cubic', Mg, 10.0, 20.0)[0]}", "1e-6", rel_tol=1e-6)
raise SystemExit(finish())
