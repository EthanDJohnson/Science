"""M-MECHANIST-05 (F7): bottle-side required loss 1.30e-5 s^-1.
Gas upscattering: UCN are nearly at rest relative to gas molecules, so rate = n * sigma * <v_rel>,
<v_rel> ~ mean gas speed sqrt(8 kT / (pi m)); sigma taken at thermal gas speed (lens's ASSUMPTION:
N2 20 b, H2 160 b, He 0.8 b). p = n k T at 300 K. Spin flip: survival exp(-r t). SI; pressures also in mbar."""
import math, sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, units, limit, finish

kB = 1.380649e-23; amu = 1.66053906660e-27; T = 300.0
lam = 1 / 877.82 - 1 / 887.97
print(f"required rate = {lam:.4e} s^-1")
gases = {"N2": (28.014, 20e-28, 6e-4), "H2": (2.016, 160e-28, 2e-5), "He": (4.0026, 0.8e-28, 5e-3)}
for g, (A, sig, claim) in gases.items():
    vbar = math.sqrt(8 * kB * T / (math.pi * A * amu))
    n = lam / (sig * vbar)
    p = n * kB * T
    print(f"{g}: vbar = {vbar:.1f} m/s, n = {n:.3e} m^-3, p = {p:.3e} Pa = {p/100:.3e} mbar (lens {claim} mbar)")
    quantity(f"{p/100}", f"{claim}", rel_tol=0.1)
units("1e19 m^-3 * 1e-27 m^2 * 500 m/s", "Hz")
# spin flip: 1.3e-5 s^-1 over 1000 s
p1000 = 1 - math.exp(-lam * 1000)
print(f"spin-flip loss over 1000 s = {p1000*100:.3f} %")
quantity(f"{p1000}", "0.013", rel_tol=0.01)
limit("(1 - exp(-r*t))/(r*t)", "r", 0, 1)
# per wall collision at 5 and 50 collisions/s
for nu, claim in ((50, 2.6e-7), (5, 2.6e-6)):
    print(f"per-bounce at {nu}/s = {lam/nu:.3e}")
    quantity(f"{lam/nu}", f"{claim}", rel_tol=0.01)
raise SystemExit(finish())
