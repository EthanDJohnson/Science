# Prior-art check: van-den-broeck, angle "citations"

- Finding: Van Den Broeck 1999 (CQG 16, 3973; gr-qc/9905084): QI check not redone for the published (femtometre, v5) parameters; printed QI numbers belong to the Planck-scale (v1-v4) parameters.
- Angle: citation trail (INSPIRE refersto:arxiv:gr-qc/9905084)
- Date: 2026-10-27
- Source of finding: runs/2026-09-29-alcubierre-negative-energy/verdicts/C3-0.md (quick run, sources unchecked)

## Searches run
(append below)

## Works
(append below)

### S1 lit_search.py "refersto:arxiv:gr-qc/9905084" --source inspire --max 250 --sort mostrecent
- Returned 96 results (not "a few hundred"). Saved to scratchpad cit/citing_all.txt. Titles scanned. Candidates for opening (QI / warp-bubble analyses): VdB gr-qc/9906050; Krasnikov gr-qc/0207057; Lobo-Visser gr-qc/0406083; Lobo LNP 617 gr-qc/0204038; Finazzi-Liberati-Barcelo 0904.0141; Bobrick-Martire 2102.06824; Alcubierre-Lobo 'Warp Drive Basics'; Santiago-Schuster-Visser 2105.03079; Lobo book 0710.4474; Loup et al gr-qc/0107097; Barzegar et al 2407.00720 and 2602.16495 ('demystification', 'errors in the literature'); Helmerich 2404.03095 (Warp Factory); Barcelo-Finazzi-Liberati 1001.4960; Finazzi 'Quantum effects in warp drives' 2013; Ridgely physics/0010027; Hart et al gr-qc/0207109; Pfenning-Ford is NOT in list (it predates, is cited BY VdB).

### S2 fetch_text.py greps of first-priority citers (own runs this session; outputs in scratchpad cit/)
- Krasnikov gr-qc/0207057 (PRD 67 104013), section "2. Van Den Broeck's trick", footnote 8 [p.18] VERIFIED (fetch_text --grep "original paper"): "8 We take r different from that proposed in the original paper [23], because the latter, first, leads to a much (by ~ 10^36) greater amount of exotic matter and, second, violates the quantum inequality (e. g. in w = 0.98)." [23] = C. Van Den Broeck, CQG 16, 3973 (1999). Context p.19: his own pocket needs ~ -10^-3 g (Planck-size capsule); so 10^36 x 1e-3 g = 1e33 g = 1e30 kg ~ matches v5's E_II,- = -1.4e30 kg => Krasnikov compared with the CORRECTED (v5/CQG) energy, not v1-v4's -3.4e-3 kg. No computation shown, no parameters quoted, no mention of eq.(7) change or of printed QI numbers. Acknowledges Ford, Pfenning, Fewster.
- VdB gr-qc/9906050 v4 (STAIF-2000 talk) [p.4] VERIFIED: "Using this scheme, the required total energy can be reduced to stellar magnitude, in such a way that the QI is satisfied. On the other hand, the energy densities are still unreasonably large, and the spacetime has structure with sizes only a few orders of magnitude above the Planck scale." (restates claim, no re-check, no parameters). Summary [p.5]: grep 'Planck'. 
- Lobo-Visser gr-qc/0406083 [p.1] VERIFIED: "To reduce the enormous amounts of exotic matter needed in the superluminal warp drive, van den Broeck proposed a slight modification of the Alcubierre metric which considerably ameliorates the conditions of the solution [24]." Only other mention is ref [24] and in p.2 comparison with Gravel-Plante Krasnikov tubes. No QI recheck. => unrelated/background citation.
- Finazzi-Liberati-Barcelo 0904.0141: "Broeck" occurs only in the reference list ([8] C. Van Den Broeck, CQG 16, 3973 (1999)); text cite as [8] still to be located.
