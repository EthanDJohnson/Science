"""M-CONSTRAINTS-05 (F5): BAO+BBN. h r_d = 101.54 Mpc fixed (DESI DR2 LCDM), r_d from the Aubourg et al. 2015 fit
r_d = 55.154 exp(-72.3 (omega_nu + 0.0006)^2) / (omega_cb^0.25351 omega_b^0.12807) Mpc, omega_cb = Omega_m h^2 - omega_nu.
Solve h(Omega_m); find Omega_m with h = 0.73264 (lens 0.338; +4.7 sigma for omega_b 0.02218, +5.2 for 0.02166);
d ln H0 / d ln Omega_m (lens 0.52). Sanity: Omega_m = 0.2975, omega_b = 0.02218 should give ~68.5 (DESI+BBN)."""
import sys, math
import sympy as sp
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/constraints")
from math_checks import identity, finish
from _bg import bisect, near, ONU

def rd(h, Om, wb):
    wcb = Om * h * h - ONU
    return 55.154 * math.exp(-72.3 * (ONU + 0.0006) ** 2) / (wcb ** 0.25351 * wb ** 0.12807)

def h_of(Om, wb):
    return bisect(lambda h: h * rd(h, Om, wb) - 101.54, 0.4, 1.0, tol=1e-10)

near("sanity H0 at DESI Om, BBN wb", 100 * h_of(0.2975, 0.02218), 68.5, 0.4)
e = 1e-4
sl = (math.log(h_of(0.2975 * (1 + e), 0.02218)) - math.log(h_of(0.2975 * (1 - e), 0.02218))) / (2 * e)
print("d ln H0/d ln Om =", sl)
near("slope", sl, 0.52, 0.02)
# analytic: h^(1-2*0.25351) Om^-0.25351 = const -> slope = 0.25351/(1 - 0.50702)
a, K, O = sp.symbols("a K O", positive=True)
hsol = (K * O ** a) ** (1 / (1 - 2 * a))      # solves h^(1-2a) O^(-a) = K
identity(sp.simplify(O * sp.diff(sp.log(hsol), O)), a / (1 - 2 * a), domain={"a": (0.1, 0.4), "K": (0.1, 10), "O": (0.1, 1)})
print("analytic slope (omega_nu neglected) =", 0.25351 / (1 - 2 * 0.25351))
for wb, nsig in [(0.02218, 4.7), (0.02166, 5.2)]:
    Om = bisect(lambda O: h_of(O, wb) - 0.73264, 0.2, 0.5, tol=1e-8)
    print(f"wb={wb}: Om needed {Om:.4f}, {(Om-0.2975)/0.0086:.2f} sigma")
    if wb == 0.02218:
        near("Om needed", Om, 0.338, 0.003)
    near("n sigma", (Om - 0.2975) / 0.0086, nsig, 0.2)
raise SystemExit(finish())
