"""M-EXAMINER-04 (F3, F10, P7): mass bias -> apparent gamma.
Definition: v~ = v_p / sqrt(G M_est / s). A velocity test with Kepler template fits gamma_app such that
v_p^2 = gamma_app G M_est (template shape) while truth is v_p^2 = gamma_true G M_true (same shape).
So gamma_app = gamma_true * M_true / M_est. All dimensionless; masses in Msun.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, sign, finish

gt, Mt, Me, G, v, s, b = sp.symbols("gamma_t M_t M_e G v s b", positive=True)
# truth: v^2 = gamma_t G M_t / s * c ; template: v^2 = gamma_app G M_e / s * c  -> solve
c = sp.symbols("c", positive=True)
gapp = sp.solve(sp.Eq(gt * G * Mt / s * c, sp.Symbol("ga") * G * Me / s * c), sp.Symbol("ga"))[0]
identity(gapp, gt * Mt / Me)
limit(gapp.subs(Me, Mt), "M_t", 1, "gamma_t")       # correct mass -> no bias
# fractional under-estimate u: M_e = (1-u) M_t; gamma_app = 1.37 with gamma_t = 1 -> u = 1 - 1/1.37
u = 1 - 1 / sp.Rational(137, 100)
print("required under-estimate u =", sp.N(u, 5), "(lens 27.0%)")
identity(sp.Float(round(float(u), 3)), sp.Float(0.270))
print("2.0/1.56 =", sp.N(sp.Rational(200, 156), 5))
identity(sp.Float(round(200 / 156, 3)), sp.Float(1.282))
# 10% bias in the low-g bin only: M_e = 0.9 M_t -> 1.111 ; M_e = 1.1 M_t -> 0.909
for f, want in ((sp.Rational(9, 10), 1.11), (sp.Rational(11, 10), 0.91)):
    val = gapp.subs({gt: 1, Me: f * Mt})
    print(f"M_e/M_t = {f}: gamma_app = {sp.N(val, 5)}")
    identity(sp.Float(round(float(val), 2)), sp.Float(want))
sign(sp.diff(gapp, Me), "negative")    # under-estimating mass raises gamma_app
raise SystemExit(finish())
