"""Falsifier C6-0: checks on the Gambini-Porto-Pullin (GPP 2004, hep-th/0406260) decoherence.

Units: SI unless stated. GPP work in hbar = c = 1; we restore SI.
Parts:
 A. Coefficient of the two-level exponent: GPP Eq.(6) (3/2) vs what Eq.(1)+Eq.(2) give.
 B. Clock-choice (Tmax) dependence of the decoherence accrued by a fixed elapsed time.
 C. Where the T^(1/3) comes from: free-mass (Salecker-Wigner) spreading premise vs
    a clock-agnostic energy-time + no-black-hole premise (gives dT >= t_P, T-independent),
    and what GPP's own Eq.(2) then gives (sigma = d(dT^2)/dT = 0).
 D. Black-hole claim: GPP Eq.(4)-(5); coherence left one Planck time before evaporation.
"""
import sympy as sp
import math

hbar = 1.054571817e-34   # J s
G = 6.67430e-11          # m^3 kg^-1 s^-2
c = 2.99792458e8         # m/s
tP = math.sqrt(hbar*G/c**5)  # s
w = 2*math.pi*429e12     # rad/s, Sr clock transition
print(f"t_P = {tP:.4e} s ; omega = {w:.4e} rad/s")

# ---------------- A. coefficient ----------------
t, T, Tm, Tp, W = sp.symbols('t T T_max t_P omega', positive=True)
dT2 = Tp**sp.Rational(4, 3)*T**sp.Rational(2, 3)          # (dT)^2 from GPP Eq.(1)
sigma_def = sp.diff(dT2, T)                                  # GPP: sigma = d(dT^2)/dT
expo_def = W**2*sp.integrate(sigma_def.subs(T, t), (t, 0, T))  # -ln|rho12| from Eq.(2)
sigma_paper = Tp*(Tp/(Tm - t))**sp.Rational(1, 3)           # GPP's stated sigma(T)
# closed form of W^2*Integral_0^T sigma_paper dt, verified by differentiation below
expo_paper = W**2*Tp**sp.Rational(4, 3)*sp.Rational(3, 2)*(Tm**sp.Rational(2, 3) - (Tm - T)**sp.Rational(2, 3))
_chk = (sp.diff(expo_paper, T) - W**2*sigma_paper.subs(t, T)).subs({Tm: 7, T: 3, Tp: 2, W: 5}).evalf()
assert abs(_chk) < 1e-12 and expo_paper.subs(T, 0) == 0, _chk
expo_paper_full = sp.simplify(expo_paper.subs(T, Tm))
expo_gauss = W**2*dT2/2                                      # Gaussian average of exp(-i w t)
print("\nA. -ln|rho12| coefficient of t_P^(4/3) T^(2/3) omega^2:")
print("   sigma = d(dT^2)/dT with Eq.(1):", sp.simplify(expo_def/(Tp**sp.Rational(4,3)*T**sp.Rational(2,3)*W**2)))
print("   GPP stated sigma, integrated to T = Tmax:", sp.simplify(expo_paper_full/(Tp**sp.Rational(4,3)*Tm**sp.Rational(2,3)*W**2)))
print("   direct Gaussian blur exp(-w^2 dT^2/2):", sp.simplify(expo_gauss/(Tp**sp.Rational(4,3)*T**sp.Rational(2,3)*W**2)))
print("   GPP stated sigma vs derivative of Eq.(1):", sp.simplify(sigma_paper.subs(t, T)), "vs", sp.simplify(sigma_def))
for coef in (0.5, 1.0, 1.5):
    print(f"   coef {coef}: exponent at T=1 s, Sr = {coef*tP**(4/3)*1.0**(2/3)*w**2:.3e}")

