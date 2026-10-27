#!/usr/bin/env python3
"""fuchs_table1_check.py - which shift does Fuchs et al. Table 1 (7.6 ns) correspond to?

Fuchs et al. 2024 (arXiv:2405.02709) Sec. 5.1 / Table 1 give a co-minus-counter light-timing
difference dt for 'Warp Shell' = 7.6 ns, 'Alcubierre R = 15 m' = 8.0 ns, with the Table caption
'for v_warp = 0.04 c'. Sec. 4.1 says the energy-condition-checked shell has beta_warp = 0.02.

This script (run from the project root; no cd):
  1. Alcubierre top-hat, R = 15 m, v = 0.04: axis light-time difference (checks the convention:
     the paper's 8.0 ns should be reproduced by (-x) - (+x) one-way difference across the bubble).
  2. Warp Shell rebuild (warp_shell.py) at beta_warp = 0.02 and 0.04 for several smoothing spans
     span_P (the paper does not print its spans), same axis light-time difference.
Nothing here is the paper's own number except where labelled 'paper'.
"""
import sys

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from warp_shell import build_shell  # noqa: E402

C = 299792458.0
M, R1, R2 = 4.49e27, 10.0, 20.0


def light_time(shell, L=300.0, n=120001):
    x = np.linspace(-L, L, n)
    g = shell.metric_cartesian(0.0, x, np.zeros_like(x), np.zeros_like(x))
    g00, g0x, gxx = g[:, 0, 0], g[:, 0, 1], g[:, 1, 1]
    disc = np.sqrt(g0x ** 2 - g00 * gxx)
    u_plus = (-g0x + disc) / gxx
    u_minus = (-g0x - disc) / gxx
    dx = x[1] - x[0]
    return np.sum(1.0 / u_plus) * dx, np.sum(1.0 / np.abs(u_minus)) * dx


def alcubierre_diff_ns(v, R, sigma, L=300.0, n=600001):
    x = np.linspace(-L, L, n)
    f = (np.tanh(sigma * (np.abs(x) + R)) - np.tanh(sigma * (np.abs(x) - R))) / (2 * np.tanh(sigma * R))
    dx = x[1] - x[0]
    tp = np.sum(1.0 / (1.0 + v * f)) * dx   # dx/dt = 1 + v f along +x (bubble moving +x, c = 1)
    tm = np.sum(1.0 / (1.0 - v * f)) * dx
    return (tm - tp) / C * 1e9


def main():
    print("1. Alcubierre top-hat, R = 15 m, v = 0.04 (paper Table 1: 8.0 ns)")
    for sigma in (0.5, 1.0, 2.0, 8.0):
        print(f"   sigma = {sigma:4.1f}/m: (-x)-(+x) difference = {alcubierre_diff_ns(0.04, 15.0, sigma):.3f} ns;"
              f" linear estimate 2 v (2R)/c = {2*0.04*30.0/C*1e9:.3f} ns")
    print("2. Warp Shell rebuild (paper Table 1 row: 7.6 ns; Sec. 4.1: beta_warp = 0.02)")
    for span_P in (0.5, 1.0, 2.0, 3.0):
        row = []
        for beta in (0.02, 0.04):
            sh = build_shell(M, R1, R2, beta_warp=beta, span_P=span_P)
            tp, tm = light_time(sh)
            row.append((beta, (tm - tp) / C * 1e9, sh.M_ADM))
        print(f"   span_P = {span_P:.1f} m (span_rho = {1.72*span_P:.2f} m): "
              + "; ".join(f"beta {b:.2f}: {d:.2f} ns (M_ADM {m:.3e} kg)" for b, d, m in row))
    print("3. Linear scaling of the rebuild: beta_warp that would give 7.6 ns")
    sh = build_shell(M, R1, R2, beta_warp=0.02)
    tp, tm = light_time(sh)
    d02 = (tm - tp) / C * 1e9
    print(f"   rebuild default spans: {d02:.3f} ns at 0.02 -> 7.6 ns needs beta_warp ~ {0.02*7.6/d02:.4f}"
          f" (ratio paper/rebuild at 0.02 = {7.6/d02:.3f}; at 0.04 = {7.6/(2*d02):.3f})")


if __name__ == "__main__":
    main()
