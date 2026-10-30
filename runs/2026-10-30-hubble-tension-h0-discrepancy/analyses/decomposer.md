# Analysis: decomposer (methodical doubt and decomposition)
status: final

## Method applied
The question ("what dominantly causes the local ~73 vs early ~67–68 H0 gap, and what would decide it") is rewritten as a tree of sub-questions that each end in a calculation, measurement or cited result; every premise used by the question and the dossier is entered in an assumption ledger and classified (measured / derived / assumed / unknown); the load-bearing assumption is named with its test; and sub-questions are sorted into settled vs open.

## Findings

F1. **Gap size depends on the pair chosen, by a factor ~7 in significance.** H0DN-corrected (73.264 ± 0.806 [D-22]) minus CMB-SPA (67.19 ± 0.38 [D-44]) = +6.07 ± 0.89 km/s/Mpc, 9.0%, 0.188 mag in 5 log10 H0, 6.8σ (uncorrelated). SH0ES 2025 (73.49 ± 0.93 [D-20]) vs CMB-SPA: +6.30 ± 1.00, 0.195 mag, 6.3σ. Against DESI BAO+BBN (68.50 ± 0.58 [D-45]): 4.8σ (H0DN), 4.6σ (SH0ES). CCHP TRGB (70.39, total σ 1.94 [D-24]): 1.6σ vs CMB-SPA, 0.9σ vs BAO+BBN; CCHP JWST-only (68.81 ± 2.25 [D-25]): 0.7σ and 0.1σ. [calc: runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-decomposer_partitions.py]

F2. **Partition test (premise 2).** On a minimal-overlap set of ten results, one per method class (SH0ES, CCHP TRGB, SBF, TDCOSMO-2026, masers, sirens, CMB-SPA, DESI BAO+BBN, r_s-free BAO 69.6 [D-49], equality 65.1 [D-50]), one common H0 gives χ² = 49.7 for 9 dof (p = 1.3×10⁻⁷, ~5.3σ). The best two-group split found by exhaustive search is "all local (ladders + one-step) vs all early-type (CMB, BAO+BBN, r_s-free BAO, equality)": χ² = 8.5/8 (p = 0.39). "All distance ladders vs everything else" gives 11.2/8; "r_s-using vs not" 12.6/8; "SH0ES alone vs everything else" 16.9/8 (p = 0.03), i.e. Δχ² = 8.5 worse than early-vs-local. The next-best splits (dropping CCHP or sirens from the local group) are within Δχ² ≤ 0.4: the data cannot tell where CCHP or the one-step methods belong. [calc: same file]. Caveat: shared NGC 4258 anchor and shared SNe not modelled (see F6).

F3. **The significance is carried by the SN/Cepheid distance ladder.** One-step methods alone (TDCOSMO + masers + sirens, 71.27 ± 1.93): 2.1σ vs CMB-SPA, 1.4σ vs BAO+BBN. All local except SH0ES (71.56 ± 1.19): 3.5σ / 2.3σ. SBF + one-step (no SN ladder, 72.26 ± 1.51): 3.3σ / 2.3σ. All local: 72.76 ± 0.73, 6.7σ / 4.6σ. This matches the TDCOSMO companion's 2.7σ after excluding the whole ladder [D-57, D-90]. [calc: same file]

F4. **Required size vs published levers (gap 0.188 mag = 9.0%).** Measured bounds: JWST–HST Cepheid photometry, 2σ upper 0.07 mag = 37% of gap [D-09, D-78]; reddening correction total 0.03 mag = 16% [D-15]; dropping the metallicity term 0.012 mag = 7% [D-23]; ΛCDM cosmic variance 0.010 mag per σ, gap = 19.6σ [D-10]. Contested proposals: Wojtak–Hjorth two-population SNe 0.087 mag = 47% [D-35]; Percival selection sum 0.078 mag = 42% [D-88]; Dong peculiar velocities 0.087 mag = 47% [D-82]; MW parallax offset 0.019 mag ≤ 10% [D-86]. No single named ladder effect reaches the full gap; ~2 of the contested ones would have to add coherently. [calc: same file]

