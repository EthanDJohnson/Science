# Research: engineering
status: final
Mandate: experimental and engineering state of the art: what has been built or measured, at what scale, and its technology readiness; and the planned or running experiments that will improve on it. Extended on 2026-10-08 with the demonstrated-capability anchors carried from the 2026-10-01 warp-drive run (RE-25 to RE-33).
Access: lit_search INSPIRE ok, arXiv rate-limited (HTTP 429) on several queries, Semantic Scholar rate-limited (HTTP 429) on the second pass, Crossref ok; fetch_text worked on arxiv.org PDFs, nasa.gov, nature.com abstract pages (body paywalled; arxiv.org/pdf/2102.01064 returned HTTP 406); find_fulltext opened Vahlbruch (arXiv) and Lough (APS, cc-by); MDPI Physics 2, 1 (Avino), EPJ Web Conf. 319 09003 (Mangano) and Springer not openable (403 / SSL); WebSearch ok

## Claims

- [RE-01] CLAIM: The 2022 Google Sycamore "wormhole" experiment (Jafferis et al., Nature 612, 51) ran a teleportation protocol using a learned, sparsified SYK-like Hamiltonian realised with 164 two-qubit gates on a nine-qubit circuit. It is a quantum-information simulation of a 2D (AdS2/JT) dual; no spacetime region was created, and the authors describe it as "a step towards a program for studying quantum gravity in the laboratory".
  SOURCE: Jafferis et al. 2022, Traversable wormhole dynamics on a quantum processor, Nature 612, 51-55, https://www.nature.com/articles/s41586-022-05424-3
  QUOTE: "Here we use learning techniques to construct a sparsified SYK model that we experimentally realize with 164 two-qubit gates on a nine-qubit circuit and observe the corresponding traversable wormhole dynamics." ; "By interrogating a two-dimensional gravity dual system, our work represents a step towards a program for studying quantum gravity in the laboratory."
  ACCESS: full-text (abstract page, paywalled body)
  STATUS: peer-reviewed (an Author Correction published 4 Apr 2025 and a Matters Arising published 23 Jul 2025 are listed on the page)
  CONFIDENCE: high

