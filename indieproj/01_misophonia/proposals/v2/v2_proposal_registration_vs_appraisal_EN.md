# Registration versus Appraisal of Bodily Sensation: Misophonia as a Test Case for Appraisal-Driven Symptomatology

> Author: Chaeha Dong (CAI DONG)
> Version: **v2** — 2026-08-21 (v1 archived in `_v1_archive/`; do not cite)
> Purpose: Discussion document for meeting with Prof. Juyoen Hur / personal research proposal
> Data: CAD Lab Misophonia Neural Mechanisms Study (primary); Sinjin-gwaje longitudinal study (secondary)

---

## 1. The core question

> **Is misophonia severity driven by how strongly bodily sensations are *registered*, or by how threatening those sensations are *appraised* to be?**

### Why the distinction matters

Two separable steps lie between bodily sensation and clinical symptom:

- **Registration (S)**: the degree to which internal bodily signals are noticed and perceived
- **Appraisal (A)**: the degree to which those signals are judged dangerous, intolerable, or action-demanding

These are conceptually independent and have been shown to be empirically dissociable — a person can be highly attuned to bodily sensation without finding it frightening, and vice versa.

**Most discussion of misophonia implicitly assumes the problem lies at the registration level** (sensation is too strong; sensory input is amplified). If what actually drives symptoms is appraisal, the clinical implication is entirely different: intervention should target the evaluation of bodily sensation rather than sensory desensitization.

### The claim, stated sharply

> **Misophonia is not a disorder of audition, nor of the autonomic response, but of the appraisal of one's own bodily reaction to a sound.**

The causal chain:

```
Trigger sound → autonomic response (tachycardia, muscle tension, hyperventilation)
              → that response is registered interoceptively (S)
              → that response is appraised as intolerable / dangerous / demanding escape (A)
              → clinical severity (M)
```

> ⚠ **This section previously contained a claim that has been deleted**: an earlier draft asserted that autonomic responses in misophonia are only moderately elevated while subjective distress is extreme, and that this mismatch constitutes the phenomenon. The claim does not hold — Edelstein et al. (2013) report a **significant positive correlation** between subjective aversiveness and skin conductance response, i.e. subjective and physiological responses were consistent with one another. See §2 of `NOVELTY_AUDIT_文献查证_20260821.md`.
>
> **Lesson**: any empirical claim entering a proposal must be searched before it is written.

**⚠ The novelty of this proposal's central claim is constrained**: a closely overlapping model was published in 2025 (*Toward cognitive models of misophonia*, which explicitly proposes that reaction intensity is shaped by "misinterpretation of bodily sensations"), and ASI-3 prediction of misophonia severity was published in 2026 (in an OCD sample).

**The study is therefore repositioned as the first competitive quantitative test of an existing model's central claim**, rather than as a new framework. The increment lies in entering registration and appraisal **simultaneously in one model** within a misophonia clinical sample (the prior ASI-3 study was conducted in an OCD sample and included no interoceptive measures), and in the Layer-2 trial-level specificity test, for which no precedent was found.

The full audit is in `NOVELTY_AUDIT_文献查证_20260821.md`; a candidate new framework derived from that audit is in `NEW_FRAMEWORK_登记分化评价.md`.

### Interface with the current controversy about misophonia

Misophonia is not in the DSM, and its classification remains contested: sensory processing disorder? anxiety disorder? OCD-spectrum condition?

**The registration/appraisal decomposition maps directly onto the core of that disagreement**, and can be tested with data already being collected.

### A three-layer test structure

The same claim yields independently testable predictions at three levels of evidence. **Each layer is separately deliverable; failure of a later layer does not affect an earlier one.**

| Layer | Data | fMRI preprocessing required? | Delivery |
|---|------|:---:|---|
| **1 · Questionnaire** | MAIA/BPQ, ASI-3, AMISOS-R, SPSQ, OCI-R | No | M4–M7 |
| **2 · In-scanner behavior** | Trial-level sound ratings from the auditory task | No (behavioral logs only) | M7–M11 |
| **3 · Neural** | Insula response during the interoceptive attention task | Yes | Once preprocessing is available |