F5. **New-physics fits without a SH0ES prior close part of the gap.** Relative to 67.19 → 73.26: ACT DR6 EDE 69.9 closes 45%, PMF 69.1 31%, modified recombination 69.6 40%, Planck NPIPE EDE upper 69.5 38%, Poulin 2026 EDE 71.0 63%, eROSITA+ EDE 71.4 69% (residual 1.9 km/s/Mpc) [D-52, D-53, D-94]. DESI w0wa moves H0 the wrong way (63.6: −59%; with Pantheon+ 67.51: +5%) [D-51, D-12]. [calc: same file]

F6. **Null model (underestimated errors).** To bring H0DN vs CMB-SPA to 3σ the ladder σ must be 1.99 km/s/Mpc (×2.5 the quoted 0.806); to 2σ, ×3.7. With ladder errors ×2.5 the ten-result set is consistent with one H0 ≈ 67.9 (χ² = 16.3/9, p = 0.06); inflating the early errors ×3 still fails (p = 0.004). An error-budget null therefore must be a *ladder* null; it cannot be spread evenly. [calc: same file]

F7. **Reframe arithmetic.** For H0 = 73.26 at the CMB-SPA H0·r_d, r_d = 134.8 Mpc (8.3% below 147.00); at DESI DR2 h·r_d = 101.54 Mpc, 138.6 Mpc (5.7%). For CCHP's 70.39: 4.6% and 1.9%. The ladder–inverse-ladder M_B difference is 0.12–0.14 mag [D-21], comparable to but not commensurate with the 0.19 mag H0 gap (different SN systems). [calc: same file]

F8. **Shared-ladder correlation lowers the significance; it doesn't change the best partition.** I added a common offset σ_c, correlated across SH0ES, CCHP and SBF, as a stand-in for the shared NGC 4258 anchor and shared SN zero point. Local vs early-type then falls from 6.4σ (σ_c = 0) to 5.6σ (0.5), 4.4σ (1.0), 3.5σ (1.5) and 3.0σ (2.0 km/s/Mpc). "Local vs early-type" stays the best two-group split at every σ_c, with χ² 8.2–8.5/8. "SH0ES alone vs the rest" stays worst (12.7–16.9). A ~1.5% common-mode ladder error, about the NGC 4258 distance error, is enough to take the combined local value from "decisive" to ~4σ. [calc: runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-decomposer_correlated.py]

F9. **Precision a deciding ladder-free, r_s-free H0 needs.** Separating "true H0 = CMB-SPA ΛCDM", which covers every ladder-side cause including the M_B/G_eff variant, from "true H0 = 73.26" needs σ(H0) ≤ 2.0 km/s/Mpc (2.9%) at 3σ and ≤ 1.2 (1.7%) at 5σ. Separating "true = 67.19" from the best surviving EDE fit (71.0) needs ≤ 1.27 (1.8%) at 3σ and ≤ 0.76 (1.1%) at 5σ. Separating BAO+BBN 68.5 from EDE 71.0 needs ≤ 0.83 (1.2%) at 3σ. Naive 1/√N scaling from TDCOSMO-2026 (3.3% with 11 lenses [D-31]) gives about 30 lenses for 2%, 53 for 1.5% and 120 for 1%, ignoring the MSD floor [D-16]. Sirens need about 35× the GWTC-5.0 information for 2% (from 11.8% [D-33]). [calc: same file]

F10. **There is still no reply in the SH0ES–CCHP selection dispute.** A search found only Percival's selection-effect preprint, already in the dossier [D-88]: [new: arXiv:2607.22425 (Percival 2026), abstract via lit_search, "selecting objects using one observable while analyzing another can also lead to a selection bias"]. It also turned up a Hoyt, Jang, Freedman et al. 2026 ApJ paper on ladder systematics, whose treatment of the selection argument could not be confirmed: [new: WebSearch, search-summary, SUMMARY "the closest match is a May 2026 ApJ paper by Hoyt, Jang, Freedman and colleagues, which focuses on systematics in distance-ladder H0 measurements ... can't confirm the details of its response"]. This leaves gap §6 of the dossier open.

## Lens-specific outputs

### Sub-question tree

Root Q: what dominantly causes the gap between the local (~73) and early-type (~67–68) H0, and which feasible measurement would decide it?

