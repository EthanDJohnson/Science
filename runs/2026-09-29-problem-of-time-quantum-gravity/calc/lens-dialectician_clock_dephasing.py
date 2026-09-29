#!/usr/bin/env python3
"""Dialectician, contradiction II: exact relational unitarity (HSL) vs fundamental decoherence (GPP).

Part A (natural units hbar = 1, rad/s and s): Page-Wootters state with a near-ideal clock (d = 64 levels);
qubit H_S = diag(0, Delta), initial |+>. Condition on a clock reading with Gaussian error sigma and compare
the coherence |rho_01| with the closed form 0.5 exp(-sigma^2 Delta^2 / 2).

Part B (SI): Gambini-Porto-Pullin (GPP) exponent  ln(rho12(T)/rho12(0)) = -(3/2) t_P^(4/3) T^(2/3) w12^2
(dossier Q-15) equals Gaussian clock-reading dephasing sigma^2 w12^2 / 2 with sigma(T) = sqrt(3) t_P^(2/3) T^(1/3)
= sqrt(3) * deltaT_GPP(T), where deltaT_GPP = t_P (T/t_P)^(1/3) (dossier Q-14). Check numerically.

Part C (SI): time-scaling of the decoherence exponent for the rival mechanisms, as log-log slopes:
 GPP ~ T^(2/3); Pikovski time-dilation ~ (t/tau_dec)^2; Markovian collapse / classical-gravity diffusion ~ T^1.
"""
import sys
import math
import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import page_wootters as pw  # noqa: E402

# ---------------- Part A
d, w = 64, 1.0                       # clock spacing 1 rad/s
Delta = 3.0                          # qubit splitting 3 rad/s (resonant: -3 in clock spectrum)
HC = pw.equally_spaced_clock(d, w, k0=-(d - 1))   # E = -(d-1) .. 0 rad/s
HS = np.diag([0.0, Delta]).astype(complex)
m = pw.PWModel(HC, HS)
psi0 = np.array([1, 1], dtype=complex) / math.sqrt(2)
Psi = m.physical_state(psi0)
print("Part A: PW state, ideal equally spaced clock d=64 (w=1 rad/s), qubit Delta=3 rad/s, initial |+>")
rows = m.track(Psi, [0.0, 0.7, 2.1])
print("  sharp conditional fidelities with exp(-i H_S t):", [f"{r['fidelity']:.9f}" for r in rows])
for sigma in [0.05, 0.2, 0.4, 0.8]:
    cc = m.coarse_conditional(Psi, 10.0, sigma)
    coh = abs(cc["rho"][0, 1])
    pred = 0.5 * math.exp(-sigma**2 * Delta**2 / 2)
    print(f"  sigma={sigma:.2f} s | |rho01|={coh:.6f} | 0.5 exp(-sigma^2 Delta^2/2)={pred:.6f} | purity={cc['purity']:.6f}")

# ---------------- Part B
tP = 5.39e-44                         # Planck time, s
w12 = 2 * math.pi * 429e12            # rad/s (optical clock transition, as in dossier Q-15)
yr = 3.156e7
print("\nPart B: GPP exponent vs Gaussian clock dephasing with sigma = sqrt(3) * deltaT_GPP")
for T in [1.0, yr, 13.8e9 * yr]:
    gpp = 1.5 * tP ** (4 / 3) * T ** (2 / 3) * w12**2
    dT = tP * (T / tP) ** (1 / 3)
    sig = math.sqrt(3) * dT
    gauss = sig**2 * w12**2 / 2
    print(f"  T={T:.3e} s | GPP exponent={gpp:.3e} | deltaT_GPP={dT:.3e} s | sigma^2 w^2/2 (sigma=sqrt3 dT)={gauss:.3e} | ratio={gauss/gpp:.6f}")

# ---------------- Part C
print("\nPart C: log-log slope d ln(exponent)/d ln T for the rival mechanisms (T from 1 s to 10 s)")
T1, T2 = 1.0, 10.0
def slope(f):
    return (math.log(f(T2)) - math.log(f(T1))) / (math.log(T2) - math.log(T1))
tau_dec = 1.04e-3                     # s, Pikovski example (dossier Q-08)
print(f"  GPP realistic clock           : slope {slope(lambda T: 1.5*tP**(4/3)*T**(2/3)*w12**2):.4f}")
print(f"  Pikovski time dilation        : slope {slope(lambda T: (T/tau_dec)**2):.4f}")
print(f"  Markovian collapse / diffusion: slope {slope(lambda T: 1e-3*T):.4f}")
# Energy-difference dependence: GPP ~ w12^2 -> exponent quadruples when splitting doubles
print(f"  GPP exponent ratio for w12 -> 2 w12 at T = 1 s: {(1.5*tP**(4/3)*(2*w12)**2)/(1.5*tP**(4/3)*w12**2):.3f}")
