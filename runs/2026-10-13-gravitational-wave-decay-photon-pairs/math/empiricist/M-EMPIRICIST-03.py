"""M-EMPIRICIST-03: eq. 17 resonance shortfall for a real chirp (SI).
sigma_omega = m v^2/(2 hbar); ULDM coherence time t_coh = 2 pi hbar/(m v^2).
Equal-mass binary, total mass M from the ISCO relation; Newtonian (leading-order quadrupole) chirp:
  fdot = (96/5) pi^(8/3) (G Mc/c^3)^(5/3) f^(11/3),  dE/df = (pi^(2/3)/3) G^(2/3) Mc^(5/3) f^(-1/3)
Time in fractional band v^2/2: dt = (v^2/2) f / fdot.  In-band gravitons N_band = dE/df * (f v^2/2) / (hbar omega).
N0 = (2/65) M c^2/(hbar omega). Suppression (N_band/N0)^2 multiplies W_phi (rate ~ N0^2).
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, quantity, units, finish

# 1. symbolic energy balance: (dE/df) * fdot equals the quadrupole luminosity (32/5) c^5/G (pi G Mc f/c^3)^(10/3)
Gs, Mc, f, c = sp.symbols("G_N M_c f c", positive=True)
fdot_s = sp.Rational(96, 5) * sp.pi**sp.Rational(8, 3) * (Gs * Mc / c**3)**sp.Rational(5, 3) * f**sp.Rational(11, 3)
dEdf_s = sp.pi**sp.Rational(2, 3) / 3 * Gs**sp.Rational(2, 3) * Mc**sp.Rational(5, 3) * f**sp.Rational(-1, 3)
L_s = sp.Rational(32, 5) * c**5 / Gs * (sp.pi * Gs * Mc * f / c**3)**sp.Rational(10, 3)
identity(sp.powsimp(dEdf_s * fdot_s, force=True), L_s)
# Kepler limit: dE/df = d/df of -(1/2) G M mu / a with a from Kepler at f_orb = f/2, equal masses (mu = M/4, Mc^(5/3) = mu M^(2/3))
M = sp.symbols("M", positive=True)
a = (Gs * M / (sp.pi * f)**2)**sp.Rational(1, 3)
Eorb = -Gs * M * (M / 4) / (2 * a)
identity(sp.diff(-Eorb, f) * -1 * -1, dEdf_s.subs(Mc, (M / 4)**sp.Rational(3, 5) * M**sp.Rational(2, 5)))
units("(1/3) * pi^(2/3) * G^(2/3) * (1 Msun)^(5/3) * (1 Hz)^(-1/3)", "J/Hz")

G, cc, hbar, eV = 6.67430e-11, 299792458.0, 1.054571817e-34, 1.602176634e-19
Msun = 1.3271244e20 / G
yr = 365.25 * 86400

def numbers(m_eV, v=1e-3, frac=2 / 65):
    w = m_eV * eV / hbar
    sigma = w * v**2 / 2
    tcoh = 2 * math.pi / (w * v**2)
    Mt = 8800 * math.pi / w * Msun
    mc = Mt * 0.25**0.6
    fr = w / (2 * math.pi)
    fdot = 96 / 5 * math.pi**(8 / 3) * (G * mc / cc**3)**(5 / 3) * fr**(11 / 3)
    t_in = (v**2 / 2) * fr / fdot
    dEdf = math.pi**(2 / 3) / 3 * G**(2 / 3) * mc**(5 / 3) * fr**(-1 / 3)
    Nband = dEdf * fr * v**2 / 2 / (hbar * w)
    N0 = frac * Mt * cc**2 / (hbar * w)
    return dict(w=w, sigma=sigma, inv_sigma=1 / sigma, tcoh_yr=tcoh / yr, inv_sigma_yr=1 / sigma / yr, f=fr,
                P_gw_days=1 / fr / 86400, P_orb_days=2 / fr / 86400, f_over_fdot=fr / fdot, t_in=t_in,
                shortfall=t_in * sigma, Nband=Nband, N0=N0, supp=(Nband / N0)**2)

r = numbers(1e-21)
for k, val in r.items():
    print(f"m = 1e-21 eV: {k} = {val:.4e}")
quantity(f"{r['sigma']} Hz", "7.6e-13 Hz", rel_tol=0.01)
quantity(f"{r['inv_sigma']} s", "1.32e12 s", rel_tol=0.01)
quantity(f"{r['inv_sigma_yr']} yr", "4.2e4 yr", rel_tol=0.01)
quantity(f"{r['tcoh_yr']} yr", "1.3e5 yr", rel_tol=0.02)
quantity(f"{r['f']} Hz", "2.4e-7 Hz", rel_tol=0.02)
quantity(f"{r['f_over_fdot']} s", "2.4e7 s", rel_tol=0.03)
quantity(f"{r['t_in']} s", "12 s", rel_tol=0.03)
quantity(f"{r['shortfall']}", "9.2e-12", rel_tol=0.03)
quantity(f"{r['Nband']}", "1.4e89", rel_tol=0.04)
quantity(f"{r['supp']}", "5.1e-14", rel_tol=0.03)
W_face = 3.8411e13  # from M-EMPIRICIST-02 (2/65, x = 1)
quantity(f"{W_face * r['supp']} W", "2.0 W", rel_tol=0.03)
r2 = numbers(2e-20)
print("m = 2e-20 eV: shortfall =", f"{r2['shortfall']:.4e}", "supp =", f"{r2['supp']:.4e}")
quantity(f"{r2['shortfall']}", f"{r['shortfall']}", rel_tol=1e-9)   # m-independence
quantity(f"{r2['supp']}", f"{r['supp']}", rel_tol=1e-9)
quantity(f"{9.6028e10 * r2['supp']} W", "4.9e-3 W", rel_tol=0.03)
raise SystemExit(finish())
