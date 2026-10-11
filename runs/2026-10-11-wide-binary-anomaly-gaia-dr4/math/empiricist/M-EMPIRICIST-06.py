"""M-EMPIRICIST-06: alpha_grav -> gamma conversion (F7, L1).

Brief's scoring rule: gamma = 1 + alpha (gamma_M - 1). alpha = -0.021 +0.065/-0.045 (Banik+24).
Claims: gamma = 0.993 +0.022/-0.015 for gamma_M = 1.333; 0.991 +0.029/-0.020 for gamma_M = 1.44.
The map is linear and increasing in alpha for gamma_M > 1, so errors map as (gamma_M - 1) * sigma_alpha.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, sign, inequality, finish

a, gM = sp.symbols("alpha gM", real=True)
g = 1 + a * (gM - 1)
dom = {"alpha": (-1, 2), "gM": (1.01, 2)}
limit(g, "alpha", 0, "1", domain=dom)            # Newton template
identity(g.subs(a, 1), gM, domain=dom)           # MOND template, alpha = 1
sign(sp.diff(g, a), "positive", domain=dom)       # monotone: upper error of alpha -> upper error of gamma
for gm, lens in [(1.333, (0.993, 0.022, 0.015)), (1.44, (0.991, 0.029, 0.020))]:
    c = 1 - 0.021 * (gm - 1); up = 0.065 * (gm - 1); dn = 0.045 * (gm - 1)
    print(f"gM = {gm}: gamma = {c:.4f} +{up:.4f} -{dn:.4f} (lens {lens})")
    inequality(f"abs({c} - {lens[0]})", "<", "0.0006")
    inequality(f"abs({up} - {lens[1]})", "<", "0.0006")
    inequality(f"abs({dn} - {lens[2]})", "<", "0.0006")
# insensitivity: d gamma/d gM = alpha, so across gM 1.333->1.44 the centre moves by -0.021*0.107
print(f"centre shift across gM 1.333 -> 1.44: {-0.021*(1.44-1.333):.5f}")
identity(sp.diff(g, gM), a, domain=dom)
raise SystemExit(finish())
