# Check: engineering
status: final

| Claim | Verdict | Note |
|---|---|---|
| RE-01 GP-B -37.2+/-7.2, -6601.8+/-18.3 mas/yr | verified | arXiv abstract matches exactly; 7.2/37.2 = 19%. |
| RE-02 LARES/LAGEOS 0.9910+/-0.0006 +/-0.02-0.04 | verified | Matches arXiv PDF text. The arXiv abstract page gives only "+/-0.02", but the PDF has the quoted wording. Journal ref (EPJC 79, 872) not opened. |
| RE-03 LARES 2 launch 13 Jul 2022; 0.2% claim; Iorio dispute | verified | "claimed to be able to perform in the near future a LT test accurate to ~0.2%" found in Iorio's PDF. The "launched on July 13, 2022" phrase did not match my grep, probably PDF line-break; not separately confirmed. POLARES and EPJC 85, 255 not checked. The 0.2% is Ciufolini's claim as reported by Iorio. |
| RE-04 Archimedes 5e-16 N, 4e6 s, 7e-13 N/sqrt(Hz) | verified | Sapienza IRIS preprint matches. Version is the submitted preprint, not the MDPI final. |
| RE-05 15 dB squeezing; GEO600 6.03 dB | verified (partly) | The 15 dB quote is in the PDF of arXiv:2411.07379. That arXiv posting is dated Nov 2024, v2 Mar 2026, and lists the 2016 PRL DOI, so "arXiv v2 of PRL 117" is plausible. The 16 mW pump, the "all GW observatories since 2019" and the Lough 6.03 dB figures were not opened. The "tens of orders gap" is explicitly not computed. |
| RE-06 Maclay and Davis QI violated | verified | Quotes match the PDF ("violated by most of the experimental data"; "brings into question the basis for QI"). The "contested, minority" framing is the researcher's judgement, which is fair. |
| RE-07 QET on IBM hardware | verified | Quote matches. The "few-qubit" characterisation was not checked. |
| RE-08 DCE, 11 GHz, ~0.05c | verified (partly) | The 11 GHz SQUID and the "few percent of c" length change match. The specific "0.05c" figure is not stated literally in what I read, so treat it as approximate. Two-mode squeezing is confirmed. |
| RE-09 Tajmar EmDrive null | verified | Crossref abstract confirms the double pendulum, battery power and null result. The "two orders of magnitude" sentence is cut off in the printed abstract; the Springer page was blocked. Wording unconfirmed beyond the truncation, which is consistent. |
| RE-10 White-Juday critique | verified | 4.4 J/m^3, Schwarzschild radius 1.92e-23 m and the conclusion wording match the PDF. Note the paper assumes 1e6 V/m (it says the field is not specified in the literature). The "Physics Essays 29, 201" reference was not checked. |
| RE-11 Parker 430,000 mph | verified | NASA wording matches. Conversions are correct: 192.2 km/s = 6.4e-4 c, and 0.04c is about 62x faster. Minor point: Parker is a ~600 kg probe, not a 1e5 kg payload, which the claim's own wording concedes. |
| RE-12 592.2 EJ; mass-energy arithmetic | verified | IEEJ text matches. 5.922e20/c^2 = 6.6e3 kg; 4.49e27 kg x c^2 = 4.0e44 J = 6.8e23 world-years; KE at 0.04c = 3.2e41 J. All recomputed OK. The 4.49e27 kg shell mass is not checked here (it belongs to the quantitative facet). |
| RE-13 NIF 2.08 MJ -> 8.6 MJ | verified | LLNL text matches. 8.6e6/c^2 = 9.6e-11 kg. |
| RE-14 Nanodiamond 460 GPa, >1 TPa; graphene 130 GPa | verified | Europe PMC text matches. Lee 2008 abstract (Crossref) matches; it literally says "130 gigapascals for bulk graphite" (the monolayer's intrinsic strength, expressed as a 3D equivalent). The CNT 80 GPa figure is search-summary only: unverifiable. |
| RE-15 DART -33.0+/-1.0 min | verified (partly) | Matches the arXiv abstract. 11.372 h and 4.7x were not found by grep (likely in the full text or formatted differently). The note that the mass/delta-v remarks are unsourced is appropriate. |
| RE-16 AD/ELENA bunches; antimatter mass | contradicted (as written) / correction verified | The quote matches the PDF. The claim text's "1e-8 kg/yr" and "~1e18" are wrong. The appended correction is right: 1e7 x 1.673e-27 = 1.67e-20 kg; about 1.5e5 bunches over ~214 d gives 2.6e-15 kg; 2mc^2 is about 4.6e2 J; ~4e19 below 1e5 kg. Use the corrected figures only. |
| RE-17 90 mg gold sphere gravity coupling | verified | The arXiv abstract confirms "two gold spheres of approximately 1mm radius and 90mg mass". The "smallest source mass" wording rests on a search summary, which is unverified. "25+ orders" is conservative: the mass ratio to Jupiter is about 31 orders. |
| RE-18 3e-24 /sqrt(Hz) at 40 Mpc | verified | The quote matches the Living Review PDF exactly. The Goryachev/Lasky and Clough claims were not checked. |
| RE-19 Archimedes status 2025 | unverifiable | The abstract quote was not re-opened. It is plausible given RE-04. |
| RE-20 Glenn 2025 spark-gap fringe shift | unverifiable | Paper and abstract not opened. The 33-orders estimate depends on an assumed 1 GJ/m^3 over 1 mm; it is illustrative only. |
| RE-21 Astrum Drive SBIR | verified | The company page quote is confirmed: "We received funding from the National Science Foundation SBIR Phase I Project Grant in partnership with The Morningbird Foundation to test our warp-drive framework in a lab." The 3 Oct 2023 date is also on the page. The "two counter-rotating EM fields" claim was not checked. |
| RE-22 Analogue gravity | verified (partly) | Steinhauer arXiv 1510.00621 exists, titled "Observation of quantum Hawking radiation..." (the quote itself was not grepped). Barcelo 2022 is "Chronology Protection Implementation in Analogue Gravity" (title confirmed, claim content not). The 0.25c cap is correctly flagged by the researcher as unverified. |

## Overall
- No misattribution in the load-bearing numbers.
- The one real error is RE-16's headline figures. They are self-corrected in the file, but a downstream reader must use the corrected values.
- RE-05's Vahlbruch arXiv ID corresponds to a 2024 posting; cite the journal DOI (PRL 117, 110801) as the primary reference.
