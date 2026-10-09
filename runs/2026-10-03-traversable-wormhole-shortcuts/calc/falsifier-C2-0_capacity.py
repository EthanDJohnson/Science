"""Falsifier C2-0: information capacity of the Standard-Model MMP wormhole.

C2 claims SM fields "pass only qubit-scale signals" (argument: "only single quanta
below about 1e8 eV pass"). MMP (arXiv:1807.04726 p.19) say the binding energy is
larger than the throat energy gap "by a factor of q". The back-reaction limit is on
the TOTAL energy in the throat, so the number of gap-scale quanta (each able to
carry >= 1 qubit) that can be in the throat at once is ~ |E_min| / E_gap.

Natural units hbar = c = 1 for the algebra (sympy); SI for the numbers.
Inputs: the lens readings already verified in math/ (M-ENGINEER-05, M-CONSTRAINTS-16).
"""
import sympy as sp
import math

# ---- algebra (natural units, G = l_P^2) ----
re, G, q, N = sp.symbols('r_e G q N', positive=True)
ell = 16 * re**3 / (G * q * N)                 # MMP eq 5.31 with lens N-species extension (N=1 is MMP)
Emin = G * q**2 * N**2 / (256 * re**3)         # |E_min|
prod = sp.simplify(Emin * ell)
print("ALGEBRA |E_min| * ell (hbar=c=1) =", prod, "  -> at N=1:", prod.subs(N, 1))
# check against MMP's statement binding/gap ~ q
print("ALGEBRA  ratio |E_min| / (1/ell) = q*N/16 : ", sp.simplify(prod - q * N / 16) == 0)

# 2D chiral CFT entropy at energy E on a loop of length L, central charge c:
# u = pi c T^2/12, s = pi c T/6  ->  S = sqrt(pi c L E / 3)
c_, L_, E_ = sp.symbols('c L E', positive=True)
T = sp.sqrt(12 * E_ / (sp.pi * c_ * L_))
S = sp.simplify((sp.pi * c_ * T / 6) * L_)
print("ALGEBRA  S(E) chiral CFT =", S, " ; check S^2 = pi c L E/3:", sp.simplify(S**2 - sp.pi*c_*L_*E_/3) == 0)
S_sub = sp.simplify(S.subs({c_: q / 2, L_: sp.pi * ell.subs(N, 1), E_: Emin.subs(N, 1)}))
print("ALGEBRA  S at E=|E_min|, c=q/2, L=pi*ell (N=1) =", S_sub, "=", sp.N(S_sub / q, 4), "* q nats")

# ---- SI numbers ----
hbar = 1.054571817e-34   # J s
cc = 2.99792458e8        # m/s
Gs = 6.67430e-11         # m^3 kg^-1 s^-2
lP = math.sqrt(hbar * Gs / cc**3)
eV = 1.602176634e-19
r_e = hbar * cc / (1e12 * eV)   # 1/TeV in m
print(f"\nSI  l_P = {lP:.4e} m ; r_e = hbar c / TeV = {r_e:.4e} m")

cases = [("engineer g=0.06, N=1", 4.13e14, 1),
         ("engineer g=0.06, N=54", 4.13e14, 54),
         ("constraints g=e, N=1", 2.114e15, 1)]
for name, qq, NN in cases:
    l_m = 16 * r_e**3 / (lP**2 * qq * NN)            # m
    Eb = hbar * cc * qq * NN**2 / (256 * r_e**3) * lP**2  # J  (G q^2 N^2/(256 r_e^3) -> hbar c l_P^2 q^2 N^2/(256 r_e^3)) per q? see below
    # careful: natural-units E = G q^2 N^2 /(256 r_e^3) has dimension 1/length; SI energy = hbar c * that
    Eb = hbar * cc * lP**2 * qq**2 * NN**2 / (256 * r_e**3)
    t_tr = math.pi * l_m / cc
    for label, Eq in (("E_q = hbar c/ell", hbar * cc / l_m), ("E_q = 2 pi hbar c/ell", 2 * math.pi * hbar * cc / l_m)):
        Nq = Eb / Eq
        print(f"SI  [{name}] ell = {l_m:.3e} m, |E_min| = {Eb:.3e} J = {Eb/eV/1e6:.3g} MeV, "
              f"transit pi*ell/c = {t_tr:.3e} s; {label} = {Eq/eV:.3e} eV -> N_quanta in throat = {Nq:.3e} "
              f"(q N/16 = {qq*NN/16:.3e}); qubit rate ~ N/transit = {Nq/t_tr:.3e} qubit/s")
    S_nats = math.sqrt(math.pi * (qq / 2) * (math.pi * l_m) * Eb / (3 * hbar * cc))
    print(f"SI  [{name}] chiral-gas entropy at E=|E_min| (c=q/2, L=pi*ell) = {S_nats:.3e} nats = {S_nats/math.log(2):.3e} bits")
    print(f"SI  [{name}] |E_min| / (1 kg c^2) = {Eb/(1*cc**2):.3e} ; log10 = {math.log10(Eb/cc**2):.2f}")
print("\nRESULT: per-transit capacity ~1e12-1e15 qubits, not ~1 qubit; energy cap still ~25-29 orders below 1 kg c^2.")

# ---- Conservative case: a sender in the broken-phase exterior must use massive charged
# fermions (electrons, m_e c^2 = 0.511 MeV) to reach the LLL channels; each such quantum
# costs >= m_e c^2 of throat energy. Bits per electron <= log2(2q) (channel label + spin).
me_c2 = 0.51099895e6 * eV
print("\nCONSERVATIVE (electron carriers, E >= m_e c^2):")
for name, qq, NN in cases:
    l_m = 16 * r_e**3 / (lP**2 * qq * NN)
    Eb = hbar * cc * lP**2 * qq**2 * NN**2 / (256 * r_e**3)
    t_tr = math.pi * l_m / cc
    Ne = Eb / me_c2
    bits = Ne * math.log2(2 * qq)
    print(f"SI  [{name}] N_e = |E_min|/m_e c^2 = {Ne:.3g} electrons in throat at once; "
          f"<= {bits:.3g} bits per transit; sustained <= {bits/t_tr:.3g} bit/s")

# ---- Separation: MMP put SM mouths within d < 1/TeV (or d < 1/m_e). T_thru/T_ext = pi*ell/d.
d_TeV = r_e
d_me = hbar / (9.1093837e-31 * cc)
print("\nSEPARATION (SM-MMP): d < 1/TeV = %.3e m, or d < hbar/(m_e c) = %.3e m" % (d_TeV, d_me))
for name, qq, NN in cases:
    l_m = 16 * r_e**3 / (lP**2 * qq * NN)
    print(f"SI  [{name}] T_ext <= {d_me/cc:.3e} s ; T_thru = {math.pi*l_m/cc:.3e} s ; "
          f"T_thru/T_ext >= {math.pi*l_m/d_me:.3e} (d = 1/m_e), {math.pi*l_m/d_TeV:.3e} (d = 1/TeV)")
