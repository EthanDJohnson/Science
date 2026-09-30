"""Falsifier C6-2 (bounds): independent constraints on the excited-neutron (n*) and
field-dependence variants of C6.  SI units (s, s^-1); energies in keV/MeV (hbar=c=1).

Inputs (from dossier / candidates.md / cited sources):
  BL1 887.7 +- 2.25 s (1.2 stat (+) 1.9 sys); proton-beam mean 887.97 +- 2.04 s
  UCNtau 877.82 +- 0.28 s; storage mean 878.32 +- 0.43 s
  J-PARC 2024 877.2 +4.35/-3.98 s (1.7 stat (+) +4.0/-3.6 sys)
  Blatnik et al. arXiv:2406.10378: no n* with tau_gamma > 139 s (95% CL, equal f).
  Koch-Hummel arXiv:2403.00914: t_beam ~ 2e-2 s << tau_gamma << t_bottle (>300 s).
  Nab arXiv:2508.16045: m_n < 939.565 + 0.021 MeV (90% CL) for tau_gamma >> t_transit.
"""
import math

def z(a, sa, b, sb):
    return (a - b) / math.hypot(sa, sb)

print("=== 1. Required n* population (Koch-Hummel eq. 10) ===")
tau_g = 877.82           # s, ground-state (storage) lifetime
tau_b = 887.7            # s, BL1
dtau = tau_b - tau_g
for dtau_e in [20.0, 50.0, 100.0, 1e3, 1e4, 1e9]:
    # exact: 1/tau_b = (g/tau_g + e/tau_e)/(g+e)  -> r = e/g
    tau_e = tau_g + dtau_e
    r = (1/tau_g - 1/tau_b) / (1/tau_b - 1/tau_e)
    print(f"  dtau_e = {dtau_e:10.3g} s -> n*/n(0) = {r:.4g}  (n* fraction {r/(1+r):.4%})")
print("  beta-stable n* limit: fraction >= dtau/tau_b =", f"{dtau/tau_b:.4%}")

print("\n=== 2. J-PARC electron-counting beam under n* (t_beam << tau_gamma) ===")
# n* hypothesis: every cold beam (tens of ms after production) reads tau_beam, whatever
# decay product is counted, if the n* fraction is production-independent.
pred = 887.7; spred = 2.25
jp = 877.2; jp_up = math.hypot(1.7, 4.0); jp_dn = math.hypot(1.7, 3.6)
print(f"  J-PARC sigma facing prediction (upper side) = {jp_up:.3f} s")
print(f"  z(pred BL1 887.7 vs J-PARC)       = {z(pred, spred, jp, jp_up):.3f} sigma")
print(f"  z(pred beam 887.97 vs J-PARC)     = {z(887.97, 2.04, jp, jp_up):.3f} sigma")
print(f"  z(J-PARC vs UCNtau 877.82)        = {z(jp, jp_up, 877.82, 0.28):.3f} sigma")
# likelihood ratio of J-PARC under tau=878.32 vs tau=887.97 (Gaussian, facing sides)
def lnL(x, mu, sup, sdn):
    s = sup if mu > x else sdn
    return -0.5 * ((x - mu) / s) ** 2
LR = math.exp(lnL(jp, 878.32, jp_up, jp_dn) - lnL(jp, 887.97, jp_up, jp_dn))
print(f"  likelihood ratio J-PARC: storage-value vs beam-value = {LR:.2f} : 1")

print("\n=== 3. Escape via tau_gamma ~ t_beam (J-PARC neutrons older than BL1's) ===")
# For J-PARC to read <= 878+~4 s while BL1 reads 887.7, J-PARC's n* fraction must be
# <= ~0.1-0.4 of BL1's: exp(-(tJ - tB)/tau_gamma) <= x.
for x in [0.1, 0.4]:
    for dt in [0.01, 0.02, 0.05]:
        tg = dt / math.log(1 / x)
        print(f"  suppress to {x:.1f}: dt(J-PARC - BL1) = {dt*1e3:4.0f} ms -> tau_gamma <= {tg*1e3:6.2f} ms")
# consequence: BL1 fraction itself decays over t_BL1 -> production fraction must be amplified
for tB in [0.02, 0.05]:
    for tg in [0.005, 0.01, 0.02]:
        amp = math.exp(tB / tg)
        f0 = 0.0111 * amp
        print(f"  t_BL1 = {tB*1e3:3.0f} ms, tau_gamma = {tg*1e3:4.0f} ms -> needed n* fraction at production "
              f"(beta-stable n*) = {f0:.3g} {'(>1: impossible)' if f0 > 1 else ''}")
# velocity dependence inside BL1: v spans ~factor 2 around the mean -> t spans factor 2
tg = 0.01; tB = 0.03
print(f"  within BL1 (tau_gamma=10 ms, mean t=30 ms): n* ratio slow(t=45ms)/fast(t=15ms) = "
      f"{math.exp(-(0.045-0.015)/tg):.3g} -> strongly velocity-dependent shift")

print("\n=== 4. Field variant (SM Zeeman) ===")
mu_n = 6.0308e-8 * 1e-6   # MeV/T (|mu_n| = 60.3 neV/T)
Q = 0.782                  # MeV
for B in [4.6, 5.0]:
    x = mu_n * B / Q
    print(f"  B = {B} T: |mu_n|B/Q = {x:.3e}; 5x/needed(1.14e-2) shortfall = {1.14e-2/(5*x):.3g}")

print("\n=== 5. Remaining n* window (equal-fraction assumption) ===")
print("  lower edge: tau_gamma >> t_beam ~ 2e-2 s (K-H hierarchy; else BL1 is velocity-dependent)")
print("  upper edge: tau_gamma <= 139 s (UCNtau reanalysis, 95% CL)")
print(f"  window spans {math.log10(139/0.02):.2f} decades, all of which predict J-PARC ~ 888 s")
