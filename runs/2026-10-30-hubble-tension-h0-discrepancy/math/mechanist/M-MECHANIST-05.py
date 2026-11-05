"""M-MECHANIST-05: d ln h / d ln θ_* at fixed ω_b, ω_c in flat ΛCDM, and the θ_* shift needed.
θ_* = r_s(z_*)/D_M(z_*); ω_b = 0.02237, ω_c = 0.1200, 100θ_* = 1.04110 ± 0.0003 [D-40].
Needed shift: ln(73.264/67.19)/(d ln h/d ln θ). Lens: 5.1(2), 1.69%, "about 59σ of its 0.03% precision".
Limit check: as h → large (Λ-dominated) D_M shrinks so θ grows: dθ/dh > 0 (sign). Check also the
Einstein–de Sitter-like low-h end where Ω_Λ → 0. Units: θ is a ratio of two lengths in Mpc.
"""
import math
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/mechanist")
from math_checks import inequality, quantity, finish
from mm_common import near
import mm_bg as B

ob, oc, th = 0.02237, 0.1200, 1.04110e-2
h0 = B.h_from_theta(th, ob, oc)
print(f"baseline h = {h0:.5f} (Planck 2018 with one massive nu quotes 0.6736 for 100θ_* = 1.04110)")
print(f"r_s(z_*) = {B.sound_horizon(B.zstar(ob, ob+oc), h0, ob, ob+oc):.3f} Mpc, z_* = {B.zstar(ob, ob+oc):.2f}")
eps = 1e-3
hp, hm = B.h_from_theta(th * (1 + eps), ob, oc), B.h_from_theta(th * (1 - eps), ob, oc)
deriv = (math.log(hp) - math.log(hm)) / (math.log(1 + eps) - math.log(1 - eps))
near("dlnh/dlntheta", deriv, 5.12, 0.15)
# sign / monotonic limit: theta increases with h across the domain
inequality(f"{B.theta_star(0.75, ob, oc)!r}", ">", f"{B.theta_star(0.65, ob, oc)!r}")
# exact (non-linearised) theta needed for h = 0.73264 * (h0/0.6719) i.e. same ratio
target = h0 * 73.264 / 67.19
th_need = B.theta_star(target, ob, oc)
shift = 100 * (th_need / th - 1)
near("theta shift % (exact)", shift, 1.69, 0.05)
near("theta shift % (linear)", 100 * math.log(73.264 / 67.19) / deriv, 1.69, 0.05)
prec = 100 * 0.0003 / 1.0411
print(f"precision of θ_*: {prec:.4f}%")
near("sigma using 0.0288% (D-40 numbers)", shift / prec, 59, 1.5)
near("sigma using rounded 0.03% (as the lens words it)", shift / 0.03, 59, 1.5)
quantity("147.1 Mpc / (14130 Mpc)", "0.01041", rel_tol=2e-3)  # dimensionless ratio of lengths
raise SystemExit(finish())
