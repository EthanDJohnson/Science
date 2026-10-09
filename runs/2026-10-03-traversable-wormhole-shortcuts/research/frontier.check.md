# Check: frontier
status: final

Quotes checked with fetch_text.py --grep against arxiv.org abs/pdf full text. Covers RF-01 to RF-31 (relaunch 2026-10-08 added RF-22 to RF-31).

| Claim | Verdict | Note |
|---|---|---|
| RF-01 Kain: BHs form, EDM wormholes not traversable | verified | Quote exact. Paper also says it cannot rule out some other asymmetric EDM wormhole. Scope (specific parameters, spherical symmetry) correctly stated. PRD reference not independently checked. |
| RF-02 Kain R0 75-498 l_P, NEC violated | verified | Table I values 75.28 to 498.4 at mu-bar 0.2, e-bar/sqrt(4pi) 0.03; "two orders of magnitude" quote exact; Eq. 40 as stated. |
| RF-03 Konoplya-Zhidenko critique | verified | Both quotes exact. Paper also says "Apparently this kind of configuration could not exist in nature" about the symmetric solutions; omitted but not distorted. |
| RF-04 Churilova et al. / Stuchlik et al. | unverifiable | Abstract-only, not opened. Journal refs not checked. Low load-bearing. |
| RF-05 MM tidal 20g, r_e > 1.5e7 m, 0.05 s, N_f > 1e52 | verified | Eqs 3.26 and 2.16 match. Paper also gives RS II numbers in 3.27 (E_bin ~ -5e9 kg, gamma ~ 2e12, l ~ 3e3 ly with R5 = 50 micron) which the file omits. |
| RF-06 MM not a shortcut, <1 s vs tens of thousands of years, CMB blueshift | verified | Both quotes exact; "less than a second" is proper time; the exterior comparison is the authors' statement. |
| RF-07 MM "secret signals or qubits" | verified | Quote exact. |
| RF-08 Fu-Grado-White-Marolf t_min = d + logs | verified | Quote exact. Instability ~d^{3/2} and engineered cosmic strings confirmed. "No shortcut" gloss holds only as "approaches the minimum", "at least in higher dimensions". |
| RF-09 Emparan et al. multi-mouth F_2 vs F_3 | verified | Abstract confirms F2 vs F3 and the asymptotic flatness quote. |
| RF-10 Bilotta Kerr preprint | verified | ANEC quote exact; preprint status as stated. "First move toward astrophysical rotating BHs" is the file's gloss. |
| RF-11 Kontou long wormholes, DSNEC new result | verified | Quotes exact; DSNEC constraint on MMP stated as new in abstract. "DSNEC only in Minkowski / below curvature scale" not checked. |
| RF-12 achronal ANEC "free of counterexamples" | verified | Quote exact; correctly framed as review statement. |
| RF-13 Kobrin-Schuster-Yao | verified | Quote exact. "Seven Majorana fermions" detail not checked; five commuting terms confirmed. Preprint. |
| RF-14 Jafferis et al. reply | verified | Quote exact; "counterfactual", size winding 2<~t<~5, and t=2.8 artifact confirmed. |
| RF-15 Byun-Kim-Lee 2026 | verified | "First quantum-hardware realization ... explicitly chaotic" exact. Preprint. |
| RF-16 Byun et al. ANEC restatement | verified | Re-checked this pass: the ER bridge / "negative-energy shockwave violates the averaged null energy condition" sentence is in the full text (p. 1), wording matches the quote. |
| RF-17 Shapoval, Weinstein | unverifiable | Abstract-snippet pointers only, as admitted. |
| RF-18 Ahn et al., Liu-Miao | unverifiable | Search-summary only; no source opened. |
| RF-19 Avalos et al., Garattini et al. | unverifiable | Abstract snippets only. |
| RF-20 Bilotta review of MMP | verified | "Safe for human travel" sentence and interior instability confirmed. |
| RF-21 MM geometry and mass | verified | Eq. 2.5 matches. 1.5e7 m x 1.35e27 kg/m = 2.0e34 kg correct. Caveat: extremal BH mass, whereas the paper's binding energy is ~5e9 kg (3.27). |
| RF-22 Weinbaum: Einstein-Dirac no-go (PRD 114, 084004; 2607.28738) | verified | Both quotes exact (abstract and p. 45, 76 pages). Journal reference (PRD 114, 084004) not visible on the arXiv abstract text I fetched, so "peer-reviewed" is unconfirmed; treat as preprint-at-least. Claim is correctly scoped to Einstein-Dirac, and notes derivation unread. |
| RF-23 Freivogel et al.: scalars suppressed, fermions unit transmission (2606.12528) | verified | Quote exact (abstract, p. 4, p. 37); 69 pages. Preprint as stated. "sigma_r ~ A (omega r_e)^2" scaling not checked. |
| RF-24 Sadhukhan MMP stability (2609.33511, 2610.09847) | verified | Paper 1 abstract quote exact. Paper 2 "no growing mode for l>=2" exact, stated "within the O(alpha) truncation"; v1 dated 7 Oct 2026, so newer than 2026-10-01 holds. Assumptions (lowest Landau level only, q>>1, l<<sqrt q) confirmed. Single-author preprints. |
| RF-25 Kanai et al. no-go within EFT (2511.21017) | verified | Quote exact; abstract not truncated in the full text ("prevents the formation of the traversable throat structure"). PRD 113, 064026 reference not checked. |
| RF-26 Mondal et al. MMP echoes (2511.22671) | verified | Quote exact; J ~ pi L_wh/2 ~ 2.2e35 in r_* confirmed on p. 41. Note the abstract says distance "10^35"; file's 2.2e35 is the paper's J (one half of 2D). Units are the problem's own (tortoise coordinate), not stated as SI. |
| RF-27 Lu-Yang-Zheng channel capacity (2603.26051) | verified | Quote exact. The "|p+|Delta p+ ~< |a+|/G_N ~ g" bound and "one-shot" remark not checked. Preprint. |
| RF-28 Djogama et al. fermionic Kerr/CFT | unverifiable | Not opened this pass; abstract-only in source file. |
| RF-29 Chakrabarti; Pasten et al. | verified (Chakrabarti); unverifiable (Pasten) | Chakrabarti quote exact (4-page preprint, "comments welcome"). Pasten quote and CQG 43, 115014 reference not checked. |
| RF-30 Junior et al.; Blazquez-Salcedo et al. 2026 | unverifiable | Not opened; abstract-snippet only. |
| RF-31 Le S-lemma test, carried from warp run | verified | Abstract sentences exact (v-number not checked). Correctly scoped as warp-only application and preprint. |

Most serious problem: none contradicted or misattributed. The newest items (RF-22 to RF-24) are sound on quote wording, but RF-22's "peer-reviewed" status rests on a journal reference I could not see; and RF-04, RF-17 to RF-19, RF-28, RF-30 and the Pasten half of RF-29 remain unverifiable abstract or search-summary entries. RF-05 and RF-21 should be read with the paper's eq. 3.27 numbers.
