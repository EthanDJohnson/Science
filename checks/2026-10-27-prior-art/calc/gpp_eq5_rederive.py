"""Independent re-derivation of the coefficient in eq. (5) of Gambini, Porto & Pullin,
PRL 93, 240401 (hep-th/0406260), from the paper's own eqs. (2) and (4) and its sigma(T).
Angle: versions.  Written for checks/2026-10-27-prior-art (does not import the earlier run's script).

Printed ingredients (arXiv v1 TeX source, the only arXiv version):
  (2)  d rho/dT = -i[H,rho] - sigma(T) [H,[H,rho]]
  sigma(T)  = (tP/(Tmax-T))^(1/3) tP
  (4)  omega12(T) = 1/((8 pi)^2 tP) * (tP/(Tmax-T))^(1/3)
  (5)  log(rho12(T)/rho12(0)) = i Int_0^T omega12 dT' + 1/(8 pi)^2 log((Tmax-T)/Tmax)

Part A  symbolic: reduce (2) to the 12 element, integrate, read off the coefficient k with
        omega12 = a/tP (tP/(Tmax-T))^(1/3) for a general prefactor a.
Part B  which a reproduces the printed (5)?  a=1/(8 pi)^2 (eq. 4 as printed) vs a=1/(8 pi)
        (the authors' own hep-th/0405183: omega = kT/hbar = 1/(8 pi M), M=(Tmax/tP)^(1/3)).
Part C  numbers: Tmax for a solar-mass hole; coherence left one Planck time before evaporation;
        time before evaporation at which one e-fold has accumulated (log10 seconds).
        Also a numerical quadrature check of the closed form.
Part D  MY OWN EXTENSION, not in the paper: replace the paper's order-of-magnitude Tevap = M^3 tP
        by Hawking's Tevap = 5120 pi G^2 M^3/(hbar c^4) and set the gap to k_B T_H.  Shows how
        sensitive k is to the O(1) constants the paper drops.

Run:  python3 checks/2026-10-27-prior-art/calc/gpp_eq5_rederive.py
"""
import mpmath as mp
import sympy as sp

mp.mp.dps = 60

# ------------------------------------------------------------------ Part A (sympy)
print("=" * 72)
print("PART A: reduce eq. (2) to the 12 matrix element and integrate (sympy)")
tP, Tm, T, Tp, a, w, s = sp.symbols("t_P T_max T Tprime a omega sigma", positive=True)
E1, E2 = sp.symbols("E1 E2", real=True)
# In the energy basis [H,rho]_12 = (E1-E2) rho12, [H,[H,rho]]_12 = (E1-E2)^2 rho12.
# Verify with explicit 2x2 matrices rather than asserting it:
r11, r22 = sp.symbols("r11 r22")
r12, r21 = sp.symbols("r12 r21")
H = sp.diag(E1, E2)
rho = sp.Matrix([[r11, r12], [r21, r22]])
comm = lambda A, B: A * B - B * A
C1 = comm(H, rho)
C2 = comm(H, C1)
print("  [H,rho]_12     =", sp.factor(C1[0, 1]), "  (= (E1-E2) rho12)")
print("  [H,[H,rho]]_12 =", sp.factor(C2[0, 1]), "  (= (E1-E2)^2 rho12)")
assert sp.simplify(C1[0, 1] - (E1 - E2) * r12) == 0
assert sp.simplify(C2[0, 1] - (E1 - E2) ** 2 * r12) == 0

# d(rho12)/dT = [-i (E1-E2) - sigma (E1-E2)^2] rho12   =>   d log rho12/dT = -i w - sigma w^2
sigma_T = tP * (tP / (Tm - T)) ** sp.Rational(1, 3)
omega_T = a / tP * (tP / (Tm - T)) ** sp.Rational(1, 3)  # general prefactor a
integrand = sp.simplify(sigma_T * omega_T**2)
print("  sigma(T)*omega12(T)^2 =", integrand, "   (should be a^2/(Tmax-T))")
assert sp.simplify(integrand - a**2 / (Tm - T)) == 0

