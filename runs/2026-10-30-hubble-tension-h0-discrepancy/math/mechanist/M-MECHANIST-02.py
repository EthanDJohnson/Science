"""M-MECHANIST-02: single-rung required sizes (finding 3, table B).
(a) Crowding. Crowding adds flux to host Cepheids, making them too BRIGHT in HST (smaller m), which
    shortens host distances, makes calibrator SN M_B too faint, shortens Hubble-flow distances, raises H0.
    To raise H0 by the 0.188 mag gap, m_HST - m_true = -0.188 mag, so with JWST as truth
    HST - JWST = -0.188 mag. Dossier D-78 quotes "HST-JWST = -0.01 +- 0.03 mag". The lens writes
    "JWST-HST = -0.01 +- 0.03" and gets 6.6 sigma.
(b) Metallicity. Δm_H0 = γ·L with lever L (dex). Dropping the term: 73.50 -> 73.08 [D-23]; γ = -0.234 ± 0.052.
(c) Dust: 0.188 / 0.03. (d) Anchors: 9.04% / per-anchor precision (NGC 4258 0.073/7.558; MW 0.9%).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/mechanist")
import sympy as sp
from math_checks import identity, sign, finish
from mm_common import dmag, near

gap = dmag(73.264, 67.19)
# (a) sign chain: dH0/H0 = -(ln10/5) * d(mu_host) ; d(mu_host) = d(m_ceph) (P-L zero point fixed by anchors)
dm = sp.symbols("dm", real=True)
dlnH = -(sp.log(10) / 5) * dm           # host Cepheid m bias -> H0 bias
sign(dlnH, "positive", domain={"dm": (-1, -1e-6)})   # brighter (negative dm) -> H0 up
needed_HST_minus_JWST = -gap
meas, sig = -0.01, 0.03                  # D-78 convention HST-JWST
n_dossier = abs(needed_HST_minus_JWST - meas) / sig
n_flipped = abs(needed_HST_minus_JWST - (+0.01)) / sig   # lens's JWST-HST = -0.01 means HST-JWST = +0.01
print(f"crowding: sigma with D-78 sign = {n_dossier:.2f}; with lens's flipped sign = {n_flipped:.2f}")
near("crowding sigma (dossier convention) vs lens 6.6", n_dossier, 6.6, 0.15)   # expected to FAIL
near("crowding sigma (lens convention) reproduces 6.6", n_flipped, 6.6, 0.05)

# (b) metallicity
g, L, dg = sp.symbols("gamma_Z L dgamma", positive=True)
identity(sp.diff(g * L, g) * dg, L * dg)   # linear lever: error in slope times lever
lever_mag = dmag(73.50, 73.08)
near("metallicity lever mag", lever_mag, 0.012, 0.0006)
lever_dex = lever_mag / 0.234
near("lever dex", lever_dex, 0.05, 0.004)
slope_err = gap / lever_dex
near("slope error needed mag/dex", slope_err, 3.5, 0.05)
near("slope error in sigma", slope_err / 0.052, 68, 1.0)
# (c) dust
near("dust ratio", gap / 0.03, 6.3, 0.05)
# (d) anchors
frac = 100 * (10 ** (gap / 5) - 1)
near("distance scale error %", frac, 9.0, 0.05)
near("NGC4258 precision %", 100 * 0.073 / 7.558, 0.97, 0.005)
near("NGC4258 sigma", frac / (100 * 0.073 / 7.558), 9.0, 0.5)
near("MW sigma", frac / 0.9, 10.0, 0.1)
raise SystemExit(finish())
