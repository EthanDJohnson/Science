#!/usr/bin/env python3
"""Refuter C8-0.  Does the one-at-a-time partial derivative exist, and is the metric an observable?

Three independent tests, SI units throughout (m, s, m/s, m/s^2).

TEST A (symbolic).  C8 defect (3) says: "The partial derivative does not exist as an operation.
Perception range and braking acceleration are exact substitutes in the stop bound (e_s + e_a = 1
identically)".  I re-derive the stop bound from scratch, write all three partials in closed form,
show the identity e_s + e_a = 1 is Euler's theorem for a function homogeneous of degree one in
(s, a) -- a statement ABOUT the partials, which therefore exist -- and test whether the two are
"exact substitutes" in the only sense that would block a ranking: a constant marginal rate of
substitution.  They are not: the iso-speed trade rate e_s/e_a = (W+tau)/(W-tau) varies over the
dossier's own parameter box, and e_s > e_a strictly whenever tau > 0, so the two are strictly
ordered, not degenerate.

TEST B (ordering robustness).  The ordering of the three elasticities over a box of operating
points covering the dossier's ranges, to see whether a ranking exists and where it changes.

TEST C (arithmetic on the simulator lens's own verified one-at-a-time table).  Arc elasticities
ln(v2/v1)/ln(x2/x1) recomputed from the speeds printed in
calc/lens-simulator_sweep.py.log (gate tol 0.20 m, plant perturbed, controller nominal,
bandwidth retuned by the model's closed-form rule).  M-SIMULATOR-07 independently re-derived this
elasticity table and verdict "verified".  If these numbers are separated, the operation C8 calls
unavailable has already been carried out on a verified plant.

TEST D (observability cost).  C8's own decisive test, costed in cumulative air time: how much
flying is needed to turn the metric into a measurement at the Clopper-Pearson n C8 itself derives.
"""
import math

import sympy as sp

print("=" * 78)
print("TEST A -- do the partials exist, and are range and braking 'exact substitutes'?")
print("=" * 78)

s, a, tau, v, k = sp.symbols("s a tau v k", positive=True)

# stop bound: travel s while reacting for tau at speed v then braking at a
constraint = sp.Eq(v * tau + v**2 / (2 * a), s)
sols = sp.solve(constraint, v)
vstar = [x for x in sols if sp.simplify(sp.limit(x, tau, 0)) != 0]
vstar = sp.simplify(vstar[0])
print("stop bound solved from v*tau + v^2/(2a) = s :  v =", vstar)

# all three partials, in closed form
dv_ds = sp.simplify(sp.diff(vstar, s))
dv_da = sp.simplify(sp.diff(vstar, a))
dv_dtau = sp.simplify(sp.diff(vstar, tau))
print("dv/ds   =", dv_ds)
print("dv/da   =", dv_da)
print("dv/dtau =", dv_dtau)
print("all three partials are finite closed-form expressions: the operation exists")

W = sp.sqrt(tau**2 + 2 * s / a)
e_s = sp.simplify(s / vstar * dv_ds)
e_a = sp.simplify(a / vstar * dv_da)
e_tau = sp.simplify(tau / vstar * dv_dtau)
print("e_s   - (W+tau)/(2W)  simplifies to", sp.simplify(e_s - (W + tau) / (2 * W)))
print("e_a   - (W-tau)/(2W)  simplifies to", sp.simplify(e_a - (W - tau) / (2 * W)))
print("e_tau - (-tau/W)      simplifies to", sp.simplify(e_tau + tau / W))
print("e_s + e_a - 1         simplifies to", sp.simplify(e_s + e_a - 1))

# Euler's theorem: the identity is a CONSEQUENCE of degree-1 homogeneity in (s,a)
hom = sp.simplify(vstar.subs({s: k * s, a: k * a}) - k * vstar)
print("homogeneity check  v(ks,ka,tau) - k v(s,a,tau) =", hom,
      "  -> degree-1 homogeneous in (s,a), so Euler gives e_s + e_a = 1")

