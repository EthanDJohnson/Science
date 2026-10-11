"""M-DECOMPOSER-07: inner-binary period vs Gaia baseline, and baseline suppression of short-period
orbital velocity in a fitted proper motion (finding 10).

Claims: a_in = 5 au, M_in ~ 1 Msun gives P_in <~ 11 yr, "within ~2x the 66-month baseline";
short-period wobble averages out over the baseline, long-period reflex motion enters the PM as a
near-linear shift.
Independent derivation: Kepler III P = 2 pi sqrt(a^3/(G M)) (SI). For a photocentre on a circular
orbit x(t) = A sin(w t + phi), the least-squares linear slope over t in [-T/2, T/2] (continuous,
uniform sampling) is S = (12/T^3) int t x dt.  Ratio R(w T) = max_phi |S| / (A w) is the fraction of
the instantaneous orbital speed that leaks into the fitted proper motion.
Must satisfy: R -> 1 as P/T -> inf (wT -> 0); R -> 0 like ~ 6/(wT)... as P/T -> 0.
Also order of magnitude: inner orbital speed vs v_c(s) of the wide pair.
"""
import sys
import sympy as sp
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, limit, identity, inequality, finish

quantity("2*pi*((5 au)^3/(6.674e-11 m^3/(kg s^2) * 1.989e30 kg))^0.5", "11.18 yr", rel_tol=2e-3)
quantity("66/12 yr", "5.5 yr", rel_tol=1e-3)   # 66-month baseline
quantity("11.18/5.5", "2.03", rel_tol=2e-3)
# a_in = 0.1 au and 300 au periods for scale
quantity("2*pi*((300 au)^3/(6.674e-11 m^3/(kg s^2) * 1.989e30 kg))^0.5", "5196 yr", rel_tol=3e-3)

t, T, w, A, phi = sp.symbols("t T w A phi", positive=True)
S_sin = sp.simplify(12 / T**3 * sp.integrate(t * sp.sin(w * t), (t, -T / 2, T / 2)))   # coefficient of cos(phi)
S_cos = sp.simplify(12 / T**3 * sp.integrate(t * sp.cos(w * t), (t, -T / 2, T / 2)))   # odd -> 0
print("slope coefficient (sin part):", S_sin, " cos part:", S_cos)
identity(S_cos, 0)
x = sp.symbols("x", positive=True)  # x = w T / 2
R = sp.simplify((S_sin / w).subs(w, 2 * x / T))
print("R(x) =", R)
identity(R, 3 * (sp.sin(x) - x * sp.cos(x)) / x**3)
limit(R, "x", 0, 1)          # long period: full orbital velocity enters the PM
limit(R * x, "x", sp.oo, 0)   # short period: R ~ -3 cos(x)/x^2 -> 0
for P_over_T, label in ((10.0, "P=10T"), (2.0, "P=2T"), (1.0, "P=T"), (0.2, "P=0.2T")):
    xv = sp.pi / P_over_T
    print(label, "R =", sp.N(R.subs(x, xv), 6))
inequality(str(sp.N(R.subs(x, sp.pi / 2), 15)), ">", "0.75")   # P = 2T retains >75%
inequality(str(sp.N(abs(R.subs(x, sp.pi / 0.2)), 15)), "<", "0.03")   # P = 0.2T retains <3%
# order of magnitude: inner orbital speed at a_in = 50 au (1 Msun) vs v_c of a 1.5 Msun pair at 10 kau
quantity("((6.674e-11 m^3/(kg s^2) * 1.989e30 kg)/(50 au))^0.5", "4.21 km/s", rel_tol=3e-3)
quantity("((6.674e-11 m^3/(kg s^2) * 1.5*1.989e30 kg)/(10000 au))^0.5", "0.365 km/s", rel_tol=3e-3)
raise SystemExit(finish())
