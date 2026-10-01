# Analysis: engineer (Archimedes: what it would take to build, in numbers)
status: final

## Method applied
For each candidate construction I compare the required quantities (mass, energy, density, stress, negative-energy density, speed, measurement sensitivity) with the best demonstrated values, compute log10(required/demonstrated) in Python, give the scaling law, keep engineering limits apart from physics limits, assign a TRL to the key component, and name the next milestone experiment. The 2024 shell is rebuilt with the run's `warp_shell.py`; the trip comparison uses `rocket_tools.py`. Units are SI unless marked geometric (G = c = 1). All gap numbers come from [calc: runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-engineer_build_gaps.py].

## Findings
- F1. **Only one positive-energy build target.** Of the named constructions, only the 2024 shell has an energy-condition claim that no peer-reviewed source has conceded or refuted, so it is the only positive-energy option to cost out. Its validity is contested: Barzegar Error 18 is a preprint [D-08, D-31, D-84]. Its energy-condition-checked case is beta_warp = 0.02. The 0.04c figure belongs to the time-delay table, according to the run's rebuilt `warp_shell.py` docstring, which quotes the paper.
- F2. **Every superluminal option needs negative energy or DEC-violating matter at the reference case:**
  - Alcubierre: −7.48e31 kg (Eulerian) at R = 100 m, Δ = 1 m, v = 10c [D-28].
  - Natário: −6.0e33 kg at v = 1c [D-34].
  - Fell–Heisenberg concede that the WEC fails [D-05].
  - Lentz's positivity is disputed [D-30].
  - Superluminal positive-energy spherical drives need DEC-violating "superluminal matter" [D-65].
- F3. **Archimedes, demonstrated sensitivity.** The room-temperature prototype at SAR-GRAV, Sardinia: [new: Allocca et al. 2024, EPJ Plus 139, 158, doi:10.1140/epjp/s13360-024-04920-x, submitted version at boa.unimib.it, full-text, "the sensitivity in torque ˜τn is about ˜τn ≈ 2 ∗ 10−12Nm/ √ Hz at 10 mHz and reaches a minimum of about ˜τn ≈ 7 ∗ 10−13Nm/ √ Hz at tens of mHz, corresponding to the force sensitivity ˜Fn of ˜Fn ≈ 3 ∗ 10−12N/ √ Hz"].
  - Required, from the same source (pp. 1–2): "The amplitude of the weight variations is expected to be of the order of few 10−16 N modulated at a frequency of about 10 mHz", and "a sensitivity balance better than 10−13Nm/ √ Hz is required, with a balance arm 1.4 m long, so to detect the signal in an integration time of the order of 106 s (about 2 weeks)".
  - Gap: 0.85 orders in torque. In force, 3e-15 N (1σ over 1e6 s) against 5e-16 N is 0.78 orders [calc].
- F4. **Translational (motional) gravitomagnetism is already tested in the weak field.** This is the premise behind a shift sourced by matter currents.
  - Lunar laser ranging: [new: Murphy, Nordtvedt & Turyshev 2007, PRL 98, 071102, arXiv:gr-qc/0702028, abstract, "the effect has in fact been confirmed via lunar laser ranging (LLR) to approximately 0.1% accuracy"]. Contested by [new: Kopeikin 2007, PRL 98, 229001, abstract, "lunar laser ranging (LLR) is not currently capable to detect gravitomagnetic effects"].
  - Light passing a moving mass, the analogue of the Fuchs time-delay observable: [new: Kopeikin et al. 2007, GRG 39, 1583, arXiv:gr-qc/0510077, abstract, "the 2002 deflection experiment of a quasar by Jupiter where the aberration of gravity from its orbital motion was measured with accuracy 20%"].
  - Both test only the linear term. Jupiter's compactness is about 1e-8, not the 0.33 of the shell.
- F5. **The 2024 shell rebuilt at the published parameters** (R1 = 10 m, R2 = 20 m, M = 4.49e27 kg, beta = 0.02):
  - mass and compactness: M_ADM = 4.51e27 kg = 2.38 M_J, with 2GM/(c²R2) = 0.335;
  - peak energy density: 1.38e40 J/m³ (ρ = 1.53e23 kg/m³);
  - peak stresses: radial 9.6e38 Pa; tangential from −1.2e38 to +3.9e39 Pa;
  - energy conditions: the zero-shift shell meets all four exactly (type I), with max |p|/ε = 0.60;
  - static lapse at the centre: 0.761 [calc].
  These match D-22 (mean density 1.53e23 kg/m³; ρc² = 1.4e40 Pa). With the shift turned on, the all-observer energy-condition test is the constraints lens's job; I did not redo it.
