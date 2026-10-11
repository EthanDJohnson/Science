"""Examiner lens: numerical tests of hidden premises (SI units unless stated).

A. Is "gamma_MOND in the scoring bin" one number?  (premise 10; scoring rule)
B. Is the bin itself well defined?  g_N with r = 1.2 s vs r = s  (premise 6)
C. Mass normalisation degeneracy  (premise 7)
D. Galactic tide size at 10 kau  (is "real but not gravity-law" a live option?)
E. Eccentricity-template mismatch, from dossier D-48 medians  (premise 5)
F. Parent-catalogue proper-motion cut and the E2 sqrt(2) cut under Newton vs MOND  (premises 1, 4, 8)
G. Separation dependence of the triple effect on the median, and the f_triple rise needed
   to fake gamma ~ 1.37 in a full-median test calibrated at high acceleration  (premise 2)
"""
import sys
import numpy as np
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import wide_binary_population as wbp

G = 6.674e-11
MSUN = 1.989e30
AU = 1.496e11
PC = 3.086e16
A0 = 1.2e-10

print("=== A. gamma_MOND (force boost, dimensionless) at log10 g_N [m/s^2] ===")
models = ["chae2024", "bz18_simple", "bz18_standard", "isolated"]
for lg in (-9.5, -9.84, -10.0, -10.16, -10.5, -11.0):
    vals = [float(wbp.gamma_mond(10 ** lg, model=m)) for m in models]
    print(f"log gN={lg:6.2f}: " + "  ".join(f"{m}={v:.3f}" for m, v in zip(models, vals)))
for m in ("bz18_simple", "bz18_standard", "chae2024"):
    L = wbp.efe_limit(model=m)
    print(f"EFE limit {m}: eta={L['eta']:.4f} gamma_par={L['gamma_par']:.4f} gamma_perp={L['gamma_perp']:.4f}")

print("\n=== B. bin definition: g_N proxy with r = 1.2 s vs r = s ===")
shift = np.log10(1.2 ** 2)
print(f"factor (r/s)^2 = {1.2**2:.3f}  -> bin shift = {shift:.3f} dex")
for m in ("chae2024", "bz18_simple"):
    g1 = float(wbp.gamma_mond(1e-10, model=m)); g2 = float(wbp.gamma_mond(10 ** (-10 - shift), model=m))
    g3 = float(wbp.gamma_mond(10 ** (-10 + shift), model=m))
    print(f"{m}: gamma(1e-10)={g1:.3f}; at -0.158 dex {g2:.3f}; at +0.158 dex {g3:.3f}")
# s at which g_N = 1e-10 for M = 1.5 Msun, under both conventions
M = 1.5 * MSUN
for ros in (1.0, 1.2):
    s = np.sqrt(G * M / 1e-10) / ros
    print(f"M=1.5 Msun, r/s={ros}: g_N=1e-10 m/s^2 at s = {s/AU:.0f} au")

print("\n=== C. mass normalisation: gamma_app = M_true / M_est (v~ ∝ M^-1/2) ===")
for mt, me in ((1.56, 2.0), (2.0, 1.56), (1.0, 0.9), (1.0, 1.1)):
    print(f"M_true={mt} Msun, M_assumed={me} Msun -> gamma_app factor = {mt/me:.3f}")
print("Required uniform mass UNDER-estimate to fake gamma=1.37 at fixed true gamma=1: M_est/M_true = "
      f"{1/1.37:.3f}  (i.e. {100*(1-1/1.37):.1f}% low)  -- but only if confined to the low-g_N bin")

print("\n=== D. Galactic tidal acceleration at r = 10 kau vs g_N ===")
kmskpc = 1e3 / (1e3 * PC)          # (km/s/kpc) in s^-1
A_, B_ = 15.3, -11.9               # Oort constants, km/s/kpc (approx. literature values)
tid_plane = 4 * A_ * (A_ - B_) * kmskpc ** 2 * (1e4 * AU)
rho = 0.1 * MSUN / PC ** 3         # local mid-plane density ~0.1 Msun/pc^3 (approx.)
tid_z = 4 * np.pi * G * rho * (1e4 * AU)
gN10 = G * 1.5 * MSUN / (1e4 * AU) ** 2
print(f"in-plane tide ~ {tid_plane:.2e} m/s^2; vertical tide ~ {tid_z:.2e} m/s^2; g_N(1.5 Msun, 10 kau) = {gN10:.2e} m/s^2;"
      f" ratio (vertical/g_N) = {tid_z/gN10:.1e}")

print("\n=== E. eccentricity-template mismatch from dossier D-48 median v~ (no noise) ===")
med = dict(circular=0.6925, e05=0.6159, uniform=0.5896, thermal=0.5269, a13=0.5134, a2=0.4880, a4=0.4486)
pairs = [("thermal", "a13"), ("a13", "thermal"), ("a13", "a2"), ("a2", "a13"), ("a13", "uniform")]
for templ, true in pairs:
    print(f"template {templ:8s} true {true:8s}: gamma_app = (med_true/med_templ)^2 = {(med[true]/med[templ])**2:.3f}")

print("\n=== F/G. synthetic catalogues (wide_binary_population.generate, DR3 noise) ===")
N = 60000
def cat(gravity, f_triple, s_lo, s_hi, seed, ecc="htz"):
    return wbp.generate(N, gravity=gravity, ecc=ecc, f_triple=f_triple, release="DR3",
                        s_range=(s_lo * AU, s_hi * AU), seed=seed)

# F: parent-catalogue cut v~ <= sqrt(5 Msun / M_est) (El-Badry+21 5 Msun circular-orbit bound, no 2-sigma allowance)
for grav, lab in ((1.0, "Newton"), ("chae2024", "MOND chae2024")):
    c = cat(grav, 0.0, 5000, 30000, 7)
    vt = c["vtilde"]; Mest = c["M_est"] / MSUN
    cut = np.sqrt(5.0 / Mest)
    lost_parent = np.mean(vt > cut)
    lost_e2 = np.mean(vt > np.sqrt(2))
    print(f"{lab:14s} 5-30 kau, no triples: frac removed by v~>sqrt(5/M) = {lost_parent:.4f}; by v~>sqrt2 = {lost_e2:.4f};"
          f" median v~ = {np.median(vt):.4f}; median M_est = {np.median(Mest):.2f} Msun")

# G: triple effect on median vs separation (Newton)
zones = {"calib 300-700 au": (300, 700), "test 5-30 kau": (5000, 30000)}
base = {}
for zname, (lo, hi) in zones.items():
    meds = {}
    for f in (0.0, 0.1, 0.2, 0.3, 0.45, 0.6):
        c = cat(1.0, f, lo, hi, 100 + int(100 * f))
        meds[f] = float(np.median(c["vtilde"]))
    base[zname] = meds
    print(f"{zname}: median v~ by f_triple: " + ", ".join(f"{f}:{m:.4f}" for f, m in meds.items()))
    print(f"   gamma_app vs f=0 template: " + ", ".join(f"{f}:{(m/meds[0.0])**2:.3f}" for f, m in meds.items()))
t = base["test 5-30 kau"]
print("If f_triple is calibrated at 0.2 but the true wide-zone value is f: gamma_app = (med(f)/med(0.2))^2 =")
print("   " + ", ".join(f"f={f}:{(t[f]/t[0.2])**2:.3f}" for f in t))
# MOND reference median in the test zone
cm = cat("chae2024", 0.2, 5000, 30000, 999)
print(f"MOND chae2024 with f=0.2, test zone: gamma_app vs Newton f=0.2 = {(np.median(cm['vtilde'])/t[0.2])**2:.3f}")
