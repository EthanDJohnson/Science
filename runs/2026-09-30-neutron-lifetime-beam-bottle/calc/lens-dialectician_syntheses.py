"""Dialectician lens: numbers behind the three syntheses.
Units: lifetimes in s (SI), rates in s^-1, energies in MeV (natural units for the spectrum integral),
lambda, b, fractions dimensionless.
Inputs: dossier D-20, D-23, D-24, D-25, D-27, D-28, D-40, D-42, D-43, U-01; Beck 2024 (b(c), lambda(c));
Caylor 2025 (0.3% loss at 1e-7 Pa).
"""
import math, sys
import numpy as np
from scipy import integrate

sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/tools")
import neutron_beta_decay as nbd

def sym(lo, hi):
    return 0.5 * (abs(lo) + abs(hi))

def tension(x1, s1, x2, s2):
    return (x1 - x2) / math.hypot(s1, s2)

print("=== Reference values ===")
BL1, sBL1 = 887.7, math.hypot(1.2, 1.9)            # D-20
UCNT, sUCNT = 877.82, math.hypot(0.22, sym(0.20, 0.17))  # D-27
GRAV, sGRAV = 881.5, math.hypot(0.7, 0.6)          # D-28
JP, sJP_up, sJP_dn = 877.2, math.hypot(1.7, 4.0), math.hypot(1.7, 3.6)  # D-23
print(f"BL1 {BL1} +- {sBL1:.2f} s; UCNtau {UCNT} +- {sUCNT:.2f} s; Gravitrap {GRAV} +- {sGRAV:.2f} s")
print(f"J-PARC {JP} +{sJP_up:.2f}/-{sJP_dn:.2f} s (stat+sys quadrature)")

print("\n=== Synthesis I: J-PARC internal scatter ===")
# D-24: value, stat, sysA(lo,hi), sysB(lo,hi) ; we combine stat only for the chi2 of configs (as the paper's chi2 15.8/3)
cfg = {
    "100kPa/oldSFC": (870.9, 3.5),
    "100kPa/newSFC": (868.3, 4.0),
    "50kPa/oldSFC":  (868.2, 7.7),
    "50kPa/newSFC":  (884.8, 2.4),
}
x = np.array([v[0] for v in cfg.values()]); s = np.array([v[1] for v in cfg.values()])
w = 1 / s**2
m = np.sum(w * x) / np.sum(w); sm = 1 / math.sqrt(np.sum(w))
chi2 = float(np.sum(w * (x - m)**2)); S = math.sqrt(chi2 / 3)
print(f"stat-weighted mean of 4 configs = {m:.2f} +- {sm:.2f} s (stat); chi2 = {chi2:.1f}/3; PDG S = {S:.2f}")
print("(paper quotes chi2/DOF = 15.8/3 and combined 877.2 +- 1.7 stat: our stat-only reconstruction differs because the paper's weights include per-condition systematics)")
# inflate paper's stat by paper's S = sqrt(15.8/3)
S_paper = math.sqrt(15.8 / 3)
st_inf = 1.7 * S_paper
up_inf, dn_inf = math.hypot(st_inf, 4.0), math.hypot(st_inf, 3.6)
print(f"paper S = {S_paper:.2f}; inflated stat = {st_inf:.2f} s; total +{up_inf:.2f}/-{dn_inf:.2f} s")
for lab, (up, dn) in {"quoted": (sJP_up, sJP_dn), "S-inflated": (up_inf, dn_inf)}.items():
    t_beam = (BL1 - JP) / math.hypot(sBL1, up)    # BL1 above JP: use JP upper error
    t_bot = (JP - UCNT) / math.hypot(sUCNT, dn)   # JP below UCNtau: use JP lower error
    print(f"  [{lab}] J-PARC vs BL1: {t_beam:.2f} sigma ; J-PARC vs UCNtau: {t_bot:.2f} sigma")
# How far from the beam value is each configuration?
for k, (v, e) in cfg.items():
    print(f"  config {k}: {v} s; (BL1 - v)/stat = {(BL1 - v)/math.hypot(e, sBL1):.2f} sigma incl. BL1 error")
