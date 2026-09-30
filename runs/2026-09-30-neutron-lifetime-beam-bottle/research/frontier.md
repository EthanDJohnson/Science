# Research: frontier
status: final
Mandate: newest material (2024-2026) on the neutron lifetime puzzle: preprints, talks, updates, errata, critiques, new theory; each with evidential status.
Access: lit_search INSPIRE ok (strict field parsing; several multi-word queries returned nothing), arXiv ok, Crossref ok, Semantic Scholar rate-limited (HTTP 429); WebFetch not used; WebSearch ok; fetch_text worked on arxiv.org, indico.psi.ch, inspirehep.net API; find_fulltext worked for doi:10.1103/q8jf-dc9b (OSTI accepted manuscript), no free copy for the Desai EPJA paper.

## Claims
- [RF-01] CLAIM: J-PARC 2024 (Fuwa et al., arXiv:2412.19519, submitted 27 Dec 2024) electron-counting cold-beam result is tau_n = 877.2 +- 1.7 (stat) +4.0/-3.6 (sys) s; the authors state it agrees with the bottle method and shows 2.3 sigma tension with the average of proton-counting beam experiments (10.8 s shorter). As of the INSPIRE record retrieved 2026-09-30 it carried no journal reference (preprint status; verify whether published).
  SOURCE: Fuwa et al. 2024, Improved measurements of neutron lifetime with cold neutron beam at J-PARC, arXiv:2412.19519, https://arxiv.org/pdf/2412.19519
  QUOTE: "Analysis of all acquired data yielded a neutron lifetime ofτn = 877.2 ± 1.7(stat.) +4.0 −3.6(sys.) s. This result is consistent with bottle method measurements but exhibits a 2.3 σ tension with the average value obtained from the proton-detection-based beam method."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RF-02] CLAIM: The J-PARC 2024 result is internally inconsistent across run conditions: four (gas pressure, spin-flip-chopper) configurations give 870.9 +-3.5 (100 kPa/old SFC), 868.3 +-4.0 (100 kPa/new SFC), 868.2 +-7.7 (50 kPa/old SFC) and 884.8 +-2.4 s (50 kPa/new SFC) (stat only, plus cut-position and other sys as in the table); combination gives chi2/DOF = 15.8/3 with cause undetermined. The 50 kPa/new-SFC point sits ~7 s above the others, at or above the 100 kPa points by more than 3 sigma stat.
  SOURCE: Fuwa et al. 2024, arXiv:2412.19519, Table II and text, https://arxiv.org/pdf/2412.19519
  QUOTE: "The combining average yielded χ2/DOF = 15.8/3, though the underlying cause of this deviation remains undetermined." and Table II: "100 kPa/old SFC 870.9 3.5 +1.8/-2.8 +5.5/-4.9 100 kPa/new SFC 868.3 4.0 +1.5/-2.9 +3.8/-3.2 50 kPa/old SFC 868.2 7.7 +2.7/-0.9 +4.8/-3.9 50 kPa/new SFC 884.8 2.4 +0.8/-1.3 +3.2/-3.0 Combined 877.2 1.7 +4.0/-3.6"
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RF-03] CLAIM: The dominant systematic of J-PARC 2024 is the gamma-ray/beta background from gas-scattered neutrons in the TPC; the stated remedy is the LiNA experiment with a solenoidal field around the TPC, expected to cut that background by a factor 50 (authors' projection, not yet a result).
  SOURCE: Fuwa et al. 2024, arXiv:2412.19519, https://arxiv.org/pdf/2412.19519
  QUOTE: "The primary limitation of this experiment is the γ ray background from gas-scattered neutrons in the TPC. To suppress this background, the upcoming LiNA experi- ment [51, 52] will apply a solenoidal magnetic field to the TPC. This setup is expected to reduce background events by a factor of 50."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RF-04] CLAIM: J-PARC status talk (Mishima, PSI 2025 workshop, 13 Sep 2025): the stated goal is a beam-method lifetime with ~1 s accuracy via the LiNA solenoid-TPC experiment (600 mT applied field, 50 mPa 3He in 4He:CO2 at 85:15 kPa); a first LiNA commissioning run of two weeks in Feb 2024 at J-PARC MLF BL05 took neutron-decay data for two days with and without field. Simulation says gas-induced background falls to 2% with 600 mT.
  SOURCE: Mishima, K. (J-PARC), "A new results of neutron lifetime measurement with cold neutron beam at J-PARC", PSI2025 workshop slides, https://indico.psi.ch/event/17167/contributions/57991/attachments/31516/62849/20250913_Mishima_LifetimePSI2025_upload.pdf
  QUOTE: "We aim to provide the most precise experimental neutron lifetime value for beam method as an important piece to solve the neutron lifetime puzzle • Goal: measurement with ~1 s accuracy" and "gas induced background will be reduced to 2% by applying 600 mT in comparison with no magnetic field environment"
  ACCESS: full-text
  STATUS: preliminary
  CONFIDENCE: medium
