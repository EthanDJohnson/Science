"""Falsifier C8-0 (magnitude): size and significance of the team-independent
(non-SH0ES) local H0 excess, its robustness to input choices, and whether it
is distinguishable from the SH0ES gap.
Units: H0 in km/s/Mpc (astronomical units); magnitudes in mag; z in Gaussian sigma.
Inputs from dossier: D-20, D-22, D-23, D-24, D-25, D-29, D-30, D-31, D-32, D-33, D-44, D-45, D-42.
"""
import math
import numpy as np

def q(*a):
    return math.sqrt(sum(x * x for x in a))

def ivw(vals):
    w = np.array([1 / s ** 2 for _, s in vals])
    x = np.array([v for v, _ in vals])
    m = (w * x).sum() / w.sum()
    return m, w.sum() ** -0.5

def gls(x, C):
    Ci = np.linalg.inv(C)
    one = np.ones(len(x))
    var = 1 / (one @ Ci @ one)
    return var * (one @ Ci @ x), math.sqrt(var)

def z(a, sa, b, sb):
    return (a - b) / q(sa, sb)

def p2(zz):
    return math.erfc(abs(zz) / math.sqrt(2))

# local, non-SH0ES (symmetrised totals)
CCHP = (70.39, q(1.22, 1.33, 0.70))           # D-24
CCHP_JW = (68.81, q(1.79, 1.32))              # D-25 JWST-only
SBF = (73.8, q(0.7, 2.3))                     # D-29
TF = (73.3, q(2.1, 3.5))                      # D-30 (Cepheid/TRGB zero point)
TD = (71.1, 2.35)                             # D-31 symmetrised
MAS = (71.6, 3.7)                             # D-32 stat only
GW = (71.7, (9.4 + 7.5) / 2)                  # D-33 symmetrised
SH0ES = (73.49, 0.93)                         # D-20
H0DN = (73.264, 0.806)                        # D-22
H0DN_noCeph = (72.509, 1.296)                 # D-23 V08
refs = {"CMB-SPA": (67.19, 0.38), "Planck+SPT+ACT(H0DN)": (67.24, 0.35),
        "BAO+BBN": (68.50, 0.58), "DESI+CMB": (68.17, 0.28),
        "P-ACT-LB DR2": (68.43, 0.27), "PR4": (67.64, 0.52)}

base = {"CCHP": CCHP, "SBF": SBF, "TF": TF, "TD": TD, "MAS": MAS, "GW": GW}

def report(label, m, s):
    zs = ", ".join(f"{k} {z(m, s, *v):.2f}" for k, v in refs.items())
    print(f"{label:46s} {m:6.2f} +- {s:4.2f} | excess vs SPA {m-67.19:4.2f} "
          f"({5*math.log10(m/67.19):.3f} mag) | z: {zs}")

print("=== 1. Non-SH0ES local combination (candidate's set) ===")
m0, s0 = ivw(list(base.values()))
report("non-SH0ES IVW (6 classes)", m0, s0)

print("\n=== 2. Robustness variants ===")
v = dict(base); v["CCHP"] = CCHP_JW
report("CCHP -> JWST-only 68.81", *ivw(list(v.values())))
v = dict(base); v.pop("TF")
report("drop TF (Cepheid-zero-point)", *ivw(list(v.values())))
v = dict(base); v.pop("TF"); v["CCHP"] = CCHP_JW
report("drop TF + CCHP JWST-only", *ivw(list(v.values())))
v = dict(base); v["MAS"] = (71.6, 2 * 3.7)
report("ASSUMED: maser sigma doubled for sys", *ivw(list(v.values())))
for k in base:
    v = dict(base); v.pop(k)
    report(f"leave out {k}", *ivw(list(v.values())))
# GLS: CCHP, SBF and masers share NGC 4258 at 1.45% in distance (D-29, D-32, M-EXAMINER-04)
keys = list(base); x = np.array([base[k][0] for k in keys])
C = np.diag([base[k][1] ** 2 for k in keys])
shared = ["CCHP", "SBF", "MAS"]
for i, a in enumerate(keys):
    for j, b in enumerate(keys):
        if i != j and a in shared and b in shared:
            C[i, j] = (0.0145 * x[i]) * (0.0145 * x[j])
report("GLS shared NGC4258 (CCHP,SBF,MAS) off-diag", *gls(x, C))
report("H0DN without Cepheids (D-23 V08)", *H0DN_noCeph)

print("\n=== 3. Is the non-SH0ES excess smaller than the SH0ES excess? ===")
d = SH0ES[0] - m0; sd = q(SH0ES[1], s0)
print(f"SH0ES - nonSH0ES = {d:.2f} +- {sd:.2f} km/s/Mpc, {d/sd:.2f} sigma "
      f"({5*math.log10(SH0ES[0]/m0):.3f} mag)")
ex, sex = m0 - 67.19, q(s0, 0.38)
print(f"non-SH0ES excess over CMB-SPA {ex:.2f} +- {sex:.2f}; 95% interval "
      f"[{ex-1.96*sex:.2f}, {ex+1.96*sex:.2f}]; SH0ES gap 6.30 lies "
      f"{(6.30-ex)/sex:.2f} sigma above it")
frac = math.log10(m0 / 67.19) / math.log10(SH0ES[0] / 67.19)
print(f"fraction of the 0.195 mag gap carried by the non-SH0ES excess: {frac:.2f}")
# expected significance if the true local value equals SH0ES
zexp = (SH0ES[0] - 67.19) / q(s0, 0.38)
zobs = (m0 - 67.19) / q(s0, 0.38)
print(f"expected z of non-SH0ES set if true local = 73.49: {zexp:.2f}; observed {zobs:.2f}; "
      f"shortfall {zexp - zobs:.2f} sigma (one-sided p = {0.5*math.erfc((zexp-zobs)/math.sqrt(2)):.3f})")
need5 = 67.19 + 5 * q(s0, 0.38)
print(f"non-SH0ES central value needed for 5 sigma vs CMB-SPA at sigma {s0:.2f}: {need5:.2f}")
# decomposition of the significance drop 6.27 -> zobs
zS = (SH0ES[0] - 67.19) / q(SH0ES[1], 0.38)
print(f"SH0ES z {zS:.2f}; drop factor {zobs/zS:.3f} = gap factor {(m0-67.19)/6.30:.3f} x "
      f"sigma factor {q(SH0ES[1],0.38)/q(s0,0.38):.3f}")

print("\n=== 4. SH0ES itself against r_d-based references (is >=5 sigma CMB-specific?) ===")
for k, vv in refs.items():
    print(f"SH0ES vs {k}: {z(*SH0ES, *vv):.2f} sigma; H0DN vs {k}: {z(*H0DN, *vv):.2f}")

print("\n=== 5. Within-local consistency (SH0ES vs rest) chi2 ===")
allv = list(base.values()) + [SH0ES]
ma, sa = ivw(allv)
chi = sum(((vv - ma) / ss) ** 2 for vv, ss in allv)
print(f"all-local (7) IVW {ma:.2f} +- {sa:.2f}; chi2 {chi:.2f}/6")
