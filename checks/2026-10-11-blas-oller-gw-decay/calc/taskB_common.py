#!/usr/bin/env python3
"""Task B shared helpers: position-space free fields of narrow-band spherical (l = 0) and quadrupole-pattern (l = 2, m = 0)
coherent states, built exactly as in B&O eq. 3/5 (a superposition of ON-SHELL plane waves = the Pauli-Jordan / radiation
field, regular everywhere), plus the outgoing (retarded) multipole fields used for the physical comparison.

Conventions (scalar proxy for each graviton polarisation component; hbar = c = 1, units w_s = 1 unless stated):
    psi(x) = int d3k/((2pi)^3 2k) f(|k|) Y_lm(k^) exp(-i k t + i k.x)       (positive-frequency part, B&O eq. 2-3 measure)
           = (i^l/(4 pi^2)) [int dk k f(k) j_l(k r) exp(-i k t)] Y_lm(x^)  =: R_l(r, t) Y_lm(x^)
    For l = 0 we use the isotropic profile WITHOUT the Y_00 factor (B&O's f_s), i.e. psi = (1/(4pi^2)) int dk k f j_0 e^{-ikt}.
    Mean graviton number: N = int d3k/((2pi)^3 2k) |f|^2 |Y|^2  = (1/(16 pi^3)) int dk k |f|^2   (l with Y_lm)
                                                               = (1/(4 pi^2))  int dk k |f|^2   (isotropic l = 0).
    j_l(kr) = [h_l^(1)(kr) + h_l^(2)(kr)]/2 splits psi EXACTLY into an incoming (e^{-ik(r+t)}) and an outgoing
    (e^{+ik(r-t)}) spherical wave; D_n(u) = int dk f(k) k^{-n} e^{iku} carries all k-integrals.
Profiles: 'gauss'  f = exp(-(k-w)^2/(2 sig^2));  'tophat' f = 1 on [w - sig/2, w + sig/2] (B&O's top hat, Theta = 1).
"""
from __future__ import annotations

import math

import numpy as np
from scipy.special import exp1

PI = math.pi


class Band:
    """Narrow-band radial profile f(k) and D_n(u) = int dk f(k) k^-n e^{iku} (n = 0, 1, 2).

    tophat: closed forms (D_0 elementary, D_1 = E1(-iau) - E1(-ibu), D_2 by parts), exact for every u.
    gauss : D_0 closed form (k-range extended to -inf, error ~ exp(-w^2/2sig^2)); D_1, D_2 from a k-quadrature table on
            |u| <= 16/sig (outside, |D_n| < exp(-128) relative: set to 0)."""

    def __init__(self, profile: str = "gauss", w: float = 1.0, sig: float = 0.1, nk: int = 801):
        self.profile, self.w, self.sig = profile, w, sig
        if profile == "tophat":
            self.a, self.b = w - 0.5 * sig, w + 0.5 * sig
            x, wx = np.polynomial.legendre.leggauss(400)
            self.k, self._wk = w + 0.5 * sig * x, 0.5 * sig * wx
            self.f = np.ones_like(self.k)
        elif profile == "gauss":
            k = np.linspace(w - 9 * sig, w + 9 * sig, nk)
            wk = np.full_like(k, k[1] - k[0])
            wk[0] *= 0.5
            wk[-1] *= 0.5
            self.k, self._wk, self.f = k, wk, np.exp(-(k - w) ** 2 / (2 * sig * sig))
            self.umax = 16.0 / sig
            self.u = np.linspace(-self.umax, self.umax, 20001)
            self.E = [None]
            for n in (1, 2):
                g = self._wk * self.f * self.k ** (-n)
                En = np.empty(self.u.size, complex)
                for i in range(0, self.u.size, 2000):
                    uu = self.u[i:i + 2000]
                    En[i:i + 2000] = np.exp(1j * np.outer(uu, self.k - w)) @ g
                self.E.append(En)
        else:
            raise ValueError(profile)

    def D(self, n: int, u):
        u = np.asarray(u, float)
        w = self.w
        if self.profile == "gauss":
            if n == 0:
                return math.sqrt(2 * PI) * self.sig * np.exp(1j * w * u - 0.5 * (self.sig * u) ** 2)
            inside = np.abs(u) <= self.umax
            uc = np.clip(u, -self.umax, self.umax)
            re = np.interp(uc, self.u, self.E[n].real)
            im = np.interp(uc, self.u, self.E[n].imag)
            return np.where(inside, np.exp(1j * w * u) * (re + 1j * im), 0.0)
        a, b = self.a, self.b
        small = np.abs(u) < 1e-9
        us = np.where(small, 1.0, u)
        if n == 0:
            val = (np.exp(1j * b * us) - np.exp(1j * a * us)) / (1j * us)
            return np.where(small, b - a, val)
        D1 = exp1(-1j * a * us) - exp1(-1j * b * us)
        D1 = np.where(small, math.log(b / a), D1)
        if n == 1:
            return D1
        val = np.exp(1j * a * us) / a - np.exp(1j * b * us) / b + 1j * us * D1
        return np.where(small, 1.0 / a - 1.0 / b, val)

    def number_iso(self) -> float:
        """N for the isotropic l = 0 state (B&O normalisation, f = this profile, no Y_00)."""
        return float(np.sum(self._wk * self.k * self.f ** 2)) / (4 * PI * PI)

    def number_lm(self) -> float:
        """N for f(k) Y_lm(k^)."""
        return float(np.sum(self._wk * self.k * self.f ** 2)) / (16 * PI ** 3)


