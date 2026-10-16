"""Arithmetic on published numbers (quantitative facet). SI units.

1. Elasticity of time-optimal lap time on thrust-to-weight ratio (TWR), from the
   (TWR, lap time) pairs published by Foehn et al. 2021 (Science Robotics 6, eabh1221),
   motion-capture track, planner thrust bound at the stated TWR.
   elasticity = d ln(T) / d ln(TWR); speed elasticity = -that if path length is fixed
   (it is not exactly: the optimal path changes with TWR, so this is approximate).
2. Same for the extra-latency case in Agilicious (Foehn et al. 2022): tracking RMSE vs latency.
3. Fraction of model-optimal lap time in Song et al. 2023.
4. Dimensionless ratios: latency/time-constant, frame period.
"""
import math

pairs = [(2.5, 7.14), (3.15, 6.27), (3.3, 6.10), (3.6, 5.81)]  # (TWR, lap time s)
print("Foehn 2021 time-optimal lap time vs TWR (s):", pairs)
for (a, ta), (b, tb) in zip(pairs, pairs[1:]):
    e = math.log(tb / ta) / math.log(b / a)
    print(f"  TWR {a}->{b}: dlnT/dlnTWR = {e:.3f}  (speed elasticity ~ {-e:.3f})")
a, ta = pairs[0]
b, tb = pairs[-1]
e = math.log(tb / ta) / math.log(b / a)
print(f"  overall TWR {a}->{b}: dlnT/dlnTWR = {e:.3f}  (speed elasticity ~ {-e:.3f})")

# Agilicious latency vs tracking error (MOCAP), 4 g / 60 km/h trajectories
lat = [(35.0, 0.322), (75.0, 0.474)]  # (ms, RMSE m); the 75 ms is a lower bound (">75 ms")
(l1, r1), (l2, r2) = lat
print("Agilicious: latency (ms) vs positional RMSE (m):", lat, "(75 ms is a lower bound)")
print(f"  d lnRMSE / d lnLatency <= {math.log(r2/r1)/math.log(l2/l1):.3f}  (upper bound because latency is >75 ms)")
print(f"  RMSE increase = {100*(r2/r1-1):.1f} per cent for latency +{l2-l1:.0f} ms")

# Song 2023: model-optimal 4.9 s vs real RL 5.35 s
print("Song 2023: 4.9/5.35 =", round(4.9 / 5.35, 3), " ; 4.92/5.35 =", round(4.92 / 5.35, 3))

# Ratios
print("latency/tau: 35/39.1 =", round(35 / 39.1, 3), "; 40/39.1 =", round(40 / 39.1, 3))
print("30 Hz frame period (ms) =", round(1000 / 30, 2), "; 100 Hz VIO period (ms) =", 1000 / 100)
print("Swift static thrust 35 N / (0.870 kg * 9.81) =", round(35 / (0.870 * 9.81), 3))
print("Song 63 N / (0.52 kg * 9.81) =", round(63 / (0.52 * 9.81), 2))
print("Agilicious 131 km/h =", round(131 / 3.6, 2), "m/s ; 108 km/h =", round(108 / 3.6, 2), "m/s ; 65 km/h =", round(65 / 3.6, 2), "m/s")
# Verification: finite-difference check of elasticity on a power law
T = lambda w: 7.0 * w ** -0.5
print("check: power law T~w^-0.5 gives", round(math.log(T(3.0) / T(2.5)) / math.log(3.0 / 2.5), 6))
