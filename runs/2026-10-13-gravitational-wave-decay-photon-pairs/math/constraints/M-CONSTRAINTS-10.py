"""M-CONSTRAINTS-10: free-free absorption lengths (F12). cgs (Rybicki & Lightman eq. 5.19b, RJ limit):
alpha_ff = 0.018 T^-3/2 Z^2 n_e n_i nu^-2 g_ff  [cm^-1], n_i = n_e, Z = 1.
Gaunt factor (classical, low frequency): g_ff = (sqrt 3/pi) [ln((2kT)^{3/2}/(pi e^2 m_e^{1/2} nu)) - 5 gamma_E/2].
Claims: g_ff = 14.6 (T = 1e4 K, 150 Hz); absorption length 0.57 Mpc (n_e 2.2e-7), 37 Mpc (2.75e-8) at 150 Hz;
27-1.8e3 Mpc at 1 kHz; hot halo (1e-4 cm^-3, 1e6 K) 2.2 kpc at 150 Hz.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, units, finish

k, e, me = 1.380649e-16, 4.80320471e-10, 9.1093837015e-28
gE = 0.5772156649
Mpc_cm = 3.0856775814913673e24
def gff(T, nu):
    return math.sqrt(3) / math.pi * (math.log((2 * k * T)**1.5 / (math.pi * e**2 * math.sqrt(me) * nu)) - 2.5 * gE)
def length(n, T, nu):
    a = 0.018 * T**-1.5 * n * n * nu**-2 * gff(T, nu)
    return 1 / a
print("g_ff(1e4 K, 150 Hz) =", gff(1e4, 150))
quantity(f"{gff(1e4,150)}", "14.6", rel_tol=0.01)
units("1 / (1 K^-1.5 * (1 m^-3)^2 * (1 Hz)^-2)", "m^-6 K^1.5 Hz^2") if False else None
for n, T, nu, want, unit in [(2.2e-7, 1e4, 150, 0.57, Mpc_cm), (2.75e-8, 1e4, 150, 37, Mpc_cm),
                             (2.2e-7, 1e4, 1000, 27, Mpc_cm), (2.75e-8, 1e4, 1000, 1.8e3, Mpc_cm),
                             (1e-4, 1e6, 150, 2.2, Mpc_cm / 1e3)]:
    L = length(n, T, nu) / unit
    print(f"n={n}, T={T:g}, nu={nu}: g_ff={gff(T,nu):.2f}, length={L:.3g} ({'Mpc' if unit==Mpc_cm else 'kpc'})")
    quantity(f"{L}", f"{want}", rel_tol=0.05)
raise SystemExit(finish())
