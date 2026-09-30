"""Statistician lens, part 3: how rare is the observed normalized disagreement under the empirical
heavy-tailed (Student-t, nu ~ 2-4; Bailey 2017) distribution of measurement disagreements, versus Gaussian.
Dimensionless."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from scipy import stats
from stats_tools import sigma_to_p

for z, lab in [(4.63, "p-beam vs storage"), (4.10, "BL1 vs storage"), (3.80, "Serebrov18 vs Musedinovic25"),
               (2.95, "material vs magnetic"), (2.24, "J-PARC vs p-beam"), (3.49, "PERKEO III vs aSPECT 2024")]:
    g = sigma_to_p(z, two_sided=True)
    row = ["%s z=%.2f: Gaussian p2 %.2e" % (lab, z, g)]
    for nu in (2, 3, 4):
        row.append("t(nu=%d) p2 %.3f" % (nu, 2 * stats.t.sf(z, nu)))
    print("; ".join(row))
# Likelihood ratio: density of z under t_nu (unit scale) vs Gaussian -> how much more probable a 4.63 sigma
# unrecognised-error outcome is than a pure fluctuation
from stats_tools import sidak_global_p, p_to_sigma, min_bayes_factor, prior_needed
for z, n, lab in [(2.95, 5, "material vs magnetic, ~5 post-hoc splits of storage"),
                  (3.49, 3, "lambda A-route vs a-route, ~3 splits of lambda data"),
                  (2.24, 1, "J-PARC vs p-beam (pre-stated test)")]:
    pl = sigma_to_p(z, two_sided=True); pg = sidak_global_p(pl, n)
    b = min_bayes_factor(pl)
    print("%s: local z %.2f -> global p %.3g, z %.2f; Sellke max odds %.1f:1, prior needed for 50%% %.3f"
          % (lab, z, pg, p_to_sigma(pg, True), b["max_odds_against_null"], prior_needed(b["max_odds_against_null"])))
for nu in (2, 3, 4):
    print("nu=%d: density ratio t/Gauss at z=4.63: %.0f" % (nu, stats.t.pdf(4.63, nu) / stats.norm.pdf(4.63)))
