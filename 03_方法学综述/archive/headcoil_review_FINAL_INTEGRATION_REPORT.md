# Final Integration Report
## Multi-Agent Critical Review — Revised Head Coil Review (headcoil_review_REVISED.md)

**Date:** 2026-07-20
**Reviewers:**
- **R1:** Senior MRI Physicist — RF coil design, phased-array physics, fMRI hardware optimization
- **R2:** Senior fMRI Methodologist & Biostatistician — multi-site harmonization, resting-state FC, statistical control for hardware confounds
- **R3:** Senior Journal Reviewer — *NeuroImage* / *Biological Psychiatry*, 200+ manuscripts reviewed

---

## 1. Summary of Findings

The revised review is a **substantial improvement** over the original. It correctly reframes the problem from a within-scanner partial-array difference to a cross-site harmonization problem. The citation corrections (Panman, Kaza) are verified. The [Confirmed] / [Inference] / [No Direct Evidence] framework is disciplined and appropriate for a PI-level decision memo.

However, all three reviewers independently identified material gaps that reduce its reliability for guiding multi-year data collection and publication decisions:

| Dimension | R1 (Physics) | R2 (Methods) | R3 (Journal) |
|-----------|:---:|:---:|:---:|
| **Score** | **7.0/10** | **7.0/10** | **5.5/10** |
| **Must Fix** | 3 | 3 | 5 |
| **Should Add** | 4 | 5 | 5 |
| **Optional** | 3 | 5 | 4 |

**Consensus:** The review is **directionally correct but incompletely specified**. The physics claims it makes are accurate; the gaps are in what it *does not* say (g-factor estimates, noise correlation physics, recent literature, power analysis, feasibility). The journal reviewer's lower score reflects that the review is a strong internal memo but not yet a publishable analysis plan.

---

## 2. Reliability Scores — Final Consensus

| Domain | Score | Rationale |
|--------|:-----:|-----------|
| **Hardware Physics Accuracy** | **8.0/10** | Core SNR, tSNR, and Triantafyllou claims are correct. B₁⁺ oversimplified. Detachable-ring error not explicitly corrected. |
| **Statistical Methods Evaluation** | **6.5/10** | Correct direction (harmonization > covariates) but missing: tSNR collider bias warning, SWD, CovBat, 2024+ citations. |
| **Literature Coverage** | **5.5/10** | Strong for foundational papers (Wiggins, Triantafyllou, Panman). Weak for 2023–2026 developments. No evidence of systematic PubMed search for recent harmonization literature. |
| **Scenario Analysis & Risk Assessment** | **7.5/10** | Clear and defensible for Scenarios A/B. Scenario C (longitudinal mixed-configuration) underdeveloped. |
| **Actionability / Feasibility** | **5.0/10** | Missing: power analysis, cost estimates, decision boundaries, PRIS-style pre-registration commitment. Traveling-subject numbers underspecified. |
| **Publishability Readiness** | **5.5/10** | Strong literature foundation. Weak implementation plan. Would face Major Revision at *NeuroImage* or *Biological Psychiatry*. |

**Overall Reliability Score: 6.5/10**

---

## 3. Required Revisions — Master List

All items below are drawn from the three audit reports. Priority is determined by (a) consensus across reviewers, (b) severity of potential harm, and (c) feasibility.

### 3.1 MUST FIX (11 items)

