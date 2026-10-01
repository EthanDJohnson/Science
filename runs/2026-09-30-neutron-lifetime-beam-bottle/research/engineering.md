# Research: engineering
status: final
Mandate: the neutron-lifetime measurements method by method (value, stat/sys as quoted, largest systematics, blinding, in-situ tests, supersession and shared apparatus) and the planned or running lifetime experiments (who, target precision, timing).
Access: lit_search INSPIRE ok (several plain-word queries returned nothing), arXiv ok via fetch_text; Semantic Scholar rate-limited; Springer and PMC blocked (bot check); WebFetch domains that worked: indico.psi.ch (overview only; book-of-abstracts PDF read through fetch_text)

## Claims
- [RE-01] CLAIM: J-PARC 2024 electron-counting beam (Fuwa et al., arXiv:2412.19519): tau_n = 877.2 +/- 1.7 (stat) +4.0/-3.6 (sys) s. It is a fivefold precision improvement over J-PARC 2020 (898 +/- 10 (stat) +15/-18 (sys) s), and the new run SUPERSEDES the 2020 number (same apparatus, improved beam transport and lower TPC gas pressure; J-PARC 2020 = Hirota et al., PTEP 2020, 123C02). Neutron lifetime is from the ratio of decay-electron counts to 3He(n,p)3H counts in the same TPC gas (detection efficiencies from Geant4 MC). The authors quote 2.3 sigma tension with the proton-counting beam average and consistency with the bottle average (878.4 +/- 0.5 s as they quote it).
  SOURCE: Fuwa et al. (J-PARC NOP collaboration), 2024, arXiv:2412.19519 [nucl-ex], https://arxiv.org/pdf/2412.19519
  QUOTE: "Analysis of all acquired data yielded a neutron lifetime ofτn = 877.2 ± 1.7(stat.) +4.0 −3.6(sys.) s. This result is consistent with bottle method measurements but exhibits a 2.3 σ tension with the average value obtained from the proto..." ; "Our first result in 2020, τn = 898 ± 10(stat.) +15 −18 (sys.) s [32], was consis- tent with both beam and bottle methods."
  ACCESS: full-text
  STATUS: preprint (check journal version in a later claim)
  CONFIDENCE: high
