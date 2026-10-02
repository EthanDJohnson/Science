# Analysis: mechanist (causes and mechanisms)
status: final

## Method applied
For each way a warp-type spacetime could move a payload, I write the causal chain (what produces the shift or curvature, what it acts on, what sustains it, what ends it), classify the mechanism by kind of phenomenon and governing theory, and evidence each link from the dossier or a calculation in `calc/`. The brief assigns this lens the acceleration phase (premise 5): what a time-dependent shift requires, and what momentum and energy must be supplied or ejected to start and stop.

## Findings
1. **The 2024 shell's own account of what its shift is for.** Fuchs et al. present the coasting shift as the residue of an acceleration phase they do not solve: "If the drive undergoes acceleration with a condition of dui/dt = 0, then having a shift vector during the constant velocity phase is required as the passengers prior to this point had ui/u0 < vs and only a shift vector can provide the require[d] dxi/dt" [new: Fuchs et al. 2024, arXiv:2405.02709, full-text, p. 4, "If the drive undergoes acceleration with a condition of dui/dt = 0, then having a shift vector during the constant velocity phase is required"]. They also say "we will focus on analyzing the constant velocity phase of warp flight" (same source, p. 4). So the shift is a memory of an assumed, unsolved, inertia-free acceleration; the coasting solution says nothing about whether that acceleration exists [D-08].
2. **Rebuilt shell at the published parameters (toolkit, not my code).** `warp_shell.py shell --M "2.365 Mjup" --R1 "10 m" --R2 "20 m" --beta 0.02` gives M_ADM = 4.51e27 kg (2.376 M_J), 2GM_ADM/(c²R₂) = 0.335, centre lapse 0.761, interior shift −0.02 c, and an Eulerian speed relative to the shell at the centre of 0.0263 c, in the frame "comoving with the shell = asymptotic rest frame of the Schwarzschild exterior". The zero-shift shell passes the exact type-I NEC/WEC/SEC/DEC test, with max |p|/ε = 0.60 (SI; toolkit output, run by me, not saved to a log; the constraints lens owns the shifted-shell table). The lapse and Eulerian-speed values are re-used as inputs in [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-mechanist_acceleration.py].
3. **In its own rest frame the coasting warp shell has zero ADM momentum.** In the shell frame the exterior is static Schwarzschild with zero shift [D-08; Finding 2], so K_ij = 0 near infinity and the ADM momentum P_i = (1/8π)∮(K_ij − K h_ij)dS^j vanishes exactly (standard ADM definition; my statement, not quoted from a source). The linearized momentum constraint confirms it pointwise. For β_x = β₀f(r) on a flat slice, j_x = −(β₀/16π)[f″ sin²θ + f′(1 + cos²θ)/r] (geometric; θ from the x axis; checked symbolically). Its volume integral is (8π/3)[r²f′] at the endpoints, which is zero. At the published profile the numerical total is 1.4e-6 of either signed part [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-mechanist_acceleration.py]. **Mechanism:** the interior shift is produced by counter-streaming momentum inside the wall, a "gravitomagnetic solenoid", not by any net motion. Each signed part is P₊ = −P₋ = 6.8e34 kg m/s = 0.050 M_ADM c at β_int = 0.02, and 1.35e35 kg m/s = 0.10 M_ADM c at β_int = 0.04 (SI). In a two-thin-layer harmonic-gauge equivalent, layers each holding M/2 would counter-stream at u = 0.060 c (β = 0.02) and 0.119 c (β = 0.04). Linear theory at compactness 0.33–0.67 is a scale estimate, not a solution.
4. **The internal currents are what bound the shift (premise 7, linear estimate).** The DEC requires |T^{0i}| ≤ T^{00}, so the pointwise linear momentum density must stay below the shell's own energy density. With the rebuilt density profile, the worst ratio is |T^{0x}|/ε = 18.6 β_int at r = 12.2 m. The necessary condition therefore fails above β_int ≈ 0.054 c. At β_int = 0.02 the worst ratio is 0.37; at 0.04 it is 0.74. All of the momentum sits where the density is positive; the apparent r < 6.6 m points are 1e-14-level finite-difference noise [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-mechanist_acceleration.py]. This is a necessary, linear-order condition, not a full DEC test. It suggests the published 0.02–0.04 c sits close to a matter-supported ceiling of about 0.05 c for this density profile, consistent with the authors' qualitative "momentum flux" cap [D-64]. A cruder two-layer cap, using the energy budget E_in + E_out ≤ Mc² with |P| ≤ E/c in each layer, is β_cc ≤ C₁ − C₂ = 2GM/(c²R₁) − 2GM/(c²R₂) = 0.335 for this shell. It stays below 1 for any horizon-free single shell only in the thin-wall limit, and linear theory is outside its validity there.
5. **Ramping the shift with internal forces alone does not carry the payload; it throws it at the wall.** In the shell frame a time-dependent uniform interior shift gives a uniform gravito-electric field, a ≈ −c ∂_tβ in linear order. A payload initially at rest relative to the shell ends the ramp moving at the interior Eulerian speed, 0.0263 c relative to the shell (Finding 2). It then crosses R₁ = 10 m in 1.27 µs. The 2.4 M_J shell recoils by 1.7e-16 m/s (SI) [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-mechanist_acceleration.py]. This is gravitational induction (classical field, linearized GR). Momentum is exchanged between payload and currents, and the ADM momentum is unchanged. To keep the payload riding with the shell, the shell itself must be moved. This agrees with the authors' statement that moving the centre while growing the shift needs negative energy or mass shedding [D-08], and with Bobrick–Martire's "any warp drive requires propulsion" [D-07, D-69].
6. **The ramp itself costs the energy conditions little if it is slow.** In the unit-lapse, flat-slice estimate, the extra stress is S_ramp ~ β₀|f′|/(8π cτ) (geometric), against ε at the mid-wall. Ramping to β = 0.04 over cτ = 10 m (τ = 33 ns) gives S_ramp/ε = 0.28; over τ = 3.3 µs, 2.8e-3; over τ = 1 s, 9.3e-9 [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-mechanist_acceleration.py]. So, at order of magnitude, the time-dependence of the shift is not where the energy conditions break. They break in the momentum budget (Finding 7), and in any attempt to move the centre without exhaust [D-08].
7. **Start-and-stop budget: everything must be pushed.** With an ideal photon rocket (or an ideal one-sided GW beam, the only "self-propulsion" the brief admits), start then stop at v needs a mass ratio of (1 + v)/(1 − v). At 0.04 c that is 1.0833. For shell plus payload, the momentum to supply is 5.41e34 kg m/s and the exhaust energy is 3.38e43 J (3.76e26 kg = 0.198 M_J; 5.7e22 years of world primary energy at 592.2 EJ/yr [D-46]). For the 1e5 kg payload alone it is 7.49e20 J, 1.26 world-years. The ratio is 4.5e22 (SI) [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-mechanist_acceleration.py], matching the dossier's shell-to-payload mass ratio [D-23, D-39]. Pushing the shell at 1 g needs 1.33e37 W of exhaust, 3.5e10 L_sun, for 14.2 days to reach 0.04 c.
8. **The only passenger benefit found is clock slowing, and it is small.** With centre lapse 0.761, the 0.04 c coast to α Cen (109.2 yr exterior) takes 83.1 yr of passenger proper time; at 0.02 c, 218.5 yr becomes 166.3 yr [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-mechanist_acceleration.py]. A 1 g photon rocket takes 3.58 yr ship time [D-39]. This is Bobrick–Martire's "slow down the time" effect [D-07, D-37]: a gravitational-redshift (lapse) effect of the shell's mass, present with zero shift.
9. **Inertia-free acceleration (no g-forces) by induction drag is the one mechanism that could make a pushed shell beat a pushed payload, and only in strong field.** In linear theory, a shell pushed with acceleration A drags interior inertial frames by a fraction κ ≈ 4GM/(c²R). This is my harmonic-gauge estimate, from the uniform interior h₀ᵢ of a moving shell; the stresses of the pushing agent are ignored, so it is low confidence. For the published shell κ is formally 1.34 at R₁ and 0.67 at R₂, so linear theory has failed: full dragging plausibly needs compactness of order unity. At 1 M_J and R = 100 m, κ = 0.056 [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-mechanist_acceleration.py]. The Fuchs narrative needs exactly this (u_i conserved during acceleration, Finding 1), but no solution exhibits it [D-08, D-31].

