# Check: theory
status: final

Checked against fetch_text.py output (arxiv.org/pdf, text as fetched; B&O version label not printed by tool). Gibbons/Springer pages blocked.

| Claim | Verdict | Note |
|---|---|---|
| RT-01 B&O eq. 5, h_c = Pauli-Jordan field, coherent state | verified | Quote matches p.2. The "S = T exp[...] eq. (1)" form and "used as in-state" were not located by grep (no match for "S=T"); that part is the researcher's reading. Pauli-Jordan = ret minus adv is standard knowledge, B&O only call it "Pauli-Jordan function". |
| RT-02 outgoing spherical wave packet, burst dt~1/sigma_w | verified | Quote matches p.2 (text just before eq. 5 region). The top-hat Theta = sqrt(2 pi^2 N/(w_s sigma_w)) form was not grepped; not load-bearing. |
| RT-03 eq. 6 amplitudes and eq. 7 (s^2-2tu)/s | verified | Eq. 6 (A++++ = A---- = 8 pi G t^2/s, A++-- = A-++ = 8 pi G u^2/s) and eq. 7 prefactor 4 pi G/(2pi)^6 and delta_{mu1 mu2} match p.2. Eq. 7 says "unpolarized graviton state". Interpretation (equal-sign coherent sum) is inference. |
| RT-04 supplement S3 on-shell intermediate graviton drops out | verified | Quote matches SM p.9. "Every bilinear combination" and "even if states were different" not grepped separately; the passage says the other three bilinears are "handled analogously". |
| RT-05 2 pi delta(0) -> T, T~1/sigma_w, provided 1/sigma_w >> tau | verified | Matches SM p.10 (S6). |
| RT-06 eqs. 8-10, "tau << dt ~ 1/sigma_w, Poissonian sqrt(sigma_w tau)" | verified | Quote matches p.3. "Pair rate" reading (photons = 2 x pairs) is inference but consistent with "each reaction removes two gravitons and generates two photons". |
| RT-07 "equivalent to creation of photons in a background h_c at second order" | verified | Matches p.2. Not "in the average sense" detail; that appears in footnote 3 (p.3) about photon direction, consistent. |
| RT-08 Gibbons 1975 results and scope | unverifiable | Full text blocked. INSPIRE abstract confirms: massive scalar field, plane sandwich wave of arbitrary profile and polarization, no particles, Feynman propagator exact, any reasonable regularisation of <T> must vanish. "without hindrance" ending not confirmed, and the researcher's "ACCESS: full-text" is overstated (abstract only). Scope note (scalar, massive) correct per abstract: the abstract says MASSIVE scalar, which strengthens the researcher's own caveat. |
| RT-09 Khusnutdinov EPJ Plus 141, 532 | verified | Abstract quote matches (arXiv:2508.11558). Journal reference/DOI not independently checked. Note: the paper treats scalar and vector fields (p.6), consistent. |
| RT-10 Redi-Tesi N_dec formulas, c_J values, null-like no production | verified | eq. 5 with -c_J/(30720 pi), c_0=4/3, c_1/2=4, c_1=16, and "null-like tensor and vector perturbations do not produce particles" all match (p.4, p.6). Eq. 6 coefficient c_J/(2560 pi) quoted in the claim also present. Preprint status correct. The interpretive "first-order near zone" gloss is inference. |
| RT-11 Khusnutdinov tension, beta ~ delta(k_v+l_v) | verified | Both quotes match (p.2, p.7). Source says the Bogolyubov claims (refs 26-28) are for massless scalars; "photons" flux wording appears in the p.7 sentence. "Exact for non-collinear massless" is the researcher's gloss. |
| RT-12 Tourrenc 1970, Skobelev 1975, Gibbons Green function | verified | Refs [23],[24],[25] match reference list; Gibbons/DeWitt-Schwinger sentence matched in the text of paper per quote (reference list and intro seen). Skobelev dating is by citation only. |
| RT-13 Cristofoli et al. abstract | verified | Abstract matches. Inference about S|0> as in-state is the researcher's and flagged as partial in Gaps. |
| RT-14 Caron-Huot et al. | verified | Abstract and Sec. 4.4 quotes match (p.1, p.26); retarded products appear in the reduction formula. The in-out/in-in "first order agree" is flagged as inference by the researcher. |
| RT-15 Bjerrum-Bohr et al. amplitudes and cross section | verified | Eq. 5.2/5.4 match, agreement with Skobelev stated. Caveat: the quoted "only nonvanishing" list in the paper also includes longitudinal D1(00;++) = 8 pi G su/t, which the paper then argues is unphysical in the massless limit; the claim's omission is acknowledged by its own scope sentence. Crossing to gg->gamma gamma is the researcher's inference but standard. |
| RT-16 B&O "all the hbar disappear ... classical process" | verified | Matches p.3. Context: it is stated for the background-photon stimulated-emission case; the claim says so. Eq. 11 shows linear-in-hbar for the vacuum power, which the claim does not mention (B&O: "quantumness comes from the energy of photons"). |
| RT-17 Jones, McDougall, Singleton PRD 95, 065010 | verified | Abstract matches arXiv:1610.02973. Journal ref consistent with Khusnutdinov ref [26] (page printed as 65010). |
| RT-18 Garriga-Verdaguer 1991 | unverifiable | Abstract not re-fetched. Khusnutdinov's attribution (beta=0 for massive; Pauli-Villars confirmation of Gibbons for scalars; beta ~ delta(k_v+l_v)) confirmed. |
| RT-19 Dorca-Verdaguer wave-packet quantisation | verified | Both quotes match arXiv:gr-qc/9403015 p.3 and abstract. Journal refs not checked. |
| RT-20 Deser 1975 | unverifiable | Search-summary only, as the researcher states (confidence low). Not checked. |

Verdict counts: verified 16, unverifiable 3 (RT-08, RT-18, RT-20), contradicted 0, misattributed 0, status-wrong 0.

Main issues: RT-08 labelled full-text but only the abstract could be confirmed; the Gibbons abstract says "massive scalar", so the extension to photons rests on Khusnutdinov and Deser (unverified). RT-01's in-state reading of the S-matrix eq. (1) was not located in the fetched text.
