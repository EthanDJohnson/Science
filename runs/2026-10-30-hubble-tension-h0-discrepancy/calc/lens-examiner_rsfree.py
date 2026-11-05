"""Examiner lens: does the r_s-free (sound-horizon-free) class discriminate early-time new physics?

Units: H0 in km/s/Mpc. Asymmetric errors: the side facing the other value (stats_tools.tension).
If an early-time r_s reduction were the whole answer, H0 inferred WITHOUT r_s from BAO/CMB-shape
data should agree with the local ~73, not with the r_s-based ~67-68. Inputs: D-49, D-50, D-20, D-44.
Caveat: the D-49 sets share DESI DR1 and are correlated; they are not combined here.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from stats_tools import tension  # noqa: E402

shoes = (73.49, 0.93)        # D-20
cmb = (67.19, 0.38)          # D-44
rsfree = {
    "Zaborowski CMBlens x unWISE": (69.2, (1.3, 1.4)),
    "Zaborowski DES Y3 6x2pt": (70.3, (1.4, 1.2)),
    "Zaborowski CMBlens + DESY5 SNe": (69.6, (1.3, 1.8)),
    "2411.16677 DESY5": (66.7, (1.7, 1.9)),
    "2411.16677 Pantheon+": (67.9, (1.9, 2.1)),
    "2411.16677 Union3": (67.8, (2.0, 2.2)),
    "Philcox equality (Pantheon Om)": (65.1, (3.0, 5.4)),
    "Philcox equality (BAO-lensing)": (70.6, (3.7, 5.0)),
}
print("r_s-free H0 vs SH0ES 73.49+-0.93 and vs CMB-SPA 67.19+-0.38 (km/s/Mpc)")
for k, (v, e) in rsfree.items():
    a = tension(v, e, *shoes)
    b = tension(v, e, *cmb)
    print(f"  {k:34s} {v:5.1f}  z_vs_SH0ES={a['z']:.2f}  z_vs_CMB={b['z']:.2f}")
print("Reading: an early-time r_s reduction predicts these ~73 (they bypass r_s); late-universe or ladder")
print("explanations predict them ~67-68. A 1.5% r_s-free H0 (sigma ~1.0) would separate 73.3 from 67.5 at ~5.8 sigma.")
d = 73.3 - 67.5
print(f"  separation for sigma_rsfree=1.0 (plus SH0ES/CMB not needed): z = {d/1.0:.1f}")
