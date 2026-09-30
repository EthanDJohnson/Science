"""M-EMPIRICIST-09: SM tau_beta from lambda (F13; used by candidates A, C and the ledger).
tau_beta = K/(Vud^2 (1 + 3 lambda^2)). Independent pairing: CMS 2018 K = 4908.6 s with its own consistent
Vud = 0.97420 (i.e. K' = K/Vud^2 = 5172.0 s), per D-48/U-01 constants. Error propagation:
sigma^2 = (dtau/dlambda sigma_lambda)^2 + (2 tau sigma_V/V)^2 + sigma_K^2, sigma_V = 0.00032 (D-43), sigma_K = 0.19 s.
lambda inputs: D-40, D-41, D-42. Lifetimes in s (SI)."""
import sys
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/empiricist")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from _inputs import *
from math_checks import identity, limit, sign, quantity, finish
import sympy as sp

K, V, lam = sp.symbols("K V lam", positive=True)
tau = K / (V ** 2 * (1 + 3 * lam ** 2))
identity(sp.diff(tau, lam), -6 * lam * tau / (1 + 3 * lam ** 2))
identity(sp.diff(tau, V), -2 * tau / V)
limit("K/(V**2*(1 + 3*lam**2))", "lam", 0, "K/V**2")      # pure-Fermi limit
sign(sp.diff(tau, lam), "negative")                        # larger |lambda| -> shorter tau
quantity("4908.6 s / 0.97420^2", "5172.0 s", rel_tol=2e-4)

Kp = 4908.6 / 0.97420 ** 2
print(f"K' = {Kp:.3f} s")
inputs = {"PERKEO III": (1.27641, q(0.00045, 0.00033), 878.50, 0.88),
          "UCNA": (1.2772, 0.0020, 877.60, 2.36),
          "PERKEO II": (1.2748, q(0.0008, 0.00105), 880.34, 1.40),
          "aSPECT 2024": (1.2668, 0.0027, 889.58, 3.20),
          "aCORN": (1.2796, 0.0062, 874.86, 7.07)}
for name, (l, sl, lt, ls) in inputs.items():
    t = Kp / (1 + 3 * l * l)
    dl = 6 * l * t / (1 + 3 * l * l)
    s = q(dl * sl, 2 * t * 0.00032 / 0.97367, 0.19)
    s_alt = q(dl * 0.0011, 2 * t * 0.00032 / 0.97367, 0.19)
    print(f"{name}: tau {t:.3f} s (lens {lt}); sigma {s:.3f} s (lens {ls}); dtau/dlambda {dl:.1f} s; "
          f"sigma with sigma_lambda=0.0011: {s_alt:.3f}")
    agree(f"{name} tau (pairing spread 0.06 s)", t, lt, 0.08)
    agree(f"{name} sigma", s, ls, 0.02)
raise SystemExit(finish())
