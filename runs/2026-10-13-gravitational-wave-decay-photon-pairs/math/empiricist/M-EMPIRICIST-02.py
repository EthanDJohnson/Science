"""M-EMPIRICIST-02: eq. 18 numbers (SI outputs, natural-unit formula converted).
W_phi = 9 pi G_nat E_m^2 v^3 N0^2 (hbar H0)^2 Omega_DM x / (256 hbar), G_nat = G/(hbar c^5),
E_m = m c^2, N0 = E_rel / E_m, E_rel = (2 or 3)/65 M c^2, M from omega_s = 8800 pi (Msun/M) s^-1 = E_m/hbar.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, identity, units, finish

G, c, hbar, eV = 6.67430e-11, 299792458.0, 1.054571817e-34, 1.602176634e-19
Msun = 1.3271244e20 / G
Mpc = 3.0856775814913673e22
H100 = 1e5 / Mpc
# Omega_DM H0^2 = Omega_c h^2 * H100^2 (only the product enters)
OmH2 = 0.120 * H100**2

# check the ISCO relation itself: f_GW,ISCO = c^3/(6^{3/2} pi G M) -> omega = 2 pi f
w_isco_1 = 2 * math.pi * c**3 / (6**1.5 * math.pi * G * Msun)
print(f"omega_ISCO(1 Msun) = {w_isco_1:.1f} rad/s vs 8800 pi = {8800*math.pi:.1f}")
quantity(f"{w_isco_1} Hz", f"{8800*math.pi} Hz", rel_tol=0.01)

def row(m_eV, frac, v=1e-3, x=1.0):
    Em = m_eV * eV
    w = Em / hbar
    M = 8800 * math.pi / w * Msun
    Erel = frac * M * c**2
    N0 = Erel / Em
    Gn = G / (hbar * c**5)
    W = 9 * math.pi * Gn * Em**2 * v**3 * N0**2 * hbar**2 * OmH2 * x / (256 * hbar)
    return M / Msun, N0, W, W / Em

for m_eV in (1e-22, 1e-21, 2e-20):
    for frac in (2 / 65, 3 / 65):
        M, N0, W, rate = row(m_eV, frac)
        print(f"m = {m_eV:.0e} eV, E_rel = {frac*65:.0f}/65 Mc^2: M = {M:.3e} Msun, N0 = {N0:.3e}, W = {W:.3e} W, scalars/s = {rate:.3e}")

M, N0, W2, r2 = row(1e-21, 2 / 65)
_, _, W3, r3 = row(1e-21, 3 / 65)
quantity(f"{M}", "1.82e10", rel_tol=0.01)
quantity(f"{N0}", "6.2e95", rel_tol=0.02)
quantity(f"{W2} W", "3.8e13 W", rel_tol=0.03)
quantity(f"{W3} W", "8.6e13 W", rel_tol=0.03)
quantity(f"{r2} Hz", "2.4e53 Hz", rel_tol=0.03)
quantity(f"{r3} Hz", "5.4e53 Hz", rel_tol=0.03)
quantity(f"{row(1e-22, 2/65)[2]} W", "3.8e15 W", rel_tol=0.03)
quantity(f"{row(2e-20, 2/65)[2]} W", "9.6e10 W", rel_tol=0.03)
quantity(f"{row(2e-20, 3/65)[2]} W", "2.2e11 W", rel_tol=0.03)
# scaling limit: W ~ m^2 N0^2 with N0 ~ M/m ~ 1/m^2 -> W ~ m^-2 (B&O eq. 18 shows (1e-21 eV/m)^2)
ratio = row(1e-22, 2/65)[2] / row(1e-21, 2/65)[2]
print(f"W(1e-22)/W(1e-21) = {ratio:.4f} (expected 100 for m^-2 scaling)")
quantity(f"{ratio}", "100", rel_tol=1e-9)
units("(G/(hbar*c^5)) * (1 eV)^2 * (hbar * 1 Hz)^2 / hbar", "W")
raise SystemExit(finish())