- F6. **Build gaps for the published shell** (log10 of required/demonstrated) [calc]:
  - mass against the ISS (419,725 kg): **22.0**. Source: [new: NASA, "Space Station Facts and Figures", nasa.gov, full-text, "Mass: 925,335 pounds (419,725 kilograms)"];
  - Mc² = 4.0e44 J against one year of world primary energy (5.9e20 J [D-46]): **23.8**;
  - peak density against osmium: **18.8**; against nuclear saturation (0.16 fm⁻³, a standard value not sourced here): **5.8**;
  - peak stress against 1 TPa static [D-44]: **27.6**; against nanodiamond yield: **27.9**; against ρ_nuc c²: **5.2**;
  - speed 0.02c against the Parker Solar Probe [D-45]: **1.5**; 0.04c: **1.8**.

  Speed is the only gap below 2 orders.
- F7. **Scaled to a 100 m payload** (ours: self-similar, fixed compactness):
  - M = 4.5e28 kg = 23.8 M_J;
  - mass gap 23.0; energy gap 24.8;
  - density 3.8 orders above nuclear; stress 25.6 orders above 1 TPa [calc].
- F8. **Scaling law, and what shrinks the gap** (ours). At fixed compactness C = 2GM/(c²R2):
  - M = C c² R2/(2G) ∝ R2;
  - ρ_mean ∝ C/R2²;
  - stress ∝ C²/R2².

  Growing the shell lowers the density but raises the mass:
  - Mean density reaches nuclear saturation at R2 = 15 km (M = 1.7 M_sun), which is a neutron star.
  - It reaches osmium density only at R2 = 5.2e10 m (M = 5.9e6 M_sun) [calc].

  No size brings mass, density and stress all within reach. The trade is fixed by compactness, a physics limit (Buchdahl/Andréasson [D-27]), not by engineering.
- F9. **Why the compactness can't be lowered much** (ours; weak-field, order of magnitude, used beyond its domain at C = 0.33).
  - In linearised GR, counterflowing mass currents ±P at R1 and R2 give a uniform interior shift beta = (4GP/c³)(1/R1 − 1/R2) and no net exterior momentum.
  - The DEC caps cP at the flowing energy E_flow. So beta = 0.02 at R1 = 10 m, R2 = 20 m needs E_flow ≥ 1.2e43 J = 1.35e26 kg-equivalent, which is 0.03 of the published Mc² [calc]. This is consistent with the published mass if the matter carries momentum equivalent to a counterflow of about 0.03c.
  - With flows at material speeds (10 km/s), the same shift needs 4e30 kg. Even a crawling beta = 1e-6 (300 m/s) needs 2e26 kg.
  - The law is beta ~ compactness × (u/c). The required mass scales linearly with beta and with R, and inversely with the internal flow speed.
- F10. **Manufacturing tolerance.** The shell's density edge must be smoothed over at least about 1 m, which is 10% of the wall thickness.
  - With the smoothing span set to 0.5 m, the zero-shift shell already fails the DEC (max |p|/ε = 1.15).
  - At 1 m it holds (0.60); at 2 m it holds (0.32) [calc].
  - The unsmoothed shell carries a hoop-stress sheet that violates the DEC (`warp_shell.py` docstring). The radial profile of a 2-Jupiter-mass object must be shaped to better than about 1 m.
- F11. **Assembly heat.** Assembling the shell releases a binding energy of about GM²/R̄ = 9e43 J, or 0.22 Mc², which is 1.5e23 world-years of primary energy. It would have to be radiated away during construction (Newtonian estimate) [calc].
- F12. **Trip to α Cen, 1e5 kg payload, photon-rocket propulsion for the start and stop** [calc, rocket_tools.py]:

  | Option | Mass ratio | Propellant energy | Trip time |
  |---|---|---|---|
  | Shell plus payload at 0.04c | 1.083 | 3.4e43 J = 5.7e22 world-years (22.75 orders above one world-year) | coast 109 yr |
  | Same payload alone at 0.04c | 1.083 | 7.5e20 J = 1.3 world-years | coast 109 yr |
  | Payload alone, 1 g photon rocket | 40.4 | 3.5e23 J | 3.58 yr ship time, 6.00 yr Earth time |

  The shell multiplies the propulsion bill by M_shell/m_payload = 4.5e22 (22.65 orders).
