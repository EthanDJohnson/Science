# Brief: The neutron lifetime puzzle — beam (~888 s) versus bottle (~878 s)
slug: 2026-09-30-neutron-lifetime-beam-bottle | depth: deep | type: anomaly | date: 2026-09-30

## Question as asked
"What explains the neutron lifetime puzzle, where beam experiments that count decay protons give about 888 s but ultracold-neutron bottle experiments give about 878 s? Weigh unidentified experimental systematics (in which method, and which specific effect) against new physics such as dark decay or neutron–mirror-neutron oscillation. Take account of the 2024 J-PARC electron-counting beam result, the axial coupling gA and CKM unitarity, and name the measurement that would settle it."

## Question made precise
The question is read as: **what is the dominant cause of the gap between the proton-counting beam lifetime and the ultracold-neutron (UCN) storage lifetime, with what credence, and which feasible measurement would decide it?** The answer is a ranked, mutually exclusive slate of causes, each with the size of effect it needs, the evidence for and against it, and its predictions for the measurements still to come.

Definitions of loaded terms:
- **Neutron lifetime τn.** The total mean life of a free neutron at rest, 1/Γ_total, summed over every decay channel, visible or not.
- **β-decay partial lifetime τ_β.** 1/Γ(n → p e⁻ ν̄_e (+γ)). In the Standard Model (SM), τ_β = τn up to the bound-state branch n → H ν̄, whose branching ratio of order 4×10⁻⁶ (to be confirmed) is far below the anomaly. Radiative decays still produce a proton and an electron.
- **Beam method.** A cold-neutron beam passes through a decay volume. The decay rate is counted from one product, and the neutron density or fluence is measured absolutely. It measures a **partial** rate: Γ(n → p + anything) when protons are counted, Γ(n → e⁻ + anything) when electrons are counted.
  - *Proton-counting beam:* NIST BL1 (and BL2) and Sussex–ILL. Decay protons are held in a Penning-type trap in a strong (≈4–5 T) field. The fluence comes from a thin ⁶Li (or ¹⁰B) capture deposit, calibrated absolutely.
  - *Electron-counting beam:* J-PARC. A time-projection chamber (TPC) with a known ³He admixture counts decay electrons, and ³He(n,p)³H captures in the same gas give the neutron density. It has no strong trapping field.
- **Bottle method.** UCN are stored in a trap, and the survivors are counted after varying holding times. It measures the **total** disappearance rate, Γ_total + Γ_loss, so it needs every non-decay loss to be identified. Sub-classes, which have different systematics:
  - *material bottles:* wall losses, extrapolated to zero (Gravitrap, MAMBO II, Arzumanov, Steyerl and others);
  - *magnetic or magneto-gravitational traps:* no wall contact; depolarization and marginally trapped neutrons instead (UCNτ, Ezhov, and in future τSPECT and PENeLOPE).
- **"About 888 s" and "about 878 s."** Placeholders. The current values, their uncertainties and the tension between them are to be established by the research and computed by the statistician. "Beam" here means proton-counting beam unless stated otherwise.
- **Unidentified experimental systematic.** An effect within established physics that shifts a published result by more than its quoted uncertainty and is missing from, or underestimated in, the published error budget. A systematic explanation must name:
  - the method (proton-counting beam, electron-counting beam, material bottle or magnetic trap);
  - the specific effect (for example, the absolute efficiency of the neutron-fluence monitor, proton losses or trapping in the end regions of the proton trap, proton backscattering or detection efficiency, marginally trapped UCN, depolarization, or an unmodelled wall-loss energy dependence);
  - the size it would need against the published budget.
- **New physics.** Any effect beyond the SM that makes the rate seen by a beam experiment differ from the total disappearance rate. Examples:
  - a non-SM decay branch without a proton (Fornal–Grinstein dark decays n → χγ, n → χφ, n → χe⁺e⁻);
  - neutron → mirror-neutron (n → n′) conversion whose rate depends on the magnetic field (Berezhiani);
  - any other proposal the research turns up, such as a dependence of the decay rate on the environment or on the field.
- **"Settle."** A measurement or set of measurements, feasible within about 10 years (by 2036), that separates the leading surviving explanations at 3σ or more (5σ preferred). The answer must give its target precision, who is doing it and when results are expected.

Admissible physics:
- **Established:** the SM electroweak theory, with QED and electroweak radiative corrections; lattice QCD as a source of gA; nuclear-structure inputs to superallowed 0⁺→0⁺ decays; neutron optics and UCN physics; neutron-star physics at the level of standard equations of state.
- **Speculative, allowed only when labelled:** dark-sector particles and mediators, mirror sectors, and any other beyond-SM mechanism.

