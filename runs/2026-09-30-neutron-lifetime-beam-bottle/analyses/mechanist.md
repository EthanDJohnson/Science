# Analysis: mechanist (Aristotle: efficient causes and mechanisms)
status: final

Units: SI (s, s⁻¹, T, m/s); particle energies in neV/eV/MeV with ħ = c = 1 where noted.

## Method applied
For each candidate cause of the proton-beam/bottle gap I write the causal chain (producer → what it acts on → what sustains it → what ends it), classify it by phenomenon type and governing theory, evidence each link from the dossier or mark it assumed, and size it against the gap and against the published error budgets (calc scripts under calc/lens-mechanist_*).

## Findings
1. **BL1 proton storage time.** In BL1 decay protons are stored in the Penning trap for a cycle of "order 10 ms"; "The precision lifetime data were taken with trapping times of 5 ms and 10 ms" [new: Nico et al. 2005, arXiv nucl-ex/0411041, full-text, "The precision lifetime data were taken with tr apping times of 5 ms and 10 ms."]. Protons are born uniformly during the cycle, so the mean storage time is about half the cycle (≈2.5 ms and ≈5 ms). Any proton loss that grows with storage time (charge exchange or scattering on residual gas) therefore scales in a known way with the trapping period, and the two data sets act as a built-in lever arm (see F4). The vacuum is UHV with ion pumps, but the solenoid bore "is the most notable exception" to routine bake-out [new: same source, full-text, "The solenoid bore is the most notable exception to that procedu re."]. I found no printed pressure value in the grep.
2. **Size of the gap this lens uses.** Proton beam (BL1 [D-20] with the unverified Sussex–ILL lead [D-22]) 887.97 ± 2.04 s against UCNτ 877.82 s [D-27]: Δτ = 10.15 s, a fraction of 1.143 %, a missing rate of 1.30×10⁻⁵ s⁻¹ (time constant 7.7×10⁴ s ≈ 0.89 d). BL1 alone gives 9.88 s (1.11 %). Against Gravitrap [D-28] the gap is only 6.5 s (0.73 %) [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-mechanist_required_sizes.py]. The statistician's combination is the reference; these are for sizing.
3. **What BL1's formula makes a mechanism act on.** Nico 2005 eq. 6: τn = L Ṅ_α+t ε_p/(Ṅ_p ε_0 v_0) [new: Nico et al. 2005, arXiv nucl-ex/0411041, full-text, "τn = L ˙Np ˙Nα +t ǫo ǫp vo . (6)" (PDF extraction garbles the fraction)]. The measured τ scales as ε_p/ε_0. A proton-side mechanism must remove 1.14 % of protons *in proportion to trap length*, because the slope-versus-length analysis cancels any length-independent end loss [D-08]. A fluence-side mechanism must make the true ⁶Li monitor efficiency 1.16 % higher than assumed. The same source says that decay-in-flight and residual-gas changes to the beam between trap and monitor are "less than 0.001 %" [new: same source, full-text, "changes in the neutron beam due to decay-in-ﬂig ht and residual gas interaction are less than 0.001 %"]. So the neutron side of the chain can only fail through the absolute monitor efficiency, not through beam attenuation.
4. **Required size against BL1's own budget.** The gap is 20× the 2013 fluence uncertainty (0.5 s), 6× the carried-over non-fluence systematics (1.7 s), 12.7× the trap-nonlinearity uncertainty, 10× the beam-halo uncertainty, 25× the backscatter uncertainty, and 1.9× the full size of the trap-nonlinearity and ⁶Li-absorption corrections [D-21][calc: lens-mechanist_required_sizes.py]. The 2013 Alpha-Gamma recalibration moved τ by +0.16 %, away from the bottles [D-07]. A single mis-estimated item must therefore be wrong by 6–25× its quoted error, or a correction of about 5 s must have the wrong sign or be doubled. That is not impossible (the nonlinearity and absorption corrections are each about half the gap), but it is a large error.
5. **Residual-gas proton loss: needed density and a built-in test.** Loss = n σ v t_store. With decay protons at about 300 eV (v ≈ 2.4×10⁵ m/s), a mean storage time of 5 ms (10 ms cycle) and an ASSUMED H⁺ + H₂ charge-transfer cross section of 10⁻²⁰ to 10⁻¹⁹ m², a 1.14 % loss needs n_H₂ ≈ 10¹⁴–10¹⁵ m⁻³, which is 4×10⁻⁷ to 4×10⁻⁶ Pa (4×10⁻⁹ to 4×10⁻⁸ mbar) at 300 K. That is above good UHV but not absurd for an unbaked cold bore (F1). The loss scales with storage time, so BL1's 10 ms and 5 ms data sets would differ by about **5.1 s** [calc: lens-mechanist_required_sizes.py]. Whether BL1 published that split is not established here. Caylor's ~0.3 % H₂ estimate [D-17] would give only 2.7 s, 26 % of the gap.
6. **Unresolved link in the charge-exchange chain (dossier gap).** p + H₂ → H + H₂⁺ turns the proton into a neutral atom, but it leaves a positive ion born near thermal energy inside the same well. On the Penning-trap physics this ion should be trapped and then ejected and accelerated onto the detector like a proton. The charge exchange then removes a count only if the molecular ion is lost (not confined, dissociated, or below the detector threshold or outside the timing gate). The dossier has no evidence for that step (Serebrov [D-72] asserts the loss; Caylor [D-17] measured that the process occurs). This is the weakest link of the most-cited proton-beam systematic, and it is ASSUMED in every version I can reconstruct.
7. **Bottle-side required loss.** An extra loss of 1.30×10⁻⁵ s⁻¹ needs one of the following [calc: lens-mechanist_required_sizes.py]:
   - residual-gas upscattering, with order-of-magnitude ASSUMED cross sections: N₂ ≈ 6×10⁻⁴ mbar, H₂ ≈ 2×10⁻⁵ mbar or He ≈ 5×10⁻³ mbar at 300 K. All are orders of magnitude above the working pressure of storage experiments (itself an ASSUMPTION; the dossier gives no bottle vacuum values), so gas is eliminated as the common cause;
   - in a magnetic trap, a spin-flip probability of 1.3×10⁻⁵ per second (1.3 % over a 1000 s hold);
   - in a material bottle, an extra loss of 2.6×10⁻⁷ to 2.6×10⁻⁶ per wall collision at 5–50 collisions per second.

   These are physically distinct agents (depolarisation or marginal trapping against wall absorption and upscattering). A "bottle systematic" that shortens both classes by the same ~1 % would have to be two unrelated errors of equal size and sign, or one common agent that does not depend on walls or fields. No mundane agent of that kind (residual gas) reaches the needed rate. In fact material bottles read higher, not lower (Gravitrap 881.5 s; material 880.0 against magnetic 877.8 s [D-32][D-73]), the opposite of an uncorrected extra loss in walled traps.
