# Audit of report.md
status: final
| # | Report claim | Traced to | Status |
|---|---|---|---|
| 1 | Factor-2 relaxation on the dodge task: range +117.8 %, thrust +28.3, motor tau +5.9, latency +5.5, drag +1.8 | calc/falsifier-C7-0_factor2.py.log prints exactly these | supported |
| 2 | Bottom line: ordering "proved to hold for every parameter value"; also stated in C1 as "e_s = 1 > e_a < 1/2 > \|e_tau\| proved over the whole domain (M-DIAL-06, M-EXAMINER-01)" | math/dialectician.md M-DIAL-06 proves e_s = 1, e_a in (0, 1/2), e_tau in (-1, 0). Only the dominance of range over each other term is proved. "\|e_tau\| < 1/2" is not proved (M-STAT-06 has \|e_tau\| = 0.5 at tau = 161-343 ms), and the thrust > motor lag > latency > drag order is shown at one parameter point only. Range-over-all-others does hold in closed form (also calc C8 log: strict ordering e_s > e_a > \|e_tau\| at 80/80 grid points, not "every value") | contradicted (overstated: "\|e_tau\| < 1/2" is wrong and the full ordering is not proved for all parameters) |
| 3 | Range elasticity +0.986 (3->6 m) / +1.082 (6->10 m), M-SIMULATOR-07 verified, reproduced by three refuters to 0.13 % | C4 log: +0.986, +1.085, reproduction 0.00 / 0.00 / 0.13 % (one script, one point at 0.13 %) | supported (the "three refuters" wording not fully traced; 1.085 vs 1.082 minor) |
| 4 | Usable stereo range 4.1-5.8 m at 50 mm baseline | M-MECH-06 verified (4.106 m, 5.807 m) | supported |
| 5 | Plant verification: energy drift 5.9e-12, ang. momentum 7.1e-15, RK4 order 4.005, 8.9e-16 | 7.1e-15 and 4.005 reproduced in C2 drift log; others in lens-simulator_verify.py.log (not reopened) | supported |
| 6 | Lowest hardware-capped ceiling 9.55 m/s (4.1 m, a_u 16.3); 0.96x the 10 m/s point | falsifier-C4-0 log (C) | supported |
| 7 | One hardware swap (range 6->10 m) gives +74 % vs C4's 20 % threshold | C4 log (B): +74.1 % | supported |
| 8 | Horizontal-FoV reading gives caps 9.9-17.4 m/s | C1 slack log D: 9.85-17.40 m/s | supported |
| 9 | A-21 bounds 12.0 / 13.2 / 13.5 m/s, slack 1.6-3.8x at 7 m/s | dossier A-21; C1 slack log A, B (range legs 1.57-3.82x) | supported |
| 10 | Unseen-course hardware 10/10 at 5, 8/10 at 7, 6/10 at 10 m/s; CP lower 0.741; p = 0.264 | M-STAT-01, M-STAT-02 verified; dossier A-20 | supported |
| 11 | "Clopper-Pearson lower bound 0.49" for 8/10 | Not printed in any log or math row found; plausible by calculation but untraced | unsupported (minor) |
| 12 | Flights to certify: 29 / 46 / 76 (0/1/3 failures) | M-STAT-11 corrected form | supported |
| 13 | M-MECH-03: FoV +4.67 % vs range +5.85 %; leg (1b) demoted | math/mechanist.md M-MECH-03 refuted-row | supported |
| 14 | C1 hardware evidence: failure at 7 m/s attributed to late field-of-view entry [D-13] | dossier line 70 (quote "objects entered the field of view very late because of the high ...") | supported |
| 15 | SUPER: "over 20 m/s in unknown environments", ~3x depth-camera figures; 1.55x Swift mean | C3 log (B): 2.71x vs unseen geo-mean, 1.552x vs Swift; source is abstract plus press only | weak (search summary / abstract; the report flags this itself) |
| 16 | C2: VIO ATE 98.2 and 47.2 m at 19.4 m/s; Gate-IO 0.48; IMO 0.56 m | dossier lines 56-67, 101-105 (Cioffi et al., quoted table) | supported |
| 17 | Blur rotation-dominated above 229 deg/s | M-MECH-07 verified | supported |
| 18 | Drift elasticity -0.023 and -0.191; 12.5 % of distance tolerated by A-20 | C2 drift log | supported |
| 19 | Latency elimination: elasticities -0.03 to -0.36; human vs Swift \|e\| 0.016-0.113 (0.02-0.11) | M-EMP-05 log: 0.0163 to 0.1126 (lens 0.122; empiricist.md summary says 0.02-0.14). -0.03 to -0.36 consistent with M-STAT-05/06 | supported |
| 20 | C7: 10.73 and 10.85 m/s coincide to 1.1 % (M-EXAMINER-08) | C4 log (E): 1.11 % | supported |
| 21 | C7: top term leads by 4.16x; seven of seven spreads exceed 2; 2.33 on endpoints | C7 factor2 log (4.161; 2.326, 3.992, 3.050, 7.570, 2.230, 5.260) | supported |
| 22 | C4: 0/20 vs 17/20, p < 1e-6 (trial counts inferred) | M-STAT-09 z = 5.44, p = 5.4e-8, verified; counts inferred per its own note | weak (trial counts inferred; a single paper) |
| 23 | C3 elimination: seen/unseen 1.54-1.92x in mean class; 1.29x best vs best; chi2 71.8 vs 53.3; 1.2-1.9x | C3 split log (A3, C, E: 1.152, 1.540, 1.919, 1.288, 71.78 vs 53.26) | supported |
| 24 | C5: elasticity to installed thrust +0.0000 at 8.5->12 N; +0.527 was the 6->7.5 N arc; halving motor lag +15.8 % | C5 envelope log | supported |
| 25 | C5 vs headline: thrust gives +28 % per doubling (bottom line) while elasticity to installed thrust is 0.00 at measured value | Different tasks (dodge vs slalom at tol 0.20 m; the C5 log shows envelope active at tol 0.50 m only). Both logged, but the report places them in tension without reconciling it | weak (unreconciled; the +28 % holds only on the dodge task) |
| 26 | C6: closed-loop error 0.151 / 0.202 m vs 0.445 / 0.503 m open-loop; removing aero model error gives x0.59-0.77 | C6 aero log | supported |
| 27 | C6: Table VIII 0.147 vs 0.371 m; Tal and Karaman 6.6 cm at 12.9 m/s | verdicts/C6-0.md lines 45-54, 91 (6.6 cm yes); the "12.9 m/s" and the paper itself were not independently opened | weak (single secondary trace, verdict file only) |
| 28 | C8: partials closed form, strict order 80/80; 26 min of air time | C8 log lines 33, 63 (25.9 min) | supported |
| 29 | M-STAT-11 and M-STAT-12 refuted two of C8's statistical legs | math/statistician.md refuted rows; they concern flight counts and look-elsewhere z, not specifically C8's legs | weak (attribution to C8 not traced) |
| 30 | Pack sag costs about 10 % of speed [M-MECH-09 corrected] | M-MECH-09 refuted-and-corrected: -9.7 % | supported |
| 31 | Delay margins 27.57 ms vs 2.00; 354.0 vs 22.5 ms | M-SIMULATOR-05 verified | supported |
| 32 | Time-optimal denominator 4.502 s flying start, 5.039 s rest-to-rest, 98.315 m | 4.502 s and 98.315 m in logs (C5, C2); 5.039 s and "12 per cent longer" taken from M-SIMULATOR-01 note, ratio 1.119 consistent | supported |
| 33 | Hardware T/W sweep d ln(lap)/d ln(TWR) = -0.565 | dossier A-16; M-STAT-07 verified | supported |
| 34 | Hardware attribution: "range 7 -> ... the one large range increment on hardware"; 120-250 flights test plan | Derived from 29/46 per cell over ~4-6 cells; arithmetic only | supported |
| 35 | Math checks refuted list (M-MECH-03/04/09, M-SIMULATOR-11/12/13, M-STAT-11/12, ...) "none reversed a ranking" | Matches refuted rows found; M-MECH-03 did invert FoV vs range within C1 (the report says so). M-SIMULATOR-12 refuted "2 to 10x every rival" (true span 1.87-7.57x), which the report's "4x largest elasticity" avoids | supported |
| 36 | Probabilities sum: 0.40+0.12+0.11+0.10+0.07+0.06+0.05+0.05+0.04 | = 1.00, slate exclusive with "none of these" | supported |
| 37 | Bottom line: range doubling +118 % vs thrust +28 % "on a verified simulation of a 0.75 kg racing quadrotor" | Verified plant (24/24) per C2/C4 logs; omissions (drift, blur, sag, flapping) stated in the report's assumptions | supported |

## Summary: 37 claims checked, 7 flagged; most serious: the bottom line says the ordering of all limits "is proved to hold for every parameter value", and C1 states "e_a < 1/2 > \|e_tau\|". M-DIAL-06 proves only that range elasticity (exactly 1) exceeds each of the others. \|e_tau\| is bounded by 1, not 1/2 (it reaches 0.5 at tau of 161-343 ms), and the order among thrust, motor lag, latency and drag is shown at one parameter point. Smaller flags: the CP lower bound 0.49 is untraced; +28 % thrust sits unreconciled beside the C5 result of 0.00 elasticity on a different task; SUPER, the Tal and Karaman figure and the A-14 trial counts rest on abstracts, secondary files or inferred counts.