- [RE-02] CLAIM: J-PARC 2024 systematic budget as tabulated (seconds): statistic 1.7; cut position 0.9; gas-induced background +1.1/-2.0; pile up +1.5/-0.6; 12C(n,gamma)13C contamination +1.7/-0.0; gamma-ray scattering at LiF shutter 1.3; unbunched neutron from SFC +1.1/-1.0; inject 3He 1.2; 3He in G1He +1.5/-1.4; 3He(n,p)3H cross section 1.2; total systematic +4.0/-3.6 s. The largest items are the 12C(n,gamma)13C and pile-up (upper side), gas-induced background (lower side), and 3He amount in the G1He gas. The 3He(n,p)3H cross section used is 5333 +/- 7 barn. Note the electron-counting normalisation (3He(n,p) in the same gas) is different from the NIST 6Li deposit.
  SOURCE: Fuwa et al. 2024, arXiv:2412.19519, Table of uncertainties (p. 4)
  QUOTE: "Effect Uncertainty Statistic 1.7 Cut position 0.9 Gas-induced background +1.1/-2.0 Pile up +1.5/-0.6 Contamination from 12C(n,γ)13C +1.7/-0.0 γ-ray scattering at LiF shutter 1.3 Unbunched neutron from SFC +1.1/-1.0 Inject 3He 1.2 3He in G1He +1.5/-1.4 3He(n,p)3H cross section 1.2 Total systematic +4.0/-3.6"
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RE-03] CLAIM: UCNtau (Los Alamos magneto-gravitational trap, Musedinovic et al. 2025, PRC 111, 045501; arXiv:2409.05560): the 2020-2022 runs alone give 877.94 +/- 0.37 s; the all-data UCNtau average (2018+2019 data of Pattie 2018 / Gonzalez 2021 plus these) is 877.82 +/- 0.22 (stat) +0.20/-0.17 (sys) s. It SUPERSEDES Gonzalez et al. 2021 (PRL 127, 162501, 877.75 s) and Pattie et al. 2018 (Science 360, 627, 877.7 s) as the current UCNtau value; it shares the apparatus and includes those data. Per-year values (average of four analyses A-D): 2018 877.73 +/- 0.32; 2019 877.80 +/- 0.50; 2020 879.39 +/- 0.89; 2021 878.41 +/- 0.58; 2022 876.93 +/- 0.57.
  SOURCE: Musedinovic et al. 2025, Measurement of the free neutron lifetime in a magneto-gravitational trap with in situ detection, PRC 111, 045501; arXiv:2409.05560
  QUOTE: "We report a measured value for these runs from 2020-2022 for the neutron lifetime of 877.94±0.37 s; when all the data from UCNτ are averaged we report an updated value for the lifetime of 877.82±0.22 (statistical)+0.20-0.17 (systematic) s."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RE-04] CLAIM: UCNtau 2025: the largest systematic is the choice of event-definition parameters (dip/pulse-shape cuts) in the in-situ UCN detector, followed by residual uncleaned or heated (marginally trapped) UCN. Improvements: better monitor detectors, reduced correction for UCN upscattering on ambient gas, four different main-detector geometries to probe rate dependence.
  SOURCE: Musedinovic et al. 2025, arXiv:2409.05560, p. 23 and abstract
  QUOTE: "...am’s event definition parameters, and it is the largest contributor to the systemic uncertainty in the reported lifetime, followed by the systematic uncertainty from the residual uncleaned or heated UCNs in the trap."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RE-05] CLAIM: NIST BL1 proton-counting beam, current value (Yue et al. 2013, PRL 111, 222501): tau_n = (887.7 +/- 1.2 [stat] +/- 1.9 [syst]) s. This is a RE-ANALYSIS that SUPERSEDES Nico et al. 2005 (PRC 71, 055502; 886.3 +/- 1.2 [stat] +/- 3.2 [syst] s) using the SAME beam data; only the neutron-fluence (6Li monitor) efficiency was re-measured (alpha-gamma device) and a correction of +1.4 s applied. Nico 2005's dominant uncertainty was the absolute neutron fluence (2.7 s). The 2005 and 2013 values therefore must not be averaged as independent results.
  SOURCE: Yue et al., Improved Determination of the Neutron Lifetime, PRL 111, 222501 (2013), arXiv:1309.2623
  QUOTE: "The most precise determination of the neutron lifetime using the beam method was completed in 2005 and reported a result of τn=(886.3±1.2[stat]±3.2[syst]) s. The dominant uncertainties were attributed to the absolute determination of the fluence of the neutron beam (2.7 s)." ; "The updated lifetime is τn = (887.7 ± 1.2 [stat] ± 1.9 [syst]) s."
  ACCESS: full-text (first quote from lit_search abstract; second from arXiv PDF)
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RE-06] CLAIM: BL1 2013 systematic budget (Table II of Yue 2013), relative to the 2005 beam result: improved neutron fluence determination correction +1.4 s with uncertainty 0.5 s; change in 6Li deposit mass +0.0 s, uncertainty 0.9 s; systematics unassociated with neutron fluence 1.7 s; proton counting statistics 1.2 s; neutron counting statistics 0.1 s; total correction +1.4 s, total uncertainty 2.3 s (stat and sys in quadrature as the table gives it). The fluence monitor efficiency was re-measured with the Alpha-Gamma device; the 6Li deposit's areal density change since 2005 could not be measured destructively, so non-destructive comparison with 14 deposits (approx. 20, 30, 40 ug/cm2) set a bound of 0.1% on Delta-rho, costing 0.9 s. The 1.7 s 'systematics unassociated with neutron fluence' are carried over from the 2005 experiment (itemised in RE-18) and not re-measured in 2013.
  SOURCE: Yue et al. 2013, arXiv:1309.2623, Table II (p. 4) and p. 3
  QUOTE: "TABLE II. The new uncertainty budget for the neutron life- time. Corrections shown are relative to the 2005 beam lifeti me result. Source of uncertainty Correction (s) Uncertainty (s) Improved neutron ﬂuence determination +1.4 0.5 Change in 6Li deposit mass +0.0 0.9 Systematics unassociated with neutron ﬂuence 1.7 Proton counting statistics 1.2 Neutron counting statistics 0.1 Total +1.4 2.3"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RE-07] CLAIM: Gravitrap (PNPI, Serebrov et al. 2018, PRC 97, 055503) material bottle with low-temperature Fomblin-coated copper trap, geometry (trap-size) extrapolation: tau_n = 881.5 +/- 0.7 (stat) +/- 0.6 (sys) s (total 1.3 s). Table in the paper (Serebrov's own summary) gives for other bottle results: Pattie 2017 877.7 (0.7 stat, 0.3 sys); Arzumanov 2015 880.2 +/- 1.2 (stat) and 1.2 sys; Ezhov 2014 878.3 +/- 1.9; Steyerl 2012 882.5 (1.4, 1.5); Pichlmaier 2010 880.7 (1.3, 1.2); Serebrov 2004/5 878.5 (0.7, 0.3); Yue 2013 887.7 (1.2, 1.9). Geometry extrapolation reduces dependence on the UCN-wall loss model (simulated energy-extrapolation error of order 20-40 s falls to about 2 s or less). Gravitrap 2018 supersedes Serebrov 2017 (JETP Lett. 106, 623: 881.5 +/- 0.7 +/- 0.6 s; same data reported in short form) and is from the same PNPI group and similar method as Serebrov 2004/5 (878.5 (0.7 stat, 0.3 sys) in the same table; earlier apparatus). The table lists "Serebrov 2017 881.5 ... chi2 2.4" and "Yue 2013 887.7 ... chi2 7.0", showing the PNPI group's own view that BL1 is the outlier.
  SOURCE: Serebrov et al. 2018, Neutron lifetime measurements with a large gravitational trap for ultracold neutrons, PRC 97, 055503, arXiv:1712.05663, history table p. 13
  QUOTE: "author year value error χ² Ref stat sys Σ Serebrov 2017 881.5 0.7 0.6 1.3 2.4 — Pattie 2017 877.7 0.7 0.3 1.0 3.2 [21] Arzumanov 2015 880.2 1.2 1.2 0.4 [22] Ezhov 2014 878.3 1.9 1.9 0.4 [23] Yue 2013 887.7 1.2 1.9 3.1 7.0 [24] Steyerl 2012 882.5 1.4 1.5 2.9 1.1 [25] Pichlmaier 2010 880.7 1.3 1.2 2.5 0.2 [26] Serebrov 2004 878.5 0.7 0.3 1.0 1.0 [15, 16]"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: medium (the clause about 2005 re-interpretation is unverified and must be dropped if not confirmed)
- [RE-08] CLAIM: Ezhov et al. 2018 (JETP Lett. 107, 671): UCN stored in a permanent-magnet magneto-gravitational trap give tau_n = 878.3 +/- 1.6 (stat) +/- 1.0 (syst) s; the 2014 arXiv preprint (arXiv:1412.7434) gave the same central value with error 1.9 s described as "purely statistical" (its text: "The result extracted using data from runs A and B is τn = (878.3 ± 1.9) s ... where the error is purely statistical"), so the 2018 JETP Letters paper is the same data with a systematic budget added (this reading is mine; the 2018 paper itself was not opened). Use the 2018 split (1.6 stat, 1.0 syst) as current. Spin-flip loss (depolarisation) is corrected using a measured efficiency epsilon, and residual-gas upscattering was estimated from the pressure dependence. The apparatus monitors UCN leaking out of the trap to control the main systematic loss. Ezhov et al. 2023 (JETP Lett. 117, 91) discuss depolarisation and small heating as loss channels and propose online detection.
  SOURCE: WebSearch (Springer page blocked), Ezhov et al. 2018; Ezhov et al. 2023 abstract via lit_search (Crossref)
  SUMMARY: "The Ezhov et al. 2018 measurement in JETP Letters volume 107, pages 671-675 reported a neutron lifetime value of τ_n = (878.3 ± 1.6_stat ± 1.0_syst) s ... A unique feature of the experiment was the monitoring of leaking neutrons providing a robust control of the main systematic loss." ; Crossref abstract 2023: "Possible systematic effects in experimental measurements of the lifetime of the neutron using magneto-gravitational traps to store ultracold neutrons have been discussed. Methods for the online detection of possible losses, including depolarization losses and a small heating of neutrons stored in a trap, have been proposed."
  ACCESS: search-summary
  STATUS: peer-reviewed
  CONFIDENCE: medium
- [RE-09] CLAIM: Blinding and in-situ tests in UCNtau: the holding times are blinded with a factor in the range 0.99986-1.00171, data unblinded only after at least two analysers agreed per data set; four independent analyses (A-D) per year; after unblinding an analysis bias was found in the 2020 set (seven runs wrongly excluded for high chi2) and, with them added back, shifted the fitted lifetime of a 659-run portion of 2020 by 1.0 s (vs 1.0 s statistical error of that subset). In-situ tests: movable in-trap "dagger" detector at cleaning height to search for uncleaned or heated UCN, variable-height barriers, four dagger geometries, monitor detectors. Year-to-year scatter: 2020 879.39 +/- 0.89 s and 2022 876.93 +/- 0.57 s differ by about 2.3 s.
  SOURCE: Musedinovic et al. 2025, arXiv:2409.05560, pp. 9, 7-8, 23
  QUOTE: "Our data are blinded with a blinding factor in the range of 0.99986-1.00171 that hides the actual holding time from analyzers ... We unblinded our data after achieving agreement between at least two analyzers for each of the three data sets."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RE-10] CLAIM: Bottle average as quoted by the PDG (via J-PARC paper and PSI page): 878.4 +/- 0.5 s ("tau_n^bottle"); J-PARC paper quotes a 9.5 s (4.6 sigma) discrepancy with the beam (proton-counting) average, i.e. beam average near 887.9 s. The PDG number predates Musedinovic 2025 and J-PARC 2024. NIST (Yue 2013) plus Byrne 1996 (Sussex-ILL) are the two proton-counting inputs; per the Serebrov 2018 table the beam average is 887.7 +/- 3.1 s (his own average including BL1 only).
  SOURCE: Fuwa et al. 2024, arXiv:2412.19519, p. 1; PSI UCN group page https://www.psi.ch/en/ltp-ucn-physics/neutron-lifetime
  QUOTE: "...producing an average value ofτ bottle n = 878.4 ± 0.5 s. The 9.5-s (4.6σ) discrepancy between the two methods is known as the “neutron lifetime puzzle”" ; PSI: "The average lifetime of the free neutron, 878.4 ± 0.5 s [ S. Navas et al. ]"
  ACCESS: full-text
  STATUS: peer-reviewed (PDG) via preprint
  CONFIDENCE: medium (PDG edition not opened; statistician recomputes)
