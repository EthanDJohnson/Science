# The neutron lifetime puzzle, proton-counting beam (~888 s) versus UCN storage (~878 s): report
*Run 2026-09-30-neutron-lifetime-beam-bottle · 2026-09-30 · depth deep · question: "What explains the neutron lifetime puzzle, where beam experiments that count decay protons give about 888 s but ultracold-neutron bottle experiments give about 878 s? Weigh unidentified experimental systematics (in which method, and which specific effect) against new physics such as dark decay or neutron–mirror-neutron oscillation. Take account of the 2024 J-PARC electron-counting beam result, the axial coupling gA and CKM unitarity, and name the measurement that would settle it."*

Units: SI throughout (lifetimes in s, rates in s⁻¹, fields in T); λ = gA/gV, a, b and branching ratios dimensionless; particle masses and energies in MeV or neV.

## Bottom line
The gap is real, not a chance fluctuation, and it sits almost entirely in one measurement. The most likely cause, at roughly 60%, is an unidentified error in the proton-counting beam method that makes it read about 1.1% too long; the storage value near 878 s is most likely the true lifetime. The biggest reason is that every independent check that neither counts protons nor stores neutrons, namely the electron-counting J-PARC beam and the Standard-Model prediction from the electron-asymmetry coupling gA, lands at 878 s, while the beam side rests on a single 2005 dataset. Nobody has found an effect of the needed size, so about a seventh of the probability goes to several smaller beam-side errors plus bad luck. New physics totals under 10%. Nab's a-coefficient measurement will decide.

## Ranked answers
| # | Candidate | Measurements it shifts, and by how much against the gap | Consistent with independent data? | Deciding measurement (who, when) | Probability |
|---|---|---|---|---|---|
| 1 | C1 Unidentified proton-counting-beam systematic (storage true) | Proton beam +9.65 s (whole gap, 1.10 ± 0.23% fitted to BL1 and Sussex–ILL); zero elsewhere | Yes: J-PARC −0.26σ, A-route SM +0.41σ, CKM −1.2σ. Only aSPECT's a-route is against (3.0–3.5σ) | Nab a (ORNL SNS; no date) plus BL2/BL3 with trap-time, gas and field scans (NIST; "next few years"/no date) | 0.62 |
| 2 | C7 Null, narrowed to the proton side: BL1's error ~2× too small, several same-sign items plus fluctuation | Carries the gap only as a proton-side excursion; J-PARC contributes 0 s and material bottles −0.46 s (wrong sign) | As C1, but must also absorb Sussex–ILL (2.2σ) and aSPECT (3.2σ) same-sign excursions | BL2/BL3 scans: C7 predicts no single lever ≥ 3.3 s; needs ≲ 1 s per scan | 0.14 |
| 3 | C8 Reframe, sharp form: one pre-detection proton-side cause behind both the lifetime and the aSPECT λ tension | Proton beam +9.9 s and aSPECT \|a\| low by 2.7% | Detector-side link excluded in situ (aSPECT 2024 reanalysis; BL1 voltage extrapolation); only a loss tuned to T₀ ≈ 21–22 eV fits both | Nab a aSPECT-like together with LiNA/UCNProBe ≈ 878 s | 0.05 |
| 4 | C2 Unidentified storage-only loss (beam true) | Magnetic traps −10.2 s, material −7.9 s; needs 49–140× UCNτ's in-situ bounds; J-PARC needs a separate −10.8 s | No on the A route: storage-free data put 888 s at 3.8–4.2σ; yes only if aSPECT's λ is right | UCNProBe β-rate minus storage lifetime in one trap (LANL; 1–2 s; no date): +9.65 s vs 0 | 0.04 |
| 5 | C3 Invisible dark-decay branch ≈ 1.1% (speculative) | Proton beam and J-PARC both +9.7 s; bottles 0 | J-PARC 2.2σ against; PDG-scaled world λ 7σ against (2.4σ conditional on aSPECT); needs dark repulsion for 2 M☉ stars | LiNA (J-PARC; ~1 s; no date): 888 vs 878 s, plus Nab a | 0.04 |
| 6 | C6 Excited neutron n* with 0.3 s ≲ τγ < 139 s (speculative) | Proton beam +9.9 s; predicts J-PARC ≥ 887.8 s because its neutrons are younger | J-PARC 2.4σ against (1σ scaled); escape needs fission-only production; field variant eliminated | LiNA, and a proton-counting beam at a spallation source | 0.02 |
| 7 | C5 Proton-less, electron-always X⁺ branch (speculative) | Proton beam +9.9 s only if τ_X ≲ 1 ms; then bound neutrons decay 10⁴–10¹⁶× faster than limits allow | Preprint's own parameters excluded by nuclear stability; only a ~1 MeV mass sliver nobody has modelled survives; needs a-route λ | Nab a; refit of PERKEO II/UCNA e⁺e⁻ data with a continuous spectrum | 0.01 |
| 8 | C4 n → n′ conversion in the 4.6–5 T trap (speculative) | Needs SNS regeneration ≥ 9×10⁻⁴ against a limit of 2.5×10⁻⁸ | No: excluded by two SNS searches that used BL1's measured field map | Already done (Broussard 2022, Gonzalez 2024) | 0.01 |
| 9 | None of these | — | — | — | 0.07 |

