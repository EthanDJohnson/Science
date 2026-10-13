#!/usr/bin/env python3
"""Idealizer lens: where is the pair yield of an OUTGOING wave generated?  Toy (scalar multipole) model.

Local kinetic rate density (incoherent, unpolarised, geometric optics), derived in the analysis:
    Gamma(x) = (1/2) sum_ij n_i n_j sigma_avg v = (2 pi/5) G^2 T_{mu nu} T^{mu nu}      (natural units)
because T^{mu nu} = sum_i n_i k_i^mu k_i^nu / w_i  =>  T_{mu nu}T^{mu nu} = sum_ij n_i n_j w_i w_j (1 - cos_ij)^2.
Checks: isotropic bath T = diag(rho, rho/3 x3) -> (2pi/5)(4/3) rho^2 = (8 pi/15) rho^2 = B&O eq. 14; single plane
wave: T null -> 0 (no-go).
Toy field: massless scalar multipole psi = h_l^(1)(kr) Y_lm(theta,phi) e^{-iwt} (outgoing), or j_l(kr) Y_lm
(standing = time-symmetric in+out, the analogue of a Pauli-Jordan field), cycle-averaged stress tensor <T>.
We compute f(x) = r^4 int dOmega <T>_{mu nu}<T>^{mu nu} / L^2 with L = r^2 int dOmega <T^{0r}> (outgoing flux;
for the standing wave we normalise to the flux of its outgoing half, |j| = |h|/2 asymptotically).
Packet of duration ell and luminosity L passing radius r: yield beyond r0,
    P(>r0) = (2 pi/5) G^2 ell int_{r0} dr int dOmega r^2 TT = (2 pi/5) G^2 ell L^2 w int_{x0} f(x)/x^2 dx,
compared with B&O's in-state total for the same packet, (12 pi/25) G^2 w L^2 ell  [calc lens-idealizer_coeff.py]:
    R(x0) = P(>r0)/P_BO = (5/6) int_{x0}^inf f(x)/x^2 dx.
Units: natural (w = k = 1, so x = kr = r/lambda-bar).  Scalar toy only: spin-2 changes O(1) factors, not powers.
"""
import math

import mpmath as mp
import numpy as np

mp.mp.dps = 30


def radial(l, x, kind):
    if kind == "out":
        return mp.spherical_jn(l, x) + 1j * mp.spherical_yn(l, x) if hasattr(mp, "spherical_jn") else None
    return None


def sph_j(l, x):
    return mp.sqrt(mp.pi / (2 * x)) * mp.besselj(l + mp.mpf(1) / 2, x)


def sph_y(l, x):
    return mp.sqrt(mp.pi / (2 * x)) * mp.bessely(l + mp.mpf(1) / 2, x)


def R_and_dR(l, x, kind):
    if kind == "out":
        R = sph_j(l, x) + 1j * sph_y(l, x)
        dR = mp.diff(lambda z: sph_j(l, z) + 1j * sph_y(l, z), x)
    else:
        R = sph_j(l, x)
        dR = mp.diff(lambda z: sph_j(l, z), x)
    return complex(R), complex(dR)


def Ylm_parts(l, m, th, ph):
    Y = complex(mp.spherohar(l, m, th, ph)) if hasattr(mp, "spherohar") else complex(mp.spherharm(l, m, th, ph))
    h = 1e-6
    f = lambda a, b: complex(mp.spherharm(l, m, a, b))
    dth = (f(th + h, ph) - f(th - h, ph)) / (2 * h)
    dph = 1j * m * Y
    return Y, dth, dph


def stress_TT(l, m, x, kind, nth=40, nph=16):
    """Return (int dOmega <T><T>, int dOmega <T^{0r}>) at radius x (k = w = 1), orthonormal frame (t,r,th,ph)."""
    R, dR = R_and_dR(l, x, kind)
    gth, wth = np.polynomial.legendre.leggauss(nth)
    TT = 0.0
    flux = 0.0
    eta = np.diag([1.0, -1.0, -1.0, -1.0])
    for c, wc in zip(gth, wth):
        th = math.acos(c)
        for ph in np.linspace(0, 2 * math.pi, nph, endpoint=False):
            Y, dth, dph = Ylm_parts(l, m, th, ph)
            # covariant derivatives of complex psi in orthonormal frame: d_t, d_r, (1/r)d_th, (1/(r sin))d_ph
            d = np.array([-1j * R * Y, dR * Y, R * dth / x, R * dph / (x * math.sin(th))])
            A = 0.5 * np.real(np.outer(d, np.conj(d)))           # <d_mu Phi d_nu Phi>, Phi = Re psi
            # lower-index frame components: d_mu with mu spatial in orthonormal basis are "lower" components;
            # T_{mu nu} = A_{mu nu} - (1/2) eta_{mu nu} eta^{ab} A_{ab}
            trace = np.sum(np.diag(eta) * np.diag(A))
            T = A - 0.5 * eta * trace
            Tup = eta @ T @ eta
            TT += wc * (2 * math.pi / nph) * float(np.sum(T * Tup))
            flux += wc * (2 * math.pi / nph) * float(-T[0, 1])   # T^{0r} = -T_{0r} with (+,-,-,-)
    return TT, flux * x**2   # L = r^2 int dOmega T^{0r}


if __name__ == "__main__":
    cases = [(2, 2, "out"), (2, 0, "out"), (2, 2, "stand")]
    xs = [1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0]
    store = {}
    for (l, m, kind) in cases:
        print(f"\n--- scalar l={l} m={m} {kind} ---")
        # flux normalisation: outgoing flux of the outgoing wave (x-independent); standing: use outgoing half = 1/4 of |h|^2 flux
        _, Lout = stress_TT(l, m, 50.0, "out")
        Lnorm = Lout if kind == "out" else Lout / 4.0
        fs = []
        for x in xs:
            TT, fl = stress_TT(l, m, x, kind)
            f = x**4 * TT / Lnorm**2
            fs.append(f)
            print(f"x = kr = {x:6.1f}: r^4 int TT dOmega / L^2 = f = {f: .4e}; flux/L = {fl/Lnorm: .4f}")
        fs = np.array(fs)
        sl = np.diff(np.log(np.abs(fs))) / np.diff(np.log(xs))
        print("local power-law slope d ln f / d ln x:", np.round(sl, 3))
        store[(l, m, kind)] = (np.array(xs), fs)
    print("\n--- cumulative yield beyond x0 relative to B&O in-state total, R(x0) = (5/6) int f/x^2 dx (outgoing) ---")
    for key in [(2, 2, "out"), (2, 0, "out"), (2, 2, "stand")]:
        xs_, fs_ = store[key]
        # fit the asymptotic power law f = A x^p from the last three points and integrate analytically beyond
        p, lnA = np.polyfit(np.log(xs_[-3:]), np.log(fs_[-3:]), 1)
        if key[2] == "stand":
            p, lnA = 0.0, math.log(float(np.mean(fs_[2:])))   # oscillates about a constant
        A = math.exp(lnA)
        print(f"{key}: asymptotic f ~ {A:.3e} x^{p:.3f}")
        for x0 in (1.0, 2 * math.pi, 1e2, 1e4, 4.7e5):
            Rx = (5 / 6) * A * x0**(p - 1) / (1 - p)   # = (5/6) int_{x0}^inf A x^(p-2) dx
            print(f"   x0 = {x0:9.3g}: R(x0) ~ {Rx:.3e}")
    print("\nstanding (time-symmetric) wave: f -> const means TT ~ L^2/r^4 (head-on in x out), "
          "outgoing: f falls as a power of x -> yield converges at x ~ 1 (near zone).")