"Viable" has two tiers:
- **Now:** consistent with every current measurement, search and bound, within its stated assumptions.
- **Decidable:** a measurement expected by about 2036 would confirm or exclude it.

## Hidden premises to test
1. **The discrepancy is real and about 4σ.** The proton-counting side rests essentially on one experiment, NIST BL1, plus the older Sussex–ILL result. The bottle side is dominated by UCNτ. Test: the proper combination, scale factors, the choice of which results enter (superseded values excluded), and the look-elsewhere effect.
2. **"Beam versus bottle" is the right partition.** Since J-PARC, the right partition may be "proton counting versus everything else" (a method-specific effect), or "strong magnetic field versus weak" (a field-dependent effect). Test each partition against the data.
3. **The bottles are right.** Bottle results drifted by about 6σ around 2005–2010, older material-bottle values were higher, and later values still scatter (for example Gravitrap about 881.5 s against UCNτ about 877.8 s). Could an unidentified loss shorten every bottle result? A loss with a time constant of order 10⁵ s, about a day, would be needed. Would that loss have to be common to both material and magnetic traps?
4. **Beam and bottle measure the same quantity in the SM.** Check the size of every SM effect that makes τ_β differ from τn (the bound-state branch, radiative decays, protons not produced), and whether any of them approaches 1%.
5. **The J-PARC 2024 result is independent, correct and discriminating.** Check its central value, its systematic budget (about 4 s, to be verified), how its neutron normalization differs from NIST's, and its tension with each side. Can it on its own disfavour any candidate? Note that a dark decay with no electron predicts J-PARC ≈ beam, a proton-counting systematic predicts J-PARC ≈ bottle, and a strong-field n → n′ effect also predicts J-PARC ≈ bottle.
6. **The SM prediction from gA and Vud can arbitrate.** It depends on which measurement of λ = gA/gV is used (PERKEO III against aSPECT, which disagree), on the radiative corrections (the size of ΔR^V and its uncertainty, and the newer radiative correction to λ), and on the superallowed nuclear-structure corrections. The first-row CKM unitarity deficit ("Cabibbo angle anomaly") may mean the superallowed Vud is itself shifted. Test whether the SM prediction today favours the bottle value, the beam value, or neither.
7. **Dark decay is invisible to bottles and to J-PARC.** Check this channel by channel: could an e⁺e⁻ or γ final state be counted as a decay electron in the J-PARC TPC, or leave a signal in UCNτ's detectors?
8. **The neutron-star bound kills dark decay.** It holds only unless χ has repulsive self-interactions, or unless other dark-sector content stiffens the equation of state. Test how model-dependent it is.
9. **n → n′ conversion is excluded.** Test which regions of mixing time, mass splitting and mirror field the searches (ORNL/HFIR, PSI, ILL and others) exclude, and whether the region needed to explain the gap survives.

## What counts as an answer
- **A ranked, mutually exclusive slate with credences.** It must include at least:
  - a **proton-counting-beam systematic**, with named rival effects as sub-hypotheses;
  - a **bottle systematic** (unidentified loss), with sub-hypotheses for material and magnetic traps;
  - **dark decay**, with its variants;
  - **n → n′ oscillation**;
  - **any other new physics** the research supports;
  - the **null:** a statistical fluctuation together with underestimated errors spread over several experiments, with no single dominant cause.

  It must also consider a **reframe** in which the premise is wrong, for example that the real anomaly is "BL1 against everything" rather than "beam against bottle".
- **For each candidate:**
  - the shift it produces in each class of measurement, with its sign, against the observed gap (about 1.1% of τ, or a missing loss rate of about 1.3×10⁻⁵ s⁻¹; to be recomputed from the combined values);
  - its causal chain and weakest link;
  - the evidence for and against it, by dossier ID;
  - whether the published error budgets leave room for it.
- **A prediction matrix,** with one column per independent class of measurement:
  - proton-counting beam (BL1, and BL2 and BL3 to come);
  - electron-counting beam (J-PARC);
  - material bottles;
  - magnetic traps;
  - in-bottle β counting (UCNProBe or similar);
  - space-based measurements (Lunar Prospector, MESSENGER);
  - the SM prediction from λ and Vud;
  - direct searches: n → χγ, n → χe⁺e⁻, n → n′, and ¹¹Be;
  - neutron-star bounds.
- **The gA and CKM verdict:** τ_β predicted by the SM for each λ input, the resulting upper bound on an exotic branching ratio, and how the λ tension and the first-row unitarity deficit change it.
- **The J-PARC verdict:** what the 2024 result excludes or disfavours, and at what significance.
- **The deciding measurement:**
  - the single measurement that would settle the question, with its target precision, who is doing it, when it is expected, and the result each candidate predicts;
  - a runner-up, and the precision on λ (from Nab or PERC) at which the SM prediction becomes decisive on its own.