10. **Gravitational-wave self-propulsion is permitted, and nature reaches 0.05 c with it, but only as a GW rocket.** With no matter flux, the ADM/Bondi momentum changes only through radiated momentum [D-69]. The ideal bound is the photon-rocket bound: 3.9% of the mass radiated, fully beamed, per 0.04 c leg, and 7.7% (3.47e26 kg, 3.1e43 J) for start plus stop of the published shell [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-mechanist_acceleration.py]. Numerical relativity shows such kicks exist: "In astrophysical, quasicircular inspirals, such kicks can be as large as ~3,000 km/s; here, we find configurations that exceed ~15,000 km/s. We find that the maximum recoil is to a good approximation proportional to the total amount of energy radiated in gravitational waves" [new: Sperhake et al. 2011, PRD 83 024037, arXiv:1011.3281, abstract (fetched), quote as printed]. 15,000 km/s = 0.050 c (ours). Those kicks come from ultrarelativistic black-hole encounters, and no warp construction radiates this way.
11. **Swimming or gliding in curved spacetime gives displacement, not speed.** "An extended test body moving in a curved spacetime does not typically follow a geodesic, because of forces that arise from couplings between its multipole moments and the ambient curvature … Wisdom … showed that the motion of a quasi-rigid body undergoing cyclic changes of shape in a curved spacetime deviates, in general, from a geodesic" [new: Mendes et al. 2017, arXiv:1707.08870, abstract]. It needs external curvature and conserves the momentum of the isolated system, so it is not a drive. I computed no magnitude.
12. **Induction of an oppositely directed interior field by an accelerated shell is established in the EM analogue, with gravitational analogues discussed.** "When a charged insulating spherical shell is uniformly accelerated, an oppositely directed electric field is produced inside … We discuss gravitational analogues" [new: Lynden-Bell, Bičák & Katz 1999, Ann. Phys. 271 1, arXiv:gr-qc/9812033, abstract (fetched)]. They also report that inside a balanced shell "the acceleration of a free test particle, relative to a static observer, is reduced correspondingly" by the interior g₀₀ ratio (same source). This supports the existence of the induction link in Findings 5 and 9, not my κ coefficient.
13. **No lab-scale handle on induction drag.** κ ≈ 4GM/(c²R) is 3.0e-24 for 1e3 kg at 1 m and 3.0e-22 for 1e6 kg at 10 m [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-mechanist_acceleration.py]. Weak-field gravitomagnetism is measured only around the Earth, at about 19% (GP-B) and a claimed 2% (LAGEOS/LARES) [D-18, D-42a, D-42b].

