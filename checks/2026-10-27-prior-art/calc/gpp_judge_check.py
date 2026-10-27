"""Judge's independent re-check for finding gambini-porto-pullin (2026-10-27).

GPP 2004 PRL (hep-th/0406260v1):
  eq. (2): d rho/dT = -i[H, rho] - sigma(T) [H,[H,rho]]
  sigma(T) = t_P (t_P/(Tmax-T))^(1/3)
  eq. (4): omega12 = a/t_P * (t_P/(Tmax-T))^(1/3), printed a = 1/(8 pi)^2
  eq. (5): log(rho12(T)/rho12(0)) = i Int omega12 + k log((Tmax-T)/Tmax), printed k = 1/(8 pi)^2

Checks:
  A. symbolic: k = a^2 follows from eq. (2) with eq. (4) and sigma.
  B. numbers at Tmax - t_P, and the e-fold interval, for printed k and k = (8 pi)^-4.
  C. sensitivity (judge's own extension, assumptions stated): what a is if the
     two-level gap is k_B T_Hawking and the exact Hawking lifetime
     Tmax = 5120 pi M^3 (Planck units) is used instead of the PRL's eq. (1)
     convention Tmax = M^3; and the effect of the 1/36 sigma normalisation the
     authors adopt in gr-qc/0501027.
"""
import sympy as sp
import mpmath as mp

# ---------- A. symbolic ----------
T, Tm, tP, a = sp.symbols('T T_max t_P a', positive=True)
sigma = tP * (tP / (Tm - T)) ** sp.Rational(1, 3)
omega = a / tP * (tP / (Tm - T)) ** sp.Rational(1, 3)
# For a two-level system, [H,[H,rho]]_12 = omega12^2 rho12, so
# d log|rho12| / dT = -sigma omega^2. Integrate from 0 to T.
rate = sp.simplify(sigma * omega ** 2 * (Tm - T))
print("A. sigma*omega^2*(Tmax-T) =", rate)
Tp = sp.symbols('Tp', positive=True)
integral = sp.integrate((sigma * omega ** 2).subs(T, Tp), (Tp, 0, T))
print("   -Int_0^T sigma omega^2 dT' =", sp.simplify(-integral))
a_printed = 1 / (8 * sp.pi) ** 2
print("   k with printed eq.(4) a = (8pi)^-2:", sp.nsimplify(a_printed ** 2), "=", sp.N(a_printed ** 2, 6))
print("   k with a = 1/(8pi) (hep-th/0405183 omega=1/(8 pi M)):", sp.N((1 / (8 * sp.pi)) ** 2, 6))
print("   printed eq.(5) k = (8pi)^-2 =", sp.N(a_printed, 6), "; mismatch factor (8pi)^2 =", sp.N((8 * sp.pi) ** 2, 6))

# ---------- B. numbers ----------
mp.mp.dps = 50
G = mp.mpf('6.67430e-11'); hbar = mp.mpf('1.054571817e-34'); c = mp.mpf('299792458')
t_P = mp.sqrt(hbar * G / c ** 5)
Msun = mp.mpf('1.98892e30')


def tmax(M):
    return 5120 * mp.pi * G ** 2 * M ** 3 / (hbar * c ** 4)


k_pr = 1 / (8 * mp.pi) ** 2
k_cons = 1 / (8 * mp.pi) ** 4
print("\nB. t_P = %s s, log10 t_P = %s" % (mp.nstr(t_P, 6), mp.nstr(mp.log10(t_P), 6)))
for name, M in [("solar mass", Msun), ("1e12 kg", mp.mpf('1e12'))]:
    Tx = tmax(M)
    print("  %s: Tmax = %s s" % (name, mp.nstr(Tx, 5)))
    for kn, k in [("printed (8pi)^-2", k_pr), ("consistent (8pi)^-4", k_cons)]:
        coh = (t_P / Tx) ** k
        efold = mp.log10(Tx) - 1 / (k * mp.log(10))
        print("    k=%s: coherence at Tmax-t_P = %s ; one e-fold at Tmax-T = 10^%s s"
              % (kn, mp.nstr(coh, 6), mp.nstr(efold, 6)))