## Why, candidate by candidate

**The observed gap.** Proton-counting beam 887.97 ± 2.04 s (BL1 carries 82% of the weight) against all storage 878.32 ± 0.43 s (scale factor 1.85): Δ = 9.65 ± 2.08 s, 4.63σ local, 4.1–4.4σ after 3–10 look-elsewhere partitions [calc: lens-statistician_combination.py; M-STATISTICIAN-02/-03]. A pure fluctuation is effectively excluded (maximum odds 8000:1). With four classes the within-class χ² is 8.4/7 and the between-class χ² 38.0/3, so the disagreement is structured by method, not diffuse. Bailey's heavy-tail base rate says a 4.6σ two-method gap is a 1-in-25 to 1-in-100 event in the record of unrecognised errors, and 0 of 7 sourced precision disagreements ended in new physics (empiricist analysis).

**C1 (0.62).** *For:* every storage-free arbiter sides with 878 s: J-PARC 877.2 +4.35/−3.98 s (0.26σ from storage, 2.24σ from the beam); A-route τ_β = 878.70 ± 0.83 s (0.41σ from storage, 4.2σ from the beam); the first-row CKM sum is 0.99898(87) (−1.2σ) with storage but 0.98842(251) (−4.6σ) with BL1 [M-CONSTRAINTS-02/-04]. Without BL1 the proton-versus-rest tension is 2.2σ. A single 1.09% multiplicative count deficit fits both proton-counting results (χ² 0.08/1) and disturbs no other class (C1-0). *Against:* no identified effect reaches the size. In-situ measurements close the fluence monitor (Yue 2018: 0.058% ↦ 0.51 s, 19× short), H₂ charge exchange (Caylor 2025: H₂⁺ is detected within 1.5% of protons; worst case < 0.5 s) and proton detection (0.64 s) (C1-1). The advocate conceded all three (cruxes/C1.md). aSPECT's a-route (τ_β = 889.58 ± 3.20 s) is 3.0–3.5σ against C1, but it is one experiment against three consistent β-asymmetry results (χ² 1.51/2). *Which effect:* current data cannot identify it. Of C1's 0.62, about 0.38 is "unidentified"; about 0.14 is A4, a mis-sized or mis-signed large correction (⁶Li absorption +5.4 s or trap nonlinearity −5.3 s: a 2× error gives 55% of the gap, a sign error 112%, untested); about 0.10 is A2-other, charge exchange or neutralisation on non-H₂ residual gas (qualitative support from Byrne 2019/2022, abstracts only, at trapping times 10³× BL1's). Neither named effect has a quantified mechanism of the right size, so neither ranks above "unidentified". Scope: Sussex–ILL's agreement favours a method-generic error (A-gen, roughly 60:40 over BL1-specific), which matters for the test: BL2 as built could also read long.

**C7 narrowed (0.14).** All three verdicts kill the cross-class form: J-PARC is in neither pole (d(gap)/d(J-PARC) = 0), and the material bottles' +2 s widens the gap. What survives is "BL1's total error underestimated about 2×, several modest same-sign items plus a fluctuation": doubling BL1's error puts it 2.19σ from UCNτ [M-DIALECTICIAN-08]. In heavy-tail Monte Carlo, gaps like this are single-outlier-dominated in 85–90% of draws (C7-1), which supports BL1 as the tail event but not "no single effect": Bailey's and the 2005 neutron-lifetime precedents were resolved by identified effects. C7 is nearly degenerate with C1's BL1-specific scope; it differs only in whether one lever ≥ 6.6 s will ever be found.

**C8 sharp form (0.05).** The partition statement is right (proton-counting against the rest beats beam against bottle by Δχ² = 5.3, all from J-PARC) but that is C1. The sharp claim, one proton-side cause for both tensions, fails at the one shared element: a uniform 1.1% proton loss changes aSPECT's fitted a by 0.000% because its normalisation is free (C8-2 calc, 2 PASS), aSPECT's 2024 reanalysis raised detector losses 35% with "no effect on the final result", and BL1 extrapolates detector-energy-dependent losses away in situ. Only a recoil-energy loss tuned to ±1 eV in T₀ fits both (C8-0). The advocate conceded the detector-side case. Its residual weight comes from the real coincidence that three proton-detecting results all read high.

**C2 (0.04).** Every named loss channel in wall-free UCNτ (depolarisation, heating, gas) is 49–195× too small, and the needed rate is not common (material 0.98×10⁻⁵ s⁻¹ against magnetic 1.27×10⁻⁵ s⁻¹, 2.95σ). Storage-free data (J-PARC plus SM) exclude 888 s at 4.2σ on the A route, 3.4σ on the PDG λ, and favour it only on the a route (profile likelihood C1:C2 = 7100:1, 244:1, 0.14:1) (C2-2). The documented storage systematics of 2005–2010 had the opposite sign. The advocate withdrew "common" and concedes C2 needs one more independent failure than C1.

**C3 (0.04).** *New-physics prior:* the base rate gives about 0.07–0.11 for any new-physics resolution (Laplace on 0/7 or 0/12 cases). *Evidence that moved it down:* J-PARC counts electrons and reads 877.2 s where C3 needs 888 s (likelihood 5–12:1 against); the three β-asymmetry λ measurements each exclude the needed |λ| = 1.2681 ± 0.0018 at 3.0–4.4σ; the PDG-scaled world λ plus J-PARC gives Br_X = 0.066 ± 0.140%, 95% upper limit 0.30%, needed 1.09% at 7.2σ (C3-2 log). The fair conditional statement, conceded by the advocate, is 2.4σ on the a route plus discarding the whole A group. Minimal dark decay collapses neutron stars to 0.69–0.70 M☉ [M-CONSTRAINTS-09]; escapes exist but the threshold is EOS-dependent. The math check M-CONSTRAINTS-08 corrected the single-χ mixing rate prefactor and made τ_H fall 1.1–17× below its bound, closing those variants. What survives is the invisible χφ/χχχ/χA′ channel with dark repulsion, conditional on aSPECT.

**C6 (0.02).** The field variant is short by 3×10¹⁰ (6×10⁹ with the Q⁵ lever) [M-MECHANIST-13 corrected the factor; elimination stands]. J-PARC's neutrons are 10–40 ms old against BL1's 47–155 ms, so under equal production J-PARC must read ≥ 887.8 s (2.4σ against; 1σ scaled) (C6-0/-1). UCNτ bounds τγ < 139 s (Blatnik) and Nab bounds ΔE ≲ 21 keV. A fission-only n* escapes but is unmotivated. One lens supported it.

**C5 (0.01).** An X⁺ within 0.084% of the proton's charge-to-mass ratio is trapped and counted by BL1 unless τ_X ≲ 0.5–1 ms; that width makes bound neutrons decay through an off-shell X⁺ at 10⁷–10²³ yr against ≥ 1.6×10²⁵ yr mode-independent limits, Earth heat flow and Borexino (three independent calculations, C5-0/-1/-2). The advocate conceded the preprint's model is dead; only a 0.83 MeV tuned sliver with no neutron-star model survives.

**Deciding measurement.** Nab's a coefficient (ORNL SNS; goal Δλ/|λ| = 0.04%, σ_λ ≈ 0.0005; upgraded for precision running November 2025; no a value, no date [D-107]). A PERKEO-like result sits 3.5σ from aSPECT and makes the SM route decisive on its own (τ_β = 878.50 ± 0.84 s, 4.3σ below the proton pole), ending C2, C3, C5 and C8's sharp form. An aSPECT-like result sits 12.7σ from the A route and would refute C1 as stated. Read it with LiNA (J-PARC; ~1 s; commissioned February 2024; no date) or UCNProBe (LANL; 1–2 s; no date): 888 s at 1 s is 8.9σ from the storage pole, but 878 s is at most 4.4σ from BL1 because BL1's own 2.25 s error caps that side [M-EXAMINER-11 refuted the lenses' "≥ 5σ"; M-STATISTICIAN-14]. A 5σ decision against the beam pole therefore also needs BL2/BL3. On the SM route alone, 5σ needs σ_λ ≤ 0.00156 (0.12%), which PERKEO III already meets; the bottleneck is the A/a split, not precision. Runner-up: LiNA with a pressure scan.

