"""M-DIALECTICIAN-09: fraction of the gap closed by EDE-class fits, and residuals (F8).

fraction = (H_m - 68.22)/(73.264 - 68.22) with P-ACT-LB LCDM 68.22 [D-42] and H0DN 73.264 +- 0.806 [D-22].
residual z = (73.264 - H_m)/sqrt(s_up^2 + 0.806^2), using the model's upper-side error.
Model values [D-52, D-53, D-94, D-95]: P-ACT-LB EDE 69.9 (+0.8), P-ACT EDE 69.3 (+0.9), Poulin 71.0 +- 1.1,
eROSITA 71.4 +- 1.4, mod. recombination 69.6 +- 1.0, PMF 69.1 +- 0.5, n_e fluctuations 69.3 +- 0.5.
NPIPE 95% upper H0 = 69.5: (73.264 - 69.5)/0.806.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import limit, inequality, finish

limit("(h - lo)/(hi - lo)", "h", "hi", "1", domain={"lo": (60, 69), "hi": (70, 80), "h": (60, 80)})
limit("(h - lo)/(hi - lo)", "h", "lo", "0", domain={"lo": (60, 69), "hi": (70, 80), "h": (60, 80)})

L, T, sT = 68.22, 73.264, 0.806
models = [("P-ACT-LB EDE", 69.9, 0.8, 0.33, 2.96), ("P-ACT EDE", 69.3, 0.9, 0.21, 3.28),
          ("Poulin", 71.0, 1.1, 0.55, 1.66), ("eROSITA", 71.4, 1.4, 0.63, 1.15),
          ("mod rec", 69.6, 1.0, 0.27, 2.85), ("PMF", 69.1, 0.5, 0.17, 4.39), ("n_e fluct", 69.3, 0.5, 0.21, 4.18)]
for name, h, s, f_l, z_l in models:
    f = (h - L) / (T - L); z = (T - h) / math.hypot(s, sT)
    print(f"{name}: fraction {f:.3f} (lens {f_l}); residual {z:.3f} sigma (lens {z_l})")
    inequality(f"abs({f} - {f_l})", "<=", "0.006")
    inequality(f"abs({z} - {z_l})", "<=", "0.01")
zn = (T - 69.5) / sT
print(f"NPIPE: {zn:.2f} H0DN-sigma (lens 4.7)")
inequality(f"abs({zn} - 4.7)", "<=", "0.05")
raise SystemExit(finish())
