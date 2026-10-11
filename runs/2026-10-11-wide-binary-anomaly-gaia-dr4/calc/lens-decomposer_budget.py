#!/usr/bin/env python3
"""Decomposer lens: split the published DR3 gamma gap (Chae ~1.37 vs Newton-side ~1.0) into
sample, estimator-family and pipeline/model parts, using only dossier numbers (dimensionless gamma).

Chain on (approximately) ONE catalogue, Chae's 2024 sample (D-22, D-31):
  Chae 2024b family-1 pipeline:            gamma = 10^(2*0.068) = 1.368      [D-22]
  Boufourou full-median (E1-like) on it:   gamma ~ 1.12 (global) - 1.20 (deep) [D-31]
  Boufourou E2 tail-truncated on it:       1.045                              [D-31]
  Boufourou E3 mixture on it:              1.05                               [D-31]
Family 4 on ONE dataset of 36 pairs (D-26): 1.56 (Chae-like deprojection) vs 1.00 (independent a).
Sample flip (D-29): Cookson family-2 test, d<150 pc w/o ipd cut -> MOND 12x preferred; with cut -> Newton 88x.
Gap shares are in ln(gamma).
"""
import math

chae = 10 ** (2 * 0.068)
e1_lo, e1_hi = 1.12, 1.20
e2 = 1.045
tot = math.log(chae / e2)
print(f"Chae 2024b gamma = {chae:.3f}; total ln-gap to E2 = {tot:.3f}")
for lab, e1 in (("E1 global 1.12", e1_lo), ("E1 deep 1.20", e1_hi)):
    pipe = math.log(chae / e1)
    est = math.log(e1 / e2)
    print(f"{lab}: pipeline/calibration part ln = {pipe:.3f} ({100 * pipe / tot:.0f}%), "
          f"estimator-family part ln = {est:.3f} ({100 * est / tot:.0f}%)")
print(f"E3 vs E2 on same data: ln = {math.log(1.05 / 1.045):.4f}")
fam4 = math.log(1.56 / 1.00)
print(f"Family-4 deprojection-prior swing on 36 pairs: ln = {fam4:.3f}  (ratio {1.56 / 1.00:.2f}) -> exceeds the whole family-1 gap ln {math.log(chae):.3f}: {fam4 > math.log(chae)}")
# Generator-based full-median triple bias (from lens-decomposer_transfer.py.log): differential TEST/CAL
for f, d in ((0.2, 1.075), (0.3, 1.128)):
    print(f"f_triple={f}: generator differential residual {d:.3f}; share of Chae ln-gap explained = {100 * math.log(d) / math.log(chae):.0f}%")
# Boufourou bias claim 1.08-1.13 as share
for b in (1.08, 1.13):
    print(f"Boufourou E1 Newtonian bias {b}: share of ln(1.368) = {100 * math.log(b) / math.log(chae):.0f}%")
