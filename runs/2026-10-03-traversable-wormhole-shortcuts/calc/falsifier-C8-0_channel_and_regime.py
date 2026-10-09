"""Falsifier C8-0 (physics angle).

Two checks on C8 ("two-sided wormholes never beat their coupling channel;
Sycamore-type runs test size winding, not spacetime").

(A) Maldacena-Qi rate check. Plugge, Lantagne-Hurtubise & Franz (PRL 124, 221601;
    arXiv:2003.03914) find the L->R revival frequency omega_re ~ mu^(2/3) (units J = 1,
    hbar = 1), "much larger than the naive guess omega_re ~ mu". Does this mean the
    wormhole beats its coupling channel in rate?  Compare:
      * naive single-mode rate of the bare coupling: ~ mu
      * wormhole transfer: N/2 qubits (N Majoranas per side) moved in t_re ~ pi / mu^(2/3)
        -> qubit rate R_wh ~ (N/2) * mu^(2/3) / pi   [qubits per unit 1/J]
      * the coupling Hamiltonian's own entangling capacity (small-incremental-entangling
        theorem, Van Acoleyen et al. 2013): dE/dt <= c ||H_int|| log2(d),
        d = min(dim L, dim R) = 2^(N/2); ||H_int|| <= N mu / 2 for H_int = i mu sum psi_L psi_R
        with psi^2 = 1/2 (each term norm mu/2).
        Qubit transmission rate <= entanglement-generation rate (a transmitted qubit half
        of a Bell pair yields one ebit), so R_wh <= c ||H_int|| log2 d is required.
      c is taken as 2 (optimistic) and 18 (first proven constant) - both shown.
(B) Gravity-regime check for Sycamore-type sizes. Semiclassical JT/Schwarzian regime
    needs 1 << beta J  and Schwarzian coupling N alpha_S / (beta J) >> 1
    (Maldacena-Stanford 2016, eq. 4.176-4.178: S = -N alpha_S/J int Sch).
    alpha_S(q=4) bracketed between 0.007 (commonly quoted numerical value, not
    verified here) and 1/(4 q^2) = 0.0156 (large-q formula quoted in the source).
"""
import math

print("=== (A) Maldacena-Qi: wormhole transfer rate vs coupling-channel capacity ===")
print("units: hbar = 1, J = 1 (rates in units of J/hbar)")
for N in (100, 1000, 10000):
    for mu in (1e-2, 1e-3, 1e-4):
        naive = mu
        omega_wh = mu ** (2.0 / 3.0)
        enh = omega_wh / naive
        R_wh = (N / 2.0) * omega_wh / math.pi
        Hnorm = N * mu / 2.0
        log2d = N / 2.0
        for c in (2.0, 18.0):
            cap = c * Hnorm * log2d
            print(f"N={N:6d} mu={mu:.0e}: omega_wh/omega_naive = {enh:7.2f};"
                  f" R_wh = {R_wh:10.3e} qubit/(1/J); c={c:4.1f} capacity bound = {cap:10.3e};"
                  f" bound/R_wh = {cap / R_wh:10.3e}")
# where would the bound bite?  bound/R_wh = c*pi*N*mu^(1/3)/2 ... solve = 1
print("bound/R_wh = c * pi * N * mu^(1/3) / 2  (analytic)")
for c in (2.0, 18.0):
    for N in (100, 1000):
        mu_crit = (2.0 / (c * math.pi * N)) ** 3
        print(f"c={c:4.1f}, N={N}: bound would bite only for mu < {mu_crit:.2e} J")
print("Also: at mu = 0 the L-R transmission amplitude vanishes identically (decoupled TFD,"
      " no signal through the bulk) -- nothing is delivered without the channel.")

print()
print("=== (B) Semiclassical-gravity window for Sycamore-type SYK sizes ===")
for alphaS in (0.007, 1.0 / (4 * 4 ** 2)):
    print(f"alpha_S = {alphaS:.4f}")
    for N, bJ, label in ((7, 4.2, "Sycamore learned (N=7; beta J illustrative)"),
                         (8, 3 * math.sqrt(2), "Byun et al. N=8, beta=3, J=sqrt2"),
                         (20, 5.0, "N=20 proposed"),
                         (100, 5.0, "N=100 proposed"),
                         (10000, 10.0, "N=1e4 for comparison")):
        C = N * alphaS / bJ
        print(f"  {label:45s}: N alpha_S = {N * alphaS:8.3f}; beta J = {bJ:5.2f};"
              f" Schwarzian coupling N alpha_S/(beta J) = {C:8.3f}"
              f" -> {'weakly coupled gravity' if C > 10 and bJ > 3 else 'NOT semiclassical'}")
    # minimum N for a window with beta J >= 3 and N alpha_S/(beta J) >= 10
    Nmin = 10 * 3 / alphaS
    print(f"  N needed for beta J >= 3 and N alpha_S/(beta J) >= 10: N >= {Nmin:.0f}")
