"""Falsifier C3-0 (magnitude): what shift does a ~1.1% invisible dark-decay branch produce in each
class of measurement, and can it carry the whole beam-storage gap consistently across classes?

Units: lifetimes in s (SI); lambda = |gA/gV|, Vud, Br_X dimensionless.
Inputs (from runs/.../candidates.md prediction matrix and dossier D-23, U-01 calc):
  proton-beam combination 887.97 +- 2.04 s (S-scaled); BL1 887.7 +- 2.25 s
  all storage 878.32 +- 0.43 s; UCNtau 877.82 +- 0.30 s
  J-PARC 2024 electron counting 877.2 +4.35/-3.98 s (D-23)
  Vud = 0.97361(32) with the GS2023 inner RC (consistent pairing, U-01)
  lambda: PERKEO III 1.27641(56); UCNA 2018 1.27720(20e-4); PERKEO II 1.27480(13e-4);
          aSPECT 2024 1.26680(28e-4); aCORN 1.27960(62e-4)   (as used in calc/user_rc_pairing.py)
Under C3 (invisible branch, no p, no e): proton beams AND electron-counting beams AND the SM
formula all give tau_beta; storage gives tau_n = tau_beta (1 - Br_X).
"""
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from neutron_beta_decay import tau_beta, lambda_from_tau  # noqa: E402
from stats_tools import _chi2_sf, p_to_sigma  # noqa: E402

VUD, SVUD = 0.97361, 0.00032
PB, sPB = 887.97, 2.04
BL1, sBL1 = 887.7, 2.25
ST, sST = 878.32, 0.43
UT, sUT = 877.82, 0.30
JP, JPup, JPdn = 877.2, 4.35, 3.98
LAM = {
    "PERKEO III": (1.27641, 0.00056),
    "UCNA 2018": (1.27720, 0.0020),
    "PERKEO II": (1.27480, 0.0013),
    "aSPECT 2024": (1.26680, 0.0028),
    "aCORN": (1.27960, 0.0062),
}

print("=" * 78)
print("1. Branch needed to carry the whole gap")
br_all = 1 - ST / PB
br_bl1 = 1 - UT / BL1
print(f"Br_X needed (proton-beam combo vs all storage) = {100*br_all:.3f} %  (gap {PB-ST:.2f} s)")
print(f"Br_X needed (BL1 vs UCNtau)                    = {100*br_bl1:.3f} %  (gap {BL1-UT:.2f} s)")

print("=" * 78)
print("2. Shift C3 produces in each class, relative to tau_n = storage 878.32 s")
shift = PB - ST
print(f"proton-counting beam : predicted +{shift:.2f} s ; observed +{PB-ST:.2f} s (fit by construction)")
print(f"electron-counting J-PARC : predicted +{shift:.2f} s ; observed {JP-ST:+.2f} s")
zJ = (PB - JP) / math.hypot(JPup, sPB)
print(f"   J-PARC vs C3 prediction (tau_beta = {PB}): z = {zJ:.2f} (upper J-PARC error {JPup} s)")
frac_J = (JP - ST) / shift
sf = math.hypot(JPup, sST) / shift
print(f"   fraction of the C3 shift J-PARC shows: {frac_J:+.2f} +- {sf:.2f}  (C3 needs 1.00)")
print("material & magnetic bottles: predicted 0 shift between them (both read tau_n)")

print("=" * 78)
print("3. SM tau_beta from each lambda (GS2023 RC, Vud 0.97361(32)) and the implied Br_X")
sm = {}
for k, (l, s) in LAM.items():
    r = tau_beta(l, s, VUD, SVUD, rc_set="GS2023")
    sm[k] = (r["tau"], r["sigma"])
    br = 1 - ST / r["tau"]
    sbr = (ST / r["tau"]) * math.hypot(sST / ST, r["sigma"] / r["tau"])
    zn = (br_all - br) / sbr
    frac = (r["tau"] - ST) / shift
    print(f"{k:12s} tau_beta = {r['tau']:.2f} +- {r['sigma']:.2f} s ; Br_X = {100*br:+.3f} +- {100*sbr:.3f} % ;"
          f" needed 1.087% at {zn:+.1f} sigma ; fraction of gap = {frac:+.2f}")