- **Q1. Is there a gap to explain, and how big?**
  - Q1a. Size in km/s/Mpc, % and mag for each defensible pair. Settled by calculation (F1): 6.1 ± 0.9 km/s/Mpc, 9.0%, 0.188 mag (H0DN vs CMB-SPA).
  - Q1b. Significance once correlations are included. Partly settled: 6.8σ uncorrelated, falling to 3.5–4.4σ with a 1–1.5 km/s/Mpc common ladder offset (F8). The statistician owns the full covariance.
  - Q1c. Does the gap survive dropping the SN/Cepheid ladder? Settled (F3, [D-90]): 2.1–3.5σ, depending on which non-ladder methods enter.
- **Q2. Which partition of the data is the real one?** (premise 2)
  - Q2a. χ² for the competing two-group splits. Settled for a minimal-overlap set (F2, F8): local vs early-type is best, all-ladders vs rest is close (Δχ² ≈ 2.7), and SH0ES vs rest is worst (Δχ² ≈ 8.5).
  - Q2b. Where do CCHP and the one-step methods belong? Open: the data cannot place them (Δχ² ≤ 0.4, F2).
- **Q3. Can the early side be wrong?**
  - Q3a. A systematic in a single CMB experiment? Settled: Planck, ACT and SPT each give 66.5–67.6 [D-02, D-41–D-43], and BAO+BBN, which uses no CMB anisotropies, gives 68.5 [D-08].
  - Q3b. An error-budget failure on the early side? Settled: inflating the CMB and BAO+BBN errors ×3 still fails (p = 0.004, F6).
  - Q3c. Does the H0 value depend on the model? Yes [D-01]. This makes Q4 open-ended rather than settling anything.
- **Q4. Can new physics move the early-type inference to ~73?**
  - Q4a. Early-time. Settled at the bound level: fits without a ladder prior reach 69.1–71.4 and close 31–69% of the gap (F5, [D-52, D-53, D-94]). Open at the 2σ level: does the residual 1.9–4.2 km/s/Mpc close with Simons Observatory, SPT-3G Ext and DESI final? See also the D-83 dispute.
  - Q4b. Late-time H(z). Settled: the inverse ladder [D-70, D-07] rules it out, and DESI w0wa lowers H0 [D-12, D-51].
  - Q4c. A late-time change of M_B or G_eff that leaves H(z) alone. Open and speculative [D-92]. Its only constraint is unverifiable [D-82, RC-32].
- **Q5. Can the local value differ from the global one?**
  - Q5a. ΛCDM cosmic variance. Settled: 0.31 km/s/Mpc, so the gap is 19.6σ of it [D-10, F4].
  - Q5b. A void outside ΛCDM. Settled against: SN Hubble-diagram bounds [D-11, D-77]. Only a minority preprint dissents [D-97].
  - Q5c. Flow corrections. Settled: they raise local H0 (+0.6 km/s/Mpc for SNe) [D-36].
- **Q6. Can the ladder be wrong by 0.19 mag?**
  - Q6a. Cepheid photometry and crowding. Settled against as a sole cause: at most 0.07 mag at 2σ [D-09, D-78, F4].
  - Q6b. Metallicity, dust and reddening. Settled as small: each 0.01–0.03 mag [D-15, D-23].
  - Q6c. Anchors. Mostly settled: leave-one-anchor-out runs move H0 by ≤ 0.4 km/s/Mpc [D-23]. The MW parallax offset is ≤ 0.02 mag [D-86]. Gaia DR4 (Dec 2026) re-tests it.
  - Q6d. SN standardisation, calibrator vs Hubble flow. Open: Wojtak–Hjorth 0.087 mag [D-35] against Huang (unverifiable) [D-82]. No SH0ES reply.
  - Q6e. Calibrator or Cepheid selection. Open: Percival 0.078 mag [D-88], Li 2026's 11 omitted hosts [D-27], and SH0ES's distance-limited 72.6 ± 2.0 [D-28].
  - Q6f. Peculiar velocities in the SN intercept. Open: Dong 0.087 mag [D-82] against H0DN's 6.8σ [D-22].
  - Q6g. Do non-SN ladders independently give ~73? Partly settled: SBF gives 73.8 ± 2.4 [D-29] and TF 73.3 ± 4.1 [D-30], but both share calibrators and anchors (NGC 4258, TRGB). H0DN without SNe gives 73.43 ± 1.80 [D-23].
  - Q6h. Do the SH0ES and CCHP differences come from method, sample or SN photometry? Open [D-80, D-81, F10].
