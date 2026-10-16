#!/usr/bin/env python3
"""Falsifier C6-0: does UNMODELLED AERODYNAMICS bind first, as model error against gate
clearance, above about 13 m/s?

C6's own decisive discriminator (candidates.md, C6 "decisive test"):
    "measure *closed-loop* tracking error at 15-20 m/s to see whether it follows the
     open-loop power law (about 0.4 m) or is rejected (about 0.05 m)"
and C6's own prediction:
    "a NeuroBEM-grade model buys 1.8-2.2x the speed of a polynomial drag model on the
     same airframe and track"

This script runs that discriminator inside the simulator lens's own verified 17-state
plant (calc/lens-simulator_model.py, platform Sun et al. 2022, 0.75 kg, T/W 4.62), with
three arms that differ ONLY in the controller's aerodynamic model:

  A. BLIND     controller models no aerodynamics (the lens baseline, maximal model error)
  B. EXACT     controller feeds forward the plant's own aero force exactly, using the
               measured attitude and velocity (an upper bound on any aero model: zero
               aerodynamic model error, i.e. a perfect NeuroBEM)
  C. NO-AERO   plant aero switched off AND controller blind (zero model error because
               there is no aerodynamics to model)

Measured: U* (largest reference rate passing all six gates) and the worst LATERAL/VERTICAL
gate error, which is the quantity C6's clearance budget is about.

SI units throughout (m, s, kg, N).
"""
from __future__ import annotations

import math
import os
import sys
import time
from dataclasses import replace

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from importlib import import_module

M = import_module("lens-simulator_model")
from quadrotor import platform_sun2022, quat_to_rot  # noqa: E402  (same module M imported)

G = M.G
PASS = []


def check(name, got, want, tol, rel=True):
    err = abs(got - want) / abs(want) if rel else abs(got - want)
    ok = err <= tol
    PASS.append(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got:.4f}, want {want:.4f} "
          f"({'rel' if rel else 'abs'} err {err:.3g} <= {tol:g})")


class ExactAeroCascade(M.Cascade):
    """Cascade whose thrust/attitude command feeds forward the plant's exact aero force.

    This is the zero-aero-model-error arm: f_desired = m a_des + m g e3 - R f_aero(v_B),
    evaluated with the (delayed, measured) attitude and velocity.  No other change.
    """

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._v_m = np.zeros(3)

    def outer(self, p_m, v_m, p_ref, v_ref, a_ref):
        self._v_m = np.asarray(v_m, float)
        return (a_ref + self.w_vel * (v_ref - v_m)
                + self.w_pos * self.w_vel * (p_ref - p_m))

    def thrust_and_attitude(self, a_des, q_m, yaw_ref=0.0):
        m = self.nominal.mass
        R = quat_to_rot(q_m)
        vB = R.T @ self._v_m
        fa = self.q.aero_force_body(vB)          # exact knowledge of the plant's aero force
        f_w = m * (a_des + np.array([0.0, 0.0, G])) - R @ fa
        nf = float(np.linalg.norm(f_w))
        if nf < 1e-9:
            f_w, nf = np.array([0.0, 0.0, 1e-9]), 1e-9
        zb_des = f_w / nf
        T = float(f_w @ (R @ np.array([0.0, 0.0, 1.0])))
        return max(T, 0.0), zb_des


def arm(label, plant, ctl_cls, tol, lo=5.0, hi=22.0, dt=2e-3, iters=7, **ckw):
    course = M.Slalom(tol=tol)
    ctl = ctl_cls(plant, **ckw)
    t0 = time.time()
    r = M.max_speed(plant, ctl, course, dt=dt, mode="preview", lo=lo, hi=hi, iters=iters)
    el = time.time() - t0
    if not np.isfinite(r["U_max"]):
        print(f"  {label:34s} FAILS at U_lo = {lo} m/s   [{el:.0f}s]")
        return r
    print(f"  {label:34s} U*={r['U_max']:7.3f}  v={r['v_mean']:6.3f} m/s  "
          f"t={r['t_finish']:.3f} s  worst gate err={r['worst_gate_err']:.3f} m  "
          f"w_rate={ctl.w_rate:6.2f}  [{el:.0f}s]")
    return r


def fixed_U(label, plant, ctl_cls, tol, U, dt=2e-3, **ckw):
    course = M.Slalom(tol=tol)
    ctl = ctl_cls(plant, **ckw)
    r = M.run_course(plant, ctl, course, U, dt=dt, mode="preview")
    print(f"  {label:34s} U={U:5.2f}  ok={str(r['ok']):5s}  worst lat/vert gate err="
          f"{r['worst_gate_err']:.4f} m  mode={r['failure_mode']:16s} "
          f"v_mean={r['v_mean_path'] if np.isfinite(r['v_mean_path']) else float('nan'):.3f}")
    return r