# integrate with u = Tmax - T' (u runs from Tmax down to Tmax-T) to stay on the real branch
u = sp.symbols("u", positive=True)
# d(log|rho12|)/dT' = -sigma*omega^2 = -a^2/(Tmax-T').  With u = Tmax-T': Int_0^T g(Tmax-T') dT' = Int_{Tmax-T}^{Tmax} g(u) du.
decay = -sp.integrate(a**2 / u, (u, Tm - T, Tm))
print("  log|rho12(T)/rho12(0)| (from sigma term) = -Int_{Tmax-T}^{Tmax} a^2/u du =", decay)
target = a**2 * sp.log((Tm - T) / Tm)
print("  difference from a^2 log((Tmax-T)/Tmax):", sp.simplify(sp.expand_log(decay - target, force=True)))
print("  => |rho12(T)/rho12(0)| = ((Tmax-T)/Tmax)^k with k = a^2   (phase -i Int omega dT' from the commutator term)")
print("  Note: eq. (5) prints +i Int omega; with eq. (2) as printed (-i[H,rho]) the phase sign depends on")
print("        the sign convention for omega12 = E1-E2 vs E2-E1.  The modulus is unaffected.")

# ------------------------------------------------------------------ Part B
print("=" * 72)
print("PART B: which prefactor a reproduces the printed eq. (5) coefficient 1/(8 pi)^2 ?")
pi = mp.pi
cands = {
    "a = 1/(8 pi)^2  (eq. 4 AS PRINTED)": 1 / (8 * pi) ** 2,
    "a = 1/(8 pi)    (omega = kT/hbar = 1/(8 pi M), hep-th/0405183)": 1 / (8 * pi),
}
printed_k = 1 / (8 * pi) ** 2
for name, av in cands.items():
    k = av**2
    print(f"  {name}: k = a^2 = {mp.nstr(k, 6)}   = (8 pi)^-{'4' if abs(k - (8*pi)**-4) < 1e-30 else '2'}"
          f"   matches printed (5)? {abs(k - printed_k) < mp.mpf('1e-30')}")
print(f"  printed (5) coefficient 1/(8 pi)^2 = {mp.nstr(printed_k, 6)};  (8 pi)^-4 = {mp.nstr((8*pi)**-4, 6)};  ratio = {mp.nstr((8*pi)**2, 6)}")


# Mapping from the authors' hep-th/0405183 convention: omega = kT/hbar = 1/(8 pi M) (G=c=hbar=1) and
# Tevap = (M/mP)^3 tP.  Check numerically that this gives omega12 = a/tP (tP/Tmax)^(1/3) with a = 1/(8 pi).
_G = mp.mpf("6.67430e-11"); _c = mp.mpf("299792458"); _hb = mp.mpf("1.054571817e-34")
_tP = mp.sqrt(_hb * _G / _c**5); _mP = mp.sqrt(_hb * _c / _G)
_M = mp.mpf("1.98847e30")
_Tm = (_M / _mP) ** 3 * _tP                       # paper-convention evaporation time
_omH = _c**3 / (8 * mp.pi * _G * _M)              # k_B T_H / hbar
_a_eff = _omH * _tP / ((_tP / _Tm) ** (mp.mpf(1) / 3))
print(f"  Hawking gap with the authors' Tevap=(M/mP)^3 tP:  omega_H * tP / (tP/Tmax)^(1/3) = {mp.nstr(_a_eff, 10)}   1/(8 pi) = {mp.nstr(1/(8*mp.pi), 10)}")

# ------------------------------------------------------------------ Part C (numbers)
print("=" * 72)
print("PART C: numbers for a solar-mass hole (SI, CODATA 2018)")
G = mp.mpf("6.67430e-11")
c = mp.mpf("299792458")
hbar = mp.mpf("1.054571817e-34")
kB = mp.mpf("1.380649e-23")
tP_s = mp.sqrt(hbar * G / c**5)
mP = mp.sqrt(hbar * c / G)
Msun = mp.mpf("1.98847e30")
print(f"  t_P = {mp.nstr(tP_s, 6)} s ; m_P = {mp.nstr(mP, 6)} kg ; M_sun = {mp.nstr(Msun, 6)} kg")


def Tevap_hawking(M):
    return 5120 * pi * G**2 * M**3 / (hbar * c**4)


def Tevap_paper(M):  # order-of-magnitude law used in hep-th/0405183 eq (4): t = (M/Mp)^3 tP
    return (M / mP) ** 3 * tP_s


def report(label, Tmax, k):
    # |rho12(Tmax - tP)/rho12(0)| = (tP/Tmax)^k ; one e-fold at (Tmax-T)/Tmax = exp(-1/k)
    left = mp.e ** (k * mp.log(tP_s / Tmax))
    log10_dt = mp.log10(Tmax) - 1 / (k * mp.log(10))
    print(f"    {label}: k = {mp.nstr(k, 5):>10} | coherence left at Tmax-tP = {mp.nstr(left, 5):>10}"
          f" | one e-fold at Tmax-T = 10^{mp.nstr(log10_dt, 6)} s")
    return left, log10_dt