| ID | Area | Issue | Lead | Fix Summary | Source |
|----|------|-------|------|-------------|--------|
| **MF1** | Physics | B₁⁺ claim oversimplified — omits cable-trap/detuning edge cases and housing-loading effects at 3T | R1 | Add <2% edge-case qualifier and SAR-model caveat at vertex | R1-C1 |
| **MF2** | Physics | Original "detachable upper ring" error not explicitly corrected — creates inconsistency between original and revised review | R1 | Add explicit correction: "The 32ch head coil is a monolithic helmet; 20ch mode is software-based element deselection, not mechanical removal." | R1-C2 |
| **MF3** | Physics | g-factor numerical estimates omitted without replacement — critical for GRAPPA protocol decisions | R1 | Add conditional g-factor estimates depending on US coil type (lower-20 vs standalone 20ch) | R1-D1 |
| **MF4** | Statistics | tSNR-as-covariate recommendation lacks shared-noise / collider bias warning | R2 | Add caveat: tSNR derived from same EPI as connectivity → shared-noise risk. Recommend independent tSNR or sensitivity analysis with/without adjustment. | R2-MF1 |
| **MF5** | Statistics | No citations from 2024–2026; SWD and CovBat absent | R2 | Conduct systematic PubMed search for 2023–2026 harmonization literature; add SWD, CovBat, ABCD framework. | R2-MF2 |
| **MF6** | Statistics | Covariate modeling section oversimplified — conflates fixed-effect (insufficient) with random-intercept/mixed-effects (can partially address spatial non-uniformity) | R2 | Reframe: "Site+coil as fixed-effect covariates captures only global shifts. Site as random intercept or site×ROI interaction terms can partially address spatial non-uniformity." | R2-MF3 |
| **MF7** | Publishability | No statistical power analysis for exclusion of 20ch sessions | R3 | Simulate power across: n=40–120/group, effect d=0.2–0.5, 20ch proportion=5/15/30%, with and without ComBat/SMA. | R3-M1 |
| **MF8** | Publishability | ComBat/SMA not validated for small, structured batch effects typical of coil differences | R3 | Validate via simulation: at effect sizes matching CAD Lab's predicted bias, show ComBat/SMA false-positive and false-negative rates remain acceptable. | R3-M2 |
| **MF9** | Publishability | Risk of ROI cherry-picking (primary=subcortical, secondary=dorsal) without pre-registration | R3 | Pre-register analysis hierarchy: Tier 1 subcortical/limbic (confirmatory), Tier 2 dorsal (exploratory). Specify that Tier 2 findings require independent replication. | R3-M3 |
| **MF10** | Publishability | Longitudinal mixed-coil scenario (Scenario C) lacks a concrete analysis plan | R2, R3 | Add Scenario C subsection: per-subject coil-switch summary, E-value sensitivity analysis for unmeasured confounding, extreme-case analysis testing treatment-effect robustness under worst-case bias direction. | R3-M4 |
| **MF11** | Publishability | No explicit decision boundaries — "conditionally acceptable" is ambiguous without quantified thresholds | R3 | Add decision flowchart: 20ch < 10% → Tier I; 10–30% → Tier II; > 30% → Tier III or exclude. Add tSNR thresholds (e.g., dlPFC tSNR < 80 → exclude session). | R3-M5 |

### 3.2 SHOULD ADD (8 items)

| ID | Area | Issue | Source |
|----|------|-------|--------|
| **SA1** | Physics | Noise correlation / mutual inductance change at boundary of remaining 20 elements | R1-SA1 |
| **SA2** | Physics | Cable-trap and preamplifier decoupling network effects from element removal | R1-SA2 |
| **SA3** | Physics | Coil loading dependence on head size / tissue composition | R1-SA3 |
| **SA4** | Physics | GRAPPA protocol recommendation justification (why R=2, why not R=3) | R1-SA4 |
| **SA5** | Methods | Traveling-subject recommendation needs quantitative anchor: minimum 5–6 subjects (Yamashita 2019) | R2-SA2 |
| **SA6** | Methods | ICA-based denoising (FIX/AROMA) standardization — lower SNR in 20ch → fewer identifiable components | R2-SA3 |
| **SA7** | Methods | Global signal regression (GSR) — must be uniformly applied or uniformly omitted across sites | R2-SA4 |
| **SA8** | Methods | Power implications of harmonization — ComBat/SMA preserve n but add variance; net effect study-specific | R2-SA5 |

### 3.3 OPTIONAL (6 items)

| ID | Area | Issue | Source |
|----|------|-------|--------|
| **OP1** | All | Resolve ABIDE citation "confirm before manuscript" flag | R1-OP1, R2-O4 |
| **OP2** | Physics | Dielectric effects at 3T (receive-side negligible, note for completeness) | R1-OP2 |
| **OP3** | Physics | Multi-echo EPI as partial SNR mitigation (Kundu 2012, 2017) | R1-OP3 |
| **OP4** | General | SMA acronym precision ("Subsampling Maximum-mean-distance based") | R2-O1 |
| **OP5** | General | ROI-specific bias cross-reference to original review Appendix B | R2-O3 |
| **OP6** | Publishability | Cost/workload estimate for full analysis plan (scanner hours, analyst hours, subject payments, IRB amendments) | R3-S1 |

---

## 4. Inter-Reviewer Agreement Analysis

### Strong Agreement (all three reviewers)
- The revised review is a meaningful improvement over the original.
- The [Confirmed]/[Inference]/[No Direct Evidence] framework is valuable and should be retained.
- The core physics and literature claims are directionally correct.
- The review is strong as a **diagnostic** document but weak as an **implementation** plan.

