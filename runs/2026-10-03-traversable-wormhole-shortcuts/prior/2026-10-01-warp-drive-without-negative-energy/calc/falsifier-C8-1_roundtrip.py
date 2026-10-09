"""Falsifier C8-1: Earth-clock round-trip time with a Krasnikov tube vs light round trip.

Units: SI-derived astronomical (distance in light-years, time in years, speeds in units of c).
Model (Krasnikov 1998, Everett & Roman 1997): outbound leg is subluminal at v_out
(no one-way advance, consistent with Krasnikov's Proposition 1); the tube built along the
outbound path lets the return leg be made in Earth-clock time eps -> 0 (idealised).
Light round trip reference: 2 D / c with an instantaneous turnaround (stay = 0).
"""
D_ly = 4.37  # alpha Centauri, ly
stay_yr = 0.0
eps_yr = 0.0  # idealised return through tube (Krasnikov: 'arbitrarily short')
light_rt = 2 * D_ly  # yr
print(f"Light round trip (Earth clock): {light_rt:.3f} yr")
for v in (0.1, 0.5, 0.9, 0.99):
    out = D_ly / v
    rt = out + stay_yr + eps_yr
    one_way_adv = D_ly - out  # positive would be a one-way advance; must be <= 0
    print(f"v_out={v:4.2f} c: outbound {out:7.3f} yr (one-way advance {one_way_adv:+.3f} yr, never >0); "
          f"tube round trip {rt:7.3f} yr; round-trip advance over light {light_rt - rt:+.3f} yr")
# break-even outbound speed for any round-trip advance: D/v < 2D  ->  v > 0.5 c
print("Round-trip advance exists iff v_out > 0.5 c (D/v_out < 2D/c).")
