#!/usr/bin/env python3
"""Statistics toolkit for /conundrum's statistics lens (standard library only).

Is a claimed signal real? These functions cover the calculations that most often go wrong
when significance is estimated by hand:

    sigma_to_p, p_to_sigma          Gaussian tail conversions (one- or two-sided)
    poisson_p_value                 P(N >= n_obs) for a counting experiment with known background
    asimov_z                        expected discovery significance for s signal over b background,
                                    optionally with an uncertainty on b (Cowan's formula)
    sidak_global_p                  look-elsewhere correction for N independent tries
    gross_vitells_global_p          look-elsewhere correction from up-crossings of a scanned test statistic
    fisher_combined_p, stouffer_z   combining independent results
    weighted_mean                   inverse-variance mean, chi2 and the PDG scale factor for disagreeing data
    min_bayes_factor                the most evidence a p-value can carry against the null
    posterior_probability           prior probability x Bayes factor -> posterior probability
    exposure_to_reach               how much more data a real effect needs to reach a target significance

Run from the project root:
    python3 .claude/skills/conundrum/scripts/stats_tools.py selftest
In a script:
    import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
    from stats_tools import sigma_to_p, sidak_global_p, min_bayes_factor
"""
from __future__ import annotations

import math
import sys

SQRT2 = math.sqrt(2.0)


# ---------------------------------------------------------------- Gaussian tails
def sigma_to_p(z: float, two_sided: bool = False) -> float:
    """Tail probability beyond z standard deviations. One-sided by default (particle-physics convention)."""
    p = 0.5 * math.erfc(z / SQRT2)
    return min(1.0, 2 * p) if two_sided else p


def p_to_sigma(p: float, two_sided: bool = False) -> float:
    """Inverse of sigma_to_p, by bisection on erfc (accurate to ~1e-12 in z for 1e-300 < p < 1)."""
    if not 0.0 < p < 1.0:
        raise ValueError("p must be strictly between 0 and 1")
    target = p / 2 if two_sided else p
    lo, hi = -40.0, 40.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if 0.5 * math.erfc(mid / SQRT2) > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------- counting experiments
def poisson_p_value(n_obs: int, background: float) -> float:
    """P(N >= n_obs) for N ~ Poisson(background): the chance of at least this many events from background alone."""
    if n_obs <= 0:
        return 1.0
    if background <= 0:
        return 0.0
    # Sum the shorter tail in log space to stay accurate for large counts.
    log_terms = [k * math.log(background) - background - math.lgamma(k + 1) for k in range(n_obs)]
    top = max(log_terms)
    below = math.exp(top) * sum(math.exp(t - top) for t in log_terms)
    if below < 0.5:
        return 1.0 - below
    k, upper, term = n_obs, 0.0, 1.0
    while term > 1e-17 * max(upper, 1e-300) or k < background + 20:
        term = math.exp(k * math.log(background) - background - math.lgamma(k + 1))
        upper += term
        k += 1
        if k > n_obs + 10_000_000:
            break
    return upper


def asimov_z(signal: float, background: float, sigma_b: float = 0.0) -> float:
    """Median expected significance for discovering `signal` events over `background` events.

    With sigma_b = 0: Z = sqrt(2((s+b) ln(1+s/b) - s)), which tends to s/sqrt(b) for s << b.
    With an absolute uncertainty sigma_b on the background, Cowan's formula (G. Cowan, "Discovery
    sensitivity for a counting experiment with background uncertainty", 2012) applies.
    """
    s, b = float(signal), float(background)
    if s <= 0:
        return 0.0
    if sigma_b <= 0:
        return math.sqrt(2 * ((s + b) * math.log(1 + s / b) - s))
    v = sigma_b**2
    term1 = (s + b) * math.log((s + b) * (b + v) / (b * b + (s + b) * v))
    term2 = (b * b / v) * math.log1p(v * s / (b * (b + v)))   # log1p: tiny sigma_b must recover the no-uncertainty limit
    return math.sqrt(max(0.0, 2 * (term1 - term2)))