**Layer 1 alone constitutes a publishable paper.** Layers 2 and 3 are escalating validations, with hypotheses fixed before data are seen.

---

## 2. Design constraints (binding, and prior to any theoretical consideration)

1. **Zero new data collection** — only variables the lab already collects; nothing appended to existing protocols
2. **No dependence on fMRI preprocessing** — imaging is the slowest bottleneck; all primary analyses rest on questionnaire data
3. **Analyzable in increments** — must produce interpretable results at interim n

**Rationale**: a one-year window to graduation; secondary analysis carries the lowest administrative cost (**to be confirmed whether it requires only investigator addition rather than an IRB amendment**); questionnaire data accrue continuously while scanning proceeds, and are the only stream capable of yielding results within a year.

**Directions deliberately forgone**: language variables, bilingual emotion granularity, freeze-response psychophysiology, norm-calibration vignettes — all requiring new measurement; recorded in `../个人项目_语言与心智化/06_开放问题与下一步.md`. **What is bought is executability; the trade is made deliberately.**

---

## 3. Data and variables

### 3.1 Primary source: Misophonia Neural Mechanisms Study

- N = 80 (50 clinical / 30 control), ages 18–39
- Drawn from a prior behavioral study (N = 159; 145 consented to recontact) → **no new recruitment required**
- Single 2-hour session; 14 online questionnaires
- Study period through 2028-08-31

### 3.2 Variable mapping (all existing questionnaires)

| Role | Instrument | Items |
|------|-----------|:---:|
| **S · Registration** | MAIA-2 (8 subscales); BPQ-SF-A | 37 / 26 |
| **A · Appraisal** | **ASI-3** (Physical / Cognitive / Social Concerns) | 18 |
| **M · Outcome (primary)** | AMISOS-R misophonia severity | 12 |
| **M · Outcome (comparison)** | IDAS-II dimensional distress | 99 |
| **Discriminant 1** | SPSQ general sensory processing sensitivity | 16 |
| **Discriminant 2** | OCI-R obsessive-compulsive symptoms | 18 |
| **Sensitivity analysis only** | K-CTQ (5 subscales); LTE-Q | 28 / 12 |
| Also known to be in battery | K-BDEFS-SF; K-SADS-PL-Tic | 20 / 48 |

Eleven confirmed; three further instruments were not extractable from the protocol (one is a Korean validation per Woo et al., 2010) — **request the complete list at the meeting.**

### 3.3 ⚠ Important correction regarding the interoception task

The protocol's interoception task is an **interoceptive attention task** (heart / gut / visual-control conditions alternating, 10 min fMRI), not a heartbeat detection or counting task.

**It therefore yields no interoceptive accuracy and no confidence ratings, and cannot support the accuracy or awareness dimensions in Garfinkel's sense.** The three-dimensional dissociation design in v1 is void.

The present v2 **does not depend on that task at all**, substituting the MAIA/BPQ (sensibility) versus ASI-3 (appraisal) decomposition, which is available entirely at the questionnaire level.

---

## 4. Hypotheses

### Study 1 (primary) · Relative contribution of registration and appraisal

**H1 · Main effect (adequately powered)**
Controlling for registration (MAIA-2, BPQ-SF-A), ASI-3 continues to predict AMISOS-R.
→ The appraisal contribution is independent of registration.

**H1b · Relative importance**
Dominance analysis or relative-importance decomposition comparing the variance in AMISOS-R attributable to S versus A.
→ More robust than comparing standardized regression coefficients, which are unstable under collinearity.

**H2 · Discriminant validity (adequately powered)**
H1 holds after controlling for SPSQ and OCI-R.
→ The effect is attributable neither to generalized sensory sensitivity nor to OCD-spectrum comorbidity.
**This is the study's most consequential set of controls.** If SPSQ absorbs the effect, misophonia is one expression of sensory sensitivity; if OCI-R absorbs it, OCD-spectrum classification gains support. Both outcomes are informative.

