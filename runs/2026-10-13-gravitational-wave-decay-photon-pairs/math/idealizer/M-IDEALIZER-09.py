"""M-IDEALIZER-09: GW150914 numbers in F8 (SI). Inputs as the lens states them: E = 2 (or 3) Msun c^2,
f = 150 Hz (w = 2 pi f), sigma_w = 200 s^-1; P = (4/25) G^2 E^2 w sigma/c^10 (M-01/M-03); B&O rate = P/T_eff,
T_eff = 4 pi/(3 sigma); pattern factor 0.562 (tool value, not re-derived here); stimulated factor 1 + 2 f_BE(hbar w/kT_CMB);
far-zone fraction R(>x) = A x^-3 with A = 0.069 (lens) vs 0.0632 (exact asymptote, M-08); profile-free law (12 pi/25) G^2 w L^2 dt/c^10.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, units, finish

G, c, hbar, kB = 6.67430e-11, 299792458.0, 1.054571817e-34, 1.380649e-23
Msun = 1.98841e30; AU = 1.495978707e11; Mpc = 3.0856775814913673e22; TCMB = 2.7255
w, sig = 2 * math.pi * 150, 200.0
def P(E): return 4 / 25 * G**2 * E**2 * w * sig / c**10
P2, P3 = P(2 * Msun * c**2), P(3 * Msun * c**2)
Teff = 4 * math.pi / (3 * sig)
print(f"P(2 Msun) = {P2:.4e}, P(3 Msun) = {P3:.4e}, rate = {P2/Teff:.4e} /s, T_eff = {Teff*1e3:.2f} ms")
quantity(f"{P2}", "2.93e-6", rel_tol=5e-3); quantity(f"{P3}", "6.59e-6", rel_tol=5e-3)
quantity(f"{P2/Teff}", "1.40e-4", rel_tol=5e-3); quantity(f"{Teff} s", "20.9 ms", rel_tol=5e-3)
units("(6.674e-11 m^3/(kg s^2))^2 * (2 Msun c^2)^2 * (942 /s) * (200 /s) / c^10", "dimensionless")
Pc = 0.562 * P2; Eph = Pc * 2 * hbar * w
print(f"circular: {Pc:.3e} pairs, {Eph:.3e} J, fraction {Eph/(2*Msun*c**2):.3e}")
quantity(f"{Pc}", "1.65e-6", rel_tol=5e-3); quantity(f"{Eph}", "3.3e-37", rel_tol=2e-2); quantity(f"{Eph/(2*Msun*c**2)}", "9e-85", rel_tol=3e-2)
fBE = 1 / math.expm1(hbar * w / (kB * TCMB))
print(f"1 + 2f = {1+2*fBE:.4e}; stimulated pairs {Pc*(1+2*fBE):.4e}, energy {Pc*(1+2*fBE)*2*hbar*w:.3e} J")
quantity(f"{1+2*fBE}", "7.6e8", rel_tol=1e-2); quantity(f"{Pc*(1+2*fBE)}", "1.25e3", rel_tol=1e-2)
quantity(f"{Pc*(1+2*fBE)*2*hbar*w}", "2.5e-28", rel_tol=2e-2)
rg = G * 65 * Msun / c**2
print(f"c/w = {c/w:.4e} m = {c/w/rg:.3f} GM/c^2 (65 Msun)")
quantity(f"{c/w} m", "318 km", rel_tol=3e-3); quantity(f"{c/w/rg}", "3.31", rel_tol=3e-3)
for name, r, lens in (("lambda", c / 150.0, 8.3e-10), ("1 AU", AU, 2.0e-24), ("410 Mpc", 410 * Mpc, 3.3e-66)):
    x = w * r / c
    lensA, exactA = 0.069 * x**-3 * P2, 0.0632 * x**-3 * P2
    print(f"beyond {name} (kr = {x:.3g}): 0.069 law {lensA:.3e}, exact-asymptote law {exactA:.3e}; lens {lens:.1e}")
    quantity(f"{lensA}", f"{lens}", rel_tol=0.1)
Lp = 3.6e49
for tdur, lens in ((5e-3, 7e-6), (10e-3, 1.4e-5)):
    Pl = 12 * math.pi / 25 * G**2 * w * Lp**2 * tdur / c**10
    print(f"profile-free L = 3.6e49 W for {tdur*1e3:.0f} ms: P = {Pl:.3e}")
    quantity(f"{Pl}", f"{lens}", rel_tol=2e-2)
units("(6.674e-11 m^3/(kg s^2))^2 * (942 /s) * (3.6e49 W)^2 * (5 ms) / c^10", "dimensionless")
raise SystemExit(finish())