- [RF-05] CLAIM: Caylor et al. (NIST/Tulane/Indiana etc., Phys. Rev. C 112, 065501, 2025; arXiv:2506.01682) measured charge exchange of trapped protons with molecular hydrogen in a BL1-type proton trap (charge exchange does occur; detection efficiency for H2+ ions determined) and conclude that the NIST beam lifetime is unlikely to have been significantly affected. This is a check of one candidate proton-trap systematic (residual-gas proton loss), by the BL1 group itself; it also advises against thick (100 ug/cm^2) gold surface-barrier detectors because of efficiency differences.
  SOURCE: Caylor et al. 2025, Detection of molecular hydrogen in a neutron beam lifetime experiment, Phys. Rev. C 112, 065501, arXiv:2506.01682, https://arxiv.org/pdf/2506.01682
  QUOTE: "We demonstrate that charge exchange with molecular hydrogen can occur with trapped protons, and we determine the efficiency with which the molecular hydrogen ions in the trap are detected. ... We find that the result of the beam neutron lifetime performed at NIST is unlikely to have been significantly affected by charge exchange with molecular hydrogen."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RF-06] CLAIM: UCNtau (LANL magneto-gravitational trap, in situ detection) published in Phys. Rev. C 111, 045501 (2025; arXiv:2409.05560) three more years of data (2020-2022): 877.94 +-0.37 s for those runs, and an updated all-data UCNtau value of 877.82 +-0.22 (stat) +0.20/-0.17 (sys) s. This supersedes the earlier all-data value 877.75 +-0.28 +0.22/-0.16 s (Gonzalez et al., PRL 127, 162501, 2021) because it includes those data. Per-year values in the paper: 2018 877.73+-0.32, 2019 877.80+-0.50, 2020 879.39+-0.89, 2021 878.41+-0.58, 2022 876.93+-0.57 s (average over four analyses). Largest systematic: event-definition parameters, then residual uncleaned/heated UCN in the trap.
  SOURCE: Musedinovic et al. 2025, Measurement of the free neutron lifetime in a magneto-gravitational trap with in situ detection, Phys. Rev. C 111, 045501, arXiv:2409.05560, https://arxiv.org/pdf/2409.05560
  QUOTE: "We report a measured value for these runs from 2020-2022 for the neutron lifetime of 877.94±0.37 s; when all the data from UCNτ are averaged we report an updated value for the lifetime of 877.82±0.22 (statistical)+0.20-0.17 (systematic) s."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RF-07] CLAIM: PSI (Ayres et al., PRL 137, 051802, 2026; arXiv:2602.23487) dedicated high-sensitivity n -> n' search with UCN in a scanned field (5 uT < B < 109 uT) found no anomalous neutron loss; the previously claimed anomaly parameter space (Berezhiani et al.) is excluded at 95% C.L. for 99.98% of the 4 pi solid angle of the unknown mirror-field direction, with a small residual region |cos(b)|-1 < 1e-4 not excluded. Applies to the mass-degenerate n-n' model in a mirror magnetic field B'; it is a search, not a direct test of the beam-bottle gap.
  SOURCE: Ayres et al. 2026, New High-Sensitivity Search for Neutron to Mirror-Neutron Oscillations at the PSI Ultracold Neutron Source, Phys. Rev. Lett. 137, 051802, arXiv:2602.23487, https://arxiv.org/pdf/2602.23487
  QUOTE: "No evidence of anomalous neutron losses was found. Consequently, new limits for the n−n′ oscillation time constant were set. The parameter space, previously claimed for potential signals, has been excluded to 99.98 %." and "Within 99.98% of the full 4π solid angle, all previously claimed anomalies are excluded at 95% C.L. There remains a small region |cos(b)|−1<10−4 in which these anomalies are not excluded."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RF-08] CLAIM: ORNL SNS search (Gonzalez et al., Phys. Rev. D 110, 072022, 2024; arXiv:2402.15981) improves limits on n -> n' with Delta m != 0 (the model proposed as an explanation of the lifetime anomaly); its introduction quotes bottle tau_n = 878.4 +-0.5 s against beam 888.0 +-0.7 s (>4 sigma) and notes a second ~3 sigma anomaly between material-bottle (880.0 +-0.7 s) and magnetic-bottle (877.8 +-0.2 s) averages. These are the authors' own groupings (citing their refs), not independent averages.
  SOURCE: Gonzalez et al. 2024, Improved limits on n->n' transformation from the Spallation Neutron Source, Phys. Rev. D 110, 072022, arXiv:2402.15981, https://arxiv.org/pdf/2402.15981
  QUOTE: "The lifetime of UCN stored inside of a magnetic or material “bottle” has been measured as τn = 878.4± 0.5 s [37– 39, 56–60]. This value disagrees with the lifetime of τn = 888.0± 0.7 s determined by measuring neutron de- cay products in a cold neutron “beam” by> 4σ [61–63]" and "a second 3 σ anomaly exists between experiments storing UCN in material bottles ( τn = 880 .0± 0.7 s) [38, 39], and storing UCN in magnetic bottles ( τn = 877.8± 0.2 s) [58, 60]."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RF-09] CLAIM: A critique of J-PARC 2024 (Desai, Eur. Phys. J. A 62, 154, 2026; single author, not endorsed by the J-PARC collaboration) argues that the pressure dependence seen in the J-PARC configurations (large chi2, cf. RF-02) can come from small pressure-dependent detector response and background terms, which shift the extracted lifetime significantly; it says independent estimates of the pressure coefficient are of the same order as the fitted one. This bears on whether the 877.2 s central value is an artefact, and so on whether J-PARC discriminates. The paper's full text was not reachable.
  SOURCE: Desai 2026, Pressure-dependent detector effects in beam-based neutron lifetime measurements, Eur. Phys. J. A 62, 154, doi:10.1140/epja/s10050-026-01929-x (abstract via INSPIRE record 3187398)
  QUOTE: "the data exhibit relatively large $\chi ^2$ values and a noticeable dependence of the measured neutron lifetime on gas pressure. ... We show that even small pressure-dependent variations can lead to significant shifts in the extracted neutron lifetime. ... These results demonstrate that pressure-dependent detector effects provide a plausible explanation for the observed variations in gas-based beam neutron lifetime measurements, such as those performed at J-PARC."
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: low
- [RF-10] CLAIM: Space-based neutron lifetime (Lunar Prospector) re-examined by Vydula et al., Phys. Rev. C 112, 015807 (2025; arXiv:2501.18831): the choice of lunar temperature model shifts the lifetime by 28.7 +-15.5 s and the choice of composition map (20 deg and 5 deg maps) by 10.3 +-12.2 s, and accounting for these systematics raises the measured lifetime. The authors state the LP data are not competitive with laboratory results and serve as a systematics study; the earlier LP value quoted there is 887 +-14 s (Wilson et al. 2020). Space-based values therefore cannot arbitrate the 10 s gap.
  SOURCE: Vydula, Coupland, Mesick, Hardgrove 2025, Systematic uncertainties in the measurement of the neutron lifetime using the Lunar Prospector neutron spectrometer, Phys. Rev. C 112, 015807, accepted manuscript (OSTI) of doi:10.1103/q8jf-dc9b
  QUOTE: "accounting for the systematic effects increase the measured lifetime. However, the reported measurements are not competitive with the laboratory results due to large unaccounted systematics resulting from nonoptimized measurements and modeling assumptions. ... We estimate the effect on the lifetime from the choice of temperature model to be to be 28.7 ± 15.5 s, and choice of compositional map (for 20 ◦ and 5◦ maps) to be 10.3 ± 12.2 s."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RF-11] CLAIM: Nab (SNS/ORNL) status as of Nov 2025: commissioning data from 2023 gave the first full Dalitz-plot of neutron beta decay (Phys. Rev. C 113, 035501, 2026, per a search summary) and new limits on a hypothesised excited neutron state proposed to explain the beam-bottle discrepancy; detector upgrades were then made for precision data taking. No a (and hence lambda) result was found in this search. Nab's goal is Delta a/a = 1e-3. The same proceedings restate the lambda conflict: -1.27641 +-0.00056 (beta asymmetry) versus -1.2668 +-0.0027 (electron-neutrino correlation), about 3 sigma apart.
  SOURCE: Broussard et al. 2025, From Commissioning to Precision Data-Taking: Resolving Operational Challenges in the Nab Detector Systems, EPJ Web Conf. 378, 04001, arXiv:2511.16678, https://arxiv.org/pdf/2511.16678
  QUOTE: "The most precise determinations of λ=−1.27641±0.00056 [3] from the beta-asymmetry andλ=−1.2668±0.0027 [4] from the electron-neutrino correlation disagree by about 3σ." and "Recent upgrades to the Nab detector system have improved the robustness and stability of the detector performance in terms of proton detection efficiency, noise performance, and detector segment availability, setting the stage for high precision physics data-taking."
  ACCESS: full-text
  STATUS: preliminary
  CONFIDENCE: medium
  (The Dalitz-plot publication detail is ACCESS: search-summary. SUMMARY: "The first full Dalitz plot measurement in neutron β decay using the Nab spectrometer was published in Physical Review C 113, 035501 (2026)".)