# 2x2 decomposition (stat weights): pressure effect within each SFC
dP_old = cfg["50kPa/oldSFC"][0] - cfg["100kPa/oldSFC"][0]
dP_new = cfg["50kPa/newSFC"][0] - cfg["100kPa/newSFC"][0]
s_old = math.hypot(7.7, 3.5); s_new = math.hypot(2.4, 4.0)
print(f"pressure effect tau(50)-tau(100): old SFC {dP_old:+.1f} +- {s_old:.1f} s; new SFC {dP_new:+.1f} +- {s_new:.1f} s")
print(f"  interaction (new - old) = {dP_new - dP_old:+.1f} +- {math.hypot(s_old, s_new):.1f} s ({(dP_new-dP_old)/math.hypot(s_old,s_new):.2f} sigma)")
# linear background model: if tau bias proportional to pressure p: tau(p) = tau0 + k p ; fit to all four (stat weights)
p = np.array([100, 100, 50, 50.])
A = np.vstack([np.ones(4), p]).T
Wm = np.diag(w)
cov = np.linalg.inv(A.T @ Wm @ A)
beta = cov @ A.T @ Wm @ x
chi2_lin = float(np.sum(w * (x - A @ beta)**2))
print(f"linear-in-pressure fit: tau(p=0) = {beta[0]:.1f} +- {math.sqrt(cov[0,0]):.1f} s, slope = {beta[1]:.3f} +- {math.sqrt(cov[1,1]):.3f} s/kPa, chi2 = {chi2_lin:.1f}/2")
# needed precision for LiNA to separate BL1-like 887.7 from 877.8 at 5 sigma
gap = BL1 - UCNT
print(f"gap BL1-UCNtau = {gap:.2f} s; LiNA sigma for 5 sigma separation (ignoring BL1 error) = {gap/5:.2f} s; for 3 sigma = {gap/3:.2f} s")

print("\n=== Synthesis II: A-route vs a-route lambda, and the Fierz reconciliation ===")
# <m_e/E_e> over the neutron beta spectrum (Z=1 Fermi function, relativistic approx via toolkit if available)
me = 0.51099895; Q = 1.29333236 - me  # kinetic endpoint approx (neglect recoil): E0 total = Delta
E0 = 1.29333236  # total electron endpoint energy ~ mn-mp (recoil neglected, <1e-3 effect)
def spec(E, fermi=True):
    pe = math.sqrt(max(E*E - me*me, 0.0))
    F = 1.0
    if fermi and pe > 0:
        eta = 1/137.036 * E / pe
        F = 2*math.pi*eta / (1 - math.exp(-2*math.pi*eta))
    return pe * E * (E0 - E)**2 * F
for fermi in (False, True):
    N = integrate.quad(lambda E: spec(E, fermi), me, E0, limit=200)[0]
    M = integrate.quad(lambda E: spec(E, fermi) * me / E, me, E0, limit=200)[0]
    print(f"<m_e/E_e> (Fermi function {'on' if fermi else 'off'}) = {M/N:.4f}")
mE = M / N

res0 = nbd.tau_beta(1.27641, 0.00056, 0.97361, 0.00032, rc_set="GS2023")
res = {k: res0[k] for k in ("tau", "sigma")}
print("toolkit tau_beta(PERKEO III, GS2023 Vud 0.97361) ->", res)
def tau_of(lam, b, base_tau=None):
    r = nbd.tau_beta(lam, 0.0, 0.97361, 0.0, rc_set="GS2023")
    t = r["tau"]
    return t / (1 + b * mE)
t_P3 = tau_of(1.27641, 0.0)
t_aS = tau_of(1.2668, 0.0)
t_c = tau_of(1.2724, -0.0181)
print(f"tau_beta SM (b=0): PERKEO III lambda {t_P3:.2f} s; aSPECT 2024 lambda {t_aS:.2f} s")
print(f"tau_beta with Fierz synthesis lambda(c)=1.2724, b(c)=-0.0181: {t_c:.2f} s")
# uncertainty by Monte Carlo on (lambda, b); aSPECT gives correlated fit but the combined correlation is not quoted:
rng = np.random.default_rng(1)
for rho in (-0.8, 0.0, 0.8):
    cv = np.array([[0.0013**2, rho*0.0013*0.0065], [rho*0.0013*0.0065, 0.0065**2]])
    smp = rng.multivariate_normal([1.2724, -0.0181], cv, 20000)
    lam_s = smp[:, 0]; b_s = smp[:, 1]
    t0 = tau_of(1.2724, 0.0)
    # scale by (1+3l^2) analytically for speed
    ts = t0 * (1 + 3*1.2724**2) / (1 + 3*lam_s**2) / (1 + b_s*mE)
    ts = ts * math.sqrt(1)  # Vud error added in quadrature below
    sd = math.hypot(np.std(ts), 0.6)
    print(f"  rho(lambda,b)={rho:+.1f}: tau = {np.mean(ts):.1f} +- {sd:.1f} s (incl. Vud 0.6 s); vs UCNtau {(np.mean(ts)-UCNT)/math.hypot(sd,sUCNT):.2f} sigma; vs BL1 {(np.mean(ts)-BL1)/math.hypot(sd,sBL1):.2f} sigma; vs J-PARC {(np.mean(ts)-JP)/math.hypot(sd,sJP_up):.2f} sigma")
