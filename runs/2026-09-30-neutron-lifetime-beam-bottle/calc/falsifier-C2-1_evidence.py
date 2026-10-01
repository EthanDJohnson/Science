"""Falsifier C2-1 (evidence angle): how strongly the non-storage evidence contradicts
'the proton-beam value near 888 s is the true lifetime', and what loss each storage
experiment would need. Units: SI (s, s^-1)."""
import math

def wmean(vals):
    w = [1/s**2 for _, s in vals]
    m = sum(wi*v for wi, (v, _) in zip(w, vals))/sum(w)
    e = 1/math.sqrt(sum(w))
    chi2 = sum(((v-m)/s)**2 for v, s in vals)
    return m, e, chi2

def z(a, sa, b, sb):
    return (a-b)/math.hypot(sa, sb)

BL1 = (887.7, 2.25)          # D-20, stat (+) sys in quadrature
PROT = (887.97, 2.04)        # proton class (statistician)
JPARC_up = (877.2, 4.35)     # J-PARC 2024, upper error (faces the beam), D-23
JPARC_S = (877.2, 4.35*math.sqrt((2.29**2*1.7**2 + 4.0**2))/4.35/ math.hypot(1.7,4.0)*1.0)  # placeholder, replaced below
# J-PARC with stat inflated by S=2.29 (15.8/3), sys upper 4.0 s
JPARC_S = (877.2, math.hypot(2.29*1.7, 4.0))
A_route = (878.70, 0.83)     # tau_beta, beta-asymmetry group (U-01 / constraints)
a_route = (887.21, 2.93)     # tau_beta, proton-recoil group
aSPECT24 = (889.58, 3.20)

print("== 1. Non-storage evidence against 'beam value is true' ==")
for name, x in [("J-PARC (quoted)", JPARC_up), ("J-PARC (stat x2.29)", JPARC_S), ("A-route tau_beta", A_route)]:
    print(f"{name:22s} {x[0]:.2f} +- {x[1]:.2f} s : vs BL1 {z(BL1[0],BL1[1],x[0],x[1]):.2f} sigma, vs proton class {z(PROT[0],PROT[1],x[0],x[1]):.2f} sigma")
m, e, c = wmean([JPARC_up, A_route])
print(f"J-PARC + A-route combined: {m:.2f} +- {e:.2f} s (chi2 {c:.2f}/1); vs BL1 {z(BL1[0],BL1[1],m,e):.2f} sigma; vs proton class {z(PROT[0],PROT[1],m,e):.2f} sigma")
# SM route taking both lambda families with PDG-style scale factor
m2, e2, c2 = wmean([A_route, a_route])
S = math.sqrt(c2/1)
print(f"SM tau_beta, A and a groups together: {m2:.2f} +- {e2:.2f} s, chi2 {c2:.2f}/1, S = {S:.2f}, scaled error {e2*S:.2f} s")
print(f"   vs BL1 {z(BL1[0],BL1[1],m2,e2*S):.2f} sigma")
m3, e3, c3 = wmean([JPARC_up, (m2, e2*S)])
print(f"J-PARC + scaled SM route: {m3:.2f} +- {e3:.2f} s; vs BL1 {z(BL1[0],BL1[1],m3,e3):.2f} sigma; vs proton class {z(PROT[0],PROT[1],m3,e3):.2f} sigma")
m4, e4, c4 = wmean([JPARC_S, (m2, e2*S)])
print(f"J-PARC(inflated) + scaled SM route: {m4:.2f} +- {e4:.2f} s; vs BL1 {z(BL1[0],BL1[1],m4,e4):.2f} sigma")

print("\n== 2. Loss rate each storage result needs if BL1 (887.7 s) is true ==")
storage = {
    "UCNtau 2025 (magnetic)": (877.82, math.hypot(0.22, 0.20)),
    "Ezhov 2018 (magnetic)": (878.3, math.hypot(1.6, 1.0)),
    "Serebrov 2005 (material)": (878.5, math.hypot(0.7, 0.3)),
    "Arzumanov 2015 (material)": (880.2, 1.2),
    "MAMBO II 2010 (material)": (880.7, math.hypot(1.3, 1.2)),
    "Gravitrap 2018 (material)": (881.5, math.hypot(0.7, 0.6)),
    "Steyerl 2012 (material)": (882.5, math.hypot(1.4, 1.5)),
}
Ls = []
for k, (t, s) in storage.items():
    L = 1/t - 1/BL1[0]
    sL = s/t**2          # storage error only; BL1 error common to all, treated separately
    Ls.append((L, sL))
    print(f"{k:28s} tau {t:.2f} +- {s:.2f} s -> needed loss {L*1e6:6.2f} +- {sL*1e6:.2f} x1e-6 s^-1 (time constant {1/L/86400:.2f} d)")
mL, eL, cL = wmean(Ls)
n = len(Ls)
from math import erfc
print(f"single common loss fit: {mL*1e6:.2f} +- {eL*1e6:.2f} x1e-6 s^-1, chi2 {cL:.2f}/{n-1}")
# chi2 survival for dof n-1 via series (even/odd handled numerically)
def chi2_sf(x, k):
    # numerical integration of chi2 pdf tail
    import math
    def pdf(t):
        return t**(k/2-1)*math.exp(-t/2)/(2**(k/2)*math.gamma(k/2))
    N = 200000; hi = x + 200.0; h = (hi - x)/N
    s = 0.5*(pdf(x)+pdf(hi)) + sum(pdf(x+i*h) for i in range(1, N))
    return s*h
print(f"   p-value {chi2_sf(cL, n-1):.2e}")
print(f"range of needed loss: {min(l for l,_ in Ls)*1e6:.2f} to {max(l for l,_ in Ls)*1e6:.2f} x1e-6 s^-1")
mag = [Ls[0], Ls[1]]; mat = Ls[2:]
mm, em, _ = wmean(mag); mt, et, ct = wmean(mat)
print(f"magnetic needs {mm*1e6:.2f} +- {em*1e6:.2f}; material needs {mt*1e6:.2f} +- {et*1e6:.2f} (chi2 {ct:.2f}/{len(mat)-1}) x1e-6 s^-1; ratio {mt/mm:.2f}")
print(f"difference {(mm-mt)*1e6:.2f} x1e-6 s^-1 at {(mm-mt)/math.hypot(em,et):.2f} sigma (unscaled)")

print("\n== 3. In-situ bounds in UCNtau 2025 (Musedinovic, table) vs needed loss ==")
tau = 877.82
Lneed = 1/tau - 1/BL1[0]
for name, dt in [("depolarization unc. +0.07 s", 0.07), ("heating unc. +0.07 s", 0.07), ("residual gas corr. 0.05 s", 0.05), ("total sys +0.20 s", 0.20)]:
    Lb = dt/tau**2
    print(f"{name:30s} -> {Lb*1e8:.2f}e-8 s^-1 ; needed/bound = {Lneed/Lb:.0f}")
print(f"needed shift in UCNtau: {BL1[0]-tau:.2f} s")
