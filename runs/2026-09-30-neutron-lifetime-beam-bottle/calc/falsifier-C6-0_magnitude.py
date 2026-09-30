"""Falsifier C6-0 (magnitude): excited-neutron (n*) and field-dependence variants.
Units: SI (s, m, m/s, J, eV where stated).

1. Required n* fraction in a beam (exact, from tau = -n/ndot, Koch-Hummel Eq. 6).
2. Time since production of decaying neutrons: NIST BL1 (68 m, 40 K pseudo-Maxwellian)
   vs J-PARC BL05 (TPC ~20 m from source, lambda 2-8 Angstrom).
3. J-PARC lifetime predicted by n* given the BL1 shift, as a function of tau_gamma.
4. Storage-side bias as a function of tau_gamma (UCNtau-like load 150 s, holds 20 s / 1020 s).
5. Field variant: Zeeman energy / Q.
"""
import numpy as np

h = 6.62607015e-34; m_n = 1.67492750e-27; kB = 1.380649e-23
eV = 1.602176634e-19

tau_g = 877.82       # s, magnetic-trap average (candidates.md prediction matrix)
tau_beam = 887.7     # s, BL1
dtau = tau_beam - tau_g
print("== 1. Required n* fraction ==")
print(f"tau_g = {tau_g} s, tau_beam(BL1) = {tau_beam} s, dtau = {dtau:.2f} s")
for ratio in [25/9, 25.0, 1e6]:
    tau_e = ratio * tau_g
    dte = tau_e - tau_g
    x_exact = (tau_e / tau_g) * dtau / (dte - dtau)       # n_e/n_g exact
    f_exact = x_exact / (1 + x_exact)
    x_kh = dtau / (dte - dtau)                              # Koch-Hummel Eq. (10) leading order
    # direct check: tau = n / (n_e/tau_e + n_g/tau_g)
    tau_check = 1.0 / (f_exact / tau_e + (1 - f_exact) / tau_g)
    print(f"tau_e/tau_g = {ratio:.4g}: exact n_e/n = {f_exact:.4e} (check tau = {tau_check:.3f} s);"
          f" KH Eq.10 n_e/n_g = {x_kh:.4e}; exact/KH = {x_exact/x_kh:.3f}")
print(f"Model-independent minimum (tau_e -> inf): n_e/n = dtau/tau_beam = {dtau/tau_beam:.4e}")
# KH quoted 5.5e-3 for tau_e = 25/9 tau_g
print("KH quoted n_e/n_n = 5.5e-3 for Gamma_e = 9/25 Gamma_g")

print("\n== 2. Time since production of decaying neutrons ==")
# NIST BL1: pseudo-Maxwellian, T_eff = 40 K; flux phi(v) ~ v^3 exp(-v^2/vT^2); density ~ phi/v
vT = np.sqrt(2 * kB * 40.0 / m_n)
v = np.linspace(1.0, 8000.0, 400001)
dens = v**2 * np.exp(-(v / vT)**2)
dens /= np.trapezoid(dens, v)
L_nist = 68.0
t_nist = L_nist / v
mean_t = np.trapezoid(dens * t_nist, v)
cdf = np.cumsum(dens) * (v[1] - v[0])
v10 = v[np.searchsorted(cdf, 0.10)]; v50 = v[np.searchsorted(cdf, 0.5)]; v90 = v[np.searchsorted(cdf, 0.90)]
print(f"NIST: vT = {vT:.1f} m/s, L = {L_nist} m; density-weighted <t> = {mean_t*1e3:.1f} ms;"
      f" median t = {L_nist/v50*1e3:.1f} ms; 10-90% t range = {L_nist/v90*1e3:.1f}-{L_nist/v10*1e3:.1f} ms")
L_jp = 20.0
lam = np.array([2e-10, 5e-10, 8e-10])
v_jp = h / (m_n * lam)
t_jp = L_jp / v_jp
for l, vv, tt in zip(lam, v_jp, t_jp):
    print(f"J-PARC: lambda = {l*1e10:.0f} A, v = {vv:.0f} m/s, t = {tt*1e3:.1f} ms (L = {L_jp} m)")