## Lens-specific outputs

### Causal chains

Convention: ds² = −N²c²dt² + h_ij(dxⁱ + βⁱdt)(dxʲ + βʲdt), with the shell or bubble frame stated per row. "Assumed" marks a link with no dossier or calculation support.

**M1. Alcubierre / Natário bubble (superluminal or subluminal, unit lapse, flat slices).**
- Produces: a localized shift gradient (expansion for Alcubierre, shear only for Natário) on a flat slice [D-01, D-02].
- Acts on: the payload region's inertial frames, which are carried at v_s relative to the exterior. The payload is geodesic [D-01].
- Sustained by: stress-energy with negative Eulerian density, in the wall toroid for Alcubierre and the whole wall for Natário [D-02]. The NEC fails for every observer class in the generic Natário family [D-41, D-58]. The source must be exotic matter, or a quantum vacuum state limited by quantum inequalities to walls of about 1e-32 m at v = 10 c [D-29, D-67]. Lab "negative energy" is sub-vacuum noise, not a gravitating source [D-16].
- Ended by: removing the wall. Superluminally, the centre cannot create or control the front wall [D-13], and the renormalized stress-energy grows exponentially there [D-13]. Collapse radiates GWs [D-14].
- Class: exotic matter or quantum vacuum effect. Theory: classical GR plus QFT in curved spacetime.
- Weakest link: a macroscopic, sustained negative-energy source. Test: no lab test reaches gravitating negative energy (D-16, D-19). The decisive calculation is the QI bound itself [D-67].

