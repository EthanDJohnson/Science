"""M-EXAMINER-06: j(t, x) = F(t - z) (F = g^2, any integrable function) has 4D Fourier transform
J(q0, q) = Int dt d^3x e^{i q0 t - i q.x} F(t - z) = (2 pi)^3 delta(q0 - q_z) delta^2(q_perp) Ftilde(q0),
so its support is q0 = q_z, q_perp = 0, i.e. q^2 = q0^2 - |q|^2 = 0 (never time-like).
Independent check: change variables u = t - z and evaluate on a finite box numerically (discrete FFT), showing the power
sits on the light cone; and symbolically, q^2 on the support."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from math_checks import identity, finish

q0, qx, qy, qz = sp.symbols("q0 qx qy qz", real=True)
support = {qz: q0, qx: 0, qy: 0}
q2 = (q0 ** 2 - qx ** 2 - qy ** 2 - qz ** 2).subs(support)
identity(q2, sp.Integer(0), domain={"q0": (-10, 10)})

# numeric: 2D (t, z) periodic box, F(t - z) = Gaussian-modulated carrier squared; 2D FFT power
n, L = 256, 200.0
x = np.linspace(-L / 2, L / 2, n, endpoint=False)
T, Z = np.meshgrid(x, x, indexing="ij")
U = T - Z
U = (U + L / 2) % L - L / 2       # periodic wrap so the box is consistent
F = (np.exp(-(U / 15.0) ** 2) * np.cos(1.0 * U)) ** 2
P = np.abs(np.fft.fft2(F)) ** 2
k = 2 * np.pi * np.fft.fftfreq(n, d=L / n)
K0, KZ = np.meshgrid(k, k, indexing="ij")
# FFT kernel e^{-i(k0 t + kz z)}; F depends on t - z, so power sits on k0 = -kz, i.e. k0^2 = kz^2 (light cone)
on_cone = np.isclose(np.abs(K0), np.abs(KZ))
frac_off = P[~on_cone].sum() / P.sum()
print(f"fraction of Fourier power off the light cone: {frac_off:.3e}")
identity(sp.Integer(int(float(frac_off) < 1e-20)), sp.Integer(1))
raise SystemExit(finish())