### Partial Agreement (two of three)
- **g-factor omission:** R1 flags it as Must Fix; R2 does not mention it; R3 implicitly expects it via "power analysis." → Consensus: Should Add at minimum.
- **tSNR covariate issue:** R2 flags collider bias; R3 flags double-edged-sword; R1 physics scope does not cover it. → Consensus: Must Fix.
- **Missing recent literature:** R2 and R3 both identify this; R1 accepts it as an internal memo limitation. → Consensus: Should Add for a methods-facing audience.

### Disagreement
- **R3 severity gap:** R3 scores 5.5/10 while R1 and R2 score 7.0/10. This reflects different evaluation lenses: R1 and R2 evaluate the memo on its own terms (does it accurately summarize known physics and methods?), while R3 evaluates its fitness as a basis for publishable work (can a manuscript be built from this?). Both perspectives are valid but produce different results. The PI should decide which lens matters most for the intended use.

---

## 5. Gating Issue

All three reviewers identified the same **gating issue**:

> **"Establish what the US '20-channel' coil physically is."**

Until CAD Lab determines whether it is:
- (a) lower-20 mode of a Siemens 32ch coil (software-based element deselection),
- (b) a standalone Siemens 20ch head/neck coil, or
- (c) another vendor/model,

the physics analysis cannot be finalized. SNR loss, g-factor, noise correlation, and even the correct citation base differ substantially between cases.

**Recommendation:** This should be the first action item, before any protocol harmonization or pilot scanning. A 30-minute phone call or email to the US site's MRI physicist can resolve this.

---

## 6. Final Research Recommendation

### Can CAD Lab combine Korea 32-ch and US 20-ch fMRI data?

**Verdict:** **Conditionally acceptable** — strengthened to **Conditionally acceptable with active harmonization and local validation** — provided the 11 Must Fix items above are addressed.

If the 11 Must Fix items are addressed:
- **For NeuroImage / HBM submission:** Likely **Minor Revision** → Accept
- **For Biological Psychiatry / Translational Psychiatry submission:** Likely **Major Revision** → Accept (with clinical reviewer skepticism about feasibility)
- **For a grant application:** The revised review (with Should Add items) is sufficient — grant reviewers rarely demand the implementation detail that journal reviewers will.

If the 11 Must Fix items are NOT addressed:
- **For any journal:** Likely **Major Revision → Reject** if the power analysis, ComBat/SMA validation, and pre-registration are missing. A journal reviewer will recognize these absences as fundamental methodological gaps.

### Confidence level after audit: Low-to-moderate (unchanged from the revised review's self-assessment)

The revised review's self-assessment of "Low-to-moderate" confidence is accurate and should not be upgraded without the Must Fix items. The general phenomenon (coil differences produce real, regionally specific fMRI biases) is well-confirmed. The specific cross-site 20-vs-32 situation remains **not directly studied**. This audit does not change that fundamental limitation — it only evaluates how well the review communicates it.

### Recommended immediate next steps (ordered by priority)
1. **Determine the US coil type** — gating issue for all physics analysis.
2. **Conduct systematic 2023–2026 literature search** for recent harmonization developments (MF5).
3. **Run statistical power simulations** for the expected 20ch session rate (MF7).
4. **Add the tSNR collider-bias caveat** to the statistical plan (MF4).
5. **Correct the detachable-ring error** and add conditional g-factor estimates (MF2, MF3).
6. **Add Scenario C** (longitudinal mixed-configuration) as a formal analysis section (MF10).
7. **Pre-register the analysis hierarchy** on OpenNeuro or aspredicted.org (MF9).

---

## 7. Appendix: Cross-Reference to Original Files

| File | Path | Status |
|------|------|--------|
| Revised review (English) | `headcoil_review_REVISED.md` | **Saved — audit completed** |
| Revised review (Chinese) | `headcoil_review_REVISED_中文.md` | Saved |
| Revised review (Korean) | `headcoil_review_REVISED_한국어.md` | Saved |
| Original review (superseded) | `headcoil_literature_review.md` | **Contains uncorrected citation errors** — should be archived |
| R1 Audit Report | *(embedded in session)* | Complete |
| R2 Audit Report | *(embedded in session)* | Complete |
| R3 Audit Report | *(embedded in session)* | Complete |
| Final Integration Report | `headcoil_review_FINAL_INTEGRATION_REPORT.md` | **This file** |

---

*End of Final Integration Report*
