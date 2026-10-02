"""falsifier-C1-2 (part 4): the most a NEC-clean shift can do for a payload beyond a plain shell.

Units: SI (c = 2.998e8 m/s); speeds also in units of c. Inputs: beta_NEC and interior lapse N
from falsifier-C1-2_design_gap.py / _thickwall.py logs; R1 the cavity radius.
1. Shift-ramp kick (M-MECHANIST-06 mechanism): a payload at rest keeps u_x = 0 and ends with
   relative speed beta/N to the shell. Its displacement relative to the shell is bounded by the
   cavity diameter 2 R1 before it meets the wall, so no net travel is gained.
2. Shift-induced one-way light-time asymmetry across the cavity (Sagnac-type), 2*2R1*beta/(c(N^2-beta^2)).
3. Photon-rocket bill (start+stop) of shell vs payload: ratio = M_shell/m_payload, same as any
   massive vehicle of that mass -- the shift does not enter.
"""
c = 2.99792458e8
cases = [
    ("published shell (R1=10 m, C=0.333)", 10.0, 0.0239, 0.7611, 4.511e27),
    ("thick wall (R1=0.5 m, C=0.333)", 0.5, 0.0624, 0.7246, 4.49e27),
    ("thick wall (R1=2 m, C=0.6)", 2.0, 0.0829, 0.4546, 8.08e27),
]
m_pay = 1e5  # kg, the run's payload convention
for name, R1, b, N, M in cases:
    vrel = b / N
    t_wall = R1 / (vrel * c)
    asym = 2 * (2 * R1) * b / (c * (N ** 2 - b ** 2))
    print(f"{name}: kick speed beta/N = {vrel:.4f} c = {vrel*c:.3e} m/s; reaches wall in {t_wall*1e6:.3f} us; "
          f"max relative displacement 2R1 = {2*R1:.1f} m; cavity light asymmetry {asym*1e9:.3f} ns; "
          f"shell/payload mass (= propulsion-bill ratio) {M/m_pay:.3e}")
