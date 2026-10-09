# Analysis: engineer (Archimedes: what it would take to build, in numbers)
status: final

## Method applied
For each construction that survives as a traversable wormhole, compare required quantities (mass, energy, field, charge, temperature, negative-energy density, size) with demonstrated values, compute log10(required/demonstrated) in Python, give the scaling law, the engineering limits, a TRL for the key component, and the next milestone. Owner of the brief's cost table and test-sensitivity table.

## Findings
1. MMP parameter relations, read from the paper (ħ = c = 1): "E = r3 e GN𝓁2− q 8𝓁 (5.30) ... 𝓁 = 16 r3 e GNq = 16π3/2q2lp g3 , E min =−GNq2 256r3 e =− g3 256π3/2qlp (5.31)". Hence r_e = √π q l_p/g, and |E_min| = g²ħc/(256π r_e): the energy that can be added before the throat is destroyed falls as 1/r_e, so widening an MMP throat at fixed coupling and field content lowers its payload capacity. Validity: "valid only when 𝓁≪q3lp (5.43)". The Standard-Model version needs "re, is much smaller than the electroweak scale (say 1/TeV)". The paper also links temperature to throat length by "T = 1 2π𝓁 (5.28)". [new: Maldacena, Milekhin & Popov, arXiv:1807.04726, full-text, quotes as printed above] [D-06] [Q-10] [Q-11]
2. Demonstrated-capability anchors gathered for this lens (dossier lacks them):
   - Continuous field record 45.5 T [new: Hahn et al. 2019, Nature 570, 496, title via Crossref (lit_search), "45.5-tesla direct-current magnetic field generated with a high-temperature superconducting magnet"]; destructive pulsed 1200 T for about 100 µs [new: physicsworld.com, search-summary, SUMMARY "researchers in Japan used a less violent indoor process to reach 1200 T for 100 µs"].
   - Lowest temperature 38 pK, in a free-falling BEC of about 10⁵ Rb atoms, held about 2 s [new: Deppner et al. 2021 PRL via livescience/space.com, search-summary, SUMMARY "Christian Deppner and colleagues in the QUANTUS project achieved a record for the lowest temperature at 38 picokelvin"].
   - World primary energy use 592 EJ in 2024, i.e. 6.6×10³ kg of mass-energy per year [new: Energy Institute Statistical Review 2025 via news reports, search-summary, SUMMARY "the world consumed 592 exajoules of primary energy in 2024"].
   - Sparse SYK keeps the holographic (maximally chaotic) sector with only k ∼ O(1) terms per fermion [new: Xu, Swingle et al., arXiv:2008.02303, abstract, "this sparse SYK model recovers the interesting global physics of ordinary SYK even when $k$ is of order unity"]. Demonstrated hardware scale: N = 7 Majoranas, 164 two-qubit gates, fidelity below ½ of noiseless [D-16] [Q-37].
   - Casimir: smallest measured gap 0.2 µm [D-19] [Q-33]; ideal |u| there 0.27 J/m³, areal energy 5.4×10⁻⁸ J/m² [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-engineer_cost_table.py].