- F13. **The shell's only rocket-beating feature is a modest proper-time saving.** The interior static lapse is 0.761 [calc], so the crew ages about 24% less than exterior clocks: about 83 yr on the 109 yr coast at 0.04c. A 1 g rocket gives 3.58 yr ship time.
  - No inertia-free acceleration is on offer either. The only worked start-stop construction (Le, preprint) states that "an observer needs a force to follow the accelerating cavity center" [D-72].
  - Its radiative steering costs m_i/m_f = e^(3L) [D-38]. Taking L as the rapidity path length 2 artanh(v), which is our reading, that gives 1.27 at 0.04c start and stop, against 1.083 for an ideal photon rocket [calc]. Steering costs more than a plain photon rocket.
- F14. **Superluminal options against the best demonstrated negative energy.** The best is the Casimir effect at the smallest measured separation [new: Mohideen & Roy 1998, PRL 81, 4549, abstract, "The force was measured for plate-sphere surface separations from 0.1 to 0.9 μm"].
  - The parallel-plate energy density at 0.1 µm is −4.3 J/m³. A hypothetical 1 m² cavity holds −4.3e-7 J.
  - Peak |ρ| required for Alcubierre at R = 100 m, Δ = 1 m: 1.2e42 J/m³ at v = 1c and 1.2e44 J/m³ at v = 10c. The density gaps are **41.4** and **43.4** orders.
  - Total-energy gaps against the 1 m² cavity:

    | Option and case | Gap (orders) |
    |---|---|
    | Alcubierre, 10c | 55.2 |
    | Natário, 1c | 57.1 |
    | Rodal, at the author's v = c case | 50.5 |
    | Alcubierre, QI-limited wall | 87.2 |

  - Against one year of world energy, the required magnitudes are 23–30 orders over for the walls above, and 60 orders at the QI-limited wall.
  - The QI wall (1.6e-32 m [D-29]) is 12 orders below the LHC probe scale (1.45e-20 m) and 21.8 orders below a 1 Å tolerance [calc].
  - None of the laboratory negative energy is shown to gravitate [D-16, D-19].
- F15. **Lab gravitomagnetism, the nearest premise test for a shell.**
  - A 1e4 kg rotor of R = 1 m at a 1 km/s rim gives a frame-dragging rate of about 1.5e-20 rad/s.
  - The demonstrated ring-laser noise is [new: Di Virgilio et al. 2024, PRL 133, 013601, arXiv:2301.01386, abstract, "GINGERINO active--ring laser upper limiting noise is close to $2 \times 10^{-15}$ rad/s for $\sim 2 \times 10^5$ s of integration time"].
  - The gap is **5.1 orders** [calc].
  - The same mass used as a translational counterflow gives an interior beta ≈ 1e-28. That is 26 orders short of the shell's 0.02, so a lab test can probe only the linear gravitomagnetic physics, never a warp-scale shift.
- F16. **A self-propelled claim can be tested now, and GR predicts zero thrust.**
  - The Tajmar balance resolves thrust below the 3.3 nN/W photon-thrust level [U-01].
  - The Eagleworks-class claim of 1.2 µN/W is excluded by 2.6 orders [calc]. The momentum accounting is [D-69].
  - Any lab "warp" thruster, such as the unreported Astrum EM-field "recipe" [D-82], must show thrust above about 3 nN/W on such a balance.
- F17. **Gravitational-wave memory as a technosignature.** Boosting the 2.4 M_J shell to 0.04c (kinetic energy 3.2e41 J) would give a memory strain of about 3.5e-22 at 1 kpc and 3.5e-25 at 1 Mpc. This is a Newtonian-order estimate (ours) [calc].
  - At 1 kpc it is near ground-detector strain levels in amplitude, but the bandwidth is not modelled.
  - It bears on D-77 and D-78 (searches for a non-zero-ADM-mass accelerating warp object). It is an observation, not a build milestone.

## Lens-specific outputs

