#!/usr/bin/env python3
"""Task D(1): pair rate of an isotropic, unpolarised, INCOHERENT graviton gas (B&O eq. 14), the '1e-110' number
emissivity, and the depletion equation (B&O eq. 15 / S9).

Quantities (kept apart throughout):
  Gamma        = mean number of photon PAIRS produced per unit volume per unit time (in-in mean number, leading order);
                 B&O's dP/dtdV.  Photons per volume per time = 2 Gamma (B&O's 'number emissivity 2 dP/dtdV').
  Gamma_1(k)   = loss rate (per unit time) of ONE graviton of momentum k in the gas (each pair removes two gravitons:
                 int dn_1 Gamma_1 = 2 Gamma).
  sigma        = g g -> gamma gamma cross section for given incoming PHYSICAL helicities, summed over photon
                 helicities, identical-photon 1/2 included (counts pairs).

Route (independent of B&O's text):
  (a) sigma from the closed-form |M| = 8 pi G t^2/s, u^2/s (opposite physical helicities; same helicities 0), exact
      sympy integration; spot-check of the module's helicity amplitudes and sigma_total.
  (b) Glauber-Sudarshan P-representation: for a Gaussian P (thermal-like, random phases) the 4th moment
      <a_i a_j a*_k a*_l> = N_i N_j (d_ik d_jl + d_il d_jk) turns the coherent amplitude (1/2) sum a_i a_j m_ij into the
      kinetic sum over UNORDERED graviton pairs sum_{i<j} N_i N_j |m_ij|^2 (this is where the initial-state 1/2 of
      Gamma = (1/2) int dn dn sigma v comes from).  Monte Carlo over random phases checks it.
  (c) the isotropic average (sympy) and, as a second route, the module's two-beam rate (beams_pair_rate, full
      background-field amplitude + its own phase-space quadrature) averaged over relative angle and helicities;
      spectrum independence; polarised backgrounds; B&O's coherent/incoherent comparison (V w sigma^2 -> 40 pi^2/9).
  (d) SI numbers: Gamma_SI = (8 pi/15) G^2 rho^2 / c^7 (no hbar), with rho_GW from Delta N_eff.
  (e) depletion: Gamma_1(k) = (16 pi/15) G^2 k rho (sympy + module); redshift bookkeeping of S9 (sympy); numerical
      check of the formal solution y(k,z) = y(k,0) exp(-k Phi(z)); |Phi| up to z = 1e28 in SI; CMB-stimulated and
      plasma-frequency caveats.
Natural units hbar = c = 1 (G = 1 in parts a-c), SI in d-e.  Usage: python3 taskD1_sgwb_rate.py [--part a|b|c|d|e]
"""
import argparse
import math
import os
import sys

import numpy as np
import sympy as sp
from scipy import constants as K_
from scipy import integrate

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills", "conundrum", "scripts"))
import qft_second_order as q2  # noqa: E402

PI = math.pi
ap = argparse.ArgumentParser()
ap.add_argument("--part", default="all", choices=["a", "b", "c", "d", "e", "all"])
args = ap.parse_args()
run = lambda p: args.part in (p, "all")  # noqa: E731


def hdr(t):
    print("\n" + "=" * 110 + "\n" + t + "\n" + "=" * 110)