# ---------------- B. clock-choice dependence ----------------
print("\nB. -ln|rho12| accrued at elapsed T' = 1 s (Sr), GPP sigma, clock optimised for Tmax:")
f = sp.lambdify((Tm, T, Tp, W), expo_paper, 'mpmath')
import mpmath as mp
mp.mp.dps = 40
ref = None
for label, Tmax in [("1 s", 1.0), ("1 day", 86400.0), ("1 yr", 3.15576e7), ("13.8 Gyr", 13.8e9*3.15576e7)]:
    val = f(mp.mpf(Tmax), mp.mpf(1), mp.mpf(tP), mp.mpf(w))
    if ref is None:
        ref = val
    print(f"   Tmax = {label:9s}: {mp.nstr(val, 5)}   ratio to Tmax=1 s: {mp.nstr(val/ref, 4)}")

# ---------------- C. origin of T^(1/3) ----------------
dt, M, E, Tl = sp.symbols('deltaT M DeltaE T', positive=True)
hb, GG, cc = sp.symbols('hbar G c', positive=True)
# Premise set 1 (Salecker-Wigner free-mass spreading + clock not a black hole, size/c <= dT):
#   dT^2 >= hbar T/(M c^2),  dT >= 2 G M / c^3   -> eliminate M at equality
Msol = sp.solve(sp.Eq(dt, 2*GG*M/cc**3), M)[0]
sw = sp.solve(sp.Eq(dt**2, hb*Tl/(Msol*cc**2)), dt)
print("\nC. Premise set 1 (free-mass spreading + no BH): dT_min =", sp.simplify(sw[0]))
# Premise set 2 (clock-agnostic: energy-time resolution dT >= hbar/(2 DeltaE), clock mass-energy
#   >= DeltaE, size >= Schwarzschild radius, dT >= size/c): dT >= max(hbar/(2E), 2 G E/c^5)
Esol = sp.solve(sp.Eq(hb/(2*E), 2*GG*E/cc**5), E)[0]
dmin2 = sp.simplify(hb/(2*Esol))
print("   Premise set 2 (energy-time + no BH, no free spreading): dT_min =", dmin2,
      "= t_P * ", sp.simplify(dmin2/sp.sqrt(hb*GG/cc**5)), "; depends on T?", dmin2.has(Tl))
print("   GPP Eq.(2) rate with T-independent dT: sigma = d(dT^2)/dT =", sp.diff(dmin2**2, Tl))
print(f"   residual fixed blur exponent (t_P^2 w^2/2), Sr: {tP**2*w**2/2:.3e} (non-accumulating)")

# ---------------- D. black-hole claim ----------------
print("\nD. GPP Eq.(4)-(5) black hole. |rho12(T)/rho12(0)| = ((Tmax-T)/Tmax)^k")
# consistency of prefactor: omega12^2 * sigma with Eq.(4) omega12 = (1/(8 pi)^2)(1/t_P)(t_P/(Tmax-T))^(1/3)
om12 = (1/(8*sp.pi)**2)/Tp*(Tp/(Tm - t))**sp.Rational(1, 3)
rate = sp.simplify(om12**2*sigma_paper)
print("   omega12^2 * sigma =", rate, " -> k from Eq.(4)+(2) =", sp.simplify(rate*(Tm - t)),
      "; paper's Eq.(5) states k = 1/(8 pi)^2 =", float(1/(8*math.pi)**2))
def tevap(Mkg):
    return 5120*math.pi*G**2*Mkg**3/(hbar*c**4)
for k_label, k in [("paper 1/(8pi)^2", 1/(8*math.pi)**2), ("Eq4-consistent 1/(8pi)^4", 1/(8*math.pi)**4)]:
    for name, Mkg in [("1 solar mass", 1.989e30), ("1e12 kg", 1e12)]:
        Tmax = tevap(Mkg)
        coh = (tP/Tmax)**k
        ln_needed = 1.0/k  # e-fold needs ln(Tmax/(Tmax-T)) = 1/k
        log10_gap = math.log10(Tmax) - ln_needed/math.log(10)
        print(f"   [{k_label}] {name}: Tmax = {Tmax:.3e} s; coherence left at T = Tmax - t_P: {coh:.4f};"
              f" 1/e reached only at Tmax - T = 10^{log10_gap:.1f} s (t_P = 10^{math.log10(tP):.1f} s)")