- [RF-12] CLAIM: Dark-decay theory update (Bastero-Gil et al., Phys. Rev. D 110, 083003, 2024; arXiv:2403.08666), speculative and model-dependent: a dark fermion chi (m_chi ~ 1 GeV) with light scalar phi (m_phi ~ O(MeV)) gives the ~1% branching ratio and a thermal-relic DM candidate; dark self-interactions via phi plus an effective repulsive chi-neutron interaction from scalar-Higgs coupling would allow heavy enough neutron stars. Combined constraints restrict 2 m_e < m_phi < 2 m_e + 0.0375 MeV. This shows the neutron-star bound is evaded, not killed, in a specific model.
  SOURCE: Bastero-Gil et al. 2024, Neutron decay anomaly, neutron stars, and dark matter, Phys. Rev. D 110, 083003 (abstract via INSPIRE record 2768400)
  QUOTE: "the combined effect of the dark matter self-interactions mediated by the light scalar and an effective repulsive interaction with the neutrons induced by the scalar-Higgs coupling would allow heavy enough neutron stars. Combining the constraints from neutron lifetime, dark matter abundance, neutron stars, Higgs physics, and big bang nucleosynthesis, we can restrict the light scalar mass to the range 2 m e < m ϕ < 2 m e + 0.0375 MeV."
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: medium
- [RF-13] CLAIM: Harris et al. (Phys. Rev. D 113, 103033, 2026; arXiv:2509.25838) find the in-medium neutron dark-decay rate (n -> chi + phi, vacuum BR of 1% or less) in neutron-star matter is quite slow, lowering the Urca bulk viscosity by at most a factor 2-3; a new (merger-signature) probe rather than a new exclusion of the lifetime-anomaly model.
  SOURCE: Harris et al. 2026, Bulk viscosity from neutron decays to dark baryons in neutron star matter, Phys. Rev. D 113, 103033 (abstract via INSPIRE record 2983528)
  QUOTE: "We find that the neutron dark decay rate in medium is quite slow, and thus the dark baryons modify the dense matter equation of state in a way that decreases the Urca bulk viscosity by, at most, a factor of 2–3."
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: medium
- [RF-14] CLAIM: Commentary on the status of the beam method in the Lunar Prospector paper states that a more precise beam result with <1 s uncertainty is expected "in the next few years" (citing its ref [5]; the facility is not named in the quoted passage, presumably BL2/BL3 at NIST, not verified). No BL2 or BL3 lifetime result was found in this search (2024-2026).
  SOURCE: Vydula et al. 2025, accepted manuscript (OSTI) of doi:10.1103/q8jf-dc9b
  QUOTE: "Further, a more precise value is ex- pected with <1 s of uncertainty in the next few years [ 5]."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: low