# ------------------------------------------------------------------------------------------------ (a)
if run("a"):
    hdr("(a) sigma(g g -> gamma gamma): closed form (sympy) and module spot checks")
    s, c, G, ph = sp.symbols("s c G phi", positive=True)
    t = -s * (1 - c) / 2
    u = -s * (1 + c) / 2
    M2 = (8 * sp.pi * G) ** 2 * (t ** 4 + u ** 4) / s ** 2       # sum over the two nonzero photon assignments
    dphi2 = 1 / (32 * sp.pi ** 2)                                  # dPhi_2 = dOmega/(32 pi^2), massless
    sig_full = sp.Rational(1, 2) / (2 * s) * sp.integrate(sp.integrate(M2 * dphi2, (c, -1, 1)), (ph, 0, 2 * sp.pi))
    sig_hemi = 1 / (2 * s) * sp.integrate(sp.integrate(M2 * dphi2, (c, 0, 1)), (ph, 0, 2 * sp.pi))
    print("sigma_opp, full sphere with identical-photon 1/2 :", sp.simplify(sig_full))
    print("sigma_opp, hemisphere (each pair once), no 1/2   :", sp.simplify(sig_hemi))
    print("expected (4/5) pi G^2 s                          :", sp.Rational(4, 5) * sp.pi * G ** 2 * s)
    sig_unpol = sp.Rational(1, 4) * (2 * sig_full + 2 * 0)
    print("unpolarised average (1/4) sum_{l1 l2} sigma      :", sp.simplify(sig_unpol), "  (same helicities give 0)")

    print("\nmodule helicity amplitudes (physical helicities along each particle's own momentum), |M|/(8 pi G):")
    for sv, th in ((1.0, 0.4), (2.5, 1.3), (0.7, 2.4)):
        amps = q2.helicity_amplitudes_cm(sv, th, 0.37, final="photon")
        tv, uv = -sv * (1 - math.cos(th)) / 2, -sv * (1 + math.cos(th)) / 2
        nz = {k: abs(v) / (8 * PI) for k, v in amps.items() if abs(v) > 1e-9 * 8 * PI * sv}
        mx_zero = max(abs(v) for k, v in amps.items() if k not in nz) / (8 * PI * sv)
        print(f"  s={sv}, theta={th}: t^2/s={tv*tv/sv:.12f}, u^2/s={uv*uv/sv:.12f}; nonzero: "
              + ", ".join(f"{k}:{v:.12f}" for k, v in sorted(nz.items())) + f";  max |others|/(8 pi s) = {mx_zero:.1e}")
    print("\nmodule sigma_total / ((4/5) pi G^2 s):")
    for sv in (0.5, 3.0):
        row = []
        for p1, p2 in (("R", "L"), ("L", "R"), ("R", "R"), ("L", "L"), ("plus", "plus"), ("plus", "cross")):
            row.append(f"{p1}/{p2}={q2.sigma_total(sv, p1, p2, 'photon') / (0.8 * PI * sv):.12f}")
        print(f"  s={sv}: " + ", ".join(row))

# ------------------------------------------------------------------------------------------------ (b)
if run("b"):
    hdr("(b) P-representation (Gaussian, random phases) -> kinetic sum over unordered graviton pairs")
    rng = np.random.default_rng(7)
    nm = 5
    Nocc = np.array([3.0, 1.0, 2.5, 0.7, 1.8])
    mm = rng.normal(size=(nm, nm)) + 1j * rng.normal(size=(nm, nm))
    mm = 0.5 * (mm + mm.T)                     # symmetric pair amplitude to ONE fixed final photon state
    for with_diag in (False, True):
        m = mm.copy()
        if not with_diag:
            np.fill_diagonal(m, 0.0)               # physical: i = j means K = 2k null, amplitude 0
        nsamp, acc, acc2 = 0, 0.0, 0.0
        for _ in range(40):
            z = (rng.normal(size=(100000, nm)) + 1j * rng.normal(size=(100000, nm))) / math.sqrt(2)
            al = z * np.sqrt(Nocc)                 # <|alpha_i|^2> = N_i, uniform random phases
            A = 0.5 * np.einsum("si,ij,sj->s", al, m, al)
            acc += float(np.sum(np.abs(A) ** 2))
            acc2 += float(np.sum(np.abs(A) ** 4))
            nsamp += al.shape[0]
        mean = acc / nsamp
        err = math.sqrt(max(acc2 / nsamp - mean ** 2, 0) / nsamp)
        pred = sum(Nocc[i] * Nocc[j] * abs(m[i, j]) ** 2 for i in range(nm) for j in range(i + 1, nm))
        pred += 0.5 * sum(Nocc[i] ** 2 * abs(m[i, i]) ** 2 for i in range(nm))
        print(f"  diagonal m_ii {'kept' if with_diag else 'zero'}: <|A|^2>_P = {mean:.5f} +- {err:.5f};"
              f"  sum_(i<j) N_i N_j |m_ij|^2 (+ (1/2) sum N_i^2 |m_ii|^2) = {pred:.5f}")
    m = mm.copy()
    np.fill_diagonal(m, 0.0)
    pred = sum(Nocc[i] * Nocc[j] * abs(m[i, j]) ** 2 for i in range(nm) for j in range(i + 1, nm))
    al = np.sqrt(Nocc).astype(complex)
    print("  a single COHERENT state with the same N_i (|A|^2 / incoherent value):")
    print(f"     all phases equal      : {abs(0.5 * al @ m @ al) ** 2 / pred:.4f}")
    for k in range(3):
        alr = al * np.exp(2j * PI * rng.random(nm))
        print(f"     fixed random phases #{k}: {abs(0.5 * alr @ m @ alr) ** 2 / pred:.4f}")
    print("  => the incoherent rate is the phase average of the coherent one; interference between different graviton")
    print("     pairs feeding the same final state is what a coherent state adds (it can raise or lower the rate).")
    print("  continuum: sum_{i<j} = (1/2) sum_{i != j}  ->  Gamma = (1/2) sum_{l1 l2} int dn_l1 dn_l2 sigma_{l1 l2} v_rel,")
    print("             v_rel = 1 - cos theta_12 (massless Moller flux); no zero-point (1/2) term: normal ordering.")