- [RE-11] CLAIM: BL1 to BL2 to BL3 programme (NIST/Tulane): BL2 is the running upgrade of the proton-counting experiment, led by Hoogerheide and Caylor, with stated goal of overall uncertainty below 1 s ("1 s a realistic goal") and focus on systematic issues, in particular proton charge exchange with residual gas in the trap. BL3 is an all-new, larger apparatus (larger proton trap and detector, improved neutron flux monitor, upgraded alpha-gamma device for absolute flux-monitor calibration) aiming at 0.3 s precision with systematics evaluated at the same level; at the 13 Sept 2025 PSI workshop BL3 was in construction with "a plan and timeline for mounting the experiment" (no date given in the abstract).
  SOURCE: Wietfeldt, The NIST Beam Neutron Lifetime Experiments, and Hoogerheide, The BL3 Neutron Lifetime Experiment, PSI workshop Neutron Lifetime Puzzle, 13 Sep 2025, Book of Abstracts, https://indico.psi.ch/event/17167/book-of-abstracts.pdf; BL2 goal from WebSearch summary of "Progress on the BL2 beam measurement of the neutron lifetime" (PMC9706643, blocked)
  QUOTE: "We will review the previous BL1 exper- iment (2005, 2013); discuss the current BL2 experiment and systematic issues we have focused on, in particular proton charge exchange with residual gas in the trap; and describe BL3, a new next- generation version of the experiment with improved systematics and capable of a high precision result at the <0.3 s level." ; "The goal of the BL3 Beam Neutron Lifetime Experiment is to improve the precision of beam-based neutron lifetime experiments to the 0.3 s level ..."
  ACCESS: full-text (workshop abstracts); BL2 '1 s' goal is search-summary only
  STATUS: preliminary
  CONFIDENCE: medium