## Eliminated, and what eliminated them
- **C4 (strong-field n → n′):** verdicts C4-0, C4-1, C4-2, all refuted. Two independent profile calculations put the SNS regeneration signal 2.5×10⁴–1.4×10⁷ times above the 2.5×10⁻⁸ limit everywhere in the 278–320 neV window (C4-0 log), and Broussard 2022 and Gonzalez 2024 (p < 3.1×10⁻¹⁰) used BL1's measured field map. Below 277 neV the sign reverses. Tan's inverse variant contradicts UCNτ and J-PARC; the weak-field variant is excluded by PSI.
- **Sub-hypotheses:** C1's A1, A2-H₂ and A3 (C1-1, in-situ bounds); C6's field dependence (C6-0/-1/-2); C5's preprint parameters (C5-0/-1/-2); C7's cross-class form (C7-0/-1/-2); C8's detector-side common cause (C8-1/-2); C3's χγ, χe⁺e⁻ (except T_ee < 32 keV), single-χ mixing and minimal neutron-star sector (C3-1/-2, M-CONSTRAINTS-08/-09).

## Assumptions every surviving answer shares
- The reference gap as computed: BL1's quoted 2.25 s total error; Sussex–ILL entered from the PDG listing, not the paper; Ezhov from a search summary.
- J-PARC 2024 is a preprint; its four run conditions (χ² 15.8/3) are treated as a scale factor, not a bias. If Desai's pressure effect moved it upward by ≥ 5 s, C1's second leg weakens and C3 gains.
- The SM route pairs Vud = 0.97361(32) with its own ΔR^V (U-01, verified), with V−A couplings and b = 0.
- One of the two λ families (β-asymmetry or proton-recoil) is wrong; the material–magnetic 2.2 s split is a separate second-order tension left to the null.
- Planned-experiment precisions (BL2 < 1 s, LiNA ~1 s, UCNProBe 1–2 s, Nab 0.04%) come from proceedings and search summaries.