# ------------------------------------------------------------------------------------------------ (c)
if run("c"):
    hdr("(c) isotropic gas: Gamma = (8 pi/15) G^2 rho^2 ?  (sympy, then module two-beam route)")
    k1, k2, c, G = sp.symbols("k1 k2 c G", positive=True)
    np_, nm_ = sp.symbols("n_p n_m", positive=True)      # helicity +2 / -2 densities (monochromatic check)
    sig_opp = sp.Rational(4, 5) * sp.pi * G ** 2 * 2 * k1 * k2 * (1 - c)
    ang = sp.Rational(1, 2) * sp.integrate(sig_opp * (1 - c), (c, -1, 1))      # isotropic relative directions
    # Gamma = (1/2) sum_{l1 l2} n n <sigma v>: only (+,-) and (-,+) contribute
    Gam = sp.Rational(1, 2) * 2 * np_ * nm_ * ang
    w, rho, p = sp.symbols("omega rho p", positive=True)
    Gam_mono = sp.simplify(Gam.subs({k1: w, k2: w}))
    print("Gamma (physical helicities)            =", sp.factor(Gam_mono), " ; with n_p w = rho_p, n_m w = rho_m:",
          sp.factor(Gam_mono.subs({np_: sp.Symbol('rho_p') / w, nm_: sp.Symbol('rho_m') / w})))
    unpol = sp.simplify(Gam_mono.subs({np_: rho / (2 * w), nm_: rho / (2 * w)}))
    print("unpolarised (rho_p = rho_m = rho/2)     =", unpol, "  ;  B&O eq. 14: 8 pi G^2 rho^2/15 ; ratio =",
          sp.simplify(unpol / (8 * sp.pi * G ** 2 * rho ** 2 / 15)))
    print("helicity fraction p of +2:  Gamma/(8 pi G^2 rho^2/15) =",
          sp.simplify(Gam_mono.subs({np_: p * rho / w, nm_: (1 - p) * rho / w}) / (8 * sp.pi * G ** 2 * rho ** 2 / 15)),
          " -> 0 for a fully circularly polarised background")
    alt = sp.Rational(1, 2) * (np_ ** 2 + nm_ ** 2) * ang.subs({k1: w, k2: w})
    print("if eq. 6's equal labels were PHYSICAL helicities (same-helicity pairs radiate):  Gamma/(8 pi G^2 rho^2/15) =",
          sp.simplify(alt.subs({np_: p * rho / w, nm_: (1 - p) * rho / w}) / (8 * sp.pi * G ** 2 * rho ** 2 / 15)),
          " (= 1 only at p = 1/2: eq. 14 is blind to the label reading)")
    print("spectrum: sigma v ~ k1 k2, so Gamma = (32 pi/15) G^2 (int k dn_+)(int k dn_-) = (8 pi/15) G^2 rho^2 for ANY "
          "isotropic unpolarised spectrum (the integrand factorises).")

    print("\nmodule route: beams_pair_rate (full amplitude, module phase space), Gauss-Legendre average over cos(theta_12)")
    cg, wg = np.polynomial.legendre.leggauss(12)

    def ang_avg(w1, w2, p1, p2):
        tot = 0.0
        for cc, ww in zip(cg, wg):
            r = q2.beams_pair_rate(w1, 1e-3, w2, 1e-3, math.acos(cc), p1, p2, "photon", G=1.0)
            tot += 0.5 * ww * r["pair_rate"] / (r["n1"] * r["n2"])
        return tot                                 # = <sigma v> over isotropic relative directions

    res = {}
    for (w1, w2) in ((1.0, 1.0), (0.5, 2.0), (0.3, 1.7)):
        for p1, p2 in (("R", "L"), ("L", "R"), ("R", "R"), ("L", "L")):
            res[(w1, w2, p1, p2)] = ang_avg(w1, w2, p1, p2)
        sv_unpol = 0.25 * sum(res[(w1, w2, a, b)] for a, b in (("R", "L"), ("L", "R"), ("R", "R"), ("L", "L")))
        # Gamma = (1/2) n^2 <sigma v>_unpol for one monochromatic population; for two lines use (w1 w2) scaling
        print(f"  w1={w1}, w2={w2}: <sigma v>(R,L)/(w1 w2) = {res[(w1, w2, 'R', 'L')]/(w1*w2):.12f}"
              f" [sympy: 32 pi/15 = {32*PI/15:.12f}],  (R,R)/(w1 w2) = {res[(w1, w2, 'R', 'R')]/(w1*w2):.2e};"
              f"  (1/2)<sigma v>_unpol/(w1 w2) = {0.5*sv_unpol/(w1*w2):.12f}  [8 pi/15 = {8*PI/15:.12f}]")
    # two-line spectrum: fractions of number f_a at w_a; rho = sum n_a w_a
    wl, fl = np.array([0.3, 1.7]), np.array([0.6, 0.4])
    Gam_two = 0.0
    for a in range(2):
        for b in range(2):
            if a == b:
                svab = 0.25 * sum(ang_avg(wl[a], wl[a], x, y) for x, y in (("R", "L"), ("L", "R"), ("R", "R"), ("L", "L")))
            else:
                svab = 0.25 * sum(res[(0.3, 1.7, x, y)] for x, y in (("R", "L"), ("L", "R"), ("R", "R"), ("L", "L")))
            Gam_two += 0.5 * fl[a] * fl[b] * svab
    rho_two = float(fl @ wl)
    print(f"  two-line isotropic spectrum (60% at 0.3, 40% at 1.7, unpolarised, n = 1): Gamma/rho^2 = {Gam_two/rho_two**2:.12f}"
          f"  (8 pi/15 = {8*PI/15:.12f})")

    hdr("(c') B&O's coherent/incoherent comparison: eq. 8 vs eq. 14 for N gravitons in a volume V")
    N, V, sg, eps, lam = sp.symbols("N V sigma epsilon lambda", positive=True)
    r8 = 3 * G ** 2 * N ** 2 * w ** 3 * sg ** 2 / (25 * sp.pi)
    r14 = 8 * sp.pi * G ** 2 / 15 * (N * w / V) ** 2 * V
    Veq = sp.solve(sp.Eq(r8, r14), V)[0]
    print("eq.8 / (eq.14 x V) =", sp.simplify(r8 / r14), ";  equal when V w sigma^2 =", sp.simplify(Veq * w * sg ** 2),
          " (B&O: 40 pi^2/9)")
    Veff = sp.simplify(Veq.subs({sg: eps * w}).subs({w: 2 * sp.pi / lam}))
    print("V_eff with sigma = eps w, w = 2 pi/lambda:", Veff, " (B&O: 5 lambda^3/(9 pi eps^2));  eps = 0.1:",
          f"{float(Veff.subs({eps: 0.1, lam: 1})):.2f} lambda^3; eps = 0.15: {float(Veff.subs({eps: 0.15, lam: 1})):.2f} lambda^3")

