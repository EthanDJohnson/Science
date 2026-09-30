# Research: quantitative
status: final
Mandate: SM inputs and related measured quantities (lambda, Vud, Vus, Vub, unitarity, radiative corrections, constants) and planned lambda/correlation experiments
Access: lit_search INSPIRE ok (multi-word queries often returned 0 hits), arXiv ok via fetch_text; find_fulltext ok (OSTI for Hardy-Towner); WebFetch not used; WebSearch used for PERC/BRAND status (search-summary only); PDG 2024 pdfs readable.

## Claims
- [RQ-01] CLAIM: PERKEO III (Märkisch et al. 2019; pulsed cold-neutron beam, electron spectra) gives lambda = gA/gV = -1.27641(45)stat(33)sys, i.e. A0 = -0.11985(17)stat(12)sys. Dimensionless.
  SOURCE: Märkisch et al. 2019, Phys. Rev. Lett. 122, 242501 (arXiv preprint 1812.04666), https://arxiv.org/pdf/1812.04666
  QUOTE: "From the electron spectra we obtainλ=gA/gV =−1.27641(45)stat(33)sys which conﬁrms recent measurements with improved precision. This corresponds to a value of the parity violating beta asymmetry parameter ofA0 = −0.11985(17)stat(12)sys."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RQ-02] CLAIM: The PERKEO III paper itself derives Vud = 0.97351(60) from tau_n = 879.7(8) s (its then world average) and its lambda, using the pre-2018 radiative correction (RC error 19e-5, tau_n error 44e-5, lambda error 35e-5), and notes agreement with superallowed Vud = 0.97417(21). Shows the tau_n used matters at the 4e-4 level in Vud. The authors did not use the reduced-uncertainty common radiative correction of Ref. [60] "as theoretical discussions are ongoing".
  SOURCE: Märkisch et al. 2019, PRL 122, 242501 (arXiv preprint 1812.04666)
  QUOTE: "Vud = ( 4908.6(1.9) τn·(1 + 3λ2) )1/2 = 0.97351(19)RC(44)τn(35)λ, = 0.97351(60), (6) where the error denoted RC stems from radiative cor- rections [59]."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RQ-03] CLAIM: PDG 2024 lambda = gA/gV average is -1.2754 ± 0.0013 with scale factor 2.7 (chi2 = 35.1, confidence level < 0.0001). Inputs listed: Hassan 2021 (aCORN) -1.2796 ± 0.0062; Beck 2020 (aSPECT, from a) -1.2677 ± 0.0028; Märkisch 2019 (PERKEO III) -1.27641 ± 0.00045 ± 0.00033; Brown 2018 (UCNA) -1.2772 ± 0.0020; Mund 2013 (PERKEO II) -1.2748 ± 0.0008 +0.0010 -0.0011. Older (Schumann 08, Mostovoi 01, Liaud 97, Yerozolimsky 97, Bopp 86) also enter. The ideogram prints per-experiment chi2 contributions but the extraction does not show unambiguously which number belongs to which experiment, so I do not attribute them; total chi2 = 35.1. The aSPECT value is the one farthest from the beta-asymmetry results. Note the PDG 2024 entry quotes the ORIGINAL aSPECT 2020 value; aSPECT was re-analysed in 2024 (see RQ-04).
  SOURCE: PDG (Navas et al.) 2024, Phys. Rev. D 110, 030001, neutron listings, https://pdg.lbl.gov/2024/listings/rpp2024-list-n.pdf
  QUOTE: "− 1.2754 ± 0.0013 OUR A VERAGE ... Error includes scale factor of 2.7. See the ideogram below. − 1.2796 ± 0.0062 1 HASSAN 21 SPEC Proton recoil spectrum − 1.2677 ± 0.0028 2 BECK 20 SPEC Proton recoil spectrum − 1.27641± 0.00045 ± 0.00033 3 MAERKISCH 19 SPEC pulsed cold n, polarized − 1.2772 ± 0.0020 4 BROWN 18 UCNA Ultracold n, polarized − 1.2748 ± 0.0008 + 0.0010 − 0.0011 5 MUND 13 SPEC Cold n, polarized"
  ACCESS: full-text
  STATUS: textbook-or-review
  CONFIDENCE: high

