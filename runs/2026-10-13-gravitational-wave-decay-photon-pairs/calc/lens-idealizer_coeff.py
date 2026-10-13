#!/usr/bin/env python3
"""Idealizer lens: independent closed-form and brute-force reproduction of B&O eq. 8 (3/(25 pi)) and the scalar
7/(450 pi), inside B&O's own model (isotropic coherent shell, top-hat narrow band, real-sign 'unpolarized'
amplitude (t^2+u^2)/s per photon helicity configuration, two configurations; scalar 2tu/s, one configuration).
Natural units hbar = c = 1; G kept symbolic (coefficients are pure numbers multiplying G^2 N^2 w^3 sigma[^2]).

Route (written independently of the run's tool gw_coherent_fusion.py):
  F(p1,p2) = (1/2) int dk1~ dk2~ f f M (2pi)^4 delta^4,  dk~ = d^3k/((2pi)^3 2k)
  int dk1~dk2~ (2pi)^4 delta^4(k1+k2-K) g = (1/(16 pi^2 |K|)) int da dphi g      (d^3k1 = (ab/|K|) da db dphi)
  P = (1/2) sum_configs int d^4K/(2pi)^4 int dOmega*/(32 pi^2) |F|^2
Equal lab energies => CM graviton axis perpendicular to K, so cos(Theta) = sin(theta) cos(phi - psi) and the
ring integral is analytic: int dphi (1 + cos^2 Theta) = 2 pi (1 + sin^2 theta / 2).
"""
import math
import sys

import numpy as np
import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")

PI = math.pi
print("=== Part 1: closed form (sympy), narrow band, top hat, real-sign model ===")
w, sig, G, N, K, x, s = sp.symbols("omega sigma G N K x s", positive=True)
Theta2 = 2 * sp.pi**2 * N / (w * sig)               # top hat per helicity, N = 2 Theta^2 w sigma/(4 pi^2)
# photon: per configuration, M_eff = Theta^2 * 8 pi G (t^2+u^2)/s = Theta^2 8 pi G (s/2)(1+cos^2 Theta)
ring_ph = sp.pi * s * (1 + (1 - x**2) / 2)           # int dphi (s/2)(1+cos^2Theta), x = cos(theta*)
ring_sc = sp.pi * s * (1 - (1 - x**2) / 2)           # scalar: 2tu/s = (s/2) sin^2 Theta
ang_ph = 2 * sp.pi * sp.integrate(((1 + (1 - x**2) / 2))**2, (x, -1, 1))
ang_sc = 2 * sp.pi * sp.integrate(((1 - (1 - x**2) / 2))**2, (x, -1, 1))
print("int dOmega* (1+sin^2/2)^2 =", sp.simplify(ang_ph), " (photon, per config)")
print("int dOmega* (1-sin^2/2)^2 =", sp.simplify(ang_sc), " (scalar)")
# F = (1/2) Theta^2 8 pi G (1/(16 pi^2 K)) L(K0) * pi s (..)  ->  prefactor G Theta^2 L s (..)/(4K)
intL2 = sp.Rational(2, 3) * sig**3                     # int dK0 L(K0)^2 for the top hat (triangle overlap)
sK = 4 * w**2 - K**2
Kint = sp.integrate(sK**2, (K, 0, 2 * w))
print("int_0^{2w} s^2 dK =", sp.simplify(Kint))


def P_total(ang, nconf):
    # P = (1/2) nconf int dK0 4 pi K^2 dK/(2pi)^4 * (1/(32 pi^2)) * Theta^4 G^2 L^2 s^2 (ang)/(16 K^2)
    pref = sp.Rational(1, 2) * nconf * 4 * sp.pi / (2 * sp.pi)**4 / (32 * sp.pi**2) / 16
    return sp.simplify(pref * Theta2**2 * G**2 * intL2 * Kint * ang)


