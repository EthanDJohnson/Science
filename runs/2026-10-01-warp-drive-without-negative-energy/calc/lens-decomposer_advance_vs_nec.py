"""Decomposer lens: Olum / Gao-Wald on a worked example.

lens-decomposer_transit_time.py found that the rebuilt Fuchs shell gives NO one-way time
advance at its published mass (2.365 M_J) for any beta_warp up to 0.95, but DOES give a net
advance (-1.87 ns on the +x axis, D = 1e3 m) when the mass is cut 100x with beta_warp = 0.04.
The theorems predict that such a spacetime must violate the NEC somewhere along the path.
This script scans NEC/WEC/DEC for all observers (numeric_stress_energy.py, Hawking-Ellis
classification) through the wall for both configurations and the published one.

Geometric units (G = c = 1), lengths in metres, t = ct. Points in the x-z plane,
r in [R1 - 2, R2 + 2] m, polar angles 0, 45, 90, 135, 180 deg from the shift (x) axis.
"""
import sys
import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import warp_shell as ws  # noqa: E402
import numeric_stress_energy as nse  # noqa: E402

MJ = 1.898e27


def metric_fn(shell):
    def g(t, x, y, z):
        arr = shell.metric_cartesian(t, x, y, z)
        return np.moveaxis(arr, (-2, -1), (0, 1))
    return g


def points():
    pts = []
    for ang in np.deg2rad([0, 45, 90, 135, 180]):
        for r in np.linspace(8.0, 22.0, 57):
            pts.append((0.0, r * np.cos(ang), 0.0, r * np.sin(ang)))
    return np.array(pts)


def run(label, M, beta, h=0.05):
    sh = ws.build_shell(M, 10.0, 20.0, beta_warp=beta)
    ns = nse.NumericSpacetime(metric_fn(sh), h)
    res = ns.scan_energy_conditions(points())
    print(f"--- {label}: M = {M/MJ:.4f} M_J, beta_warp = {beta}, h = {h} m ---")
    print(f"points {res['points']}, skipped {res['skipped']}, unconverged {res['unconverged']}")
    print(f"robust violations {res['violations']}")
    print(f"strict violations {res['violations_strict']}")
    print(f"marginal {res['marginal']}")
    print(f"types {res['types']}")
    for k, (val, q) in res["worst"].items():
        print(f"worst {k} = {val:.4e} 1/m^2 at {q}")
    return res


def main():
    run("published-mass shell, zero shift", 2.365 * MJ, 0.0)
    run("published-mass shell, paper's EC-checked shift", 2.365 * MJ, 0.02)
    run("published-mass shell, shift 0.04", 2.365 * MJ, 0.04)
    run("light shell that showed a time advance", 0.01 * 2.365 * MJ, 0.04)
    # step check on the light shell
    run("light shell, step check", 0.01 * 2.365 * MJ, 0.04, h=0.025)


if __name__ == "__main__":
    main()