- [RQ-04] CLAIM: PDG 2024 A (electron asymmetry) average is -0.11958 ± 0.00021 (scale factor 1.2, CL = 0.261), i.e. the beta-asymmetry data alone are mutually consistent; the lambda scale factor 2.7 is driven by the a-coefficient (proton recoil) inputs aSPECT/aCORN. SM relations: A = -2 lambda(lambda+1)/(1+3 lambda^2), B = 2 lambda(lambda-1)/(1+3 lambda^2).
  SOURCE: PDG 2024, neutron listings (e- asymmetry parameter A), https://pdg.lbl.gov/2024/listings/rpp2024-list-n.pdf
  QUOTE: "In the Standard Model, A is related to λ ≡ gA/gV by A = − 2 λ (λ + 1) / (1 + 3 λ2); this assumes that gA and gV are real. VALUE DOCUMENT ID TECN COMMENT − 0.11958± 0.00021 OUR A VERAGE ... Error includes scale factor of 1.2."
  ACCESS: full-text
  STATUS: textbook-or-review
  CONFIDENCE: high

- [RQ-05] CLAIM: PDG 2024 (31 May 2024 review) |Vud| from the average of the fifteen most precise superallowed 0+→0+ decays is 0.97367 ± 0.00032 (error about twice that of the 2020 edition because of a more conservative nuclear-structure uncertainty). PDG also quotes neutron-lifetime-based Vud as limited by lambda, and pion beta decay |Vud| = 0.9739 ± 0.0027.
  SOURCE: PDG 2024, CKM Quark-Mixing Matrix review, https://pdg.lbl.gov/2024/reviews/rpp2024-rev-ckm-matrix.pdf
  QUOTE: "Taking the average of the ﬁfteen most precise determinations [9] yields [10] |Vud|= 0.97367±0.00032. (12.7) ... This uncertainty is slightly more than twice as large as that in the 2020 edition, due to a more conservative estimate of the nuclear structure uncertainties."
  ACCESS: full-text
  STATUS: textbook-or-review
  CONFIDENCE: high

- [RQ-06] CLAIM: PDG 2024 CKM global-fit unitarity sums: first row |Vud|²+|Vus|²+|Vub|² = 0.9984 ± 0.0007 (2.3 sigma below 1); second row 1.001 ± 0.012; first column 0.9971 ± 0.0020; second column 1.003 ± 0.012.
  SOURCE: PDG 2024, CKM review, https://pdg.lbl.gov/2024/reviews/rpp2024-rev-ckm-matrix.pdf
  QUOTE: "|Vud|2 +|Vus|2 +|Vub|2 = 0.9984±0.0007 (1st row),|Vcd|2 +|Vcs|2 +|Vcb|2 = 1.001±0.012 (2nd row),|Vud|2 +|Vcd|2 +|Vtd|2 = 0.9971±0.0020 (1st column) ... Due to the recent re- duction of the value of|Vud|, there is a2.3σtension with unitarity in the 1st row"
  ACCESS: full-text
  STATUS: textbook-or-review
  CONFIDENCE: high

- [RQ-07] CLAIM: PDG 2024 |Vus| from K_l3 (|Vus| f+(0) = 0.21656 ± 0.00035, f+(0) = 0.9698 ± 0.0017 from Nf = 2+1+1 lattice QCD) is 0.2233 ± 0.0005; from K→μν/π→μν (fK/fπ = 1.1932 ± 0.0021) is 0.2250 ± 0.0004; average, error scaled by sqrt(chi2) = 2.5, is |Vus| = 0.22431 ± 0.00085. The K_l3 vs K_mu2 tension (about 0.0017 in |Vus|) is thus part of the unitarity problem.
  SOURCE: PDG 2024, CKM review, https://pdg.lbl.gov/2024/reviews/rpp2024-rev-ckm-matrix.pdf
  QUOTE: "The average of these ﬁve decay modes yields|Vus|f+(0) = 0.21656±0.00035. ... gives|Vus|= 0.2233±0.0005 [10]. ... leads to |Vus|= 0.2250±0.0004, where the accuracy is limited by the knowledge of the ratio of the decay constants. The average of these two determinations, with the error scaled according to the PDG prescription [21] by √ χ2 = 2.5, is quoted as [10] |Vus|= 0.22431±0.00085. (12.8)"
  ACCESS: full-text
  STATUS: textbook-or-review
  CONFIDENCE: high