# are they EXACT substitutes?  that requires a constant marginal rate of substitution.
mrs = sp.simplify(dv_ds / dv_da)                      # ds/da along an iso-v curve (up to sign)
print("MRS (dv/ds)/(dv/da) =", sp.simplify(mrs))
print("d/dtau of MRS =", sp.simplify(sp.diff(mrs, tau)),
      " -> not identically zero, so the MRS is NOT constant: not exact substitutes")

print()
print("=" * 78)
print("TEST B -- is there an ordering, and over what regime does it hold?")
print("=" * 78)


def elas(s_, a_, tau_):
    W_ = math.sqrt(tau_**2 + 2 * s_ / a_)
    return ((W_ + tau_) / (2 * W_), (W_ - tau_) / (2 * W_), -tau_ / W_)


op = (6.0, 39.0, 0.040)                      # dossier operating point used by the examiner lens
es, ea, et = elas(*op)
vop = op[1] * (-op[2] + math.sqrt(op[2] ** 2 + 2 * op[0] / op[1]))
print(f"operating point s={op[0]} m, a={op[1]} m/s^2, tau={op[2]*1e3:.0f} ms -> v = {vop:.4f} m/s")
print(f"  e_s = {es:.4f}   e_a = {ea:.4f}   e_tau = {et:.4f}")
print(f"  e_s/e_a = {es/ea:.4f}   e_s/|e_tau| = {es/abs(et):.3f}")
print("  strict ordering e_s > e_a > |e_tau| at the operating point:", es > ea > abs(et))

box_s = [3.0, 6.0, 9.0, 12.0]
box_a = [20.0, 30.0, 39.0, 44.3]
box_t = [0.005, 0.017, 0.040, 0.080, 0.130]
n = flip_at = 0
flips = []
for s_ in box_s:
    for a_ in box_a:
        for t_ in box_t:
            es_, ea_, et_ = elas(s_, a_, t_)
            n += 1
            if not (es_ > ea_ > abs(et_)):
                flip_at += 1
                flips.append((s_, a_, t_ * 1e3, es_, ea_, et_))
print(f"box of {n} operating points: strict ordering e_s > e_a > |e_tau| holds at "
      f"{n - flip_at}/{n}")
print("  e_s > e_a everywhere in the box:",
      all(elas(s_, a_, t_)[0] > elas(s_, a_, t_)[1]
          for s_ in box_s for a_ in box_a for t_ in box_t))
print("  points where latency overtakes braking (the regime boundary):")
for f in flips:
    print(f"    s={f[0]:5.1f} m a={f[1]:5.1f} m/s^2 tau={f[2]:6.1f} ms  "
          f"e_s={f[3]:.3f} e_a={f[4]:.3f} e_tau={f[5]:.3f}")

print()
print("=" * 78)
print("TEST C -- arc elasticities of the simulator lens's one-at-a-time table")
print("    source: calc/lens-simulator_sweep.py.log, gate tol 0.20 m; the elasticity table")
print("    was independently re-derived and marked 'verified' in M-SIMULATOR-07")
print("=" * 78)


def arc(v1, v2, x1, x2):
    return math.log(v2 / v1) / math.log(x2 / x1)


rows = [
    # label, (x1, v1), (x2, v2)   -- x in its own units, v in m/s
    ("motor_tau   local 19.55->39.1 ms", (19.55, 18.719), (39.10, 16.165)),
    ("motor_tau   wide  5->78.2 ms    ", (5.00, 19.862), (78.20, 7.954)),
    ("tau_vio     local 20->40 ms     ", (20.0, 16.165), (40.0, 14.514)),
    ("tau_vio     wide  10->130 ms    ", (10.0, 17.419), (130.0, 10.601)),
    ("tau_imu     local 0.5->2 ms     ", (0.5, 16.852), (2.0, 15.468)),
    ("tau_imu     wide  0.5->5 ms     ", (0.5, 16.852), (5.0, 11.249)),
    ("thrust_max  6->10 N (tol 0.50)  ", (6.0, 16.840), (10.0, 19.600)),
]
vals = {}
for lab, (x1, v1), (x2, v2) in rows:
    e = arc(v1, v2, x1, x2)
    vals[lab.strip()] = e
    print(f"  {lab}  e = {e:+.4f}")