# ------------------------------------------------------------------------------------------------ (d)
G_SI, c_SI, hb, kB = K_.G, K_.c, K_.hbar, K_.k
T0 = 2.7255
Mpc = 1e6 * K_.parsec
H0 = 67.4e3 / Mpc
rho_gam = (PI ** 2 / 15) * (kB * T0) ** 4 / (hb * c_SI) ** 3            # J/m^3
rho_crit = 3 * H0 ** 2 * c_SI ** 2 / (8 * PI * G_SI)                     # J/m^3
fnu = (7 / 8) * (4 / 11) ** (4 / 3)


def gamma_SI(rho):                     # pairs per m^3 per s; (8 pi/15) G^2 rho^2/c^7 (no hbar)
    return 8 * PI / 15 * G_SI ** 2 * rho ** 2 / c_SI ** 7


if run("d"):
    hdr("(d) number emissivity 2 dP/dtdV with Delta N_eff-allowed rho_GW (SI)")
    print("units: Gamma_nat = (8 pi/15) G_nat^2 rho_nat^2 -> Gamma_SI = (8 pi/15) G^2 rho_E^2 / c^7 (pairs m^-3 s^-1);")
    print("       G_nat = G/(hbar c^5), rho_nat = rho_E (hbar c)^3, rate density / (hbar^4 c^3): hbar cancels.")
    print(f"rho_gamma(T0 = {T0} K) = {rho_gam:.4e} J/m^3 ; rho_crit(H0 = 67.4) = {rho_crit:.4e} J/m^3")
    print("Planck 2018 abstract: N_eff = 2.99 +- 0.17 (68%), SM 3.044 -> Delta N_eff <~ 0.3 at 2 sigma")
    for dN in (0.1, 0.2, 0.29, 0.5):
        rg = fnu * dN * rho_gam
        print(f"  Delta N_eff = {dN:4.2f}: rho_GW = {rg:.3e} J/m^3 (Omega_GW h^2 = {rg/rho_crit*0.674**2:.2e});"
              f"  Gamma = {gamma_SI(rg):.2e} pairs m^-3 s^-1;  2 Gamma = {2*gamma_SI(rg):.2e} photons m^-3 s^-1")
    target = 1e-110
    rg_t = math.sqrt(target / 2 / (8 * PI / 15 * G_SI ** 2 / c_SI ** 7))
    print(f"  B&O's '2 dP/dtdV ~ 1e-110 m^-3 s^-1' needs rho_GW = {rg_t:.2e} J/m^3, i.e. Delta N_eff = {rg_t/(fnu*rho_gam):.3f}"
          f" (Omega_GW h^2 = {rg_t/rho_crit*0.674**2:.1e})")
    print("  energy emissivity for photons of energy hbar*omega: 2 Gamma hbar omega (linear in hbar)")
    for nu in (1e-9, 1e2):
        x = hb * 2 * PI * nu / (kB * T0)
        f = 1 / math.expm1(x)
        print(f"  with the CMB stimulated factor (1 + 2 f), nu = {nu:.0e} Hz: 1 + 2 f = {1+2*f:.2e} ->"
              f" 2 Gamma (1 + 2 f) = {2*gamma_SI(fnu*0.29*rho_gam)*(1+2*f):.1e} m^-3 s^-1 (monochromatic estimate)")