- [RE-12] CLAIM: No BL2 or BL3 lifetime result is public in the sources I opened (as of the Sept 2025 abstracts). BL1's largest remaining budget item (fluence-independent systematics 1.7 s) is what BL2/BL3 target; charge exchange of decay protons on residual gas is named as the focus issue (the J-PARC paper notes it is 'considered negligible' per ref. [20]).
  SOURCE: Fuwa et al. 2024, arXiv:2412.19519 p. 1; PSI workshop abstracts 2025
  QUOTE: "Possible causes for this discrepancy include unac- counted systematic uncertainties, such as protons from neutron decay undergoing charge exchange with residual gas [19], though this effect is considered negligible [20]."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium
- [RE-13] CLAIM: tauSPECT (Mainz/PSI; Fertl, Ries, Heil groups): a fully magnetic 3D gradient-field trap at the PSI UCN source since 2023, loaded by double spin-flip; target tau_n uncertainty < 0.3 s; a first BLINDED science run in 2024 with anticipated statistical precision 1 s; dominant concern is quasi-trapped (marginally trapped) UCN which bias the lifetime low; physics data taking in 2025 (search summary). No tau_n value published. Earlier Mainz TRIGA commissioning gave a storage time 859(16) s, explicitly not a lifetime.
  SOURCE: Fertl, tauSPECT - towards a new measurement..., PSI workshop Book of Abstracts 13 Sep 2025, https://indico.psi.ch/event/17167/book-of-abstracts.pdf; Auler et al., J. Phys. G 51 (2024) 115103
  QUOTE: "In a first step, τSPECT aims to determine τn with an uncertainty of < 0.3 s to illuminate the neutron lifetime puzzle ... In 2024, τSPECT has performed a first blinded science data run with an anticipated statistical precision of 1 s on τn. ... Quasi-trapped UCNs could leave the trap on the timescale of τn, and a strict control of these marginally trapped UCNs is required to avoid a bias towards a low value of τn."
  ACCESS: full-text (abstract of talk)
  STATUS: preliminary
  CONFIDENCE: high
