# Misophonia Indieproj — 1:1 Update (Process Version)

> Reference document for your own prep — the reasoning trail behind the clean version, in case Prof. Hur asks "why does this look different" or wants to go deeper on any step. Not meant to be read aloud.

---

## 1. Where v2 stood

v2 (2026-08-21/24) proposed the registration/appraisal (S/A) model as "the first competitive quantitative test of an existing cognitive model's central claim" — honest about not being a new framework, but the novelty statement was vague (didn't name which specific literature gap it closed).

## 2. Self-review pass (reviewer-standard critique applied to our own design)

Applied the same rigor standard used earlier on a labmate's RI-CLPM paper, to our own proposal:

- **Discriminant validity of S and A themselves was never tested** — we'd controlled for SPSQ/OCI-R (adjacent constructs) but never asked whether MAIA-2/BPQ and ASI-3 are separable from *each other*. Added as a mandatory step-zero analysis (§3.4 of v3).
- **Causal-chain language overclaimed relative to design** — the "sensation → registered → appraised → severity" figure implies temporal sequence; every actual test (H1–H6) is correlational/cross-level, not sequential. Flagged for either softening the figure or being explicit that ordering isn't tested this year.
- **"Gating" was being used as a name for an interaction term, not a tested mechanism** — added a pre-specified functional-form test (simple-slope comparison: does registration→severity slope differ at high vs. low appraisal, vs. just being uniformly amplified) so "gating" isn't claimed until that specific pattern is shown.
- **Layer 3 ROI definition was underspecified** — originally said "atlas-based, TBD." Now specified: Nord, Lawson & Dalgleish (2021, *AJP*) meta-analytic coordinates for posterior/mid insula (need to pull exact MNI coordinates from the paper before building the mask — not yet done), cross-checked against a Neurosynth/NeuroQuery term-based map for the anterior-insula locus, so no ROI is picked from our own contrast (avoids circularity/double-dipping).

## 3. Considered and rejected: AI brain-modeling tools

Asked whether newer AI models (Meta's TRIBE v2; "Digital Twin Brain" / The Virtual Brain-style disorder simulators) could shortcut the neural analysis. Both rejected, for different reasons — worth having the reasoning ready if asked about "using AI for the fMRI analysis":

- **TRIBE v2**: an encoding model (stimulus → predicted BOLD), trained on naturalistic movies/podcasts/text, built for *group-average* prediction of *new stimuli*, not individual-difference prediction. Our task stimuli (short trigger-sound clips, block-design body-attention instructions) are out of its training distribution, and it has no mechanism for relating a trait score to an individual's regional response — which is exactly what H7 needs.
- **Digital Twin Brain / Virtual Brain-style models**: closer in spirit ("disease simulation"), but built on structural-connectivity data (our protocol doesn't include diffusion imaging) and trained/validated on population-scale consortia (IMAGEN, STRATIFY — thousands of subjects), not a single-site N=80 clinical sample. Applying one would require access/collaboration with the originating group and far more engineering than the planned SPM route.
- Conclusion: the literature-coordinate ROI approach (Nord 2021 + Neurosynth/NeuroQuery) remains the right-sized tool for this specific, targeted hypothesis test.

## 4. Literature landscape (verified 2026-09-03, not taken on faith from a prior AI-generated summary)

Checked every citation in the novelty argument against a real source before writing it into any document — full table in `literature/NOVELTY_AUDIT_ADDENDUM_20260903.md`. Key finding to have ready: the 2022 Wang/Vitoratou paper (N=703) is the closest existing precedent, and its null result for anxiety sensitivity/interoception (once appraisal variables are modeled) is suggestive but not confirmatory for our claim — it used different outcomes (outbursts/impairment, not severity) and different instruments. This is the honest caveat, not just the favorable read.

## 4b. Second verification round (2026-09-03) — a batch of claims from another AI's literature summary

A second round of "supporting literature" arrived (2026 fMRI papers + an open stimulus archive, "MATA") from an external AI-generated summary — checked each individually before using any of it, same rule as above:

- **MATA (Misophonia Audiovisual Trigger Archive)**: real, but the summary overstated it — it's a **bioRxiv preprint** (not published in *Scientific Data*), and it's **1,300 clips**, not 1,400+. Added to v3 §4.6 as an external construct-validity citation only (supports that trigger-specific distress replicates across stimulus sets/labs), not as a new stimulus or data source — using it to collect new online data would violate our zero-new-collection constraint, so that's flagged as a separate possible future project, not part of this plan.
- **Two 2026 fMRI papers (Ajmera/Khan, *Hearing Research*; Jain/Ajmera, *Cognitive, Affective, & Behavioral Neuroscience*)**: both real and on-topic, added to v3 §1 as background. Couldn't independently confirm their specific findings (PMC/PubMed access blocked repeatedly) — cited as existence-confirmed, findings-unconfirmed. Also share an author, so not two independent lines of evidence.
- **"Neacsiu et al., *BMC Psychiatry*, 2026"**: on 2026-09-03, could not find this paper despite extensive searching (PubMed/PMC/Google all came up empty) — wrongly called likely-fabricated. **Corrected 2026-09-07**: found it via the OpenAlex API (PubMed/Google had missed it, probably because it was very recently indexed — published 2026-06-29). It's real: Neacsiu, Gerlus, Graner, Bukhari-Parlakturk, Choi, Rosenthal & LaBar, *BMC Psychiatry*, DOI 10.1186/s12888-026-08331-3. The finding is also real and close to the original claim: right insula–dmPFC connectivity differs between misophonia and other high-emotional-dysregulation adults, and shifts between passive listening and active reappraisal. **Revised lesson**: a citation that resists search-engine verification isn't automatically fabricated — try a structured metadata API (OpenAlex, Europe PMC, Semantic Scholar) before writing it off, and when in doubt call the verdict "unconfirmed, search harder" rather than "likely fabricated."

## 5. What's still genuinely open (not yet resolved by any amount of writing)

- Meeting question 13: PI coordination/permission for using the shared fMRI dataset for Layer 3 — this is the one dependency that isn't a design problem, it's a real decision that needs Prof. Hur's input.
- Whether Layer 3's timeline cost (SPM learning + preprocessing + the analysis itself) comes out of this year's writing time or gets pushed past the one-year mark — a scheduling tradeoff, not something to decide unilaterally.