**M2. Lentz soliton (EM-plasma source, unit lapse, flat slices).**
- Produces: a shift from a scalar potential with hyperbolic source equation [D-06].
- Acts on: the interior, as M1.
- Sustained by: a claimed Einstein–Maxwell-plasma source. No full solution of the coupled system is exhibited [D-06]. Positivity is shown only for Eulerian observers, and the NEC theorem names this metric [D-41, D-30]. The direct recomputation finds negative regions (preprint) [D-30].
- Ended by: not addressed.
- Class: as claimed, classical field (EM plus plasma); in fact exotic matter, by D-41.
- Weakest link: the sustaining link, which fails by theorem.

**M3. Fell–Heisenberg (unit lapse, flat slices).** The authors concede ρ + p_i < 0 [D-05]. Exotic matter. Their "superluminal" is |β| > N, not a time advance [D-05]. Weakest link: the sustaining link, conceded by the authors.

**M4. Positive-matter warp shell (Bobrick–Martire Class I; Fuchs et al. 2024).**
- Produces: in the shell frame, a static massive shell with a Schwarzschild exterior and zero exterior shift [D-08, Finding 2], plus an interior shift. The shift is generated by counter-streaming momentum in the wall with zero net momentum (Finding 3): a gravitomagnetic "solenoid".
- Acts on: interior inertial frames, which have a uniform shift. Locally this is pure gauge (flat interior). Its invariant traces are the Sagnac-type round-trip delay [D-09, D-25] and, while β changes, an induction field −c∂_tβ that kicks free payloads (Finding 5).
- Sustained by: the shell's own stresses (a TOV pressure or elastic hoop stress [D-74]) plus the internal currents. The linear momentum-density condition |T^{0i}| ≤ ε fails above β_int ≈ 0.054 c for this profile (Finding 4). Whether a matter model sustains the shell is contested [D-31, D-74].
- Moves at v only because the whole shell is boosted, carrying ADM momentum γMv (Finding 3).
- Ended by: nothing in the coasting solution. Stopping needs the same external momentum as starting (Finding 7).
- Class: classical field (GR gravitomagnetism) plus material property. Theory: classical GR.
- Weakest link: whether it is a solution with a self-consistent matter model [D-31] and, for transport, the unsolved acceleration [D-08]. Test: the decisive calculation is a time-dependent numerical-relativity solve of a pushed shell with a matter model obeying its equations of motion (frontier: none exists [D-15, §6]). No experiment reaches the strong-field shift (Finding 13).

**M5. Radiative steering (Le, preprint) [D-72, D-38].**
- Produces: a flat cavity joined to a Kinnersley photon-rocket exterior.
- Acts on: the whole shell. Its momentum changes by anisotropic photon emission.
- Sustained by: a surface layer obeying the strict DEC, with mass loss m_f/m_i = e^(−3L).
- Ended by: stopping the emission.
- Class: classical field (radiation reaction). Theory: classical GR.
- Weakest link: the mass cost. If L is the rapidity path length (not checked), e^(−3L) is the cube of an ideal photon rocket's e^(−L), so it would never beat a photon rocket [D-69]. Stability after a turn is open [D-72].

