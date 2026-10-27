# Prior art: Gambini, Porto & Pullin 2004 (PRL 93, 240401), the eq. (5) coefficient and the black-hole information claim
status: final
Checked: 2026-10-27. Finding dated 2026-09-29.

## The finding

Source in this repository: `runs/2026-09-29-problem-of-time-quantum-gravity/verdicts/C6-0.md` (point 1 and calculation part D). Its script is `runs/2026-09-29-problem-of-time-quantum-gravity/calc/falsifier-C6-0_gpp_bound.py`.

**The paper.** R. Gambini, R. A. Porto and J. Pullin (GPP), "Realistic clocks, universal decoherence and the black hole information paradox", Phys. Rev. Lett. 93, 240401 (2004), arXiv:hep-th/0406260. arXiv has only v1, dated 28 Jun 2004.

**What the paper says:**
- Eq. (2) is a Lindblad-type master equation, dρ/dT = −i[H, ρ] − σ(T)[H,[H,ρ]].
- The rate for an optimal black-hole clock is σ(T) = t_P (t_P/(Tmax − T))^(1/3).
- Eq. (4) gives a two-level black hole with gap ω12 = 1/((8π)² t_P) · (t_P/(Tmax − T))^(1/3).
- Eq. (5) gives log(ρ12(T)/ρ12(0)) = i∫ω12 dT′ + (1/(8π)²) log((Tmax − T)/Tmax).
- The abstract concludes that "all information is lost through the fundamental decoherence before the black hole can evaporate".

**Our points:**
- **Point 1 (coefficient).** Eqs. (2) and (4), with the stated σ, give ω12²σ = 1/((8π)⁴(Tmax − T)). The coefficient in eq. (5) should therefore be (8π)^-4 = 2.5e-6, not the printed (8π)^-2 = 1.58e-3.
- **Point 2 (black-hole claim).** With either coefficient, coherence vanishes only in the limit T → Tmax.
  - One Planck time before evaporation, the coherence left is 0.650 (solar mass, Tmax = 6.6e74 s) and 0.794 (1e12 kg) with the printed coefficient. With (8π)^-4 it is 0.9993 and 0.9996.
  - One e-fold of decoherence is reached only within 10^-199.5 s (solar mass) or 10^-254.4 s (1e12 kg) of evaporation. Both are far below t_P = 10^-43.3 s.
  - So the abstract's claim does not follow from the paper's own formulas at any resolvable time.
- **Caveat.** We had not opened GPP's longer derivation, New J. Phys. 6, 45 (2004).

## Verdict

**Partly anticipated.** No paper, comment, reply or erratum states point 1, the mismatch between eqs. (4) and (5). Nobody has published our Planck-time numbers.

Point 2 is partly anticipated by the authors themselves. Their 2005 Braz. J. Phys. paper (gr-qc/0501027) says the PRL's formula "is not a valid expansion for t = Tmax". It replaces "erased completely" with a finite residual of about 10^-28, from a different calculation that still claims large decoherence.

Third-party critiques of the black-hole claim exist, but on conceptual and structural grounds, not numerical ones: Okon & Sudarsky 2016, Unruh & Wald 2017, Anastopoulos et al. 2022.

## Is the finding itself right?

**The numbers are right. Two parts of the wording need tightening.** I re-derived everything independently in `checks/2026-10-27-prior-art/calc/gpp_judge_check.py`. Five scripts by the searchers and the verifier agree with it.

**Confirmed against the primary text** (arXiv v1, with `fetch_text.py` re-run today):
- Eq. (4) prints (8π)² in ω12, and eq. (5) prints the coefficient 1/(8π)².
- The text after eq. (5) reads "when time reaches the evaporation time T = Tmax, the density matrix element vanishes".
- The abstract sentence is verbatim.
- OpenAlex shows the published PRL abstract is identical to the arXiv one.

**Confirmed by calculation** (sympy and mpmath):
- σω12²(Tmax − T) = a², where a is the prefactor in eq. (4). The printed a = (8π)^-2 gives k = 1/(4096π⁴) = 2.506e-6. The printed eq. (5) has 1.583e-3, a mismatch of (8π)² = 631.7.
- Coherence left at Tmax − t_P is 0.650202 (solar mass, Tmax = 6.618e74 s) and 0.794248 (1e12 kg). With k = (8π)^-4 it is 0.999319 and 0.999635.
- One e-fold is reached at Tmax − T = 10^-199.50 s and 10^-254.40 s.