def main():
    q_aero = platform_sun2022()                       # plant aero ON (kd and kh)
    q_noaero = replace(q_aero, enable_drag=False, enable_h_force=False)
    print(M.model_card(q_aero, M.Slalom(tol=0.2), M.Cascade(q_aero)))
    print()

    print("=" * 100)
    print("0. REPRODUCTION of the simulator lens's own rows (lens-simulator_sweep.py.log)")
    print("=" * 100)
    r_b02 = arm("A BLIND, tol 0.20 m  [lens 14.875]", q_aero, M.Cascade, 0.20)
    r_b05 = arm("A BLIND, tol 0.50 m  [lens 18.050]", q_aero, M.Cascade, 0.50)
    r_n02 = arm("C NO-AERO, tol 0.20 m [lens 8.875]", q_noaero, M.Cascade, 0.20)
    check("reproduce baseline U* at tol 0.20 m", r_b02["U_max"], 14.875, 0.02)
    check("reproduce baseline U* at tol 0.50 m", r_b05["U_max"], 18.050, 0.02)
    check("reproduce aero-off U* at tol 0.20 m", r_n02["U_max"], 8.875, 0.03)

    print()
    print("=" * 100)
    print("1. C6's OWN DISCRIMINATOR: closed-loop lateral/vertical gate error at 13-20 m/s")
    print("   against C6's open-loop power laws e(v) = 0.0493 v^0.858 (BEM) and")
    print("   0.0439 v^1.173 (poly fit) [M-CONSTRAINTS-08 verified], clearance budget 0.449 m")
    print("=" * 100)
    for U in (13.0, 15.0, 18.0, 20.0):
        e_bem = 0.0493 * U ** 0.858
        e_fit = 0.0439 * U ** 1.173
        rr = fixed_U("A BLIND (max model error)", q_aero, M.Cascade, 0.50, U)
        print(f"      C6 predicts at {U:.0f} m/s: e_BEM={e_bem:.3f} m, e_fit={e_fit:.3f} m; "
              f"measured closed-loop={rr['worst_gate_err']:.3f} m  "
              f"ratio to e_BEM={rr['worst_gate_err']/e_bem:.3f}")

    print()
    print("=" * 100)
    print("2. THE AERO-MODEL-ON/OFF ARM (C6 predicts a better aero model buys 1.8-2.2x speed)")
    print("   B EXACT = exact feedforward of the plant's own aero force = zero model error")
    print("=" * 100)
    r_e02 = arm("B EXACT aero model, tol 0.20 m", q_aero, ExactAeroCascade, 0.20)
    r_e05 = arm("B EXACT aero model, tol 0.50 m", q_aero, ExactAeroCascade, 0.50)
    r_k02 = arm("B' lens know_drag=True, tol 0.20", q_aero, M.Cascade, 0.20, know_drag=True)

    for lab, rb, re in (("tol 0.20 m", r_b02, r_e02), ("tol 0.50 m", r_b05, r_e05)):
        if np.isfinite(re["U_max"]) and np.isfinite(rb["U_max"]):
            g = re["U_max"] / rb["U_max"]
            print(f"  GAIN from removing ALL aerodynamic model error, {lab}: "
                  f"U* {rb['U_max']:.3f} -> {re['U_max']:.3f} m/s, factor {g:.4f} "
                  f"({100*(g-1):+.1f} per cent); C6 needs 1.8-2.2x")
    if np.isfinite(r_k02["U_max"]):
        print(f"  GAIN from the lens's own know_drag arm, tol 0.20 m: "
              f"factor {r_k02['U_max']/r_b02['U_max']:.4f}")

    print()
    print("=" * 100)
    print("3. SIGN TEST: does unmodelled aerodynamics help or hurt in this plant?")
    print("=" * 100)
    r_n05 = arm("C NO-AERO, tol 0.50 m", q_noaero, M.Cascade, 0.50)
    for lab, rn, rb in (("tol 0.20 m", r_n02, r_b02), ("tol 0.50 m", r_n05, r_b05)):
        if np.isfinite(rn["U_max"]):
            print(f"  {lab}: zero-model-error (no aero at all) U*={rn['U_max']:.3f} m/s vs "
                  f"full unmodelled aero U*={rb['U_max']:.3f} m/s -> removing the unmodelled "
                  f"aerodynamics changes speed by {100*(rn['U_max']/rb['U_max']-1):+.1f} per cent")

    print()
    print("=" * 100)
    print("4. WHERE THE AERO FORCE ACTS: body-frame components at the measured kd, kh")
    print("=" * 100)
    for v in (7.0, 13.0, 15.0, 20.0):
        # level flight along +x_W at tilt theta = atan(a/g) is irrelevant here; take the
        # airspeed purely along body x, the worst case for the along-track component.
        fa = q_aero.aero_force_body(np.array([v, 0.0, 0.0]))
        print(f"  v_B = ({v:.1f}, 0, 0) m/s -> f_aero_B = ({fa[0]:+.3f}, {fa[1]:+.3f}, "
              f"{fa[2]:+.3f}) N;  |along-track| = {abs(fa[0]):.3f} N = "
              f"{abs(fa[0])/(q_aero.mass*G)*100:.1f} per cent of weight; "
              f"lateral = {abs(fa[1]):.3f} N")

    print()
    print(f"SUMMARY: {sum(PASS)}/{len(PASS)} reproduction checks PASS")


if __name__ == "__main__":
    main()