- **Q7. What decides it?**
  - Q7a. Required precision. Settled (F9): a ladder-free, r_s-free H0 at 1.1–1.8% (σ ≈ 0.8–1.3 km/s/Mpc).
  - Q7b. Who, and when? Partly open: time-delay lensing at ~30–50 lenses (TDCOSMO and successors), LVK sirens (O5 timeline "in discussion"), Gaia DR4 for the anchor [dossier §6].

### Assumption ledger

| # | Premise | Used by | Class | Basis / what it rests on |
|---|---|---|---|---|
| L1 | θ_* is measured model-independently to 0.03% | early inference | measured | [D-01, D-40] |
| L2 | Flat ΛCDM holds from recombination to today when turning θ_* into H0 | CMB H0 | assumed | [D-01]. w0wa lowers H0 [D-51]. |
| L3 | Standard pre-recombination physics, so r_s and r_d are as in ΛCDM (147.00 Mpc) | CMB H0, BAO+BBN, inverse ladder | assumed | This is what early-time new physics denies. Constraints in [D-52, D-53, D-74]. |
| L4 | BBN ω_b from deuterium | BAO+BBN | measured (plus nuclear-rate input) | [D-46]. The d(p,γ) rate shift is unverified. |
| L5 | SN Ia standardisation does not evolve with z | inverse ladder, late-time no-go | assumed, partly tested | Popovic: < 0.1 km/s/Mpc [D-07]. The DES5Y–Pantheon+ offset is 0.04 mag [D-85]. |
| L6 | Calibrator-host SNe standardise like Hubble-flow SNe | every SN ladder | **assumed** | Contested [D-35, D-82]. This is untested by any independent team. |
| L7 | Cepheid photometry is unbiased by crowding | SH0ES | measured (SH0ES team) | ≤ 0.03 mag [D-09, D-78]. No independent-team JWST re-reduction is in the dossier. |
| L8 | The geometric anchors are correct (NGC 4258, LMC, MW, SMC) | all ladders and masers | measured | NGC 4258 ~1.5% [dossier §6]. MW offset −14 ± 6 µas [D-86]. Leave-one-out ≤ 0.4 km/s/Mpc [D-23]. |
| L9 | Different ladders have independent errors (no common mode) | combined-local significance | **assumed** | NGC 4258 and Pantheon+ are shared [dossier §7]. Untested in amplitude. F8 shows the significance is sensitive to it. |
| L10 | The calibrator sample is not selection-biased | SH0ES and CCHP | assumed | Contested [D-27, D-28, D-88]. |
| L11 | Local H0 equals global H0 to within cosmic variance | ladder → H0 | derived (ΛCDM N-body) | [D-10]. Tested by SN void bounds [D-11]. |
| L12 | The one-step methods' systematics are under control (MSD, lens mass profiles, maser PVs, siren selection) | one-step H0 | partly measured | MSD widens the error ×4 [D-16]. The lens-model choice moves H0 by ~8 km/s/Mpc [D-91]. |
| L13 | Errors are Gaussian and the quoted budgets are complete | every σ count | assumed | The null candidate tests this. F6 shows the ladder budget would need ×2.5. |
| L14 | "H0" means the same thing in each method: the FRW ȧ/a at t0 | the comparison itself | assumed (definitional) | Fails under backreaction or timescape (not covered [D-97]) and under G_eff(z) [D-92]. |
| L15 | GR holds and G is constant from the Cepheid hosts (z ~ 0.005) to the Hubble flow (z ~ 0.1) | ladder M_B transfer | assumed | It is the M_B/G_eff escape [D-92]. |
| L16 | Superseded values are correctly identified, and preprints are taken at face value | inputs | derived (dossier §7) | Many key 2026 inputs are preprints: TDCOSMO-2026, masers, Percival, Dong, Riess 2025. |
| L17 | My minimal-overlap set treats SBF and CCHP as independent of SH0ES | F2 and F3 | assumed (approximation) | F8 partly relaxes this. |

### Load-bearing assumption

**L9 together with L6: "the SN-calibrated distance ladders carry no common-mode error at the primary-indicator → SN Ia calibration step larger than their quoted budgets".**

