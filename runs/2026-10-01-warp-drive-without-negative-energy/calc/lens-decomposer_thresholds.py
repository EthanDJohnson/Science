"""Decomposer lens: thresholds on the rebuilt Fuchs shell (warp_shell.py defaults).
(1) beta_warp at which the NEC first fails (all observers, sampled points) at fixed mass,
    for several masses -> the shift cap positive matter allows in this family;
(2) beta_warp at which a one-way time advance (+x axis, D = 1e3 m) first appears.
Olum/Gao-Wald require (2) to lie inside the NEC-violating range: beta_adv > beta_NEC.
Geometric units for curvature; SI for times. R1 = 10 m, R2 = 20 m.
"""
import sys
import importlib.util
import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import warp_shell as ws  # noqa: E402
import numeric_stress_energy as nse  # noqa: E402

spec = importlib.util.spec_from_file_location(
    "tt", "runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-decomposer_transit_time.py")
tt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tt)
spec2 = importlib.util.spec_from_file_location(
    "av", "runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-decomposer_advance_vs_nec.py")
av = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(av)

MJ = 1.898e27
G, C = 6.67430e-11, 299792458.0


def nec_fails(M, beta):
    sh = ws.build_shell(M, 10.0, 20.0, beta_warp=beta)
    res = nse.NumericSpacetime(av.metric_fn(sh), 0.05).scan_energy_conditions(av.points())
    return res["violations"]["nec"] > 0


def advance(M, beta):
    sh = ws.build_shell(M, 10.0, 20.0, beta_warp=beta)
    tp, _ = tt.transit(sh, 1.0e3, n_in=8001, n_out=8001)
    return tp < 0


def bisect(pred, lo, hi, n=14):
    if pred(lo):
        return lo
    if not pred(hi):
        return None
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        if pred(mid):
            hi = mid
        else:
            lo = mid
    return hi


def main():
    print("frac of 2.365 M_J | 2GM/(c^2 R2) | beta_NEC (first NEC failure) | beta_adv (first advance, D=1e3 m)")
    for frac in [0.001, 0.01, 0.1, 0.5, 1.0]:
        M = frac * 2.365 * MJ
        comp = 2 * G * M / (C ** 2 * 20.0)
        bn = bisect(lambda b: nec_fails(M, b), 0.0, 0.95)
        ba = bisect(lambda b: advance(M, b), 0.0, 0.95)
        bn_s = f"{bn:.4f}" if bn is not None else "> 0.95"
        ba_s = f"{ba:.4f}" if ba is not None else "> 0.95 (none)"
        ok = "consistent" if (ba is None or (bn is not None and bn <= ba)) else "INCONSISTENT"
        print(f"{frac:7.3f} | {comp:.5f} | {bn_s} | {ba_s} | Olum ordering: {ok}")


if __name__ == "__main__":
    main()