# b needed (with PERKEO-III lambda fixed) to make SM tau equal to bottle or beam
for lab, T in {"UCNtau": UCNT, "BL1": BL1}.items():
    bneed = (t_P3 / T - 1) / mE
    print(f"b needed with PERKEO III lambda to give tau = {T} s ({lab}): {bneed:+.4f}")
# the a-coefficient discrepancy size
def a_of(l): return (1 - l*l) / (1 + 3*l*l)
def A_of(l): return -2*(l*l - l) / (1 + 3*l*l)  # lambda<0 convention: A = -2(l^2 + |l|)/(1+3l^2)
print(f"a predicted from PERKEO III lambda = {a_of(1.27641):.5f}; aSPECT measured -0.10402(82): diff = {(-0.10402 - a_of(1.27641)):.5f} = {(-0.10402 - a_of(1.27641))/0.00082:.2f} sigma_aSPECT; fractional |a| deficit = {1 - 0.10402/abs(a_of(1.27641)):.4f}")

print("\n=== Synthesis III: charge exchange in the proton trap ===")
need = 1 - 1/ (BL1/UCNT)   # fraction of protons lost that would lengthen tau from UCNtau to BL1
print(f"proton-loss fraction needed to take true {UCNT} s to {BL1} s: {need*100:.3f} %")
P_caylor = 0.003
print(f"Caylor 0.3% loss at 1e-7 Pa, 10 ms: lifetime shift if every exchanged proton were lost undetected = {P_caylor*UCNT/(1-P_caylor):.2f} s")
print(f"H2 partial pressure needed (linear in n) for {need*100:.2f}% loss, ions undetected: {1e-7*need/P_caylor:.2e} Pa")
print("Caylor worst case for BL1 (H2+ detected as charge): shift < 0.5 s => net missing fraction <", f"{0.5/BL1*100:.3f} %")
print(f"Fraction of the gap covered by <0.5 s: < {0.5/gap*100:.1f} %; by full 0.3% undetected loss: {P_caylor*UCNT/(1-P_caylor)/gap*100:.0f} %")

print("\n=== Synthesis IV: bottle-side loss and the J-PARC coincidence ===")
for lab, T in {"UCNtau": UCNT, "Gravitrap": GRAV}.items():
    print(f"missing loss rate if BL1 true, {lab}: {1/T - 1/BL1:.3e} s^-1 (time constant {1/(1/T-1/BL1):.3e} s)")
print(f"Gravitrap - UCNtau = {GRAV-UCNT:.2f} s, {tension(GRAV, sGRAV, UCNT, sUCNT):.2f} sigma")
print(f"J-PARC shift needed if BL1 true: {BL1-JP:+.1f} s = {(BL1-JP)/sJP_up:.2f} x its quoted upper total error")

print("\n=== Null: error inflation of the size seen inside the field ===")
for Sx in (1.0, 1.5, 2.0, 2.3):
    print(f"BL1 error x{Sx}: BL1 vs UCNtau = {(BL1-UCNT)/math.hypot(Sx*sBL1, sUCNT):.2f} sigma")
print(f"J-PARC zero-pressure extrapolation 896.9 +- 5.3 s vs UCNtau: {(896.9-UCNT)/math.hypot(5.3,sUCNT):.2f} sigma; vs BL1: {(896.9-BL1)/math.hypot(5.3,sBL1):.2f} sigma (stat-only, exploratory)")