# ------------------------------------------------------------------------------------------------ (e)
if run("e"):
    hdr("(e) depletion: Gamma_1(k), B&O eqs. 15 / S9 and |Phi|")
    k1, k2, c, G, rho, w = sp.symbols("k1 k2 c G rho omega", positive=True)
    sig_unpol = sp.Rational(2, 5) * sp.pi * G ** 2 * 2 * k1 * k2 * (1 - c)
    # graviton k1 (either helicity) in an isotropic unpolarised gas: Gamma_1 = int dn_2 <sigma_{l1, l2} v>, n_2 split
    # equally between helicities -> sigma_unpol on average (+ only meets -: (n/2) sigma_opp = n sigma_unpol)
    G1 = sp.Rational(1, 2) * sp.integrate(sig_unpol * (1 - c), (c, -1, 1))       # per partner of energy k2, density 1
    G1 = sp.simplify(G1)
    print("Gamma_1(k1) per unit partner density at energy k2:", G1, " -> int dn_2: (16 pi/15) G^2 k1 rho  (rho = int k2 dn_2)")
    print("check: int dn_1 Gamma_1 = (16 pi/15) G^2 rho^2 = 2 x Gamma(eq. 14) (two gravitons per pair):",
          sp.simplify(sp.Rational(16, 15) * sp.pi * G ** 2 * rho ** 2 / (sp.Rational(8, 15) * sp.pi * G ** 2 * rho ** 2)))
    # module cross-check of the coefficient: helicity +2 graviton at w1 in unpolarised gas at w2
    cg, wg = np.polynomial.legendre.leggauss(12)
    tot = 0.0
    for cc, ww in zip(cg, wg):
        r = q2.beams_pair_rate(0.8, 1e-3, 1.9, 1e-3, math.acos(cc), "R", "L", "photon", G=1.0)
        tot += 0.5 * ww * r["pair_rate"] / (r["n1"] * r["n2"])
    # partner density n (unpolarised) -> n/2 of opposite helicity; Gamma_1/(k1 rho) with rho = n * 1.9
    print(f"module: Gamma_1/(k1 rho) for k1 = 0.8, partners at 1.9 = {0.5*tot/(0.8*1.9):.12f}; 16 pi/15 = {16*PI/15:.12f}")

    z, H, k0 = sp.symbols("z H k0", positive=True)
    yco = sp.Function("Y")(z)            # dRho_co/dlnk at fixed comoving k0
    rco = sp.Symbol("rho_co", positive=True)
    # physical: d(dRho/dlnk)/dt = -(16 pi/15) G^2 k_phys rho_phys dRho/dlnk ; dRho/dlnk = (1+z)^4 Y ; rho_phys = (1+z)^4 rho_co
    # dt = -dz/((1+z) H); free streaming keeps Y constant, so only the collision term changes Y:
    dYdz = (sp.Rational(16, 15) * sp.pi * G ** 2 * (1 + z) * k0 * (1 + z) ** 4 * rco * (1 + z) ** 4 * yco) / ((1 + z) * H) / (1 + z) ** 4
    print("d Y/dz from the physical collision rate (k_phys = (1+z) k0):", sp.simplify(dYdz))
    print("B&O S9 right side:                                         ",
          sp.simplify(16 * sp.pi * G ** 2 / (15 * H) * (1 + z) ** 4 * k0 * rco * yco),
          " -> identical (k = comoving / today's momentum)")

    print("\nformal solution check (toy units G = 1, H(z) = (1+z)^2, y(k, z_i) = k e^{-k}, z from 3 to 0):")
    kg = np.linspace(1e-3, 30, 3000)
    zi = 3.0

    def rhs(zz, Y):            # Y = y(k) = dRho_co/dk on the grid; d y/dz = r(z) rho_co(z) k y  (B&O S9 / k)
        rc = np.trapezoid(Y, kg)
        return 16 * PI / 15 * (1 + zz) ** 4 / (1 + zz) ** 2 * rc * kg * Y

    lam = 0.02
    sol = integrate.solve_ivp(lambda zz, Y: lam * rhs(zz, Y), (zi, 0.0), kg * np.exp(-kg), rtol=1e-10, atol=1e-14,
                              dense_output=True)
    zz = np.linspace(0, zi, 400)
    rc_z = np.array([np.trapezoid(sol.sol(x), kg) for x in zz])
    Phi = -np.array([np.trapezoid((lam * 16 * PI / 15 * (1 + zz[:i + 1]) ** 2) * rc_z[:i + 1], zz[:i + 1]) for i in range(len(zz))])
    y0 = sol.sol(0.0)
    err = np.max(np.abs(y0 * np.exp(-kg * Phi[-1]) - sol.sol(zi))) / np.max(sol.sol(zi))
    print(f"  max |y(k,0) exp(-k Phi(z_i)) - y(k,z_i)| / max y = {err:.1e};  depletion of rho_co: {rc_z[0]/rc_z[-1]:.4f}"
          f"  (high-k end depleted most: y(k=20,0)/y(k=20,z_i) = {np.interp(20, kg, y0)/np.interp(20, kg, sol.sol(zi)):.3e},"
          f" y(k=1,0)/y(k=1,z_i) = {np.interp(1, kg, y0)/np.interp(1, kg, sol.sol(zi)):.4f})")

    print("\n|Phi| in SI: exponent = omega0 * |Phi|, |Phi| = int_0^z (16 pi/15)(G^2 hbar/c^7)(1+z)^4 rho_co / H(z) dz  [s]")
    Om_g = rho_gam / rho_crit
    Om_r = Om_g * (1 + 3.044 * fnu)
    Om_m, Om_L = 0.315, 1 - 0.315 - Om_r

    def Hz(zv, gstar=False):
        H2 = Om_r * (1 + zv) ** 4 + Om_m * (1 + zv) ** 3 + Om_L
        if gstar:
            # radiation with g_* steps (crude): factor (g*/g*0)(g*s0/g*s)^(4/3), T = T0 (1+z) approx
            T_eV = 8.617e-5 * T0 * (1 + zv)
            g = 3.36 if T_eV < 1e5 else (10.75 if T_eV < 1e8 else (61.75 if T_eV < 1e11 else 106.75))
            gs = 3.91 if T_eV < 1e5 else (10.75 if T_eV < 1e8 else (61.75 if T_eV < 1e11 else 106.75))
            H2 = Om_r * (g / 3.36) * (3.91 / gs) ** (4 / 3) * (1 + zv) ** 4 + Om_m * (1 + zv) ** 3 + Om_L
        return H0 * math.sqrt(H2)

    for dN in (0.29,):
        rco_SI = fnu * dN * rho_gam
        for gstar in (False, True):
            lz = np.linspace(0, math.log(1e28), 20001)
            zv = np.expm1(lz)
            integrand = np.array([16 * PI / 15 * G_SI ** 2 * hb / c_SI ** 7 * (1 + x) ** 4 * rco_SI / Hz(x, gstar) * (1 + x)
                                  for x in zv])
            Phi_s = np.trapezoid(integrand, lz)
            print(f"  Delta N_eff = {dN}, rho_co = {rco_SI:.2e} J/m^3, z_max = 1e28 (T = {8.617e-5*T0*1e28/1e9:.1e} GeV),"
                  f" {'g_* steps' if gstar else 'constant Omega_r'}: |Phi| = {Phi_s:.2e} s   (B&O: ~1e-25 Hz^-1)")
            for nu in (1e-9, 1e2, 1e9):
                x = hb * 2 * PI * nu / (kB * T0)
                print(f"      nu0 = {nu:.0e} Hz: omega0|Phi| = {2*PI*nu*Phi_s:.1e};  with CMB-stimulated (1 + 2f):"
                      f" {2*PI*nu*Phi_s*(1+2/math.expm1(x)):.1e}")
    e_HL = math.sqrt(4 * PI * K_.fine_structure)
    print(f"\ncaveat (plasma): relativistic e+- plasma, omega_pl = e T/3 = {e_HL/3:.3f} T; GW today at nu0 << GHz has"
          f" k/T = {hb*2*PI*1e2/(kB*T0):.1e} (100 Hz), so 2-photon final states (photon energies ~k) are below the"
          " plasma cutoff while the plasma is relativistic: S9 integrated to z ~ 1e28 overstates even this tiny depletion.")
    ne0 = 0.88 * 0.0224 * 3 * (100e3 / Mpc) ** 2 / (8 * PI * G_SI) / K_.m_p
    wp0 = math.sqrt(ne0 * K_.e ** 2 / (K_.epsilon_0 * K_.m_e))
    print(f"        today's mean (fully ionised) n_e = {ne0:.2f} m^-3 -> omega_pl0 = {wp0:.1f} rad/s; nHz PTA photons cannot"
          " propagate at all.")
