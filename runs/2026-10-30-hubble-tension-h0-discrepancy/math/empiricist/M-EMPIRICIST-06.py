"""M-EMPIRICIST-06: between-class chi^2 among local classes.
Classes: Cepheid-SN (SH0ES), TRGB-SN (CCHP), non-SN ladder (SBF, with or without TF), one-step (TDCOSMO,
masers, sirens). Each class is its inverse-variance mean; chi^2 = Σ (m_g - M)^2 / s_g^2 about the
weighted mean M of the classes, dof = 4 - 1 = 3. Claim: chi^2 = 2.90, p = 0.41, 0.83σ (two-sided equivalent).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/empiricist")
import mpmath as mp
from math_checks import identity, finish
from _common import H, gls, cmp

# chi^2 survival for 3 dof in closed form: Q(3/2, x/2) = erfc(sqrt(x/2)) + sqrt(2x/pi) exp(-x/2)
x = mp.mpf("2.9")
q_gamma = mp.gammainc(mp.mpf(1.5), x / 2, mp.inf, regularized=True)
q_closed = mp.erfc(mp.sqrt(x / 2)) + mp.sqrt(2 * x / mp.pi) * mp.exp(-x / 2)
identity(str(q_gamma), str(q_closed))


def chi2(groups):
    ms = [gls(g) for g in groups]
    w = [1 / s**2 for _, s in ms]
    M = sum(wi * m for wi, (m, _) in zip(w, ms)) / sum(w)
    return float(sum((m - M) ** 2 / s**2 for m, s in ms)), ms


for label, nonsn in {"SBF only": ["SBF"], "SBF + TF": ["SBF", "TF"]}.items():
    c, ms = chi2([["SH0ES"], ["CCHP"], nonsn, ["TDCOSMO", "masers", "sirens"]])
    p = float(mp.gammainc(1.5, c / 2, mp.inf, regularized=True))
    z = float(mp.sqrt(2) * mp.erfinv(1 - p))
    print(f"  {label}: groups {[(round(m, 2), round(s, 2)) for m, s in ms]}, chi2 = {c:.3f}, p = {p:.3f}, {z:.2f} sigma")
    if label == "SBF only":
        cmp("chi2 (SBF-only non-SN class)", c, 2.90, 0.006)
        cmp("p", p, 0.41, 0.006)
        cmp("sigma equivalent", z, 0.83, 0.006)
raise SystemExit(finish())