3. Classical Ellis/Morris–Thorne throat (SI). Required |ρ| = c⁴/(8πG b₀²): 4.8×10⁴² J/m³ at b₀ = 1 m, 4.8×10⁴⁴ at 0.1 m, 4.8×10⁵⁴ at 1 µm. Gap to the Casimir energy density at the smallest measured gap: 43.2 orders (1 m), 45.2 (0.1 m), 55.2 (1 µm); 38–50 orders even against ideal 10 nm plates. Scaling ρ ∝ b₀⁻²: equality only at b₀ = 4.2×10²¹ m (4.5×10⁵ ly). Ford–Roman band (f = 0.01, Q-21), ∝ b₀^{1/3}: 1.5×10⁻²¹ m at 1 m, 11 orders thinner than an atom; it reaches the 0.2 µm Casimir gap only at b₀ = 2.5×10⁴² m, 15.7 orders beyond the observable universe. So no throat size closes both gaps at once: shrinking the throat helps the band and hurts the density, widening does the reverse. Plate area at 0.2 µm needed to hold |Ω|c² for b₀ = 1 m: 4.5×10⁵¹ m², 37 orders above Earth's surface. [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-engineer_cost_table.py] [Q-24] [Q-26] [Q-21] [K-08]
4. Visser thin shell, flat limit: |σ| = c⁴/(2πG a) = 1.9×10⁴³ J/m² at a = 1 m, against 5.4×10⁻⁸ J/m² for Casimir plates at 0.2 µm: 50.6 orders (51.6 at 0.1 m, 56.6 at 1 µm). σ ∝ 1/a: equality at a = 3.6×10⁵⁰ m, 24 orders beyond the observable universe. Shell rest mass |m_s| = 2ac²/G = 2.7×10²⁷ kg at 1 m. [calc: same] [Q-29] [D-14]
5. MMP with Standard-Model fields (r_e = 1/TeV = 2.0×10⁻¹⁹ m, the upper limit; hypercharge unit coupling g = 0.06, my reading of "lowest charged fermion has charge one"; g = 0.3 shown for sensitivity). Flux q = 4.1×10¹⁴ (2.1×10¹⁵); mouth mass 2.7×10⁸ kg each; throat length ℓ = 1.1 m for one charge-one flavour, 2.1 cm with N_eff = 54 (my assumption that the Casimir term scales with N_eff); binding |E_min| = 7.2×10⁻¹³ J (4.5 MeV) for N = 1, 2.1×10⁻⁹ J (13 GeV) for N_eff = 54; required temperature T < 1/(2πℓ) = 0.3 mK (N = 1) to 17 mK (N_eff = 54), which dilution refrigerators reach; validity ℓ/(q³l_p) ∼ 10⁻⁹ ≪ 1. Horizon field B_h = 1.8×10³⁷ T. Formation mass-energy for two mouths: 4.8×10²⁵ J = 8×10⁴ years of world primary energy (4.9 orders above one year). Payload: 1 kg needs 25.6 more orders of binding energy and 17.7 orders more throat radius. A qubit carried by a sub-MeV charged fermion fits within |E_min|. [calc: same]
6. Widened MMP / MM 2020 at r_e = 1.5×10⁷ m: pure 4D, N = 1, |E_min| = 9×10⁻³⁹ J, less than one 1 meV photon. With the perturbativity limit g²N ≤ 1, |E_min| ≤ N ħc/(256π r_e), so the species count needed is N ≥ 2.3×10⁴⁴ (1 kg, r_e = 0.1 m), 2.4×10⁵⁴ (human, r_e = 1.5×10⁷ m), 3.4×10⁵⁵ (MM's 10³ kg ship). That is 12–24 orders above MM's cap of 10³² species. MM quote N_f > 10⁵² for the same ship; my scaling is about 3.5 orders stricter, an order-of-magnitude reproduction (the verdict, far above the 10³² cap, is the same). Mouth mass 2.0×10³⁴ kg (1.0×10⁴ M_☉), B_h = 2.3×10¹¹ T (8.3 orders above 1200 T), formation mass-energy 3.6×10⁵¹ J = 6×10³⁰ years of world energy. [calc: same] [Q-02] [Q-03] [Q-04] [Q-08]
7. MM environment. With γ = ℓ/r_e ∼ 2×10¹² (Q-02), a CMB photon reaches the traveller boosted by γ² = 4×10²⁴, i.e. 9×10²⁰ eV. Keeping it under 1 eV (my tolerance criterion) needs ambient T < 2.9×10⁻²¹ K: 21 orders below the CMB and 10 orders below the 38 pK lab record, which was reached in a 10⁵-atom cloud rather than a 10²¹ m³ region. The dark sector must be below 10⁻²⁶ eV = 1.2×10⁻²² K (11.5 orders below 38 pK). Cosmic expansion supplies this unaided: in a Λ-dominated universe (H₀ = 67.4 km/s/Mpc, Ω_Λ = 0.685, standard values assumed) the CMB falls to 2.9×10⁻²¹ K after about 8.5×10¹¹ yr; the de Sitter floor is 2.2×10⁻³⁰ K. [calc: same] [D-08] [Q-07]

8. Creating MMP or MM mouths by pair creation. Garfinkle & Strominger: "if topology change is allowed in quantum gravity, it is possible to create a Wheeler wormhole, i.e. a pair of oppositely charged extreme Reissner-Nordstrom black holes identified at their throats, in an electromagnetic field" [new: Garfinkle & Strominger 1991, PLB 256, 146, abstract]. Their rate formula was not retrieved. I use the Schwinger form exp(−πM²c³/(ħ g_m B)), my approximation, which reduces exactly to S_BH = πr_e²/l_p² when B equals the mouth's own horizon field, as the calculation confirms.
   - SM-MMP mouths at 1200 T: exponent 6.9×10⁶⁶. An unsuppressed rate needs B ∼ B_h = 1.8×10³⁷ T, 34.2 orders above the destructive-pulse record.
   - MM mouths at 1200 T: exponent 5.2×10⁹². That exceeds S_BH = 2.7×10⁸⁴ by 8 orders, so even a possible e^{S} enhancement leaves the rate effectively zero. They need B ∼ 2.3×10¹¹ T coherent over a region larger than the pair separation.
   - The other route, assembling the flux from monopoles, needs 4×10¹⁴ flux units for SM-MMP, against zero monopoles ever observed. MoEDAL excludes monopoles only up to 75 GeV, and an SM-MMP mouth weighs 1.5×10³⁵ GeV/c², 33 orders higher.
   [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-engineer_cost_table.py] [D-25] [Q-46]
9. FGM 2019 environment and strut.
   - The construction uses Hartle–Hawking states. A hole is hotter than the 2.725 K CMB only below 4.5×10²² kg (Schwarzschild formula, my proxy for the charged non-extremal hole). Heavier holes therefore need CMB isolation over a region larger than the separation d.
   - The cosmic-string strut balancing the attraction 2GM²/d² of opposite extremal charges has Gμ/c² = 2(GM/c²d)², which is 2×10⁻⁶ at d = 10³ GM/c² for any mass. No cosmic string has been observed.
   - The payload is perturbative quanta, traversability is "exponentially fragile", and the transit time is t_min = d + logs, so this is not a shortcut.
   [calc: same] [D-07] [Q-13]
10. EDM (BKR family). The fermion must satisfy q/μ < 1 in Planck units, a regime that bounds all the solutions found (Q-19), not a proven necessity.
   - Electron: q/μ = 2.0×10²¹ (Gaussian) to 7.2×10²¹ (Heaviside–Lorentz), a gap of 21.3 to 21.9 orders.
   - Top quark (my PDG-value assumption, 172.6 GeV, charge 2/3): q/μ = 4.0×10¹⁵ to 1.4×10¹⁶, a gap of 15.6 to 16.2 orders.
   - The fermion mass needed is 7×10¹⁷ to 4×10¹⁸ GeV.
   - The throat radii in Kain's static solutions are 1.2×10⁻³³ to 8.1×10⁻³³ m. Kontou says a Planck-size throat "would not be traversable" [D-27].
   - The dynamics fail as well: Kain finds them not traversable [D-11], and Weinbaum finds no two-ended solution [D-12].
   [calc: same] [Q-18] [Q-19]
11. Quantum-processor analogue. Sycamore's fidelity, below ½ of noiseless after 164 gates, implies an effective error of at least 4.2×10⁻³ per gate.
   - A chaotic sparse-SYK teleportation circuit with k = 4 terms per fermion, Jordan–Wigner strings of about N/2, 10 Trotter steps and two sides needs about 2kN²n_T gates: 3.2×10⁴ at N = 20, 2.0×10⁵ at N = 50, 8.0×10⁵ at N = 100.
   - That is 2.3 to 3.7 orders more gates, and error per gate at most 2.2×10⁻⁵ to 8.7×10⁻⁷, 2.3 to 3.7 orders lower than demonstrated. The gate count and error demand scale as N².
   - The gate model is my estimate, not sourced. It shows the gap is a few orders and closable with error correction, unlike every gravitational row.
   - As a payload channel, teleporting the state of 1 kg (about 10²⁶ atoms) or a human (about 7×10²⁷ atoms) needs 26 to 28 more orders of qubits than one teleported qubit, plus 2 classical bits per qubit sent at no more than c (MSY [D-02]). It can never beat the classical channel.
   [calc: same] [D-16] [D-17] [Q-37] [Q-39]
12. Test sensitivities [calc: same]:
   - **S2 orbit.** Needs 10⁻⁶ m/s², has achieved 4×10⁻⁴: a gap of 2.6 orders, 1.3 with the 20-year projection [Q-43].
   - **EHT.** The resolution λ/D at 1.3 mm is 21 µas. A 10⁴ M_☉ extremal mouth (MM) has a shadow of 0.79 µas at 1 kpc and 0.079 µas at 10 kpc, 1.4 to 2.4 orders below resolution.
   - **Extremal versus Schwarzschild shadow.** An extremal-RN shadow is 0.77 times a Schwarzschild one (4M against 3√3M). For Sgr A* that 23% shrinkage exceeds the ∼10% consistency window [Q-45], by my comparison. This bears on Sgr A* only, not on MM mouths.
   - **GW echoes.** The MM echo delay is πℓ/c ≈ 9.4×10³ yr [Q-06], 3.7 orders beyond a 2-year observing run.
   - **Primordial magnetic black holes.** Bai et al. say their masses "could range from the Planck scale up to the Earth mass" and that the Parker bound "can be extended by several orders of magnitude using the large-scale coherent magnetic fields in Andromeda" [new: Bai et al. 2020, JHEP 10, 210, arXiv:2007.03703, abstract]. This is the only search class that targets MMP-type objects.

## Lens-specific outputs

### A. Cost table (owner: engineer). SI units. "Gap" is log10(required/demonstrated) for the binding item.
| Construction (status) | Payload | Mass per mouth / exotic mass | Energy | Charge / field | Environment | Timescale | Binding gap (orders) | TRL key component |
|---|---|---|---|---|---|---|---|---|
| Ellis / Morris–Thorne (classical; not a shortcut by default; QI-limited) | qubit (b₀ = 1 µm) | \|Ω\| = 2.7×10²¹ kg exotic | \|ρ\| = 4.8×10⁵⁴ J/m³ | none | negative energy in a band ≤ 1.5×10⁻²³ m | static, but unstable [D-13] | 55.2 (density vs Casimir at 0.2 µm); band 12.8 below an atom | 1 |
| same | 1 kg (b₀ = 0.1 m) | 2.7×10²⁶ kg | 4.8×10⁴⁴ J/m³ | none | band ≤ 6.9×10⁻²² m | unstable | 45.2; band 11.2 below an atom | 1 |
| same | human (b₀ = 1 m; 1.5×10⁷ m with MM's tidal criterion) | 2.7×10²⁷ kg (4.0×10³⁴ kg) | 4.8×10⁴² (2.1×10²⁸) J/m³ | none | band ≤ 1.5×10⁻²¹ (3.7×10⁻¹⁹) m | unstable | 43.2 (28.9); band 10.8 (8.4) below an atom | 1 |
| Visser thin shell, flat limit | qubit / 1 kg / human (a = 1 µm / 0.1 m / 1 m) | \|m_s\| = 2.7×10²¹ / 2.7×10²⁶ / 2.7×10²⁷ kg | \|σ\| = 1.9×10⁴⁹ / 1.9×10⁴⁴ / 1.9×10⁴³ J/m² | none | as above | stable only for β₀² < 0 at a₀ > 3M [D-14] | 56.6 / 51.6 / 50.6 (areal energy vs Casimir) | 1 |
| GJW / MSY / Maldacena–Qi / FGM 2018 (AdS or 2D; two-sided) | qubit | not realisable in our universe; the analogue is a sparse-SYK simulator | – | – | – | open for less than a Planck time (GJW, [D-03]) | gravitational: no route (AdS); simulator: 2.3 to 3.7 (gates, error rate) | 1 gravitational; 4 simulator |
| same | 1 kg / human | – | – | – | – | – | about 26 / 28 more qubits than demonstrated; capped by the classical channel | 1 |
| MMP, Standard-Model fields (4D; long, not a shortcut) | qubit (a sub-MeV charged fermion) | 2.7×10⁸ kg per mouth (r_e ≤ 2×10⁻¹⁹ m) | 4.8×10²⁵ J for the pair; \|E_min\| = 4.5 MeV to 13 GeV | 4×10¹⁴ hypercharge flux units; B_h = 1.8×10³⁷ T | T < 0.3 to 17 mK; ℓ = 2 cm to 1.1 m | eternal if stable (open, [D-C5], [F-01]) | magnetic charge: none observed (unbounded); field for pair creation 34.2; energy 4.9 (vs one year of world energy) | 1 |
| same | 1 kg | – | needs 25.6 more orders of \|E_min\| | – | – | – | 25.6 (energy), 17.7 (size) | 1 |
| MMP widened / MM 2020 (RS II + dark U(1), speculative) | human | 2.0×10³⁴ kg = 1.0×10⁴ M_☉ per mouth | 3.6×10⁵¹ J (6×10³⁰ yr of world energy); E_bin ≈ −5×10⁹ kg [Q-02] | B_h = 2.3×10¹¹ T; or N ≥ 2×10⁵⁴ species in pure 4D | dark sector < 1.2×10⁻²² K; CMB < about 3×10⁻²¹ K seen boosted | traverse 0.16 s proper, 9.4×10³ yr outside [Q-06] | 30.8 (energy); 22 to 24 (species vs 10³² cap); 10 to 11.5 (temperature vs 38 pK); field 8.3 | 1 (needs an unobserved sector) |
| MM pure 4D | 1 kg | – | – | N ≥ 2.3×10⁴⁴ | – | – | 12.4 vs 10³² cap | 1 |
| FGM 2019 (4D flat; transient; t_min = d + logs) | qubit only (perturbative) | M ≤ 4.5×10²² kg unless CMB-isolated | – | cosmic string Gμ/c² = 2(GM/c²d)² | Hartle–Hawking bath at T_H | transient; merger time ∼ d^{3/2} | no cosmic string observed (unbounded); payload is perturbative | 1 |
| EDM (BKR / KZ) | none | throat 1.2×10⁻³³ to 8×10⁻³³ m | – | fermion q/μ < 1 needs m ≳ 10¹⁸ GeV | – | collapses to black holes [D-11] | 15.6 to 21.9 (fermion charge-to-mass) | 1, likely eliminated |

### B. Scaling laws (what shrinks the gap)
- Ellis: |ρ| ∝ b₀⁻², |Ω| ∝ b₀, Ford–Roman band ∝ b₀^{1/3}. Widening lowers the density gap by 2 orders per decade but raises the exotic mass by 1 order per decade. Equality with Casimir density needs b₀ = 4×10²¹ m, where the band is still about 10⁻¹⁴ m. No b₀ closes both gaps.
- Thin shell: σ ∝ a⁻¹, so a factor of 10 in radius buys 1 order. 50 orders are needed.
- MMP: |E_min| = N²g²ħc/(256π r_e). It falls as 1/r_e, so widening at fixed fields reduces payload capacity. Only the species count N (with g²N ≤ 1, giving |E_min| ∝ N) raises it, at 1 order per order of N. Mouth mass and formation energy grow ∝ r_e. The pair-creation exponent is ∝ M²/B ∝ r_e²/B. The required temperature falls as 1/ℓ ∝ N q/r_e³.
- Quantum simulator: gates ∝ kN²n_T, and the allowed error per gate ∝ 1/gates. Each doubling of N costs about 0.6 orders.

### C. TRL table (key component; NASA TRL 1–9)
| Option | Key component | TRL | Evidence |
|---|---|---|---|
| Ellis / MT | macroscopic NEC-violating stress ≥ 10²⁸ J/m³ | 1 | negative energy exists only as Casimir or squeezed vacuum at 0.27 J/m³ scales [D-19] [D-20]; QI bounds forbid the band [K-08] |
| Thin shell | negative surface energy ≥ 10⁴³ J/m² | 1 | same |
| GJW-family, gravitational | boundary-coupled AdS black hole | 1 | theory only, not our spacetime [D-01] [D-04] |
| GJW-family, simulator | holographic-teleportation circuit | 4 | 3 hardware platforms, N = 6 to 9 qubits, contested gravitational reading [D-16] [D-17] [D-C1] [Q-39] |
| MMP (SM) | extremal magnetic black hole pair joined by a throat | 1 | no magnetic charge observed [D-25]; formation only via a topology-change instanton (Garfinkle–Strominger) |
| MMP (SM) | mK cryogenics around the mouths | 9 (as a technology) | dilution refrigerators are routine (my general knowledge, unsourced); not the binding item |
| MM 2020 | RS II + dark U(1) sector | 1 (speculative) | authors' own "science fiction" [D-08] |
| FGM 2019 | cosmic-string strut + charged black-hole pair | 1 | no cosmic string observed |
| EDM | classical Dirac-sourced throat | 1, likely eliminated | [D-10] to [D-12] |
| Natural-wormhole searches | lensing, S2, EHT, echoes | instruments 7 to 9 | null results [D-22] to [D-24] |

### D. Test sensitivity table
| Test | What it tests | Required | Achieved | Gap (orders) | Date |
|---|---|---|---|---|---|
| Sycamore-type teleportation | holographic-dual signatures (size winding, ANEC-sign asymmetry), not spacetime | chaotic sparse SYK N ≳ 20 to 100; error/gate ≲ 10⁻⁵ to 10⁻⁶ | N = 7 to 8; ≈ 4×10⁻³ effective | 2.3 to 3.7 | N ≈ 20 plausible within about 5 to 10 yr with error mitigation or correction (my estimate) |
| Ellis / negative-mass microlensing | classical Ellis throats 100 to 10⁷ km; abundance | detect ∼4% "gutters" [Q-42] | null; SDSS n < 10⁻⁴ h³ Mpc⁻³ (10 to 10⁴ pc) [Q-40] | n/a (blind to MMP/MM) | ongoing surveys |
| S2 orbit perturbation | mass behind Sgr A* if it is a mouth | 10⁻⁶ m/s² | 4×10⁻⁴ (projected 2×10⁻⁵) | 2.6 (1.3) | ∼2040 for the projection [Q-43] |
| EHT shadow | horizon versus throat; charge | 0.8 µas for a 10⁴ M_☉ mouth at 1 kpc | 21 µas | 1.4 to 2.4 | needs space VLBI |
| GW echoes | reflecting throat | delay ∼10³ to 10⁴ yr (MM) | ms to s searches, runs of ∼2 yr | 3.7 | not reachable |
| Magnetic-charge searches | existence of the mouths' magnetic charge | any macroscopic magnetic charge | MoEDAL < 75 GeV (1 to 3 g_D); Parker-type flux bounds [Bai et al.] | SM-MMP mouth 33 orders above MoEDAL | ongoing |
| Lab negative energy / QEI | whether sub-vacuum energy obeys QEIs | time-resolved local energy density in J/m³ | none in J/m³ (squeezing only as noise, 15 dB) [D-20]; Maclay–Davis contested [D-C6] | undefined (no measurement exists) | – |

### E. Next milestone per option
- Ellis / MT and thin shell (kill or raise): a direct, time-resolved measurement of a sub-vacuum local energy density in J/m³ compared with the Fewster–Eveson bound [K-09]. A confirmed QEI violation would be the only route to reopening these. Theory: apply the Ford–Roman band argument to Visser shells, expecting confirmation.
- GJW family (simulator): chaotic sparse-SYK teleportation at N ≥ 20 with an ANEC-sign asymmetry that grows with N as the holographic prediction says. This would move TRL 4 to 5 as a simulator, never as a channel.
- MMP (SM): complete the linear stability analysis in every sector (Sadhukhan covers one [F-01]), and compute the Garfinkle–Strominger rate including the fermion Casimir term. Observationally, any detection of a magnetically charged object (primordial magnetic black holes, the Bai et al. bounds) would move the key component from TRL 1 to 2.
- MM 2020: short-range gravity tests below the R₅ = 50 µm that MM's worked example uses [Q-02], and dark-photon searches. A tighter bound worsens MM's parameters, so this is a kill test for the worked example.
- FGM 2019: a non-perturbative, back-reacted solution showing whether traversability survives beyond "exponentially fragile". Nothing is observable now.
- EDM: Weinbaum-type search extended to the Maxwell-coupled asymmetric branch, the kill test for what remains of D-C2.

## Calculations
- `runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-engineer_cost_table.py` (log `.py.log`) computes:
  - Casimir anchors (|u| = 0.271 J/m³, P = 0.813 Pa, |E/A| = 5.42×10⁻⁸ J/m² at 0.2 µm);
  - Ellis density, exotic mass and Ford–Roman band gaps (43.2 to 55.2 orders; band 10.8 to 12.8 orders below atomic; b₀ for equality 4.2×10²¹ m and 2.5×10⁴² m);
  - thin-shell σ gaps (50.6 to 56.6 orders);
  - MMP-SM parameters (q = 4.1×10¹⁴, ℓ = 0.021 to 1.14 m, |E_min| = 7.2×10⁻¹³ to 5.2×10⁻⁸ J, T < 0.3 to 86 mK across g = 0.06 to 0.3 and N = 1 to 54, M = 2.66×10⁸ kg, B_h = 1.76×10³⁷ T);
  - formation energy 4.78×10²⁵ J = 8.07×10⁴ yr of world energy;
  - pair-creation exponents (6.9×10⁶⁶ at 1200 T; equal to S_BH = 4.68×10³² at B_h, an identity check);
  - MM species requirement (2.3×10⁴⁴ to 3.4×10⁵⁵);
  - MM energy 3.63×10⁵¹ J and the CMB boost requirement 2.9×10⁻²¹ K, cosmic cooling time 8.5×10¹¹ yr, de Sitter floor 2.2×10⁻³⁰ K;
  - FGM strut Gμ/c² = 2×10⁻⁶ at d = 10³ r_g and the 4.5×10²² kg CMB-temperature mass;
  - EDM q/μ gaps (15.6 to 21.9 orders);
  - simulator gate and error scaling (2.3 to 3.7 orders);
  - test gaps (S2 2.6 and 1.3; EHT 1.4 to 2.4; echoes 3.7; RN/Schwarzschild shadow ratio 0.770).
- A bug in the first run (a missing factor of M in the pair-creation exponent) was caught by the B = B_h → S_BH identity and fixed before any number was used.

## Candidate answers (at least 3; the null and a reframe count)
- [ENGINEER-A] Null for practice. No wormhole that holds a payload can be built or widened within about 100 years, for any payload size.
  - **Smallest gap.** The cheapest real-universe construction is the Standard-Model MMP pair, which carries a qubit only.
  - **Requirements and gaps for that construction.**
    - It needs magnetic charge, and none has ever been observed.
    - Pair creation needs a field 34 orders above the record.
    - Its rest energy is 4.9 orders above a year of world energy.
  - **Larger payloads.** 1 kg needs at least 25 orders more; a human needs at least 22 orders, and in any case new physics.
  - status: surviving | why: every gravitational row of table A has a binding gap of at least 4.9 orders plus an unbounded item, and the classical rows are 38 to 57 orders out | test: any detection of macroscopic magnetic charge, or a measured QEI violation, would reopen it | confidence: high
- [ENGINEER-B] In principle, the cheapest gravitational traversable wormhole in our universe is the Standard-Model MMP pair.
  - **Scale.** Mouths are 2.7×10⁸ kg extremal magnetic black holes (r_e ≲ 2×10⁻¹⁹ m) with about 4×10¹⁴ hypercharge flux units, about 5×10²⁵ J in total.
  - **Environment.** It needs millikelvin surroundings.
  - **Capacity.** It passes qubit-scale signals up to MeV to 10 GeV of energy. It is a long wormhole, not a shortcut.
  - **Widening.** Widening it lowers capacity (|E_min| ∝ 1/r_e).
  - status: strained | why: consistent with established physics plus the MMP calculation, but the formation route is a topology-change instanton, stability is open [D-C5], and the N_eff² and coupling reading are my assumptions | test: full MMP stability analysis; a Garfinkle–Strominger rate with fermions; a primordial magnetic black hole search | confidence: medium
- [ENGINEER-C] A human-scale wormhole (MM 2020) is possible in principle only with labelled speculative physics.
  - **Requirements.** It needs an RS II plus dark U(1) sector, or about 10⁵⁴ species in pure 4D (22 orders over the 10³² cap), and 10⁴ M_☉ magnetically charged mouths (3.6×10⁵¹ J).
  - **Environment.** Ambient photons must be below about 3×10⁻²¹ K and the dark sector below 1.2×10⁻²² K. Cosmic expansion alone reaches these after about 10¹² yr.
  - **In practice.** It is eliminated in practice and is not a shortcut.
  - status: strained | why: no formation mechanism (the authors say so); the energy gap is 31 orders; the pair-creation exponent is about 10⁹² | test: short-range gravity tests below 50 µm; dark-photon searches | confidence: medium
- [ENGINEER-D] Classical Morris–Thorne and thin-shell wormholes are eliminated on engineering grounds alone, independent of the shortcut question.
  - **Negative energy.** The required density or areal energy exceeds the best laboratory negative energy (Casimir) by 38 to 57 orders.
  - **Band thickness.** The Ford–Roman band is thinner than an atom for any throat smaller than 3×10³² m.
  - **Scaling.** Widening and narrowing move the two gaps in opposite directions.
  - status: eliminated | why: tables A and B | test: a measured QEI-violating energy density would be needed to revive it | confidence: high
- [ENGINEER-E] Reframe. The only "wormhole" technology plausible within 100 years is the holographic-teleportation simulator.
  - **Status.** It is at TRL 4, and reaching the regime where its gravity dual is controlled is 2 to 4 orders away (gates, error rate) at N = 20 to 100.
  - **Limits.** It tests features of the dual model. It cannot carry a payload or beat its classical channel: 1 kg would need about 10²⁶ teleported degrees of freedom.
  - status: surviving | why: the gap is small and closable by error correction, unlike every gravitational row | test: chaotic sparse SYK at N ≥ 20 with N-scaling of the asymmetry | confidence: medium-high
- [ENGINEER-F] The Einstein–Dirac–Maxwell "no exotic matter" wormholes are not a buildable option.
  - **Fermion.** In the explored family the fermion needs q/μ < 1, so a mass of at least about 10¹⁸ GeV. That is 15.6 to 21.9 orders beyond known charged fermions.
  - **Throat.** It is Planck-scale.
  - **Dynamics.** The solutions collapse to black holes.
  - status: eliminated | why: findings 10, [D-11], [D-12] | test: Weinbaum-type analysis of the asymmetric Maxwell branch | confidence: medium-high
- [ENGINEER-G] FGM 2019 is a transient, perturbative signal channel in 4D, not a shortcut.
  - **Requirements.** A cosmic-string strut (Gμ/c² = 2(r_g/d)²), and holes either lighter than 4.5×10²² kg or CMB-isolated.
  - **Status.** It carries no payload beyond perturbative quanta, and there is no route to building it.
  - status: strained | why: no cosmic string is known; it is exponentially fragile | test: a non-perturbative solution | confidence: medium-low

## What would change my mind
- A detected macroscopic magnetic charge or primordial magnetic black hole would lift MMP's key component from TRL 1 to 2 to 3, though not the payload gap.
- A laboratory measurement of a QEI-violating negative energy density would reopen the classical rows.
- A calculation showing MMP's Casimir term scales faster than N_eff², or that g²N ≤ 1 is not needed, would shrink my MM species gap. MM's own figure (10⁵² against my 3×10⁵⁵) already differs by 3.5 orders.
- A published Garfinkle–Strominger rate with a prefactor or e^{S} enhancement large enough to compete with exponents of about 10⁶⁶ to 10⁹² at laboratory fields; I consider this implausible.

## Assumptions I relied on
- **Couplings.** The hypercharge unit coupling g ≈ 0.06 (g′/6) is my reading of MMP's normalisation; g = 0.3 is shown for sensitivity.
- **Casimir scaling.** MMP's Casimir term scales by N_eff, giving |E_min| ∝ N_eff². This is my extension, not in the paper; for N = 1 I use the paper's formulas exactly.
- **Payload criterion.** The payload rest energy must stay below |E_min| (MM's |E_bin| > ship-mass criterion [Q-03]).
- **Field and extremal relations.** Mouth fields use extremal RN in SI electromagnetism (as RE-15). The pair-creation rate is approximated by the Schwinger form, not Garfinkle–Strominger's own formula.
- **Tolerances and cosmology.**
  - The CMB tolerance is 1 eV per photon, my criterion.
  - Standard ΛCDM values: H₀ = 67.4 km/s/Mpc, Ω_Λ = 0.685.
  - The top-quark mass is 172.6 GeV.
  - EHT resolution is taken as λ/D at 1.3 mm over an Earth-diameter baseline.
- **Simulator model.** The gate model is about 2kN²n_T with k = 4 and n_T = 10, my estimate.
- **Search-summary anchors.** The 1200 T, 38 pK and 592 EJ values rest on search summaries, labelled as such. The 45.5 T value rests on the paper's title only.
