"""M-STATISTICIAN-14: heavy-tail likelihood ratio (F13, S3).
Local values x_i with scale s_i; residuals r_i = (x_i - mu)/s_i have unit-scale Student-t(nu) density.
H0: mu = 67.58 (early mean, its own error ignored); H1: mu free (maximised).
-2 ln Lambda = 2 [max_mu sum ln f(r_i(mu)) - sum ln f(r_i(67.58))]; z = sqrt(-2 ln Lambda) (Wilks, 1 dof).
Gaussian (nu -> inf) case reduces to (xbar_w - 67.58)^2 / sigma_w^2."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/statistician")
import mpmath as mp
from _common import quad, wmean, close
from math_checks import limit, units, finish

D = {"SH": (73.49, 0.93), "CC": (70.39, float(quad(1.22, 1.33, .70))), "SBF": (73.8, float(quad(.7, 2.3))),
     "TF": (73.3, float(quad(2.1, 3.5))), "TD": (71.1, 2.35), "MAS": (71.6, 3.7), "GW": (71.7, 8.45)}
nsl = wmean([D["SBF"][0], D["TF"][0]], [D["SBF"][1], D["TF"][1]])
MU0 = mp.mpf("67.5834")


def lnf(r, nu):
    if nu is None:
        return -r**2 / 2
    nu = mp.mpf(nu)
    return -(nu + 1) / 2 * mp.log(1 + r**2 / nu)


def m2lnL(keys, nu, merge_nsl=False):
    pts = [D[k] for k in keys]
    if merge_nsl:
        pts = [D[k] for k in keys if k not in ("SBF", "TF")] + [(nsl[0], nsl[1])]
    ll = lambda mu: sum(lnf((mp.mpf(v) - mu) / sg, nu) for v, sg in pts)
    grid = [mp.mpf(60) + mp.mpf(i) / 100 for i in range(0, 2001)]
    best = max(grid, key=ll)
    best = mp.findroot(lambda mu: mp.diff(ll, mu), best) if True else best
    return 2 * (ll(best) - ll(MU0)), best


sets = {"all 7 classes": ["SH", "CC", "SBF", "TF", "TD", "MAS", "GW"],
        "without SH0ES": ["CC", "SBF", "TF", "TD", "MAS", "GW"],
        "no-SN": ["SBF", "TF", "TD", "MAS", "GW"], "one-step": ["TD", "MAS", "GW"]}
out = {}
for name, keys in sets.items():
    for nu in (None, 2, 3):
        for merge in (False, True):
            if merge and not ("SBF" in keys):
                continue
            v, mu = m2lnL(keys, nu, merge)
            out[(name, nu, merge)] = v
            print(f"{name:15s} nu={str(nu):4s} SBF+TF merged={merge!s:5s}: -2lnL = {float(v):7.2f}, z = {float(mp.sqrt(v)):.2f}, mu_hat = {float(mu):.2f}")
close("all, Gaussian: -2lnL (lens 51.1)", out[("all 7 classes", None, False)], 51.1, 1.0)
close("all, nu=2: -2lnL (lens 18.2)", out[("all 7 classes", 2, False)], 18.2, 0.5)
close("all, nu=3: -2lnL (lens 20.0)", out[("all 7 classes", 3, False)], 20.0, 0.5)
close("without SH0ES, nu=2..3: z (lens 3.3)", mp.sqrt(out[("without SH0ES", 3, False)]), 3.3, 0.15)
close("no-SN, nu=3: z (lens 3.1)", mp.sqrt(out[("no-SN", 3, False)]), 3.1, 0.15)
close("one-step, nu=3: z (lens 2.0)", mp.sqrt(out[("one-step", 3, False)]), 2.0, 0.15)
limit("-(n+1)/2*log(1 + r**2/n)", "n", "oo", "-r**2/2")
units("(73.49 km/s/Mpc - 67.58 km/s/Mpc) / (0.93 km/s/Mpc)", "dimensionless")
raise SystemExit(finish())