- **Why it is load-bearing.** Every route to a > 4σ tension goes through it. Take out the SN/Cepheid ladder and the remaining local evidence sits 2.1–3.5σ from the CMB and 1.4–2.3σ from BAO+BBN (F3). A shared ~1.5 km/s/Mpc offset (0.045 mag) cuts the combined local–early split to 3.5σ (F8). If L9 or L6 fails at the 0.1–0.19 mag level, the question changes. It is no longer "what new physics explains a 6σ gap" but "why do ladder-free late methods sit 1–2σ high", which the null or a small early-time shift can absorb. If L9 and L6 hold, the gap is real and the answer must be new physics. Within new physics, L3 (standard r_d) then decides the early-vs-late verdict, because the inverse ladder kills every pure H(z) change [D-70].
- **Secondary load-bearing premise.** L3 decides *which* new physics; L9 and L6 decide *whether* new physics is needed at all.
- **Tests.**
  1. Decisive, ladder-free: a strong-lensing time-delay or siren H0 at ≤ 1.2–1.3 km/s/Mpc (≈ 1.7–1.8%). It must be independent of both r_s and SN calibration. This separates "true H0 ≈ 67–68.5" from "true H0 ≥ 71" at 3σ, and from 73 at 5σ (F9).
  2. Within the ladder, L6: an analysis by a team other than SH0ES of the same calibrator-host and Hubble-flow SNe, with host-matched standardisation. Use the same host type, or cut the Hubble flow to star-forming spirals, and see whether M_B moves by ≥ 0.08 mag.
  3. Within the ladder, L10: one rule-based, distance-limited calibrator set analysed by both teams with all three primary indicators. [D-28] is a first SH0ES-side version, 72.6 ± 2.0.
  4. L8: Gaia DR4 (Dec 2026) MW Cepheid parallaxes.

### Settled vs open sub-questions

| Sub-question | Status | Settled by / what is missing |
|---|---|---|
| Q1a gap size | settled | F1 |
| Q1b correlated significance | open (partly) | statistician's full covariance; F8 gives the range |
| Q1c gap without the SN ladder | settled | F3, [D-90] |
| Q2a best partition | settled (on current data) | F2, F8: local vs early-type |
| Q2b CCHP and one-step placement | open | needs ≤ 1.5% one-step H0 and a resolved CCHP–SH0ES sample question |
| Q3a/Q3b early-side systematic | settled (against) | [D-02, D-08], F6 |
| Q4a early-time new physics, full closure | settled (no full closure without a ladder prior), open (partial closure plus a residual) | [D-52, D-53, D-83, D-94], F5 |
| Q4b late H(z) | settled (against) | [D-70, D-12] |
| Q4c M_B/G_eff transition | open (speculative) | no verified test in the dossier |
| Q5 local structure | settled (against) | [D-10, D-11, D-36] |
| Q6a–c photometry, metallicity, dust, anchors | settled (each too small alone) | F4 |
| Q6d–f SN standardisation, selection, PVs | open | no replies [dossier §6], F10 |
| Q6g non-SN ladders | partly settled | they share anchors and calibrators |
| Q6h SH0ES vs CCHP | open | [D-80, D-81] |
| Q7a precision | settled | F9 |
| Q7b schedule | partly open | dossier §6 lists no collaboration targets |

## Calculations

- `runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-decomposer_partitions.py` (log beside it) computes:
  - gap sizes in km/s/Mpc, % and mag for 4 local × 3 early pairs (F1);
  - χ² of five named two-group partitions, plus an exhaustive search over all two-group splits of a 10-result minimal-overlap set (F2);
  - the tension with blocks of local evidence removed (F3);
  - each ladder lever as a fraction of the 0.188 mag gap (F4);
  - the fraction of the gap each new-physics fit closes (F5);
  - the error inflation the null needs (F6);
  - the r_d needed and the M_B differences (F7).
  - Key results: χ²(one mean) = 49.65/9; best split, local vs early-type, 8.48/8; SH0ES vs rest 16.94/8; one-step only vs CMB-SPA 2.07σ; ladder error ×2.47 for 3σ.
- `runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-decomposer_correlated.py` (log beside it) computes:
  - a GLS partition fit with a common ladder offset σ_c = 0–2 km/s/Mpc. The local–early split goes 6.42σ → 2.99σ, and the partition ranking is unchanged (F8);
  - the one-step H0 precision needed to separate the candidates' predictions, plus naive lens and siren counts (F9).