**Wording 1: point 1 over-asserts which equation is wrong.**
- In their earlier paper (hep-th/0405183) the authors use ω = kT/ħ = 1/(8πM), with a single 8π. Combined with the PRL's convention Tmax = M³ t_P, that gives exactly the printed eq. (5) coefficient, (8π)^-2. So eq. (4)'s extra 8π may be the misprint.
- Against that, the authors print (8π)² in ω12 again in 2005 (eq. 12, refereed text) and in 2007 (eq. 19).
- So the correct statement is "eqs. (4) and (5) are mutually inconsistent as printed, by a factor (8π)²". "The coefficient should be (8π)^-4" is too strong.

**Wording 2: point 2 holds for the printed formulas only.** That is how the finding words it. It is not a robust statement that the mechanism cannot work.

The exponent is k = (gap/clock-rate scale)² × (σ normalisation). The crude model leaves each of these factors loose by more than the margin involved.

My own checks (assumptions stated in the script):
- **The threshold is close.** Reaching one e-fold of decoherence by Tmax − t_P needs k ≥ 1/ln(Tmax/t_P). That is 3.68e-3 for a solar-mass hole, only 2.3 times the printed k, and 6.9e-3 for 1e12 kg, 4.3 times the printed k. A 10^-28 residual at Tmax − t_P needs k ≈ 0.24.
- **The exact Hawking lifetime does not change k.** Suppose the exact lifetime 5120π M³ t_P is used in both the gap and the clock resolution, δT = c1·M·t_P. Then the 5120π cancels, and k = c1²/(96π²) = 1.06e-3 · c1². That is close to the printed value when c1 = 1. One e-fold at a Planck time needs c1 ≈ 1.9, and a 10^-28 residual needs c1 ≈ 15. GPP do not fix c1.
- **One mixed convention gives k ≈ 1.** The versions searcher put the exact lifetime into ω only and kept the PRL's σ. That gives k ≈ 1.009 and a coherence of 7e-120 at Tmax − t_P. This mixes conventions, but it shows how much rides on the constants.
- **The authors' own later σ shrinks k.** Their 2005 normalisation of σ (a factor 1/36) lowers k further. With the printed k it leaves 0.988 of the coherence at Tmax − t_P for a solar-mass hole.

**The caveat is resolved, not realised.** NJP 6, 45 (gr-qc/0402118) contains no black-hole evaporation calculation. "evapor" has no match in its text, and its only black-hole sentence defers to a paper "in preparation". It does not fix the coefficient or σ(T).

**Could not check.** The typeset PRL body could not be read: APS, link.aps.org and the LSU repository PDF all returned 403. A change to eq. (4) or (5) during refereeing therefore cannot be excluded. The published abstract and the refereed 2005 follow-up were readable.

**Context for the wording.** The PRL body already hedges: "we have taken a very crude model for the black hole and a more detailed calculation is needed". The abstract is stronger than the body. That should be said as "the abstract overstates the body", not presented as a hidden flaw.

## Point by point