## Gaps
- No BL2 or BL3 (NIST) lifetime result, status talk or preprint for 2024-2026 was found; only the BL2-apparatus hydrogen study (RF-05). A targeted search of the APS/CIPANP/PSI2025 indico lists may find one.
- No published journal version of J-PARC 2024 (arXiv:2412.19519) was confirmed; INSPIRE showed no journal reference on 2026-09-30. Mishima's CKM2025 slides (https://indico.cern.ch/event/1440982/contributions/6591707/attachments/3136283/5565097/Mishima_CKM2025.pdf) and the PSI2025 talk (beyond the LiNA slides, RF-04) were not read in full; they may give an updated analysis or error budget. J-PARC proceedings: Tanida et al., Proc. 4th J-PARC Symposium 2024, doi:10.7566/jpscp.45.011083 (not opened).
- The lit_search tool returned nothing for several queries on Delta R^V, Vud superallowed updates, PDG 2025 neutron lifetime average, tau-SPECT, PENeLOPE, HOPE, Gravitrap upgrades and aCORN/PERKEO III lambda updates, so no 2024-2026 claim on those was written (left to quantitative and engineering facets). A lattice first-row unitarity proceedings (R. Merino 2026, Acta Phys. Pol. B Proc. Suppl. 19, doi:10.5506/aphyspolbsupp.19.4-a15) states a first-row deficit persists, but only an abstract stub was seen.
- Not opened: Gardner 2025 (PoS QCHSC24 223), pulsar-timing limits on neutron-star energy loss from neutron dark decay; Sombillo et al. 2026 (PoS HADRON2025 258).
- Excluded as fringe/non-physics-community: SSRN and journal items on "MMA-DMF", "Relational Field Theory", Oks 2025, Adams 2025, Balevsky 2026, Zevatskiy 2025 (STATUS: fringe; unreplicated or no data).
- PAPER TO REQUEST: doi:10.1140/epja/s10050-026-01929-x | Pressure-dependent detector effects in beam-based neutron lifetime measurements (Desai, EPJA 2026) | whether the pressure coefficient is quantitatively large enough to move J-PARC 877.2 s by several seconds (and in which direction).