- [RE-02] CLAIM: The Nature paper lists five "key properties of traversable wormhole physics" it tests: perfect size winding, coupling on either side consistent with a negative-energy shockwave, a Shapiro time delay, causal time-order of signals emerging from the wormhole, and scrambling/thermalization dynamics. The experiment was run on the Google Sycamore processor.
  SOURCE: same as RE-01
  QUOTE: "the sparsified SYK model preserves key properties of the traversable wormhole physics: perfect size winding, coupling on either side of the wormhole that is consistent with a negative energy shockwave, a Shapiro time delay, causal time-order of signals emerging from the wormhole, and scrambling and thermalization dynamics."
  ACCESS: full-text (abstract)
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RE-03] CLAIM: Kobrin, Schuster & Yao (2023, arXiv preprint) argue the learned Hamiltonian is seven Majorana fermions with five mutually commuting terms, does not thermalise, reproduces SYK teleportation only for the two operators used in training, and that perfect size winding is generic for small fully commuting models. Hence the gravitational interpretation is not supported.
  SOURCE: Kobrin, Schuster, Yao 2023, Comment on "Traversable wormhole dynamics on a quantum processor", arXiv:2302.07897, https://arxiv.org/pdf/2302.07897
  QUOTE: "We find: (i) in contrast to these claims, the learned Hamiltonian does not exhibit thermalization; (ii) the teleportation signal only resembles the SYK model for operators that were used in the machine-learning training; (iii) the observed perfect size winding is in fact a generic feature of small-size, fully-commuting models, and does not appear to persist in larger-size fully-commuting models or in non-commuting models at"
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RE-04] CLAIM: Jafferis et al.'s reply (arXiv:2303.15423) says the Kobrin et al. comment agrees on two key points (size winding is the microscopic mechanism; the system thermalises and scrambles at teleportation time) and that the objections concern "counterfactual scenarios outside of the experiment"; they argue all fermions show size winding at 2 <~ t <~ 5 (in SYK units) and that adding a large non-commuting term preserves size winding.
  SOURCE: Jafferis et al. 2023, Comment on "Comment on ...", arXiv:2303.15423, https://arxiv.org/pdf/2303.15423
  QUOTE: "We observe that the comment of Kobrin et al. [1] is consistent with Jafferis et al. [2] on key points: i) the microscopic mechanism of the experimentally observed teleportation is size winding and ii) the system thermalizes and scrambles at the time of teleportation."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RE-05] CLAIM: Nature published (23 Jul 2025, Nature 643, E17-E19) the Kobrin-Schuster-Yao Matters Arising, so the critique is now peer-reviewed-published as a Matters Arising: the Hamiltonian in Jafferis et al. does not satisfy two stated criteria for gravitational physics (it does not thermalise; the teleportation signal does not resemble wormhole behaviour), and perfect size winding appears only because the Hamiltonian is fully commuting. (Whether the authors' published reply appears alongside was not confirmed.)
  SOURCE: Kobrin, Schuster, Yao 2025, Experiments implementing small commuting models lack gravitational features, Nature 643, E17-E19, https://www.nature.com/articles/s41586-025-08939-7
  QUOTE: "ria for gravitational physics: it does not thermalize and the teleportation signal does not resemble traversable wormhole behaviour. Moreover, a third feature of gravitational systems—perfect size winding—appears to be satisfied only because the Hamiltonian implemented in Jafferis et al. 4 is fully commuting, which is the exact property that leads to non-thermalizing behaviour."
  ACCESS: full-text (abstract, paywalled body)
  STATUS: peer-reviewed (Matters Arising)
  CONFIDENCE: high

- [RE-06] CLAIM: A 2026 preprint (Byun et al., arXiv:2604.10090) reports what it calls "the first quantum-hardware realization of the TW protocol driven by an explicitly chaotic Hamiltonian": N=8 chaotic binary sparse SYK, q=4, J=sqrt2, beta=3, |mu|=12, first-order Trotter, tomography on two qubits. It notes the sign convention in which mu<0 "corresponds to ANEC violation and hence to traversability" in the holographic interpretation, and that the Sycamore Hamiltonian was N=7 with five nonzero terms. It confirms that the sparsification-at-small-N concern is considered live in the field. (Preprint, no journal ref; hardware platform not checked.)
  SOURCE: Byun et al. 2026, Quantum simulation of traversable-wormhole-inspired quantum teleportation in a chaotic binary sparse SYK model, arXiv:2604.10090, https://arxiv.org/pdf/2604.10090
  QUOTE: "To the best of our knowledge, this constitutes the first quantum-hardware realization of the TW protocol driven by an explicitly chaotic Hamiltonian."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium

- [RE-07] CLAIM: Independent (non-authors) analysis: a 2023 arXiv paper (Shapoval/Weinstein type secondary analysis) notes that Sycamore errors attenuated the teleportation signal and that the team chose the 9 least-noisy qubits of the 72-qubit chip; the circuit fidelity was already below half of the noiseless fidelity. This is a technology-readiness anchor: ~164 two-qubit gates on 9 qubits gives a measurable but noise-attenuated signal; scaling to the N>>1 limit where the semiclassical gravity picture holds is not demonstrated.
  SOURCE: "The Neverending Story of the Eternal Wormhole and the Noisy Sycamore", arXiv:2301.03522 (secondary discussion paper, quoting Jafferis et al.), https://arxiv.org/pdf/2301.03522
  QUOTE: "Circuit fidelity exponentially decays with the number of gates and qubits (and the experimentally measured fidelity was already below 1/2 of the noiseless fidelity)."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium

- [RE-08] CLAIM: Brown et al. (PRX Quantum 4, 010320, 2023) state the program: protocols "readily executed in table-top experiments" that mimic Gao-Jafferis-Wall / Maldacena-Stanford-Yang traversable wormholes: "information that is scrambled into one half of an entangled system will, following a weak coupling between the two halves, unscramble into the other half." That is, the experimentally accessible object is a teleportation protocol in an entangled non-gravitational system, a holographic analogue, not a spacetime.
  SOURCE: Brown, Gharibyan, Leichenauer, Lin, Nezami, Salton, Susskind, Swingle, Walter 2023, Quantum Gravity in the Lab. I, PRX Quantum 4, 010320, arXiv:1911.06314
  QUOTE: "we propose holographic teleportation protocols that can be readily executed in table-top experiments. These protocols exhibit similar behavior to that seen in the recent traversable-wormhole constructions of [1, 2]: information that is scrambled into one half of an entangled system will, following a weak coupling between the two halves, unscramble into the other half."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RE-09] CLAIM: Other hardware has run the same "wormhole-inspired" teleportation protocol: a 2026 preprint implements an N=8 chaotic binary sparse SYK instance on a superconducting IBM processor, with mutual information I_PT of order 0.01 (scale in its Fig. 5b, 10,000 shots per tomography circuit, 10 independent runs) and a sign-dependent asymmetry near the teleportation time; Quanta (Mar 2023) reports an earlier IBM/Quantinuum "wormhole-inspired" teleportation-by-scrambling experiment (Su et al.). Scale: all experiments so far use <= ~10 qubits, i.e. N ~ 7-8 Majorana fermions per side, far from the N >> 1 limit where the bulk gravity description is controlled.
  SOURCE: Byun et al. 2026, arXiv:2604.10090 (IBM runs); Quanta Magazine "Wormhole Experiment Called Into Question" 2023-03-23 (for the Su et al. IBM/Quantinuum run; search summary only)
  QUOTE: "We subsequently implement the corresponding TW circuit on a superconducting IBM quantum processor. The measured mutual-information dynamics exhibit a clear sign-dependent asymmetry near the teleportation time, in good qualitative agreement with exact numerics."
  ACCESS: full-text (Byun); search-summary (Quanta/Su)
  STATUS: preprint
  CONFIDENCE: medium

- [RE-10] CLAIM: SDSS Quasar Lens Search (about 50,000 quasars, 50,836 in the statistical sample) shows no multiple images attributable to negative-mass compact objects or Ellis wormholes; the bound is a number density n < 1e-4 h^3 Mpc^-3 for Ellis wormholes with throat radius a = 10-1e4 pc (search-summary for the wormhole bound), and n < 1e-8 (1e-4) h^3 Mpc^-3 for negative-mass objects with |M| > 1e15 (1e12) Msun, i.e. |Omega| < 1e-4 for |M| = 1e12-1e15 Msun. Scope: a classical Ellis/negative-mass lens with zero ADM mass; a wormhole mouth of a Maldacena-Milekhin type (extremal magnetic black-hole mouths with positive mass) is not constrained by this.
  SOURCE: Takahashi & Asada 2013, Observational upper bound on the cosmic abundances of negative-mass compact objects and Ellis wormholes from the SDSS quasar lens search, ApJ Letters 768, L16, arXiv:1303.1301
  QUOTE: "There are no multiple images lensed by the above two exotic objects for ∼ 50000 distant quasars in the SQLS data. Therefore, an upper bound is put on the cosmic abundances of these lenses. The number density of negative mass compact objects is n < 10−8(10−4)h3Mpc−3 at the mass scale |M | > 1015(1012)M⊙, which corresponds to the cosmological density parameter |Ω | < 10−4 at the galaxy and cluster mass range |M | = 10 12−15M⊙."
  ACCESS: full-text (Ellis-wormhole number n < 1e-4 h^3 Mpc^-3 for a = 10-1e4 pc is from the abstract as relayed by search summary)
  STATUS: peer-reviewed
  CONFIDENCE: high (negative mass) / medium (Ellis number)

