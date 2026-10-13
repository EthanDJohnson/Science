"""Mechanist lens: physical coherent-state coefficients for realistic polarisation patterns vs B&O's real-sign model.

Uses the toolkit gw_coherent_fusion (tree-level g g -> gamma gamma inside one coherent packet, physical helicity
amplitudes with phases from qft_second_order). Natural units hbar = c = 1.
c_tot: per-packet in-out pair yield P = c_tot G^2 N^2 w^3 sigma (a TOTAL).
c_rate: B&O bookkeeping 'rate' P/T_eff = c_rate G^2 N^2 w^3 sigma^2 (B&O eq. 8: 3/(25 pi) = 0.0382 for photons).
Quadrature uncertainty of the physical patterns ~2-4% (tool docstring).
"""
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import gw_coherent_fusion as gf  # noqa: E402

print(f"B&O eq. 8 coefficient 3/(25 pi) = {3/(25*math.pi):.6f}; per-packet 4/25 = {4/25:.6f}")
ref = None
for prof in ("tophat", "gaussian"):
    for pat in ("bo_real_sign", "circular_binary", "linear_quadrupole", "pure_circular"):
        c = gf.coefficients(pat, prof)
        if pat == "bo_real_sign" and prof == "tophat":
            ref = c
        print(f"{pat:18s} {prof:8s} photon: c_tot = {c['c_tot']:.5g}  c_rate = {c['c_rate']:.5g}"
              f"  c_tot/c_tot(B&O tophat) = {c['c_tot']/ref['c_tot']:.4g}  c_rate/(3/(25pi)) = {c['c_rate']/(3/(25*math.pi)):.4g}")
