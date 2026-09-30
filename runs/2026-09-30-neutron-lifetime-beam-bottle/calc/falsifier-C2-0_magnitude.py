"""Falsifier C2-0 (angle: magnitude). SI units: lifetimes in s, rates in s^-1.

C2: an unidentified loss ~1.2e-5 s^-1 common to material and magnetic UCN traps
shortens every storage result; proton beam ~888 s is the true lifetime.

Computes:
 1. Required extra loss rate per storage experiment (tau_true = BL1 887.7 s and
    proton-beam mean 887.97 s), split into the part independent of the beam
    and the part common to all (beam error).
 2. Fit of ONE common loss rate to all storage results (beam fixed): chi2.
    Compared with C1-style common tau: the same heterogeneity (not a discriminator).
 3. UCNtau (Gonzalez 2021 Table II) loss-type budget lines vs needed shift.
 4. Class-by-class shift table under C2 and residuals.
 5. Two-parameter fits C2 vs C1 on the class data incl. J-PARC.
"""
import math

# ---- inputs (dossier D-20/D-22/D-27..D-30, candidates.md reference block) ----
BL1 = (887.7, 2.25)
PBEAM = (887.97, 2.04)
JPARC = (877.2, 4.35, 3.98)  # +up / -down total
storage = {  # name: (tau, sigma_total, class)
    "Serebrov05": (878.5, math.hypot(0.7, 0.3), "mat"),
    "Pichlmaier10": (880.7, math.hypot(1.3, 1.2), "mat"),
    "Steyerl12": (882.5, math.hypot(1.4, 1.5), "mat"),
    "Arzumanov15": (880.2, 1.2, "mat"),
    "Gravitrap18": (881.5, math.hypot(0.7, 0.6), "mat"),
    "Ezhov18": (878.3, math.hypot(1.6, 1.0), "mag"),
    "UCNtau25": (877.82, math.hypot(0.22, 0.185), "mag"),
}

def lam(tb, tt):
    return 1.0 / tb - 1.0 / tt

print("== 1. Required extra loss rate per storage experiment ==")
print(f"{'expt':14s} {'tau':>8s} {'lam(BL1) s^-1':>14s} {'+-indep':>9s} {'+-beam(common)':>15s} {'shift s':>8s} {'x own sigma':>11s}")
rates = {}
for k, (t, s, c) in storage.items():
    l = lam(t, BL1[0])
    s_ind = s / t**2
    s_beam = BL1[1] / BL1[0]**2
    rates[k] = (l, s_ind, c)
    print(f"{k:14s} {t:8.2f} {l:14.4e} {s_ind:9.2e} {s_beam:15.2e} {t-BL1[0]:8.2f} {abs(t-BL1[0])/s:11.1f}")

