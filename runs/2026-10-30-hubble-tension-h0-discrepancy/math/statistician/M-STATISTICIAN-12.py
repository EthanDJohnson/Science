"""M-STATISTICIAN-12: precision a deciding measurement needs (F19).
Separate two hypotheses H_a, H_b at k sigma with a measurement of total error sigma: sigma = |H_a - H_b|/k
(optionally with the reference's own error s_ref in quadrature: sigma = sqrt((Delta/k)^2 - s_ref^2)).
N objects with per-object error sigma_1 and floor f: sigma^2 = sigma_1^2/N + f^2 -> N = sigma_1^2/(sigma^2 - f^2)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/statistician")
import mpmath as mp
from _common import quad, close
from math_checks import limit, units, finish

E, L, EDE, sref = mp.mpf("67.58"), mp.mpf("73.3"), mp.mpf("71.0"), mp.mpf("0.318")
for (a, b, k, cl) in [(E, L, 3, 1.91), (E, L, 5, 1.14), (E, EDE, 3, 1.14), (E, EDE, 5, 0.68), (EDE, L, 3, 0.77), (EDE, L, 5, 0.46)]:
    close(f"sigma needed {float(a)} vs {float(b)} at {k} sigma", abs(b - a) / k, cl, 0.01)


def nobj(sig1, delta, k, floor=0, ref=0):
    tgt2 = (delta / k) ** 2 - ref**2
    den = tgt2 - floor**2
    return mp.inf if den <= 0 else sig1**2 / den


for s_lens in (mp.mpf("2.35"), mp.mpf("2.4")):
    s1 = s_lens * mp.sqrt(11)
    for ref in (0, sref):
        r = [nobj(s1, L - E, 3, 0, ref), nobj(s1, L - E, 5, 0, ref), nobj(s1, EDE - E, 3, 0, ref),
             nobj(s1, L - E, 5, mp.mpf("0.71"), ref), nobj(s1, EDE - E, 5, mp.mpf("0.71"), ref)]
        print(f"11-lens error {float(s_lens)}, ref err {float(ref)}: N = " + ", ".join(f"{float(x):.1f}" for x in r))
s1 = mp.mpf("2.35") * mp.sqrt(11)
close("lenses, 3 sigma 67.6 vs 73.3 (lens 17)", nobj(s1, L - E, 3, 0, sref), 17, 1.5)
close("lenses, 5 sigma 67.6 vs 73.3 (lens ~50)", nobj(s1, L - E, 5, 0, sref), 50, 4)
close("lenses, 3 sigma 67.6 vs 71.0 (lens ~51)", nobj(s1, EDE - E, 3, 0, sref), 51, 4)
close("lenses, 5 sigma 67.6 vs 73.3 with 1% floor (lens 79)", nobj(mp.mpf("2.4") * mp.sqrt(11), L - E, 5, mp.mpf("0.71")), 79, 5)
print("  67.6 vs 71.0 at 5 sigma with floor 0.71 > 0.684 -> never:", nobj(s1, EDE - E, 5, mp.mpf("0.71")))
s_gw = mp.mpf("0.15") * 70
close("sirens 3 sigma (lens ~30)", nobj(s_gw, L - E, 3), 30, 1.5)
close("sirens 5 sigma (lens ~84)", nobj(s_gw, L - E, 5), 84, 3)
print("CCHP cap")
close("max z, sys only", mp.mpf("3.10") / mp.mpf("1.33"), 2.33, 0.005)
stat_now = quad(1.22, 0.70, 0.93)
need = mp.sqrt((mp.mpf("3.10") / 3) ** 2 - (mp.mpf("1.33") / 2) ** 2)
close("data factor with halved sys (lens 4.6)", (stat_now / need) ** 2, 4.6, 0.1)
close("difference error for 5 sigma", mp.mpf("3.10") / 5, 0.62, 0.001)
limit("s1**2/((d/k)**2 - f**2)", "f", 0, "s1**2*k**2/d**2")
units("10.5 km/s/Mpc / 30^0.5", "km/s/Mpc")
raise SystemExit(finish())