| Our point | Status | Closest prior work (citation, link, date, status) | Verified quote |
|---|---|---|---|
| 1. Eqs. (2) and (4) with the stated σ give k = (8π)^-4; eq. (5) prints (8π)^-2 | **Not found.** Should be reworded as "inconsistent as printed" | Authors' earlier paper: Gambini, Porto & Pullin, IJMPD 13, 2315, [hep-th/0405183](https://arxiv.org/abs/hep-th/0405183), May 2004, peer-reviewed. It does not state the mismatch, but its single-8π frequency reproduces eq. (5). The (8π)² is repeated without comment in Braz. J. Phys. 35, 266 (2005), eq. 12, and in GRG 39, 1143 (2007), eq. 19 | "If we now consider a black hole, the energy fluctuations in the system are characterized by, kT = ħ/8πM, which yields a frequency, ω = kT/ħ = 1/8πM (we use units in which G = c = 1.)" |
| 2a. Coherence vanishes only as T → Tmax; 0.650 / 0.794 left at Tmax − t_P; one e-fold only within 10^-199.5 s / 10^-254.4 s | **Partly anticipated, by the authors only.** They concede the PRL formula is invalid at Tmax and replace complete erasure with a finite residual. Our numbers are not found | Gambini, Porto & Pullin, "Fundamental decoherence in quantum gravity", Braz. J. Phys. 35, 266, [gr-qc/0501027](https://arxiv.org/abs/gr-qc/0501027), Jan 2005, peer-reviewed proceedings (the refereed text via redalyc carries the same sentences) | "Even though strictly speaking it is not a valid expansion for t = Tmax, one can show that it is a good approximation to the exact result provided τ(t) << Tmax − t". Also: "The calculation in [8] yielded the remarkable result that it erased completely the information by the time evaporation occurs. In this paper we have integrated the full evolution equation and again one finds that there is a large level of decoherence by the time of evaporation." |
| 2b. The abstract's "all information is lost … before the black hole can evaporate" does not follow from the paper's own formulas | **Partly anticipated.** The authors softened the claim. Third-party critiques exist on different, non-numerical grounds | Authors: GRG 39, 1143, [gr-qc/0603090](https://arxiv.org/abs/gr-qc/0603090), 2006/2007, peer-reviewed. Third party: Okon & Sudarsky, Found. Phys. 46, 852, [arXiv:1512.05298](https://arxiv.org/abs/1512.05298), 2015/2016, peer-reviewed (conceptual). Unruh & Wald, Rep. Prog. Phys. 80, 092002, [arXiv:1703.02140](https://arxiv.org/abs/1703.02140), 2017, peer-reviewed (does not name GPP) | GRG: "So we can say that the paradox is effectively eliminated for large black holes and we cannot say for sure for smaller ones using this simplified analysis." Okon & Sudarsky: "the puzzle, when formulated in terms of the fundamental physical laws, is still present, and it only seems to disappear when we look at things in a less precise way." Unruh & Wald: "Markovian evolution would not be an appropriate model for black hole evaporation, since the black hole clearly should retain a "memory" of what energy it previously emitted." |
| Caveat: NJP 6, 45 might fix the coefficient or σ(T) | **Resolved.** NJP has no black-hole calculation | Gambini, Porto & Pullin, New J. Phys. 6, 45, [gr-qc/0402118](https://arxiv.org/abs/gr-qc/0402118), Feb 2004, peer-reviewed | "It may play a role in founda tions of quantum mechanics, in solving the black hole information problem [24], and may be observed experimentally." Ref. [24] is "(in preparation)" |

## Closest prior work

**The authors' own revision: Braz. J. Phys. 35, 266 (2005), gr-qc/0501027.**
- This is the only work that overlaps a core point.
- The authors call the PRL result a first-order expansion that "is not a valid expansion for t = Tmax". They redo the calculation with a clock-window average and get |ρ12(Tmax)| ~ (M_P/M_Sun)^(2/3) ~ 10^-28 |ρ12(0)|. They call this "a large level of decoherence".
- Footnote [14] says the PRL used "an estimated σ(t)", and that the explicit value carries a factor 1/36.
- The paper keeps (8π)² in ω12 (eq. 12) and never mentions the eq. (4)/(5) mismatch.
- So it anticipates the qualitative part of point 2: the PRL's "vanishes at Tmax" result is not trustworthy near Tmax. It reaches the opposite practical conclusion, by a different mechanism (phase averaging over the clock window, not the Lindblad term), and without our numbers.
- A side observation: (M_P/M_Sun)^(2/3) is 4.9e-26, not 1e-28. Two agents' evaluations of the authors' eq. (16) give 4.9e-23. This is not part of our finding.

**The authors' later restatements.** These soften the claim, and none revisits eq. (5):
- **GRG 39, 1143 (2007), gr-qc/0603090.** It calls the result "a naive estimate" and says the paradox is "effectively eliminated for large black holes and we cannot say for sure for smaller ones". It prints ω12 with (8π)² again (eq. 19).
- **"Discrete space-time", gr-qc/0505023 (2005).** It says a solar-mass hole "would have de facto become a mixed state".
- **GRF essay, IJMPD 15, 2181 (2006), gr-qc/0611148.** It says only that "the order of magnitude of the speed of the effect is appropriate".
- **Later Montevideo-interpretation and loop-quantum-gravity black-hole papers** (2008-2020). These never return to the clock-decoherence black-hole estimate.

**The authors' predecessor: IJMPD 13, 2315 (2004), hep-th/0405183.**
- It uses ω = kT/ħ = 1/(8πM) with a single 8π and calls the extrapolation "a rough order-of-magnitude estimation".
- It is the authors' own evidence that eq. (5), not eq. (4), may be the intended form.

**Third-party critiques.** All are different from our points:
- **Okon & Sudarsky (2016).** Replying to Crull's reading of "Gambini et al.", they argue that in fundamental time the evolution is still unitary, so the puzzle is relocated rather than solved. The argument is conceptual and has no calculation.
- **Anastopoulos & Hu (CQG 25, 154003, 2008).** They criticise GPP's conditional-probability derivation of the master equation, not the black-hole application.
- **Anastopoulos, Hu et al. (AVS Quantum Sci. 4, 015602, 2022) and Unruh & Wald (2017).** They argue in general terms that black-hole non-unitarity is incompatible with Markovian master equations. Neither names GPP at that point.
- **Butterfield (2015), Baez & Olson (2002) and Ng & van Dam (2003).** They dispute the clock-accuracy premise behind σ(T). This is background to the finding's wider verdict (C6-0 point 4), not to points 1 and 2.

**Neutral citers.** Flanagan (2005), Smith & Ahmadi (2019), Okon & Sudarsky (2014), Nandi et al. (2026) and Coppo et al. (2026) cite GPP without checking any formula.
- The 2004 Physics Forums thread checks no formula either. One poster wrote "so far no one has pointed out any flaw in the GPP paper".

**Unverified.** Y. Li, "Non-Markovian Gravitational Decoherence and the Black Hole Information Paradox", Int. J. Theor. Phys. 63, 293 (2024), doi:10.1007/s10773-024-05837-y.
- It cites GPP according to INSPIRE, but only a truncated abstract could be read.
- Whether it criticises GPP's Markovian eq. (2)/(5) is unknown. PAPER TO REQUEST.

## Coverage

**Primary text:**
- arXiv v1 of the PRL, from the TeX source, the rendered pages and `fetch_text.py`. There is no other arXiv version.
- The published abstract, via OpenAlex.
- The typeset PRL body was not read: APS, link.aps.org and the LSU repository PDF all returned 403.

**The authors' related papers**, all read in arXiv text:
- NJP 6, 45 (2004), IJMPD 13, 2315 (2004), Braz. J. Phys. 35, 266 (2005; also the refereed text via redalyc), gr-qc/0505023 (2005), quant-ph/0507262 (2005), GRG 39, 1143 (2007), IJMPD 15, 2181 (2006) and Found. Phys. 37, 1074 (2007).
- Montevideo-interpretation papers (2008-2020) and LQG black-hole papers (2014-2019), checked by keyword search of the extracted text only.

**Not read:**
- The Gambini-Pullin 2012 chapter in Fundam. Theor. Phys. 172 (no free copy).
- A 2008 chapter that could not be located.
- Their textbook.

**Citation trail:**
- INSPIRE lists 86 citers of the PRL. All 86 abstracts were scanned. About a dozen were opened in full, and the 8 newest were re-listed today with nothing new.
- Semantic Scholar gave 81 citers, 24 of them with context snippets.
- A full-text regex sweep covered 147 arXiv citers of the PRL and five follow-up papers. It catches citations by author name only, not bare bracket numbers.
- INSPIRE shows no erratum, comment or related record, and no citer title with comment/reply/erratum/critique. zbMATH Open has no entry.

**Web:**
- WebSearch, including searches restricted to Stack Exchange, PhysicsOverflow, physics blogs and phys.org, found only the 2004 Physics Forums thread.
- newscientist.com, reddit and mathoverflow were not reachable by the search tool.

**Rate limits and blocked sources:**
- OpenAlex cited-by listings and parts of Semantic Scholar were rate-limited.
- Li 2024, Crull 2015 (known only through Okon & Sudarsky's quotation) and the APS April 2005 meeting abstract (403) could not be opened.
- Talks, referee reports and unindexed material cannot be searched.

**Dates.** All sources predate the finding (2026-09-29).

## What this means

**What is new.**
- The mismatch in point 1, a factor (8π)² = 632 between eqs. (4) and (5) of a 2004 PRL, has apparently never been noted. It is real but small-scale: the authors' own earlier paper suggests it is a misprint in eq. (4), not an error in the result.
- Our Planck-time numbers for point 2 are also new. Its substance, that the PRL's "vanishes at Tmax" result rests on a formula invalid near Tmax, is something the authors conceded themselves in 2005. They have stated the claim in softened form ever since, so the critique is aimed at a position they no longer hold.
- Point 2 is also fragile beyond the printed constants. The printed exponent is only a factor 2-4 below the value that would give real decoherence by a Planck time. The crude model's constants, such as the clock-resolution factor and the σ normalisation, move it by more than that.

**What to do with it.**
- It is not worth a paper or a formal Comment.
- A short, courteous note to Gambini and Pullin would be reasonable. It should flag the eq. (4)/(5) inconsistency, phrased as "inconsistent as printed", and ask which form is intended.
- Inside our own C6-0 verdict, the wording should change. Point 1 should read "inconsistent as printed". Point 2 should read "the PRL's printed formulas do not support the abstract at resolvable times, as the authors' 2005 paper effectively concedes", rather than suggesting the mechanism itself fails.
