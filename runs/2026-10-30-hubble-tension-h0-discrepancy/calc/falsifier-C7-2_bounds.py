"""Falsifier C7-2 (bounds): test the 'two calibrations, not expansion rates' reframe
against independent constraints.  Units: H0 in km/s/Mpc, magnitudes in mag,
N_eff dimensionless.  All inputs are dossier values (IDs in comments)."""
import math

def wmean(vals):
    w = [1/s**2 for _, s in vals]
    m = sum(wi*v for wi, (v, _) in zip(w, vals))/sum(w)
    s = 1/math.sqrt(sum(w))
    chi2 = sum(wi*(v-m)**2 for wi, (v, _) in zip(w, vals))
    return m, s, chi2, len(vals)-1

def pchi2(x, k):
    # survival function of chi2 with k dof (series for integer k via regularized gamma)
    from math import exp, lgamma
    a = k/2.0; xx = x/2.0
    # lower incomplete gamma by series
    term = 1.0/a; s = term; n = 1
    while n < 500:
        term *= xx/(a+n); s += term; n += 1
    P = s*math.exp(-xx + a*math.log(xx) - lgamma(a))
    return 1-P

def z(a, sa, b, sb):
    return (a-b)/math.sqrt(sa**2+sb**2)

print("=== 1. Internal consistency of the two calibrator groups (C7's own prediction) ===")
rd = [(67.19, 0.38), (68.50, 0.58)]           # CMB-SPA [D-44], DESI BAO+BBN [D-45]
m, s, c, k = wmean(rd)
print(f"r_d group (CMB-SPA, BAO+BBN, independent): {m:.2f} +- {s:.2f}, chi2={c:.2f}/{k}, p={pchi2(c,k):.3f}, z={z(68.50,0.58,67.19,0.38):.2f}")
anc = [(73.49, 0.93), (70.39, 1.94), (73.8, math.hypot(0.7, 2.3)), (73.3, 4.1)]  # SH0ES, CCHP, SBF, TF [D-20,D-24,D-29,D-30]
m, s, c, k = wmean(anc)
print(f"anchor group (SH0ES, CCHP total, SBF, TF): {m:.2f} +- {s:.2f}, chi2={c:.2f}/{k}, p={pchi2(c,k):.3f}")
jagb = (67.80, math.hypot(2.17, 1.64))         # CCHP JWST JAGB [D-26]
print(f"CCHP JWST JAGB {jagb[0]} +- {jagb[1]:.2f} vs SH0ES: z = {z(73.49,0.93,*jagb):.2f}; vs r_d group 67.51+-0.29: z = {z(jagb[0],jagb[1],67.51,0.29):.2f}")
print(f"CCHP total 70.39+-1.94 vs SH0ES: z = {z(73.49,0.93,70.39,1.94):.2f}")

print("\n=== 2. Does late-time H(z) freedom move the r_d-side H0? (DESI DR2, D-45, D-51) ===")
ref = (68.17, 0.28)   # DESI+CMB LCDM [D-45]
H0DN = (73.264, 0.806)  # [D-22]
gap_ref = H0DN[0]-ref[0]; sg_ref = math.hypot(H0DN[1], ref[1])
print(f"LCDM DESI+CMB gap to H0DN: {gap_ref:.2f} +- {sg_ref:.2f} ({gap_ref/sg_ref:.2f} sigma)")
cases = {"w0wa DESI+CMB (no SN)": (63.6, 1.85), "w0wa +Pantheon+": (67.51, 0.59),
         "w0wa +Union3": (65.91, 0.84), "w0wa +DESY5": (66.74, 0.56),
         "wCDM DESI+CMB (no SN)": (69.51, 0.92), "wCDM +Pantheon+": (67.97, 0.57),
         "wCDM +Union3": (68.01, 0.68), "wCDM +DESY5": (67.34, 0.54)}
for name, (h, sh) in cases.items():
    g = H0DN[0]-h; sg = math.hypot(H0DN[1], sh)
    dH = h-ref[0]
    print(f"{name:24s} H0={h:6.2f}  dH0 vs LCDM={dH:+5.2f}  gap={g:5.2f}+-{sg:4.2f} ({g/sg:4.2f} sig)  "
          f"gap change = {dH/sg_ref:+5.2f} x sigma_gap(LCDM)  frac of gap {abs(dH)/gap_ref:.2f}")
print("Only fits WITHOUT SNe move H0 up; every fit with SNe moves the r_d-side H0 DOWN (gap widens).")

print("\n=== 3. M_B closure: is the H0 gap fully an M_B gap? (D-21, D-48, D-85) ===")
for hinv, dMB in [(67.19, 0.122), (67.67, 0.141)]:
    need = 5*math.log10(73.04/hinv)
    print(f"R22 73.04 vs inverse ladder {hinv}: gap in mag {need:.3f}; quoted dM_B {dMB:.3f}; residual {need-dMB:+.3f} mag")
print("D-85: DES5Y vs Pantheon+ common-SN offset ~0.04 mag -> residual is of the size of a SN-system mismatch")

print("\n=== 4. Is the 'r_d-free' arbiter calibration-free? Equality-scale H0 under Delta N_eff ===")
# k_eq [h/Mpc] ~ Omega_m h / sqrt(omega_r), omega_r ∝ 1+0.2271 N_eff; at fixed measured k_eq/h and Omega_m: h ∝ sqrt(1+0.2271 N_eff)
base = 1+0.2271*3.044
for target, frm in [(73.264, 67.19), (73.264, 68.50)]:
    r = (target/frm)**2
    N = (r*base-1)/0.2271
    print(f"equality-scale H0 {frm}->{target}: needs N_eff = {N:.2f} (dN = {N-3.044:.2f}); ACT DR6 2.86+-0.13 -> {(N-2.86)/0.13:.1f} sigma")
print("Under Delta N_eff the equality route moves WITH r_d (both early calibrations shift), so it is not a clean arbiter for that variant; N_eff bound closes it.")

print("\n=== 5. Arbiters: anchor-free, r_d-free values vs the two calibrator groups (67.51+-0.29 r_d; 73.02+-0.78 anchors; M-EXAMINER-06) ===")
arb = {"one-step mean (TD, masers, sirens) M-DIAL-07": (71.27, 1.93),
       "TDCOSMO-2026 [D-31]": (71.1, 2.35),
       "Zaborowski r_d-free mean-ish 69.6 [D-49]": (69.6, 1.55),
       "2411.16677 r_d-free DESY5 [D-49]": (66.7, 1.8),
       "equality BOSS [D-50]": (65.1, 4.2)}
for n, (h, sh) in arb.items():
    f = (h-67.51)/(73.02-67.51)
    print(f"{n:45s} z(vs r_d grp)={z(h,sh,67.51,0.29):+5.2f}  z(vs anchor grp)={z(h,sh,73.02,0.78):+5.2f}  position frac={f:.2f}")

print("\n=== 6. Age bound (D-55): calibration-free clock ===")
for h in (67.19, 73.264):
    t = 13.857*68/h
    print(f"LCDM t0 at H0={h}: {t:.2f} Gyr; GC 13.81+-0.34 -> z={(t-13.81)/math.hypot(0.25,0.23):+.2f}")
