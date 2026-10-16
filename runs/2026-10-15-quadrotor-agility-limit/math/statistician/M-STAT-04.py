"""M-STAT-04  (statistician F5, F11; STAT-B, STAT-H; table row S5)

Claim checked, stated precisely.
  Nine demonstrated speeds v_i (m/s) are grouped by course type. Working in x_i = ln(v_i / 1 m/s)
  with an *assigned* common fractional spread sigma = 0.20 (so sigma_x = 0.20, the lens's own
  assumption, no source quotes an uncertainty), and modelling each x_i as Gaussian with that
  standard deviation:
    within-group chi2 = 2.97 (2 dof, seen gate track, geometric mean 26.2 m/s),
                        5.28 (3 dof, unseen clutter, 7.4 m/s),
                        0.47 (1 dof, mocap, 33.0 m/s);
    between-group chi2 = 104.2 (2 dof), p = 2.4e-23, z = 10.0;
    pooled weighted mean 15.7 m/s with PDG scale factor S = 3.76;
    at sigma = 0.80 the between-group chi2 is 6.5 (2 dof, p = 0.039);
    with equicorrelated within-group errors at rho = 0.8 the between-group chi2 is 37.6 (2 dof,
    p = 6.7e-9, z = 5.8) and the unseen-clutter group's own mean carries an 18 % effective error.
  Group membership is reconstructed from the dossier speeds the lens cites: seen gate track
  {27.8, 32.2, 20.0} m/s [A-26 abstract, A-26 table, A-31]; unseen clutter {10, 8, 7, 5.3} m/s
  [A-20 x2, A-29 x2]; mocap {30.0, 36.4} m/s [A-12, A-02]. The reconstruction is validated by
  reproducing the lens's three group means to 0.1 m/s.
Domain: v_i > 0 (m/s), sigma_x > 0, rho in [0, 1).

Independent derivation: for a group of n equicorrelated measurements with covariance
  C = sigma_x^2 [(1 - rho) Id + rho J], the generalised-least-squares mean and its variance are
  computed from C^{-1} directly (numpy solve), giving var(mean) = sigma_x^2 (1 + (n-1) rho)/n;
within-group chi2 = (x - mean)^T C^{-1} (x - mean); between-group chi2 = sum_g (m_g - M)^2/var_g
with M the inverse-variance weighted mean of the group means. Scale invariance of the whole
construction under v -> c v is checked explicitly (so the choice of 1 m/s as the log reference
cannot matter).
"""
import sys

import numpy as np
from scipy.stats import chi2 as chi2dist
from scipy.stats import norm

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, inequality, limit, quantity, units  # noqa: E402

GROUPS = {
    "seen gate track": [27.8, 32.2, 20.0],
    "unseen clutter": [10.0, 8.0, 7.0, 5.3],
    "mocap peak": [30.0, 36.4],
}


def analyse(groups, sig=0.20, rho=0.0, scale=1.0):
    means, varm, within = [], [], {}
    for name, vals in groups.items():
        x = np.log(np.array(vals) * scale)
        n = len(x)
        C = sig ** 2 * ((1 - rho) * np.eye(n) + rho * np.ones((n, n)))
        Ci = np.linalg.inv(C)
        one = np.ones(n)
        vm = 1.0 / (one @ Ci @ one)
        m = vm * (one @ Ci @ x)
        r = x - m
        within[name] = (float(r @ Ci @ r), n - 1, float(np.exp(m) if scale == 1 else np.exp(m) / scale))
        means.append(m)
        varm.append(vm)
    means, varm = np.array(means), np.array(varm)
    w = 1 / varm
    M = float(np.sum(w * means) / np.sum(w))
    between = float(np.sum(w * (means - M) ** 2))
    return within, between, len(means) - 1, M, np.sqrt(varm)


print("=== M-STAT-04: grouped chi2 of ln(speed/1 m/s), speeds in m/s ===")
within, between, dof, M, se = analyse(GROUPS)
for name, (c, d, gm) in within.items():
    print(f"within {name:16s}: chi2 = {c:.3f} / {d} dof, geometric mean = {gm:.2f} m/s")
p_bet = chi2dist.sf(between, dof)
print(f"between groups     : chi2 = {between:.2f} / {dof} dof, p = {p_bet:.3g}, "
      f"z(one-sided) = {norm.isf(p_bet):.2f}, z(two-sided) = {norm.isf(p_bet / 2):.2f}")