- [RQ-08] CLAIM: CODATA 2018 neutron-proton mass difference mn − mp = 1.29333236 ± 0.00000046 MeV (PDG 2024 listing; SI-derived energy units); neutron mass in u = 1.008664919 ± 0.000000014 u. These fix the phase-space factor inputs in the master formula and are known to ~1e-7 relative, so they are irrelevant to the anomaly.
  SOURCE: PDG 2024 neutron listings (Tiesinga 2021 CODATA), https://pdg.lbl.gov/2024/listings/rpp2024-list-n.pdf
  QUOTE: "1.29333236± 0.00000046 1 TIESINGA 21 RVUE 2018 CODATA value"
  ACCESS: full-text
  STATUS: textbook-or-review
  CONFIDENCE: high

- [RQ-09] CLAIM: PDG 2024 |Vub| (inclusive/exclusive, error scaled by sqrt(chi2)=1.4) is of order 3.7–4.1e-3, so |Vub|² ~ 1.5e-5 and is negligible in the first-row sum (inclusive |Vub| = (4.13±0.12 +0.13 −0.14 ±0.18)e-3; exclusive B→π l ν with lattice and LCSR (3.67±0.09±0.12)e-3). Gorchtein & Seng: "|Vub|² ~ 1e-5 can safely be dropped".
  SOURCE: PDG 2024 CKM review, https://pdg.lbl.gov/2024/reviews/rpp2024-rev-ckm-matrix.pdf
  QUOTE: "Ref. [15] quotes the inclusive average, |Vub|= (4.13±0.12 +0.13 −0.14±0.18)×10−3 ... yield a combination, |Vub|= (3.67±0.09±0.12)×10−3 [15,24]."
  ACCESS: full-text
  STATUS: textbook-or-review
  CONFIDENCE: high

- [RQ-10] CLAIM: Hardy & Towner 2020 critical survey of 23 superallowed 0+→0+ decays (222 measurements, 174 references) gives Vud = 0.97373 ± 0.00031, lower than their 2015 value by one standard deviation with the error increased by 50%; the change comes from new radiative-correction calculations, not from data. Also limit on Fierz interference bF ≤ 0.0033 (90% CL). Uses Vud = G_V/G_F with muon-decay G_F.
  SOURCE: Hardy & Towner 2020, Phys. Rev. C 102, 045501 (accepted manuscript, OSTI, of doi:10.1103/PhysRevC.102.045501)
  QUOTE: "Their ave rage, F t, when combined with the muon lifetime, yields the up-down quark-mixing element of the Cabibbo-Kobayashi-Maskawa matrix, Vud = 0 . 97373 ± 0. 00031. This is lower than our 2015 result by one standard devi ation and its uncertainty is increased by 50%. This is a consequence, not o f any shifts in the experimental data, but of new calculations for the radiative corrections."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RQ-11] CLAIM: Gorchtein & Seng (Ann. Rev. Nucl. Part. Sci. 74, 2024) summarise: Hardy–Towner 2020 gives |Vud|_0+ = 0.97361(5)exp(6)δR′(4)δC(28)δNS(10)RC total; combined with |Vus| = 0.2243(8) from kaon channels this gives Δu^0+ ≡ |Vud|²+|Vus|²−1 = −0.00166(69), a 2.4σ top-row unitarity deficit. Neutron decay with PDG-average inputs gives Δu^n = −0.00037(174), i.e. no significant deficit, "a mild disagreement which is to be understood". (The 0.97361 value reflects a later radiative-correction reevaluation than the 0.97373 of HT2020; the review attributes it to the HT survey with updated inputs.)
  SOURCE: Gorchtein & Seng 2024, "Superallowed Nuclear Beta Decays and Precision Tests of the Standard Model", Ann. Rev. Nucl. Part. Sci. 74, 23; arXiv:2311.00044, https://arxiv.org/pdf/2311.00044
  QUOTE: "|Vud|0+ = 0.97361(5)exp(6)δ′ R (4)δC(28)δNS(10)RC[31]total . (42) Combined with|Vus| = 0.2243(8) from kaon decays channels [45], it returns∆0+ u ≡| Vud|2 0+ + |Vus|2− 1 =−0.00166(69) which indicates a2.4σ unitarity-deficit. This is to be compared to neutrondecay[47]: ∆n, PDG-av u =−0.00037(174)whichshowsnosuchdeficit, amilddisagreement which is to be understood."
  ACCESS: full-text
  STATUS: textbook-or-review
  CONFIDENCE: high