- [RE-14] CLAIM: PENeLOPE (TUM, now at TRIUMF): superconducting magnetic trap, about 550 litre storage volume, about 1.8-2 T multipole field, 42 coils, real-time detection of decay protons; built at TUM 2020, moved to TRIUMF 2024 to use the new TUCAN UCN source; cryostat tests in 2025; no lifetime data and no quoted precision or date for a result in the abstract.
  SOURCE: Gundel et al., PENeLOPE talk abstract, PSI workshop 13 Sep 2025, Book of Abstracts
  QUOTE: "With the large storage volume of about 550 liters as well as the design allowing for real time detection of decay protons, we aim at a high precision measurement with unprecedented systematic and statistical uncertainties. The system was constructed and set up at the Technical University of Munich in 2020. Following initial tests, PENeLOPE was transferred to TRIUMF in 2024 to perform first measurements at the new TUCAN UCN source."
  ACCESS: full-text (abstract of talk)
  STATUS: preliminary
  CONFIDENCE: high
- [RE-15] CLAIM: UCNProBe (LANL; Krivos, Morris) is an in-bottle beta-counting design: UCN stored in a deuterated-polystyrene scintillator box that also detects decay electrons, neutrons counted with a boron-coated YAP:Ce scintillator; a beam-type (partial rate) measurement but with UCN; aimed at 1-2 s precision (search summary). It counts electrons from a material trap, so it is a third, independent partition (storage + decay product count) that separates 'proton counting' from 'storage' explanations. Status at Sept 2025: 'upcoming experiment', no result.
  SOURCE: Krivos, UCNProBe a beam-type experiment using ultracold neutrons, PSI workshop Book of Abstracts 2025; 1-2 s goal from WebSearch summary of APS DNP 2019 abstract
  QUOTE: "UCNProBe will follow the beam-type measurement method but uniquely incorporate UCN characteristics. In this setup, UCN will be confined within a material bottle made of deuterated polystyrene box that will also serve as an in-situ detector for electrons from the beta decay. For neutron counting, a boron-coated YAP:Ce crystal scintillator will be used."
  ACCESS: full-text (abstract of talk); 1-2 s goal search-summary
  STATUS: preliminary
  CONFIDENCE: medium