- [RE-11] CLAIM: Abe (2010) gives the weak-field microlensing light curve of the Ellis wormhole (one image outside, one inside the Einstein ring; "gutters" of about 4% just outside Einstein-ring crossing; magnification generally less than Schwarzschild lensing). Wormholes with throat radius 100-1e7 km could be constrained or detected with Galactic microlensing (stated in Takahashi & Asada 2013 introduction); throat radii below ~1 km are very hard to detect because the finite source (~1e6 km stellar radius) smears the features. Yoo et al. 2013 (cited in Takahashi & Asada) give n <~ 1e-9 AU^-3 for throat ~1 cm from GRB femtolensing. Dedicated microlensing survey search for wormhole events: not found.
  SOURCE: Abe 2010, Gravitational microlensing by the Ellis wormhole, ApJ 725, 787, arXiv:1009.6084; Takahashi & Asada 2013 (above)
  QUOTE: "The light curves calculated have gutters of approximately 4% immediately outside the Einstein ring crossing times. The magnification of the Ellis wormhole lensing is generally less than that of Schwarzschild lensing." ; "The detection of a lens for which the Einstein radius is smaller than the star radius ( ≈ 106km) is very difficult because most of the features of the gravitational lensing are smeared out by the finite-source effect."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RE-12] CLAIM: Dai & Stojkovic (2019) propose a gravitational test: if Sgr A* were a traversable wormhole, a star orbiting on the far side would perturb S2's orbit. With acceleration precision 1e-6 m/s^2 (SI), a few-solar-mass star on the other side at a few gravitational radii would be detectable. S2 acceleration is 1.5 m/s^2; measured precision 4e-4 m/s^2 (2 yr data), projected 2e-5 m/s^2 with 20 yr data, 1e-6 m/s^2 only if velocity uncertainty drops to 2 km/s. The test assumes a wormhole connecting two regions with gravity propagating through the mouth (a classical Morris-Thorne-type picture). Result today: no detection; sensitivity not yet reached.
  SOURCE: Dai & Stojkovic 2019, Observing a wormhole, Phys. Rev. D 100, 083513, arXiv:1910.00429
  QUOTE: "In particular, with a near future acceleration precision of 10 −6m/s 2, a few solar masses star orbiting around Sgr A* on the other side of the wormhole at the distance of a few gravitational radii would leave detectable imprint on the orbit of the S2 star on our side."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RE-13] CLAIM: Simonetti, Kavic, Minic, Stojkovic & Dai (2020/21) apply the same idea to a triple system with a non-accreting black hole: the mass limit on a far-side perturber is ~4 orders of magnitude better than from S2 at Sgr A*; a pulsar in an S2-like orbit would be ~10 orders of magnitude more sensitive than S2.
  SOURCE: Simonetti et al., A sensitive search for wormholes, arXiv:2007.12184
  QUOTE: "The mass limit obtained on the perturber is ∼ 4 orders of magnitude better than for observations of S2 orbiting the supermassive black hole at Sgr A*."
  ACCESS: full-text
  STATUS: preprint (journal ref not checked)
  CONFIDENCE: medium

- [RE-14] CLAIM: Maldacena-Milekhin (2020) "humanly traversable" wormholes: the engineering requirements as stated by the authors. (a) Tidal limit: they take a maximal sustainable acceleration of about 20 g for short durations, with a ~0.5 m size, giving throat/extremal-horizon radius r_e > 1.5e7 m (~0.05 light-seconds), i.e. a charged "intermediate mass" black-hole-like object. (b) In the massless-fermion version, they require |E_bin| > 1e3 kg (spaceship mass ~1e3 kg) and r_e > 1e7 m, giving N_f > 1e52 fermion species, "too large", which motivates the Randall-Sundrum II (extra-dimension, speculative) version. (c) Transit: under a second of traveller proper time between distant points of the galaxy but "tens of thousands of years for somebody looking from the outside", so it is NOT a shortcut as seen from outside; very large boost gamma at the centre. (d) Practical problems: a CMB photon falling in is boosted by gamma and seen with gamma^2 by the traveller, so the black hole would need to be in "a refrigerator"; the wormhole must exist in cold, flat ambient space "much colder than the present universe"; and the authors "have not given any plausible mechanism for their formation". Also "the wormhole" is built from two oppositely charged (magnetic) extremal black-hole mouths that must be kept from attracting each other (rotation/orbit), i.e. an extra engineering requirement.
  SOURCE: Maldacena & Milekhin 2020/2021, Humanly traversable wormholes, arXiv:2008.06618 (Phys. Rev. D 103, 066007)
  QUOTE: "Using them, one could travel in less than a second between distant points in our galaxy. A second for the observer that goes through the wormhole. It would be tens of thousands of years for somebody looking from the outside." ; "20g >a∼ size r2 e → re > 1.5×107m∼.05s" ; "So one would have to put the huge black hole inside a refrigerator in order to prevent this." ; "We have not given any plausible mechanism for their formation. We have only argued that they are configurations allowed by the equations."
  ACCESS: full-text
  STATUS: peer-reviewed (PRD); contains speculative ingredients (RS II extra dimension, 1e52 species or dark-sector/monopole charges)
  CONFIDENCE: high

