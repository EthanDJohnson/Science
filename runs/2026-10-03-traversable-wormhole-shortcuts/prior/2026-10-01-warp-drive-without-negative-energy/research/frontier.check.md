# Check: frontier
status: final

Method: fetch_text.py greps of arXiv abstract pages and PDFs, plus Crossref for journal references. Abstract-only claims were checked against the abstract only; body-level numbers were not re-derived.

| Claim | Verdict | Note |
|---|---|---|
| RF-01 (Bolívar et al., E_min ~ v²R⁴/(4Δ³)) | verified | Abstract wording matches exactly, including the "sharp constant 1/4". It is a preprint. The "slice-dependent, not ADM mass" caveat is not in the abstract I read, so that part is unchecked. |
| RF-02 (Le, radiative steering, v4) | verified | The abstract has the strict surface DEC, e^(-3L) and "Self-gravitating settling ... remains open". The quote joins two sentences with an ellipsis. The abstract also says self-similar shells have growing normal modes, which the claim omits. |
| RF-03 (Le, Warpax, 73%) | verified | The quote matches. The abstract says the comparison covers "subluminal and superluminal speeds". It also states that the type labels and fractions are samples distinct from the interval bounds. |
| RF-04 (Rodal, 38x, 2.6e3x, 60x) | verified | The abstract matches. Crossref gives GRG, issue 1, published 2025-12-17 and print Jan 2026, so the peer-reviewed status holds. arXiv v1 was submitted 19 Dec 2025, after journal publication; this is odd but not a contradiction. The 0.04% figure was not checked. |
| RF-05 (Le, elastic shells) | verified | The abstract wording matches. Preprint. |
| RF-06 (Garattini & Zatrimaylov, de Sitter) | verified | The abstract matches; the only difference is the "non--negative" hyphenation. The claim's caveat that the energy conditions hold only "up to a total divergence term that averages to zero" is correct. |
| RF-07 (Jusufi & Lobo) | verified | The "Exotic matter remains necessary ..." text and the "effective ansatz" statement are in the abstract. The abstract grep did not directly display E = -(15π/1024) v_s² l, so that formula was not seen. |
| RF-08 (Fell & Loeb, >1 TW) | verified | The abstract matches. It also says low-velocity or at-rest bubbles would not produce such luminosities. The "10% c" figure was not checked. |
| RF-09 (Clough et al.) | verified | The abstract matches. It explicitly acknowledges "a requirement for negative energy", consistent with the claim. Peer-reviewed status was not checked against a journal record. |
| RF-10 (Lentz & Felton) | verified | The abstract matches. It says "positive energy sources potentially sourced by known classical physics", which is an assumption, not a calculation. |
| RF-11 (Barzegar et al. review) | verified | Consistent with the PDF, which contains the Theorems IV.31-33 and Errors. The exact quote was not re-grepped. Preprint. |
| RF-12 (Buchert & Frackowiak) | verified | The "expected generic instability" quote matches. Crossref confirms Universe 12(5) 132, issued 2026-05-03. |
| RF-13 (Bolívar et al., boundary obstruction) | verified | The abstract has p_r = -ρ, p_perp = -ρ - rρ'/2 and the NEC/WEC violation. The abstract goes on to "close the adjacent unit-lapse, curved-sli..." (truncated); the claim's lapse-release statement was not seen in my excerpt. |
| RF-14 (Chowdhury, Martel-Poisson) | unverifiable | Not opened. It is a low-stakes side claim. |
| RF-15 (Le, momentum accounting) | verified | The PDF quote "An observer needs a force ... freely falling test observers in the interior are inertial" and the vanishing Bondi news are confirmed. The Lemma 2.1 rocket-equation statement and "zero flux leaves momentum fixed" were not grepped. The "does not beat a photon rocket" conclusion is the researcher's inference but is consistent with the text. |
| RF-16 (Rodal v = c scope) | verified | The PDF quote matches exactly. This is a useful scope limit on RF-04. |
| RF-17 (Barzegar Thm IV.32) | verified | The PDF has "Theorem IV.32. The Natário zero-expansion warp drive violates the WEC" and the proof as quoted. Theorem IV.31 (Natário 2002: violates WEC or SEC) is also present. Preprint. |
| RF-18 (Barzegar on Fuchs, Santiago) | verified | "refuted correctly (fully or partially) by Santiago et al." and Error 18 are confirmed in the PDF. The claim that the 2024 shell was refuted rests on Error 18 alone (the TOV argument). Contested preprint critique; the claim already flags this. |
| RF-19 (Fell & Loeb, zero ADM mass) | verified | The PDF quote matches. |
| RF-20 (Sellers et al., second-hand) | verified | The Fell & Loeb sentence about Sellers et al. [15] is exact. The primary source was not found, and the claim already marks it low-confidence and secondary. |
| RF-21 (Rodal, metamaterial coupling) | unverifiable | Not opened. Low-stakes. |
| RF-22 (Rodal, Natário 35x) | verified | The abstract has the 35x quote. arXiv lists "International Journal of Theoretical Physics, Volume 63, Article 168, (2024)", and Crossref gives 8 Jul 2024. The 2025 arXiv posting is later than the journal year, as the claim notes, so the claim's own concern is resolved. The abstract also says Mattingly et al. underestimated the curvature invariants by 21 orders of magnitude. |
| RF-23 (Shirokov, Bondi dipole) | verified | The abstract has the numbers: 0.056c at t=400, momentum zero to ≲1%. Requires negative active mass; preprint. |
| RF-24 (Abellán; Bolívar, paywalled) | unverifiable | Not opened. The claim is already labeled low-confidence and based on abstract fragments. |

Summary: 20 verified, 3 unverifiable (RF-14, RF-21, RF-24), 0 contradicted, 0 misattributed, 0 status-wrong. The researcher's stated statuses (preprint or peer-reviewed) match what I could check. The most serious open caveat is RF-16: Rodal's "predominantly positive" results are for v = c only, so nothing here supports a positive-energy superluminal drive. Several 2026 preprints (Le's) are revised repeatedly, so their numbers are moving.
