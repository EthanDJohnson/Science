"""M-STAT-10  (statistician F9, F10, F4, F13)

Claims checked, stated precisely.
  (a) Lap-time tension [A-14]: 4.92 +/- 0.10 s vs 5.14 +/- 0.09 s gives
      z = |4.92 - 5.14|/sqrt(0.10^2 + 0.09^2) = 1.6 when the quoted s.d. is read as one trial's
      uncertainty, and z > 7 when it is read as the s.d. of n = 25 trials (errors on the means
      sigma/sqrt(25)).
  (b) Granularity inference: 44.0, 76.0 and 20.0 per cent are integer multiples of 1/25 and
      85.0 and 50.0 per cent of 1/20, so the smallest trial counts consistent with the reported
      percentages are n = 25 (simulation) and n = 20 (real world).
  (c) Minimum Bayes factor (Sellke-Bayarri-Berger calibration of a two-sided p-value):
      BF_alt:null <= 1/(-e p ln p), and the prior probability needed for a posterior of 0.5 is
      1/(1 + BF). The lens asserts BF <= 10.1 and prior 0.090 for p = 0.0074; BF <= 5.1 and
      prior 0.165 for p = 0.018; BF <= 3.9 and prior 0.203 for p = 0.0256; and a posterior of
      0.72 at a prior of 0.20 with BF = 10.1.
Domain: times in s (SI), uncertainties in s; p in (0, 1/e) for the SBB bound; probabilities and
Bayes factors dimensionless.

Independent derivation: z from quadrature addition of independent Gaussian errors; the trial
counts from an exhaustive search over n of the smallest n with k/n equal to every reported
percentage; the SBB bound from its definition -e p ln p (the minimum of the Bayes factor for the
null over the class of one-sided-in-the-p-value calibrations), with the posterior from Bayes'
rule on odds.
"""
import math
import sys

from fractions import Fraction

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, inequality, limit, quantity, series, units  # noqa: E402


def z_tension(x1, e1, x2, e2):
    return abs(x1 - x2) / math.sqrt(e1 ** 2 + e2 ** 2)


def smallest_n(percentages, nmax=2000):
    for n in range(1, nmax):
        if all((Fraction(int(round(p * 1000)), 100000) * n).denominator == 1 for p in percentages):
            return n
    return None


def min_bf(p):
    """SBB lower bound on BF_null:alt is -e p ln p; the reciprocal bounds BF_alt:null."""
    if not 0 < p < 1 / math.e:
        raise ValueError("bound applies for p < 1/e")
    return 1.0 / (-math.e * p * math.log(p))


print("=== M-STAT-10: lap-time tension (s), trial-count granularity, Bayes-factor bounds ===")
z1 = z_tension(4.92, 0.10, 5.14, 0.09)
z25 = z_tension(4.92, 0.10 / 5, 5.14, 0.09 / 5)
print(f"4.92 +/- 0.10 s vs 5.14 +/- 0.09 s: z = {z1:.3f} (per-trial s.d.), z = {z25:.3f} (means of n = 25)")
print(f"difference = {5.14 - 4.92:.3f} s, combined per-trial sigma = {math.sqrt(0.01 + 0.0081):.4f} s")
print(f"smallest n for 44.0, 76.0, 20.0 per cent: {smallest_n([44.0, 76.0, 20.0])}")
print(f"smallest n for 85.0, 50.0 per cent      : {smallest_n([85.0, 50.0])}")
print(f"  (check: 0.44*25 = {0.44 * 25:.2f}, 0.76*25 = {0.76 * 25:.2f}, 0.20*25 = {0.20 * 25:.2f}, "
      f"0.85*20 = {0.85 * 20:.2f}, 0.50*20 = {0.50 * 20:.2f})")
for p in (0.0074, 0.018, 0.0256):
    bf = min_bf(p)
    print(f"two-sided p = {p:.4f}: min BF_alt:null <= {bf:.3f}; prior for posterior 0.5 = {1 / (1 + bf):.4f}; "
          f"posterior at prior 0.20 = {0.25 * bf / (1 + 0.25 * bf):.4f}")

units("4.92 s", "time")
units("1", "dimensionless")
quantity(f"{5.14 - 4.92:.4f} s", "0.22 s", rel_tol=1e-3)
quantity(f"{z1:.4f}", "1.6", rel_tol=3e-2)
inequality(f"{z25:.4f}", ">", "7")
quantity(f"{smallest_n([44.0, 76.0, 20.0])}", "25", rel_tol=1e-6)
quantity(f"{smallest_n([85.0, 50.0])}", "20", rel_tol=1e-6)
quantity(f"{min_bf(0.0074):.4f}", "10.1", rel_tol=5e-3)
quantity(f"{min_bf(0.018):.4f}", "5.1", rel_tol=5e-3)
quantity(f"{min_bf(0.0256):.4f}", "3.9", rel_tol=1e-2)
quantity(f"{1 / (1 + min_bf(0.0074)):.5f}", "0.090", rel_tol=5e-3)
quantity(f"{1 / (1 + min_bf(0.018)):.5f}", "0.165", rel_tol=5e-3)
quantity(f"{1 / (1 + min_bf(0.0256)):.5f}", "0.203", rel_tol=5e-3)
quantity(f"{0.25 * min_bf(0.0074) / (1 + 0.25 * min_bf(0.0074)):.5f}", "0.72", rel_tol=5e-3)
# limits: a vanishing p-value lets the Bayes factor diverge; p -> 1/e makes the bound reach 1
limit("(-exp(1)*p*log(p))", "p", 0, "0", domain={"p": (1e-9, 0.3)})
quantity(f"{-math.e * (1 / math.e) * math.log(1 / math.e):.6f}", "1.0", rel_tol=1e-6)
# the tension z must fall as 1/sqrt(n) when errors are means of n
series("1.6349/sqrt(1 + x)", "x", 0, 2, "1.6349 - 1.6349*x/2", domain={"x": (1e-6, 0.5)})
limit("1.6349/sqrt(n)", "n", "oo", "0", domain={"n": (1.0, 1e6)})
raise SystemExit(finish())