- [RE-15] CLAIM: Derived scale for the Maldacena-Milekhin humanly traversable wormhole (my calculation from the paper's r_e > 1.5e7 m, assuming each mouth obeys the extremal Reissner-Nordstrom relation r_e = GM/c^2; SI): M per mouth about 2.0e34 kg (about 1.0e4 solar masses); rest energy of the two mouths about 3.6e51 J; magnetic charge about 1.6e41 Dirac charges per mouth; surface magnetic field about 2.3e11 T at r_e (magnetar-surface scale). Light-crossing time of r_e is 0.05 s. For contrast, the heaviest single monopole excluded at colliders is a few TeV (~1e-23 kg), a mass gap of order 1e57 per quantum, and no macroscopic magnetic charge has ever been detected (RE-19). The extremal-RN mapping is my assumption; the paper says the mouths have "up to a small correction" the same mass and charge as extremal black holes.
  SOURCE: [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/engineering_mm_scale.py], with the input r_e from Maldacena & Milekhin arXiv:2008.06618 eq. (3.26)
  SUMMARY: "Computed, see script output: r_e=1.5e7 m gives M=2.02e34 kg=1.02e4 Msun per mouth; g/g_D=1.6e41; B(r_e)=2.3e11 T."
  ACCESS: full-text (input) plus calculation
  STATUS: calculation
  CONFIDENCE: medium

- [RE-16] CLAIM: Maldacena-Milekhin-Popov (2018, Traversable wormholes in four dimensions, arXiv:1807.04726) is a pair of entangled near-extremal magnetically charged black holes whose Casimir-type negative energy from massless charged fermions supports the wormhole. Embedding in the Standard Model requires the mouth separation d, and hence r_e, to be below the electroweak scale (the authors write "say 1/TeV", i.e. about 2e-19 m), with Standard Model fermions acting like N_f = 54 charge-one flavours. Transit: traveller proper time of order the light-crossing time r_E ~ q, much shorter than the outside time pi*l ~ q^2, so it is a long wormhole, not a shortcut as seen from outside. Implication: a Standard-Model realisation is sub-electroweak in size, so far too small for any payload but possibly a single particle or qubit (not demonstrated).
  SOURCE: Maldacena, Milekhin, Popov, arXiv:1807.04726 (v3, Nov 2020), https://arxiv.org/pdf/1807.04726
  QUOTE: "It is a long wormhole that does not lead to causality violations in the ambient space. It can be viewed as a pair of entangled near extremal black holes with an interaction term generated by the exchange of fermion fields. The solution can be embedded in the Standard Model by making its overall size small compared to the electroweak scale." ; "the proper time that it takes for an observer to go through the wormhole is of order the light crossing time of the black hole, or rE∼q. This is much smaller than the time it takes to go through the wormhole as seen from the outside, which is π𝓁∝q2."
  ACCESS: full-text
  STATUS: peer-reviewed (published version not checked)
  CONFIDENCE: high

- [RE-17] CLAIM: Blazquez-Salcedo, Knoll, Radu (PRL 126, 101102, 2021) build asymptotically flat traversable wormholes in Einstein-Dirac-Maxwell theory with two gauged fermions treated as classical spinor wave functions (semiclassical; no Casimir term). All solutions found have Q_e/M > 1 (charge exceeds mass), the family is scale-invariant under (M,Q_e) -> lambda (M,Q_e) with a "one particle condition" Q_N = 1 per spinor, so physical size is set by the fermion mass in Planck units. No creation mechanism, payload analysis or dynamical stability analysis appears in the paper; I did not compute the physical throat size for an electron-like fermion.
  SOURCE: Blazquez-Salcedo, Knoll, Radu 2021, Traversable wormholes in Einstein-Dirac-Maxwell theory, PRL 126, 101102, arXiv:2010.07317
  QUOTE: "A semiclassical approach has been used, in which case the Dirac-Maxwell and Einstein equations are coupled, the fermionic matter being treated as a quantum wave function, a treatment which may provide a reasonable approximation under certain conditions" ; "Also, we have found that all solutions constructed so far have Qe/M > 1 and q/µ < 1."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RE-18] CLAIM: Konoplya & Zhidenko (PRL 128, 091104, 2022) note the mirror-symmetric BKR solutions are non-smooth at the throat, a configuration that "could not exist in nature", and show asymmetric smooth EDM wormholes. They also state that wormholes have never been observed and that formation scenarios are disputable.
  SOURCE: Konoplya & Zhidenko 2022, Traversable wormholes in General Relativity, PRL 128, 091104, arXiv:2106.05034
  QUOTE: "The normalizable numerical solutions found therein require a peculiar behavior at the throat: the mirror symmetry relatively the throat leads to the nonsmoothness of gravitational and matter fields." ; "Wormholes have never been observed and even their existence and formation scenarios are highly disputable questions."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RE-19] CLAIM: MoEDAL's first Schwinger-mechanism monopole search (ultraperipheral Pb-Pb at 5.02 TeV per nucleon, 0.235 nb^-1, Nov 2018; SQUID scan of trapping detectors) found no signal and excluded monopoles with 1 g_D <= g <= 3 g_D and masses up to 75 GeV/c^2. No magnetic charge or magnetic black hole has been detected at any scale. Later MoEDAL mass limits up to about 3.9 TeV for 1-10 g_D (search summary only).
  SOURCE: MoEDAL Collaboration, Search for magnetic monopoles produced via the Schwinger mechanism, Nature 602, 63 (2022), arXiv:2106.11933
  QUOTE: "MMs with Dirac charges 1gD≤g≤ 3gD and masses up to 75 GeV/c2 were excluded by the analysis. This provides the first lower mass limit for finite-size MMs from a collider search and significantly extends previous mass bounds."
  ACCESS: full-text (75 GeV); search-summary (3.9 TeV)
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RE-20] CLAIM: Gravitational-wave echo searches (probes of horizonless compact objects, including a wormhole model) in LIGO-Virgo-KAGRA O3 events found no significant echoes; earlier O1 claims (Abedi-Dykaar-Afshordi, about 2.5 sigma by search summary) were disputed. Scope: model-dependent probes of a reflective surface or wormhole-like cavity near a merger remnant; they do not test Maldacena-Milekhin-type mouths, which look like extremal black holes from outside.
  SOURCE: Search for GW echoes in O3 LIGO-Virgo-KAGRA events, arXiv:2309.01894; Cardoso, Hopper, Macedo, Palenzuela, Pani, Echoes of ECOs, arXiv:1608.08637
  QUOTE: "Our results show that the distributions of p-values for all events analyzed in this study are consistent with the noise distribution. This means that no significant echo signals are found for both models from O3 events."
  ACCESS: full-text
  STATUS: preprint (journal ref for 2309.01894 not checked)
  CONFIDENCE: medium

