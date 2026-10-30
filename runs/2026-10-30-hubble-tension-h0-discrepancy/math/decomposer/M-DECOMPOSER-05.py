"""M-DECOMPOSER-05: fraction of the gap closed by new-physics fits (F5).

fraction = (H_fit - H_ref)/(H_target - H_ref), with H_ref = 67.19 (CMB-SPA) and H_target = 73.264
(H0DN corrected; the lens writes 73.26). All km/s/Mpc.
"""
import sys
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/decomposer")
from _common import num, finish, limit, units

REF, TGT = 67.19, 73.264
fits = {"ACT DR6 EDE": (69.9, 45), "PMF": (69.1, 31), "modified recombination": (69.6, 40),
        "NPIPE EDE upper": (69.5, 38), "Poulin 2026 EDE": (71.0, 63), "eROSITA+ EDE": (71.4, 69),
        "DESI w0wa DESI+CMB": (63.6, -59), "DESI w0wa + Pantheon+": (67.51, 5)}
for k, (h, pct) in fits.items():
    num(f"{k} fraction %", 100 * (h - REF) / (TGT - REF), pct, 0.6)
num("eROSITA residual km/s/Mpc", TGT - 71.4, 1.9, 0.06)
# Q4a residual range 1.9-4.2: 73.26 - 71.4 and 73.26 - 69.1
num("largest residual (PMF)", TGT - 69.1, 4.2, 0.06)
from _common import identity
identity("((r + t)/2 - r)/(t - r)", "1/2", domain={"r": (60, 68), "t": (70, 80)})
units("(69.9 km/s/Mpc - 67.19 km/s/Mpc)/(73.264 km/s/Mpc - 67.19 km/s/Mpc)", "dimensionless")
raise SystemExit(finish())