loc = {"motor_tau": vals["motor_tau   local 19.55->39.1 ms"],
       "tau_vio": vals["tau_vio     local 20->40 ms"],
       "tau_imu": vals["tau_imu     local 0.5->2 ms"],
       "thrust": vals["thrust_max  6->10 N (tol 0.50)"]}
wide = {"motor_tau": vals["motor_tau   wide  5->78.2 ms"],
        "tau_vio": vals["tau_vio     wide  10->130 ms"],
        "tau_imu": vals["tau_imu     wide  0.5->5 ms"]}
order_loc = sorted(loc, key=lambda q: -abs(loc[q]))
order_wide = sorted(wide, key=lambda q: -abs(wide[q]))
print("  |e| ranking, local perturbations :", " > ".join(order_loc))
print("  |e| ranking, wide  perturbations :", " > ".join(order_wide))
print("  ranking of the three shared axes invariant to perturbation span:",
      order_wide == [q for q in order_loc if q in wide])
sp_loc = max(abs(x) for x in loc.values()) / min(abs(x) for x in loc.values())
print(f"  spread of the four local elasticities (max|e|/min|e|) = {sp_loc:.2f}x")
print("  so one-at-a-time perturbation on the verified 17-state plant returns"
      " distinct, ordered numbers")

print()
print("=" * 78)
print("TEST D -- what would it cost to make the metric an observation?")
print("    C8's own decisive test: 29 flawless flights per speed bin, 4 bins")
print("=" * 78)
n_bin, bins = 29, 4
course_len = 98.315                      # m, the simulator lens's slalom arc length
for sp_ in (5.0, 7.0, 9.0, 11.0):
    print(f"  one traversal at {sp_:4.1f} m/s over {course_len:.1f} m = "
          f"{course_len/sp_:5.1f} s of flight")
air = sum(course_len / sp_ for sp_ in (5.0, 7.0, 9.0, 11.0)) * n_bin
print(f"  {n_bin} flights x {bins} bins = {n_bin*bins} traversals, "
      f"{air:.0f} s = {air/60:.1f} min of cumulative air time")
print(f"  with a 3.0 min usable hover endurance per pack: "
      f"{air/60/3.0:.1f} pack-equivalents of flight energy")
print(f"  at 8 trials/hour including turnaround: {n_bin*bins/8:.0f} h of range time")
print("  Clopper-Pearson lower bound at 29/29, one-sided 95 per cent: "
      f"{0.05**(1/29):.4f}  (>= 0.90: {0.05**(1/29) >= 0.90})")
print("  the quantity is therefore measurable with 2026 hardware at a cost of tens of")
print("  minutes of air time: it is UNMEASURED, not unobservable")

print()
print("=" * 78)
print("TEST E -- C8 defect (4): is the IMU-vs-VIO latency gap 'a factor of 20'?")
print("=" * 78)
e_imu, e_vio = 0.062, 0.132                    # C8's own quoted elasticities
t_imu = math.sqrt(0.5 * 2.0)                   # geometric-mean tau of the 0.5-2 ms interval, ms
t_vio = math.sqrt(10.0 * 40.0)                 # geometric-mean tau of the 10-40 ms interval, ms
print(f"  elasticity ratio                     = {e_vio/e_imu:.3f}x   (C8 says 20)")
print(f"  per-millisecond derivative ratio     = "
      f"{(e_imu/t_imu)/(e_vio/t_vio):.3f}x   (matches the 9.39 that M-SIMULATOR-07 verified)")
print("  neither route gives 20: C8's own factor is wrong by 2.1x to 9.4x")