- [RQ-12] CLAIM: Czarnecki–Marciano–Sirlin 2018 SM master formula: |Vud|² τn (1 + 3 gA²) = 4908.6(1.9) s, with phase-space factor f = 1.6887(1) and the uncertainty dominated by radiative corrections (RC). Units: seconds; gA here = |lambda|. This coefficient is the pre-2023 baseline; the 2023 EFT evaluation (RQ-14) shifts the rate correction by +0.026% (so the constant changes by about 0.03% ≈ 1.3 s of the 4908.6 s).
  SOURCE: Czarnecki, Marciano & Sirlin 2018, "Neutron lifetime and axial coupling connection", Phys. Rev. Lett. 120, 202002 (arXiv preprint 1802.01804), https://arxiv.org/pdf/1802.01804
  QUOTE: "leads to f = 1 . 6887(1) [30, 31] ... Using the above input parameters, but keeping Vud, τn and gA arbitrary, produces the SM master formula |Vud|2τn(1 + 3g2 A) = 4908 . 6(1. 9)s (2) where the uncertainty comes primarily from the RC."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RQ-13] CLAIM: Seng, Gorchtein, Patel & Ramsey-Musolf 2018 dispersive evaluation of the universal inner radiative correction: ΔR^V = 0.02467(22) and |Vud| = 0.97366(15) (assuming other SM inputs unchanged), which "raises tension with first-row CKM unitarity". The same value enters both superallowed and neutron decay.
  SOURCE: Seng et al. 2018, Phys. Rev. Lett. 121, 241804 (arXiv preprint 1807.10197), https://arxiv.org/pdf/1807.10197
  QUOTE: "we obtain an updated value of ∆ V R = 0.02467(22), wherein the hadronic uncertainty is reduced. Assuming other Standard Model theoretical calculations and experimental measurements remain unchanged, we obtain an updated value of|Vud| = 0.97366(15), raising tension with the ﬁrst row CKM unitarity constraint."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RQ-14] CLAIM: Cirigliano, Dekens, Mereghetti & Tomalak 2023 (EFT, top-down matching, RG to the electron mass; Phys. Rev. D 108, 053003) re-evaluate the inner radiative correction and Δf. Extraction of Vud from neutron decay: with PDG-average tau_n and lambda, V_ud^n,PDG = 0.97430(2)Δf(13)ΔR(82)λ(28)τn [88]total; with UCNτ tau_n = 877.75(36) s and PERKEO III lambda, V_ud^n,best = 0.97402(2)Δf(13)ΔR(35)λ(20)τn [42]total. Relative to the baseline of Refs. [1–6,8] (CMS 2018/Seng 2018 type), ΔR shifts by +0.061%, Δf by −0.035%, net +0.026% in the rate correction, giving δVud ≃ −13e-5. Both neutron Vud values lie above PDG-2024 superallowed 0.97367(32): 'best' 0.97402(42) is 0.00035 above (about 0.7σ using the two quoted errors in quadrature, my arithmetic), PDG-average 0.97430(88) is 0.00063 above (about 0.7σ). NOTE: these inputs use the UCNτ (bottle) lifetime; a beam lifetime of about 888 s would lower the extracted Vud by about 0.57% (Vud ∝ τ^-1/2), see RQ-19. CAUTION: a bare master-formula evaluation (RQ-19) with K = 4908.6 s, UCNτ and PERKEO III gives Vud = 0.97459, i.e. 5.7e-4 higher than the quoted 0.97402; the quoted value therefore rests on a different (updated) rate constant than CMS 2018's 4908.6 s; the paper's baseline 'Ref. [8]' is Cirigliano, Crivellin, Hoferichter & Moulson, Phys. Lett. B 838, 137748 (2023), ΔR = 3.983(27)×10^-2 compiled from Refs. [1–6]. The new paper finds ΔR = 4.044(27)% and Δ_TOT = 7.761(27)% against 7.735(27)% from the earlier compilation ("about one σ below our result"). Exactly how the constant maps onto 4908.6 s was not checked (the cause of the 5.7e-4 offset is unresolved: possibly recoil/lambda-specific corrections or a different f). Treat the bare-formula Vud values in RQ-19 as CMS-2018-baseline only.
  SOURCE: Cirigliano et al. 2023, "Effective field theory for radiative corrections to charged-current processes: Vector coupling", Phys. Rev. D 108, 053003 (arXiv preprint 2306.03138), https://arxiv.org/pdf/2306.03138
  QUOTE: "Using the PDG [56, 57] averages for the experimental input, we obtain V n, PDG ud = 0.97430(2)∆f (13)∆R(82)λ(28)τn[88]total. (7) ... if we instead use the most precise neutron lifetime measurement τn = 877.75(36) s from UCNτ@LANL [58] and the determination ofλ from the most precise measurement of the beta asymmetry in polarized neutron decay by PERKEO- III [59, 60], we obtain a very competitive extraction of Vud from neutron decay: V n, best ud = 0.97402(2)∆f (13)∆R(35)λ(20)τn[42]total, (8)"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RQ-15] CLAIM: Cirigliano, de Vries, Hayen, Mereghetti & Walker-Loud 2022 identify new virtual-pion radiative corrections in neutron beta decay; the largest is a percent-level shift in the axial charge gA proportional to the electromagnetic pion-mass splitting; smaller corrections (comparable to anticipated experimental precision) affect the β–ν angular correlations and the β asymmetry. Relevance: it shifts the relation between measured correlation coefficients (A, a) and the lattice/QCD gA, and so matters for the lambda comparison with lattice and for extracting lambda from a, A at the 1e-3 level; it is not a correction to the total rate beyond the ones in RQ-14. (Phys. Rev. Lett. 129, 121801.)
  SOURCE: Cirigliano et al. 2022, "Pion-induced radiative corrections to neutron beta-decay" (arXiv preprint 2202.10439), https://arxiv.org/pdf/2202.10439
  QUOTE: "We identify and compute new radiative corrections arising from virtual pions that were missed in previous studies. The largest correction is a percent-level shift in the axial charge of the nucleon proportional to the electromagnetic part of the pion-mass splitting. Smaller corrections, comparable to anticipated experimental precision, impact the β-ν angular correlations and the β-asymmetry."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: medium (journal reference from the brief's lead; quote is from the preprint)

- [RQ-16] CLAIM: The first lattice-QCD calculation of the universal axial γW box (Ma et al., PRL 132, 191901, 2024): □_γW^VA = 3.65(8)lat(1)PT × 1e-3 (dimensionless); this yields |Vud| = 0.97386(11)exp(9)RC(27)NS from superallowed decays, reducing the superallowed-based first-row unitarity tension from 2.1σ to 1.8σ. The authors also compute the vector γW box contribution to gA (□_γW^VV). So the superallowed Vud (and the size of the CKM deficit) depends at the 0.0002 level on which ΔR^V evaluation is adopted (0.97361 – 0.97386).
  SOURCE: Ma et al. 2024, PRL 132, 191901 (arXiv:2308.16755 abstract), https://arxiv.org/abs/2308.16755
  QUOTE: "Upon performing the continuum extrapolation, we arrive at $\square_{\gamma W}^{VA}=3.65(8)_{\mathrm{lat}}(1)_{\mathrm{PT}}\times10^{-3}$. Consequently, this yields a slightly higher value of $|V_{ud}|=0.97386(11)_{\mathrm{exp.}}(9)_{\mathrm{RC}}(27)_{\mathrm{NS}}$, reducing the previous $2.1\sigma$ tension with the CKM unitarity to $1.8\sigma$."
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RQ-17] CLAIM: Lattice QCD nucleon isovector axial charge (ETM twisted mass, 3 ensembles, physical point, continuum and excited-state systematics by Akaike criterion): gA^(u−d) = 1.250(24), which they state agrees with experiment; lattice precision (~2%) is ~20x worse than experimental lambda (~0.04%), so lattice gA cannot arbitrate the tau_n anomaly. (Note the PDG lambda is 1.2754(13); sign convention: lattice gA = |lambda|. Cirigliano 2022 indicates a percent-level radiative shift must be considered when comparing experiment with lattice.)
  SOURCE: Alexandrou et al. 2025, "Nucleon charges and σ-terms in lattice QCD", Phys. Rev. D 111, 054505 (arXiv:2412.01535 abstract), https://arxiv.org/abs/2412.01535
  QUOTE: "For the nucleon isovector axial charge we find $g_A^{u-d}=1.250(24)$, in agreement with the experimental value."
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RQ-18] CLAIM: Nab (ORNL SNS Fundamental Neutron Physics Beamline) first result is the full Dalitz plot of neutron β decay (electron energy > 100 keV) with new constraints on a hypothesised excited neutron state meant to explain the appearance/disappearance lifetime difference (arXiv:2508.16045, Phys. Rev. C 113, 035501, 2026). Nab's design goal is the electron–neutrino correlation a to Δa/a = 1e-3 and the Fierz term b; with the neutron lifetime that fixes Vud (a determines lambda independent of polarization). No value of a has been published yet as of the sources I found; Nab is reported as "taking data" in 2025 and in proceedings as "setting the stage for high precision physics data-taking" (Nov 2025).
  SOURCE: Gonzalez et al. (Nab), arXiv:2508.16045, https://arxiv.org/abs/2508.16045; Godri et al., PoS PSTP2024 067 (abstract via INSPIRE); Broussard et al., EPJ Web Conf. 378, 04001, arXiv:2511.16678, https://arxiv.org/abs/2511.16678
  QUOTE: "In addition, new constraints are placed on a possible excited neutron state, hypothesized to explain the disagreement between the appearance and disappearance neutron lifetime techniques." ; "aims to yield a precise measurement of the electron-neutrino correlation parameter, $a$, to $\Delta a/a=1\times10^{-3}$"
  ACCESS: abstract
  STATUS: peer-reviewed (PRC) / preprint for proceedings
  CONFIDENCE: medium