**M6. GW self-propulsion (GW rocket) (Finding 10).**
- Produces: an anisotropic emission of gravitational waves by internal motions.
- Acts on: the Bondi momentum of the system.
- Sustained by: internal energy converted to GW. At least 7.7% of the mass is needed for start plus stop at 0.04 c.
- Ended by: when the emission stops.
- Class: classical field. Theory: GR (Bondi mass loss).
- Weakest link: no mechanism beams GWs efficiently from a non-compact shell. Assumed; natural examples need black-hole mergers.

**M7. Inductive (inertia-free) acceleration of a pushed shell (Findings 5, 9, 12).**
- Produces: an external push (M5 or a rocket) accelerates the shell. Its wall currents and bulk motion induce an interior field that accelerates the payload with it.
- Acts on: the payload, which needs no contact force if the dragging is complete.
- Sustained by: the push and the shell's compactness. Linear κ ≈ 4GM/(c²R), so κ → 1 needs compactness of order unity.
- Class: classical field (gravito-electric induction). Theory: GR.
- Weakest link: whether complete dragging is reachable below horizon formation and the Buchdahl limit, in a time-dependent solution. Assumed, not computed. This is the only place a warp shell could beat a rocket: survivable acceleration far above the g-limit.

**M8. Lapse (gravitational-redshift) clock slowing [D-07, D-37, Finding 8].** Mass produces N < 1 inside. It slows passenger clocks by 24% for the published shell. Classical field. Weakest link: none physically; it is simply small, and it is unrelated to the shift.

**M9. Mundane misreadings (measurement or gauge artefact).**
- "Constant velocity" is a Galilean or Lorentz boost of the shell frame [D-31 Error 13 untested; Finding 3].
- "Superluminal" for F-H and Lentz means |β| > N (ergoregion), not a time advance [D-05].
- The Fuchs time-delay table's sign is unresolved [D-33].
- Eulerian-only positivity [D-04].
- Class: measurement or normalization artefact.

**M10. [speculative] negative-mass dipole self-acceleration [D-81]; scalar-tensor "metamaterial" coupling [D-70].** Classes: exotic matter, or new interaction. Excluded from established physics by the brief. D-70 is itself a no-go.

### Mechanism classification table

| Mechanism | Class | Governing theory | Moves payload? (coast / start-stop / self-propelled) | Needs negative energy? | Status |
|---|---|---|---|---|---|
| M1 Alcubierre / Natário | exotic matter / quantum vacuum | GR + QFTCS (QIs) | coast; start-stop unsolved; self-propelled no (zero ADM mass, control problem) | yes [D-02, D-41] | strained (exotic) |
| M2 Lentz | claimed classical field; actually exotic | GR + Einstein–Maxwell-plasma | coast only | yes, by theorem [D-41]; contested [D-30] | eliminated as positive-energy |
| M3 Fell–Heisenberg | exotic matter | GR | coast only | yes (conceded) [D-05] | eliminated as positive-energy |
| M4 positive warp shell | classical field + material | GR | coast only | no at coast, if valid [D-08, D-31]; moving the centre without exhaust needs it [D-08] | surviving as a vehicle shape |
| M5 radiative steering | classical field (radiation) | GR | start-stop, externally powered (own exhaust) | no (preprint) [D-72] | surviving, no better than a photon rocket |
| M6 GW rocket | classical field | GR | self-propelled via GW only | no | strained (no construction) |
| M7 induction drag | classical field | GR | start-stop with a pushed shell | no (assumed) | strained (strong field, unsolved) |
| M8 lapse clock slowing | classical field | GR | n/a (passenger benefit) | no | surviving, small (24%) |
| M9 artefacts | measurement / gauge | — | — | — | reframe |
| M10 negative mass | [speculative] | — | self-propelled | yes | eliminated (not established physics) |