- [RE-16] CLAIM: UCNtau+ (LANL): planned upgrade of UCNtau with a new elevator loading technique to increase the number of loaded UCN by a factor 5-10, needing systematic effects characterised 'well below 0.2 s'. A status talk by S. Seestrom was given at the 13 Sep 2025 workshop (no abstract text). No date for results found.
  SOURCE: Musedinovic et al. 2025, arXiv:2409.05560, p. 5
  QUOTE: "The analysis reported here is aimed at developing new methods to characterize and reduce systematic effects well below 0.2 s, needed for the upcoming experiment, UCNτ+, that will use a new elevator loading technique to increase the number of loaded UCN by a factor of 5-10."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RE-17] CLAIM: Partition check by apparatus: five of the current values share no apparatus (BL1/NIST; J-PARC TPC; UCNtau/LANL; Gravitrap/PNPI; Ezhov/ILL-type permanent-magnet trap). Shared-apparatus pairs: Nico 2005 and Yue 2013 (same beam data; 2013 supersedes); Pattie 2018, Gonzalez 2021 and Musedinovic 2025 (all UCNtau; Musedinovic includes all earlier data and supersedes them); J-PARC 2020 and 2024 (same TPC; 2024 supersedes). J-PARC is the only electron-counting beam result; it is a beam experiment without a strong trapping field, and its value 877.2 sits with the bottles, so the proton-counting-vs-rest partition and the strong-field-vs-weak-field partition both fit the data better than the beam-vs-bottle partition; J-PARC's own uncertainty (about +4.0/-3.6 s sys) leaves 2.3 sigma to the proton-counting average by the authors' number.
  SOURCE: this facet's synthesis of RE-01, RE-03, RE-05
  SUMMARY: derived from the cited values; no new measurement
  ACCESS: full-text (inputs)
  STATUS: secondary
  CONFIDENCE: medium

- [RE-18] CLAIM: BL1 2005 experiment (Nico et al., PRC 71, 055502; arXiv:nucl-ex/0411041) method and budget, the base that Yue 2013 re-scaled. Method: lifetime from slope of (proton rate / alpha+triton monitor rate) versus trap length, using 3 to 10 grounded electrodes (trap length L = n*l + L_end); the trap-length variation is the in-situ test that removes the electrostatic end effect, four beam collimation/Bi-filter configurations were used to look for unknown systematics, and the series intercepts (end effects) differ by up to 13%. The arXiv preprint text gives tau_n = (886.6 +/- 1.2 [stat] +/- 3.2 [sys]) s, whereas Yue 2013 quotes the 2005 result as 886.3 +/- 1.2 +/- 3.2 s (the difference between 886.6 and 886.3 is not explained in the sources I opened). Table IV: corrections (s) / uncertainty (s): 6LiF deposit areal density - / 2.2; 6Li cross section - / 1.2; neutron detector solid angle - / 1.0; absorption by 6Li +5.4 / 0.8; beam profile and detector solid angle +1.3 / 0.1; beam profile and 6Li deposit shape -1.7 / 0.1; beam halo -1.0 / 1.0; absorption by Si substrate +1.3 / 0.1; scattering by Si substrate -0.2 / 0.5; TRAP NONLINEARITY -5.3 / 0.8; proton backscatter calculation - / 0.4; dead time +0.1 / 0.1; proton counting statistics - / 1.2; neutron counting statistics - / 0.1; total -0.1 / 3.4. Setting the measured beam-off rates to zero would shift the lifetime by -0.72 s. The proton-trap corrections are large (trap nonlinearity -5.3 s, lost-proton correction applied before the fit), so any unmodelled trap effect could matter; the table's 6Li-cross-section and areal-density items (2.2 and 1.2 s) were those removed by the 2013 re-analysis.
  SOURCE: Nico et al. 2005, Measurement of the neutron lifetime by counting trapped protons in a cold neutron beam, PRC 71, 055502, arXiv:nucl-ex/0411041, Table IV (p. 35) and Sec. V (p. 67)
  QUOTE: "The result of the lifetime measurement is τn = (886.6 ± 1.2[stat] ± 3.2[sys]) s, which is the most precise measurement of the lifetime using an in-beam method." ; "Trap nonlinearity −5. 3 0 . 8 IV C Proton backscatter calculation 0. 4 IV D 3 Neutron counting dead time +0 . 1 0 . 1 II D Proton counting statistics 1. 2 IV D 2 Neutron counting statistics 0. 1 II D Total −0. 1 3 . 4"
  ACCESS: full-text
  STATUS: peer-reviewed (arXiv preprint text)
  CONFIDENCE: high for table entries; medium for the 886.6 vs 886.3 difference (probably preprint vs published version)
