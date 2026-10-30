"""M-MECHANIST-01: gap sizes in mag and percent, naive sigma (finding 2).
Claim: for local H_l and early H_e (km/s/Mpc, both > 0), the equivalent distance-modulus offset is
Δm = 5 log10(H_l/H_e) (at fixed redshift d_L ∝ 1/H0, μ = 5 log10(d_L/10 pc)), the fractional gap is
H_l/H_e − 1, and the naive tension is |H_l − H_e|/sqrt(σ_l² + σ_e²) (uncorrelated Gaussians).
Inputs (dossier): H0DN 73.264 ± 0.806 [D-22]; SH0ES 2025 73.49 ± 0.93, R22 73.04 ± 1.04 [D-20];
CMB-SPA 67.19 ± 0.38 [D-44]; BAO+BBN 68.50 ± 0.58 [D-45]; CCHP 70.39 with quad-sum 1.94 [D-24];
M_B ladder −19.253, inverse −19.375/−19.394 [D-21].
"""
import math
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/mechanist")
import sympy as sp
from math_checks import identity, limit, series, quantity, finish
from mm_common import dmag, near, tension

# Symbolic: derive Δm from μ = 5 log10(cz/H0 / 10pc) at fixed z
Hl, He, cz, d10 = sp.symbols("H_l H_e cz d10", positive=True)
mu = lambda H: 5 * sp.log(cz / H / d10, 10)
identity(sp.expand_log(mu(He) - mu(Hl), force=True), 5 * sp.log(Hl / He) / sp.log(10))
x = sp.symbols("x", positive=True)
limit("5*log(1+x)/log(10)", "x", 0, "0")                       # equal H0 -> no offset
series("5*log(1+x)/log(10)", "x", 0, 2, "5*x/log(10)")         # small-gap: 2.17 mag per unit fraction
quantity("73.264 km/s/Mpc / (67.19 km/s/Mpc)", "1.0904", rel_tol=1e-4)   # units cancel

print("Gap numbers")
near("H0DN vs CMB-SPA dH", 73.264 - 67.19, 6.07, 0.006)
near("H0DN vs CMB-SPA percent", 100 * (73.264 / 67.19 - 1), 9.0, 0.05)
near("H0DN vs CMB-SPA mag", dmag(73.264, 67.19), 0.188, 0.0006)
near("H0DN vs CMB-SPA naive sigma", tension(73.264, 0.806, 67.19, 0.38), 6.8, 0.05)
near("SH0ES 2025 vs CMB-SPA mag", dmag(73.49, 67.19), 0.195, 0.0006)
near("R22 vs CMB-SPA mag", dmag(73.04, 67.19), 0.181, 0.0006)
near("H0DN vs BAO+BBN mag", dmag(73.264, 68.50), 0.146, 0.0006)
near("SH0ES 2025 vs BAO+BBN mag", dmag(73.49, 68.50), 0.153, 0.0006)
near("CCHP vs CMB-SPA mag", dmag(70.39, 67.19), 0.101, 0.0006)
near("CCHP vs CMB-SPA naive sigma", tension(70.39, 1.94, 67.19, 0.38), 1.6, 0.05)
cchp_quad = math.sqrt(1.22**2 + 1.33**2 + 0.70**2)
near("CCHP quad-sum error", cchp_quad, 1.94, 0.01)
near("SH0ES 2025 - CCHP mag", dmag(73.49, 70.39), 0.094, 0.0006)
near("SH0ES-CCHP fraction of gap", dmag(73.49, 70.39) / dmag(73.264, 67.19), 0.5, 0.01)
near("M_B gap cosmography", -19.253 - (-19.375), 0.122, 1e-9)
near("M_B gap flat LCDM", -19.253 - (-19.394), 0.141, 1e-9)
raise SystemExit(finish())