**H3 · Gating interaction (exploratory; underpowered, explicitly flagged)**
`AMISOS-R ~ MAIA × ASI-3`
Predicted positive interaction: **bodily registration converts into symptoms only when the appraisal layer judges it threatening.**

> ⚠ **N = 80 is underpowered for an interaction.** Detecting interactions typically requires several times the sample needed for main effects; only a large interaction would be detectable here. H3 is reported as an effect estimate with confidence intervals, with no significance claim, and is positioned as hypothesis generation for subsequent work.

**H4 · Outcome specificity**
The same model with IDAS-II total as the outcome.
→ If the S×A structure explains misophonia severity better than general distress, the structure is not a generalized distress proneness.

---

### Study 1 · Layer 2: in-scanner behavioral data (no fMRI preprocessing required)

The auditory task supplies **trial-level, non-questionnaire behavioral data**: 42 sounds (trigger / unpleasant / neutral), each presented for ~15 s, after which participants classify it as pleasant / unpleasant / neutral.

**Only the behavioral log file is needed; the imaging pipeline is not touched.**

**This layer resolves both weaknesses of Layer 1:**

| Layer 1 weakness | How Layer 2 resolves it |
|---|---|
| Common method variance (S, A, M all self-report) | The outcome becomes an in-task behavioral response, not self-report |
| **Underpowered interaction** | 42 trials × 80 participants ≈ **3,360 observations**; a cross-level interaction at trial level is an order of magnitude better powered |

**H5 · Trial-level gating (adequately powered)**

```
P(rated "unpleasant")_ij ~ Sound type × ASI-3 + (1 + Sound type | Participant)
```

Ordinal or binomial mixed model (ordinal is more appropriate for the three-category rating).

**Core test**: does ASI-3 **specifically amplify aversion to trigger sounds without amplifying aversion to generally unpleasant sounds?**
→ **The unpleasant-sound condition is a built-in control**, so the design excludes generalized negativity bias without requiring additional covariates.

**H6 · Registration/appraisal dissociation at trial level**
The same model with MAIA × Sound type added.
Prediction: moderation by ASI-3 exceeds moderation by MAIA — converging with the participant-level conclusion of H1.

**Methodological declarations (fixed in advance)**:
- The three-category rating is modeled ordinally; no collapse to "unpleasant = 1, else = 0" (unless the ordinality assumption is violated, in which case the test must be reported)
- Random-effects structure: begin maximal (random intercept + random slope for sound type), simplifying stepwise per Barr et al. if convergence fails, with the simplification path reported
- Sound stimuli entered as a crossed random effect if the same stimulus set is presented to all participants

---

### Study 1 · Layer 3: neural (initiated once preprocessing is available; hypotheses pre-registered)

The interoceptive attention task (heart / gut / visual control, alternating, 10 min) combined with the established functional gradient of the insula:

| Anatomy | Established function | Corresponding construct |
|---------|---------------------|------------------------|
| Posterior / mid insula | Primary interoceptive representation | **Registration (S)** |
| Anterior insula | Integrated, evaluative representation | **Appraisal (A)** |

**H7 · Anterior–posterior double dissociation**
- AMISOS-R severity is more strongly associated with **anterior** insular response during interoceptive attention than with posterior/mid insular response
- ASI-3 associates primarily with anterior insula; MAIA primarily with posterior/mid insula

**This is an anatomical dissociation derived directly from the behavioral hypothesis, and fixed before any imaging data are seen** — methodologically far stronger than post hoc correlation hunting.

**Boundary**: this layer is not part of the one-year deliverable. If the preprocessing pipeline is unavailable within that window, the conclusions of Layers 1 and 2 are unaffected.

**To confirm**: whether the interoceptive attention task records any behavioral output (e.g., post-block sensation-intensity ratings). If so, that task can also contribute Layer 2 data.

### Study 2 (secondary) · Objective–subjective sleep discrepancy

**Status: contingent on two facts to be confirmed at the meeting** (whether EMA includes sleep items; accessibility and granularity of Garmin sleep data).

If viable: use the subjective–objective sleep discrepancy as a domain-specific index of the appraisal layer and examine its relation to distress.