# ---------- C. sensitivity (own extension) ----------
# Hawking: omega_H = k_B T_H / hbar = 1/(8 pi M) in Planck units (M in m_P, omega in 1/t_P).
# Remaining lifetime tau = 5120 pi M^3 t_P  ->  M = (tau/(5120 pi t_P))^(1/3).
# So omega_H = (5120 pi)^(1/3)/(8 pi) * (1/t_P) (t_P/tau)^(1/3): a_exact = (5120 pi)^(1/3)/(8 pi).
a_exact = (5120 * mp.pi) ** (mp.mpf(1) / 3) / (8 * mp.pi)
print("\nC. a with gap = k_B T_H and exact Hawking lifetime: %s ; k = a^2 = %s" % (mp.nstr(a_exact, 6), mp.nstr(a_exact ** 2, 6)))
for name, M in [("solar mass", Msun), ("1e12 kg", mp.mpf('1e12'))]:
    Tx = tmax(M)
    for sn, s in [("sigma as in PRL", 1), ("sigma x 1/36 (gr-qc/0501027)", mp.mpf(1) / 36)]:
        k = a_exact ** 2 * s
        coh = (t_P / Tx) ** k
        print("    %s, %s: k = %s, coherence at Tmax-t_P = %s" % (name, sn, mp.nstr(k, 5), mp.nstr(coh, 4)))
    # printed k with the 1/36 sigma
    coh36 = (t_P / Tx) ** (k_pr / 36)
    print("    %s, printed k with 1/36 sigma: coherence at Tmax-t_P = %s" % (name, mp.nstr(coh36, 6)))

# ---------- D. consistent-constant sensitivity (own extension) ----------
# If the exact lifetime is used in BOTH places: clock resolution dT = c1 * M(tau) * t_P with
# M(tau) = (tau/(5120 pi t_P))^(1/3), tau = Tmax - T, and sigma = |d(dT)^2/dT|, then
# sigma = (2/3) c1^2 (5120 pi)^(-2/3) * sigma_PRL, and with a_exact^2 = (5120 pi)^(2/3)/(8 pi)^2
# the 5120 pi cancels: k = (2/3) c1^2 / (8 pi)^2. c1 is the clock-resolution constant (not fixed by GPP).
tau, c1 = sp.symbols('tau c1', positive=True)
Mtau = (tau / (5120 * sp.pi * tP)) ** sp.Rational(1, 3)
sig_c = sp.Abs(sp.diff((c1 * Mtau * tP) ** 2, tau))
om_c = 1 / (8 * sp.pi * Mtau * tP)
k_c = sp.simplify(sig_c * om_c ** 2 * tau)
print("\nD. consistent exact-lifetime k(c1) =", k_c, "=", sp.N(k_c.subs(c1, 1), 6), "* c1^2")
# Threshold k for one e-fold of decoherence by Tmax - t_P: k_crit = 1/ln(Tmax/t_P)
for name, M in [("solar mass", Msun), ("1e12 kg", mp.mpf('1e12'))]:
    Tx = tmax(M)
    L = mp.log(Tx / t_P)
    print("  %s: ln(Tmax/t_P) = %s ; k for 1 e-fold at Tmax-t_P = %s (printed k is %s x below; (8pi)^-4 is %s x below);"
          " k for 1e-28 residual at Tmax-t_P = %s"
          % (name, mp.nstr(L, 5), mp.nstr(1 / L, 4), mp.nstr((1 / L) / k_pr, 3), mp.nstr((1 / L) / k_cons, 4),
             mp.nstr(28 * mp.log(10) / L, 4)))
