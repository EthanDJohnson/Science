"""Falsifier C5-2 (bounds): independent constraints a local-void / bulk-flow explanation must satisfy.
Units: H0 in km/s/Mpc; distances in Mpc; velocities km/s; magnitudes mag; delta, f dimensionless.
Sections:
 A. SN Hubble-diagram void bound (Kenworthy+2019: |delta|>0.20 excluded at 4-5 sigma; delta<0.27 at 5 sigma)
    translated into a ceiling on the local H0 excess, vs the gap and the 'dominant' threshold.
 B. CF4 Tully-Fisher field-level void fits (Stiskalek, Desmond, Banik 2025): fraction of the gap carried.
 C. Coherent bulk flow (dipole) -> monopole leak into H0 for an SN-like sample.
 D. Toy SN Hubble-diagram fit: a 9.04% local excess with an edge at z_e, fitted by flat LCDM (M, Om free)
    and by flat wCDM (M, Om, w free); chi^2 penalty with Pantheon+-like counts (assumed, stated).
"""
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize

H_loc, H_glob = 73.264, 67.19          # H0DN-corrected (D-22) and CMB-SPA (D-44), km/s/Mpc
eps_gap = H_loc / H_glob - 1
mid = 0.5 * (H_loc + H_glob)
eps_dom = H_loc / mid - 1              # local excess needed to move true global below midpoint
print(f"A0 gap excess eps_gap = {eps_gap*100:.2f}%  midpoint {mid:.3f}; 'dominant' needs eps > {eps_dom*100:.2f}%")

def lin(d, f):  return -f * d / 3.0
def bern(d, f): return (f / 2.0) * (1 - (1 + d) ** (2.0 / 3.0))

for Om in (0.30, 0.315):
    f = Om ** 0.55
    for d in (-0.20, -0.27):
        print(f"A1 Om={Om} f={f:.3f} delta={d}: dH/H lin {lin(d,f)*100:.2f}%  Bern {bern(d,f)*100:.2f}%"
              f"  -> fraction of gap (Bern) {bern(d,f)/eps_gap:.2f}; vs dominant threshold {bern(d,f)/eps_dom:.2f}")
    # delta needed for 'dominant' and for full gap (Bernardeau, solve)
    from scipy.optimize import brentq
    d_dom = brentq(lambda d: bern(d, f) - eps_dom, -0.99, -1e-6)
    d_full = brentq(lambda d: bern(d, f) - eps_gap, -0.99, -1e-6)
    print(f"A2 Om={Om}: delta for >half (dominant) = {d_dom:.3f}; delta for full gap = {d_full:.3f} (Bernardeau)")

# B. Stiskalek+2025 predicted local H0 for void models fitted to CF4 TF, Planck background (assumed 67.4)
Hbg = 67.4
for name, h in (("exponential (disfavoured by evidence)", 72.1), ("Gaussian", 70.4), ("Maxwell-Boltzmann", 70.2)):
    frac = (h - Hbg) / (H_loc - Hbg)
    print(f"B {name}: local {h} -> void carries {h-Hbg:.2f} of {H_loc-Hbg:.2f} km/s/Mpc = {frac*100:.0f}% of gap")

# C. Dipole bulk flow leak. Sample uniform in comoving volume 0.023<z<0.15 (cz in km/s), equal weights in mu.
c = 299792.458
z = np.linspace(0.023, 0.15, 20001); w = z**2; w /= w.sum()
inv_cz = np.sum(w / (c * z))
for v in (400.0, 1000.0):
    for cos_mean, lab in ((0.0, "isotropic sky"), (0.25, "strongly lopsided sky"), (0.5, "one hemisphere only"), (1.0, "all SNe along flow")):
        print(f"C v={v:.0f} km/s, <cos>={cos_mean} ({lab}): dH/H = {v*cos_mean*inv_cz*100:.2f}%  (gap {eps_gap*100:.2f}%)")
v_need = eps_gap / inv_cz
print(f"C bulk speed needed with all SNe along the flow: {v_need:.0f} km/s; with one hemisphere: {2*v_need:.0f} km/s")
print(f"C monopole outflow speed at R=100,300,430 h^-1 Mpc for eps_gap: {[round(eps_gap*100*R) for R in (100,300,430)]} km/s")

# D. Toy Hubble diagram
def Dc(zz, Om, w=-1.0):
    return quad(lambda x: 1.0 / np.sqrt(Om*(1+x)**3 + (1-Om)*(1+x)**(3*(1+w))), 0, zz)[0]
zgrid = np.concatenate([np.linspace(0.023, 0.15, 25), np.linspace(0.16, 0.4, 25), np.linspace(0.42, 0.8, 20), np.linspace(0.85, 2.2, 15)])
Nper = np.concatenate([np.full(25, 500/25), np.full(25, 450/25), np.full(20, 400/20), np.full(15, 150/15)])  # assumed counts
sig_sn = 0.14  # mag per SN (assumed, Pantheon+-like total scatter)
Om0 = 0.315
Dg = np.array([Dc(zz, Om0) for zz in zgrid])

def mu_void(ze, smooth):
    Dge = Dc(ze, Om0)
    if smooth:  # gradual: local excess decays as exp(-(z/ze)^2)... in effective H, D = Dg/(1+eps*g)
        g = np.exp(-(zgrid / ze) ** 2)
        D = Dg / (1 + eps_gap * g)
    else:       # sharp edge: D = Dg/(1+eps) inside; constant absolute deficit outside
        D = np.where(zgrid < ze, Dg / (1 + eps_gap), Dg - Dge * eps_gap / (1 + eps_gap))
    return 5 * np.log10((1 + zgrid) * D)

def fit(mu_data, sig_eff, model_w):
    def chi2(p):
        Om, M = p[0], p[1]; w = p[2] if model_w else -1.0
        if not (0.05 < Om < 0.7) or not (-2.5 < w < -0.3): return 1e9
        mu_m = 5 * np.log10((1 + zgrid) * np.array([Dc(zz, Om, w) for zz in zgrid])) + M
        return np.sum(Nper * (mu_data - mu_m) ** 2) / sig_eff ** 2
    p0 = [0.3, 0.0, -1.0] if model_w else [0.3, 0.0]
    r = minimize(chi2, p0, method="Nelder-Mead", options={"xatol": 1e-5, "fatol": 1e-4, "maxiter": 4000})
    return r.fun, r.x

for smooth in (False, True):
    for ze in (0.15, 0.2, 0.3):
        mu_d = mu_void(ze, smooth)
        for sig_eff in (sig_sn, 0.20):
            c2, p = fit(mu_d, sig_eff, False)
            c2w, pw = fit(mu_d, sig_eff, True)
            print(f"D {'smooth' if smooth else 'sharp'} z_e={ze} sigma_SN={sig_eff}: LCDM dchi2={c2:.1f} (Om={p[0]:.3f})"
                  f" | wCDM dchi2={c2w:.1f} (Om={pw[0]:.3f}, w={pw[2]:.2f}) [N_SN={Nper.sum():.0f}]")
print("D check: zero-void data refit gives", f"{fit(5*np.log10((1+zgrid)*Dg), sig_sn, False)[0]:.2e}")