print("\n== 3. J-PARC prediction given the BL1 shift, equal birth fraction f0 ==")
tau_JP, sig_JP_up = 877.2, 4.35     # s, J-PARC 2024 (preprint), upper total error
sig_BL1 = 2.25
lam_grid = np.linspace(2e-10, 8e-10, 601)
t_grid = L_jp * m_n * lam_grid / h   # uniform-in-lambda weighting (spectrum shape not modelled)
for ratio in [25/9, 1e6]:
    tau_e = ratio * tau_g
    # n* fraction needed at BL1 (density-weighted average survival)
    f_bl1 = (1/tau_g - 1/tau_beam) / (1/tau_g - 1/tau_e)
    for tg in [0.03, 0.1, 0.3, 1.0, 10.0]:
        S_nist = np.trapezoid(dens * np.exp(-t_nist / tg), v)
        S_jp = np.mean(np.exp(-t_grid / tg))
        f0 = f_bl1 / S_nist
        if f0 > 1:
            print(f"tau_e/tau_g={ratio:.3g} tau_gamma={tg:5.2f} s: f0 = {f0:.2f} > 1, impossible")
            continue
        f_jp = min(f0 * S_jp, 1.0)
        tau_jp_pred = 1.0 / (f_jp / tau_e + (1 - f_jp) / tau_g)
        z1 = (tau_jp_pred - tau_JP) / sig_JP_up
        z2 = (tau_jp_pred - tau_JP) / np.hypot(sig_JP_up, sig_BL1)
        print(f"tau_e/tau_g={ratio:.3g} tau_gamma={tg:5.2f} s: f0={f0:.4f}, f(BL1)={f_bl1:.4f},"
              f" f(J-PARC)={f_jp:.4f}, J-PARC predicted {tau_jp_pred:.1f} s vs 877.2:"
              f" {z1:.2f} sigma (J-PARC err), {z2:.2f} sigma (with BL1 err)")

S = np.sqrt(15.8 / 3)   # J-PARC internal chi2/DOF = 15.8/3 (D-24), PDG-style scale factor
print(f"Scale factor sqrt(15.8/3) = {S:.3f}; floor prediction 887.8 s vs 877.2 s with inflated error "
      f"{sig_JP_up*S:.2f} s: {(887.8-877.2)/(sig_JP_up*S):.2f} sigma;"
      f" with BL1 err too: {(887.8-877.2)/np.hypot(sig_JP_up*S, sig_BL1):.2f} sigma")

print("\n== 4. Storage-side bias vs tau_gamma (UCNtau-like) ==")
# n* fraction at start of holding: f0 * exp(-t_load/tau_gamma); two-point lifetime from t1=20 s, t2=1020 s
tau_e = 25/9 * tau_g
f0 = 0.0178 / 1.0   # birth fraction if tau_gamma >> 0.1 s (from section 3)
for tl in [150.0, 300.0]:
    for tg in [5.0, 10.0, 20.0, 30.0, 50.0, 100.0]:
        fs = f0 * np.exp(-tl / tg)
        t1, t2 = 20.0, 1020.0
        # integral of n_e fraction (deficit rate) between t1 and t2
        I = fs * tg * (np.exp(-t1 / tg) - np.exp(-t2 / tg))
        dG = -(1/tau_g - 1/tau_e) * I / (t2 - t1)      # apparent change of decay rate
        dtau_bottle = -tau_g**2 * dG
        print(f"t_load={tl:.0f} s tau_gamma={tg:5.1f} s: n* at hold start {fs:.2e}, bottle bias +{dtau_bottle:.3f} s")

print("\n== 5. Field variant ==")
mu_n = 9.6623651e-27  # J/T
Q = 0.782333e6 * eV
for B in [4.6, 5.0]:
    r = mu_n * B / Q
    print(f"B = {B} T: |mu_n|B = {mu_n*B/eV*1e9:.1f} neV, ratio to Q = {r:.3e};"
          f" needed 1.13e-2 -> shortfall {1.13e-2/r:.2e} (x/5 with Gamma~Q^5: {1.13e-2/(5*r):.2e})")
