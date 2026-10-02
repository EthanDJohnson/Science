# Analysis: decomposer (Descartes: methodical doubt and decomposition)
status: final
## Method applied
Rewrote the question as a tree of sub-questions that end at a theorem, a calculation or a measurement; built an assumption ledger (measured / derived / assumed / unknown) over the question and the dossier; checked each no-go theorem's hypotheses against each metric (the brief assigns this lens the theorem-applicability ledger, premise 3); named the load-bearing assumption and sorted the sub-questions into settled and open. Literature searches filled two of the dossier's gaps: the positive-mass theorem in its E ≥ |P| form, and the evolution of the centre of mass. Three scripts test the theorems on the rebuilt 2024 shell: a travel-time integral, an all-observer energy-condition scan, and thresholds in shift and mass.
## Findings
F1. **WEC implies NEC, so the brief's own standard for "without negative energy" (WEC for all observers) puts every candidate under the NEC-based theorems.** Olum 1998 needs the WEC, and in its proof only R_ab K^a K^b ≥ 0 on null K, which is the NEC [D-59; research RT-03 quotes the Raychaudhuri step]. Gao–Wald needs the NEC plus the null generic condition plus null geodesic completeness [D-60]. So, for headline (A), the energy-condition question reduces to: does the candidate violate the generic condition, completeness, or asymptotic flatness? It does not turn on the energy condition.

