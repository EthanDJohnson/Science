# Analysis: idealizer (Plato)
status: final

## Method applied
Simplest model that keeps the question: a static spherical matter shell (mass M, cavity radius R1, outer radius R2, Schwarzschild exterior) carrying a shift that is uniform in the cavity and zero outside. Solved (i) as an Israel thin shell, (ii) in linearized GR with a finite wall, then idealizations relaxed one at a time.

## Findings
1. **Thin shell (Israel): a uniform interior shift is gauge at O(β) and a shape change at O(β²).** Flat cavity with lapse N and uniform shift β (g_0i = +β_i), glued at r = R to a static Schwarzschild exterior, shell at rest in those coordinates (the 2024 shell's frame, [D-08]). The induced tube metric from inside has a cross term h_tθ = −βR sin θ, which is the exact form d(βR cos θ) dt. The relabelling t = τ + βR cos θ/(N² − β²) removes it. What is left is a static 2-metric R²[(N² − β²cos²θ)/(N² − β²) dθ² + sin²θ dφ²], with Gaussian curvature N²/(R²(N² − β²)) at the poles and (N² − β²)/(N²R²) at the equator. That is a Lorentz-elongated (prolate) cavity, axis ratio γ = N/√(N² − β²): 1.0002 at β = 0.02, N = 1, and 1.0008 at β = 0.04. So Israel's first junction condition against a round exterior fails only at O(β²), and it is cured by building the cavity prolate. No surface momentum S_tA is required at O(β). [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-idealizer_thinshell.py]
2. **Thin-shell Sagnac delay and Killing twist vanish.** The interior chord contributes 2Rβ/(N² − β²) to ∮ g_0i/(−g_00) dx^i. The Israel matching requires a time relabelling between the two shell crossings that is exactly 2Rβ/(N² − β²). So the loop integral, which is the Sagnac or gravitomagnetic flux, is zero. A thin shell can carry no physical "warp": the interior shift is a coordinate artefact. [calc: same file]
3. **Plain static thin shell energy conditions.** σ = (1 − √(1 − 2M/R))/(4πR) and p = [(1 − M/R)/√(1 − 2M/R) − 1]/(8πR), in geometric units. p/σ = 0.056 at 2M/R = 0.333 and 0.183 at 2M/R = 0.667, and the DEC (p ≤ σ) holds up to 2M/R = 24/25 = 0.96. The NEC, WEC and SEC hold for all 2M/R < 1. So in the idealized model the positive-energy shell itself is never the problem, and the shift is what has to be paid for. [calc: same file]
4. **Linearized momentum constraint, checked symbolically.** For unit lapse, flat slices and a small covariant shift w = g_0i, G_0i = ½[∇×∇×w]_i exactly at linear order, so T_0i = (1/16π)∇×∇×w. The Eulerian density enters only at O(w²); its sign there is negative (−2.4e-3 ε² at a test point). Any gradient (gauge) part of w drops out of T_0i, so the momentum density is gauge-invariant at this order. [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-idealizer_jcheck.py] (uses gr_tensors.py)
5. **A physical shift is a gravitomagnetic "solenoid" in the wall.** With w = β S(r) ẑ (S = 1 in the cavity, 0 outside), B_g = ∇×w = β S′ r̂×ẑ is azimuthal about the drive axis and confined to the wall, like the field of a toroidal winding. The cavity has B_g = 0: no gyroscope precession and no tidal change. The wall must carry poloidal momentum currents T_0i = (1/16π)∇×∇×w, with zero net momentum because ∫∇×∇×w dV is a surface term that vanishes when w has compact support. What remains in the cavity is the gravitational analogue of an Aharonov–Bohm potential. [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-idealizer_thickwall.py]
6. **NEC cap on the shift (linear theory) at the 2024 parameters** (R1 = 10 m, R2 = 20 m, M = 4.49e27 kg = 3.334 m geometric [D-21]). The NEC for a type-I block requires |T_0i| ≤ (ρ + p)/2.
   - Uniform-density wall, p = 0: β_max = 0.0272 with Fuchs's eq. (28) sigmoid, 0.0476 with a cubic smoothstep and 0.0439 with a quintic. These are converged to 5 digits on grid doubling.
   - Pressure p = 0.1ρ raises the cap by 10%.
   - Placing density where the currents are, so that the NEC is saturated pointwise as a mass budget, gives 0.084 (sigmoid) to 0.107 (cubic).
   - Cross-check: Fuchs et al. report that the shift "is possible for βwarp = 0.02 without any energy condition violation", with a footnote saying "This is likely not an upper limit as optimizations could be considered" [new: Fuchs et al. 2024, arXiv:2405.02709 p. 17, full-text]. The model's sigmoid cap of 0.027 sits just above their checked 0.02, and their Table 1 value v_warp = 0.04 [D-25] sits above that cap. The model therefore predicts that 0.04 with a uniform wall would violate the NEC in linear theory. This is a prediction of the model, not a computed check of their metric. They also anticipate the density-shaping gain: "strategically place energy density where the momentum flux is highest" [new: same, p. 27, full-text].
   [calc: lens-idealizer_thickwall.py]
7. **Scaling law.** β_max ≈ k · (2GM/(c²R2)) · (Δ/R2), with Δ = R2 − R1.
   - Cubic profile: k ≈ 0.18–0.37 for a uniform wall and 0.46–0.83 for a shaped wall, as Δ/R2 runs from 0.09 to 0.9.
   - The law is exactly scale-free: the (10 m, 20 m) and (100 m, 200 m) shells give the same β_max = 0.0476 at 2M/R2 = 0.333.
   - It tends to 0 as Δ → 0, consistent with finding 2: a thin shell holds no flux.
   - At compactness 2M/R2 = 0.05 the cap is 7e-3 (uniform, R2 = 2R1).
   - A 100 m payload at the 2024 proportions needs M = 4.48e28 kg = 23.6 M_J (ours) for the same β_max.
   [calc: lens-idealizer_thickwall.py]
8. **The gauge-invariant observable is the gravitomagnetic flux, and it reproduces Fuchs's 7.6 ns.** The Sagnac round-trip difference along the axis is Δt = 2β∫S(|z|)dz/c, with ∫S dz = 30.0 m for all three profiles. At β = 0.04 that gives 8.0 ns in linear theory with N = 1, against the 7.6 ns of their Table 1 [D-25]. The difference from a plain boosted shell is this flux and nothing else in the cavity. [calc: lens-idealizer_thickwall.py]
9. **The advance from the shift never beats the shell's own Shapiro delay.** The comparison is along the axis, with endpoints at rest at ±L.
   - Shapiro delay = 16.5 m (54.9 ns) at L = 20 m, 37.9 m at L = 100 m and 99.3 m at L = 10 km.
   - Advance = 30.0 m × β.
   - A net advance needs β ≥ 0.55 even at the shortest baseline, 5–20× above the NEC caps. At the cap, advance/delay = 0.05–0.20 (L = 20 m) and falls with L.
   - Structural reason: in linear harmonic gauge the delay density ½h_kk = 2∫T_kk/|x − x′| d³x′ is pointwise ≥ 0 under the NEC. That is the Visser–Bassett–Liberati result [D-61]: the matter currents that make the shift also make a larger delay.
   - Fuchs et al. say the same of their own shell: the Shapiro time delay "from B to A is still a delay compared to the propagation time in" flat space [new: arXiv:2405.02709 p. 27, full-text].
   [calc: lens-idealizer_thickwall.py]
10. **The payload rides with the shell, not with the shift.** In the paper's comoving frame the exterior is static Schwarzschild, so ∂_t is the asymptotic rest frame. A payload at rest relative to the cavity walls follows this Killing flow, which makes it geodesic, because the cavity is flat with constant metric. Its clock rate is √(−g_00) = 0.7611 with or without the shift, since the construction leaves g_00 unchanged. That is no proper-time gain [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-idealizer_payload.py].
    - The observers that "move" are the cavity's Eulerian observers. At β_warp = 0.02 they move at 0.026 c relative to the walls, and at 0.04 at 0.053 c. They reach the wall within about 2.5 µs and 1.3 µs respectively, so they are not a payload.
    - A stationary isolated solution therefore coasts only as a whole, and "the 2024 shell coasting at v" is the same matter shell with payload boosted to v.
    - By the paper's own definition this is the trivial case: "For a non-trivial solution, the original trajectory Cbackground should not be a geodesic, i.e. the passengers should not 'already be going' from point A to point B" [new: Fuchs et al. 2024, arXiv:2405.02709 p. 2, full-text].
11. **The shift carries no momentum, so start and stop costs the whole mass.** ∫T_0z dV/β = 9.4e-7 m against ∫|T_0z| dV/β = 13.0 m in geometric units, a ratio of 7e-8, which is zero to grid accuracy. That holds because ∫∇×∇×w dV is a surface term.
    - Reaching 0.04 c and stopping takes a photon-rocket mass ratio of 1.0833. That is 3.74e26 kg of propellant (0.197 M_J) for the 4.49e27 kg shell, against 8.3e3 kg for the 1e5 kg payload alone, a ratio of 4.5e22 (cf. [D-23]).
    - Momentum conservation of the isolated system means no self-propulsion [D-07], [D-69].
    [calc: lens-idealizer_payload.py]
12. **One real perk of a heavy shell under acceleration is not a warp effect.** If the shell is pushed, interior inertial frames are partly dragged along.
    - Pfister et al. 2005 build this "linear dragging" model and find the interior of the accelerated shell "stays flat" [new: Pfister et al. 2005, CQG 22 4743, doi:10.1088/0264-9381/22/22/007, abstract, "It is shown that the interior of this (Reissner–Nordström-like) shell stays flat. The dragging of neutral test particles inside the shell, defined by their acceleration, scaled by the overall acceleration of the (rigid) shell, is calculated for the weak field case for a highly massive but weakly charged shell and for the general strong field case."].
    - Our naive weak-field coefficient, in harmonic gauge and ignoring the pusher's stresses, is 4GM/(c²R). That is 0.67 at R = 20 m and 1.33 at R = 10 m for the 2024 mass. Linear theory fails there, so the expectation is strong dragging.
    - This could reduce the acceleration the crew feels during start and stop. It needs no shift, and it does nothing to the momentum bill. [calc: lens-idealizer_payload.py]
13. **Sagnac comparison corrected for the interior lapse.** The cavity's −g_00 = 0.579 raises the cavity part of ∮g_0i/(−g_00)dx^i by 1.73. The straight-through axis estimate therefore lies between 8.0 ns (N = 1) and 13.8 ns (whole path at the cavity lapse). Fuchs's two-arm light path was not modelled, so "consistent within a factor 2" is the honest statement. [calc: lens-idealizer_payload.py, lens-idealizer_thickwall.py]

## Lens-specific outputs

### The idealized model
- **Geometry.** Static spherical shell, R1 < r < R2, mass M, Schwarzschild exterior. The shell is at rest in the exterior's asymptotic frame, which is the 2024 paper's comoving frame [D-08].
- **Shift.** Covariant shift g_0z = w = β S(r), with S = 1 in the cavity and S = 0 outside R2. Sign convention: g_0i = +β_i, from_adm form ds² = −N²dt² + h_ij(dx^i + b^i dt)(dx^j + b^j dt). Fuchs's g_0x = −Sβ_warp is the same with β → −β.
- **Idealizations.**
  - (I1) Spherical symmetry of the matter.
  - (I2) Stationarity.
  - (I3) Weak field, linear in M and β, with M·β cross terms dropped. This applies to the thick wall only; the thin shell is exact.
  - (I4) Uniform wall density.
  - (I5) Stresses p ≪ ρ (p = 0 in the cap).
  - (I6) A one-parameter family of smooth radial profiles S(r).
  - (I7) The NEC tested as |T_0i| ≤ (ρ + p)/2, which is the exact type-I-block condition when the stresses are isotropic and small.
  - (I8) A thin wall as an Israel surface layer.

### Model results (scaling laws)
| Quantity | Result | Basis |
|---|---|---|
| Thin-shell interior shift | Gauge at O(β); prolate cavity, axis ratio N/√(N² − β²), at O(β²); surface momentum 0; Sagnac flux 0 | F1, F2 |
| Thin static shell energy conditions | NEC, WEC, SEC for all 2M/R < 1; DEC for 2M/R ≤ 24/25 | F3 |
| Physical shift needs | Poloidal wall currents T_0i = (1/16π)∇×∇×w with zero net momentum; B_g toroidal, confined to the wall | F4, F5, F11 |
| NEC cap on the shift | β_max ≈ k(2GM/c²R2)(Δ/R2): k = 0.18–0.37 for a uniform wall and 0.46–0.83 for a shaped wall (cubic); 0.027 / 0.084 for the 2024 sigmoid at 2024 parameters | F6, F7 |
| Thin limit | β_max ∝ Δ → 0 | F2, F7 |
| Invariant difference from a boosted plain shell | Gravitomagnetic flux ∮w·dl, i.e. a Sagnac Δt = 2β∫S dz/c = 8.0 ns at β = 0.04 (N = 1) against 7.6 ns published | F8, F13 |
| Time advance | advance/delay ≤ 0.20 at the NEC cap (shortest baseline); a net advance needs β ≥ 0.55 | F9 |
| Payload speed relative to infinity | Equal to the shell's: v_payload = v_shell; no proper-time gain (g_00 unchanged) | F10 |
| Start/stop | Momentum γMv from outside; propellant 4.5e22× the bare payload's | F11 |

### Relaxing the idealizations one at a time
| Idealization relaxed | Direction of change | Rough size | Changes the verdict? |
|---|---|---|---|
| I3 weak field → strong field (2M/R2 = 0.33, 2M/R1 ≈ 0.67) | The cap shifts by O(1) factors; Shapiro delay grows faster than linear; the redshift raises the flux by up to 1.73× | factor ≲ 2 either way on β_max; the delay margin (≥ 5×) survives | No. The Gao–Wald theorem [D-60] covers the nonlinear NEC case if the null generic condition and completeness hold. |
| I4 uniform → shaped density | Cap rises | ×2.3 (cubic) to ×3.1 (sigmoid) | No. Advance/delay is still ≤ 0.2. |
| I5 adding stresses p | Cap rises by (1 + p/ρ) | +10% at p = 0.1ρ; ≤ +18% at the thin-shell p/σ for 2M/R = 0.67 | No |
| I6 better shift profiles | Cap rises. The sigmoid is the worst tested (high S″ near the edges) | a factor ~2 between profiles; the scaling with (2M/R)(Δ/R) is fixed by dimensions | No. VBL linear positivity is profile-independent. |
| I1 non-spherical walls (prolate, toroidal) | Flux can be concentrated, so β per unit mass may rise | unknown, O(1) expected | No for FTL. Linear VBL holds for any NEC source. |
| I2 stationary → accelerating | Needs momentum γMv from outside; heavy shells drag interior frames (F12) | dragging coefficient ~4GM/(c²R) ~ O(1) | It turns "coast" into "start and stop by external push", not self-propelled. The mechanist lens owns this. |
| I8 thin → thick wall | Thin walls give β_max → 0; physical flux needs Δ ~ R | — | It shows any "warp" needs a fat, very heavy wall. |
| Matter model | Not supplied by the model. Poloidal mass currents at speeds up to ~(ρ + p)/(2ρ)·c relative to the wall need an anisotropic, stressed medium; Le's elastic shells [D-74] are the nearest candidate | — | Leaves "in principle" open on the source side, and the physical-source requirement unmet (premise 6) |

### Where reality departs most
1. **The 2024 shell is strong-field, not weak-field.** At 2M/R1 ≈ 0.67 the linear model is good only to a factor of about 2. That departure hurts a precise cap, because the model's 0.027 against the paper's 0.02 and 0.04 is suggestive, not decisive. It does not hurt the qualitative results (F1, F2, F10, F11), which rest on exact Killing-vector, junction and momentum arguments.
2. **Whether the published shell solves Einstein's equations with a consistent source at all** [D-31]. The model presumes a consistent source exists. If Barzegar et al.'s Error 18 stands, reality is worse than the model, which hurts the shell's case.

## Calculations
- `calc/lens-idealizer_thinshell.py`: Israel thin shell with uniform interior shift. Induced metric; the time relabelling λ = β/(N² − β²); prolate residual 2-metric and Gaussian curvature; static shell σ, p (geometric) and DEC limit 2M/R = 0.960; Sagnac loop cancels exactly (2Rβ/(N² − β²) both ways).
- `calc/lens-idealizer_jcheck.py`: verifies with gr_tensors that G_0i = ½∇×∇×w at linear order (agreement to 7 digits at 9 component-points), and that the Eulerian ρ is O(w²) and negative there (−2.4e-3 ε² at a test point).
- `calc/lens-idealizer_thickwall.py`: linear thick wall.
  - NEC caps β_max at the 2024 parameters: 0.0272 sigmoid, 0.0476 cubic, 0.0439 quintic (uniform wall, p = 0); 0.084–0.107 for a shaped wall. Grid-converged to 5 digits.
  - Scaling table in 2M/R2 and Δ/R2.
  - Sagnac 8.01 ns at β = 0.04 (∫S dz = 30.0 m).
  - Axis light-time: Shapiro delay 16.46 m (54.9 ns) at ±20 m, 37.9 m at ±100 m, 99.3 m at ±10 km; β for net advance 0.55–3.3; advance/delay at the cap 0.008–0.20.
- `calc/lens-idealizer_payload.py`, using the run tool `tools/warp_shell.py`:
  - interior −g_00 = 0.5793 (clock rate 0.7611) with or without the shift; N = 0.7614 at β = 0.02;
  - Eulerian drift 0.026 c (β = 0.02) and 0.053 c (β = 0.04) relative to the cavity, with wall-crossing in 2.5 µs and 1.3 µs;
  - net momentum of the shift currents zero (ratio 7e-8);
  - start/stop at 0.04 c: photon-rocket mass ratio 1.0833, propellant 3.74e26 kg for the shell against 8.3e3 kg for the payload;
  - dragging coefficient 4GM/(c²R) = 0.67 (R = 20 m) and 1.33 (R = 10 m).

## Candidate answers (at least 3; the null and a reframe count)
- [IDEALIZER-A] **Null on (A).** No positive-energy (NEC-satisfying) warp spacetime gives a genuine time advance. In the simplest shell model the shift's one-way "advance" is at most 0.2 of the Shapiro delay of the matter whose currents create it, and the linear delay density is pointwise non-negative under the NEC. | status: surviving | Model result: F9 (advance/delay ≤ 0.20 at the NEC cap; net advance needs β ≥ 0.55, 5–20× the cap), matching VBL [D-61] and Gao–Wald [D-60] | Test: any stationary NEC solution with a measured light-time advance between exterior rest points would refute it; the decisive calculation is a nonlinear light-time integral through a fully solved shell | confidence: high
- [IDEALIZER-B] **Null on (B).** The 2024 "warp shell" is a static massive shell plus a wall-confined gravitomagnetic flux, the gravitational Aharonov–Bohm analogue. The payload moves exactly as the shell does: coasting is the boosted shell, and start and stop needs γMv of external momentum. It gives nothing a massive vehicle cannot, beyond a Sagnac offset of about 8 ns. | status: surviving | Model result: F1, F2 (the thin-shell shift is gauge), F5, F8 (only invariant: flux, 8.0 ns vs 7.6 ns published), F10 (same clock rate, the payload follows the Killing flow), F11 (zero momentum in the shift) | Test: a gauge-invariant observable inside the cavity that differs from the plain shell. The model predicts none, since B_g = 0 and g_00 is unchanged | confidence: high (qualitative), medium (numbers, linear theory)
- [IDEALIZER-C] **Reframe.** "Positive-energy warp" is linear frame dragging by mass currents. Its honest figure of merit is the flux cap β_max ≈ k(2GM/c²R)(Δ/R), with k ≈ 0.2–0.8, which vanishes for thin walls and stays ≲ 0.1 at the 2024 compactness. At fixed mass, the only useful property, partial cancellation of felt acceleration during an external push, comes from the shell's mass, not its shift. | status: surviving (as reframe) | Model result: F6, F7, F12 | Test: the scaling law can be checked against a nonlinear solve (Warp Factory or numeric_stress_energy) of shifted shells at several Δ/R and M/R | confidence: medium
- [IDEALIZER-D] **The 2024 shell at its Table 1 speed (v_warp = 0.04) satisfies the energy conditions.** | status: strained | Model result: F6. In linear theory with a uniform wall and Fuchs's sigmoid, the NEC cap is 0.027: above their checked 0.02 [new: arXiv:2405.02709 p. 17] but below 0.04. Shaped density would allow 0.084, but the published shell has constant density | Test: an exact type-I test of the published metric at β = 0.04 (constraints lens; tools/numeric_stress_energy.py) | confidence: medium
- [IDEALIZER-E] **A thin positive-energy shell can carry a warp shift.** | status: eliminated | Model result: F1, F2, F7. Israel matching makes a uniform interior shift pure gauge, with zero flux, and a physical flux in a wall of thickness Δ has β_max ∝ Δ → 0 | confidence: high
- [IDEALIZER-F] **A positive-energy shell gives the payload a proper-time advantage over a rocket.** | status: eliminated for the 2024 construction | Model result: F10 (g_00, and so the payload clock rate 0.761, is unchanged by the shift). Positive-mass shells slow interior clocks [D-07], [D-37], which is the wrong direction for the crew | confidence: high

## What would change my mind
- A fully nonlinear solution in which the shift contributes a cavity observable that is invariant and local: B_g ≠ 0, or a change in g_00 relative to the plain shell attributable to the shift at fixed matter. That would break F10's "nothing for the payload".
- A stationary, NEC-satisfying solution where the advance exceeds the Shapiro delay on some exterior-to-exterior path. That would contradict F9, and it would need a failure of the null generic condition or completeness in Gao–Wald [D-60].
- An exact energy-condition test of the published shell at β = 0.04 that passes. That would mean strong-field effects raise the cap above the linear 0.027 and would weaken IDEALIZER-D, not B.
- An isolated solution that changes its ADM momentum with no emission. That would contradict F11 and momentum conservation.

## Assumptions I relied on
- Linearized GR for the thick-wall numbers (I3). The 2024 compactness lies outside its accuracy, and the numbers are good to a factor of about 2.
- The run tool `tools/warp_shell.py` reproduces the published construction (g_00 kept, only g_0x modified, comoving frame equal to the asymptotic rest frame). The qualitative result F10 depends on g_00 being unchanged, which the tool's docstring says matches the paper and the Warp Factory code.
- The NEC for a type-I block with small isotropic stresses, |T_0i| ≤ (ρ + p)/2. Larger anisotropic stresses along the current would loosen this by O(1).
- That a consistent matter source exists for the currents. It is not shown, and it is contested for the published shell [D-31].
- Sagnac comparison: a straight axis path, not Fuchs's two-arm geometry.