def radial_free(band: Band, l: int, r, t, part: str = "all"):
    """R_l(r,t) such that psi = R_l Y_lm (l = 2) or psi = R_0 (isotropic l = 0, no Y_00).

    part = 'all' (regular Pauli-Jordan field), 'out' (outgoing e^{ik(r-t)} terms), 'in' (incoming e^{-ik(r+t)} terms).
    'out' alone is the field of a point multipole source radiating with the same spectrum (singular at r = 0)."""
    r = np.asarray(r, float)
    t = np.asarray(t, float)
    um, up = r - t, -r - t
    if l == 0:
        out = band.D(0, um) / (8j * PI * PI * r)
        inn = -band.D(0, up) / (8j * PI * PI * r)
    elif l == 2:
        pref = -(1.0 / (4 * PI * PI)) * 0.5j       # i^2/(4 pi^2) * (i/2)
        out = pref * (band.D(0, um) / r + 3j * band.D(1, um) / r ** 2 - 3 * band.D(2, um) / r ** 3)
        inn = pref * (-band.D(0, up) / r + 3j * band.D(1, up) / r ** 2 + 3 * band.D(2, up) / r ** 3)
    else:
        raise ValueError("l must be 0 or 2")
    if part == "out":
        return out
    if part == "in":
        return inn
    return out + inn


def radial_direct(band: Band, l: int, r: float, t: float) -> complex:
    """Direct k-quadrature of R_l (validation of radial_free)."""
    from scipy.special import spherical_jn
    k, f, wk = band.k, band.f, band._wk
    val = np.sum(wk * k * f * spherical_jn(l, k * r) * np.exp(-1j * k * t))
    return (1j ** l) * val / (4 * PI * PI)


def gaunt_Y20sq():
    """c_L = int Y_20^2 Y_L0 dOmega for L = 0, 2, 4 (Y_20^2 = sum_L c_L Y_L0)."""
    from scipy.special import eval_legendre
    x, wx = np.polynomial.legendre.leggauss(40)
    Y = lambda L: np.sqrt((2 * L + 1) / (4 * PI)) * eval_legendre(L, x)
    return {L: float(2 * PI * np.sum(wx * Y(2) ** 2 * Y(L))) for L in (0, 2, 4)}