cases = {
    "solar mass, Tmax(Hawking 5120 pi)": Tevap_hawking(Msun),
    "1e12 kg,    Tmax(Hawking 5120 pi)": Tevap_hawking(mp.mpf("1e12")),
    "solar mass, Tmax(paper's M^3 tP)": Tevap_paper(Msun),
}
for name, Tmax in cases.items():
    print(f"  {name}: Tmax = {mp.nstr(Tmax, 4)} s  (= {mp.nstr(Tmax/(365.25*86400), 4)} yr)")
    report("k=(8 pi)^-2 printed (5)", Tmax, (8 * pi) ** -2)
    report("k=(8 pi)^-4 from (4) as printed", Tmax, (8 * pi) ** -4)

# quadrature check of the closed form for the solar-mass case (u = Tmax - T')
Tmax = Tevap_hawking(Msun)
for label, av in (("a=(8pi)^-2", (8 * pi) ** -2), ("a=(8pi)^-1", (8 * pi) ** -1)):
    f = lambda lu: av**2  # integrand sigma*omega^2 du = a^2 du/u = a^2 dlog(u): integrate in log u
    I = mp.quad(f, [mp.log(tP_s), mp.log(Tmax)])
    print(f"  quadrature, {label}: Int_0^(Tmax-tP) sigma omega^2 dT' = {mp.nstr(I, 8)}   closed form a^2 ln(Tmax/tP) = {mp.nstr(av**2*mp.log(Tmax/tP_s), 8)}")
print("  e-fold times above are 'the amount of time left before evaporation' ; compare t_P = 10^%s s" % mp.nstr(mp.log10(tP_s), 5))

# direct numeric check of sigma*omega^2 (not assuming the algebra) at a sample point
Tm_n = Tevap_hawking(Msun)
Tn = Tm_n * mp.mpf("0.37")
sig = tP_s * (tP_s / (Tm_n - Tn)) ** (mp.mpf(1) / 3)
om = 1 / ((8 * pi) ** 2 * tP_s) * (tP_s / (Tm_n - Tn)) ** (mp.mpf(1) / 3)
print(f"  pointwise: sigma*omega^2*(Tmax-T) = {mp.nstr(sig*om**2*(Tm_n-Tn), 10)} vs (8 pi)^-4 = {mp.nstr((8*pi)**-4, 10)}")

# ------------------------------------------------------------------ Part D (my extension)
print("=" * 72)
print("PART D (extension beyond the paper; assumptions flagged): sensitivity of k to dropped O(1) constants")
print("  Take gap = hbar*omega12 = k_B T_H = hbar c^3/(8 pi G M)  and the exact Hawking lifetime")
print("  Tmax = 5120 pi G^2 M^3/(hbar c^4), with the paper's sigma unchanged.")
M0 = Msun
Tm0 = Tevap_hawking(M0)
om_H = c**3 / (8 * pi * G * M0)  # k_B T_H / hbar
om_paper_form = 1 / tP_s * (tP_s / Tm0) ** (mp.mpf(1) / 3)  # (1/tP)(tP/Tmax)^(1/3)
ratio = om_H / om_paper_form
print(f"  omega_H(T=0) / [(1/tP)(tP/Tmax)^(1/3)] = {mp.nstr(ratio, 8)}   analytic (5120 pi)^(1/3)/(8 pi) = {mp.nstr((5120*pi)**(mp.mpf(1)/3)/(8*pi), 8)}")
kH = ratio**2
print(f"  => k_H = ratio^2 = {mp.nstr(kH, 6)}  (vs (8 pi)^-2 = {mp.nstr((8*pi)**-2, 5)} and (8 pi)^-4 = {mp.nstr((8*pi)**-4, 5)})")
report("k_H, solar mass", Tm0, kH)
print("  Reading: the printed coefficient equals (gap/omega_scale)^2.  The paper only says the gap is")
print("  'proportional to the temperature' and its Tevap=M^3 tP and delta T ~ ... drop O(1) factors that")
print("  differ by (5120 pi)^(1/3) = 25 in omega, i.e. ~6e2 in k.  With the exact Hawking law k_H ~ 1 and the")
print("  coherence at Tmax - tP is ~ (tP/Tmax)^k_H (printed above, ~1e-119), i.e. the paper's qualitative claim would hold.")
print("  So the 'not complete before Tmax - tP' result depends on the printed prefactor, not on the structure")
print("  of (2)+(sigma); it is an artefact of the paper's own crude constants either way.")