- [RE-21] CLAIM: EHT Sgr A*: the observed image size is within about 10% of Kerr predictions, with inferred shadow diameters near 47-50 microarcsec (Table 1 of the paper); shadow size alone constrains deviations from Kerr only at about 10%, so Ellis-Bronnikov-type wormhole shadows are not excluded by size alone (the last point is search-summary). Horizonless surfaces at 2M-8M are excluded by infrared luminosity; this does not apply to a wormhole whose far side is a separate region.
  SOURCE: EHT Collaboration 2022, First Sagittarius A* EHT Results VI, ApJL 930, L17, arXiv:2311.09484
  QUOTE: "We use the exquisite prior constraints on the mass-to-distance ratio for Sgr A∗ to show that the observed image size is within∼ 10% of the Kerr predictions."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RE-22] CLAIM: Laboratory negative energy: squeezed-vacuum states have negative normal-ordered energy density relative to the free vacuum in quantum optics, and have been produced with large squeezing (search summary: variance reduction to about -15 dB over three decades), but no quantum energy inequality has been experimentally tested in the usual sense. Maclay & Davis (Foundations of Physics, 2019; authors with a propulsion-physics orientation, not mainstream QEI community) claim a meta-analysis of published squeezed-light data conflicts with a squeezed-light quantum inequality; this is contested and secondary evidence only. The magnitude is the engineering point: squeezed-light negative energy densities are microscopic (the search summary says "too small to be directly measurable"), versus the order 1e44 J (Jupiter-mass-equivalent) scale usually quoted for a metre-sized Morris-Thorne throat (the Jupiter figure is a lead from the brief, not verified here).
  SOURCE: Maclay & Davis 2019, Testing a Quantum Inequality with a Meta-analysis of Data for Squeezed Light, Found. Phys., arXiv:1806.01269; search summary for the 15 dB and "too small to be directly measurable" statements
  QUOTE: "In quantum field theory, coherent states can be created that have negative energy density, meaning it is below that of empty space, the free quantum vacuum." ; "This paper is the first attempt to bridge this gap and test a quantum inequality with published experimental data."
  ACCESS: full-text (the two quotes); search-summary (15 dB, direct measurability)
  STATUS: peer-reviewed (Foundations of Physics) but contested; treat the QI-violation claim as low confidence
  CONFIDENCE: low

- [RE-23] CLAIM: Casimir-energy engineering anchor: the Casimir force between a metal sphere and flat plate has been measured by atomic force microscope at the percent level (Mohideen & Roy 1998, 1.6 pN rms deviation, ~1% at the smallest separation, by search summary), with improved precision measured by Roy, Lin & Mohideen (1999, Al-coated sphere and plate, smoother coatings, reduced noise). This shows ordinary-quantum-field negative energy density is real and measurable between plates at sub-micron separations; it is not demonstrated on a scale (throat radius metres to 1e7 m) or with a geometry (flaring throat, charged fermions in a magnetic throat) relevant to MMP or MM wormholes. The throat-supporting Casimir energy of MMP is a 2D CFT effect in an AdS2 throat of massless charged fermions, i.e. no laboratory analogue exists.
  SOURCE: Roy, Lin, Mohideen 2000, Improved precision measurement of the Casimir force, Phys. Rev. D 60, 111101, arXiv:quant-ph/9906062
  QUOTE: "We report an improved precision measurement of the Casimir force. The force is measured between a large Al coated sphere and flat plate using an Atomic Force Microscope. The primary experimental improvements include the use of smoother metal coatings, reduced noise, lower systematic errors and independent measurement of surface separations."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high (measurement); medium (relevance statement is my inference)

- [RE-24] CLAIM: Technology-readiness assessment (my judgement, not from a source), by construction. Quantum-processor wormhole-inspired teleportation: TRL ~3-4 as a laboratory simulation (9-qubit circuit, 164 two-qubit gates, noise-attenuated signal, now with several hardware repeats), TRL 1 as a test of quantum gravity because the gravitational interpretation is disputed (RE-03, RE-05). Natural-wormhole astronomy (lensing, S2-orbit perturbation, EHT, echoes): observational searches at TRL 6-9 as instruments, but each is null so far and is sensitive only to classical Ellis/negative-mass or horizon-replacement models. Creating or widening any wormhole (Morris-Thorne, thin-shell, MMP, MM, EDM): TRL 0-1; no mechanism in any source I read (Maldacena-Milekhin state this explicitly; Konoplya-Zhidenko call formation scenarios "highly disputable"). Gaps to demonstrated technology: MM mouths need ~1e4 solar masses of magnetic-charged extremal black hole (RE-15), vs largest engineered mass ~1e5 kg objects, a gap of ~1e29 in mass.
  SOURCE: synthesis of RE-01, RE-03, RE-05, RE-10 to RE-15; [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/engineering_mm_scale.py]
  SUMMARY: "TRL estimates are the researcher's own judgement."
  ACCESS: search-summary (no external source for the TRL levels)
  STATUS: secondary
  CONFIDENCE: low

## Claims carried from the warp-drive run and added on 2026-10-08

- [RE-25] CLAIM: The strongest directly observed squeezed light is 15 dB below vacuum noise (Vahlbruch et al., PRL 117, 110801): measured at Fourier frequencies 3-8 MHz at 1064 nm with 16 mW of second-harmonic pump power, a detection-noise variance statement. A 15 dB variance reduction is a factor 10^-1.5 = 0.032 of the vacuum noise power. The source states a noise variance, not an energy density in J/m^3 or a spatial extent, so no negative energy density in SI units can be read from it. Squeezed vacuum is the one sub-vacuum state in routine use; correction to RE-22: its "about -15 dB over three decades" phrase (search summary) is NOT what the paper says; the paper's 15 dB is for 3-8 MHz.
  SOURCE: Vahlbruch, Mehmet, Danzmann, Schnabel 2016, Detection of 15 dB Squeezed States of Light and their Application for the Absolute Calibration of Photoelectric Quantum Efficiency, PRL 117, 110801 (arXiv:2411.07379 v2 posting of doi:10.1103/PhysRevLett.117.110801; the arXiv ID is a 2024 posting of the 2016 paper, so cite the journal DOI)
  QUOTE: "Up to 15 dB squeezing was measured with merely 16 mW of second harmonic pump power." ; "A non-classical noise reduction of up to 15 dB below vacuum noise was directly observed."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
  PRIOR: 2026-10-01-warp-drive-without-negative-energy (2026-10-01), was RE-05; re-verified