# ---------------------------------------------------------------- look-elsewhere effect
def sidak_global_p(p_local: float, n_trials: float) -> float:
    """Global p-value when the best of n independent tries is reported: 1 - (1 - p)^n."""
    return -math.expm1(n_trials * math.log1p(-p_local))


def gross_vitells_global_p(z_local: float, upcrossings_ref: float, z_ref: float = 0.0) -> float:
    """Look-elsewhere correction for a scanned search (one free parameter, chi^2 with 1 dof).

    upcrossings_ref: average number of times the scanned significance crosses z_ref upward,
    counted in background-only data or pseudo-experiments. Gross & Vitells (2010):
        p_global ~ p_local + N(z_ref) exp(-(z_local^2 - z_ref^2)/2).
    """
    p_local = sigma_to_p(z_local)
    return min(1.0, p_local + upcrossings_ref * math.exp(-(z_local**2 - z_ref**2) / 2))


# ---------------------------------------------------------------- combining results
def fisher_combined_p(p_values) -> float:
    """Fisher's method: X = -2 sum ln p_i is chi^2 with 2k dof under the null (closed form for even dof)."""
    ps = list(p_values)
    x = -2 * sum(math.log(p) for p in ps)
    half = x / 2
    return math.exp(-half) * sum(half**j / math.factorial(j) for j in range(len(ps)))


def stouffer_z(z_values, weights=None) -> float:
    """Stouffer's combined z: sum(w z) / sqrt(sum w^2)."""
    zs = list(z_values)
    ws = list(weights) if weights is not None else [1.0] * len(zs)
    return sum(w * z for w, z in zip(ws, zs)) / math.sqrt(sum(w * w for w in ws))


def weighted_mean(values, errors) -> dict:
    """Inverse-variance mean with chi^2 and the PDG scale factor S = sqrt(chi^2/(N-1)) when S > 1."""
    vals, errs = list(values), list(errors)
    w = [1 / e**2 for e in errs]
    mean = sum(wi * x for wi, x in zip(w, vals)) / sum(w)
    err = 1 / math.sqrt(sum(w))
    chi2 = sum(wi * (x - mean) ** 2 for wi, x in zip(w, vals))
    dof = len(vals) - 1
    scale = math.sqrt(chi2 / dof) if dof > 0 and chi2 > dof else 1.0
    return {"mean": mean, "error": err, "chi2": chi2, "dof": dof, "scale_factor": scale,
            "error_scaled": err * scale, "p_consistent": _chi2_sf(chi2, dof) if dof > 0 else 1.0}


def _chi2_sf(x: float, dof: int) -> float:
    """Survival function of chi^2 for integer dof (series for the regularized incomplete gamma)."""
    a, half = dof / 2, x / 2
    if half <= 0:
        return 1.0
    if half < a + 1:   # lower series, then complement
        term = total = 1 / a
        n = 1
        while abs(term) > 1e-16 * abs(total):
            term *= half / (a + n)
            total += term
            n += 1
        lower = total * math.exp(-half + a * math.log(half) - math.lgamma(a))
        return max(0.0, 1 - lower)
    # continued fraction for the upper tail (Lentz)
    tiny = 1e-300
    b = half + 1 - a
    c, d = 1 / tiny, 1 / b
    h = d
    for i in range(1, 10000):
        an = -i * (i - a)
        b += 2
        d = an * d + b
        d = tiny if abs(d) < tiny else d
        c = b + an / c
        c = tiny if abs(c) < tiny else c
        d = 1 / d
        delta = d * c
        h *= delta
        if abs(delta - 1) < 1e-15:
            break
    return math.exp(-half + a * math.log(half) - math.lgamma(a)) * h