**Methodological requirements if initiated**:
- **Do not use raw difference scores** — their reliability is bounded by the reliability of both components and their intercorrelation, and they are confounded with the level of each → use a regression-residual approach (regress subjective on objective, retain residuals)
- **Restrict claims to metrics consumer wearables measure adequately** (total sleep time, sleep onset latency); **avoid sleep staging**, for which consumer-device validity is poor

**Connection**: the EMA sleep-diary cleaning tool I developed and repeatedly audited (R package + skill; GitHub: cyracaid/sleepdiary-cleaner) constitutes the first stage of this analysis and could serve the lab's existing EMA pipeline directly.

---

## 5. Analysis plan (pre-registration points)

### 5.1 Decisions fixed before seeing data

**Subscale selection** (to close the garden of forking paths):
- The 8 MAIA-2 subscales are **not all entered**. Primary analyses use Noticing and Body Listening (registration); Not-Worrying / Not-Distracting / Trusting carry appraisal content and are **assigned to exploratory analyses and reported separately**
- ASI-3 primary analyses use the **Physical Concerns** subscale; Cognitive and Social Concerns serve as discriminants
- IDAS-II primary analyses use the total score; subscale analyses are exploratory

**Rationale**: MAIA-2(8) × ASI-3(3) × IDAS-II(18) yields hundreds of combinations. Without fixing these in advance, no "finding" is credible. This is a lesson carried over directly from the CSS project.

### 5.2 Statistical conventions

- HC3 robust standard errors by default
- Bonferroni correction across the primary hypothesis family (H1, H1b, H2, H4); FDR with reported q-values for H3 and exploratory analyses
- Covariates: age, sex, group
- **Report effect sizes and confidence intervals, not p-values alone**

### 5.3 Honest statement of power