# 2. common-rate fit (beam fixed at BL1): weighted mean of rates with independent errors
w = [1 / v[1]**2 for v in rates.values()]
lm = sum(wi * v[0] for wi, v in zip(w, rates.values())) / sum(w)
chi2 = sum(wi * (v[0] - lm)**2 for wi, v in zip(w, rates.values()))
N = len(rates)
p = math.exp(-chi2 / 2) * sum((chi2 / 2)**k / math.factorial(k) for k in range((N - 1) // 2 + 1)) if (N - 1) % 2 == 0 else float('nan')
print("\n== 2. One common loss rate for all 7 storage results ==")
print(f"best common lambda = {lm:.4e} s^-1 (+- {1/math.sqrt(sum(w)):.1e} indep, +- {BL1[1]/BL1[0]**2:.1e} from BL1)")
print(f"chi2 = {chi2:.2f} for {N-1} dof (p = {p:.4f})")
# C1 analogue: common tau for storage
wt = [1 / v[1]**2 for v in storage.values()]
tm = sum(wi * v[0] for wi, v in zip(wt, storage.values())) / sum(wt)
chi2t = sum(wi * (v[0] - tm)**2 for wi, v in zip(wt, storage.values()))
print(f"C1 analogue (common tau {tm:.2f} s): chi2 = {chi2t:.2f} for {N-1} dof -> heterogeneity is shared, not a C2-specific cost")
for cls in ("mat", "mag"):
    ws = [(1 / v[1]**2, v[0]) for v in rates.values() if v[2] == cls]
    m = sum(a * b for a, b in ws) / sum(a for a, _ in ws)
    print(f"class {cls}: required lambda = {m:.4e} +- {1/math.sqrt(sum(a for a,_ in ws)):.1e} (indep) s^-1")
ratio_min = min(v[0] for v in rates.values()); ratio_max = max(v[0] for v in rates.values())
print(f"range of required rates: {ratio_min:.3e} .. {ratio_max:.3e} s^-1, max/min = {ratio_max/ratio_min:.2f}")

print("\n== 3. UCNtau loss-type budget (Gonzalez 2021 Table II, s) vs needed shift ==")
need = PBEAM[0] - 877.82
need_bl1 = BL1[0] - 877.82
print(f"needed upward correction to UCNtau: {need:.2f} s (proton mean), {need_bl1:.2f} s (BL1)")
lines = {"Depolarization (+0.07 one-sided)": 0.07, "Uncleaned UCN (+0.11)": 0.11,
         "Heated UCN (+0.08)": 0.08, "Residual gas: 3 sigma above applied (3*0.06)": 0.18}
tot = sum(lines.values())
for k, v in lines.items():
    print(f"  {k:48s} {v:5.2f} s  = {100*v/need:5.2f}% of gap; gap = {need/v:6.1f} x line")
print(f"  linear sum of all loss-type lines at limits: {tot:.2f} s = {100*tot/need:.1f}% of the gap")
print(f"  total sys +0.20 s (Musedinovic 2025): gap = {need/0.20:.1f} x")
# depolarisation rate
l_need = lam(877.82, PBEAM[0])
print(f"  depolarisation bound 1.0e-7 s^-1 vs needed {l_need:.3e}: ratio {l_need/1e-7:.0f}")
l_gas = lam(877.82, 877.82 + 0.11)
print(f"  gas: applied correction 0.11 s <-> {l_gas:.3e} s^-1; needed/applied = {l_need/l_gas:.0f}x; "
      f"with 15% pressure uncertainty that is {(l_need/l_gas - 1)/0.15:.0f} sigma in pressure (if cross sections fixed)")
# fraction of stored UCN lost during a typical long hold
for th in (1000.0, 1400.0, 1550.0):
    print(f"  fraction of stored UCN removed by the unknown channel in {th:.0f} s: {100*(1-math.exp(-l_need*th)):.2f}%")

print("\n== 4. Class-by-class shift under C2 (agent = common storage loss only) ==")
classes = {"proton beam": PBEAM, "J-PARC e-beam": (877.2, 4.35), "material bottles": (880.03, 0.70),
           "magnetic traps": (877.82, 0.27)}
tau_true = PBEAM[0]
for name, (obs, s) in classes.items():
    gap = obs - tau_true
    if name in ("proton beam", "J-PARC e-beam"):
        shift = 0.0
    elif name == "material bottles":
        shift = obs - tau_true  # agent tuned to fit
    else:
        shift = obs - tau_true
    resid = obs - (tau_true + shift)
    se = math.hypot(s, PBEAM[1]) if name != "proton beam" else s
    print(f"{name:18s} observed-888 = {gap:+7.2f} s; C2 agent supplies {shift:+7.2f} s ({(100*shift/gap if gap else 0):5.0f}% of it); residual {resid:+6.2f} s ({abs(resid)/se:.2f} sigma)")
print("  J-PARC: C2's agent supplies 0 s of the needed -10.77 s; separate artefact required.")

print("\n== 5. Two-parameter class fits (proton, J-PARC, material, magnetic) ==")
# C2: tau free, lambda free (common to storage); beams read tau.
# C1: tau free, delta_beam free; J-PARC and storage read tau.
def chi2_c2(tau, l):
    ts = 1 / (1 / tau + l)
    js = 4.35 if 877.2 > tau else 3.98
    js = 4.35 if tau > 877.2 else 3.98
    return ((PBEAM[0]-tau)/PBEAM[1])**2 + ((877.2-tau)/js)**2 + ((880.03-ts)/0.70)**2 + ((877.82-ts)/0.27)**2
def chi2_c1(tau, d):
    js = 4.35 if tau > 877.2 else 3.98
    return ((PBEAM[0]-tau-d)/PBEAM[1])**2 + ((877.2-tau)/js)**2 + ((880.03-tau)/0.70)**2 + ((877.82-tau)/0.27)**2
best2 = min((chi2_c2(870 + i*0.01, l*1e-7), 870+i*0.01, l*1e-7) for i in range(0, 2500, 1) for l in range(0, 250, 1)
            if True) if False else None
# coarse-to-fine grid
def grid(f, xs, ys):
    return min((f(x, y), x, y) for x in xs for y in ys)
b2 = grid(chi2_c2, [870 + i*0.05 for i in range(500)], [j*1e-7 for j in range(0, 250)])
b2 = grid(chi2_c2, [b2[1] - 0.5 + i*0.005 for i in range(200)], [b2[2] - 1e-7 + j*1e-9 for j in range(200)])
b1 = grid(chi2_c1, [874 + i*0.01 for i in range(800)], [j*0.05 for j in range(0, 400)])
b1 = grid(chi2_c1, [b1[1] - 0.05 + i*0.001 for i in range(100)], [b1[2] - 0.1 + j*0.002 for j in range(100)])
print(f"C2 best: chi2 = {b2[0]:.2f} (tau = {b2[1]:.2f} s, lambda = {b2[2]:.3e} s^-1), 2 dof")
print(f"C1 best: chi2 = {b1[0]:.2f} (tau = {b1[1]:.2f} s, beam bias = {b1[2]:.2f} s), 2 dof")
print(f"delta chi2 (C2 - C1) = {b2[0]-b1[0]:.2f}; likelihood ratio C1:C2 = {math.exp((b2[0]-b1[0])/2):.1f}")
print(f"  C2 tau is pulled below BL1 to {b2[1]:.2f} s by J-PARC")