## Research facets
- **theory:**
  - owns: the SM theory of neutron β decay, meaning the V−A structure, the master formula linking τn, λ and Vud, the structure and meaning of the radiative corrections (ΔR^V, the outer correction, the phase-space factor f, and the recent λ-specific radiative correction), and the bound-state and radiative branches;
  - owns: the formal models of the new-physics candidates (the Fornal–Grinstein dark-decay variants and their allowed mass window; Berezhiani's n → n′ mechanism and its resonance condition in a magnetic field; other proposed mechanisms);
  - leaves numerical inputs to quantitative, experimental bounds to critiques, and lifetime measurements to engineering.
- **quantitative:**
  - owns: every SM input and related measured quantity: λ from PERKEO III, UCNA, aSPECT, aCORN and PERKEO II; lattice gA; |Vud| from superallowed 0⁺→0⁺ decays under each ΔR^V evaluation; |Vus| from K_l3 and K_μ2, and their tension; |Vub|; the first-row unitarity sum; the constants in the master formula; masses and the neutron magnetic moment;
  - owns: the planned or running λ and correlation experiments (Nab, PERC, BRAND, aSPECT follow-ups), with their target precision and timelines;
  - leaves the lifetime measurements themselves to engineering.
- **critiques:**
  - owns: the proposed explanations and every search and bound against them:
    - dark-decay searches: n → χγ (LANL/UCNτ), n → χe⁺e⁻ (UCNA, PERKEO II), the ¹¹Be β-delayed proton results, neutron-star bounds, nuclear stability, and cosmological or astrophysical bounds;
    - n → n′ searches: ORNL/HFIR, SNS, PSI n2EDM and ILL, including the claimed anomalies in some of them;
  - owns: published critiques of specific experiments and papers proposing a specific systematic explanation (for example critiques of the proton-trap method, of UCNτ, or of J-PARC), and the replies to them;
  - leaves each experiment's own published error budget to engineering.
- **engineering:**
  - owns: the lifetime measurements, method by method: proton-counting beam (NIST BL1, including Yue 2013 superseding Nico 2005; Sussex–ILL); electron-counting beam (J-PARC 2020 and 2024); material bottles; magnetic and magneto-gravitational traps; space-based measurements;
  - for each, owns: the value with statistical and systematic uncertainties exactly as quoted, the largest items of the systematic budget, blinding, the in-situ tests (for example BL1's variation of trap length and deposit), and which results supersede or share an apparatus with others;
  - owns: the running and planned lifetime experiments (BL2, BL3, the J-PARC upgrade, UCNτ+, τSPECT, PENeLOPE, HOPE, Gravitrap upgrades, UCNProBe and any in-bottle β-counting design), with who runs each, its target precision and when results are expected;
  - leaves λ and correlation experiments to quantitative.
- **frontier:**
  - owns: the newest material, newest first: preprints, conference talks and proceedings from 2024 to 2026 (for example any BL2 result or status talk, any J-PARC update or erratum, UCNτ or τSPECT results, first Nab results, new ΔR^V or lattice radiative-correction work, the newest n → n′ searches, and new theory proposals or reviews), each labelled with its evidential status;
  - reports a result already in a journal only when something newer (an update, erratum or critique) exists, and otherwise leaves it to the facet that owns it.

## Worked calculations
- **statistician:**
  - the weighted combination of each measurement class (proton-counting beam, electron-counting beam, material bottles, magnetic traps, space), with the PDG scale factor, excluding superseded values;
  - the tension between the proton-counting beam and the bottles, with and without J-PARC, and with J-PARC treated as its own class; grouped χ² within and between classes;
  - the tension of J-PARC 2024 with each side, using its asymmetric errors;
  - the Bayes-factor bounds for "one common value" against "two values";
  - the precision a future experiment needs to separate the leading candidates at 3σ and at 5σ.

  This is the reference for the observed gap.
- **constraints:**
  - the SM prediction of τ_β from λ and |Vud| through the master formula with radiative corrections, for each λ input (PERKEO III, UCNA, aSPECT, the PDG average) and each Vud input (superallowed, under each ΔR^V evaluation);
  - the upper bound this places on an exotic branching ratio, Br_X = 1 − τ_bottle/τ_β;
  - the sensitivity coefficients ∂τ/∂λ and ∂τ/∂Vud, and hence the λ precision at which the SM prediction becomes decisive;
  - the dark-decay kinematic window: the χ mass range from ⁹Be stability and χ stability, and the photon or e⁺e⁻ energy ranges.
- **mechanist:**
  - the required size of each systematic sub-hypothesis: the fractional error in neutron fluence or proton detection efficiency that a proton-counting beam would need, and the unidentified loss rate a bottle would need;
  - the conversion probability for n → n′ in the field profiles of the NIST proton trap, J-PARC, magnetic traps and material bottles, against the ORNL/HFIR and PSI limits.

## Known constraints, prior attempts, and user-supplied data
No user-supplied data.

Starting points for the researchers. These come from the framing session's memory and are leads, not established claims: each must be found and quoted before use, and any value here may be wrong.

- **Proton-counting beam:**
  - Yue et al. 2013, Phys. Rev. Lett. 111, 222501 (NIST BL1, about 887.7 ± 1.2 ± 1.9 s). It re-analyses and supersedes Nico et al. 2005, Phys. Rev. C 71, 055502.
  - Byrne & Dawber 1996, Europhys. Lett. 33, 187 (Sussex–ILL, about 889.2 ± 3.0 ± 3.8 s).
  - BL2 progress reports (Hoogerheide et al.) and the BL3 design.
- **Electron-counting beam:**
  - Hirota et al. 2020, Prog. Theor. Exp. Phys. 2020, 123C02 (J-PARC, about 898 ± 10 +15/−18 s).
  - The 2024 J-PARC result: arXiv:2412.19519 (believed to be Fuwa et al.; about 877.2 ± 1.7 (stat) +4.0/−3.6 (sys) s; verify all of this).
- **Bottles:**
  - Gonzalez et al. 2021, Phys. Rev. Lett. 127, 162501 (UCNτ, about 877.75 s), and Pattie et al. 2018, Science 360, 627;
  - Serebrov et al. 2018, Phys. Rev. C 97, 055503 (Gravitrap, about 881.5 s);
  - Ezhov et al. 2018, JETP Lett. 107, 671 (magnetic trap, about 878.3 s);
  - Pichlmaier et al. 2010 (MAMBO II), Arzumanov et al. 2015, Steyerl et al. 2012, Serebrov et al. 2005.
- **Space-based:** Wilson et al. 2020, Phys. Rev. Research 2, 023316 (Lunar Prospector), and a MESSENGER analysis by the same group.
- **Reviews:** Wietfeldt & Greene 2011, Rev. Mod. Phys. 83, 1173; the PDG neutron mean-life review (2024 edition or later).
- **λ:**
  - Märkisch et al. 2019, Phys. Rev. Lett. 122, 242501 (PERKEO III);
  - Brown et al. 2018, Phys. Rev. C 97, 035505 (UCNA);
  - Beck et al. 2020, Phys. Rev. C 101, 055506 (aSPECT);
  - Hassan et al. 2021 (aCORN).
- **Master formula and radiative corrections:**
  - Czarnecki, Marciano & Sirlin 2018, Phys. Rev. Lett. 120, 202002;
  - Seng, Gorchtein, Patel & Ramsey-Musolf 2018, Phys. Rev. Lett. 121, 241804;
  - Hardy & Towner 2020, Phys. Rev. C 102, 045501;
  - Cirigliano et al. 2022, Phys. Rev. Lett. 129, 121801 (pion-induced radiative correction to λ);
  - later ΔR^V updates from lattice QCD and dispersion relations.
- **Dark decay:**
  - Fornal & Grinstein 2018, Phys. Rev. Lett. 120, 191801, and its erratum;
  - Tang et al. 2018, Phys. Rev. Lett. 121, 022505 (n → χγ);
  - Sun et al. 2018, Phys. Rev. C 97, 052501 (UCNA, n → χe⁺e⁻);
  - Klopf et al. 2019, Phys. Rev. Lett. 122, 222503 (PERKEO II);
  - McKeen et al. 2018, Baym et al. 2018 and Motta et al. 2018 (neutron stars);
  - Czarnecki et al. 2018 and Dubbers et al. 2019, Phys. Lett. B 791, 6 (bounds from λ);
  - Ayyad et al. 2019, Phys. Rev. Lett. 123, 082501 (¹¹Be).
- **Mirror neutrons:**
  - Berezhiani 2019, Eur. Phys. J. C 79, 484;
  - Tan 2019, Phys. Lett. B 797, 134921;
  - Broussard et al. 2022, Phys. Rev. Lett. 128, 212503 (ORNL/HFIR);
  - Abel et al. 2021, Phys. Lett. B 812, 135993 (PSI);
  - Berezhiani et al. 2017, Eur. Phys. J. C 77, 717 (claimed anomalies).

## Prior runs
None bear on this question.
- 2026-09-29-problem-of-time-quantum-gravity (2026-09-29): ignore. It is unrelated (quantum gravity) and matched only on generic words.
- 2026-09-29-alcubierre-negative-energy and 2026-09-29-warp-bubble-shapes (2026-09-29): ignore. They are unrelated (warp drives).