| Analysis | Layer | Power at N = 80 | Status |
|----------|:---:|-----------------|--------|
| H1 / H2 multiple regression (~5 predictors) | 1 | ~74% for medium effects (f² ≈ 0.15); adequate at f² ≈ 0.20 | Primary |
| Between-group comparison (50 vs 30) | 1 | ~80% at d ≈ 0.65 (per the protocol's own G*Power justification) | Primary |
| H3 participant-level interaction | 1 | **Inadequate** | Exploratory / effect estimation |
| **H5 / H6 trial-level cross-level interaction** | 2 | **≈ 3,360 observations; adequate** | **Primary** |
| H7 neural dissociation | 3 | To be assessed against the final imaging n | Pre-registered confirmatory |

**Key point**: the gating hypothesis (registration × appraisal) is underpowered at the participant level (H3) but **adequately powered at the trial level (H5)**. The gating claim in this proposal is therefore carried principally by Layer 2, with H3 reported only as converging evidence. This is the most substantive improvement over v1.

**Interim analysis**: preliminary main-effect estimates are possible at n ≈ 40, but must be reported as estimates with wide confidence intervals rather than as hypothesis tests.

---

## 6. Known threats and responses

| Threat | Severity | Response |
|--------|----------|----------|
| **Underpowered participant-level interaction** | Mitigated | H3 demoted to exploratory; **the gating claim is carried instead by the Layer-2 trial-level model (H5), with ≈ 3,360 observations and adequate power** |
| **Layer 2 depends on log accessibility** | Unknown | Whether trial-level auditory ratings are separately archived, and in what format — listed among the must-ask meeting questions |
| **Range restriction in IDAS-II** | Moderate | The protocol excludes psychiatric disorders, substance use, psychotic disorders, and bipolar disorder → the control group is a supernormal control and the distress distribution is truncated, which **systematically attenuates any correlation involving distress**. Must be stated as a limitation; a null result for H4 cannot be read directly as absence of specificity |
| **Sample selected on misophonia severity** | Accepted | Conclusions are limited to this sample and not generalized to the general population. This boundary is accepted deliberately |
| **Common method variance** | Moderate | All primary variables are self-report questionnaires → relations among S, A, and M partly reflect shared method. Must be stated as a limitation; between-group comparisons are unaffected |
| **K-CTQ retrospective reporting bias** | Avoided | Excluded from the primary model; used only in sensitivity analyses, with conclusions phrased as "retrospectively reported childhood adversity" rather than "childhood adversity" |
| **Subscale researcher degrees of freedom** | Avoided | Fixed in advance, §5.1 |
| **Three unextracted questionnaires** | Unknown | May require minor adjustment once the complete list is obtained |

---

## 7. Relation to broader research interests (no strong coupling claimed)

I have two other independent lines of work: a submitted N=1 dream-diary study (a case in which a bodily signal was present while the representational layer refused it), and a methodological analysis of a Chinese national sample (threat interpretation moderating body–mind coupling; b = +0.035, N ≈ 6,000).

**What these three share is a form (`M ~ S × A`), not a common mechanism.** In the dream diary the prior derives from a cultural prohibition on naming; in the national sample from political-economic appraisal; in the present study from threat appraisal of bodily sensation. **Whether these produce isomorphic gating is itself an open question, not a premise assumed here.**

The present study does not depend on that larger framework being correct. It is a self-contained, publishable misophonia study. The framework explains only why I am interested in this particular question.

---

## 8. Timeline (12 months)

| Phase | Months | Content |
|-------|--------|---------|
| 1 | M1–M2 | Confirm data access and IRB procedures; obtain the complete questionnaire list; **finalize and lock the pre-registration** |
| 2 | M2–M4 | Build and validate the analysis pipeline on simulated data; literature review (misophonia classification debate, anxiety sensitivity, interoception measurement) |
| 3 | M4–M7 | Interim analysis (n ≈ 40), reported as estimation rather than testing |
| 4 | M7–M11 | Primary analyses on the expanded sample; Study 2 initiated contingent on meeting outcomes |
| 5 | M10–M12 | Writing; submission or conference abstract |

---

## 9. What I can contribute

1. **EMA data engineering**: sleepdiary-cleaner (R package + skill), repeatedly audited, near completion, deployable to the lab's EMA pipeline
2. **A complete robustness workflow**: executed hands-on across two submitted papers and one national-sample analysis — dual correction for a length confound, HC3, Bonferroni and FDR, discriminant-validity design, confound exclusion, **and a documented record of retracting findings that failed correction**
3. **A record of self-auditing**: I recently identified that one of my own cross-national analyses had used a deprecated version as its baseline, requiring a directional revision of the conclusion; the diagnosis is complete and the revision is scheduled
4. **Ongoing lab participation**

---

## 10. Meeting questions, by priority

### Determines whether analysis can begin (must ask)
1. What is the **complete list of the 14 questionnaires** in the misophonia study? (11 confirmed; 3 missing)
2. What is the current n with completed questionnaires? Projected in one year?
3. Can questionnaire data be accessed before scanning is fully complete?
4. What does secondary analysis require at the IRB level — investigator addition, or an amendment report?

### Determines Layer 2 (trial level — principal carrier of the gating hypothesis)
5. **Are the trial-level sound ratings from the auditory task separately archived? In what format, and accessible how?** — this determines whether H5/H6 can be run, and since the gating claim rests principally on this layer, it ranks alongside question 1 in importance
6. Are the type labels for the 42 sounds (trigger / unpleasant / neutral) supplied with the data? Is the stimulus set identical across participants (which determines whether a crossed random effect is appropriate)?
7. Does the interoceptive attention task record any behavioral output beyond imaging (e.g., post-block sensation-intensity ratings)?

### Determines whether Study 2 is viable
8. Does the Sinjin-gwaje EMA item set include sleep items?
9. What is the export format and granularity of Garmin sleep data? Does a cleaned version exist?
10. Could sleepdiary-cleaner be integrated into the existing EMA pipeline? To what specification?

### Ownership
11. Is anyone already conducting interoception-related analyses in the misophonia study?
12. If I proceed, is this an independent project or nested under an existing one? Authorship order?
13. Layer 3 (the insula gradient) overlaps with the lab's own interoceptive imaging aim; if I pre-register that hypothesis, how should it be coordinated with the existing division of work?

---

*v2 draft. To be revised after the meeting in light of actual data availability.*