P_ph = P_total(ang_ph, 2)
P_sc = P_total(ang_sc, 1)
c_tot_ph = sp.simplify(P_ph / (G**2 * N**2 * w**3 * sig))
c_tot_sc = sp.simplify(P_sc / (G**2 * N**2 * w**3 * sig))
T_eff = 4 * sp.pi / (3 * sig)                         # 2 pi int C^2 / (int f)^4 for the top hat
print("P_total(photon pairs) = ", c_tot_ph, "* G^2 N^2 w^3 sigma   [=", float(c_tot_ph), "]")
print("P_total(scalar pairs) = ", c_tot_sc, "* G^2 N^2 w^3 sigma   [=", float(c_tot_sc), "]")
# B&O's 2 pi delta(0) -> T: int dK0 C(K0)^2 = (2 pi delta(0)/(2pi)) * ... -> 2 pi C^2 integral / (int f)^4 = T
Teff_check = sp.simplify(2 * sp.pi * intL2 / sig**4)
print("T_eff = 2 pi int L^2 dK0 / sigma^4 =", Teff_check)
c_rate_ph = sp.simplify(c_tot_ph * sig / (T_eff * sig))  # P/T_eff in units G^2 N^2 w^3 sigma^2
c_rate_ph = sp.simplify(P_ph / T_eff / (G**2 * N**2 * w**3 * sig**2))
c_rate_sc = sp.simplify(P_sc / T_eff / (G**2 * N**2 * w**3 * sig**2))
print("B&O 'rate' photon:", c_rate_ph, " target 3/(25 pi):", sp.simplify(c_rate_ph - 3 / (25 * sp.pi)) == 0)
print("B&O 'rate' scalar:", c_rate_sc, " target 7/(450 pi):", sp.simplify(c_rate_sc - 7 / (450 * sp.pi)) == 0)
print("tau_phi/tau = (3/25)/(7/450) =", sp.Rational(3, 25) / sp.Rational(7, 450))

print("\n=== Part 2: brute force with EXACT kinematics at finite sigma/omega (top hat, real sign) ===")


def brute(sig_over_w, final="photon", nK0=40, nK=80, na=40, nx=24):
    wv = 1.0
    sg = sig_over_w * wv
    Th2 = 2 * PI**2 * 1.0 / (wv * sg)   # N = 1
    lo, hi = wv - sg / 2, wv + sg / 2
    gK0, wK0 = np.polynomial.legendre.leggauss(nK0)
    gx, wx = np.polynomial.legendre.leggauss(nx)
    tot = 0.0
    for half in (0, 1):  # split K0 at 2w (kink of the triangle)
        a0, b0 = (2 * wv - sg, 2 * wv) if half == 0 else (2 * wv, 2 * wv + sg)
        K0s = 0.5 * (b0 - a0) * gK0 + 0.5 * (b0 + a0)
        wK0s = 0.5 * (b0 - a0) * wK0
        for K0, wk0 in zip(K0s, wK0s):
            gk, wkk = np.polynomial.legendre.leggauss(nK)
            Ks = 0.5 * K0 * (gk + 1)
            wKs = 0.5 * K0 * wkk
            for Km, wkm in zip(Ks, wKs):
                ss = K0**2 - Km**2
                beta = Km / K0
                gam = 1 / math.sqrt(1 - beta**2)
                # a range: band, K0-a in band, |2a-K0| <= K
                amin = max(lo, K0 - hi, 0.5 * (K0 - Km))
                amax = min(hi, K0 - lo, 0.5 * (K0 + Km))
                if amax <= amin:
                    continue
                ga, wa = np.polynomial.legendre.leggauss(na)
                aa = 0.5 * (amax - amin) * ga + 0.5 * (amax + amin)
                wa = 0.5 * (amax - amin) * wa
                cchi = np.clip((2 * aa / (gam * math.sqrt(ss)) - 1) / beta, -1, 1)
                schi2 = 1 - cchi**2
                # ring integral of (s/2)(1+cos^2Theta) [photon] or (s/2) sin^2 Theta [scalar], vs x = cos theta*
                X = gx[:, None]
                c2 = cchi[None, :]**2 * X**2 + schi2[None, :] * (1 - X**2) / 2   # <cos^2 Theta>_phi
                ring = 2 * PI * (ss / 2) * ((1 + c2) if final == "photon" else (1 - c2))
                Fint = (ring * wa[None, :]).sum(axis=1)               # int da (Theta^2 const) ring
                F = 0.5 * Th2 * 8 * PI * 1.0 / (16 * PI**2 * Km) * Fint   # G = 1
                angsum = 2 * PI * np.sum(wx * F**2)
                nconf = 2 if final == "photon" else 1
                tot += wk0 * wkm * 0.5 * nconf * 4 * PI * Km**2 / (2 * PI)**4 / (32 * PI**2) * angsum
    return tot / (wv**3 * sg)   # c_tot