- [RQ-19] CLAIM: MY ARITHMETIC (CMS 2018 constant K = 4908.6 s; inputs as quoted above; not a source quotation). tau_beta predicted with Vud = 0.97367 (PDG superallowed): 879.41 s for PERKEO III lambda; 878.51 s UCNA; 881.25 s PERKEO II; 880.57 s PDG-average lambda (1.2754); 889.45 s with aSPECT-2020 (PDG) lambda 1.2677 and 890.50 s with the aSPECT reanalysis lambda 1.2668(27); 875.77 s with aCORN. Changing Vud to 0.97386 (Ma et al. lattice box) lowers these by about 0.34 s; using the EFT-2023 rate shift (+0.026%) lowers them by about 0.23 s. Sensitivities at lambda = 1.27641, Vud = 0.97367: dτ/dλ = −1144 s per unit λ (Δλ = 0.00087, i.e. 0.068% relative, per 1 s; 0.00044 or 0.034% per 0.5 s); dτ/dVud = −1806 s per unit Vud (ΔVud = 5.5e-4 per 1 s); the RC uncertainty on K (1.9 s) maps to 0.34 s in τ. A 10 s change in τ corresponds to Δλ = 0.0087 or ΔVud = 0.0055. Inverting: Vud = 0.97459 (UCNτ 877.75 s, PERKEO III), 0.97251 (Gravitrap 881.5 s), 0.96911 (beam 887.7 s); with a beam lifetime Vud would fall ~0.0055 below the superallowed value, i.e. a ~17σ disagreement with 0.97367(32), so the SM inputs strongly prefer the bottle side PROVIDED lambda comes from the beta asymmetry (PERKEO III, UCNA, PERKEO II) and not from a. (The constraints lens owns the official version of this calculation.) Note my bare-formula number for UCNτ (0.97459) is higher than the paper-quoted 0.97402 (RQ-14) for reasons not resolved (RQ-14 caution).
  SOURCE: derived, [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/quantitative_master_formula.py]
  SUMMARY: derived from RQ-01, RQ-03, RQ-05, RQ-12, RQ-16; see log beside the script.
  ACCESS: search-summary
  STATUS: secondary
  CONFIDENCE: medium