8. **Bottle systematic cannot reach J-PARC.** J-PARC stores no UCN [D-09], so no bottle-loss mechanism can move J-PARC's 877.2 s [D-23]. A bottle-systematic explanation therefore needs a second, independent error in J-PARC of −10.8 s (−1.23 % of the β signal). That error has a plausible agent (see F9), but the candidate then rests on two independent mechanisms.
9. **J-PARC's excess background: the right sign and more than enough size.** The observed background is 4.9–5.4 % of S_β at 100 kPa against 1.2–1.3 % predicted by MC, and 3.1–3.3 % against 0.65–0.67 % at 50 kPa [D-25]. That is an excess of about 3.6–4.2 % and 2.4–2.6 % of the signal. If even a third of the excess at 100 kPa were γ-induced events counted as β decays and not subtracted, the β rate would be overestimated and τ underestimated by the ~1.2 % needed [calc: lens-mechanist_required_sizes.py]. Whether the subtraction uses the measured or the MC background is not established in the dossier. The mechanism is a measurement artefact (detector background), and it acts only on J-PARC.
10. **J-PARC's internal spread follows gas pressure in the direction a gas-borne bias would give.** From the four Table II conditions [D-24]:
    - the 100 kPa pair averages 869.8 ± 2.6 s (stat) and the 50 kPa pair 883.3 ± 2.3 s (stat), a difference of 13.6 ± 3.5 s, 3.9σ on statistics alone. With an approximate systematic added it is 12.6 ± 5.7 s, 2.2σ;
    - a bias proportional to pressure, extrapolated linearly to 0 kPa, would give 897 ± 5 s (stat), or 895 ± 9 s (approximate sys). That is beam-like or above;
    - but the trend rests on the single 50 kPa/new-SFC point: 50 kPa/old-SFC (868.2 ± 7.7 s) does not follow it, and old against new SFC splits by a similar 10 s (870.4 against 880.4 s). Pressure and SFC are confounded, and I do not claim the extrapolation.

    Mechanistically, J-PARC's agreement with the bottles (0.16σ from UCNτ; 2.2σ from the proton beam with symmetrised errors) [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-mechanist_nnprime_jparc.py] rests on a detector whose dominant unexplained background scales with gas. The only J-PARC discrimination that holds up is "J-PARC does not independently confirm 888 s". This agrees with Desai's qualitative critique [D-71].
