"""Falsifier C8-1 (evidence angle): two small checks.
1. 1 kg payload as quanta of wavelength ~R through a throat of R = 1 m: N = m c R / hbar (SI).
2. Maldacena-Qi coupled SYK: wormhole revival time ~ mu^(-2/3) (J = 1 units, Plugge et al. 2020)
   versus the naive single-bilinear hopping time ~ pi/(2 mu), and versus a crude speed limit
   set by the full coupling norm ||H_int|| ~ N mu / 2 (N Majorana pairs): t_QSL ~ pi / (2 * N mu / 2).
   Shows the wormhole beats the naive single-channel rate but not the full coupling's speed limit.
"""
import math

hbar = 1.054571817e-34  # J s
c = 2.99792458e8        # m/s
m = 1.0                 # kg
R = 1.0                 # m
N_q = m * c * R / hbar
print(f"1. quanta for 1 kg through R = 1 m: m c R / hbar = {N_q:.3e} (dimensionless)")

print("2. MQ transfer times (units J = 1, hbar = 1; order-of-magnitude, prefactors O(1) omitted)")
print(f"{'mu':>8} {'t_WH~mu^-2/3':>14} {'t_naive~pi/(2mu)':>18} {'ratio naive/WH':>15} {'t_QSL(N=100)':>13} {'t_QSL(N=1e4)':>13}")
for mu in [1e-1, 1e-2, 1e-3, 1e-4]:
    t_wh = mu ** (-2.0 / 3.0)
    t_naive = math.pi / (2 * mu)
    for N in (100, 1e4):
        pass
    t_qsl_100 = math.pi / (2 * (100 * mu / 2))
    t_qsl_1e4 = math.pi / (2 * (1e4 * mu / 2))
    print(f"{mu:8.0e} {t_wh:14.3e} {t_naive:18.3e} {t_naive / t_wh:15.3f} {t_qsl_100:13.3e} {t_qsl_1e4:13.3e}")
# condition for wormhole transfer to respect the crude full-coupling bound: mu^-2/3 >= pi/(N mu)  <=>  N >= pi mu^-1/3
for mu in [1e-2, 1e-4]:
    print(f"   wormhole slower than full-coupling speed limit iff N >= pi*mu^(-1/3) = {math.pi * mu ** (-1/3):.2f} at mu = {mu:.0e}")
