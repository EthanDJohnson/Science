#!/usr/bin/env python3
"""M-MECH-06  Stereo depth-noise ceiling on usable range.

CLAIM (mechanist finding 6)
  Symbols: z depth [m]; b stereo baseline [m]; f focal length [px]; d = f b/z disparity [px];
  sigma_d disparity noise [px]; sigma_z depth noise [m]; W_px image width [px]; H_fov horizontal
  field of view [rad]. Assumptions: rectified pinhole stereo, small disparity error, obstacle on
  the optical axis.
  Claimed: (i) f = W_px/(2 tan(H_fov/2)) = 337 px for 640 px over 87 deg;
           (ii) sigma_z = z^2 sigma_d/(f b);
           (iii) with b = 50 mm, sigma_z = 0.1 m (a 10 cm obstacle's own size) at z = 4.1 m for
                 sigma_d = 0.1 px and z = 5.8 m for 0.05 px;
           (iv) a 10 cm obstacle subtends 3 px only within z = 11.2 m.
"""
import math
import sys

import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, limit, quantity, units  # noqa: E402

# (i) focal length
f640 = 640 / (2 * math.tan(math.radians(87.0) / 2))
f848 = 848 / (2 * math.tan(math.radians(87.0) / 2))
print(f"inputs: 87 deg HFoV; f(640 px) = {f640:.2f} px, f(848 px) = {f848:.2f} px")
quantity(f"{f640:.6f} m", "337 m", rel_tol=5e-3)

# (ii) error propagation of z = f b / d
z, b, f, d, sd = sp.symbols("z b f d sigma_d", positive=True)
z_of_d = f * b / d
dzdd = sp.simplify(sp.Abs(sp.diff(z_of_d, d)))
sigma_z = sp.simplify(dzdd.subs(d, f * b / z) * sd)
identity(sigma_z, z**2 * sd / (f * b), domain={"z": (0.1, 50), "b": (0.01, 1),
                                               "f": (10, 2000), "sigma_d": (0.001, 1)})
limit(z**2 * sd / (f * b), "z", 0, 0)                 # no depth error at zero range
units("(4.1 m)^2 * 0.1/(337.2 * 0.05 m)", "length")   # px cancels, so it is dimensionless

# (iii) range at which sigma_z equals the obstacle size
B, OBS = 0.050, 0.10
for sdv, want in ((0.1, 4.1), (0.05, 5.8)):
    zz = math.sqrt(OBS * f640 * B / sdv)
    print(f"sigma_d = {sdv} px -> sigma_z = {OBS} m at z = {zz:.3f} m   (lens: {want} m)")
    quantity(f"{zz:.6f} m", f"{want} m", rel_tol=1e-2)
# monotonicity: sigma_z grows as z^2, so the usable range shrinks as sqrt(sigma_d)
print(f"check scaling: z(0.05 px)/z(0.1 px) = {math.sqrt(0.1/0.05):.4f} (expect sqrt(2))")
quantity(f"{math.sqrt(OBS*f640*B/0.05)/math.sqrt(OBS*f640*B/0.1):.6f} m",
         f"{math.sqrt(2):.6f} m", rel_tol=1e-6)

# (iv) pixel subtense of a 10 cm obstacle
z3 = f848 * OBS / 3.0
z3_640 = f640 * OBS / 3.0
print(f"10 cm spans 3 px at z = {z3:.3f} m (f = 848 px row) / {z3_640:.3f} m (f = 640 px row)"
      f"   (lens: 11.2 m)")
# the lens's 11.2 m is the 640-px row (f = 337 px), consistent with the rest of finding 6
quantity(f"{z3_640:.6f} m", "11.2 m", rel_tol=1e-2)

raise SystemExit(finish())
