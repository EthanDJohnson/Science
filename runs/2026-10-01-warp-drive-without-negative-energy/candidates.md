# Candidate answers
exclusive: no (feasibility options: C2, C3 and C4 can all hold at once, and all three fit the faster-than-light half of the null C1. C1's claim that positive-energy shells do "nothing a massive vehicle cannot" excludes C4. C5 and C6 each contradict C1's faster-than-light half. C7 and C8 restate the question rather than compete with an answer)
lenses merged: decomposer, examiner, mechanist, dialectician, idealizer, engineer, constraints (analyses/*.md), with the math checks math/{decomposer,examiner,mechanist,dialectician,idealizer,engineer,constraints}.md
status: final

Units: geometric (G = c = 1, lengths in m) where marked "geo"; SI otherwise. β is the interior covariant shift magnitude of the 2024 shell (g_0x), in units of c, as in the run's `warp_shell.py` rebuild. C = 2GM/(c²R₂) is the shell compactness. "Rebuild" means the run's `tools/warp_shell.py` reconstruction of Fuchs et al. 2024 (M = 4.49e27 kg, R₁ = 10 m, R₂ = 20 m), whose smoothing spans are the toolkit's choice, not the paper's.

**Math-check corrections applied to this slate.** No candidate rests on a refuted claim as originally stated.
- M-CONSTRAINTS-13: β_crit is 0.0239, not 0.0244 (affects C1, C2, C3, C7).
- M-CONSTRAINTS-08: the cap at the Buchdahl compactness is ≲ 0.04–0.06, not 0.05–0.06 (C2).
- M-CONSTRAINTS-11: kinks add no surface term, which strengthens the case against C5.
- M-DECOMPOSER-09: the threshold factor is 21–80, and the Buchdahl cap ≲ 0.08 (C1, C2).
- M-DECOMPOSER-10: the "non-generic path gains nothing" lemma is refuted, so branch (c) of C6 is reopened and noted against C1.
- M-ENGINEER-05: E_flow is 0.060 Mc², not 0.03 Mc² (C7).
- M-ENGINEER-06: the assembly heat is 0.118 Mc², not 0.22 Mc² (C2).
- M-ENGINEER-15: wording only.

Not re-derived by the math checks, and so unverified: the sampled all-observer point counts (M-CONSTRAINTS-14, M-DECOMPOSER-11).

## C1: No warp spacetime moves a payload faster than light without NEC violation; positive-energy subluminal shells move payloads only as ordinary massive vehicles.
type: null
from: DECOMPOSER-A, EXAMINER-A, MECHANIST-A, MECHANIST-B, DIALECTICIAN-A, IDEALIZER-A, IDEALIZER-B, ENGINEER-A, CONSTRAINTS-A; also the eliminated fallbacks DECOMPOSER-E, CONSTRAINTS-C (semiclassical negative-energy supply) and MECHANIST-E ([speculative] negative active mass)
argument:
- **(A) Faster than light.**
  - Every metric that meets the brief's travel-time sense (Alcubierre, Natário, and Lentz if his assigned v_s is consistent) has unit lapse and flat slices, so the Santiago–Schuster–Visser theorem makes it violate the NEC [D-41].
  - Computed from the metric for all observers:
    - Alcubierre fails NEC, WEC, SEC and DEC at every sampled wall point [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-constraints_unitlapse.py].
    - Natário fails all four at every sampled wall point for every v from 0.1 to 10. The scaling T(v) = v²A + vB is exact, so this is not a superluminal effect [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-constraints_vscaling.py].
    - The zero-vorticity class (Lentz, Fell–Heisenberg, Rodal) fails the NEC at 284–288 of 312 points at every speed, and its total Eulerian energy is exactly zero (identity; see C5).
  - For lapse ≠ 1 shells, outside SSV's reach, Olum [D-59], Gao–Wald [D-60] and Visser–Bassett–Liberati [D-61] require NEC failure before any time advance. The worked shell family shows this:
    - the NEC fails at β ≈ 0.0239 (corrected, M-CONSTRAINTS-13), while a forward light advance needs β > 0.210 [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-constraints_shell.py];
    - across five masses the advance threshold lies 21–80× above the NEC threshold (corrected from "8 to 80", M-DECOMPOSER-09) [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-decomposer_thresholds.py];
    - in linear theory, advance/Shapiro delay ≤ 0.20 at the NEC cap, and a net advance needs β ≥ 0.55 [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-idealizer_thickwall.py].
  - Coasting faster than light as a whole is also closed under the DEC:
    - E ≥ |P| [new: Eichmair, Huang, Lee & Schoen 2016, JEMS 18, 83, ACCESS abstract];
    - a stationary configuration whose asymptotic Killing vector is spacelike (v > c) has p^μ = 0, so with the DEC it is flat [new: Beig & Chruściel 1996, J. Math. Phys. 37, 1939, ACCESS full-text] (kinematics verified, M-DIALECTICIAN-04).
- **(B) Moving a payload at all.**
  - The 2024 shell has P_ADM = 0 in its own frame and M_ADM = 4.511e27 kg at every β. Its conserved charges are those of a plain shell [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-constraints_shell.py] (P = 0 verified, M-MECHANIST-02).
  - The shift leaves the payload's clock rate at 0.761 [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-idealizer_payload.py].
  - The payload rides with the shell. The shift's only invariant trace is a Sagnac-type co-minus-counter light asymmetry: 6.86 ns at β = 0.02 and 13.72 ns at β = 0.04 [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-decomposer_transit_time.py].
  - Start and stop need γMv supplied from outside: ideal photon exhaust of 3.38e43 J at 0.04 c, which is 4.5e22× the payload-alone bill [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-mechanist_acceleration.py].
  - Self-propulsion is barred by conservation of ADM/Bondi momentum, except by emitting momentum. That last route is C3.
- **Eliminated fallbacks, for context.** Supplying the negative energy semiclassically fails:
  - the reference Alcubierre wall (R = 100 m, Δ = 1 m, v = 10 c) violates the Ford–Roman bound by 7.1e63;
  - complying needs Δ ≤ 1.19e-32 m, whose curvature radius (≈ 85 L_P) lies outside semiclassical validity [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-constraints_qi_horizon_trip.py] (M-CONSTRAINTS-09 verified).
  - Negative active mass [D-81] is [speculative] and excluded by the brief.
predictions:
- If true:
  - any future positive-energy faster-than-light metric, put through an all-observer or interval-certified test, shows NEC failure, a non-localized shift, or no advance;
  - every asymptotically flat superluminal coaster has zero ADM 4-momentum;
  - Le's observer-robust test of the regularized Fuchs shell finds type-IV NEC failures at v_s ≥ 0.025 and passes at ≤ 0.023;
  - any worked start-and-stop ejects ≥ γMv.
- If false: a metric appears with a certified pointwise NEC pass and a computed one-way advance between exterior rest points, or a positive-energy shell whose payload gains something (arrival time, proper time, momentum cost) that the same shell without shift does not.
evidence for: [D-41] [D-59] [D-60] [D-61] [D-05] [D-07] [D-08] [D-69]; the calcs above; [D-84] resolved by reading [new: Le, arXiv:2602.18023v6 p. 2, ACCESS full-text, "We compare four drives at matched parameters: Alcubierre, Natário, Van den Broeck, and Rodal"]. The abstract's NEC-violating walls are those four, and the regularized Fuchs shell is a separate Type-I panel (dialectician F3).
evidence against:
- **The non-generic-path lemma is refuted.** Its elimination of the non-generic-path loophole rests on "a non-generic path in vacuum is locally Minkowski and gains nothing", which M-DECOMPOSER-10 refuted: radial Schwarzschild null rays are non-generic yet curved. The null now needs the separate argument that Olum's generic condition is needed only somewhere on the path, which matter crossings supply. That argument has been sketched, not proved; see C6.
- **Finite-region gap.** Gao–Wald's K′ ≫ K caveat leaves a finite-region gap [D-60].
- **Samples, not certificates.** All energy-condition scans are samples:
  - the all-observer point counts and type splits are unverified (M-CONSTRAINTS-14; M-DECOMPOSER-11);
  - the light-shell advance of −1.87 ns at D = 1e3 m disappears at D = 1e5 m (M-DECOMPOSER-06), so even that worked advance depends on the baseline.
- **Sourcing.** Schoen–Yau/Witten is not quoted from a primary source [D-62]. The null's (B) half inherits every doubt about whether the 2024 shell is a solution at all [D-31].
decisive test:
- **Calculation:** a general bound on the one-way light-time advance through any NEC-satisfying, asymptotically flat, lapse ≠ 1 shell as a function of compactness, turning the worked family into a theorem. Alternatively, interval-certified tests (Le's Warpax method [D-73]) of any metric claimed to give an advance. Any GR or numerical-relativity group could do either now.
- **Experiment:** none tests the faster-than-light half directly.
  - The nearest premise test, for the negative-energy route, is Archimedes weighing vacuum energy. Its gap is 0.78–0.85 orders: a prototype at 3e-15 N over 1e6 s against a few × 1e-16 N needed [new: Allocca et al. 2024, EPJ Plus 139, 158, ACCESS full-text] [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-engineer_build_gaps.py]. No cryogenic-run date was found [D-19] [D-43].
  - For any propellantless "warp" thruster claim, a Tajmar-class balance below 3.3 nN/W is ready now [U-01].

## C2: The Bobrick–Martire / Fuchs 2024 warp shell is a valid positive-energy coasting vehicle: all four energy conditions hold for all observers below a compactness-set shift cap.
type: option
from: DECOMPOSER-B, EXAMINER-C, DIALECTICIAN-C, CONSTRAINTS-B, ENGINEER-B, IDEALIZER-D (as a detail); MECHANIST M4 row
argument:
- **Energy conditions in the rebuild** (published M = 4.49e27 kg, R₁ = 10 m, R₂ = 20 m):
  - At β = 0.02, NEC, WEC, SEC and DEC pass at 0 of 850 sampled points, all Hawking–Ellis type I, worst NEC margin +2.2e-5 m⁻² (geo) [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-constraints_shell.py]. M-CONSTRAINTS-06 independently gives +2.0e-5 m⁻², and M-DECOMPOSER-08 confirms the pass.
  - The zero-shift shell passes the exact type-I test with max |p|/ε = 0.60 (M-ENGINEER-02).
  - This matches Le's sampled Type-I slack of +0.021 (R_c² units) for a regularized shell at v_s = 0.02 [D-26] [new: Le, arXiv:2602.18023v6 p. 21, ACCESS full-text].
- **Shift cap (premise 7).**
  - **Bisected:** β_crit ≈ 0.0239 for the rebuild, ≈ 0.072 × C. The lens's 0.0244 ± 0.0002 was refuted as too high (M-CONSTRAINTS-13).
  - **Variants:**
    - the ratio to compactness falls from 0.082 to 0.066 as C runs 0.083–0.5;
    - a buffer of R_b = 1–2 m lowers the cap to 0.016–0.010;
    - the cap is scale-invariant to R₁ = 100 m [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-constraints_shellcap.py].
  - **Linear theory:**
    - the uniform-wall cap is 0.027 with Fuchs's sigmoid and 0.048 with a cubic profile;
    - the scale-free law is β_max ≈ k·C·(Δ/R₂), k = 0.18–0.37, with β_max → 0 for thin walls [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-idealizer_thickwall.py];
    - the DEC-necessary ceiling is ≈ 0.054 [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-mechanist_acceleration.py].
  - **At the Buchdahl compactness 8/9, the estimates disagree:**
    - ≲ 0.04–0.06 (constraints, corrected by M-CONSTRAINTS-08 from "0.05–0.06");
    - ≲ 0.08 (decomposer, corrected by M-DECOMPOSER-09 from "≲ 0.07");
    - ≲ 0.15 (dialectician, crude linear unit-lapse extrapolation, M-DIALECTICIAN-09).
- **Conserved charges:** M_ADM = 4.511e27 kg (2.376 M_J); E₊ = 1.117 M_ADM; E₋ ≈ 0 (quadrature noise) [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-constraints_shell.py]. These are toolkit outputs, not re-derived (M-CONSTRAINTS-14).
- **Grade: coast only.** Any vehicle speed v < c is a boost of the whole static solution.
- **In practice (by 2100), against demonstrated capability** [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-engineer_build_gaps.py] (verified M-ENGINEER-03):
  - mass: 22.0 orders above the ISS (419,725 kg [new: NASA Space Station Facts and Figures, ACCESS full-text]);
  - rest energy: 23.8 orders above one world-year;
  - peak density: 5.8 orders above nuclear saturation;
  - peak stress (3.9e39 Pa): 27.6 orders above 1 TPa;
  - speed: 1.5–1.8 orders above the Parker Solar Probe;
  - edge tolerance: the edge must be smoothed over ≥ 1 m, or the zero-shift shell already fails the DEC (1.16 at a 0.5 m span);
  - assembly heat: 4.75e43 J = 0.118 Mc² (GR; corrected from 9e43 J by M-ENGINEER-06);
  - TRL 1–2.
- **Scaled to a 100 m payload (ours):** 4.51e28 kg = 23.8 M_J. No size escapes the trade between mass, density and stress at fixed compactness.
predictions:
- If true: an independent, source-consistent Einstein–matter solution (elastic or anisotropic fluid with an equation of state [D-74]) reproduces the shifted shell with certified all-observer energy conditions at β ≲ 0.024, and fails them above the cap. Le-type tests at v_s ≥ 0.025 show type-IV cells.
- If false:
  - Barzegar Error 18 ("not a solution to Einstein's equations") is confirmed independently, and no matter model sustains any nonzero shift;
  - or certified tests find NEC failure already at β = 0.02;
  - or the shell is linearly unstable.
evidence for: [D-08] [D-26] [D-84] (resolved, as in C1); the rebuild scans above; idealizer F3 (an Israel static shell meets NEC/WEC/SEC for all 2M/R < 1 and the DEC up to 24/25, M-IDEALIZER-03).
evidence against:
- **Barzegar et al.** Error 18 [D-31], and Error 13 read in full: the "constant velocity warp drive" "has no meaning as long as no distinction is made between ui and ui" [new: Barzegar, Buchert & Vigneron, arXiv:2602.16495v1 p. 21, ACCESS full-text] (dialectician F2).
- **Paper's own speed fails.** The paper's Table 1 speed of 0.04 c fails the NEC at 100 of 850 points in the rebuild. The published "0.04 c" is therefore above the cap, and only the energy-condition-checked 0.02 survives.
- **What the scans show.** The energy conditions come from T = G/8π of the rebuild, not from a matter model with its own equations of motion.
- **Matter model.** Isotropic pressure cannot hold a free shell [D-74].
- **Stability.** Stability is uncomputed, and growing modes are reported for self-similar shells [D-72].
- **Sampling.** The scans sample points; they are not certificates.
- **Not a drive.** On the brief's own terms this is a vehicle shape, not a drive, since it coasts only.
decisive test:
- **Calculation:** an independent full Einstein solve of the shifted shell with a stated matter model, exact type-I or interval-certified tests at shell-edge resolution, and a linear stability analysis. Any numerical-relativity group could do it now [D-31].
- **Experiment:** none reaches a warp-scale shift.
  - The premise "matter currents source a shift" is tested only in the weak field: lunar laser ranging to about 0.1% [new: Murphy, Nordtvedt & Turyshev 2007, PRL 98, 071102, ACCESS abstract], disputed [new: Kopeikin 2007, PRL 98, 229001, ACCESS abstract]; and Jupiter light deflection at 20% [new: Kopeikin et al. 2007, GRG 39, 1583, ACCESS abstract].
  - A lab rotor beside the GINGERINO ring laser falls 5.1 orders short [new: Di Virgilio et al. 2024, PRL 133, 013601, ACCESS abstract] [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-engineer_build_gaps.py].

## C3: A positive-energy shell starts and stops only by emitting momentum (photon or gravitational-wave exhaust, e.g. Le's radiative steering), at no less than photon-rocket cost for its whole mass.
type: option
from: CONSTRAINTS-F, MECHANIST-D, DIALECTICIAN-C (start-and-stop clause), ENGINEER-D (self-propulsion eliminated), ENGINEER F12–F13, DECOMPOSER-C (momentum clause), EXAMINER P5
argument:
- **Conservation.** For an isolated, asymptotically flat system, Bondi/ADM 4-momentum changes only through flux at null infinity. The centre of mass moves at P/E [new: Nerz, arXiv:1312.6274, ACCESS full-text] [D-69].
- **Start and stop.** Reaching v and stopping therefore means emitting ≥ γMv each way.
  - The ideal photon rocket is the floor: mass ratio (1 + v)/(1 − v), which is 1.0833 at 0.04 c.
  - At 0.04 c: 3.38e43 J of exhaust (0.198 M_J; 5.7e22 world-years) for the shell plus payload, against 7.49e20 J for the payload alone [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-mechanist_acceleration.py] (M-MECHANIST-08).
  - At the cap β ≈ 0.024: mass ratio 1.050 and 2.15e26 kg radiated [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-constraints_qi_horizon_trip.py]. The momentum per leg at the corrected β_crit = 0.0239 is ≈ 3.23e34 kg m/s (M-CONSTRAINTS-13).
- **Le's construction** (preprint [D-72] [D-38]) is the only worked case: a flat cavity joined to a Kinnersley photon-rocket exterior, with strict surface DEC and m_f/m_i = e^(−3L). If L is the rapidity path length, start plus stop at 0.04 c costs 1.27, against 1.083 for a bare photon rocket [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-engineer_build_gaps.py]. The arithmetic is verified (M-ENGINEER-08); the reading of L is not.
- **Self-propelled level.** It is reachable only by gravitational-wave emission, a GW rocket. That needs ≥ 7.7% of the mass radiated for start plus stop at 0.04 c.
  - Nature makes such recoils: up to 15,000 km/s = 0.050 c in black-hole encounters [new: Sperhake et al. 2011, PRD 83, 024037, ACCESS abstract].
  - No warp construction radiates this way.
- **What does not work.**
  - Growing the shift while moving the centre needs negative energy [D-08].
  - Ramping the shift with internal forces alone leaves the shell at rest. It sends free-floating passengers into the cavity wall at 0.0263 c within 1.27 µs (M-MECHANIST-06).
  - The ramp's own stress is negligible: 9.3e-9 ε over 1 s.
- **Verdicts.**
  - In principle: allowed by conservation at the "start and stop" level, with external propulsion counted. At the "self-propelled" level, only as a GW rocket, and no construction exists.
  - In practice by 2100: eliminated with the C2 shell. The exhaust energy alone is 22.75 orders above one world-year. For a worked start-and-stop the TRL is 1 (a preprint junction construction only) [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-engineer_build_gaps.py].
predictions:
- If true:
  - an exact accelerating positive-energy solution shows Bondi mass loss equal to the emitted momentum;
  - no construction beats the photon-rocket mass ratio for the total (shell plus payload) mass;
  - the propulsion bill stays ≈ 4.5e22× the payload-alone bill for the published shell.
- If false: a time-dependent positive-energy solution changes its ADM momentum with zero flux at infinity, which would contradict conservation, or a start-and-stop construction keeps the energy conditions without any exhaust.
evidence for: [D-07] ("any warp drive requires propulsion"); [D-08]; [D-38]; [D-69]; [D-72]; the calcs above.
evidence against:
- The only construction is a preprint. Self-gravitating settling after a turn is open, and growing normal modes are reported [D-72].
- No primary-source theorem on an isolated warp spacetime changing its own ADM momentum was found [D-69].
- Le's L is unread.
- This "works" only in the sense that a rocket works: the shell multiplies the bill by 22.65 orders.
decisive test:
- **Reading:** fix Le's L by reading arXiv:2606.22531v4 (a reading, not mathematics).
- **Calculation:** a numerical-relativity evolution of a pushed matter shell with a stated equation of state, checking the energy conditions and the Bondi balance through the acceleration.
- **Observation:** the gravitational-wave memory of boosting the 2.4 M_J shell to 0.04 c is ≈ 3.5e-22 at 1 kpc (Newtonian-order, optimal orientation; M-ENGINEER-13). That is a technosignature, not a build test. Any propellantless claim must beat 3.3 nN/W on a Tajmar-class balance [U-01].

## C4: A compact positive-energy shell, pushed externally, drags its interior inertial frames so the payload accelerates without felt g-forces: the one merit where it might beat a rocket.
type: mechanism
from: MECHANIST-C, IDEALIZER F12 (with the "felt acceleration" clause of IDEALIZER-C), ENGINEER F13 / ENGINEER-C (clock-slowing gain); opposed by EXAMINER-E, IDEALIZER-F and CONSTRAINTS-E
argument:
- **(a) Inductive dragging (main sub-hypothesis).**
  - In linear harmonic gauge, a shell pushed with acceleration A gives interior test particles an acceleration κA, with κ ≈ 4GM/(c²R).
  - For the published mass, κ = 0.67 at R = 20 m and 1.33 at R = 10 m. Linear theory has broken down there, so strong dragging is plausible [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-mechanist_acceleration.py] [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-idealizer_payload.py]. This is verified only within the stated model, which ignores the pusher's stresses and retardation (M-MECHANIST-10, M-IDEALIZER-12).
  - Strong-field models exist in which the interior of an accelerated shell "stays flat" and test particles are dragged [new: Pfister et al. 2005, CQG 22, 4743, ACCESS abstract]. The EM analogue induces an opposing interior field [new: Lynden-Bell, Bičák & Katz 1999, Ann. Phys. 271, 1, ACCESS abstract].
  - The Fuchs narrative (u_i conserved during an unsolved acceleration) needs exactly this effect [new: Fuchs et al. 2024, arXiv:2405.02709 p. 4, ACCESS full-text].
  - It needs mass and compactness, not the shift.
- **(b) Clock slowing (weaker sub-hypothesis).** The interior lapse of 0.761 makes the 109.2 yr coast at 0.04 c take 83.1 yr of crew time (M-MECHANIST-09).
- **Verdicts.** In principle: open, since no strong-field time-dependent solution exists. In practice: inherits C2's 22–28-order gaps.
predictions:
- If true: a nonlinear evolution of a pushed shell at C ≈ 0.3–0.9, below horizon formation and the Buchdahl limit, shows the payload's proper acceleration well below the shell's coordinate acceleration (κ → 1).
- If false: the payload needs a contact force comparable to an unshielded rocket's, as Le states for his construction ("an observer needs a force to follow the accelerating cavity center" [D-72]).
evidence for: as listed under argument; [D-08].
evidence against:
- No time-dependent solution exists [D-08] [D-15].
- Le's construction requires a force on the payload [D-72].
- κ is a linear coefficient used where it fails.
- The momentum bill is unchanged at 4.5e22× the payload alone.
- Sub-hypothesis (b) is weak:
  - the shift leaves the clock rate unchanged (IDEALIZER-F);
  - a rocket at 0.649 c gives the same slowing (M-CONSTRAINTS-10);
  - a 1 g photon rocket reaches α Cen in 3.58 yr of ship time, against 83 yr [D-39].
- Even if (a) holds, the merit belongs to any massive shell, not to warp geometry.
decisive test:
- **Calculation:** numerical relativity of a compact elastic or fluid shell [D-74] pushed by a modelled exhaust, measuring the payload's proper acceleration against the shell's. Any numerical-relativity group could do it. No result is expected on any known timeline.
- **Experiment:** none. κ is 3.0e-24 for 1e3 kg at 1 m [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-mechanist_acceleration.py], about 20 orders below laboratory relevance. Weak-field frame dragging is measured only around the Earth (GP-B about 19%; LAGEOS/LARES about 2%) [D-42a] [D-42b].

## C5: Lentz's Einstein–Maxwell–plasma soliton moves a payload faster than light with non-negative energy, because its non-smooth source evades the unit-lapse no-go theorems.
type: option
from: EXAMINER-D, DIALECTICIAN-D, CONSTRAINTS-D, ENGINEER-E, MECHANIST M2 (all eliminated by their lenses; kept as the strongest published positive-energy faster-than-light claim); Fell–Heisenberg folded in as the same zero-vorticity class (WEC failure conceded [D-05])
argument:
- **The case for.**
  - Lentz claims everywhere-positive Eulerian density, with E_tot ~ C v_s²R²/w of order "(few)×10⁻¹ M_sun v_s²" at R = 100 m, w = 1 m [D-30a].
  - He replies that the divergence argument fails because his density is only C⁰ on the planes x = 0, y = 0 [D-30].
  - He argues that the theorems assume "a single fastest causal path" [new: Lentz, arXiv:2006.07125 p. 12, ACCESS full-text].
- **The surviving escape.** Lentz's potential obeys a hyperbolic equation, ∂_x²φ + ∂_y²φ − (2/v_h²)∂_z²φ = ρ [D-06]. A source of that equation can radiate φ along the cones r_⊥ = (v_h/√2)|z| (characteristics verified, M-DIALECTICIAN-03). A non-localized wake of that kind lies outside SSV's localization hypothesis.
- **Build cost if it existed:** 20–50 M_sun of organized plasma at v = 10 c, i.e. 3.6e48–8.9e48 J. That is 41.6–42.0 orders above NIF's 8.6 MJ and 27.8–28.2 orders above one world-year (M-ENGINEER-14).
- **Verdicts.**
  - In principle: every lens eliminates it as a localized, asymptotically flat solution.
  - In practice: TRL 1 (contested), since no source has been exhibited.
predictions:
- If true: an exhibited localized Lentz solution has ∫ρ_E > 0 (bulk plus sheets) and passes the NEC for all observers, including Israel-junction sheets at its non-smooth planes.
- If false:
  - the bulk Eulerian energy integrates to exactly zero, so negative regions must exist;
  - any kinked wall puts a compensating sheet of equal size on the kink plane;
  - only a φ that does not decay (outside asymptotic flatness) escapes.
evidence for: [D-06] [D-30a]; Lentz's replies [D-30].
evidence against:
- **SSV names the metric.** SSV covers it explicitly, with no fastest-path premise [D-41].
- **Divergence identity.** For any curl-free, localized shift on flat slices, 16πρ_E is an exact divergence, so ∫ρ_E = 0 (M-CONSTRAINTS-03, M-DIALECTICIAN-01).
  - This holds for continuous, piecewise-C¹ shifts too. A kink in ∂X adds no surface term (M-CONSTRAINTS-11). That check refuted the constraints lens's surface-term mechanism in the direction that strengthens the elimination.
  - A kink in φ moves an exactly equal and opposite amount into an Eulerian sheet (M-DIALECTICIAN-02). The sheet carries the negative part only when [g′]g(0) > 0.
- **Rest-frame density.** Eulerian momentum vanishes identically in this class (J ≡ 0, M-CONSTRAINTS-04), so ρ_E is the rest-frame density, and a negative ρ_E is a WEC failure of the source itself.
- **Smooth proxy.** It fails the NEC at 284–288 of 312 points at every speed [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-constraints_vscaling.py]. The counts are unverified (M-CONSTRAINTS-14).
- **Other critiques:**
  - Celmaster & Rubin (preprint) find negative regions [D-30];
  - the speed is assigned, not derived [new: Lentz, arXiv:2006.07125 p. 6, ACCESS full-text];
  - no full plasma solution is exhibited [D-06];
  - by Beig–Chruściel, an asymptotically flat superluminal coaster has zero ADM 4-momentum, so E_tot cannot be an ADM mass (dialectician S3).
decisive test:
- **Calculation:** an Israel-junction (distributional) energy-condition analysis of Lentz's actual rhomboid potential, plus the far-field decay rate of his hyperbolic φ. Faster than r^(−1/2) means localized, so the identity applies; otherwise the solution is outside the brief's definition. Any GR group could do it now.
- **Literature:** a Lentz reply to Celmaster & Rubin, if one appears.

## C6: Faster-than-light travel without pointwise negative energy is possible by breaking a hypothesis of the time-advance theorems: asymptotic flatness, null completeness, the generic condition, or stationarity.
type: option
from: DECOMPOSER-D, EXAMINER-F, DIALECTICIAN-E
argument: Named sub-hypotheses, each a theorem hypothesis to break:
- **(a) Not asymptotically flat.** Example: the Garattini–Zatrimaylov de Sitter bubble, which moves at the expansion speed with energy conditions holding "up to a total divergence term" [D-75].
- **(b) Distributional or singular sources, or null incompleteness,** which escape Gao–Wald's completeness hypothesis [D-60].
- **(c) A non-generic fastest path, escaping Olum's generic condition [D-59].**
  - DECOMPOSER-D eliminated this branch with the lemma "a non-generic path in vacuum with no tidal force is locally Minkowski and gains nothing". That lemma is refuted (M-DECOMPOSER-10): radial Schwarzschild null geodesics fail the generic condition while the Kretschmann scalar is 48M²/r⁶ ≠ 0.
  - Branch (c) is therefore not eliminated by that argument. It is restated here as open pending the separate argument that Olum needs the generic condition only somewhere on the path.
  - The counterexample's rays are Shapiro-delayed, not advanced, so the refutation reopens the branch without supplying an advance.
- **(d) Non-stationary (accelerating) phases.** These escape the Beig–Chruściel coasting no-go, but not Olum or Gao–Wald.
- **(e) WEC-satisfying but DEC-violating "superluminal matter"** (Bobrick–Martire Classes II/III [D-65]). This escapes the positive-mass argument but not Olum, since WEC implies NEC (M-DECOMPOSER-01). The brief classes it as an "unphysical source".
- **Verdicts.**
  - In principle: (a) falls outside the brief's asymptotically flat, pointwise definition. (b) and (c) are open only as long as no proof closes them. (d) and (e) remain under Olum and Gao–Wald.
  - In practice: no construction exists in any branch, so TRL 0.
predictions:
- If true: an exhibited metric with a certified pointwise NEC pass and a computed one-way advance between rest points of its exterior, achieved by violating one named hypothesis.
- If false:
  - every construction in (a)–(e) shows a pointwise NEC failure, or no advance relative to local light;
  - sheets in (b) fail their own Israel surface NEC;
  - de Sitter "faster than light" in (a) is cosmological recession, not a time advance in the brief's sense.
evidence for: [D-75]; Gao–Wald's own caveat that K′ may be far larger than K [D-60]; the refutation M-DECOMPOSER-10 above.
evidence against:
- No construction exists in any branch.
- (a) holds only in an averaged sense and lies outside the brief's pointwise, asymptotically flat definition [D-75].
- (b): Israel sheets carry their own surface stress, which must meet the NEC (decomposer ledger P6).
- (d) and (e) stay under Olum and Gao–Wald.
- Krasnikov's argument bars hastening arrival in globally hyperbolic spacetimes whatever the energy sign [new: Krasnikov, PRD 57, 4760 (1998), ACCESS abstract].
decisive test:
- **Calculation for (a):** a pointwise NEC certificate and a travel-time comparison against local light between comoving points for the Garattini–Zatrimaylov bubble.
- **Proof for (c):** that any path crossing matter satisfies Olum's generic condition through R_ab k^a k^b = 8π(ε + p_r) > 0, so that non-generic fastest paths are confined to vacuum and gain nothing.
- Theorists could do both now. No experiment applies.

## C7: The "positive-energy warp effect" is internal frame dragging by counter-streaming wall currents with zero net momentum, so the real question is shift per unit compactness and cost against a rocket.
type: reframe
from: DIALECTICIAN-B, IDEALIZER-C, IDEALIZER-E, CONSTRAINTS-E, ENGINEER-C, DECOMPOSER-C, EXAMINER-E (reframe R3) and examiner reframe R2, MECHANIST M9
argument: The doubtful premises are brief premise 4 (that the 2024 shell is a drive) and premise 10 (that "move a payload at all" is a meaningful bar).
- **The interior shift is a gravitomagnetic solenoid.**
  - It is sourced by poloidal wall currents, T_0i = (1/16π)∇×∇×w in linear theory, whose net momentum is exactly zero (M-DIALECTICIAN-08, M-IDEALIZER-05, M-MECHANIST-01).
  - Each sign carries 6.8e34 kg m/s (0.050 M_ADM c) at β = 0.02 (M-MECHANIST-03).
  - B_g vanishes in the cavity, so the cavity shows no gyroscope precession and no tidal change.
- **On a thin shell the shift is exactly gauge.** A boost maps the interior to Minkowski space, leaving a prolate cavity (M-IDEALIZER-01, -02).
- **The gauge-invariant separator premise 4 asks for:**
  - ADM 3-momentum: 0 for the warp shell, γMv for the same shell boosted (dialectician S1);
  - the Sagnac flux: 8.0 ns at β = 0.04 in linear theory, against Fuchs's 7.6 ns [D-25] [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-idealizer_thickwall.py]. Table 1 is a co-minus-counter difference, not an advance: an Alcubierre check gives 8.006 ns = 4Rv/c (M-EXAMINER-03), and the paper's footnote on photon paths "with or against the rotation" confirms the reading [new: Fuchs et al. 2024, arXiv:2405.02709 p. 25, ACCESS full-text].
- **The "passengers" do not ride.** Fuchs's u_i = 0 passengers drift at b/α = 0.026 c relative to the shell and reach the wall in 1.27 µs from the centre (M-IDEALIZER-10; 3.3 µs Killing time across the full diameter, M-DIALECTICIAN-06). A payload at rest relative to the shell gains only a clock deficit of 3.4e-4.
- **Counterflow law:** β ~ C·(u/c). Corrected (M-ENGINEER-05), β = 0.02 needs a flowing energy E_flow ≥ 2cP = 2.42e43 J = 0.060 Mc², a whole-mass counterflow of 0.060 c. The 0.03 Mc² first reported counted one stream.
- **Cap:** ≈ 0.072·C for the rebuild profile (corrected, M-CONSTRAINTS-13).
- **Reframed question:** "What is the largest interior frame drag positive matter of compactness C can produce, and does any interior rearrangement lower the propulsion cost below a photon rocket's?" The run's answers are about 0.07·C, and no.
predictions:
- If the reframe is right:
  - every gauge-invariant cavity observable differs from the plain shell's only through the gravitomagnetic flux (Sagnac);
  - g_00 and B_g in the cavity are unchanged;
  - the nonlinear cap follows β_max ∝ C·Δ/R₂, vanishing for thin walls.
- If wrong: a nonlinear solution shows a local cavity invariant (B_g ≠ 0, or a change in g_00 at fixed matter) caused by the shift, or a nonzero net wall momentum at second order in β.
evidence for: [D-07] [D-09] [D-25] [D-64]; [new: Fuchs et al. 2024, arXiv:2405.02709 p. 27, ACCESS full-text, "creating a linear frame dragging inside the shell"]; the calcs above.
evidence against:
- The linear models are used at compactness 0.33–0.67, valid only to a factor of about 2 (M-IDEALIZER math, unverified nonlinear validity).
- Second-order net momentum is unchecked (M-DIALECTICIAN-08).
- Fuchs's "0.04 c" label is not tied to a stated definition.
- Whether the shell is a solution at all is contested [D-31].
decisive test:
- **Calculation:** nonlinear solves of shifted shells at several Δ/R₂ and C, with Warp Factory or `tools/numeric_stress_energy.py`, to test the scaling law and compute the second-order net momentum.
- **Experiment:** weak-field translational gravitomagnetism is already confirmed (LLR, disputed; Jupiter 20%). A lab rotor with a ring laser is 5.1 orders short (M-ENGINEER-11).

## C8: The binding obstacle to faster-than-light warp travel is causal access to the bubble's front wall, not the energy sign; operationally, travellers cannot hasten arrival even with negative energy.
type: reframe
from: EXAMINER-B (reframe R1 and the O1 definitions table), DECOMPOSER load-bearing assumption (P2 with P3)
argument: The doubtful premise is brief premise 2, together with the brief's travel-time definition.
- **"|β| > N" is gauge-dependent.** At Alcubierre's flat centre the shift is 10 > N = 1 in exterior coordinates and 0 in comoving ones. The invariant is the norm of the comoving Killing vector, −1 + v²(1 − f)². At v = 10 it changes sign at r = 99.45 m, so the whole exterior lies beyond a horizon relative to the payload (M-EXAMINER-02).
- **The horizon** has T_H = 1.3e-3 K (M-CONSTRAINTS-09). This brings in the Everett–Roman control problem and the Finazzi–Liberati–Barceló instability [D-13] [D-71].
- **The eternal bubble's advance is not a launch.** The bubble's time advance (0.437 yr against 4.37 yr to α Cen at 10 c, M-EXAMINER-01) belongs to a metric already laid along the path, not to a drive launched from A.
- **Operationally it is barred.** "Under some reasonable assumptions in globally hyperbolic spacetimes the traveller cannot hasten reaching the destination" [new: Krasnikov, PRD 57, 4760 (1998), ACCESS abstract].
- **The authors concede it.**
  - Lentz's abstract names the creation difficulty [new: Lentz, arXiv:2006.07125 p. 1, ACCESS full-text].
  - Fell–Heisenberg concede that horizons prevent transport across the light barrier [D-05].
- **Reframed question:** "Can matter arranged by a traveller at A, within A's causal future, give a payload a net advance to B over light through the asymptotic exterior?" The theorems answer no, whatever the energy sign. Pre-placed infrastructure along the route (a Krasnikov tube) is the real alternative.
predictions:
- If the reframe is right: every bubble launched from rest using only matter in the launch event's causal future gives no time advance, or needs pre-placed matter or a breakdown of global hyperbolicity, even with negative energy allowed.
- If wrong: a launch-from-rest construction, inside A's causal future, gives an advance.
evidence for: [D-05] [D-13] [D-71]; the cited checks.
evidence against:
- Krasnikov's argument is cited from its abstract only, and its "reasonable assumptions" were not examined.
- Krasnikov tubes are out of scope by the brief except as a reframe.
- The reframe changes the question rather than answering the brief's travel-time definition (d), which C1 addresses.
decisive test:
- **Calculation:** extend Krasnikov's argument to the brief's travel-time definition, or attempt a numerical-relativity or semiclassical launch-from-rest of an Alcubierre-type bubble whose source lies in the causal future of the launch event. Theorists could do either now.
- **Experiment:** none applies.
