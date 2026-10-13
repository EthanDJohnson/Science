#!/usr/bin/env python3
"""Task C(1): B&O eq. S6 WITHOUT the step '2 pi delta(0) -> T'.  Exact in-out total P_tot of the top-hat coherent state,
its time profile, and what B&O's dP/dt (eq. 8) is relative to it.

Model = B&O's own (eq. 7 kernel, top-hat f = Theta on both helicities, Theta^2 = 2 pi^2 N/(w sig), real Theta):
    A_{mu mu}(q1,q2) = (1/2) int dk1~ dk2~ f(k1) f(k2) 8 pi G h (2pi)^4 delta^4(k1+k2-q1-q2),  h = (t^2+u^2)/s,
    dk~ = d^3k/((2pi)^3 2|k|),  P = (1/2) sum_{mu = +-} int dq1~ dq2~ |A_{mu mu}|^2   (1/2: identical photons).
Squaring gives TWO four-momentum deltas, delta^4(k1+k2-q) delta^4(k1'+k2'-q) = delta^4(k1+k2-q) delta^3(K-K') delta(E-E'),
E = |k1|+|k2|, E' = |k1'|+|k2'|.  The pairs (k1,k2) and (k1',k2') are DIFFERENT; delta(E-E') is a constraint on them, not
delta(0).  Exactly (no narrow-band approximation, exact 1/(2|k|) factors):

    P_tot = C0 int d^3K int dOmega_gam  2 pi int dE  H(E;K,Omega)^2 ,                                  C0 = G^2/(16384 pi^9)
    H(E;K,Omega) = int d^3k delta(E(k)-E) Theta^2 h/(|k1||k2|)  (k = relative momentum, k1,2 = K/2 -+ k).

For fixed K the shell pair is parameterised EXACTLY by a=|k1|, b=|k2|, azimuth alpha: d^3k = (a b/K) da db dalpha, and in the
pair CM frame the graviton axis has cos(theta_g*) = (a-b)/K exactly (derived below, checked numerically in (c0)).  With
h = (s/2)(1 + (n_g*.n_gam*)^2), s = E^2-K^2, the alpha and D = a-b integrals are analytic:
    H = p(E) + q(E) u^2  (u = cos of the photon CM polar angle about K),
    p = c (3 Dm - Dm^3/(3K^2)),  q = c (Dm^3/K^2 - Dm),  c = Theta^2 pi s/(2K),  Dm = min(sig - |E - 2w|, K).
B&O's replacement 2 pi delta(E-E') -> T (then /T) turns 2 pi int dE H^2 into (int dE H)^2:
    (dP/dt)_BO = R(0),  R(t) = C0 int d^3K dOmega |int dE H(E) e^{iEt}|^2,  int R(t) dt = P_tot (Parseval).
So eq. 8 is the value at t = 0 (all pair phases aligned: the focus of the free packet) of a time density whose integral is the
finite total.  Quantity: P_tot = in-out mean number of photon PAIRS over the whole history of the free packet
(t: -inf..+inf) at O(G^2); photons = 2 P_tot.  Units: w = 1, G = 1, N = 1; coefficients quoted as P_tot/(G^2N^2w^3 sig) and
R(0)/(G^2 N^2 w^3 sig^2).
"""
import math

import mpmath as mp
import numpy as np
import sympy as sp
from scipy import integrate, special

PI = math.pi
W = 1.0
C0 = 1.0 / (16384 * PI ** 9)
XG, WG = np.polynomial.legendre.leggauss(48)


def gl(a, b, n=None):
    if n is None:
        x, w = XG, WG
    else:
        x, w = np.polynomial.legendre.leggauss(n)
    return 0.5 * (b - a) * x + 0.5 * (b + a), 0.5 * (b - a) * w