F2. **The spacetime positive-mass theorem gives a causal ADM 4-momentum, which is stronger than "M ≥ 0".** [new: Eichmair, Huang, Lee & Schoen 2016, J. Eur. Math. Soc. 18, 83 (doi:10.4171/jems/584), abstract via lit_search, "This theorem asserts that for any asymptotically flat initial data set that satisfies the dominant energy condition, the inequality E ≥ | P | holds, where (E, P) is the ADM energy-momentum vector."] Rigidity: [new: Huang & Lee 2020, Commun. Math. Phys. 376, 2379 (doi:10.1007/s00220-019-03619-w), abstract via lit_search, "if an asymptotically flat initial data set satisfies the dominant energy condition and has $E=|P|$, then $E=|P|=0$"]. Consequences, our reading:
  - (a) An isolated, asymptotically flat, DEC-satisfying warp configuration (shell plus payload) has a future-causal total 4-momentum. Its centre of mass therefore moves at |P|c/E ≤ c, with equality only for flat data. A "coasting" positive-energy vehicle that moves as one unit faster than light would need a spacelike ADM 4-momentum. That is excluded.
  - (b) Zero ADM energy (Alcubierre, Natário zero-expansion [D-03]) plus the DEC forces E = |P| = 0, hence the data must be flat. This is a peer-reviewed, general version of the Barzegar Thm IV.19 statement (preprint) [D-62]. It answers half of D-32: zero ADM mass does force a DEC violation, though not necessarily a WEC or NEC violation. The Barzegar "no direct relation to the WEC" remark is compatible with this.
  - (c) The theorem needs the DEC, not just the WEC. A WEC-satisfying but DEC-violating source ("unphysical source", in the brief's terms) escapes F2 but not F1.

F3. **Self-propulsion is closed by momentum bookkeeping at infinity, not by energy conditions.** The ADM centre of mass of an isolated system translates at P/m under the Einstein equations. [new: Nerz, "Time evolution of ADM and CMC center of mass in general relativity", arXiv:1312.6274, full-text via fetch_text, "we prove that, asymptotically, their time evolution is a translation induced by the quotient of their linear mo- mentum P and mass m, as to be expected from the corresponding Newtonian setting"]. The same source notes that this needs decay strong enough for P to be defined. With ADM (E, P) conserved for an isolated system, a configuration with no emission keeps its centre-of-mass velocity. "Self-propelled" (brief level 3) is then possible only by emitting momentum to null infinity: gravitational waves (a GW rocket) or radiation, which the brief counts as external propulsion. This agrees with Bobrick–Martire's "any warp drive requires propulsion" [D-07] and Le's Bondi balance [D-69]. It holds whatever the sign of the energy density, so negative energy would not rescue self-propulsion either. Only the payload's motion *relative to its own shell* could be rearranged internally, and that does not move the centre of mass.

F4. **Travel-time test on the rebuilt 2024 shell: no advance at the published mass.** We integrated a null ray along the shift axis through the centre of the `warp_shell.py` rebuild (shell frame = exterior rest frame, Schwarzschild exterior). The one-way excess time over flat-space light, for the +x ray (along the shift), at D = 1e3 m: 240.0 ns (β_warp = 0), 236.6 ns (0.02), 233.3 ns (0.04), 187.2 ns (0.40). It stays positive (150.8 ns) even at β_warp = 0.95 [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-decomposer_transit_time.py].
  - Why: the cavity lapse² is 0.579. In the cavity alone, a local advance needs β_warp > (1 − e2a)/2 = 0.21, and the exterior Shapiro delay (≈ 100–450 ns for D = 1e2–1e5 m) swamps any gain. The weak-field estimate gives 231 ns at D = 1e3 m (R = 15 m), which agrees with the strong-field number to within 4%.
  - The shift's effect is a co- versus counter-propagating difference: 6.86 ns at β_warp = 0.02 and 13.72 ns at 0.04, independent of D. That is the size of Fuchs et al.'s 7.6 ns [D-25]. Matching 7.6 ns needs β_warp ≈ 0.022 in this rebuild, consistent with the tool's note that the paper's metric parameter is 0.02 while "0.04c" labels the table. Our reading: Fuchs's δt is a Sagnac-type asymmetry. It is **not** a time advance over exterior light, which bears on D-33.
  - The 2024 shell therefore meets neither sense of "superluminal". At v_warp = 0.04 c it does not even claim to.

F5. **Cutting the mass while keeping the shift does produce an advance.** At M = 0.01 × 2.365 M_J with β_warp = 0.04, the +x excess is −1.87 ns, a genuine advance over flat-space light between exterior rest points at ±1 km. At 0.1 × M it is +16.9 ns. Olum and Gao–Wald [D-59, D-60] predict that this light, shifted configuration must violate the NEC. That is checked in F6. It is the concrete form of premise 7: the mass is what pays for the shift, through the energy conditions.

F6. **Olum's theorem holds on the worked example, and the Eulerian blind spot shows.** We scanned all observers with `numeric_stress_energy.py` on 285 points in the x–z plane: r = 8–22 m, polar angles 0°, 45°, 90°, 135° and 180° from the shift axis, h = 0.05 m [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-decomposer_advance_vs_nec.py].
  - Published mass, β_warp = 0 and β_warp = 0.02: zero NEC/WEC/SEC/DEC violations, all Hawking–Ellis type I.
  - Published mass, β_warp = 0.04: 22 of 285 points violate the NEC (type IV, sampled). The worst NEC value is −7.9e-5 m⁻² (geometric) at r = 12.25 m, perpendicular to the shift. This configuration has no time advance (F4), which is consistent: the NEC failure is necessary for an advance, not sufficient.
  - Light shell (0.01 × M, β_warp = 0.04), the one that shows the advance: 167 of 285 points violate the NEC, worst −1.7e-4 m⁻². The result is unchanged at h = 0.025 m (6 points unconverged).
  - In every case the minimum **Eulerian** density stays positive (2.4e-6 and 2.4e-8 m⁻²). So an Eulerian-only check would have passed configurations that violate the NEC. That is brief premise 1 in action.
  - Caveats: this uses the run's rebuild with its own smoothing span, not the authors' grid. The points are a sample, not a proof. The constraints lens owns the reference table.

F7. **Shift cap and the ordering the theorems predict, across five masses** (R₁ = 10 m, R₂ = 20 m; the shift profile of the paper's eqs. 26–28 as rebuilt; bisection resolution ≈ 6e-5) [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-decomposer_thresholds.py]:

| M / (2.365 M_J) | 2GM/(c²R₂) | β_warp at first NEC failure | β_warp at first advance (D = 1e3 m) |
|---|---|---|---|
| 0.001 | 3.3e-4 | 1e-4 | 2.1e-3 |
| 0.01 | 3.3e-3 | 3e-4 | 0.021 |
| 0.1 | 0.033 | 2.8e-3 | 0.225 |
| 0.5 | 0.167 | 0.0132 | none up to 0.95 |
| 1.0 | 0.333 | 0.0246 | none up to 0.95 |

  - The advance threshold always lies above the NEC threshold, by a factor of 8 to 80. This is what Olum and Gao–Wald require, now shown on a worked family.
  - Above the lowest-mass row, the NEC cap scales roughly as β_NEC ≈ 0.074–0.084 × (2GM/c²R₂). This is our profile-specific fit, not a theorem. Extrapolated to the Buchdahl compactness 8/9, it gives β_NEC ≲ 0.07.
  - The paper's energy-condition-checked β_warp = 0.02 sits about 20% below the cap at its compactness. The "0.04 c" label lies above it in this rebuild.
  - At compactness ≥ 0.17, no shift below 0.95 gives an advance, because redshift and Shapiro delay dominate.
  - Our reading: positive mass both allows the shift (via the NEC) and delays light (via redshift). In this family, the second wins wherever the first is satisfied.

F8. **Which theorem decides which headline.**
  - (A): Olum and Gao–Wald, with the VBL linearized version as the weak-field check, decide it. They need only the NEC, the generic condition and completeness, never unit lapse or flat slices. They therefore cover the 2024-type shells that the Santiago–Schuster–Visser theorem does not [D-41].
  - The coasting form of (A): if a whole isolated configuration is to move faster than light, the DEC positive-mass theorem (E ≥ |P|) closes it independently (F2).
  - Self-propulsion in (B): ADM momentum conservation and the centre-of-mass theorem close it (F3), independently of any energy condition.
  - Santiago–Schuster–Visser, Natário Thm 1.7 and Schuster–Santiago–Visser 2023 decide only the unit-lapse, flat-slice class. Their failure to reach N ≠ 1 shells is not a loophole for (A), because Olum and Gao–Wald reach those shells anyway.
## Lens-specific outputs

### 1. Sub-question tree
Q: Can any warp spacetime move a payload faster than light, or at all, without negative energy? What would building it take, and what is the nearest test?
- **Q1. What does each metric's stress-energy do, for all observers?**
  - Q1a. Which metrics are in the unit-lapse, flat-slice (Natário) class? Settled by inspecting their definitions. Alcubierre, Natário, Lentz, Fell–Heisenberg and Rodal are in it. The 2024 shell, the Bobrick–Martire shells and Le's shells are not [D-01, D-06, D-05, D-08, D-11, D-41].
  - Q1b. Does every metric in the class violate the NEC? Yes, by Santiago–Schuster–Visser (SSV), for localized fields [D-41]. Natário Thm 1.7 [D-58] gives WEC-or-SEC.
  - Q1c. Does the 2024 shell meet the NEC, WEC, SEC and DEC for all observers? Partly. The published sampled-observer claim is in [D-08]. Our rebuild is clean at β_warp = 0.02 and fails at 0.04 (F6, F7). It is contested as a solution at all [D-31] (Barzegar Error 18). The regularized-shell preprint is internally inconsistent [D-84]. *Open*: needs a full source-consistent solution.
  - Q1d. Is there a matter model that obeys its own equations of motion? Lentz: not exhibited [D-06]. 2024 shell: TOV not solved per Barzegar [D-31]. Elastic shells can bear DEC-obeying static loads in weak gravity [D-74]. *Open* for the shifted, strong-field case.
- **Q2. Is each "superluminal" claim a travel-time advance?**
  - Q2a. Fell–Heisenberg: shift exceeds lapse, not an advance [D-05]. Lentz: horizons form [D-06]. The 2024 shell: no claim, and no advance in our test (F4).
  - Q2b. Can any NEC-satisfying asymptotically flat spacetime give an advance? No, under Olum (generic condition, no singularities) [D-59], Gao–Wald (completeness; for points far enough out) [D-60] and VBL (weak field) [D-61]. Worked example: F5–F7.
- **Q3. Can a positive-energy configuration start, stop, or self-propel?**
  - Q3a. Is centre-of-mass motion fixed for an isolated system? It is P/E, with P conserved (F3).
  - Q3b. Does acceleration with energy conditions intact exist? Only externally powered: Le's radiative steering, photon-rocket cost [D-38, D-72]. Fuchs et al. say naive acceleration needs negative energy [D-08]. The mechanist lens owns the numbers.
  - Q3c. Self-propelled? Only by emitting momentum to infinity (gravitational or electromagnetic radiation), which is a rocket by another name (F3).
- **Q4. Does positive matter cap the warp effect?**
  - Q4a. Compactness: < 8/9 for a static sphere [D-27, D-63], and R > 2GM/c² for the shell [D-64].
  - Q4b. Shift at given compactness: β_warp,NEC ≈ 0.08 × compactness in our rebuilt family (F7). This is profile-specific. The idealizer lens owns the analytic version.
- **Q5. Does the warp shell beat a rocket at anything?**
  - Passengers feel no acceleration while coasting, but neither do a coasting rocket's.
  - Interior clocks are slowed, not sped up [D-07, D-37]; the cavity lapse² is 0.579 here (F4).
  - Mass cost: the shell is 4.5e22 × the payload [D-23, D-39].
  - The only distinguishing observable is a Sagnac-type time asymmetry of about 7–14 ns (F4, D-25).
- **Q6. Build and test.** The engineer lens owns this. The nearest premise-testing experiment is frame dragging (LARES 2 at about 0.2%, contested [D-42c]). The decisive calculation is a source-consistent, all-observer solution of a shifted shell, then of an accelerating one.

### 2. Assumption ledger
| # | Premise | Class | Basis / what would test it |
|---|---|---|---|
| P1 | Classical GR holds at the shell's scale (curvature radii of metres) | assumed (well-tested in weak field) | GP-B, LARES [D-18, D-42]. The strong-field regime at compactness 0.33 is untested in the lab |
| P2 | "Without negative energy" = pointwise WEC for all observers (hence NEC) | assumed (brief's definition) | Definitional. Averaged or semiclassical readings change the scope (D-75 escapes only in the averaged sense) |
| P3 | "Superluminal" = travel-time advance between exterior rest points | assumed (brief's definition) | Definitional. A shift > lapse or a coordinate speed > c is not enough [D-05] |
| P4 | Exterior is asymptotically flat | assumed for all named metrics. Garattini–Zatrimaylov use de Sitter [D-75] | Needed by the PMT and Gao–Wald's setting. Cosmological backgrounds are a separate question |
| P5 | Generic condition holds on the candidate fastest path | derived: holds wherever there is matter or transverse tide on the path [D-59] | Violated only by special paths in exactly vacuum, tide-free regions; such a path gains no advance |
| P6 | No singularities / null geodesic completeness | assumed. Distributional sheets (Lentz C⁰, thin shells) strain it [D-30] | Israel junction conditions: a sheet has its own surface NEC, so a kink cannot hide a violation |
| P7 | Eulerian density ≥ 0 ⇒ "positive energy" | **false as a WEC test** | F6: positive Eulerian density at NEC-violating points; [D-04, D-05] |
| P8 | The 2024 shell solves Einstein's equations with a consistent source | unknown / contested | Barzegar Error 18 [D-31]; test: a full TOV-plus-shift solution with a matter EOS |
| P9 | Sampled observers establish "for all observers" | derived (numerical), unknown in completeness | Exact type-I tests where type I. Le's interval certificates [D-73]. Our 285-point sample (F6) |
| P10 | Rebuilt shell ≈ published shell | assumed | `warp_shell.py` smoothing span is ours [tools.md]; agrees on M, R₁, R₂, β |
| P11 | ADM (E, P) is defined and conserved for the configuration | derived (asymptotic decay) | Nerz caveat: needs decay strong enough for P [F3] |
| P12 | DEC holds for the source | measured in our scan only for the rebuild at β ≤ 0.02 (F6) | Needed for E ≥ \|P\| (F2) |
| P13 | Positive mass caps the shift | derived for our family (F7). No general theorem found [D-64] | Idealizer's thin-shell junction calculation |
| P14 | Acceleration can be added without breaking the energy conditions | unknown. Fuchs et al.: naive version needs negative energy [D-08] | Mechanist calculation; Le's steering [D-72] |
| P15 | The payload's time and tides are acceptable | derived: cavity flat, clocks slowed [D-07, D-74]; cavity lapse² 0.58 (F4) | Tidal tensor in the cavity (≈ 0 if flat) |
| P16 | A frame-dragging shift does something for a payload a boosted shell doesn't | **doubtful** | F4: its only effect is a Sagnac-type asymmetry; no advance, no change in centre-of-mass motion (F3) |
| P17 | Semiclassical QFT is the only established source of NEC violation | assumed (admissible physics) | QI bounds make walls Planck-thin [D-29, D-67] |
| P18 | Energy budgets compare like with like across wall conventions | derived with stated conventions [D-28, D-34] | Convention labels in the dossier |

### 3. Theorem-applicability ledger (premise 3)
Key: **A** = hypotheses hold, so the theorem applies; **n/a** = a hypothesis fails; **?** = undetermined. The consequence for the metric follows the arrow.

| Theorem (hypotheses) | Alcubierre | Natário 0-exp. | Lentz | Fell–Heis. | B–M Class I shells | Fuchs 2024 shell | Rodal 2026 | Le steering (preprint) | Garattini–Zatrimaylov (dS) |
|---|---|---|---|---|---|---|---|---|---|
| SSV 2022 [D-41] (N = 1, h = δ, localized shift) | A → NEC fails | A → NEC fails | A (named) → NEC fails; C⁰ objection [D-30] | A (named) → NEC fails (conceded [D-05]) | n/a as stated (N ≠ 1). SSV say they fail "for slightly different reasons" [D-54] | **n/a** (N ≠ 1, curved h) | A → NEC fails (confirmed [D-11]) | n/a (not Natário class) | n/a (not AF; N = 1 status ?) |
| Natário Thm 1.7 [D-58] (N = 1, h = δ, non-flat) | A → WEC or SEC fails | A (Barzegar IV.32: WEC fails) | A | A | n/a | n/a | A | n/a | ? |
| SSV 2023 massive [D-57] (N = 1, h = δ, Schwarzschild base) | n/a (M = 0) | n/a (M = 0) | A if M ≠ 0 | A if M ≠ 0 | n/a | n/a (curved slices) | ? | n/a | n/a |
| Olum 1998 [D-59] (generic condition, no singularities; travel-time FTL) | A: the v > c bubble needs WEC failure, consistent | A | A: any advance needs WEC failure | A (not an advance anyway) | A → no advance (subluminal, as B–M state) | A → no advance unless the NEC fails. Verified on our family (F5–F7) | A | A → subluminal | Local theorem applies; "FTL" there is relative to cosmological flow, outside P3 |
| Gao–Wald 2000 [D-60] (NEC, null generic, null complete) | n/a (NEC fails) | n/a | n/a if the NEC fails | n/a | A → no far-field advance | A at β ≤ 0.02 (F6) → no advance (F4 consistent) | n/a | A (photon-rocket exterior) | n/a (NEC only averaged) |
| VBL 2000 [D-61] (linearized about Minkowski, NEC) | n/a (strong, NEC fails) | n/a | n/a | n/a | A (weak field) → delay | Weak-field estimate agrees with the strong-field result within 4% (F4) → delay | n/a | A | n/a |
| PMT, DEC → E ≥ \|P\| (EHLS 2016); rigidity (Huang–Lee) (F2) (AF, DEC) | E = 0 → DEC fails or flat [D-03] | E = 0 → DEC fails or flat | ADM E ? [D-03 allows E ≠ 0]; DEC fails at N_iN^i ≥ 1 [D-06] | ? | A → E > 0, causal P | A → E > 0 (M = 2.365 M_J), coasting v < c | ? (E₊ ≈ E₋ [D-36]) | Bondi version applies | n/a (not AF) |
| Bobrick–Martire class result [D-65] (spherical; perfect fluid for DEC) | — (not positive-energy) | — | — | — | A → Class I, subluminal | Spherical matter but axial shift: ? | — | — | — |
| Andréasson / Buchdahl [D-63] (static, spherical, ρ ≥ 0, p ≥ 0) | n/a | n/a | n/a | n/a | A (zero-shift part) | A only for the zero-shift shell (compactness 0.333 < 8/9). With a shift it is stationary, not static. Shift cap from F7 instead | n/a | A for the static spheres it joins [D-38] | n/a |
| ADM/centre of mass, Nerz (F3) (AF, P defined) | ? (E = 0, P = 0 → no CM motion to speak of) | same | ? | ? | A → needs propulsion [D-07] | A → coast only; start/stop needs momentum exchange | ? | A (Bondi balance) → photon-rocket cost [D-69] | n/a |
| Pfenning–Ford QI [D-67] (free scalar, short sampling) | A → Planck-thin wall [D-29] | A (stronger cost [D-34]) | A where negative | A where negative | n/a (no negative energy) | n/a if EC hold | A (reduced) | n/a | ? |
| Everett–Roman; Finazzi–Liberati–Barceló [D-13, D-71] (v > c, horizon) | A | A | A at v > c | A (horizons, per authors) | n/a | n/a (no horizon) | A at v ≥ c | n/a | ? |

**Reading the ledger.**
- No positive-energy metric escapes all of the "superluminal" theorems. The N ≠ 1 shells escape SSV and Natário, but stay under Olum, Gao–Wald and the PMT.
- Every superluminal claim either sits in the Natário class (NEC fails) or is not a travel-time advance.
- The only hypotheses a positive-energy FTL metric could break are:
  - P5, the generic condition: breaking it buys nothing, since a vacuum, tide-free path is plain Minkowski;
  - P6, completeness/singularities: needs singular sources whose own junction stress must still meet the NEC;
  - P4, asymptotic flatness: changes the question.

### 4. Load-bearing assumption
**P3 together with P2: "superluminal" means a travel-time advance in an asymptotically flat exterior, judged against the pointwise NEC.**
- Under this pairing, Olum and Gao–Wald decide (A) analytically, as "no".
- Loosen either half and the answer flips to a trivial "yes":
  - with "superluminal = shift exceeds lapse", Fell–Heisenberg-type claims count, though they still violate the WEC [D-05];
  - with averaged energy conditions in de Sitter, see [D-75];
  - with cosmological recession, the answer is "yes" with no warp at all.
- What would test it: the examiner's travel-time integral on each metric (our F4–F7 does it for the shell family), plus a search for any NEC-satisfying, complete, asymptotically flat metric with an advance. The theorems say that search must come back empty.
- For (B), the load-bearing premise is **P8**: whether the 2024 shell is a genuine source-consistent solution. Its decisive test is a full Einstein-plus-matter solution of a shifted elastic shell, with exact all-observer energy-condition checks.

### 5. Settled versus open
**Settled by the dossier plus this lens:**
- Q1a and Q1b.
- Q2a.
- Q2b: settled by theorem, and illustrated by F5–F7.
- Q3a and Q3c (F3).
- Q4a.
- Q5 qualitatively: interior time slows [D-07]; no travel-time gain (F4); mass 4.5e22 × the payload [D-23].
- The Alcubierre and Natário verdicts (NEC fails, E_ADM = 0, so DEC fails by rigidity) (F2).

**Open:**
- Q1c and Q1d: is the 2024 shell valid, and with what matter model? (D-31, D-84, Barzegar Error 18.)
- Q3b: an accelerating positive-energy solution with solved dynamics.
- Q4b in general: we have only a profile-specific cap, with no theorem.
- Lentz's C⁰ objection: only a preprint answers it [D-30].
- Whether ADM (E, P) is well-defined for each construction's decay (P11).
- Q6 numbers (engineer lens).

## Calculations
- `runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-decomposer_transit_time.py`: one-way null transit time along the shift axis of the rebuilt Fuchs shell (SI, ns), against flat-space light.
  - Published mass, D = 1e3 m: +240.0 ns (β = 0), +233.3 ns (β = 0.04), +150.8 ns (β = 0.95). No advance.
  - Co- versus counter-propagating difference: 6.86 ns at β = 0.02 and 13.72 ns at β = 0.04.
  - Light shell (0.01 M) at β = 0.04: −1.87 ns, an advance.
  - Weak-field Shapiro check: 231 ns (D = 1e3 m).
  - Cavity lapse² = 0.579.
- `runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-decomposer_advance_vs_nec.py`: all-observer NEC/WEC/SEC/DEC scan (285 points, h = 0.05 m and 0.025 m, geometric units, m⁻²).
  - Published mass, β = 0 and 0.02: 0 violations, all type I.
  - Published mass, β = 0.04: 22 NEC violations, worst −7.9e-5 m⁻².
  - Light shell, β = 0.04: 167 violations, worst −1.7e-4 m⁻².
  - Minimum Eulerian density positive in all cases.
- `runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-decomposer_thresholds.py`: bisection for the first NEC failure and the first advance in β_warp, at five masses (table in F7).
  - β_NEC = 0.0246 at the published compactness 0.333.
  - The advance threshold is always above the NEC threshold.

## Candidate answers (at least 3; the null and a reframe count)
- [DECOMPOSER-A] **Null.** No warp spacetime moves a payload faster than light, in the travel-time sense, without violating the NEC. The positive-energy subluminal shells are massive vehicles that coast. Starting, stopping or steering them needs momentum exchange costed like a rocket. They beat a rocket at nothing: interior clocks run slow, they offer no time advance, and they carry about 4.5e22 × the payload's mass.
  - status: surviving.
  - Why: Olum and Gao–Wald need only the NEC, the generic condition and completeness, which cover N ≠ 1 shells [D-59, D-60]. The PMT (E ≥ |P|) bars faster-than-light coasting of a whole DEC configuration (F2). Momentum conservation bars self-propulsion (F3). The worked family shows NEC failure before any advance appears (F5–F7).
  - Distinguishing test: any metric whose energy conditions are certified for all observers (interval certificates [D-73]), with a computed one-way advance between exterior rest points, would refute it. The theorems predict none exists.
  - confidence: high.
- [DECOMPOSER-B] **Option.** Positive-energy (all-observer energy conditions) subluminal warp shells with N ≠ 1 and curved slices exist as **coasting vehicle shapes**. The interior frame-dragging shift is capped by the shell's compactness: β_warp ≲ 0.08 × 2GM/(c²R₂) in the rebuilt Fuchs family, so ≲ 0.07 even at the Buchdahl limit. That makes them genuine solutions but not drives.
  - status: surviving but strained.
  - Why: our rebuild passes all four conditions at the paper's β = 0.02 (F6). But source consistency is contested (Barzegar Error 18 [D-31]), the regularized-shell preprint is self-contradictory [D-84], and our cap is profile-specific.
  - Distinguishing test: a source-consistent TOV-plus-shift solution with an elastic or anisotropic matter model [D-74], checked by exact type-I tests, should confirm B. If no such solution exists at any nonzero shift, B fails and A wins outright. Second test: does the interval-certified NEC margin vanish linearly in β at fixed compactness? B predicts a cap linear in compactness.
  - confidence: medium.
- [DECOMPOSER-C] **Reframe.** The question "can warp geometry move a payload without negative energy" dissolves into momentum bookkeeping. Centre-of-mass motion of any isolated system is P/E, with P conserved, and E ≥ |P| under the DEC (F2, F3). So no geometry, positive or negative, propels anything. Warp geometry can only rearrange the interior: frame dragging (a Sagnac-type ~10 ns asymmetry, F4), clock rates (slower, under positive energy [D-07]) and tides. The real question becomes whether such interior rearrangement can lower the propulsion cost below a photon rocket's. The evidence says it raises the cost by the shell-to-payload mass ratio (about 4.5e22 [D-23, D-39]) times the rocket's mass ratio. Le's steering cost is e^(−3L) [D-38].
  - status: surviving.
  - Distinguishing test: a computed start-and-stop of a positive-energy shell whose required momentum exchange is below the payload-only photon-rocket requirement would refute it. C predicts the exchange scales with total (shell + payload) mass-energy.
  - confidence: high.
- [DECOMPOSER-D] **Loophole.** Faster-than-light travel without pointwise negative energy through a broken theorem hypothesis. Options: a non-generic fastest path; singular or distributional sources (Lentz's C⁰ planes); null incompleteness; or a non-asymptotically-flat background (de Sitter bubble [D-75]).
  - status: eliminated under the brief's definitions (P2–P4).
    - A non-generic path in vacuum with no tidal force is locally Minkowski and gains nothing.
    - Sheets carry their own Israel surface stress, which must meet the NEC.
    - The de Sitter case meets the conditions only "up to a total divergence" [D-75], so it fails pointwise, and its background is not asymptotically flat.
  - Distinguishing test: an exhibited null-complete, asymptotically flat metric with distributional sources whose surface stresses meet the NEC and which shows a time advance would revive D. Gao–Wald predict impossibility for points far enough out.
  - confidence: medium-high, since the K′ ≫ K caveat of Gao–Wald leaves a finite-region gap that only Olum's local definition closes.
- [DECOMPOSER-E] **Semiclassical supply.** Quantum fields supply the NEC violation, under established semiclassical gravity, at quantum-inequality-allowed levels.
  - status: eliminated as an answer to "without negative energy", by definition. As a route to faster-than-light travel it is strained: walls must be about 1e-32 m thick, with |E| ≈ 1e63 kg for R = 100 m and v = 10 c [D-29]. Exponential instability also arises at the front wall [D-13].
  - Distinguishing test: a measured gravitating negative energy density (Archimedes-type weighing of vacuum energy [D-19, D-43]) or a quantum-inequality violation in squeezed light [D-55] would reopen it.
  - confidence: high.

## What would change my mind
- A certified (interval-arithmetic or exact type-I) all-observer NEC pass for a metric with a computed travel-time advance between asymptotically flat rest points. That would mean an error in my reading of Olum and Gao–Wald's hypotheses.
- A source-consistent 2024-type shell whose NEC cap on the shift grows faster than linearly in compactness, or whose cavity lapse exceeds 1. Bobrick–Martire say the latter needs negative energy [D-07]. Either would loosen B's cap and the "clocks slow" claim.
- A primary-source result that ADM momentum is not defined or not conserved for the decay rates these shells have (Nerz's caveat, F3). C's bookkeeping argument would then need the Bondi version only.
- Confirmation of Barzegar Error 18 by an independent group, which would move B to eliminated.

## Assumptions I relied on
- `warp_shell.py` reproduces the published shell well enough for thresholds. Its smoothing span is the tool's own choice. Thresholds may shift by tens of per cent with the wall profile.
- The 285-point x–z sample (five angles) resolves the worst NEC regions. This is not exhaustive. Type-IV labels come from sampled boosts and null directions.
- The straight axial path is representative for the advance test. Off-axis paths and paths around the shell were not searched, and a fastest path could differ.
- Schwarzschild-coordinate time in the shell frame is the asymptotic rest-frame time. Flat-space light over ±D is the reference "undisturbed exterior" signal.
- The positive-mass theorem and centre-of-mass results are quoted from abstracts or full text as marked. Their decay hypotheses are assumed to hold for compact-support shells with Schwarzschild exteriors.