- Neither script models the full published covariance (shared Pantheon+ SNe, shared CMB data). Both use symmetrised asymmetric errors.

## Candidate answers (at least 3; the null and a reframe count)

- [DECOMPOSER-A] **Distance-ladder systematic (common mode at the SN-calibration step).**
  - Claim: the dominant cause is a ~0.1–0.19 mag error shared by the SN-calibrated ladders. It is most likely a combination of SN standardisation differences between calibrator and Hubble-flow hosts [D-35], calibrator or Cepheid selection [D-88, D-27], and Hubble-flow peculiar-velocity treatment [D-82]. Cepheid photometry, metallicity, dust and anchors are each too small alone (F4).
  - Predicted shifts: ladder → about −6 km/s/Mpc once corrected; CMB, BAO+BBN and inverse ladder unchanged; one-step methods converge to 67–68.5.
  - Collateral: none on S8, N_eff, the damping tail or stellar ages (the GC age mildly favours a low H0 [D-79]).
  - Weakest link: no single named effect is big enough. About two contested effects must add coherently, and SBF (73.8 ± 2.4) and one-step methods (71.3 ± 1.9) both sit high, at about 1.6–2σ. The ladders do share anchors.
  - status: **surviving** (strained on the "which effect" level).
  - Test: a ladder-free H0 at ≤ 1.3 km/s/Mpc comes out at ≤ 69. A non-SH0ES re-standardisation with host-matched Hubble-flow SNe moves M_B by ≥ 0.08 mag.
  - confidence: medium.
- [DECOMPOSER-B] **Early-time new physics shrinking r_s (EDE first, then varying m_e, modified recombination, PMF, dark radiation).**
  - Claim: the true H0 is ~71–73 and r_d ~ 135–140 Mpc.
  - Predicted shifts: CMB/BAO ΛCDM values wrong by +3 to +6; inverse ladder rises with r_d; one-step methods ~71–73; ladder unchanged.
  - Collateral: higher ω_c, n_s and S8 for EDE; changes to the damping tail and TE.
  - Weakest link: fits without a ladder prior reach only 69.1–71.4, closing 31–69% of the gap (F5). ACT/SPT/Planck NPIPE bounds give f_EDE < 0.06–0.07 [D-75]. N_eff = 2.86 ± 0.13 rules out dark radiation [D-74]. Varying m_e fails with DESI DR2 [D-76]. The pro-EDE results (Poulin 71.0, eROSITA 71.4) come from partial data sets [D-83].
  - status: **strained**. It can be the dominant cause only if the residual 2–4 km/s/Mpc is ladder systematics, which makes it a hybrid with A.
  - Test: SO/SPT-3G damping-tail and EE/TE data detect f_EDE > 0 at ≥ 3σ without a ladder prior. A ladder-free H0 lands at 71–73 with ≤ 0.8 km/s/Mpc error (separating it from 68.5 at 3σ, F9).
  - confidence: low–medium.
- [DECOMPOSER-C] **Null: statistical fluctuation plus underestimated errors spread over several measurements, no single dominant cause.**
  - Status: **strained** in its "spread evenly" form. Inflating the early errors ×3 still leaves p = 0.004 (F6), and three independent CMB experiments plus BAO+BBN agree. A "ladder budget underestimated ×2.5" version survives, with p = 0.06 for one H0 ≈ 67.9 (F6). That version is A without a named cause.
  - Distinguishing test, against A: under C, larger calibrator samples and team-independent analyses drift towards ~69–70 with no single variable (host colour, mass, selection, distance) carrying the residual. Under A, a specific variable carries it.
  - confidence: low.
- [DECOMPOSER-D] **Reframe: the anomaly is an SN Ia M_B (calibration) disagreement of 0.12–0.19 mag between the ladder and r_d-calibrated SNe, not a disagreement about the expansion rate.**
  - The narrower reframe "SH0ES vs everything else" is **strained**: on current data it is the worst two-group partition, Δχ² = 8.5 worse than local vs early-type (F2, F8), because CCHP and the one-step methods lean high.
  - The M_B framing is **surviving**, and it clarifies the slate. Both A and the speculative G_eff/M_B transition [D-92] act on M_B. Only B, together with the one-step methods, makes a claim about the global ȧ/a. So the deciding observable is any H0 that bypasses both M_B and r_d.
  - Test: the same as the load-bearing test. A ladder-free, r_s-free H0 at ~1.5% decides "M_B problem" (≈ 67–68.5) against "H0 problem" (≥ 71).
  - confidence: medium.