def pq(E, K, sig, Theta2):
    s = E * E - K * K
    Dm = np.minimum(sig - np.abs(E - 2 * W), K)
    Dm = np.clip(Dm, 0.0, None)
    c = Theta2 * PI * s / (2 * K)
    p = c * (3 * Dm - Dm ** 3 / (3 * K * K))
    q = c * (Dm ** 3 / (K * K) - Dm)
    return p, q


def e_nodes(K, sig, n):
    lo = max(2 * W - sig, K)
    hi = 2 * W + sig
    pts = [lo, hi, 2 * W]
    if K < sig:
        pts += [2 * W - (sig - K), 2 * W + (sig - K)]
    pts = sorted(set(x for x in pts if lo <= x <= hi))
    xs, ws = [], []
    for a, b in zip(pts[:-1], pts[1:]):
        if b - a > 1e-15:
            x, w = gl(a, b, n)
            xs.append(x)
            ws.append(w)
    return np.concatenate(xs), np.concatenate(ws)


def k_nodes(sig, n):
    pts = sorted(set([1e-12, sig, 2 * W - sig, 2 * W, 2 * W + sig, 0.5 * sig, 2 * W - 0.5 * sig]))
    pts = [p for p in pts if 0 <= p <= 2 * W + sig]
    xs, ws = [], []
    for a, b in zip(pts[:-1], pts[1:]):
        x, w = gl(a, b, n)
        xs.append(x)
        ws.append(w)
    return np.concatenate(xs), np.concatenate(ws)


def exact_coeffs(sig, nK=48, nE=48, tlist=()):
    Theta2 = 2 * PI ** 2 / (W * sig)
    Ks, wK = k_nodes(sig, nK)
    Ptot = 0.0
    R0 = 0.0
    Rt = np.zeros(len(tlist))
    tl = np.asarray(tlist, dtype=float)
    for K, wk in zip(Ks, wK):
        Es, wE = e_nodes(K, sig, nE)
        p, q = pq(Es, K, sig, Theta2)
        Ptot += wk * K * K * np.sum(wE * (2 * p * p + 4 * p * q / 3 + 2 * q * q / 5))
        P0, Q0 = np.sum(wE * p), np.sum(wE * q)
        R0 += wk * K * K * (2 * P0 * P0 + 4 * P0 * Q0 / 3 + 2 * Q0 * Q0 / 5)
        if len(tl):
            ph = np.exp(1j * np.outer(tl, Es - 2 * W))
            Pt = ph @ (wE * p)
            Qt = ph @ (wE * q)
            Rt += wk * K * K * (2 * np.abs(Pt) ** 2 + 4 * np.real(Pt * np.conj(Qt)) / 3 + 2 * np.abs(Qt) ** 2 / 5)
    Ptot *= C0 * 4 * PI * 2 * PI * 2 * PI
    R0 *= C0 * 4 * PI * 2 * PI
    Rt *= C0 * 4 * PI * 2 * PI
    return Ptot, R0, Rt


