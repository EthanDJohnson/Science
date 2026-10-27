"""Side check for the citation angle: how to read Krasnikov's footnote 8 (gr-qc/0207057).

Krasnikov (PRD 67 104013, footnote 8) says Van Den Broeck's profile "violates the quantum
inequality (e. g. in w = 0.98)". The paper's own test uses one global sampling time
tau0 = 0.1 * r_c,min. A *local* test uses tau0(w) = 0.1 * r_c(w), r_c(w) = 1/sqrt(max |sectional
curvature at w|), which is stricter wherever the local curvature radius exceeds the global minimum.

This script asks: with the Planck-scale pocket (v1-v4: alpha=1e34, Delta=1e-32 m) and with the
femtometre pocket (v5: alpha=1e17, Delta=1e-15 m), what does the local test give, in particular
near w = 0.98? It is a reading aid for what Krasnikov may have meant; it is NOT a claim about
what Krasnikov computed.

Geometry (VdB 1999, region II, eqs 11-13, 19; n = 80): ds^2 = -dt^2 + B(r)^2 (dr^2 + r^2 dOmega^2),
w = (R~ + Delta - r)/Delta, r = Delta (2 - w) for R~ = Delta,
B = alpha(-(n-1) w^n + n w^(n-1)) + 1.
rho = (1/8pi)(B'^2/B^4 - 2B''/B^3 - 4B'/(r B^3))        [1/m^2, geometric units]
K_r,theta = B'^2/B^4 - B''/B^3 - B'/(r B^3)             [eq 19]
K_theta,phi = -B'(r B' + 2B)/(r B^4)                    [other sectional curvature]
QI (Ford-Roman, as used by VdB): rho >= -3 hbar/(32 pi^2 c tau0^4)  [SI, tau0 a length]

Run: python3 checks/2026-10-27-prior-art/calc/vdb_local_qi_krasnikov.py
"""
import mpmath as mp

mp.mp.dps = 60
G, c, hbar = mp.mpf("6.6743e-11"), mp.mpf("2.99792458e8"), mp.mpf("1.054571817e-34")
LP = mp.sqrt(hbar * G / c**3)
KGM = c**2 / G
n = 80


def profile(alpha, Dt, w):
    r = Dt * (2 - w)
    B = alpha * (-(n - 1) * w**n + n * w ** (n - 1)) + 1
    Bw = alpha * n * (n - 1) * w ** (n - 2) * (1 - w)
    Bww = alpha * n * (n - 1) * ((n - 2) * w ** (n - 3) * (1 - w) - w ** (n - 2))
    Bp = -Bw / Dt            # dB/dr
    Bpp = Bww / Dt**2        # d2B/dr2
    rho = (Bp**2 / B**4 - 2 * Bpp / B**3 - 4 * Bp / (r * B**3)) / (8 * mp.pi)
    K1 = Bp**2 / B**4 - Bpp / B**3 - Bp / (r * B**3)
    K2 = -Bp * (r * Bp + 2 * B) / (r * B**4)
    return rho, K1, K2


def qi_bound(tau0):
    return 3 * hbar / (32 * mp.pi**2 * c * tau0**4)  # kg/m^3 (magnitude)


def run(label, alpha, Dt):
    print("=" * 78)
    print(f"{label}: alpha={mp.nstr(alpha,3)}, Delta~={mp.nstr(Dt,3)} m = {mp.nstr(Dt/LP,4)} L_P")
    N = 6000
    ws = [mp.mpf(i) / N for i in range(1, N)]
    rows = []
    for w in ws:
        rho, K1, K2 = profile(alpha, Dt, w)
        K = max(abs(K1), abs(K2))
        rc = 1 / mp.sqrt(K) if K > 0 else mp.inf
        rows.append((w, rho * KGM, rc))
    # global r_c,min over the scan
    rc_min = min(r_[2] for r_ in rows)
    wmin = [r_[0] for r_ in rows if r_[2] == rc_min][0]
    # global test
    neg = [(w, rhoSI) for (w, rhoSI, rc) in rows if rhoSI < 0]
    wpk, rpk = min(neg, key=lambda t: t[1])
    bound_g = qi_bound(mp.mpf("0.1") * rc_min)
    print(f"  GLOBAL test: r_c,min = {mp.nstr(rc_min,4)} m (at w={mp.nstr(wmin,4)}) = Delta/{mp.nstr(Dt/rc_min,4)}; "
          f"peak rho = {mp.nstr(rpk,4)} kg/m^3 at w={mp.nstr(wpk,4)}; bound = -{mp.nstr(bound_g,4)}; "
          f"|rho|/|bound| = {mp.nstr(-rpk/bound_g,4)}")
    # local test
    best = None
    for (w, rhoSI, rc) in rows:
        if rhoSI < 0:
            ratio = -rhoSI / qi_bound(mp.mpf("0.1") * rc)
            if best is None or ratio > best[1]:
                best = (w, ratio, rhoSI, rc)
    print(f"  LOCAL test (tau0 = 0.1 r_c(w)): max |rho|/|bound(w)| = {mp.nstr(best[1],4)} at w={mp.nstr(best[0],4)} "
          f"(rho={mp.nstr(best[2],4)}, r_c(w)={mp.nstr(best[3],4)} m)")
    for wq in ("0.2", "0.349", "0.5", "0.576", "0.9", "0.95", "0.98", "0.981"):
        w = mp.mpf(wq)
        rho, K1, K2 = profile(alpha, Dt, w)
        K = max(abs(K1), abs(K2))
        rc = 1 / mp.sqrt(K)
        rhoSI = rho * KGM
        if rhoSI < 0:
            ratio = -rhoSI / qi_bound(mp.mpf("0.1") * rc)
            print(f"    w={wq}: rho={mp.nstr(rhoSI,4)} kg/m^3, r_c(w)={mp.nstr(rc,4)} m, local |rho|/|bound| = {mp.nstr(ratio,4)}")
        else:
            print(f"    w={wq}: rho={mp.nstr(rhoSI,4)} kg/m^3 (>=0), r_c(w)={mp.nstr(rc,4)} m")


run("v1-v4 Planck-scale pocket", mp.mpf("1e34"), mp.mpf("1e-32"))
run("v5 femtometre pocket", mp.mpf("1e17"), mp.mpf("1e-15"))