- [RQ-20] CLAIM: aSPECT reanalysis (Beck et al., PRL 132, 102501, 2024) supersedes the 2020 aSPECT value (PDG 2024 still lists the 2020 number −1.2677(28)): a = −0.10402 ± 0.00082 and lambda = −1.2668(27) (shift of −0.0009 from 2020, within the error), with Fierz term b = −0.0098 ± 0.0193 from a free fit (−0.041 ≤ b ≤ 0.022 at 90% CL). aSPECT and aCORN (a-coefficient, proton recoil) lie away from the beta-asymmetry values: aSPECT 2024 is (−1.2668 − (−1.27641))/ sqrt(0.0027²+0.00056²) ≈ 3.5σ (my arithmetic) from PERKEO III. A lambda ≈ −1.267 (aSPECT) would make tau_beta ≈ 890 s (RQ-19), closer to the beam value; this is the only lambda input that would favour the beam side, and it is an outlier in the PDG fit (scale factor 2.7).
  SOURCE: Beck et al. 2024, PRL 132, 102501 (arXiv:2308.16170), https://arxiv.org/pdf/2308.16170
  QUOTE: "Our new value for thea coefficient only differs marginally from the one published in [11] (see Table I) and is given by a =−0.10402± 0.00082 . (6) Using Eq. (2) we derive for λ the valueλ =−1.2668(27)."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RQ-21] CLAIM: Planned precision for lambda and correlations: PERC (FRM II Garching, 12 m superconducting magnet system, 8 m decay region, under construction per its 2019 design paper) aims at beta asymmetry and other coefficients at the 1e-4 level; ESS ANNI proposers state the priority "10^-4 accuracy for measurements of asymmetries in neutron decay with PERC- or PERKEO-III-like experiments" to improve Vud and the CKM unitarity test, and BRAND (11 correlation coefficients, transverse electron polarization, ILL PF1B) probes exotic couplings rather than lambda. Nab (ORNL SNS) aims at Δa/a = 1e-3 and is in data-taking; my estimate (not from a source): with a = (1−λ²)/(1+3λ²), da/dλ = −8λ/(1+3λ²)² ≈ −0.295 at λ = 1.2754 and a ≈ −0.107, so Δa/a = 1e-3 means Δa ≈ 1.1e-4 and Δλ ≈ 3.6e-4 (0.028%), about 1.5 times better than PERKEO III's quoted stat+sys (0.00045 and 0.00033). A Δλ of 0.00036 is about 0.4 s in τ_β. To decide between 878 s and 888 s (10 s), Δλ of about 0.0009 (≈1 s) already suffices, and PERKEO III (0.00056 when its errors are combined in quadrature, my arithmetic) already provides that for the beta-asymmetry route; the SM prediction limit is then the radiative-correction uncertainty (±1.9 s on K maps to ±0.34 s in τ_β) and Vud (±0.00032 maps to ±0.6 s). The real bottleneck is the spread among lambda inputs (aSPECT/aCORN versus beta-asymmetry), which Nab's a measurement and PERC will test.
  SOURCE: Wang et al. (PERC Collaboration) 2019, EPJ Web Conf. 219, 04007 (arXiv:1905.10249); ESS particle-physics input document arXiv:2506.22682 (https://arxiv.org/pdf/2506.22682); Godri et al., PoS PSTP2024 067 (abstract via INSPIRE)
  QUOTE: "The priorities of the proposers are in neutron beta decay (10 –4 accuracy for measurements of asymmetries in neutron decay with PERC- or PERKEO-III-like experiments [37, 47], in particularly improving the accuracy of Vud and of tests of the CKM unitarity" (arXiv:2506.22682); "The PERC (Proton and Electron Radiation Channel) facility is currently under construction at the research reactor FRM II, Garching." (arXiv:1905.10249 abstract)
  ACCESS: full-text
  STATUS: preprint (proceedings; PERC timeline not stated in the sources I opened)
  CONFIDENCE: medium

## Gaps
- No published numerical value of the Nab electron-neutrino correlation a was found (only the Dalitz-plot paper, arXiv:2508.16045, and detector proceedings); PERC first-data dates, BRAND/HIBEAM timelines not found in opened sources (PERC status via search summary only).
- Not opened: the Nab excited-neutron limit's numerical value (the paper states it constrains the Koch–Hummel type excited-neutron hypothesis; belongs to critiques/frontier).
- Not checked: FLAG 2024 lattice gA average (only the ETM 2024 value 1.250(24) was taken); CalLat / Mainz / other lattice gA values; the pion beta-decay Vud update (PIONEER); aCORN / UCNA successor status (UCNA+, aCORN final).
- Not resolved: how Cirigliano et al. 2023's Vud numbers (RQ-14) map onto the CMS-2018 master constant (5.7e-4 offset with bare formula, RQ-19).
- Not found/checked: a 2025 update to the PDG λ average, the PDG 2025 CKM review (unitarity sum may have changed with new Vus radiative corrections, Seng 2025 "sharpens the Cabibbo angle anomaly"; only abstract seen, no numbers); the Cabibbo-angle anomaly's relation to a beam-lifetime (would make Vud from neutron even lower).
- Note: one inline python heredoc (empty, no effect) was mistakenly executed once; no output was used.