for r in (0.1, 0.03, 0.01):
    cp = brute(r, "photon")
    cs = brute(r, "scalar")
    print(f"sigma/w = {r:5.2f}: c_tot photon = {cp:.6f} (narrow-band 4/25 = 0.16), scalar = {cs:.6f} "
          f"(14/675 = {14/675:.6f}); photon B&O-rate coeff c_tot*3/(4 pi) = {cp*3/(4*PI):.6f} "
          f"vs 3/(25pi) = {3/(25*PI):.6f}")
print("grid check (sigma/w=0.03, doubled nK, na):", brute(0.03, "photon", nK=160, na=80))

print("\n=== Part 3: profile independence -> Parseval scaling law P = (12 pi/25) G^2 w int L(t)^2 dt ===")
# narrow band: P = (3/(50 pi^4)) G^2 w^5 int C(K0)^2 dK0 (photon, real sign, isotropic) for ANY profile f(k)
# with N = (w/(4 pi^2)) int |f|^2 dk (both helicities in f) and L(t) = (w^2/(8 pi^3)) |g(t)|^2, g = int f e^{-iat} da
wv = 1.0
for prof in ("tophat", "gaussian"):
    sg = 0.01
    k = np.linspace(wv - 8 * sg, wv + 8 * sg, 4001)
    dk = k[1] - k[0]
    f = np.where(np.abs(k - wv) <= sg / 2, 1.0, 0.0) if prof == "tophat" else np.exp(-(k - wv)**2 / (2 * sg**2))
    Nn = wv / (4 * PI**2) * np.sum(f**2) * dk
    f = f / math.sqrt(Nn)                     # N = 1
    C = np.convolve(f, f) * dk
    intC2 = np.sum(C**2) * dk
    P_freq = 3 / (200 * PI**4) * wv**5 * intC2   # f here carries both helicities (f = sqrt2 Theta): C_f = 2 C_Theta
    t = np.linspace(-6000 / sg * 0.01, 6000 / sg * 0.01, 20001) if prof == "tophat" else np.linspace(-40 / sg, 40 / sg, 20001)
    t = np.linspace(-400 / sg, 400 / sg, 40001)
    g = np.array([np.sum(f * np.exp(-1j * (k - wv) * tt)) * dk for tt in t[::1]]) if False else None
    # FFT-free direct evaluation on a coarser time grid
    tt = np.linspace(-400 / sg, 400 / sg, 16001)
    ph = np.exp(-1j * np.outer(tt, k - wv))
    g = ph @ f * dk
    L = wv**2 / (8 * PI**3) * np.abs(g)**2
    E = np.sum(L) * (tt[1] - tt[0])
    P_time = 12 * PI / 25 * wv * np.sum(L**2) * (tt[1] - tt[0])
    print(f"{prof:8s}: E = N w = {E:.5f} (expect 1); P from int C^2 = {P_freq:.6e}; "
          f"P from (12pi/25) w int L^2 dt = {P_time:.6e}; ratio {P_time/P_freq:.4f}")
    if prof == "tophat":
        print(f"          top hat closed form (4/25) N^2 w^3 sigma = {4/25*wv**3*sg:.6e}")
    else:
        # Gaussian closed form: int C^2 = sqrt(2 pi) sigma^3 Theta^4 with N=1 -> Theta^2 = 4 pi^2/(w sqrt(pi) sigma)
        Th2g = 2 * PI**2 / (wv * math.sqrt(PI) * sg)
        print(f"          Gaussian closed form = {3/(50*PI**4)*wv**5*PI*math.sqrt(2*PI)*sg**3*Th2g**2:.6e}"
              f" = 6 sqrt(2 pi)/25 -> c_tot = {6*math.sqrt(2*PI)/25:.6f} G^2N^2w^3 sigma")