### Acceleration-phase ledger (brief's assigned calculation)

| Quantity | Value (SI) | Source |
|---|---|---|
| ADM momentum of the coasting shell, own frame | 0 exactly (static exterior) | Finding 3 |
| Counter-streaming momentum per sign, β_int = 0.02 / 0.04 | 6.8e34 / 1.35e35 kg m/s (0.050 / 0.10 M_ADM c) | calc A |
| Linear momentum-density ceiling on β_int (|T^{0x}| ≤ ε) | ≈ 0.054 c | calc F |
| Extra stress from ramping β to 0.04 over 1 s, relative to ε | 9.3e-9 | calc F |
| Payload kick if β ramps with no shell motion | 0.0263 c relative to shell; hits the wall in 1.27 µs | calc E |
| Momentum to supply, start at 0.04 c (shell + 1e5 kg) | 5.41e34 kg m/s | calc D |
| Ideal photon exhaust, start plus stop at 0.04 c | 3.38e43 J = 0.198 M_J = 5.7e22 world-years | calc D |
| Same, payload alone | 7.49e20 J = 1.26 world-years | calc D |
| Exhaust power to push the shell at 1 g | 1.33e37 W = 3.5e10 L_sun | calc F |
| GW-rocket mass fraction, start plus stop at 0.04 c | 7.7% (3.47e26 kg) | calc G |

## Calculations
- `runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-mechanist_acceleration.py` (log beside it). All results are SI unless marked geometric.
  - **A.** Symbolic check of the linearized momentum density of a localized uniform interior shift, residual 0.0. Numerical P₊ = 6.758e34 kg m/s (β = 0.02) and 1.352e35 kg m/s (β = 0.04), with net total 1.4e-6 of P₊ (numerical). The two-layer equivalent gives u = 0.060 c and 0.119 c.
  - **B.** Two-layer linear cap β ≤ C₁ − C₂ = 0.335.
  - **C.** Linear drag κ = 1.34 (R₁) and 0.67 (R₂) for the published shell, 0.056 for 1 M_J at 100 m.
  - **D.** Start-and-stop budgets at 0.02, 0.04 and 0.1 c: shell-to-payload energy ratio 4.51e22.
  - **E.** Passenger proper time 83.1 yr (0.04 c) and 166.3 yr (0.02 c), against 109.2 and 218.5 yr exterior. Payload wall-crossing 1.27 µs; shell recoil 1.7e-16 m/s.
  - **F.** |T^{0x}|/ε worst 18.6 β_int at r = 12.2 m, giving a ceiling of 0.054 c. Ramp-stress ratios. Shell push power at 1 g, 1.33e37 W.
  - **G.** Lab κ 3.0e-24 (1e3 kg, 1 m). GW-rocket fraction 7.7%. 15,000 km/s = 0.050 c.
- `warp_shell.py shell` (toolkit) at the published parameters: M_ADM 4.51e27 kg, centre lapse 0.761, Eulerian speed relative to the shell 0.0263 c.