- [DECOMPOSER-E] **Late-time new physics.**
  - (i) H(z) variants (phantom, w0wa, interacting DE): **eliminated**. The inverse ladder [D-70, D-07] rules them out, and DESI w0wa lowers H0 to 63.6–67.5 (F5).
  - (ii) Low-z M_B/G_eff transition [D-92]: **strained**. It is speculative, needs a G change of about 10% at z ≈ 0.01, and has no independent support.
  - Test for (ii): it predicts one-step H0 ≈ 67–68 (like A) but a ladder that stays at 73 under every re-standardisation. It also predicts a step in SN residuals at z ≈ 0.01 that peculiar-velocity-corrected SN samples (ZTF DR2+) could detect.
  - confidence: low.
- [DECOMPOSER-F] **Local structure (void or bulk flow): eliminated.**
  - The gap is 19.6σ of ΛCDM cosmic variance (F4, [D-10]). The SN Hubble diagram excludes |δ| > 20% at 4–5σ [D-11]. Flow corrections raise local H0 rather than lowering it [D-36].
  - Test: a void predicts that H0 from z < 0.05 differs from H0 at 0.05–0.15, and that one-step methods at z ~ 0.5 (lenses) give ~67. The H0DN Hubble-flow-cut variants differ by only ~0.5 km/s/Mpc [D-23].
  - confidence: high (for elimination).
- [DECOMPOSER-G] **Early-universe analysis systematic (CMB likelihood or foregrounds, BAO reconstruction): eliminated as dominant.**
  - Planck, ACT and SPT each give 66.5–67.6 [D-02]. BAO+BBN gives 68.5 without CMB anisotropies [D-08]. A_L is gone in PR4 [D-79a]. Inflating the early errors ×3 still fails (F6).
  - Residual: the 2.3–2.8σ DESI–CMB Ω_m discrepancy [D-87] could move the early-type value by ~1 km/s/Mpc (67.2 → 68.5), about 20% of the gap.
  - Test: SPT-3G Ext and SO agree with Planck at 0.3 km/s/Mpc; DESI final BAO+BBN stays ≤ 69.
  - confidence: high (for not-dominant).

## What would change my mind

- **Towards A or the M_B reframe (D):**
  - a TDCOSMO or sirens H0 at ≤ 1.5% centred ≤ 69;
  - an independent-team SN re-standardisation or calibrator-selection analysis that moves the SH0ES ladder to ≤ 70;
  - Gaia DR4 shifting the MW anchor by ≥ 0.05 mag.
- **Towards B:**
  - an SO/SPT-3G detection of f_EDE (or of an m_e or recombination change) at ≥ 3σ without a ladder prior, with H0 ≥ 71;
  - one-step methods converging at ≥ 72 with ≤ 1.5% error;
  - SBF/TF ladders recalibrated on JWST-only anchors staying at 73–74.
- **Against my sorting:** a shared NGC 4258 anchor error of ~2% found by an independent geometric anchor would weaken the whole "local" block at once (F8). That would make C more viable.
- **Towards E(ii):** a significant step in Hubble-residuals at z ≈ 0.01 in large PV-corrected SN samples, with no host dependence.

## Assumptions I relied on

- Dossier values as given. Asymmetric errors are symmetrised. TDCOSMO-2026, masers, Percival, Dong and Riess 2025 are preprints taken at face value (L16).
- My minimal-overlap set treats CCHP, SBF and SH0ES as independent apart from the explicit common-offset test in F8 (L17). The r_s-free BAO value used (69.6) is one of three correlated DESI DR1 variants [D-49]. The equality value is pre-DESI [D-50].
- CMB-SPA 67.19 ± 0.38 is the early reference. H0DN's 67.24 ± 0.35 is not reconciled with it [D-44]; the difference is immaterial here.
- "Fraction of gap closed" is measured against 67.19 → 73.26 and also against each paper's own ΛCDM. The two disagree by ~10 percentage points.
- The new-physics candidates are treated as mutually exclusive with A. A hybrid (partial EDE plus partial ladder systematic) is noted under B and not scored separately.