- [RE-26] CLAIM: Squeezing in a kilometre-scale gravitational-wave detector: GEO 600 reported 6.03 +/- 0.02 dB noise reduction at 6 kHz (median noise floors averaged over 6.3-6.5 kHz, over a two-month period), equivalent at high frequencies to a factor 4 in circulating laser power. This is the largest-scale (km arm, macroscopic interferometer) deployment of quantum-vacuum sub-vacuum noise, but it reduces noise variance; it does not produce a gravitating negative energy density.
  SOURCE: Lough et al. 2021, First Demonstration of 6 dB Quantum Noise Reduction in a Kilometer Scale Gravitational Wave Observatory, PRL 126, 041102, arXiv:2005.10292 (published version, cc-by)
  QUOTE: "demonstrate for the first time a reduction of quantum noise up to 6.03 6 0.02 dB in a kilometer scale interferometer. This is equivalent at high frequencies to increasing the laser power circulating in the interferometer by a factor of 4."
  ACCESS: full-text (the extraction prints the plus-minus sign as "6"; the source reads 6.03 +/- 0.02 dB)
  STATUS: peer-reviewed
  CONFIDENCE: high
  PRIOR: 2026-10-01-warp-drive-without-negative-energy (2026-10-01), was RE-05 (second half); re-verified. The earlier "all GW observatories since 2019" remark was not re-verified and is dropped.

- [RE-27] CLAIM: The dynamical Casimir effect was observed in a superconducting circuit (Wilson et al. 2011): a coplanar transmission line whose electrical length was changed "at a few percent of the speed of light" by modulating a SQUID at ~11 GHz, giving real photons and two-mode squeezing. The source does not state 0.05c; "a few percent of c" is the quotable figure. Energy scale: photons in a microwave line (single-photon level per mode), so it demonstrates moving-boundary vacuum radiation, not a bulk negative energy density.
  SOURCE: Wilson et al. 2011, Observation of the dynamical Casimir effect in a superconducting circuit, Nature 479, 376, arXiv:1105.4714
  QUOTE: "The circuit consists of a coplanar transmission line with an electrical length that can be changed at a few percent of the speed of light. The length is changed by modulating the inductance of a superconducting quantum interference device (SQUID) at high frequencies ( ∼ 11 GHz). In addition to observing the creation of real photons, we observe two-mode squeezing of the emitted radiation"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
  PRIOR: 2026-10-01-warp-drive-without-negative-energy (2026-10-01), was RE-08; re-verified (the "~0.05c" value is not in the source and is dropped)

- [RE-28] CLAIM: Quantum energy teleportation (QET), the protocol in which local measurement on one side lets a distant side extract energy using only local operations and classical communication, has been run on IBM superconducting hardware (Ikeda 2023); results "consistent with the exact solution" after error mitigation. It is a few-qubit proof of principle and, like the Sycamore wormhole teleportation (RE-01), uses ordinary classical communication; it creates no sustained negative energy density and is not a wormhole.
  SOURCE: Ikeda 2023, Demonstration of Quantum Energy Teleportation on Superconducting Quantum Hardware, Phys. Rev. Applied 20, 024051, arXiv:2301.02666
  QUOTE: "Here we report the realization and observation of quantum energy teleportation on real superconducting quantum hardware. We achieve this by using several IBM's superconducting quantum computers. The results are consistent with the exact solution of the theory and are improved by the mitigation of measurement error." ; "Quantum energy teleportation requires only local operations and classical communication."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high (quote); medium (the few-qubit characterisation, not counted in the source text read, and the application-to-wormhole remark, which is mine)
  PRIOR: 2026-10-01-warp-drive-without-negative-energy (2026-10-01), was RE-07; re-verified

- [RE-29] CLAIM: Casimir-force measurement anchors (ordinary-quantum-field negative energy, the kind the brief's Maldacena-Milekhin-Popov mechanism is analogous to). Bressi et al. 2002 measured the force between parallel conducting surfaces over 0.5-3.0 micrometre with the coefficient determined at the 15% level (the first parallel-plate configuration measurement in the paper's own account). Decca et al. 2003 measured the force between dissimilar metals (Cu on a MEMS torsional oscillator, Au on a sphere) over 0.2-2 micrometre, noise 6 fN per root-Hz as printed in the abstract, agreement with theory better than 1% as printed. Sphere-plate measurements at the percent level exist (RE-23, Mohideen-Roy search summary). So the laboratory Casimir force is measured at 1-15% from 0.2 to 3 micrometre; nothing is measured at a throat-relevant scale.
  SOURCE: Bressi, Carugno, Onofrio, Ruoso 2002, Measurement of the Casimir force between parallel metallic surfaces, PRL 88, 041804, arXiv:quant-ph/0203002; Decca et al. 2003, Measurement of the Casimir Force between Dissimilar Metals, PRL 91, 050402, arXiv:quant-ph/0306136 (abstract via INSPIRE)
  QUOTE: "The scaling of the force with the distance between the surfaces was tested in the 0.5 - 3.0 µ m range, and the related force coefficient was determined at the 15% precision level." (Bressi) ; "The attractive force, between a Cu layer evaporated on a microelectromechanical torsional oscillator and an Au layer deposited on an Al2O3 sphere, was measured dynamically with a noise level of 6 fN/Hz. Measurements were performed for separations in the 0.2–2 μm range." (Decca abstract)
  ACCESS: full-text (Bressi); abstract (Decca)
  STATUS: peer-reviewed
  CONFIDENCE: high
  PRIOR: new this pass (the warp-drive notes held no Casimir force numbers; only the Archimedes design signal, RE-31)

