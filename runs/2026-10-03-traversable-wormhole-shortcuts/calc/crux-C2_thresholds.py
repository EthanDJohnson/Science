"""Crux C2: numbers for the deciding tests against rivals.

1. Symbolic check that MMP's energy function E(l) = A/l^2 - B/l with
   A = r_e^3/G, B = N q / 8 (hbar = c = 1, Q-10) gives |E_min| * l* = N q / 16,
   the identity all three verdicts use for the many-quanta capacity.
2. Clock-offset thresholds (C7) Delta_s = T_thru - d/c and Delta_CTC = T_thru + d/c
   for the SM-MMP rows (ell from the verdicts' logs, d <= hbar c / TeV) and MM (d = ell).
3. Transit times pi*ell/c that any MMP growth rate must be compared with (C1 strong variant).
4. Lowest-Landau-level capacity margin against MSY-type 'a few bits' (C8): Nq/16 quanta.
All SI unless marked.
"""
import sympy as sp

c = 2.99792458e8          # m/s
hbar = 1.054571817e-34    # J s
eV = 1.602176634e-19      # J
yr = 3.15576e7            # s (Julian)
ly = c * yr               # m

# ---- 1. symbolic identity --------------------------------------------------
A, B, l = sp.symbols('A B l', positive=True)
E = A / l**2 - B / l
lstar = sp.solve(sp.diff(E, l), l)[0]
Emin = sp.simplify(E.subs(l, lstar))
print("l* =", lstar, "; E_min =", Emin, "; |E_min|*l* =", sp.simplify(-Emin * lstar))
print("  with B = N q / 8  ->  |E_min| l* = N q / 16 (hbar = c = 1)")

# ---- 2/3. SM-MMP rows (ell values as reproduced in verdict logs) -------------
d_max = hbar * c / (1e12 * eV)    # 1/TeV in m
print(f"\nd_max = hbar c / TeV = {d_max:.4e} m")
rows = {"engineer g=0.06 N=1": 1.139, "constraints g=e N=1": 0.2226,
        "engineer g=0.06 N=54": 0.0211}
for name, ell in rows.items():
    T_thru = 3.141592653589793 * ell / c
    T_ext = d_max / c
    print(f"{name}: ell = {ell} m, T_thru = pi ell/c = {T_thru:.3e} s, "
          f"T_ext <= {T_ext:.3e} s, T_thru/T_ext >= {T_thru/T_ext:.2e}")
    print(f"   Delta_s = {T_thru - T_ext:.4e} s, Delta_CTC = {T_thru + T_ext:.4e} s, "
          f"window 2d/c <= {2*T_ext:.3e} s, window/Delta_s = {2*T_ext/(T_thru-T_ext):.2e}")

# ---- MM at d = ell, ell = 3e3 ly (Q-02) ------------------------------------
ell_MM = 3e3 * ly
T_thru = 3.141592653589793 * ell_MM / c
for d_ly in (3e3, 1e3, 1.0):
    T_ext = d_ly * ly / c
    print(f"MM d = {d_ly:g} ly: T_thru = {T_thru/yr:.4e} yr, Delta_s = {(T_thru-T_ext)/yr:.4e} yr, "
          f"Delta_CTC = {(T_thru+T_ext)/yr:.4e} yr, window = {2*T_ext/yr:.3e} yr")

# ---- 4. MM capacity rate (verdict C2-1 quote: ~c2 qubits per ell; c2 ~ 7e72, Q-02)
c2 = 7e72
print(f"\nMM rate ~ c2 per ell/c = {c2/(ell_MM/c):.2e} qubits/s (order of magnitude)")