print("=" * 78)
print("4. lambda that C3 needs (tau_beta = proton-beam 887.97 +- 2.04 s)")
rl = lambda_from_tau(PB, sPB, VUD, SVUD, rc_set="GS2023")
lam_need = rl["lam"]
print("lambda_from_tau output:", {k: v for k, v in rl.items()} if isinstance(rl, dict) else rl)
ln = rl["lam"]
sln = rl["sigma"]
for k, (l, s) in LAM.items():
    print(f"   {k:12s} {l:.5f}({s:.5f}) : distance from needed {ln:.5f} = {(l-ln)/math.hypot(s, sln):+.1f} sigma "
          f"(= {(l-ln)/s:+.1f} x its own error)")

# chi2 of the lambda data set at C3's lambda vs at its own best fit
def chi2_at(x, keys):
    return sum(((LAM[k][0] - x) / LAM[k][1]) ** 2 for k in keys)
keys = list(LAM)
w = [1 / LAM[k][1] ** 2 for k in keys]
lbest = sum(wi * LAM[k][0] for wi, k in zip(w, keys)) / sum(w)
slbest = 1 / math.sqrt(sum(w))
c_best = chi2_at(lbest, keys)
c_need = chi2_at(ln, keys)
print(f"lambda world (5 expts) weighted mean {lbest:.5f}({slbest:.5f}); chi2 = {c_best:.2f}/4")
print(f"chi2 of same data at C3's lambda {ln:.5f}: {c_need:.2f}/5 ; Delta chi2 = {c_need-c_best:.1f}")
S = math.sqrt(c_best / 4)
print(f"with PDG-style scale factor S = {S:.2f}: Delta chi2/S^2 = {(c_need-c_best)/S**2:.1f}"
      f" -> {math.sqrt(max(0,(c_need-c_best)/S**2)):.1f} sigma")

print("=" * 78)
print("5. Joint consistency of the tau_beta class under C3 (tau_beta free; PB, J-PARC, SM-lambda)")

def fit(points):
    # iterate to pick the J-PARC side
    t = PB
    for _ in range(20):
        pts = []
        for x, e in points:
            if isinstance(e, tuple):
                e = e[0] if t > x else e[1]
            pts.append((x, e))
        ws = [1 / e ** 2 for _, e in pts]
        t = sum(wi * x for wi, (x, _) in zip(ws, pts)) / sum(ws)
    chi = sum(((x - t) / e) ** 2 for x, e in pts)
    return t, chi, len(pts) - 1

cases = {
    "PB + J-PARC + PERKEO III tau_beta": [(PB, sPB), (JP, (JPup, JPdn)), sm["PERKEO III"]],
    "PB + J-PARC + aSPECT tau_beta": [(PB, sPB), (JP, (JPup, JPdn)), sm["aSPECT 2024"]],
    "PB + J-PARC + world-lambda tau_beta": None,
    "PB + J-PARC only": [(PB, sPB), (JP, (JPup, JPdn))],
}
rw = tau_beta(lbest, slbest * S, VUD, SVUD, rc_set="GS2023")
print(f"world-lambda (S-scaled) tau_beta = {rw['tau']:.2f} +- {rw['sigma']:.2f} s")
cases["PB + J-PARC + world-lambda tau_beta"] = [(PB, sPB), (JP, (JPup, JPdn)), (rw["tau"], rw["sigma"])]
for name, pts in cases.items():
    t, chi, dof = fit(pts)
    p = _chi2_sf(chi, dof) if dof > 0 else float("nan")
    z = p_to_sigma(p, two_sided=True) if dof > 0 else float("nan")
    print(f"C3: {name:38s} tau_beta fit {t:.2f} s ; chi2 = {chi:.2f}/{dof} ; p = {p:.2e} ; {z:.1f} sigma")