11. **n → n′ (Berezhiani strong-field model, SPECULATIVE): fine-tuned and excluded.** I ran the toolkit's solenoid model (0.6 m, 4.6 T, cold-beam velocity average with ASSUMED spectrum) [calc: lens-mechanist_nnprime_jparc.py]:
    - **Sign and window.** The beam is lengthened only when Δm sits just above |µn|B_centre. At Δm = 280 neV (B_res = 4.64 T) a +1.143 % shift needs θ0 = 1.66×10⁻³ (P_trap = 1.13×10⁻², τ_nn′ ≈ 1.4×10⁻⁶ s). At 300 neV the shift is < 0.1 s even for θ0 = 10⁻³. At 200–260 neV the beam path crosses resonance before the monitor, P_det > P_trap, and the beam is *shortened* (for example −9 s at 260 neV, θ0 = 10⁻⁴). The working window is ≲ 20–40 neV wide in Δm.
    - **SNS regeneration.** With comparable conversion per passage (ASSUMED), regeneration ~P² ≈ 1.3×10⁻⁴ against the limit 2.5×10⁻⁸ [D-62], an excess of 5×10³. The limit caps P at 1.6×10⁻⁴ per passage, which caps the beam shift at about 0.14 s, 1.4 % of the gap.
    - **Other classes in the same model.** J-PARC (0 T or 0.6 T): the time-averaged mixing 5.5×10⁻⁶ has no loss channel in a beam, so the shift is < 0.01 s and J-PARC reads τ_β. Material bottles: a wall-independent loss of 5.5×10⁻⁶ per bounce (rate 2.8×10⁻⁵ to 2.8×10⁻⁴ s⁻¹ at 5–50 bounces per second) scales with collision frequency exactly like wall loss, so size or energy extrapolation removes it. But it is a floor on the per-bounce loss of every bottle, a further test not carried in the dossier. Magnetic traps (fields below 4.64 T): no crossing and no projecting walls, so no loss.
    - The model predicts beam 888, J-PARC 878, magnetic 878 and material 878 (after extrapolation), which matches the data pattern. But it is excluded by regeneration and needs Δm tuned to the trap field. Tan's inverse variant (bottles shortened by wall-collision n → n′, beams true [D-96]) predicts wall-free UCNτ = beam value and J-PARC = beam value, both contradicted [D-27][D-23].
12. **UCNτ's own rates for the two magnetic-trap loss agents.** UCNτ assigns "a depolariza- tion rate of λdp = 0.0+1.0 −0.0× 10−7 s−1" [new: Gonzalez et al. 2021, arXiv:2106.10375, full-text, "we assign a depolariza- tion rate of λdp = 0.0+1.0 −0.0× 10−7 s−1"]. Its residual-gas correction is +0.11 ± 0.06 s, computed "run by run using the measured absolute pressure and periodic residual gas analysis of the trap" [new: same source, full-text, "Residual gas scattering +0.11 ±0.06"; "The residual gas up-scattering rate was computed run by ru[n] using the measured absolute pressure and periodic residual gas analysis of the trap"]. A 1.30×10⁻⁵ s⁻¹ loss is 130× the depolarisation bound and about 90× the gas correction (+0.11 s ↔ ≈1.4×10⁻⁷ s⁻¹).
    - A constant-rate loss is exactly degenerate with β decay in a single-exponential fit, so only these absolute rate estimates guard against it.
    - A time-dependent loss (uncleaned or heated UCN, +0.11 s and +0.08 s in the same table) would bend the storage curve and change with dagger height [D-10]. It cannot hide a 10 s shift.
