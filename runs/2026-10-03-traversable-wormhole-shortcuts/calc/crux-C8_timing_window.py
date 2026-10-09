"""Crux C8: two-sided analogue of C7's clock-offset window, and the MQ speed-up concession.

1. GJW timing window [Q-15]: a message must be inserted dt = R ln(R/(h l_P)) before the
   coupling is switched on; the eikonal treatment fails beyond (3/2) dt. So the usable
   insertion-time window (in boundary time, units of the AdS radius R, h = 1) runs from
   dt to 1.5 dt, width 0.5 dt. Every insertion in it arrives AFTER the coupling acts
   (arrival lag behind insertion is about dt, measured from the coupling time it is >= 0).
2. MQ speed-up (concession): wormhole transfer time / bare-coupling time ~ (mu/J)^(1/3)
   for q = 4 (MQ p. 28 exponent (1-2D)/(2(1-D)) with D = 1/4), as quoted in verdict C8-2.
Units: R in units of the AdS radius (dimensionless); mu/J dimensionless (J = hbar = 1).
"""
import math

print("== 1. GJW insertion window (h = 1) ==")
for log10_ratio in (2, 10, 30, 60):
    L = log10_ratio * math.log(10.0)  # ln(R/l_P)
    dt = L  # in units of R
    print(f"R/l_P = 1e{log10_ratio:<3d}: lead dt = {dt:7.1f} R; eikonal limit 1.5 dt = {1.5*dt:7.1f} R; "
          f"window width = {0.5*dt:6.1f} R")

print("== 2. MQ exponent and speed-up ==")
D = 0.25
expo = (1 - 2 * D) / (2 * (1 - D))
print(f"exponent (1-2D)/(2(1-D)) at D = 1/4: {expo:.4f}")
for r in (1e-1, 1e-2, 1e-3, 1e-4, 1e-6):
    print(f"mu/J = {r:.0e}: t_wh/t_bare ~ {r**expo:.4f}; speed-up ~ {r**(-expo):6.1f}x")