print("--- same data under 'no branch' (tau_beta = tau_n = 878.32 +- 0.43; proton beam biased, C1-like)")
for name, pts in cases.items():
    pts2 = [q for q in pts if q[0] != PB]
    chi = 0.0
    for x, e in pts2:
        if isinstance(e, tuple):
            e = e[0] if ST > x else e[1]
        chi += ((x - ST) ** 2) / (e ** 2 + sST ** 2)
    print(f"Br=0: {name:38s} chi2 = {chi:.2f}/{len(pts2)}")

print("=" * 78)
print("6. What part of the gap can C3 carry if every tau_beta-class datum is used?")
# fit Br_X with tau_n = storage; tau_beta = ST/(1-Br); data PB, J-PARC, world-lambda
for label, extra in (("world lambda", (rw["tau"], rw["sigma"])), ("PERKEO III", sm["PERKEO III"])):
    t, chi, dof = fit([(PB, sPB), (JP, (JPup, JPdn)), extra])
    # error on t
    ws = [1 / sPB**2, 1 / (JPup if t > JP else JPdn)**2, 1 / extra[1]**2]
    st = 1 / math.sqrt(sum(ws))
    br = 1 - ST / t
    print(f"{label:12s}: best tau_beta {t:.2f} +- {st:.2f} s -> Br_X = {100*br:.2f} % ; "
          f"carries {100*(t-ST)/shift:.0f} % of the gap; proton beam then {(PB-t)/math.hypot(sPB, st):.1f} sigma high")

print("=" * 78)
print("7. Sanity checks")
t0 = tau_beta(1.27641, 0.0, VUD, 0.0, rc_set="GS2023")["tau"]
print("PASS" if abs(t0 - 878.50) < 0.05 else "FAIL", f"PERKEO III tau_beta {t0:.2f} s reproduces U-01 calc 878.50 s")
print("PASS" if abs(br_bl1 - 0.01113) < 5e-5 else "FAIL", f"BL1/UCNtau Br_X {br_bl1:.5f} matches candidates' 1.113%")
t1 = tau_beta(ln, 0.0, VUD, 0.0, rc_set="GS2023")["tau"]
print("PASS" if abs(t1 - PB) < 0.01 else "FAIL", f"round trip lambda_needed -> tau_beta {t1:.3f} s")

print("=" * 78)
print("8. Robustness: J-PARC stat error inflated by S = sqrt(15.8/3) = 2.29 (its internal scatter)")
Sj = math.sqrt(15.8 / 3)
JPu2, JPd2 = math.hypot(1.7 * Sj, 4.0), math.hypot(1.7 * Sj, 3.6)
print(f"J-PARC inflated errors +{JPu2:.2f}/-{JPd2:.2f} s")
for label, extra in (("world lambda", (rw["tau"], rw["sigma"])), ("PERKEO III", sm["PERKEO III"]),
                     ("aSPECT 2024", sm["aSPECT 2024"]), ("none", None)):
    pts = [(PB, sPB), (JP, (JPu2, JPd2))] + ([extra] if extra else [])
    t, chi, dof = fit(pts)
    p = _chi2_sf(chi, dof)
    print(f"C3 with {label:12s}: tau_beta fit {t:.2f} s ; chi2 = {chi:.2f}/{dof} ; {p_to_sigma(p, two_sided=True):.1f} sigma ;"
          f" Br_X best {100*(1-ST/t):.2f} % = {100*(t-ST)/shift:.0f} % of gap")
print("=" * 78)
print("9. Note: the candidates' '9.5 sigma' treats the needed Br_X (1.087%) as exact; including the proton-beam")
zfull = (PB - sm["PERKEO III"][0]) / math.hypot(sPB, sm["PERKEO III"][1])
print(f"error (the needed value's own uncertainty), PERKEO III vs proton beam under C3 is {zfull:.2f} sigma")
