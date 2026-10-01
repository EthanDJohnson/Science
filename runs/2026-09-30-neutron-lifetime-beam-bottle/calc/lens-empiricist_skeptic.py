"""Empiricist lens: precision an honest skeptic's deciding measurements need, and the size of the historical
bottle-average shift relative to the present gap. Units: s (SI).
Inputs: gap and class means from lens-empiricist_partitions.py log (proton beam 887.97 +- 2.04 s; storage/rest
878.41 +- 0.25 s; material 880.03 +- 0.49 s; magnetic 877.83 +- 0.29 s); history from Serebrov & Fomin 2010
(arXiv:1005.4312): PDG 2006 885.7 +- 0.8 s vs Serebrov 2005 878.5 +- 0.8 s.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import stats_tools as st

gap = 887.97 - 878.41
sig_rest = 0.25
print(f"Gap proton-beam minus storage: {gap:.2f} s")
for z in (3.0, 5.0):
    tot = st.precision_needed(gap, z)
    own = math.sqrt(max(tot**2 - sig_rest**2, 0))
    print(f"  to tell a new measurement at one value from the other at {z:.0f} sigma: total sigma on difference {tot:.2f} s;"
          f" new-measurement sigma allowed {own:.2f} s (storage value error {sig_rest} s)")

# A new proton-counting beam (BL2/BL3) must also tell 'BL1 was right' from 'BL1 was off'. If BL2 lands at the storage
# value, its disagreement with BL1 (sigma 2.25 s) is what exposes a systematic. The 'which' question is separate.
bl1 = 2.25
for s_new in (1.0, 0.5, 0.3):
    t = st.tension(887.7, bl1, 878.41, s_new)
    t2 = st.tension(887.97, 2.04, 878.41, math.hypot(s_new, sig_rest))
    print(f"  new beam at storage value with sigma {s_new} s: vs BL1 z {t['z']:.2f}; beam-class mean shift test (new vs storage) z if at 888 s: "
          f"{gap/math.hypot(s_new, sig_rest):.1f}")

# Material vs magnetic sub-anomaly
d_mm = 880.03 - 877.83
for z in (3.0, 5.0):
    tot = st.precision_needed(d_mm, z)
    print(f"Material-magnetic difference {d_mm:.2f} s: needs sigma on difference {tot:.2f} s at {z:.0f} sigma; "
          f"new material bottle alone would need {math.sqrt(max(tot**2-0.29**2,0)):.2f} s")

# Electron-counting (J-PARC/LiNA) or in-bottle beta counting (UCNProBe): decide dark-decay (reads ~888) vs proton-systematic (reads ~878)
for s_new in (4.16, 2.0, 1.0):
    print(f"Electron-counting or in-bottle beta counting with sigma {s_new} s separates 888 vs 878.4 at z = {gap/math.hypot(s_new, 0.25):.2f}")

# Historical bottle shift
t = st.tension(885.7, 0.8, 878.5, 0.8)
print(f"\nHistory: PDG 2006 (885.7 +- 0.8 s) vs Serebrov 2005 (878.5 +- 0.8 s): diff {t['difference']:.1f} s, z {t['z']:.2f};"
      f" as a fraction of today's gap {t['difference']/gap:.2f}")
