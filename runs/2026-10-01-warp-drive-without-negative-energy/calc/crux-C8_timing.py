"""Crux C8: one formula for the Krasnikov-tube timings the three C8 verdicts quote.

Units: years and light-years, c = 1 (so 1 ly per yr). Flat exterior (k = 1).
Krasnikov Example 5 / Everett-Roman: the traveller flies out A -> B at speed v (< 1),
laying the tube inside J+(departure). In the tube, a homeward null ray satisfies
dt = -(1 - delta) |dx| (verdict C8-0's null vector l_I = -(1-delta) d_t - d_x),
so the fastest return loses coordinate time (1 - delta) D.

Quantities printed:
  t_B            = D / v                      arrival at B (first one-way trip)
  t_light_AB     = D                          light from A's launch event to B
  one-way advance = t_light_AB - t_B          (never > 0 for v <= 1)
  t_home         = D/v - (1 - delta) D        return through the tube (ideal, return speed -> light in tube)
  light from B at departure reaches A at D/v + D
  return-leg advance = (D/v + D) - t_home = (2 - delta) D   (independent of v)
  round trip shorter than light round trip (2D)  iff  v > 1/(3 - delta)
  C8-1's idealisation (instantaneous return, Delta t_return = 0): threshold v > 0.5
"""

D = 4.37  # ly, distance to alpha Cen (dossier D-39)

print("D = %.2f ly (c = 1, years)" % D)
for v in (0.1, 0.5, 0.9, 0.99, 0.999999):
    for delta in (0.1, 0.01):
        tB = D / v
        one_way_adv = D - tB
        t_home = D / v - (1 - delta) * D
        light_from_B_at_A = D / v + D
        ret_adv = light_from_B_at_A - t_home
        rt_adv = 2 * D - t_home
        print("v=%.6f delta=%.2f: t_B=%.3f yr; one-way advance=%.3f yr; "
              "t_home=%.4f yr; return-leg advance=%.3f yr; round-trip advance vs 2D light=%.3f yr; "
              "home before departure? %s"
              % (v, delta, tB, one_way_adv, t_home, ret_adv, rt_adv, t_home < 0))
    # C8-1's idealised instantaneous return
    print("   C8-1 instantaneous-return round trip at v=%.6f: %.3f yr (advance %.3f yr)"
          % (v, D / v, 2 * D - D / v))

for delta in (0.1, 0.01):
    print("round-trip advance threshold with tube return (delta=%.2f): v > %.4f c" % (delta, 1 / (3 - delta)))
print("round-trip advance threshold with instantaneous return (C8-1): v > 0.5000 c")
print("one-way first-arrival advance is max(D - D/v) over v<=1 = %.3f yr (never positive)" % 0.0)