## What would change this verdict
1. **Nab's a coefficient** (ORNL SNS; date unknown). aSPECT-like: C1 falls below about 0.2 and C2/C3/C8-sharp share most of the rest; PERKEO-like: C1 rises toward 0.75–0.8 and the 888-s world falls below 0.03.
2. **LiNA or UCNProBe at ≤ 1.5 s** (J-PARC/LANL; no dates). 888 s: C3 (or C2 if UCNProBe agrees) leads; 878 s: C2 and C3 drop below 0.01 each and C1 plus C7 take about 0.85.
3. **BL2/BL3 with diagnostic scans** (NIST; "next few years"/no date). 878 s with a named lever ≥ 6.6 s: C1 becomes identified, above 0.8; 878 s with no lever: C1 and C7 tie; 888 s with a new monitor and characterised gas: the beam side is replicated and the 888-s world rises to the lead.

## Key numbers
| Quantity | Value (units) | Source or calc |
|---|---|---|
| Proton-counting beam mean | 887.97 ± 2.04 s (BL1 82% of weight) | lens-statistician_combination.py; M-STATISTICIAN-01 |
| All storage mean | 878.32 ± 0.43 s (S = 1.85) | same |
| Gap | 9.65 ± 2.08 s, 4.63σ local, 4.1–4.4σ global; 1.09%; 1.24×10⁻⁵ s⁻¹ | M-STATISTICIAN-02/-03 |
| Four-class χ² | within 8.4/7, between 38.0/3 (5.55σ) | M-STATISTICIAN-04 |
| J-PARC 2024 | 877.2 ± 1.7 +4.0/−3.6 s; 0.26σ from storage, 2.24σ from beam (1.81σ inflated); internal χ² 15.8/3 | D-23, D-24; M-STATISTICIAN-05 |
| SM τ_β, A route / a route | 878.70 ± 0.83 s / 887.21 ± 2.93 s (aSPECT 2024 alone 889.58 ± 3.20 s) | M-CONSTRAINTS-02 |
| λ split | PERKEO III vs aSPECT 2024 3.49σ; A group χ² 1.51/2 | M-STATISTICIAN-10 |
| Br_X upper limit (95%) | 0.25% (PERKEO III), 0.30% (world λ + J-PARC); needed 1.09% | M-CONSTRAINTS-03; falsifier-C3-2_bounds.py |
| First-row CKM sum | 0.99898(87) (storage) vs 0.98842(251) (BL1), A-route λ | M-CONSTRAINTS-04 |
| Needed BL1 shift vs budget | 4.4× total error; monitor 19× short, H₂ < 0.5 s, detection 15× short | M-CONSTRAINTS-12; falsifier-C1-1 |
| Needed UCNτ loss vs bounds | 1.27×10⁻⁵ s⁻¹ = 49× systematic, 130–140× depolarisation | M-MECHANIST-06; falsifier-C2-0 |
| SNS regeneration | limit 2.5×10⁻⁸ (2022), 3.1×10⁻¹⁰ (2024); C4 predicts ≥ 9×10⁻⁴ | D-62; falsifier-C4-0/-1/-2 |
| Uniform 1.1% proton loss in aSPECT | Δa/a = 0.000% | falsifier-C8-2_bounds.py |
| Precision to settle | ≤ 1.93 s total for 5σ vs storage pole; vs BL1 pole capped at 4.4σ | M-STATISTICIAN-14; M-EXAMINER-11 |