### Required against demonstrated, with gaps (log10 required/demonstrated)
| Option | Quantity | Required | Demonstrated (source) | Gap (orders) | Scaling law |
|---|---|---|---|---|---|
| Fuchs shell (published) | Mass | 4.5e27 kg | ISS 4.2e5 kg (NASA) | 22.0 | M = C c²R/(2G) ∝ R |
| Fuchs shell | Rest energy | 4.0e44 J | 5.9e20 J/yr world [D-46] | 23.8 | ∝ R |
| Fuchs shell | Peak density | 1.5e23 kg/m³ | nuclear 2.7e17 (standard); osmium 2.3e4 | 5.8; 18.8 | ∝ C/R² |
| Fuchs shell | Peak stress | 3.9e39 Pa | 1 TPa static [D-44] | 27.6 | ∝ C²/R² |
| Fuchs shell | Edge tolerance | ≥ 1 m smooth edge on a 2 M_J body | none | n/a | span/(R2−R1) ≳ 0.1 |
| Fuchs shell | Speed | 0.02–0.04c | 6.4e-4c, Parker Solar Probe [D-45] | 1.5–1.8 | — |
| Fuchs shell | Start-stop energy at 0.04c (photon rocket) | 3.4e43 J | 5.9e20 J/yr | 22.75 | ∝ M(v) |
| Fuchs shell, 100 m payload (ours) | Mass; density over nuclear; stress | 4.5e28 kg; 1.5e21; 3.9e37 Pa | as above | 23.0; 3.8; 25.6 | — |
| Alcubierre, R = 100 m, Δ = 1 m, 10c | Negative energy density | 1.2e44 J/m³ | Casimir 4.3 J/m³ at 0.1 µm | 43.4 | ∝ v²/Δ² |
| Alcubierre (same case) | Total negative energy | 6.7e48 J | 4.3e-7 J (1 m² cavity, hypothetical) | 55.2 | ∝ v²R²/Δ |
| Natário, 1c | Total negative energy | 5.4e50 J | as above | 57.1 | ∝ v²R⁴/Δ³ |
| Rodal, v = c (author's parameters) | E₋ | 1.3e44 J | as above | 50.5 | not given |
| Alcubierre, QI-limited wall | Wall thickness | 1.6e-32 m | 1.45e-20 m LHC probe scale | 12.0 | Δ ∝ v L_P |
| Lentz / Fell–Heisenberg | Source | Einstein–Maxwell plasma soliton (Lentz); WEC-violating matter (Fell–Heisenberg concede) | none exhibited | not computable | E ~ v²R²/w [D-30a] |
| Lentz, R = 100 m, w = 1 m, 10c | Organized source energy | 3.6e48–8.9e48 J (20–50 M_sun) | NIF 8.6 MJ [D-47]; 5.9e20 J/yr world | 41.6–42.0; 27.8–28.2 | ∝ v²R²/w |
| Le radiative steering | Mass ratio for start and stop at 0.04c | 1.27 (e^(3L)) | photon rocket 1.083 | worse than a photon rocket | e^(3L) |

### Engineering limits, separate from physics
- **Materials.** No engineered material can carry 1e38–1e39 Pa. Even nuclear matter's ρc² (2.4e34 Pa) is 5 orders short at R = 10 m. The shell's stress would have to be carried by self-gravity, as in a neutron star.
- **Power and heat.** Assembly releases about 0.22 Mc² = 9e43 J. Boost and stop need 3.4e43 J at 0.04c. Both are about 23 orders above humanity's annual primary energy.
- **Control and stability.** The edge profile must be smooth to about 1 m or the DEC fails (F10). The stability of non-spherical or perturbed shells is open [D-74], and growing normal modes are reported in self-similar shells [D-72].
- **Cost.** Not estimable meaningfully. Collecting 2.4 M_J means dismantling a planet the size of Jupiter, roughly twice over. Our order of magnitude at today's 6.6 t/yr of mass-energy [D-46] is about 1e23 years of world output.
- **Physics limits that decide.** Compactness ≤ 8/9 (Buchdahl) [D-27] fixes the mass–density trade in F8. The NEC theorem for unit-lapse flat-slice drives (Santiago–Schuster–Visser [D-41]) and Olum [D-59] force negative energy on every superluminal option.

### TRL of each option's key component
| Option | Key component | TRL | Evidence |
|---|---|---|---|
| Alcubierre / Natário / Rodal / VdB | Macroscopic, gravitating, controllable negative energy | 1 | Sub-vacuum effects are observed (Casimir, 15 dB squeezing, dynamical Casimir effect [D-16]). None is shown to gravitate; Archimedes is unrun [D-19]. The QIs cap the wall at 1.6e-32 m [D-29] |
| Lentz soliton | A solved Einstein–Maxwell plasma source with positive energy for all observers | 1 (contested) | No full source solution [D-06]; the direct recomputation finds negative regions [D-30] |
| Fell–Heisenberg | WEC-violating matter | 1 | Authors concede the WEC fails [D-05] |
| Fuchs 2024 shell (coast) | A 2.4 M_J matter shell at C = 0.33 with internal momentum flux | 1–2 | A concept with one numerical demonstration, found by trial and error [D-08]. Contested as a solution [D-31], and the observer-robust test covers only a regularized version [D-26, D-84]. No material or assembly route |
| Shell start and stop | Externally propelled (photon) steering | 1 | Preprint junction construction only [D-72] |
| Shell, self-propelled | Change of ADM momentum without ejecta | 0 | Unsupported; "any warp drive requires propulsion" [D-07, D-69] |

### Next milestone for each option (the smallest demonstration that raises its TRL or kills it)
| Option | Milestone | Predicted effect | Demonstrated sensitivity | Gap (orders) | Who / when |
|---|---|---|---|---|---|
| Negative-energy (superluminal) family | Archimedes cryogenic run: does Casimir-type vacuum energy weigh? | few × 1e-16 N | 3e-12 N/√Hz prototype → 3e-15 N over 1e6 s | 0.8 | INFN Archimedes collaboration (SAR-GRAV); no cryogenic-run date found |
| Negative-energy family | Decisive calculation: a self-consistent semiclassical solution with the QI-respecting ⟨T_μν⟩ at a macroscopic wall | — | — | — | theory |
| Fuchs shell | Decisive calculation: an independent full Einstein solve of the shifted shell, with exact type-I tests at shell and edge resolution | — | — | — | any numerical-relativity group, now |
| Fuchs shell premise (gravitomagnetism from mass currents) | Lab rotor beside a ring laser | about 1.5e-20 rad/s | 2e-15 rad/s (GINGERINO) | 5.1 | not planned |
| Same premise, weak field | LLR and Jupiter deflection | GR term | 0.1% (contested) / 20% | already met | done |
| Self-propelled claims | nN/W thrust balance on any claimed device | 0 in GR | < 3.3 nN/W (Tajmar et al.) | ready | TU Dresden-class labs, now |
| Shell as technosignature | GW memory from a 2.4 M_J shell boosted to 0.04c | 3.5e-22 at 1 kpc | ground-detector band (not modelled) | not computed | archival |

## Calculations
- `runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-engineer_build_gaps.py` (log beside it). It computes:
  - the rebuilt 2024 shell at the published and ×10 parameters: M_ADM = 4.51e27 kg, C = 0.335, peak ε = 1.38e40 J/m³, peak p_t = 3.9e39 Pa, lapse 0.761;
  - every gap in the table above;
  - the scaling law at fixed C (nuclear density at R2 = 15 km, 1.7 M_sun; osmium density at 5.2e10 m, 5.9e6 M_sun);
  - the weak-field counterflow bound (E_flow,min = 1.2e43 J for beta = 0.02);
  - the photon-rocket and Le steering costs (1.083 against 1.27 at 0.04c), the 1 g trip (3.58 yr ship, mass ratio 40.4) and the shell propulsion energy (3.4e43 J);
  - the Casimir density 4.3 J/m³ at 0.1 µm, against 1.2e44 J/m³ required (43.4 orders);
  - Archimedes (0.78–0.85 orders), the lab rotor (5.1 orders) and the GW memory (3.5e-22 at 1 kpc);
  - smoothing sensitivity (the DEC fails at a 0.5 m span) and assembly heat (9e43 J).

  Runtime 0.2 s. Grid convergence is not separately tested; the smoothing-span scan is the sensitivity check that matters.

## Candidate answers (at least 3; the null and a reframe count)
- [ENGINEER-A] **Null, the engineering half.** No warp spacetime that moves a payload faster than light can be built without negative energy.
  - Every superluminal option needs gravitating negative energy 41–43 orders denser than the best Casimir cavity, and 50–57 orders more in total than a square metre of it holds. At the quantum-inequality limit the gap is 87 orders.
  - The positive-energy shell does nothing a far lighter rocket can't, apart from a roughly 24% clock-rate saving.
  - | status: surviving | why: the gaps in F14 hold with or without Lentz's contested positivity, because the Fell–Heisenberg and Bobrick–Martire superluminal cases need WEC- or DEC-violating matter [D-05, D-65] | test: a gravitating, sustainable negative energy density measured anywhere; Archimedes is the nearest premise test (0.8 orders) | confidence: high
- [ENGINEER-B] **The 2024 shell can coast in principle, if its solution holds, but is unbuildable by 2100.**
  - Gaps against demonstrated capability: mass 22.0 orders; energy 23.8; density 5.8 above nuclear matter; stress 27.6 above any material.
  - The edge must be smooth to 1 m on a 2.4 M_J object, and no size escapes the mass–density trade.
  - TRL 1–2.
  - | status: strained (in principle: contested as a solution [D-31]); eliminated in practice | why: F6–F11 | test: an independent full Einstein solve with exact energy-condition tests (decisive calculation); there is no experiment within 5 orders of a warp-scale shift | confidence: high (practice), medium (principle)
- [ENGINEER-C] **Reframe: the "warp shell" is a gravitomagnetic frame-dragging chamber inside a very heavy vehicle.**
  - Its shift scales as beta ~ compactness × (internal flow speed / c). A useful shift therefore needs near-black-hole compactness and relativistic internal currents.
  - Its velocity relative to the exterior must come from ordinary external propulsion, at 4.5e22 times the payload-alone bill (Le's steering is costlier still).
  - Its only gains over a rocket are the interior clock slowdown (lapse 0.761) and geodesic passengers while coasting.
  - | status: surviving | why: F9, F12, F13 | test: weak-field translational gravitomagnetism is already confirmed (LLR 0.1%, Jupiter 20%); a lab rotor with a ring laser is 5.1 orders short | confidence: medium (the counterflow bound is our weak-field estimate)
- [ENGINEER-D] **Self-propelled positive-energy warp travel (no ejecta).** | status: eliminated | why: there is no construction. Bobrick–Martire and the momentum accounting require propulsion [D-07, D-69], so TRL 0. | test: any device claim must beat 3.3 nN/W on a Tajmar-class balance [U-01]; GR predicts zero | confidence: high
- [ENGINEER-E] **Lentz-type positive-energy superluminal soliton.** | status: eliminated as a build option | why: no exhibited plasma source; its energy is of the same order as Alcubierre's (tenths of a solar mass × v_s² at R = 100 m [D-30a]); positivity disputed [D-30]. Even if positive, it needs 20–50 M_sun of organized plasma at v = 10c, which is 3.6e48–8.9e48 J. That is 41.6–42.0 orders above the largest controlled fusion yield (NIF, 8.6 MJ [D-47]) and 27.8–28.2 orders above one year of world energy [calc]. | test: an independent all-observer calculation of the Lentz metric | confidence: medium

## What would change my mind
- A peer-reviewed, independent full Einstein solution of the shifted shell at much lower compactness (C ≲ 1e-3) with beta ≳ 1e-3. That would break my weak-field scaling beta ~ C·u/c, and would cut the mass gap by more than 2 orders.
- A measurement that laboratory negative energy gravitates, with a sustainable density far above the Casimir 4.3 J/m³.
- A start-stop construction with no ejecta that conserves ADM momentum.
- Archimedes, or a successor, finding that vacuum energy does not weigh as expected. That would weaken every negative-energy option further.

## Assumptions I relied on
- The `warp_shell.py` rebuild with its default smoothing span of 1 m (ours, not the paper's) represents the published shell. The peak tangential stress varies by a factor of about 3 across spans of 0.5–2 m.
- Nuclear saturation density 0.16 fm⁻³ and osmium density 2.26e4 kg/m³ are standard values, not sourced in this run.
- The counterflow bound (F9) is linearised GR applied at C = 0.33, so it is only good to an order of magnitude.
- In Le's e^(3L), L is the rapidity path length 2 artanh(v) for a start and a stop.
- The Casimir comparison uses the ideal parallel-plate formula at the smallest separation measured in a sphere–plate geometry, and a hypothetical area of 1 m².
- The GW-memory estimate h ~ 4G·KE/(c⁴d) is Newtonian-order only.
- The rotor frame-dragging estimate Ω ~ 2Gmω/(c²R) is order of magnitude.