allx = np.log(np.concatenate([np.array(v) for v in GROUPS.values()]))
pooled_mean = allx.mean()
pooled_chi2 = float(np.sum((allx - pooled_mean) ** 2) / 0.20 ** 2)
S = np.sqrt(pooled_chi2 / (len(allx) - 1))
print(f"pooled weighted mean = {np.exp(pooled_mean):.2f} m/s; pooled chi2 = {pooled_chi2:.2f} / "
      f"{len(allx) - 1} dof; PDG scale factor S = {S:.3f}")
print(f"identity check: sum(within) + between = {sum(c for c, _, _ in within.values()) + between:.6f} "
      f"vs pooled {pooled_chi2:.6f}")
_, bet80, _, _, _ = analyse(GROUPS, sig=0.80)
print(f"at sigma = 0.80: between chi2 = {bet80:.2f}, p = {chi2dist.sf(bet80, 2):.3g}")
w8, bet8, _, _, se8 = analyse(GROUPS, rho=0.8)
p8 = chi2dist.sf(bet8, 2)
print(f"at rho = 0.8   : between chi2 = {bet8:.2f}, p = {p8:.3g}, z(one-sided) = {norm.isf(p8):.2f}")
print(f"               : effective errors on group means = {np.round(se8, 4)} (unseen clutter = {se8[1]:.4f})")
_, bet_kmh, _, _, _ = analyse(GROUPS, scale=3.6)
print(f"scale invariance (speeds in km/h): between chi2 = {bet_kmh:.6f} vs {between:.6f}")

units("27.8 m/s", "speed")
units("1", "dimensionless")                                  # chi2 and ln-ratios are dimensionless
quantity(f"{within['seen gate track'][0]:.4f}", "2.97", rel_tol=5e-3)
quantity(f"{within['unseen clutter'][0]:.4f}", "5.28", rel_tol=5e-3)
quantity(f"{within['mocap peak'][0]:.4f}", "0.47", rel_tol=1e-2)
quantity(f"{within['seen gate track'][2]:.4f} m/s", "26.2 m/s", rel_tol=3e-3)
quantity(f"{within['unseen clutter'][2]:.4f} m/s", "7.4 m/s", rel_tol=3e-3)
quantity(f"{within['mocap peak'][2]:.4f} m/s", "33.0 m/s", rel_tol=3e-3)
quantity(f"{between:.4f}", "104.2", rel_tol=3e-3)
quantity(f"{p_bet:.6g}", "2.4e-23", rel_tol=0.15)            # rounding of chi2 moves p by ~7 %
quantity(f"{norm.isf(p_bet / 2):.4f}", "10.0", rel_tol=1e-2)
quantity(f"{np.exp(pooled_mean):.4f} m/s", "15.7 m/s", rel_tol=3e-3)
quantity(f"{S:.4f}", "3.76", rel_tol=3e-3)
quantity(f"{bet80:.4f}", "6.5", rel_tol=1e-2)
quantity(f"{chi2dist.sf(bet80, 2):.6f}", "0.039", rel_tol=2e-2)
quantity(f"{bet8:.4f}", "37.6", rel_tol=5e-3)
quantity(f"{p8:.6g}", "6.7e-9", rel_tol=5e-2)
quantity(f"{norm.isf(p8 / 2):.4f}", "5.8", rel_tol=1e-2)
quantity(f"{se8[1]:.5f}", "0.18", rel_tol=3e-2)
inequality(f"abs({sum(c for c, _, _ in within.values()) + between:.9f} - {pooled_chi2:.9f})", "<", "1e-9")
inequality(f"abs({bet_kmh:.9f} - {between:.9f})", "<", "1e-9")
# the chi2 must scale as 1/sigma^2: 0.20 -> 0.80 divides it by 16
inequality(f"abs({bet80:.9f} - {between / 16:.9f})", "<", "1e-9")
# limits: an infinitely uncertain measurement cannot split the groups; rho -> 1 keeps it finite
limit("104.21/g**2", "g", "oo", "0", domain={"g": (1.0, 1e6)})
analytic = 0.20 ** 2 * (1 + 3 * 0.8) / 4
inequality(f"abs({se8[1] ** 2:.12f} - {analytic:.12f})", "<", "1e-12")
raise SystemExit(finish())
