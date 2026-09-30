# Research: frontier
status: draft
Mandate: newest material (2024-2026) on the neutron lifetime puzzle: preprints, talks, updates, errata, critiques, new theory; each with evidential status.
Access: lit_search INSPIRE (pending), arXiv (pending); WebFetch domains that worked: (pending)

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

## Gaps