## Caveats
- **Search summaries and unverified inputs:** Ezhov 2018 (search summary); Sussex–ILL from the PDG listing only; BL2, τSPECT and UCNProBe targets and dates (search summaries); WIETFELDT 24 read as aCORN by inference.
- **Papers to request:** Wietfeldt et al. 2023, PRD 107, 118501 (the BL1 team's residual-gas limits, which would bound A2-other); Desai 2026, EPJA 62, 154 (size and sign of J-PARC's pressure effect); Byrne et al. 2022, EPJA 58, 151 (whether the claimed proton-trap losses apply to BL1).
- **Unresolved contradictions:** the 3.5σ λ split; J-PARC's internal scatter and 4–5× background excess; the material–magnetic 2.95σ split.
- **Math checks:** M-CONSTRAINTS-14 (χ² ledger) is unverified and not relied on here; M-CONSTRAINTS-09's neutron-star escape threshold is EOS-dependent (50–100 MeV); M-CONSTRAINTS-13's equal-passage premise is superseded by the refuters' explicit profile calculations. Refuted items (M-CONSTRAINTS-08, M-EXAMINER-10/-11/-12, M-EMPIRICIST-11, M-MECHANIST-13, M-DECOMPOSER-01) change no ranking; M-EXAMINER-11 changes the stated "settle" precision.
- **Speculative physics used, labelled:** dark-sector decays and repulsive dark interactions (C3, C5), mirror neutrons (C4), an excited neutron state (C6).

