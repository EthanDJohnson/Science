"""M-MECHANIST-10 (and M-MECHANIST-11).

M-10: near-zone field of a quasi-circular binary, a rigidly rotating m = 2 pattern F(r, z) cos(2 phi - 2 Omega t).
Claim: its Fourier support is space-like where the pattern speed Omega r < c (so no O(h^2) massless pair
production there); q0/abs(q) ~ v. Check: for a single cylindrical harmonic, q0 = 2 Omega and the azimuthal wavenumber
is 2/r, so q0/q_phi = Omega r; any radial/vertical structure only adds to abs(q). At r ~ a the ratio is the orbital
relative speed v = Omega a (Kepler); time-like support needs r > c/Omega = lambda_GW/pi (wave zone).
M-11: in a plasma, photons have effective mass w_p; g g -> gamma gamma needs s >= 4 w_p^2 with s <= 4 w^2
(head-on, each graviton w), so it is closed if w < w_p. f_p = 8.98 kHz sqrt(n_e/cm^-3); n_e = 0.03 cm^-3 (warm ISM,
assumed) gives about 1.6 kHz > 150 Hz.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import math
import sympy as sp
from math_checks import identity, inequality, quantity, finish

r, Om, t, ph, kr, kz = sp.symbols("r Omega t phi k_r k_z", positive=True)
pattern = sp.cos(2 * ph - 2 * Om * t)
q0 = sp.diff(2 * ph - 2 * Om * t, t) * -1          # frequency of the phase
qphi = sp.diff(2 * ph - 2 * Om * t, ph) / r        # physical azimuthal wavenumber
identity(q0 / qphi, Om * r)
# with extra radial/vertical wavenumbers the ratio only falls: q0/sqrt(qphi^2+kr^2+kz^2) <= Om r
inequality(q0 / sp.sqrt(qphi**2 + kr**2 + kz**2), "<=", Om * r)
# light cylinder of the pattern: r_L = c/Omega = 2 c/w_GW = lambda_GW/pi
c, wgw = sp.symbols("c w_GW", positive=True)
identity((c / Om).subs(Om, wgw / 2), (2 * sp.pi * c / wgw) / sp.pi)
# M-11 plasma
quantity("(0.03 * 1e6 /m^3 * (1.602176634e-19 C)^2 / (8.8541878128e-12 C^2/(J*m) * 9.1093837015e-31 kg))^0.5 / (2*pi)",
         "1.56 kHz", rel_tol=0.02)
inequality("4*w**2", "<", "4*wp**2", domain={"w": (0.1, 0.99), "wp": (1.0, 10)})   # s_max < threshold when w < w_p
raise SystemExit(finish())