## Candidate answers (at least 3; the null and a reframe count)
- [MECHANIST-A] **Null, part 1.** Every mechanism that moves a payload faster than light (M1–M3) is sustained only by negative-energy (NEC-violating) stress-energy. The positive-energy proposals of 2020–21 fail at the sustaining link. | status: surviving | why: every superluminal candidate is in the unit-lapse flat-slice class covered by D-41; F-H concede the violation [D-05]; Olum and Gao–Wald need the WEC or NEC for any time advance [D-59, D-60] | test: a positive-energy metric with N ≠ 1 or curved slices that shows a genuine travel-time advance in the examiner's test; the decisive calculation is an all-observer NEC check of any such metric | confidence: high
- [MECHANIST-B] **Null, part 2: the positive-energy warp shell is a massive vehicle.** Its shift is the gravitomagnetic field of internal counter-streaming currents, with zero ADM momentum in its own frame. It moves only if the whole 2.4 M_J shell is pushed: about 3.4e43 J of ideal photon exhaust for start plus stop at 0.04 c, 4.5e22 times the cost for the payload alone. It cannot self-propel except as a GW or photon rocket. | status: surviving | why: Findings 3, 5, 7, 10; consistent with D-07, D-08, D-69 | test: a time-dependent solution in which a positive-energy shell changes its ADM momentum with no exhaust would refute it; the ADM conservation law forbids that | confidence: high (momentum accounting); medium (counter-current numbers, linear theory)
- [MECHANIST-C] **Reframe: what the shift can give is inductive, inertia-free acceleration of the payload inside an externally pushed shell (M7), plus 24% clock slowing (M8). It does not give speed or energy savings.** The induction needs strong-field compactness (linear κ ≈ 4GM/(c²R) ~ 1). For the published density profile, matter-supported currents cap the shift near 0.05 c. | status: strained | why: no time-dependent solution exists [D-08, D-15]; the κ coefficient is my linear estimate (Finding 9); the 0.054 c ceiling is a linear necessary condition (Finding 4) | test: the decisive calculation is numerical relativity of a pushed compact shell with an elastic or fluid matter model [D-74], measuring the payload's proper acceleration against the shell's; no experiment is within 20 orders (Finding 13) | confidence: low
- [MECHANIST-D] **Radiative self-propulsion (M5, M6) is the only positive-energy start-and-stop mechanism, and it is a rocket.** The ideal cost is (1 + v)/(1 − v) in mass ratio, 7.7% of the shell's mass at 0.04 c. Le's construction reports e^(−3L), which is worse. | status: surviving (in principle) / eliminated as an advantage | why: Bondi momentum balance [D-69]; superkicks show radiated-momentum recoils to 0.05 c in black-hole encounters [new: Sperhake et al. 2011] | test: check whether Le's L is rapidity, which would make e^(−3L) strictly worse than a photon rocket; this is a reading, not an experiment | confidence: medium
- [MECHANIST-E] [speculative] Self-acceleration with no exhaust needs negative active mass [D-81] or a modified coupling [D-70]. | status: eliminated under established physics | why: brief's admissibility rules; D-70 is a no-go | test: any detection of negative active gravitational mass | confidence: high (as eliminated)

## What would change my mind
- A time-dependent, positive-energy (all-observer NEC/DEC) solution in which a shell plus payload changes its ADM momentum with no matter or radiation flux at infinity. That would contradict the conservation law and would mean I had misapplied it.
- A full nonlinear calculation showing a Fuchs-type interior shift with nonzero net wall momentum while the exterior stays static. That would break Finding 3's mechanism.
- A nonlinear DEC test of the shifted shell showing |T^{0i}| ≪ ε well above β = 0.05 c. That would move the Finding 4 ceiling.
- A strong-field calculation showing complete inductive drag (κ = 1) below 8/9 compactness. That would upgrade MECHANIST-C, and make "no g-forces at high acceleration" a real advantage over rockets.

## Assumptions I relied on
- Linearized gravity on a flat slice for the counter-current and induction estimates, at compactness 0.33–0.67 where it is only a scale (Findings 3–6, 9).
- Unit-lapse, flat-slice form for the ramp-stress estimate, though the shell has N ≈ 0.76 (Finding 6).
- The rebuilt toolkit shell (`warp_shell.py`, default smoothing span is the toolkit's choice) represents the published one [D-08].
- An ideal photon or GW exhaust, fully collimated (Findings 7, 10).
- The ADM momentum of an isolated asymptotically flat spacetime changes only by radiated flux (standard; not quoted from a primary source this run, as with the positive-mass theorem [D-62]).
- The κ = 4GM/(c²R) coefficient is my derivation; the pushing agent's stresses are ignored.