## Sources
- Yue et al. 2013, PRL 111, 222501 (BL1); Nico et al. 2005, PRC 71, 055502, arXiv:nucl-ex/0411041, https://arxiv.org/abs/nucl-ex/0411041
- Yue et al. 2018, Metrologia 55, 460, arXiv:1801.03086, https://arxiv.org/abs/1801.03086
- Caylor et al. 2025, PRC 112, 065501, arXiv:2506.01682, https://arxiv.org/abs/2506.01682
- Wietfeldt et al. 2023, PRD 107, 118501 (abstract only)
- Fuwa et al. 2024 (J-PARC), arXiv:2412.19519 (preprint), https://arxiv.org/abs/2412.19519
- Musedinovic et al. 2025, PRC 111, 045501, arXiv:2409.05560, https://arxiv.org/abs/2409.05560; Gonzalez et al. 2021, arXiv:2106.10375, https://arxiv.org/abs/2106.10375
- Serebrov et al. 2018, PRC 97, 055503 (Gravitrap); Serebrov & Fomin 2010, arXiv:1005.4312, https://arxiv.org/abs/1005.4312
- PDG encoder listing s017 (2026), https://pdg.lbl.gov/encoder_listings/s017.pdf
- Märkisch et al. 2019, PRL 122, 242501, arXiv:1812.04666, https://arxiv.org/abs/1812.04666; Brown et al. 2018, PRC 97, 035505, arXiv:1712.00884
- Beck et al. 2020, PRC 101, 055506, arXiv:1908.04785, https://arxiv.org/abs/1908.04785; Beck et al. 2024, PRL 132, 102501, arXiv:2308.16170, https://arxiv.org/abs/2308.16170
- Wietfeldt et al. 2024 (aCORN), PRC 110, 015502, arXiv:2306.15042
- Czarnecki, Marciano & Sirlin 2018, PRL 120, 202002, arXiv:1802.01804; Dubbers et al. 2019, PLB 791, 6, arXiv:1812.00626
- Fornal & Grinstein 2018, PRL 120, 191801, arXiv:1801.01124, https://arxiv.org/abs/1801.01124
- Broussard et al. 2022, PRL 128, 212503, arXiv:2111.05543, https://arxiv.org/abs/2111.05543; Gonzalez et al. 2024, PRD 110, 072022, arXiv:2402.15981, https://arxiv.org/abs/2402.15981
- Koch & Hummel 2024, PRD 110, 073004, arXiv:2403.00914; Blatnik et al. 2024, arXiv:2406.10378 (preprint); Nab (Gonzalez et al.) 2026, PRC 113, 035501, arXiv:2508.16045
- Veselský et al. 2025, arXiv:2507.17340 (preprint)
- Bailey 2017, R. Soc. Open Sci. 4, 160600, doi:10.1098/rsos.160600
- González-Alonso, Naviliat-Cuncic & Severijns 2019, PPNP 104, 165, arXiv:1803.08732
- Run files: dossier.md, candidates.md, verdicts/C1–C8, cruxes/C1–C8, analyses/statistician.md, analyses/empiricist.md, math/*.md, and the calc/*.py.log files cited above (all under runs/2026-09-30-neutron-lifetime-beam-bottle/).