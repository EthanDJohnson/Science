"""Angle own-later: what does PRL eq. (5) of Gambini, Porto & Pullin (hep-th/0406260) give at the edge of the
validity region that the authors themselves state in their 2005 proceedings (gr-qc/0501027)?

2005 text (fetch_text, verbatim): the first-order Lindblad expansion used in the PRL is "not a valid expansion
for t = Tmax ... a good approximation to the exact result provided tau(t) << Tmax - t", with the optimal-clock
width tau(T) = t_P^(2/3) T^(1/3) (their eq. 24 context: tau(T) = t_P^(2/3) T^(1/3)).

So the PRL formula can only be trusted for Tmax - T >> tau(Tmax).  We evaluate the PRL eq. (5) decay factor
((Tmax-T)/Tmax)^k  at Tmax - T = tau(Tmax) (the edge), for
  k = (8 pi)^-2   (PRL eq. 5 as printed)
  k = (8 pi)^-4   (what PRL eqs 2, 4 with printed sigma give)
  and the same two divided by 36 (the 2005 paper's sigma carries an extra factor 1/36; footnote [14]).
Tmax is taken in two ways: the authors' own convention Tmax = (M/M_P)^3 t_P (2005 paper: "For a Solar sized black
hole Tmax/tP = (MSun/MP)^3") and Hawking's lifetime 5120 pi G^2 M^3/(hbar c^4) (the latter used in the
earlier calc of this folder).

Also: the authors' 2005 eq. (18) states |rho12(Tmax)| ~ (M_P/M_sun)^(2/3) ~ 1e-28.  We evaluate (M_P/M_sun)^(2/3).

Run: python3 checks/2026-10-27-prior-art/calc/gpp_own_later_validity_edge.py
"""
import mpmath as mp

mp.mp.dps = 50
hbar = mp.mpf("1.054571817e-34")
G = mp.mpf("6.67430e-11")
c = mp.mpf("2.99792458e8")
tP = mp.sqrt(hbar * G / c**5)
mP = mp.sqrt(hbar * c / G)
Msun = mp.mpf("1.98847e30")
print(f"t_P = {mp.nstr(tP, 6)} s ; M_P = {mp.nstr(mP, 6)} kg ; M_sun = {mp.nstr(Msun, 6)} kg")

ks = {
    "(8pi)^-2  [printed eq.5]": 1 / (8 * mp.pi) ** 2,
    "(8pi)^-4  [from eqs 2,4]": 1 / (8 * mp.pi) ** 4,
    "(8pi)^-2 /36 [2005 sigma]": 1 / (8 * mp.pi) ** 2 / 36,
    "(8pi)^-4 /36 [2005 sigma]": 1 / (8 * mp.pi) ** 4 / 36,
}


def report(label, M, Tmax):
    tau = tP ** (mp.mpf(2) / 3) * Tmax ** (mp.mpf(1) / 3)  # clock width at evaporation, tau(Tmax)
    print(f"\n--- {label}: M = {mp.nstr(M, 5)} kg, Tmax = {mp.nstr(Tmax, 5)} s, tau(Tmax) = {mp.nstr(tau, 5)} s "
          f"(= {mp.nstr(tau / tP, 5)} t_P)")
    x = tau / Tmax  # (Tmax - T)/Tmax at the edge of validity
    print(f"    (Tmax-T)/Tmax at the edge = tau/Tmax = {mp.nstr(x, 5)}")
    for name, k in ks.items():
        coh = x**k
        print(f"    k = {name:28s} {mp.nstr(k, 5):>12s}: coherence left at Tmax - T = tau(Tmax): {mp.nstr(coh, 6)}")


# authors' convention: Tmax = (M/M_P)^3 t_P
for name, M in [("solar mass", Msun), ("1e12 kg", mp.mpf("1e12"))]:
    report(f"authors' convention, {name}", M, (M / mP) ** 3 * tP)
# Hawking lifetime
for name, M in [("solar mass", Msun), ("1e12 kg", mp.mpf("1e12"))]:
    report(f"Hawking lifetime, {name}", M, 5120 * mp.pi * G**2 * M**3 / (hbar * c**4))

# sanity on the claimed 1e-28
r = (mP / Msun) ** (mp.mpf(2) / 3)
print(f"\n(M_P/M_sun)^(2/3) = {mp.nstr(r, 5)} = 10^{mp.nstr(mp.log10(r), 5)} (2005 paper eq. 18 says ~10^-28)")


# ---------------------------------------------------------------------------------------------------------
# Part 2: re-check of our own finding's two arithmetic claims, using only the printed PRL ingredients
#   sigma(T) = t_P (t_P/(Tmax-T))^(1/3)      omega12(T) = (8 pi)^-2 / t_P * (t_P/(Tmax-T))^(1/3)
# (a) sigma*omega12^2 = (8 pi)^-4/(Tmax-T)   (b) coherence at Tmax - t_P for the Hawking lifetime
# ---------------------------------------------------------------------------------------------------------
import sympy as sp

tp_s, D = sp.symbols("t_P Delta", positive=True)  # Delta = Tmax - T
sigma_s = tp_s * (tp_s / D) ** sp.Rational(1, 3)
omega_s = (1 / (8 * sp.pi) ** 2) / tp_s * (tp_s / D) ** sp.Rational(1, 3)
prod = sp.simplify(sigma_s * omega_s**2 * D)
print("\nPART 2 (a): sigma*omega12^2*(Tmax-T) =", prod, "= (8 pi)^-4 ?", sp.simplify(prod - 1 / (8 * sp.pi) ** 4) == 0)

print("PART 2 (b): coherence at Tmax - t_P, Hawking lifetime, k = (tP/Tmax)^... i.e. ((tP)/(Tmax))^k")
for name, M in [("solar mass", Msun), ("1e12 kg", mp.mpf("1e12"))]:
    Tmax = 5120 * mp.pi * G**2 * M**3 / (hbar * c**4)
    for kname in ["(8pi)^-2  [printed eq.5]", "(8pi)^-4  [from eqs 2,4]"]:
        k = ks[kname]
        print(f"    {name:10s} Tmax={mp.nstr(Tmax, 4):>10s} s  k={kname:26s} coherence = {mp.nstr((tP / Tmax) ** k, 5)}")


# Part 3: one e-fold of decoherence from PRL eq. (5):  ((Tmax-T)/Tmax)^k = 1/e  =>  Tmax-T = Tmax*exp(-1/k)
print("\nPART 3: Tmax - T at which one e-fold has accumulated (log10 seconds), Hawking lifetime")
for name, M in [("solar mass", Msun), ("1e12 kg", mp.mpf("1e12"))]:
    Tmax = 5120 * mp.pi * G**2 * M**3 / (hbar * c**4)
    for kname in ["(8pi)^-2  [printed eq.5]", "(8pi)^-4  [from eqs 2,4]"]:
        k = ks[kname]
        lg = mp.log10(Tmax) - 1 / (k * mp.log(10))
        print(f"    {name:10s} k={kname:26s} 1/e at Tmax-T = 10^{mp.nstr(lg, 6)} s  (t_P = 10^{mp.nstr(mp.log10(tP), 4)} s)")
