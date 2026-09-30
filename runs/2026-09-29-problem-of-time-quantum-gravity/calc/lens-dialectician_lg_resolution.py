#!/usr/bin/env python3
"""Dialectician, synthesis I+II prediction: Leggett-Garg violation from relational (record-based) two-time
correlations as a function of the clock's reading error.

Units: natural units hbar = 1; Omega in rad/s, times and sigma in s. Model: qubit precessing at Omega
(H_S = Omega sigma_x / 2, observable Q = sigma_z), so the ideal two-time correlator is C(tau) = cos(Omega tau).
Each clock reading carries an independent Gaussian error sigma, so the time difference has variance 2 sigma^2
and C -> cos(Omega tau) exp(-Omega^2 sigma^2). K3 = C12 + C23 - C13 with equal spacings tau.
Checks by Monte-Carlo averaging over clock errors, and gives the threshold Omega*sigma where K3max = 1.
"""
import math
import random

def K3_exact(x, s):            # x = Omega*tau, s = Omega*sigma
    f = math.exp(-s * s)
    return f * (2 * math.cos(x) - math.cos(2 * x))

def K3_mc(x, s, n=200000, seed=1):
    rng = random.Random(seed)
    acc = 0.0
    for _ in range(n):
        e1, e2, e3 = (rng.gauss(0, s) for _ in range(3))
        t1, t2, t3 = 0 + e1, x + e2, 2 * x + e3      # actual elapsed phases given nominal readings
        acc += math.cos(t2 - t1) + math.cos(t3 - t2) - math.cos(t3 - t1)
    return acc / n

x = math.pi / 3
print("Omega*tau = pi/3 (ideal optimum, K3 = 1.5)")
for s in [0.0, 0.2, 0.4, 0.6, 0.637, 0.8]:
    print(f"  Omega*sigma = {s:.3f} | K3 exact = {K3_exact(x, s):.4f} | K3 Monte Carlo = {K3_mc(x, s):.4f}")
print(f"threshold Omega*sigma where max K3 = 1: sqrt(ln 1.5) = {math.sqrt(math.log(1.5)):.4f}")
# Illustration in SI: optical-frequency qubit read by a clock with GPP accuracy after T = 1 s
tP = 5.39e-44
w = 2 * math.pi * 429e12
dT = tP * (1.0 / tP) ** (1 / 3)
print(f"GPP clock accuracy at T = 1 s: {dT:.3e} s; Omega*sigma for Omega = 2 pi 429 THz: {w*dT:.3e} (far below threshold)")