print("\n=== Part 4: incoherent isotropic bath (stochastic background), physical cross section ===")
import qft_second_order as q2  # noqa: E402
for sval in (1.0, 4.0):
    sRL = q2.sigma_total(sval, "R", "L", final="photon", G=1.0)
    sRR = q2.sigma_total(sval, "R", "R", final="photon", G=1.0)
    print(f"s = {sval}: toolkit sigma(RL->gg) = {sRL:.6f}, mine (4 pi/5) G^2 s = {4*PI/5*sval:.6f}; sigma(RR) = {sRR:.2e}")
# Gamma = (1/2) sum over helicity pairs int n1 n2 sigma v ; isotropic, unpolarised, arbitrary spectrum:
# sigma_avg = (2 pi/5) G^2 s, s = 2 w1 w2 (1-c), v = (1-c) -> <(1-c)^2> = 4/3
sym = sp.Rational(1, 2) * sp.Rational(2, 5) * sp.pi * 2 * sp.Rational(4, 3)
print("Gamma / (G^2 rho^2) =", sp.simplify(sym), " B&O eq.14: 8 pi/15 ->", sp.simplify(sym - 8 * sp.pi / 15) == 0)
# numeric check with a two-line spectrum: rho = n1 w1 + n2 w2; Gamma = (1/2) sum_ij n_i n_j <sigma v>_ij
n1, w1, n2, w2 = 3.0, 1.0, 0.5, 7.0
gam = 0.5 * sum(ni * nj * (2 * PI / 5) * 2 * wi * wj * (4 / 3) for ni, wi in ((n1, w1), (n2, w2)) for nj, wj in ((n1, w1), (n2, w2)))
print("two-line spectrum: Gamma/(G^2 rho^2) =", gam / (n1 * w1 + n2 * w2)**2, " = 8pi/15 =", 8 * PI / 15)

print("\n=== Part 5: eqs. 9-12 and hbar counting (symbolic) ===")
E, hb, c = sp.symbols("E hbar c", positive=True)
rate = sp.Rational(3, 25) / sp.pi * G**2 * N**2 * w**3 * sig**2
Ngam_t = 2 * rate
tau = sp.solve(sp.Eq(Ngam_t.subs(N, E / w) * sp.Symbol("t"), 1), sp.Symbol("t"))[0]
print("photon rate 2 dP/dt =", sp.simplify(Ngam_t), "; tau (one photon) =", sp.simplify(tau),
      " vs eq.10 25 pi/(6 G^2 E^2 w sigma^2):", sp.simplify(tau - 25 * sp.pi / (6 * G**2 * E**2 * w * sig**2)) == 0)
W = sp.simplify(w * Ngam_t.subs(N, E / w))
print("W_gamma = w * photon rate =", W, " vs eq.11 6 G^2 E^2 w^2 sigma^2/(25 pi):",
      sp.simplify(W - 6 * G**2 * E**2 * w**2 * sig**2 / (25 * sp.pi)) == 0)
rm, l = 2 * G * E / c**4, c / sig
W12 = sp.Rational(3, 50) / sp.pi * (rm / l)**2 * (hb * w)**2 / hb
print("eq.12 with explicit 1/hbar: (3/(50 pi))(r_m/l)^2 (hbar w)^2/hbar =", sp.simplify(W12),
      "-> power linear in hbar; pair NUMBER P = (4/25) G^2 E^2 w sigma / c^10 is hbar-free")