- [RE-30] CLAIM: Orders-of-magnitude gap between laboratory Casimir negative energy and a Morris-Thorne throat (my calculation, SI, ideal perfect-conductor parallel plates at zero temperature; real metals give tens of percent less at 0.5 micrometre). Casimir pressure P = pi^2 hbar c/(240 d^4): 1.30e5 Pa at d = 10 nm, 0.0208 Pa at 500 nm, 1.30e-3 Pa at 1 micrometre; energy density u = -pi^2 hbar c/(720 d^4) = -4.3e4 J/m^3 at 10 nm and -4.3e-4 J/m^3 at 1 micrometre. Morris-Thorne radial tension at the throat tau0 = c^4/(8 pi G r0^2) = 4.8e40 Pa for r0 = 10 m and 4.8e36 Pa for r0 = 1 km, which is 3.7e37 (b0 = 1 m) and 3.7e31 (b0 = 1 km) times the ideal Casimir pressure at 10 nm (a reference value, far below the gaps measured in RE-29; at the smallest measured gap, 0.2 micrometre, the ideal pressure is 1.3e-3 Pa x (1/0.2)^4 = 0.81 Pa by scaling the 1 micrometre row, so the measured-regime gap is about 6e42 for b0 = 1 m: 4.8e42 Pa / 0.81 Pa). Effective gravitating mass scale of the throat b0 c^2/(2G): 6.7e26 kg = 0.355 Jupiter masses for b0 = 1 m (so the "about a Jupiter mass for a 1 m throat" lead is right in order of magnitude as a mass-function scale, 6.1e43 J), 6.7e29 kg for b0 = 1 km. Casimir energy of that size at 1 micrometre gap would need a cavity volume of 1.4e47 m^3, a cube of side 5.2e15 m (about 35,000 AU; Earth volume 1.08e21 m^3), so not a route to a metre-scale throat.
  SOURCE: [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/engineering_casimir_anchors.py]; tension formula checked against Kuhfittig, A survey of recent studies concerning the extreme properties of Morris-Thorne wormholes, arXiv:2202.07431
  QUOTE: "τ(r0) = 1 8πGc −4r2 0 ≈ 5 × 1041 dyn cm2 ( 10 m r0 ) 2 . (9) In particular, for r0 = 3 km, τ(r) has the same magnitude as the pressure at the center of a massive neutron star" (Kuhfittig; the extraction scrambles the formula, which reads tau(r0) = c^4/(8 pi G r0^2); 5e41 dyn/cm^2 = 5e40 Pa, matching my 4.8e40 Pa at 10 m)
  ACCESS: full-text (Kuhfittig for the tension); calculation for the rest. The Casimir formulas are the textbook ideal results and are not quoted from a source here.
  STATUS: calculation (tension cross-checked against a preprint survey, journal reference not checked)
  CONFIDENCE: medium (the effective-mass scale b0 c^2/(2G) is an order-of-magnitude reading of the Morris-Thorne mass function, not the exotic-matter amount, which depends on the shape function)
  PRIOR: new this pass; the "Jupiter mass for a 1 m throat" lead from the brief is now checked as an order of magnitude only

- [RE-31] CLAIM: Archimedes (INFN-led, Sos Enattos mine, Sardinia) plans to weigh vacuum fluctuations in layered high-Tc superconductors with a cryogenic balance, to test whether Casimir-type vacuum energy gravitates. Status as of the latest abstracts located (2025): construction and R&D, no vacuum-weight result; only a room-temperature, thermal-noise-limited 50 cm prototype balance has been reported. The design force modulation of 5e-16 N with ~4e6 s (about two months) integration and torque ASD 7e-13 N/sqrt(Hz) came from the earlier run's reading of the 2020 Physics paper; I could not reopen that paper (MDPI 403, repository SSL error), so those numbers are NOT re-verified. Relevance to wormholes: the MMP and Maldacena-Milekhin supports are Casimir-like quantum-field energy, so whether such energy sources gravity at all is an input to Q2; Archimedes would test it for a condensed-matter Casimir term only, at a force 1e-15 N scale.
  SOURCE: Allocca et al. 2025, Weighing the vacuum with the Archimedes experiment, Int. J. Mod. Phys. A 40, 2443028, doi:10.1142/S0217751X24430280 (abstract via INSPIRE); Mangano et al. 2025, EPJ Web Conf. 319, 09003, doi:10.1051/epjconf/202531909003 (title and abstract via INSPIRE)
  QUOTE: "Tiny changes in the weight of the vacuum contained in high-temperature superconductors can be measured using a high-precision balance." ; "This will be possible thanks to a high sensitivity and cryogenic balance installed in the SarGrav laboratory in the Sos Enattos mine (Sardinia), the Italian candidate site for the third generation gravitational wave observatory Einstein Telescope."
  ACCESS: abstract
  STATUS: peer-reviewed (conference/proceedings)
  CONFIDENCE: medium for status; the numeric design signal is not re-verified
  PRIOR: 2026-10-01-warp-drive-without-negative-energy (2026-10-01), was RE-04 and RE-19; status re-verified at abstract level, numbers not re-verified

