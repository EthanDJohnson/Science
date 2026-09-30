"""M-DIALECTICIAN-07: bottle contradiction arithmetic. If BL1 is the true lifetime, a bottle reading tau_b has an
extra loss rate Gamma_loss = 1/tau_b - 1/tau_BL1 (time constant 1/Gamma_loss). SI: s, s^-1."""
import sys
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/dialectician")
from _common import *  # noqa

for name, tb, want_rate, want_T in [("UCNtau", UCN, 1.268e-5, 7.9e4), ("Gravitrap", GRV, 7.92e-6, 1.26e5)]:
    r = 1 / tb - 1 / BL1
    print(f"{name}: loss rate {r:.4e} 1/s, time constant {1/r:.4e} s")
    num(f"{name} rate", r, want_rate, unit="1/s", rel_tol=6e-4)
    num(f"{name} time const", 1 / r, want_T, rel_tol=6e-3)
d = GRV - UCN
z_face = d / q(sGRV, sUCN_up)
z_sym = d / q(sGRV, sUCN_sym)
print(f"Gravitrap - UCNtau = {d:.2f} s; {z_face:.3f} sigma (facing side), {z_sym:.3f} (symmetrized UCNtau sys)")
num("Grav - UCN", d, 3.68, abs_tol=0.006)
num("sigma", z_face, 3.8, unit="", abs_tol=0.05)
shift = BL1 - JP
up = q(JPst, JPup_sys)
print(f"J-PARC shift needed = {shift:.2f} s; upper error {up:.3f} s; ratio {shift/up:.3f}")
num("J-PARC shift", shift, 10.5, abs_tol=0.01)
num("ratio to upper error", shift / up, 2.4, unit="", abs_tol=0.05)
# identity and small-gap limit: 1/a - 1/b = (b-a)/(ab) ~ (b-a)/a^2
identity("1/a - 1/b", "(b - a)/(a*b)", domain={"a": (800, 900), "b": (800, 900)})
series("1/a - 1/(a + d)", "d", 0, 2, "d/a**2")
units("1/(877.82 s) - 1/(887.7 s)", "frequency")
raise SystemExit(finish())