13. **Caylor 2025 closes part of F6's open link.** The NIST group "determine[s] the efficiency with which the molecular hydrogen ions in the trap are detected" [new: Caylor et al. 2025, arXiv:2506.01682, abstract, "we determine the efficiency with which the molecular hydrogen ions in the trap are detected"]. They also report secondary reactions making H₃⁺ and HeH⁺ [new: WebSearch, search-summary, SUMMARY "The molecular ion H2+ produced by charge exchange in H2 undergoes secondary molecular reactions, producing the molecular ion H3+ and the ion HeH+"].
    - The count lost per charge exchange is therefore (1 − ε_ion), not 1. The needed H₂ density scales up by 1/(1 − ε_ion) over F5's 10¹⁴–10¹⁵ m⁻³, so the more efficiently the ions are detected, the less viable the mechanism.
    - Caylor's own verdict is "unlikely to have been significantly affected" [D-17].
14. **SM arbitration, re-derived with consistent pairing (GS2023, Vud 0.97361(32)) [U-01].** τ_β = 878.50 ± 0.88 s (PERKEO III), 879.65 ± 1.61 s (PDG 2024 λ) and 889.58 ± 3.20 s (aSPECT 2024) [calc: lens-mechanist_required_sizes.py]. Against UCNτ this gives Br_X = 0.077 ± 0.106 % (95 % upper 0.25 %) for PERKEO III and 0.21 ± 0.19 % (upper 0.51 %) for PDG λ, against the 1.14 % needed. Only aSPECT's λ gives 1.32 ± 0.36 %. The proton beam sits 4.3σ above τ_β(PERKEO III) and 3.2σ above τ_β(PDG). Any mechanism in which the proton beam is right about τ_β (dark decay, any proton-less branch, Veselský's X⁺ [D-95]) therefore fails through the λ link unless the a-coefficient route is right [D-74].

## Lens-specific outputs

### O1. Causal chains (producer → acts on → sustained by → ended by), with evidence per link

