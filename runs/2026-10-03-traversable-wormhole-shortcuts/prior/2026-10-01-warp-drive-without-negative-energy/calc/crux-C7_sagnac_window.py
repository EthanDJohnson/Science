"""Crux C7: Sagnac (co-minus-counter) holonomy inside the positive-energy window,
the corrected counterflow law, and the photon-rocket floor that C7's 'no' answer rests on.

Inputs (all from run files, cited in cruxes/C7.md):
- beta_crit = 0.02386 (M-CONSTRAINTS-13, NEC cap of the rebuild)
- rebuild Sagnac difference 6.86 ns at beta = 0.02, linear in beta
  (calc/lens-decomposer_transit_time.py.log, lines 15-20)
- linear N = 1 Sagnac 8.01 ns at beta = 0.04 (calc/lens-idealizer_thickwall.py.log, line 56),
  raised by ~1/N^2 for cavity lapse^2 e^{2a} = 0.5794
- Fuchs Table 1: 7.6 ns at 'v_warp = 0.04' [D-25]
- C = 0.3350, two-sheet law beta = C (u gamma)(R2/R1 - 1) (falsifier-C7-2)
Units: ns (SI time); beta dimensionless (units of c).
"""
import math

beta_crit = 0.02386
rebuild_per_beta = 6.86 / 0.02          # ns per unit beta, nonlinear rebuild
lin_N1_per_beta = 8.01 / 0.04           # ns per unit beta, linear N = 1
e2a = 0.5794
fuchs_per_beta = 7.6 / 0.04             # ns per unit 'v_warp'

print("[1] Sagnac co-minus-counter difference at the NEC cap beta_crit = %.5f" % beta_crit)
print("  rebuild (nonlinear lapse):       %.2f ns" % (rebuild_per_beta * beta_crit))
print("  linear, N = 1:                   %.2f ns" % (lin_N1_per_beta * beta_crit))
print("  linear x 1/N^2 (N^2 = %.4f):    %.2f ns" % (e2a, lin_N1_per_beta * beta_crit / e2a))
print("  Fuchs Table 1 scaled linearly:   %.2f ns" % (fuchs_per_beta * beta_crit))
print("  rebuild at 0.04 / Fuchs 7.6 ns: ratio %.2f (beta-definition mismatch)" % (rebuild_per_beta * 0.04 / 7.6))
print("  check: linear/N^2 at 0.04 = %.2f ns vs rebuild 13.72 ns" % (8.01 / e2a))

print("\n[2] corrected two-sheet counterflow law beta/C = u*gamma*(R2/R1 - 1)")
C = 0.3350
for ratio in (1.2, 2.0, 5.0):
    for u in (0.072, 0.10, 0.30):
        g = 1 / math.sqrt(1 - u * u)
        print("  R2/R1 = %.1f, u = %.3f c: beta/C = %.4f, beta = %.4f" % (ratio, u, u * g * (ratio - 1), C * u * g * (ratio - 1)))

print("\n[3] photon-rocket floor for start+stop (whole mass), fraction radiated")
for v in (0.02386, 0.04):
    leg = math.sqrt((1 + v) / (1 - v))
    R = leg * leg
    print("  v = %.4f c: mass ratio %.5f, fraction radiated %.4f" % (v, R, 1 - 1 / R))
print("  C7 prediction: at fixed M_ADM this fraction is independent of the cavity shift beta")