- [RE-32] CLAIM: Demonstrated-capability anchor for speeds: NASA's Parker Solar Probe reached 430,000 miles per hour on 24 Dec 2024, "faster than any human-made object has ever moved": 192.2 km/s = 6.41e-4 c (my conversion, SI), carried by a roughly 600 kg spacecraft. Relevance to wormholes: the Morris-Thorne-Yurtsever time-machine conversion requires mouth motion at relativistic speed, so the gap to a relativistic mouth (v of order 0.1-1 c) is 2-3 orders of magnitude in speed, but the mouth mass is the binding constraint (RE-30), not its speed.
  SOURCE: NASA Science, NASA's Parker Solar Probe Makes History With Closest Pass to Sun, https://science.nasa.gov/science-research/heliophysics/nasas-parker-solar-probe-makes-history-with-closest-pass-to-sun/
  QUOTE: "hurtled through the solar atmosphere at a blazing 430,000 miles per hour — faster than any human-made object has ever moved."
  ACCESS: full-text
  STATUS: secondary
  CONFIDENCE: high
  PRIOR: 2026-10-01-warp-drive-without-negative-energy (2026-10-01), was RE-11; re-verified (the 6.41e-4 c conversion is in the new script)

- [RE-33] CLAIM: Maclay & Davis (Found. Phys. 49, 797, 2019) report that a quantum inequality adapted to squeezed light "is violated by most of the experimental data" while the data fit an optical-parametric-amplifier model. Single group; the inequality is a quantum-optics-adapted form, not the Fewster-Eveson free-field bound; I found no rebuttal and no replication in two lit_search passes (one with --since 2019 returned nothing relevant). Treat as unreplicated and not evidence that quantum inequalities fail; no laboratory test of a QEI of the type used in wormhole arguments (Ford-Roman) has been found.
  SOURCE: Maclay & Davis 2019, Testing a Quantum Inequality with a Meta-analysis of Data for Squeezed Light, Found. Phys. 49, 797, arXiv:1806.01269
  QUOTE: "we find that the QI as given is violated by most of the experimental data, yet all experimental data are consistent with a theoretical model of the optical parametric amplifier (OPA) used to generate squeezed light."
  ACCESS: full-text
  STATUS: peer-reviewed, unreplicated
  CONFIDENCE: medium
  PRIOR: 2026-10-01-warp-drive-without-negative-energy (2026-10-01), was RE-06; re-verified. Supersedes the "low confidence" label of RE-22 for the QI statement only.

- [RE-34] CLAIM: Search for work newer than 2026-10-01 bearing on the engineering facet found no experimental result. INSPIRE with --since 2026 returned only theory preprints from October 2026, e.g. a linear-perturbation study of the Maldacena-Milekhin-Popov wormhole (arXiv:2610.09847, abstract only, no stability verdict read) and an exact NUT-charged Ellis-Bronnikov generalisation (arXiv:2610.05656). Nothing new on the Sycamore replies, Casimir tests or the Archimedes balance was found. The carried experimental claims (RE-25 to RE-33) are therefore not superseded as far as the search reaches; a PRA publication of the Byun et al. IBM run was suggested by a search result but not opened.
  SOURCE: lit_search INSPIRE --since 2026 queries "wormhole", "traversable wormhole quantum processor experiment", "Archimedes vacuum weight"
  SUMMARY: "Axial-metric/polar-gauge perturbations of the Maldacena-Milekhin-Popov wormhole ... We study linear perturbations of the Maldacena-Milekhin-Popov (MMP) wormhole in the parity sector that pairs axial metric perturbations with polar gauge perturbations." (abstract as printed, truncated)
  ACCESS: abstract
  STATUS: preprint
  CONFIDENCE: low (negative search result)

## Gaps
- Added 2026-10-08: no source gives the squeezed-light negative energy density in J/m^3 or its extent, so no gap to a throat can be put in numbers for squeezed light (the Casimir gap in RE-30 is the only computed one). No QEI/QNEC/ANEC laboratory test beyond the Maclay-Davis meta-analysis was found. PAPER TO REQUEST: 10.3390/physics2010001 | Progress in a Vacuum Weight Search Experiment | to re-verify the 5e-16 N design force and 4e6 s integration time. PAPER TO REQUEST: 10.1051/epjconf/202531909003 | Exploring Vacuum-Gravity Interaction through the Archimedes Experiment: Recent Results and Future Prospects | current Archimedes sensitivity and schedule.
- Correction to RE-24: its "largest engineered mass ~1e5 kg" anchor is unsourced; read the mass gap for Maldacena-Milekhin mouths (2.0e34 kg each, RE-15) as at least ~26 orders above any engineered object (1e8 kg ships are the unsourced upper end), and use the Parker speed anchor (RE-32) only for speed.
- Nature paper body is paywalled: could not quote the fidelity values, the sign-dependent asymmetry magnitude or the claimed Shapiro-delay numbers; only the abstract is quoted. The authors' reply to the 2025 Matters Arising was not found.
- Whether the Quantinuum/IBM "wormhole-inspired" experiment of Su et al. exists as a peer-reviewed paper was not confirmed; only a Quanta search summary.
- Brown et al. Quantum Gravity in the Lab II (arXiv:2102.01064): fetch returned HTTP 406; only the INSPIRE abstract was read.
- Searches for Ellis-wormhole events in actual microlensing survey data (OGLE/MOA/EROS) and the Cramer et al. 1995 negative-mass lens predictions: not located; Cardoso-Franzin-Pani journal reference not verified; Abedi et al. echo claim only via search summary; Yoo et al. 2013 femtolensing bound only as cited in Takahashi & Asada.
- No experiment or observation found that targets Maldacena-Milekhin-type extremal magnetic mouths; no published sensitivity for magnetic black-hole searches (Parker bounds, MACRO, IceCube) was retrieved.
- Quantum-energy-inequality tests with squeezed light and the mainstream response to Maclay & Davis not found; QNEC/ANEC laboratory analogues not searched.
- Creation mechanisms: Garfinkle-Strominger pair creation of magnetic black holes (via topology change) is only a search-summary item; no rate or lab pathway retrieved.
- Physical size of the EDM wormholes for electron-like fermions not computed (the paper's scale-invariant family fixes it only in Planck units).
- No source found that states the energy needed to pass a 1 kg or 70 kg payload through a given throat; the Jupiter-mass figure for a 1 m throat is unverified here.