**M1. Proton-beam fluence-monitor efficiency error (measurement artefact; nuclear-reaction cross sections plus neutron optics)**
1. The ⁶Li deposit's areal density × σ(⁶Li(n,t)) sets ε_0 [D-21][F3]. Evidenced.
2. The assumed ε_0 is 1.16 % below the true value [F3]. ASSUMED, and this is the weakest link: it is 20× the 2013 Alpha-Gamma uncertainty (0.5 s) and has the opposite sign to the 2013 recalibration (+1.4 s) [D-07][D-20][F4].
3. The neutron density is overestimated, and τ scales as 1/ε_0 [F3]. Evidenced (the formula).
4. It is sustained because the same deposit and calibration are used for every run. It ends when a new absolute flux calibration is made (BL3's upgraded Alpha-Gamma) [D-101].

**M2. Proton loss scaling with trap length (measurement artefact; atomic collisions and Penning-trap dynamics)**
1. Decay protons (≤ 751 eV) are stored for about 2.5–5 ms [F1].
2. Candidate agents:
   - (a) charge exchange with residual H₂: occurs [D-17][F13];
   - (b) halo protons born outside the radial acceptance [D-21];
   - (c) a mis-sized nonlinearity correction [D-08].
3. The loss must be proportional to the number of stored protons, hence to length, because length-independent end losses cancel in the slope [D-08][F3]. Evidenced as a constraint.
4. The loss must be 1.14 % [F2]. ASSUMED, and this is the weakest link:
   - (a) needs n_H₂ ≈ 10¹⁴–10¹⁵ m⁻³/(1 − ε_ion) [F5][F13], against Caylor's ~0.3 % estimate [D-17];
   - (b) needs 10× its budget;
   - (c) needs 2× the correction itself [F4].
5. It is sustained by the unbaked cold bore [F1]. It ends at a lower pressure or with a shorter trapping time: the 5 ms against 10 ms prediction is Δτ ≈ 5.1 s [F5].

**M3. Proton detection efficiency (backscatter, dead layer) (material property; ion–solid stopping)**
1. Protons accelerated to 25–32 keV hit a gold-coated Si detector [D-21]. Evidenced.
2. A fraction backscatters or stops in the dead layer below threshold. Evidenced as a budgeted effect (0.4 s and 0.5 s) [D-21].
3. The fraction must be 1.14 %. ASSUMED, and this is the weakest link: 20–25× the budget [F4].
4. It is sustained by the detector configuration. It ends when a different detector technology is used (BL2/BL3) [D-100].

**M4. Unrecognised time-independent UCN loss in bottles (measurement artefact; neutron optics and UCN physics)**
1. Agents:
   - (a) depolarisation in magnetic traps;
   - (b) residual-gas upscattering in all traps;
   - (c) an unmodelled wall-loss component in material bottles.
2. A rate of 1.30×10⁻⁵ s⁻¹ must be added and must stay constant in time [F7][F12]. ASSUMED, and this is the weakest link:
   - (a) is 130× UCNτ's depolarisation bound;
   - (b) is about 90× UCNτ's gas correction and needs orders of magnitude more pressure;
   - (c) cannot touch UCNτ;
   - one common agent across both trap classes is not available [F7].
3. It is exactly degenerate with β decay in fit [F12]. Evidenced (logic).
4. It must also move J-PARC, which it cannot [F8]. This needs a second mechanism (M5).

**M5. J-PARC gas-borne γ background not fully subtracted (measurement artefact; detector response)**
1. Gas-scattered neutrons are captured and make γ rays; γ-induced electron-like events enter S_β [D-25]. Evidenced.
2. The background is 4× the MC prediction and scales with pressure [D-25][F9]. Evidenced.
3. Residual unsubtracted events of about 1.2 % of S_β would give τ −10.8 s [F9]. ASSUMED, and this is the weakest link: the subtraction procedure is not in the dossier.
4. There is a pressure trend of 13.6 ± 3.5 s (stat) between 50 and 100 kPa, confounded with the SFC [F10]. Suggestive.
5. It ends with LiNA (solenoid field, background ×1/50) and gas-pressure scans [D-102].

**M6. Invisible dark decay n → χφ / χχχ (new particle or interaction, SPECULATIVE; Fornal–Grinstein EFT)**
1. A new operator mixes n with a dark fermion χ in the window 937.900 < m_χ + m_φ < 939.565 MeV [D-84]. Model.
2. It acts on free neutrons everywhere with Br_X ≈ 1.14 % [F2].
3. It is sustained by being a decay, with no environmental dependence.
4. Protons are missing from 1.14 % of decays, so the proton beam reads long. The bottles see total disappearance and read true. J-PARC counts electrons only, so it reads long (≈ 888 s) [D-06]. Evidenced (logic).
5. Weakest link: λ. τ_β(PERKEO III) = 878.50 ± 0.88 s leaves Br_X = 0.08 ± 0.11 % [F14]. J-PARC is 2.2σ low of the prediction [F10]. The neutron-star bound applies unless repulsive dark forces are added [D-88].

**M7. Strong-field n → n′ (Berezhiani) (new interaction, mirror sector, SPECULATIVE; two-level mixing with Landau–Zener passage)**
1. Near-degenerate n′ with Δm ≈ 280 neV is brought to resonance by the Zeeman shift in the 4.6 T trap [D-05][D-89].
2. P_trap ≈ 1.1 % needs θ0 ≈ 1.7×10⁻³ [F11].
3. It is sustained by the solenoid field during the transit through the trap.
4. It ends when the neutron leaves the solenoid. The monitor field is weak, so P_det ≈ 5×10⁻⁶ [F11].
5. Weakest link: SNS regeneration, 5×10³ above the limit [F11][D-62], plus the Δm tuning.

**M8. SM field or environment dependence of the decay rate (classical field and electroweak theory)**
1. Zeeman energy / Q ≈ 4×10⁻¹³ [D-05]. The link from "strong field" to "1 % rate change" is broken by 10 orders of magnitude, so this mechanism is eliminated.

### O2. Classification and governing theory
| Mechanism | Class | Governing theory | Acts on classes |
|---|---|---|---|
| M1 monitor efficiency | measurement artefact (normalization) | nuclear cross sections, 1/v law | proton beam only |
| M2 proton loss ∝ length | measurement artefact (loss channel) | atomic collision physics, Penning-trap dynamics | proton beam only |
| M3 proton detection | measurement artefact (detector) / material property | ion stopping in solids | proton beam only |
| M4 bottle loss | measurement artefact (loss channel) | UCN optics, spin dynamics, gas scattering | bottles only (not J-PARC) |
| M5 J-PARC background | measurement artefact (detector background) | γ/electron transport (Geant4) | J-PARC only |
| M6 dark decay | new particle or interaction (SPECULATIVE) | Fornal–Grinstein EFT | proton beam and J-PARC long; bottles true |
| M7 n → n′ strong field | new interaction, mirror sector (SPECULATIVE) | two-level mixing, Landau–Zener | high-field proton beam only |
| M8 SM field dependence | classical field | SM electroweak | none at relevant size |

### O3. Required size against the published budget (Δτ = 10.15 s, 1.143 %, 1.30×10⁻⁵ s⁻¹)
| Sub-hypothesis | Needed | Budgeted | Ratio |
|---|---|---|---|
| BL1 ⁶Li monitor ε_0 | +1.16 % | 0.5 s (0.056 %) | 20× |
| BL1 non-fluence systematics (lump) | 10.15 s | 1.7 s | 6× |
| BL1 trap nonlinearity | 10.15 s | correction −5.3 ± 0.8 s | 1.9× the correction, 12.7× its error |
| BL1 beam halo | 10.15 s | 1.0 s | 10× |
| BL1 backscatter / Si scattering | 10.15 s | 0.4 / 0.5 s | 25× / 20× |
| BL1 H₂ charge exchange | 1.14 % loss | ~0.3 % (Caylor, large unc.) | 3.8× (and more if ε_ion > 0) |
| UCNτ depolarisation | 1.30×10⁻⁵ s⁻¹ | ≤ 1.0×10⁻⁷ s⁻¹ | 130× |
| UCNτ residual gas | 1.30×10⁻⁵ s⁻¹ | ≈1.4×10⁻⁷ s⁻¹ (+0.11 s) | ≈90× |
| Material-bottle extra per-bounce loss | 2.6×10⁻⁷ – 2.6×10⁻⁶ per bounce | removed by extrapolation if ∝ bounce rate | not additive to extrapolated τ |
| J-PARC unsubtracted background | 1.23 % of S_β | observed excess over MC 2.4–4.2 % | 0.3–0.5 of the excess |

### O4. n → n′ conversion by field profile (Berezhiani model, Δm = 280 neV, θ0 = 1.66×10⁻³)
| Setting | Field | Conversion | Lifetime effect |
|---|---|---|---|
| NIST proton trap | 4.6 T solenoid | P_trap = 1.13×10⁻², P_det = 5.5×10⁻⁶ | +1.14 % (by construction) |
| J-PARC TPC | ≈0 T (LiNA 0.6 T) | ⟨P⟩ = 5.5×10⁻⁶, no loss channel | < 0.01 s |
| Material bottle | µT | 5.5×10⁻⁶ per bounce | removed by size extrapolation; per-bounce floor |
| Magnetic trap | < B_res | no crossing | ≈0 |
| SNS regeneration | 6.6 T scan | ~P² = 1.3×10⁻⁴ | limit 2.5×10⁻⁸: excluded ×5×10³ |

## Calculations
- `runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-mechanist_required_sizes.py` (log beside it). It computes:
  - the gap: 10.15 s, 1.143 %, 1.30×10⁻⁵ s⁻¹ (BL1 alone 9.88 s; Gravitrap 6.5 s);
  - BL1 item ratios;
  - the n_H₂ needed for proton charge-exchange loss (≈10¹⁴–10¹⁵ m⁻³, 4×10⁻⁷ to 4×10⁻⁶ Pa at 300 K) and the predicted 10 ms against 5 ms split (5.1 s);
  - the bottle gas pressures needed (N₂ 6×10⁻⁴ mbar, H₂ 2×10⁻⁵ mbar, He 5×10⁻³ mbar), the spin-flip rate and the per-bounce loss;
  - the J-PARC shift in terms of S_β (1.23 %);
  - SM τ_β with GS2023 pairing: PERKEO III 878.50 ± 0.88 s, PDG 879.65 ± 1.61 s, aSPECT 2024 889.58 ± 3.20 s, and Br_X for each.
- `runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-mechanist_nnprime_jparc.py` (log beside it). It computes:
  - the n → n′ beam shift as a function of Δm and θ0 through the toolkit `nn_mirror_osc.py`: θ0 = 1.66×10⁻³ needed at 280 neV, a sign reversal below µB_centre, and the regeneration excess ×5.1×10³;
  - the effects on J-PARC, bottles and magnetic traps;
  - the J-PARC pressure split: 13.6 ± 3.5 s stat, with a linear 0 kPa extrapolation of 897 ± 5 s that I do not claim;
  - J-PARC tensions: 2.24σ from the beam, 0.16σ from UCNτ.

## Candidate answers (at least 3; the null and a reframe count)
- [MECHANIST-A] **Proton-counting-beam systematic: a multiplicative ~1.1 % error in ε_p/ε_0 in BL1 (and Sussex–ILL).** Named sub-hypotheses, in mechanistic order:
  - (A1) the absolute ⁶Li monitor efficiency is 1.16 % low;
  - (A2) a proton loss that scales with trap length: residual-gas charge exchange with undetected molecular ions, halo protons, or a mis-sized nonlinearity correction;
  - (A3) proton backscatter or dead layer.

  | status: surviving | why: it is the only mechanism class whose chain predicts all of: proton beam long; J-PARC, magnetic traps and material bottles alike near 878 s; and SM τ_β(β-asymmetry λ) = 878.5 s [F14][F10]. No link needs new physics. But its weakest link is real: no named item reaches the needed size without being 6–25× its budget [O3], and Caylor finds H₂ charge exchange too small [D-17][F13]. | distinguishing prediction or test: BL2/BL3 (< 1 s, then 0.3 s [D-100][D-101]) should read ≈ 878 s. Within existing data, a gas-driven A2 predicts BL1's 10 ms and 5 ms subsets differ by ≈ 5 s [F5]. A1 predicts that re-calibrating the ⁶Li deposit with an independent absolute method (BL3 Alpha-Gamma upgrade, or ³He normalisation as in J-PARC) finds ε_0 about 1.2 % higher. | confidence: medium
- [MECHANIST-B] **Bottle systematic: a common unrecognised ~1.3×10⁻⁵ s⁻¹ loss in UCN storage.** Sub-hypotheses: (B1) magnetic traps (depolarisation, residual gas, marginal trapping); (B2) material bottles (unmodelled wall-loss energy dependence).

  | status: strained | why: the needed rate is 130× UCNτ's depolarisation bound and ≈90× its measured gas correction [F12]. Material and magnetic traps would need two unrelated agents of equal size and sign [F7], and material bottles actually read higher, not lower [D-73]. The candidate also needs a separate −10.8 s J-PARC error (M5) that no bottle mechanism supplies [F8]. B2 alone could explain part of the material/magnetic split, not the beam gap. | distinguishing prediction or test: in-bottle β counting (UCNProBe, 1–2 s [D-106]) would read the same as the storage lifetime in its own trap, and τSPECT (< 0.3 s [D-103]) with a different field geometry would read ≈ 888 s if B were true. Predicted SM τ_β(λ) ≈ 888 s requires the aSPECT λ. | confidence: medium (in its being strained)
- [MECHANIST-C] **Invisible dark decay (n → χφ, n → χχχ; SPECULATIVE)**, with the visible variants n → χγ and n → χe⁺e⁻ already excluded over ≥ 95 % of their windows [D-85][D-86].

  | status: strained | why: the chain is internally clean. But the λ link fails: τ_β(PERKEO III) = 878.50 ± 0.88 s gives Br_X = 0.08 ± 0.11 %, 95 % upper 0.25 %, against the 1.14 % needed [F14]. It also predicts J-PARC ≈ 888 s, which J-PARC disfavours at 2.2σ (weaker if J-PARC's gas-borne background is real [F10]). It needs dark repulsion to pass the neutron-star bound [D-88]. It survives only if the aSPECT a-coefficient λ is right (Br_X = 1.32 ± 0.36 %). | distinguishing prediction or test: Nab's a coefficient (Δλ/|λ| ≈ 0.04 % [D-107]) decides the λ link. LiNA at ~1 s [D-102] would read ≈ 888 s if C is true and ≈ 878 s if not. | confidence: medium
- [MECHANIST-D] **Neutron → mirror-neutron conversion in the strong proton-trap field (Berezhiani; SPECULATIVE)**, and Tan's inverse bottle-loss variant.

  | status: eliminated | why: its prediction pattern matches (beam long; J-PARC and bottles true), but it needs θ0 ≈ 1.7×10⁻³ with Δm tuned to within ~20–40 neV above |µn|·4.6 T. A Δm slightly lower reverses the sign [F11]. Its own conversion probability predicts SNS regeneration 5×10³ above the 2.5×10⁻⁸ limit, which caps the beam shift at ≈ 0.14 s [F11][D-62]. Tan's variant predicts UCNτ and J-PARC ≈ 888 s, contradicted [F11]. | distinguishing prediction or test: already done (SNS regeneration). A BL-type trap run at a different solenoid field (for example 3 T against 4.6 T) would show a large field dependence if any residual variant existed. | confidence: high
- [MECHANIST-E] **Reframe: the anomaly is "one proton-counting data set (BL1, plus the unverified Sussex–ILL) against everything", and J-PARC 2024 is not yet an independent arbiter.** Its internal 50 against 100 kPa split (13.6 ± 3.5 s stat) and its 4× excess gas-borne background are a mechanism of the right sign and size to move it by ~10 s [F9][F10]. The question then reduces to two artefact audits (BL1's ε_p/ε_0 and J-PARC's background subtraction) plus the λ tension (PERKEO against aSPECT [D-74]).

  | status: surviving (as framing) | why: every mechanistic route to "beam true" fails, except through the aSPECT λ [F14] and through J-PARC's own unexplained spread [F10]. The partition "beam against bottle" hides that the electron beam and the bottles share nothing mechanistically. | distinguishing prediction or test: J-PARC/LiNA pressure scan with the solenoid (background ×1/50 [D-102]). A flat τ(P) near 878 s removes the J-PARC caveat. A trend toward ~890 s at low P revives C and B. | confidence: medium
- [MECHANIST-F] **Null: no single dominant cause.** Several sub-budget effects each 1–3σ (for example BL1 charge exchange ~0.3 % ≈ 2.7 s [D-17], halo or nonlinearity mis-sizing, the Gravitrap/UCNτ spread [D-73], UCNτ year-to-year scatter [D-81]) plus a fluctuation.

  | status: strained | why: mechanistically the gap sits on the proton-beam side. At least three independent, unrelated items in BL1 would each need to be ~2–4× their errors, all with the same sign. The bottle side can contribute only ~3 s (the material-bottle excess), and in the wrong direction. The combined effect is still ≈ 4.5σ of BL1's total error [O3]. | distinguishing prediction or test: BL2 lands between 878 and 888 s, and several items move when BL3 varies pressure, field and detector. | confidence: low
- [MECHANIST-G] **Other new physics: excited neutron n* (Koch–Hummel), Veselský's n → X⁺e⁻ν̄ branch, or a field- or environment-dependent SM rate.**

  | status: eliminated (SM field dependence, 10¹³ too small [D-05]); strained (X⁺: every decay gives an electron, so J-PARC ≈ bottle fits, but a proton-less branch hits the same λ link as C [F14], and X⁺ is unseen [D-95]; n*: partly excluded by UCNτ holding and loading data [D-93]) | why: [F14], [D-05], [D-93], [D-95] | distinguishing prediction or test: the λ route decides X⁺. For n*, a lifetime that depends on the time since production in a beam. | confidence: medium

## What would change my mind
- A BL2 (or BL3) result near 888 s with its own new flux normalisation, a detector unlike BL1's, and a pressure or trap-time scan showing no trend. That would break the A chain and raise C, E and the J-PARC-artefact route.
- Nab or another a-coefficient measurement confirming aSPECT's λ ≈ 1.2668 at < 0.1 %. That would reopen C and B through the λ link [F14].
- BL1's published 5 ms against 10 ms subset comparison: a ~5 s difference supports A2 (gas); flat (< 1 s) disfavours it [F5].
- The J-PARC subtraction method: if the measured, not the MC, background is subtracted and a pressure-independent residual is shown, F9 and F10 lose force.
- A UCN bottle per-bounce loss ever measured below 5.5×10⁻⁶ would independently confirm the n → n′ exclusion. A measured per-bounce floor at that level would be a surprise that revives D.

## Assumptions I relied on
- The mean decay-proton energy is about 300 eV, and the H⁺ + H₂ charge-transfer cross section is 10⁻²⁰–10⁻¹⁹ m² (order of magnitude; not in the dossier).
- UCN–gas cross sections of ~20 b (N₂), 0.8 b (He) and 160 b (H₂) at thermal gas speeds, and 5–50 wall collisions per second in material bottles (order of magnitude).
- Cold-beam velocity spectrum, Maxwellian-like with 800 m/s scale, for the n → n′ average. Each SNS passage converts about as much as the NIST trap passage at resonance.
- The J-PARC Table II columns beyond stat are systematics (unlabelled in the extraction [D-24]). I used them only for the approximate-systematic variant.
- Sussex–ILL 889.2 s is used only in the gap sizing (unverified lead [D-22]). Results with BL1 alone differ by 0.3 s.
- The consistent-pairing SM τ_β [U-01] is re-derived through the toolkit calculator, not taken on trust.