- [RE-19] CLAIM: BL2-era in-situ test of proton loss mechanisms: Caylor et al. 2025 (PRC 112, 065501, arXiv:2506.01682) measured charge exchange of trapped protons on molecular hydrogen in the NIST apparatus and the detection efficiency of the resulting H2+ ions, and conclude that the NIST beam result 'is unlikely to have been significantly affected'. The trap bore is a cryopump so all residual gases except He, H2 and Ne are taken as negligible; the 4He charge-exchange cross section is about two orders of magnitude below H2 at the relevant energies (<1 keV). This is the proton-counting-beam group's own rebuttal to the charge-exchange systematic; the critiques facet owns the independent assessment.
  SOURCE: Caylor et al., Detection of molecular hydrogen in a neutron beam lifetime experiment, PRC 112, 065501 (2025), arXiv:2506.01682
  QUOTE: "We demonstrate that charge exchange with molecular hydrogen can occur with trapped protons, and we determine the efficiency with which the molecular hydrogen ions in the trap are detected. Finally, we comment on the potential impact on a neutron lifetime experiment using this beam technique. We find that the result of the beam neutron lifetime performed at NIST is unlikely to have been significantly affected by charge exchange with molecular hydrogen."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RE-20] CLAIM: Design differences that matter for the partition question: (a) the proton-counting beam (BL1) needs absolute neutron fluence from a thin 6Li deposit (thermal/cold-neutron 1/v monitor) whose largest 2005 items were deposit areal density (2.2 s) and 6Li cross-section (1.2 s), now replaced by an Alpha-Gamma absolute calibration (2013) with a residual 0.9 s from possible deposit change; (b) J-PARC needs no deposit, normalising to 3He(n,p)3H in the same gas but relying on the 3He amount (1.2 and 1.5 s terms) and the (n,p) cross section (5333 +/- 7 barn, 1.2 s); (c) UCNtau uses a wall-free trap, but its in-situ detector event definition and marginal/heated UCN dominate its small 0.20/0.17 s systematic. The J-PARC TPC has no strong magnetic trapping field, unlike BL1's roughly 4.6 T solenoid (value not quoted in opened text; do not use).
  SOURCE: synthesis of RE-02, RE-04, RE-06, RE-18
  SUMMARY: from the quoted budgets; no new measurement
  ACCESS: full-text (inputs)
  STATUS: secondary
  CONFIDENCE: medium

## Gaps
- Not opened this session: Byrne et al. 1996 (Sussex-ILL, 889.2 +/- 3.0 +/- 3.8 s as given in the brief), Pichlmaier 2010 (MAMBO II), Steyerl 2012, Arzumanov 2015 (only Serebrov's table values seen, RE-07), Serebrov 2005; Nico 2005 budget (what makes up the 1.7 s of fluence-independent systematics: trap nonlinearity, proton backscatter, residual gas, end-effect and trap-length variation); Ezhov 2018 full text (Springer blocked); PDG 2024/2025 edition (878.4 +/- 0.5 s only at second hand).
- Space-based measurements (Wilson et al. 2020, Lunar Prospector / MESSENGER) not searched.
- Not found: any numeric BL2 result; a date for BL3 first data; J-PARC upgrade plan (target precision and year) beyond 'fivefold improvement'; HOPE (Hummel/TU Wien?) and Gravitrap upgrade (cooling to 10-15 K; Serebrov plans about 0.2 s) details; UCNtau+ date; timeline for tauSPECT result; UCNProBe date. The Sept 2025 PSI workshop round table 'where will the lifetime be in 10 years' has no text.
- J-PARC 2024 journal version (Physical Review Letters?) not checked; the arXiv preprint quotes are used.
- Nico 2005 was found on arXiv (RE-18), so no paper needs requesting. The 2013 'systematics unassociated with fluence, 1.7 s' line is not itemised in Yue 2013; its makeup from the 2005 Table IV is my inference and I did not combine the items.
- Another quick search should check for BL2/BL3/J-PARC updates newer than Sept 2025 (frontier facet owns these).