if __name__ == "__main__":
    print("=" * 110)
    print("(a) narrow-band limit, symbolic (sympy): radial-offset integral with and without the delta(0) -> T step")
    print("=" * 110)
    x, sg, t = sp.symbols("x sigma t", positive=True)
    # band offsets d1,d2,d1',d2' each uniform on [-sg/2, sg/2]; for fixed E = 2w + x the D-range has length 2 (sg - |x|)
    exactE = 2 * sp.integrate((sg - x) ** 2, (x, 0, sg))            # int dx Dm(x)^2 = int (sg-|x|)^2 dx
    replaced = sp.integrate(sg - x, (x, 0, sg)) * 2                  # int dx Dm(x)  (squared below)
    print(f"   int dE Dm(E)^2 = {sp.simplify(exactE)}  ;  (int dE Dm(E))^2 = {sp.simplify(replaced**2)}")
    Teff = sp.simplify(2 * sp.pi * exactE / replaced ** 2)
    print(f"   P_tot / (dP/dt)_BO = 2 pi int Dm^2 / (int Dm)^2 = {Teff}   (= {float(Teff.subs(sg, 1)):.6f}/sigma)")
    # the same from the time profile: int dE Dm e^{iEt} -> sg^2 sinc^2(sg t/2) e^{2iwt}, so R(t)/R(0) = sinc^4(sg t/2)
    y = sp.symbols("y", real=True)
    prof = sp.integrate((sg - y) * sp.cos(y * t), (y, 0, sg)) * 2
    print(f"   int dE Dm e^(iEt) e^(-2iwt) = {sp.simplify(prof)}  (= sg^2 sinc^2(sg t/2))")
    I4 = sp.integrate((sp.sin(y) / y) ** 4, (y, -sp.oo, sp.oo))
    print(f"   int sinc^4(x) dx = {I4}  -> int R dt / R(0) = (2/sigma) x {I4} = {sp.simplify(2*I4)}/sigma")
    # B&O eq. 8 from S6 in this limit (h = (s/2)(1+sin^2 th_gam cos^2), graviton axis perpendicular to K)
    K, N, G, w = sp.symbols("K N G omega", positive=True)
    Th2 = 2 * sp.pi ** 2 * N / (w * sg)
    s = 4 * w ** 2 - K ** 2
    ang = sp.integrate(((3 - y ** 2) / 2) ** 2, (y, -1, 1))          # int du (1 + sin^2/2)^2
    R0sym = (G ** 2 / (16384 * sp.pi ** 9 * w ** 4)) * Th2 ** 2 * (w * sg) ** 4 * sp.pi ** 2 * 4 * sp.pi * 2 * sp.pi \
        * sp.integrate(s ** 2, (K, 0, 2 * w)) * ang
    # int d^3k F = (w^2 sg^2/K) Theta^2 pi s (1 + sin^2/2): ring volume (a b/K) sg^2 with a b -> w^2; the K^2 of d^3K cancels 1/K^2
    R0c = sp.nsimplify(sp.simplify(R0sym / (G ** 2 * N ** 2 * w ** 3 * sg ** 2)))
    print(f"   R(0) = (dP/dt)_BO = {R0c} G^2 N^2 w^3 sig^2   (B&O eq. 8: 3/(25 pi) = {3/(25*PI):.8f})")
    Pc = sp.nsimplify(R0c * 4 * sp.pi / 3)
    print(f"   P_tot = R(0) x 4 pi/(3 sig) = {Pc} G^2 N^2 w^3 sig = {float(Pc):.6f} G^2 N^2 w^3 sig   [pairs; photons x2]")

    print("\n" + "=" * 110)
    print("(b) 'duration' conventions: P_tot vs (dP/dt)_BO x T")
    print("=" * 110)
    teff = 4 * PI / 3
    fwhm_R = 4 * float(mp.findroot(lambda z: (mp.sin(z) / z) ** 4 - 0.5, 1.0))
    fwhm_I = 4 * float(mp.findroot(lambda z: (mp.sin(z) / z) ** 2 - 0.5, 1.4))
    print(f"   T_eff = P_tot/(dP/dt)_BO = 4 pi/(3 sig) = {teff:.5f}/sig")
    for name, T in [("B&O 'T ~ 1/sigma'", 1.0), ("FWHM of R(t) = R(0) sinc^4(sig t/2)", fwhm_R),
                    ("equivalent width of the field intensity sinc^2(sig u/2) at a point = 2 pi/sig", 2 * PI),
                    ("FWHM of the field intensity sinc^2(sig u/2)", fwhm_I)]:
        print(f"   T = {T:7.4f}/sig ({name}):  P_tot / [(dP/dt)_BO x T] = {teff/T:.4f}")

    print("\n" + "=" * 110)
    print("(c0) kinematic identity used: cos(theta_g*) = (a-b)/K for the CM direction of k1 (random check)")
    print("=" * 110)
    rng = np.random.default_rng(3)
    worst = 0.0
    for _ in range(2000):
        k1 = rng.normal(size=3)
        k2 = rng.normal(size=3)
        a, b = np.linalg.norm(k1), np.linalg.norm(k2)
        Kv = k1 + k2
        Kn = np.linalg.norm(Kv)
        E = a + b
        beta = Kn / E
        gam = 1 / math.sqrt(1 - beta ** 2)
        kpar = k1 @ Kv / Kn
        kpar_s = gam * (kpar - beta * a)
        e_s = gam * (a - beta * kpar)
        worst = max(worst, abs(kpar_s / e_s - (a - b) / Kn))
    print(f"   max |cos(theta_g*) - (a-b)/K| over 2000 random pairs = {worst:.2e}")

    print("\n" + "=" * 110)
    print("(c) exact-kinematics quadrature (B&O kernel, exact 1/(2|k|) factors, exact ring Jacobian), sig -> 0")
    print("    columns: R(0)/(G^2N^2w^3sig^2) [B&O eq.8: 3/(25pi) = 0.0381972]   P_tot/(G^2N^2w^3sig) [-> 4/25]   sig P_tot/R(0) [-> 4pi/3]")
    print("=" * 110)
    for sig in (0.4, 0.2, 0.1, 0.05, 0.02, 0.01):
        Pt, R0, _ = exact_coeffs(sig)
        Pt2, R02, _ = exact_coeffs(sig, nK=72, nE=72)
        print(f"   sig/w = {sig:5.3f}:  R(0) coeff = {R0/sig**2:.7f}   P_tot coeff = {Pt/sig:.7f}   "
              f"sig P_tot/R(0) = {sig*Pt/R0:.5f}   (finer grid: {R02/sig**2:.7f}, {Pt2/sig:.7f})")

    print("\n" + "=" * 110)
    print("(d) time profile R(t)/R(0) at sig/w = 0.1 (exact kinematics) vs sinc^4(sig t/2); Parseval int R dt vs P_tot")
    print("=" * 110)
    sig = 0.1
    tt = np.array([0.0, 5.0, 10.0, 15.0, 20.0, 30.0, 40.0, 60.0])
    Pt, R0, Rt = exact_coeffs(sig, tlist=tt)
    for ti, ri in zip(tt, Rt):
        z = sig * ti / 2
        sinc4 = 1.0 if z == 0 else (math.sin(z) / z) ** 4
        print(f"   sig t = {sig*ti:5.2f}:  R(t)/R(0) = {ri/R0:.5f}   sinc^4(sig t/2) = {sinc4:.5f}")
    Tm = 300.0                                     # sig Tm = 30; GL nodes per E-piece must resolve exp(i (E-2w) t)
    tg = np.linspace(-Tm, Tm, 6001)
    _, _, Rg = exact_coeffs(sig, nK=32, nE=120, tlist=tg)
    intR = np.trapezoid(Rg, tg)
    tail = R0 * 4 / (sig ** 4 * Tm ** 3)           # both sinc^4 tails beyond |t| = Tm: 2 x 16 (3/8)/(3 sig^4 Tm^3)
    print(f"   int_(-{Tm:.0f})^({Tm:.0f}) R dt = {intR:.6e} (+ sinc^4 tails ~{tail:.1e});  P_tot = {Pt:.6e};  "
          f"ratio (with tails) = {(intR+tail)/Pt:.5f}")

    print("\n" + "=" * 110)
    print("(e) B&O's ORIGINAL profile f ~ exp(-(k-w)^2/(2 sig^2)) (narrow band), same N: dP/dt and P_tot")
    print("=" * 110)
    z = sp.symbols("z", real=True)
    Thg2_over_Th2 = 1 / sp.sqrt(sp.pi)                                # N fixed: Theta_g^2 sqrt(pi) sig = Theta^2 sig
    g_th_int = sp.integrate(2 * (1 - z), (z, 0, 1)) * 2              # int dx 2(sig-|x|), sig = 1
    g_g_int = sp.integrate(sp.exp(-z ** 2 / 4) * 2 * sp.sqrt(sp.pi), (z, -sp.oo, sp.oo))
    g_th_sq = sp.integrate((2 * (1 - z)) ** 2, (z, 0, 1)) * 2
    g_g_sq = sp.integrate((sp.exp(-z ** 2 / 4) * 2 * sp.sqrt(sp.pi)) ** 2, (z, -sp.oo, sp.oo))
    rR0 = sp.simplify((Thg2_over_Th2 * g_g_int / g_th_int) ** 2)
    rP = sp.simplify(Thg2_over_Th2 ** 2 * g_g_sq / g_th_sq)
    R0g = sp.Rational(3, 25) / sp.pi * rR0
    Pg = sp.Rational(4, 25) * rP
    print(f"   Gaussian/top-hat at equal N and equal sig parameter: R(0) ratio = {rR0}, P_tot ratio = {rP} = {float(rP):.4f}")
    print(f"   Gaussian: dP/dt|_peak = {sp.nsimplify(R0g)} G^2N^2w^3sig^2 = {float(R0g):.5f};  P_tot = {sp.simplify(Pg)} G^2N^2w^3sig "
          f"= {float(Pg):.5f};  T_eff = {sp.simplify(Pg/R0g)}/sig = {float(Pg/R0g):.5f}/sig")
    # at equal rms bandwidth Delta of |f|^2: top hat sig = sqrt(12) Delta, Gaussian sig = sqrt(2) Delta
    print(f"   at equal rms bandwidth Delta of |f|^2:  P_tot(top hat) = {0.16*math.sqrt(12):.4f} G^2N^2w^3 Delta, "
          f"P_tot(Gauss) = {float(Pg)*math.sqrt(2):.4f} G^2N^2w^3 Delta")

    print("\n" + "=" * 110)
    print("(f) same |f| (same N, same band) but a quadratic phase spreading the packet over duration D (chirp):")
    print("    f = Theta exp(i (k-w)^2 D/(2 sig)), group delay spans [-D/2, D/2].  Narrow band: H ~ int dy exp(i y^2 D/(4 sig))")
    print("=" * 110)

    def inner_abs2(Y, c):
        # |int_{-Y}^{Y} e^{i c y^2} dy|^2 via Fresnel integrals
        if c == 0:
            return (2 * Y) ** 2
        zz = Y * math.sqrt(2 * c / PI)
        S, Cf = special.fresnel(zz)
        return 4 * (PI / (2 * c)) * (Cf ** 2 + S ** 2)

    for sD in (0.0, 2 * PI, 20.0, 50.0, 100.0, 300.0, 1000.0, 3000.0):
        c = sD / 4.0   # sig = 1
        num, _ = integrate.quad(lambda xx: inner_abs2(1 - xx, c), 0, 1, limit=400, epsabs=0, epsrel=1e-10)
        num *= 2
        ratio = num / (8.0 / 3.0)
        asym = 3 * PI / sD if sD > 0 else float("nan")
        # time-averaged rate over D: P_tot(chirp)/D;  eq.8 / that = R(0) D / (R(0) (4pi/3sig) ratio) = 3 sig D/(4 pi ratio)
        e8 = 3 * sD / (4 * PI * ratio) if sD > 0 else float("nan")
        print(f"   sig D = {sD:7.1f}:  P_tot(chirp)/P_tot(transform-limited) = {ratio:.5f}   asymptote 3pi/(sig D) = {asym:.5f}"
              f"   eq.8 / [P_tot(chirp)/D] = {e8:9.3f}   (sig D)^2/(4 pi^2) = {sD**2/(4*PI**2):9.3f}")