# ---------------------------------------------------------------- Bayesian calibration
def min_bayes_factor(p: float) -> dict:
    """Lower bounds on the Bayes factor for the null against the alternative, given a p-value.

    sellke: -e p ln p (Sellke, Bayarri & Berger 2001), valid for p < 1/e.
    gaussian: exp(-z^2/2) with z the two-sided z-score (Edwards, Lindman & Savage 1963), the
    bound over all alternatives for a Gaussian test statistic.
    max_odds_against_null is 1/sellke: the strongest evidence the p-value can represent.
    """
    sellke = -math.e * p * math.log(p) if p < 1 / math.e else 1.0
    z = p_to_sigma(p, two_sided=True)
    return {"sellke": sellke, "gaussian": math.exp(-z * z / 2), "max_odds_against_null": 1 / sellke}


def posterior_probability(prior_prob: float, bayes_factor_alt_vs_null: float) -> float:
    """Posterior probability of the alternative from its prior probability and the Bayes factor."""
    odds = prior_prob / (1 - prior_prob) * bayes_factor_alt_vs_null
    return odds / (1 + odds)


def prior_needed(bayes_factor_alt_vs_null: float, target_posterior: float = 0.5) -> float:
    """Prior probability the alternative needs to reach target_posterior with this Bayes factor."""
    target_odds = target_posterior / (1 - target_posterior)
    prior_odds = target_odds / bayes_factor_alt_vs_null
    return prior_odds / (1 + prior_odds)


def exposure_to_reach(z_now: float, z_target: float = 5.0) -> float:
    """Factor by which data (events, time, luminosity) must grow for a real, fixed effect to reach
    z_target, given it shows z_now: significance grows as sqrt(exposure), so (z_target/z_now)^2."""
    return (z_target / z_now) ** 2


# ---------------------------------------------------------------- self-test
def selftest(verbose: bool = True) -> bool:
    """Check against standard reference values. Returns True when every check passes."""
    results = []

    def check(name, got, want, rel=1e-3):
        ok = abs(got - want) <= rel * abs(want)
        results.append(ok)
        if verbose:
            print(f"{'PASS' if ok else 'FAIL'}  {name}: {got:.6g} (expected {want:.6g})")

    check("5 sigma one-sided p", sigma_to_p(5), 2.8665e-7)
    check("3 sigma one-sided p", sigma_to_p(3), 1.3499e-3)
    check("1.96 sigma two-sided p", sigma_to_p(1.959964, two_sided=True), 0.05)
    check("p = 2.8665e-7 back to sigma", p_to_sigma(2.8665157e-7), 5.0, rel=1e-6)
    check("Poisson P(N >= 10 | b = 3)", poisson_p_value(10, 3.0), 1.1025e-3)
    check("Asimov Z, s = 10 over b = 100", asimov_z(10, 100), 0.98399)
    check("Sidak: p = 1e-3 over 100 tries", sidak_global_p(1e-3, 100), 0.095208)
    check("Fisher: two p = 0.05", fisher_combined_p([0.05, 0.05]), 0.0025 * (1 + 2 * math.log(20)), rel=1e-9)
    check("Stouffer: two z = 1.6449", stouffer_z([1.644854, 1.644854]), 1.644854 * math.sqrt(2), rel=1e-9)
    check("Sellke bound at p = 0.05", min_bayes_factor(0.05)["sellke"], 0.40716)
    wm = weighted_mean([1.0, 3.0], [1.0, 1.0])
    check("weighted mean of 1 and 3", wm["mean"], 2.0)
    check("PDG scale factor for 1 +- 1 vs 3 +- 1", wm["scale_factor"], math.sqrt(2))
    check("chi2 survival, x = 3.84, 1 dof", _chi2_sf(3.841459, 1), 0.05)
    check("chi2 survival, x = 20, 10 dof", _chi2_sf(20.0, 10), 0.029253)
    check("exposure for 3 -> 5 sigma", exposure_to_reach(3.0), 25 / 9)
    passed = all(results)
    if verbose:
        print(f"\n{sum(results)}/{len(results)} checks passed")
    return passed


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        sys.exit(0 if selftest() else 1)
    print(__doc__)
