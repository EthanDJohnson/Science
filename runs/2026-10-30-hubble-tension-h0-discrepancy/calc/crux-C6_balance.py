"""Crux C6: where does the narrowed C6 hybrid live, and what precision decides it?

Units: H0 in km/s/Mpc (astronomical, not SI); magnitudes in mag; r_d in Mpc.
Model: true H0 = T. Ladder pole H_L = T + L + n_L (L >= 0 ladder bias).
Early pole H_E = T - E + n_E (E >= 0 early-side shift, i.e. r_d physics).
Optional independent probe of T: N(mu, s_T).
Classification (run's boundary rule): C1 if L > gap/2, C3 if E > gap/2, else C6.
T is integrated analytically (three Gaussian estimates of T), so the posterior
over (L, E) is exp(-chi2_min/2) of the weighted scatter of
a = H_L - L, b = H_E + E, c = mu.
Inputs: H0DN 73.264 +- 0.806 [D-22]; CMB-SPA 67.19 +- 0.38 [D-44];
probe sets as in verdict C6-0 (one-step 71.27 +- 1.93; + r_s-free 70.25 +- 1.21;
+ CCHP, SBF, TF 70.96 +- 0.92).
"""
import math

HL, sL = 73.264, 0.806
HE, sE = 67.19, 0.38
gap = HL - HE
half = gap / 2
sg = math.hypot(sL, sE)
print(f"gap = {gap:.3f} km/s/Mpc, half = {half:.3f}, sigma_gap = {sg:.3f}, midpoint = {HE+half:.3f}")

# 1. Fluctuation needed if E is capped by CMB-only bounds
caps = {
    "Planck NPIPE EDE 95% upper H0 69.5 [D-53]": 69.5 - HE,
    "P-ACT-LB EDE centre 69.9 [D-52]": 69.9 - HE,
    "modified recombination 69.6 [D-52]": 69.6 - HE,
    "PMF 69.1 [D-52]": 69.1 - HE,
    "DESI BAO+BBN offset 68.50 [D-45]": 68.50 - HE,
    "no early shift": 0.0,
}
print("\n1. With L at the C6 ceiling (half gap), fluctuation needed for C6:")
for k, E in caps.items():
    f = max(0.0, gap - half - E)
    z = f / sg
    p = 0.5 * math.erfc(z / math.sqrt(2))
    print(f"  {k}: E = {E:.2f} -> fluctuation {f:.2f} km/s/Mpc = {z:.2f} sigma (one-sided p = {p:.3g})")


def posterior(mu, sT, Emax, Lmax=10.0, step=0.01):
    pc = {"C1": 0.0, "C3": 0.0, "C6": 0.0}
    nL = int(Lmax / step) + 1
    nE = int(Emax / step) + 1
    wL, wE = 1 / sL**2, 1 / sE**2
    wT = 0.0 if sT is None else 1 / sT**2
    for i in range(nL):
        L = i * step
        a = HL - L
        for j in range(nE):
            E = j * step
            b = HE + E
            W = wL + wE + wT
            m = (wL * a + wE * b + (wT * mu if wT else 0.0)) / W
            chi2 = wL * (a - m) ** 2 + wE * (b - m) ** 2 + (wT * (mu - m) ** 2 if wT else 0.0)
            w = math.exp(-0.5 * chi2)
            if L > half and L >= E:
                pc["C1"] += w
            elif E > half:
                pc["C3"] += w
            else:
                pc["C6"] += w
    tot = sum(pc.values())
    return {k: v / tot for k, v in pc.items()}


print("\n2. Posterior class probabilities (flat L in [0,10]; E flat in [0, Emax]):")
probes = [("no independent T probe", 70.0, None),
          ("one-step 71.27+-1.93", 71.27, 1.93),
          ("one-step + r_s-free 70.25+-1.21", 70.25, 1.21),
          ("+CCHP,SBF,TF 70.96+-0.92", 70.96, 0.92)]
for Emax, lab in [(10.0, "E unconstrained (refuter C6-0 prior)"),
                  (69.9 - HE, "E <= 2.71 (P-ACT-LB EDE centre)"),
                  (69.5 - HE, "E <= 2.31 (Planck NPIPE 95% upper)")]:
    print(f" {lab}:")
    for name, mu, sT in probes:
        r = posterior(mu, sT, Emax, step=0.02)
        print(f"   {name}: P(C6)={r['C6']:.3f} P(C1)={r['C1']:.3f} P(C3)={r['C3']:.3f}")

# 3. Precision for deciding tests
print("\n3. Precision needed (combined sigma of the difference):")
def sig_needed(d, n):
    return d / n
# vs C1: early-side shift E. C6 needs E in [~2.3, 3.04]; C1 (pure) E ~ 0.
for n in (3, 5):
    print(f"  E(C6 low end 2.3) vs 0 at {n} sigma: sigma(E) <= {sig_needed(2.3, n):.2f} km/s/Mpc")
# r_d cut equivalents at H0*r_d fixed to CMB-SPA (r_d 147.00 Mpc [D-44])
for T in (69.43, 70.2, 70.6):
    print(f"  T = {T}: r_d = {147.00*HE/T:.1f} Mpc ({100*(1-HE/T):.1f}% cut) at fixed H0*r_d of CMB-SPA")
# vs C3 and C1 via anchor-free T: C6 1-sigma window [69.43, 70.60] (verdicts C6-0, C6-2)
lo, hi = 69.43, 70.60
c = 0.5 * (lo + hi)
for n in (2, 3):
    print(f"  anchor-free T at window centre {c:.2f}: exclude both edges at {n} sigma needs sigma_T <= {(hi-lo)/2/n:.2f}")
print(f"  C1 central 67.75 vs C6 centre {c:.2f} at 5 sigma: sigma_T <= {(c-67.75)/5:.2f}")
print(f"  C3 (EDE detections) 71.0 vs C6 centre {c:.2f} at 3 sigma: sigma_T <= {(71.0-c)/3:.2f}")
# vs C4(ii): M_B step between calibrators and Hubble flow: 0.146-0.188 mag vs C6 <= ladder share
mag = lambda dh, h: 5 * math.log10((h + dh) / h)
c6_step = mag(3.037, HL - 3.037)
print(f"  C6 maximal ladder share in mag: {c6_step:.3f} mag; C4(ii) needs >= 0.146 mag")
print(f"  separating 0.146 from {c6_step:.3f} mag at 3 sigma: sigma <= {(0.146-c6_step)/3:.3f} mag")
# vs C8: team-independent local value; C6 window upper edge 70.60 vs C8 band 70-72
print(f"  C8 non-SH0ES local 71.56 vs C6 upper edge {hi} at 3 sigma: sigma <= {(71.56-hi)/3:.2f}")
