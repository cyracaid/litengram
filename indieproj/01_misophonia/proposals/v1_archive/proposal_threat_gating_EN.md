# Threat Appraisal as a Gate on Body–Mind Coupling
## From population-level evidence to mechanistic validation

> Author: Chaeha Dong (CAI DONG)
> Version: v1.0 draft — 2026-08-21
> Purpose: Discussion document for meeting with Prof. Juyoen Hur / personal research direction proposal
> Related lab projects: Misophonia Neural Mechanisms Study / Sinjin-gwaje Longitudinal Study

---

## Abstract

Using the Chinese Social Survey (CSS 2023, national sample), I found — and validated across seven convergent checks — that a **threat-based interpretation of social redistribution ("common prosperity means taking from the rich") gates (tightens) the coupling between physical and mental health**. The effect survived Bonferroni correction and six stress tests, showed discriminant validity, and was independent of negative-affect disposition. However, cross-cultural replication (KGSS Korea, ESS9, WVS7) indicates the pathway is **culturally specific**.

The methodological value of this result exceeds the generality of its construct: it formalizes the hypothesis that *threat appraisal gates body-to-mind transmission*, but cross-sectional population data cannot determine whether the gating occurs at the **physiological signal level** or the **signal interpretation level**. This proposal tests the same formal hypothesis mechanistically using two existing CAD Lab datasets:

- **Study 1 (Misophonia study, questionnaire level)**: whether threat load gates the coupling between interoceptive awareness and symptom severity, with the misophonia clinical group serving as a natural model of sensory-to-threat interpretation pathology.
- **Study 2 (Sinjin-gwaje, EMA within-person)**: converting "coupling" from a statistical interaction into observed within-day dynamics, and — for the first time — dissociating **objective physiological signal** from **subjective bodily perception** to localize the level at which gating occurs.

---

## Before §0: The core question

### In one sentence

> **The strength with which a bodily signal converts into psychological distress is set by the prior imposed upon that signal — and does that prior act on the signal itself, or on its interpretation?**

### Expanded

Transmission from bodily state to psychological state is not fixed. What determines it is not only the strength of the signal, but a prior layered over it: **which bodily states warrant vigilance, and which may be treated as background noise.**

This prior has two sources, which are two phases of the same thing:

- **Early relational experience shapes it** — whether a bodily or emotional state was ever named and responded to. If never named, the prior about what counts as normal is never updated.
- **Current threat appraisal invokes it** — when a situation is read as threatening, bodily signals are assigned greater diagnostic weight.

What unifies the two is **precision weighting: the prior determines what is granted diagnostic weight.** This is also why the formal framework here is hierarchical Bayesian rather than ordinary moderation.

### The resulting level question (the core contribution)

At which level does the prior exert its effect?

| | Claim | Observable consequence |
|---|-------|------------------------|
| **H-signal** | The threat prior alters the physiological response itself | Objective physiological indices vary with the prior |
| **H-interpretation** | The physiological signal is unchanged; what changes is the weight of signal→affect transmission | Objective physiology unchanged; the subjective-perception→affect slope varies |

**This distinction cannot be drawn in any purely self-report dataset**, because self-report already fuses the signal with its interpretation into a single number. It requires objective physiology and subjective perception measured concurrently.

### How three projects converge here

| Project | Observation | Level evidence | Limitation |
|---------|-------------|----------------|------------|
| **Dream diary, N=1** (submitted) | Two years of pathological bleeding appears zero times across 384 dream entries and 1.8 MB of waking diary; an acute gynecological event entered representation 32 days before diagnosis | The signal was present throughout; the representational layer refused it → **direct evidence of interpretation-level gating** | N=1, not generalizable, no objective physiology |
| **CSS Phase 1** (population) | Threat interpretation tightens body→mind coupling (b = +0.035, seven convergent checks); SES as second-order moderator | Establishes that the effect has scale and cultural boundaries | Single-item self-report; **cannot localize the level** |
| **CAD Lab data** | To be analyzed | Objective physiology (Garmin / HRV / interoception task performance) coexists with subjective perception (MAIA / BPQ / EMA self-report) | — |

**These are not three separate projects: the N=1 proposed the mechanism, the population data showed it has scale but could not localize the level, and the lab data is the only place where the level can be localized.**

### Why this question is askable now

The lab's two datasets jointly provide the minimum configuration required to separate the two levels — objective physiology and subjective perception in the same participants within the same time window. This is not a common configuration, and it is the sole reason this proposal must be built on lab data rather than public data.

---

## 0. Design constraints (binding throughout; they take precedence over theoretical considerations)

Every design in this proposal operates under three hard constraints. **Any idea in conflict with them is excluded or demoted to a long-term direction, however high its theoretical value.**

### The three constraints

1. **Zero new data collection** — only variables the lab is already collecting. No additional measures, scales, or task items may be appended to existing protocols.
2. **No dependence on fMRI preprocessing** — the imaging preprocessing pipeline is the slowest bottleneck. Primary analyses must rest on questionnaire, behavioral-task, EMA, and wearable data; fMRI enters only as an optional extension, never as the main line.
3. **Analyzable in increments** — analyses must yield interpretable results at interim n, rather than requiring a completed sample.

### Why these are fixed

- **Time window**: one year to graduation leaves no margin for waiting on a complete dataset.
- **Administrative cost**: pure secondary analysis typically requires only the addition of an investigator, not an IRB amendment. Requesting any new measure triggers an amendment report on an uncontrollable timeline.
- **Accrual rate**: questionnaire and EMA data accumulate continuously while scanning proceeds, independent of imaging progress. This is the only data stream capable of producing preliminary results within a year.

### The trade-off being made

This proposal deliberately forgoes several theoretically richer directions that would require new measurement (language variables, bilingual emotion granularity, freeze-response psychophysiology, norm-calibration vignettes — recorded in `../个人项目_语言与心智化/06_开放问题与下一步.md`). **What is bought is executability. This exchange is made deliberately, not by default.**

### Concrete analyses under the constraints

| # | Analysis | Existing variables used | fMRI-dependent? | Incremental? |
|---|----------|------------------------|:---:|:---:|
| A | **Three-dimensional interoceptive dissociation** (primary)<br>K-CTQ Emotional Neglect → specific dissociation across accuracy / sensibility / awareness | Interoception task, MAIA-2, BPQ-SF-A, K-CTQ, IDAS-II, SPSQ | No | Yes, n ≈ 35–40 |
| B | **Objective–subjective sleep discrepancy in EMA**<br>The discrepancy itself as a domain-specific calibration index | Garmin objective sleep, EMA sleep diary, IDAS-II Insomnia, K-CTQ | No | Yes, n ≈ 25–30 |
| C | **Accuracy–sensibility gap predicting misophonia severity** | As in A, plus AMISOS-R | No | Yes, n ≈ 35–40 |

Analyses A and C fall under Study 1 (misophonia sample); analysis B falls under Study 2 (Sinjin-gwaje EMA). All three share the formal hypothesis `M ~ S × A`.

### ⚠ Three unknowns that determine feasibility (to ask at the meeting, in order of importance)

1. **Does the interoception task record confidence ratings?** Without them the awareness dimension cannot be computed and analysis A loses half its structure; C is unaffected.
2. **Does the EMA item set include sleep items? What is the export granularity and format of Garmin sleep data?** Determines whether analysis B is viable at all.
3. **Is anyone already working on the interoception–misophonia-severity line?** Determines whether C should be raised proactively.

**The answers to these three determine which analysis can begin, and take precedence over every other question in §8.**

---

## 1. Background: CSS Phase 1 results and their honest positioning

### 1.1 Completed work

Model tested in CSS 2023: `Mental Health ~ Physical Health × Threat Interpretation`

| Item | Result |
|------|--------|
| Core interaction (f4c_3 × PH) | b = +0.035, p = .0002, survives Bonferroni |
| Robustness | All six stress tests survived (weakest: HC3 robust SE, p = .012) |
| Direction | Threat interpretation **tightens** body→mind coupling (r: .590 → .673) |
| Pathway specificity | Gates body→mind only; does **not** gate cognitive-appraisal→mind |
| Discriminant validity | Injustice (−0.021, reversed), fairness, f4c_2, subjective SES — **none** gate |
| Confound exclusion | Controlling negative affect and its interaction with PH, the coefficient *increased* (.035 → .047, p < .0001) |
| Supplementary stress load | stress_total continuous interaction passed Bonferroni (HC3 p = .005), but grouped Fisher z did not support (p = .476) → graded A− supporting evidence |

### 1.2 Cross-cultural replication: partial failure, but informative

- **KGSS 2023 (Korea)**: three-way interaction (PH × MISTRUST × RANK) significant (p = .025); marginal under HC3 (p = .063). The original report concluded "opposite direction," but **that conclusion has been found to be in error** (see 1.2.1). Construct misalignment (BEFAIR indexes interpersonal mistrust, not the systemic-predation reading captured by f4c_3) remains a valid secondary explanation.

#### 1.2.1 Correction: the KGSS "direction inconsistency" was benchmarked against a deprecated version

On auditing `phase0_KGSS_replication_results.md`:

- Section **B1** of that report cites the correct v2 CSS figure (f4c_3, β = +0.033, p = .0002, tightening).
- However, the **CSS simple-slopes table in Section B3** (0.65 / 0.51 / 0.64 / 0.55, showing *weakening*) derives from the **deprecated v1 analysis** (f4c_mean, α = −0.408, already judged invalid). The code citation in Section F2 likewise points to `phase1-1-opencode/`, the v1 directory.
- The report is therefore internally inconsistent between B1 and B3, and the conclusion of "directional inconsistency across samples" rests on an incorrect CSS baseline.

**Reinterpretation against the v2 baseline:**

| | Low SES/RANK | High SES/RANK |
|---|---|---|
| CSS v2 (f4c_3) | Tightens (overall r .590 → .673) | Tightens |
| KGSS (MISTRUST) | **Tightens** (2.21 → 3.34) | Loosens (1.93 → 1.57) |

KGSS is thus not cleanly opposite but **conditionally consistent** — matching CSS in direction (tightening) among low-SES respondents, and reversing only among high-SES respondents. The significant three-way interaction (β = −0.441, p = .025) captures precisely this divergence.

Conservatism to retain: in the zero-control scan (B1), the KGSS BEFAIR interaction is genuinely opposite in sign (β = −0.653, p = .028), and the reversed MISTRUST term, while directionally consistent, is non-significant (β = +0.344, p = .303). One therefore **cannot claim that KGSS replicated CSS**; the appropriate statement is "consistent under some conditions, with SES as a plausible second-order moderator."

**Theoretical implication**: if SES determines whether threat appraisal tightens or loosens body–mind coupling, then gating is itself conditional. This adds a testable corollary to the present proposal — see H1.5 and H2.5.
- **ESS9 / WVS7 (Western)**: anti-redistribution attitudes **loosened** coupling in both (ESS b = −.072; WVS7 b = −.006), opposite to CSS; political mistrust tightened in ESS (b = +.038, consistent with CSS) but loosened in WVS7 (b = −.034); luck-belief showed no effect.

**Conclusion**: the f4c_3 pathway is specific to the Chinese context. This should be framed as a **contribution rather than a deficiency** — it establishes a cultural boundary condition on the effect.

### 1.3 Why move to lab data

Three structural limitations of CSS map directly onto what CAD Lab data can resolve:

1. **Cross-sectional and between-person**: supports only the inference that individuals with poorer physical health *and* a threat interpretation report worse mental health. It says nothing about within-individual dynamics.
2. **Physical state is self-reported only**: cannot distinguish gating at the level of **actual physiological signal** from gating at the level of **interpretation of that signal**. This is the theoretically decisive fork, and CSS cannot address it at all.
3. **Threat appraisal is a macro-social construct**: too distant from the mechanistic level of clinical psychology to interface with neural or physiological evidence.

The appropriate next step is therefore not to accumulate more cross-national cross-sectional samples, but to **descend to data with objective physiology, within-person repeated measurement, and clinical samples**.

---

## 2. Theoretical framework: the threat-gating hypothesis

### 2.1 Formal statement

> The strength of transmission from bodily state to psychological state is not fixed, but is modulated by the individual's threat appraisal of their situation. When the situation is read as threatening, bodily signals are assigned greater diagnostic weight and therefore transmit more strongly into psychological distress.

Three components:

- **S (bodily state)**: objective physiological signal, or subjective perception of that signal
- **A (threat appraisal)**: threat-based interpretation of the situation or of the bodily signal; the gating variable
- **M (psychological outcome)**: affect, symptoms

Form: `M ~ S × A`, predicting a positive interaction coefficient for `A` (tightening).

### 2.2 Interfaces with existing theory

| Framework | Interface |
|-----------|-----------|
| Garfinkel three-dimensional interoception model (2015) | Accuracy / Sensibility / Awareness are dissociable → measurement basis for S |
| Predictive processing / interoceptive inference | Threatening priors raise precision weighting on bodily prediction error → computational account of gating |
| Threat Imminence Continuum (Fanselow, Mobbs) | Threat appraisal segmented by imminence → hierarchical structure of A |
| Somatization / anxiety sensitivity | "Catastrophic interpretation of bodily sensation" is the clinical relative of this hypothesis |

### 2.3 The decisive theoretical fork (core contribution)

At which level does gating occur?

- **H-signal**: threat appraisal alters the physiological response itself (heart rate genuinely rises more)
- **H-interpretation**: threat appraisal leaves the physiological signal unchanged, and alters only the weight of signal→affect transmission

**CSS cannot separate these, having only self-reported bodily state.** Study 2 models objective Garmin physiology and EMA self-reported bodily sensation as parallel pathways, permitting a direct test: if gating appears only on the self-report→affect path and not on the objective-physiology→affect path, H-interpretation is supported.

This is the most substantive theoretical advance over CSS.

---

## 3. Study 1: Misophonia — threat load gating interoception–symptom coupling

### 3.1 Why misophonia is an ideal model

The core pathology of misophonia is a **threat interpretation of neutral or minor bodily sounds** (chewing, breathing), accompanied by amplified somatic responses (tachycardia, hyperventilation, muscle tension). Structurally this is precisely a clinical instance of the present hypothesis: sensory input → threat interpretation → amplified psychophysical response.

Prior neuroimaging converges: the anterior insula — simultaneously a hub for salience detection and for interoceptive processing — is hyperactive in misophonia (Kumar et al., 2017), implicating interoceptive abnormality. The lab's own IRB protocol explicitly lists interoception among the study aims.

### 3.2 Data source

CAD Lab Misophonia Neural Mechanisms Study:
- N = 80 (50 clinical / 30 control), ages 18–39
- Drawn from a prior behavioral study (N = 159; 145 consented to recontact; 101 clinical / 44 control) → **no cold recruitment required**
- Single 2-hour session; 14 online questionnaires

Available variables:

| Role | Instrument |
|------|-----------|
| S — bodily perception | MAIA-2 (37 items, 8 subscales); BPQ-SF-A (26 items, body awareness) |
| A — threat load | LTE-Q (threatening life events, past 6 months); K-CTQ (childhood trauma, 5 subscales) |
| M — psychological outcome | IDAS-II (99 items, dimensional depression/anxiety; Panic / Social Anxiety / Insomnia / Dysphoria subscales) |
| Discriminant | SPSQ (general sensory processing sensitivity); AMISOS-R (misophonia severity) |
| Group | Clinical / control (double-blind administration) |

### 3.3 Hypotheses

- **H1.1**: Threat load (LTE-Q) positively moderates the association between interoceptive awareness (MAIA-2 Noticing / BPQ) and symptom severity (IDAS-II). Individuals with higher threat load show tighter body-awareness–symptom coupling.
- **H1.2 (discriminant validity)**: General sensory processing sensitivity (SPSQ) does **not** produce equivalent gating. If SPSQ also gates, the effect is not threat-specific but attributable to generalized sensory sensitivity. This discriminant design is carried over directly from the strategy already validated in CSS.
- **H1.3 (group)**: Gating is stronger in the misophonia clinical group than in controls.
- **H1.4 (decomposition, exploratory)**: Among the 8 MAIA-2 subscales, "awareness-type" (Noticing, Body Listening) and "regulatory-attitude-type" (Not-Worrying, Not-Distracting, Trusting) play distinct roles — the former belongs to S, while the latter already carries threat-appraisal content and may partially overlap with A. This decomposition tests whether gating is endogenous to interoceptive structure itself.
- **H1.5 (resource conditions, derived from the KGSS correction)**: gating strength is moderated by individual resource conditions. Under low-resource conditions (low subjective SES, high childhood trauma load) threat appraisal tightens coupling, whereas under high-resource conditions the effect attenuates or reverses. This hypothesis follows directly from the reinterpretation in §1.2.1 and is the only testable corollary in this proposal derived inductively from the cross-cultural data.

### 3.4 Analysis plan (pre-registration points)

- Primary model: `IDAS-II ~ MAIA-2 × LTE-Q + age + sex + group`
- HC3 robust standard errors as default, consistent with CSS
- Multiple comparisons: Bonferroni correction across the primary hypothesis family
- **Dual-route verification**: continuous moderation *and* grouped Fisher z. (In CSS this is exactly where stress_total showed weakness; it must be declared in advance.)
- Confound control: negative-affect disposition (IDAS-II Dysphoria) and its interaction with S, reusing the CSS exclusion logic
- Sensitivity analyses: separate models by group; alternative operationalization of S (MAIA vs BPQ)

### 3.5 Feasibility

**Highest.** Questionnaire-only analysis, independent of the fMRI preprocessing pipeline; participant pool already established; questionnaire data accumulate continuously while scanning proceeds. n ≈ 35–40 suffices for interpretable preliminary results.

---

## 4. Study 2: Sinjin-gwaje EMA — signal level or interpretation level?

### 4.1 Data source

CAD Lab Sinjin-gwaje 4-year longitudinal study (currently in baseline collection):

| Module | Content |
|--------|---------|
| EMA | 2 weeks, 2–7 prompts/day (mean ≈ 6), Cadtracker app |
| Objective physiology | Garmin vivoactive 5: heart rate, sleep, activity, wear time |
| Lab physiology | HRV (BIOPAC, resting); inflammatory markers + cortisol (optional) |
| Behavioral | Executive function battery (Stroop / antisaccade / plus-minus / keep-track / local-global); interoception task |
| Clinical | SCID semi-structured interview (annually × 4); online survey (every 6 months × 8) |
| Imaging | MRI session |

### 4.2 Hypotheses

- **H2.1 (individual differences in within-person coupling)**: the within-day slope from bodily state to affect varies significantly across individuals (random slope variance > 0).
- **H2.2 (cross-level gating)**: this individual variation is systematically explained by threat appraisal disposition / threat load (LTE-Q, K-CTQ, person-mean of EMA momentary stress appraisal).
- **H2.3 (level localization — core hypothesis)**: gating is significant on the **subjective bodily perception** → affect path, but null or significantly weaker on the **objective physiology** (Garmin HR/sleep) → affect path, supporting H-interpretation.
- **H2.4 (sleep pathway)**: the effect of prior-night sleep (Garmin objective + EMA sleep diary self-report) on next-day affect is likewise gated by threat appraisal, with an objective/self-report dissociation pattern consistent with H2.3.
- **H2.5 (resource conditions, parallel to H1.5)**: the cross-level gating effect (H2.2) is itself moderated at second order by individual resource conditions (subjective SES, childhood trauma), in the direction specified by H1.5. Observing this pattern across two independent datasets would provide mechanistic support for the "conditional consistency" reading of KGSS.

### 4.3 Analysis plan (pre-registration points)

Multilevel model (three levels: beeps within days within persons):

```
Level 1: Affect_ijk ~ β0_jk + β1_jk·(BodyState_ijk − person mean) + ε
Level 2: β1_jk ~ γ10 + γ11·(ThreatAppraisal_k) + u1_jk
```

Methodological declarations to fix in advance:
- **Centering**: person-mean centering of Level-1 predictors, to strictly separate within- from between-person variance
- **Random slopes**: β1 must be permitted to vary randomly, otherwise H2.1 is untestable
- **Parallel objective and self-report models**: fitted separately rather than jointly, to prevent collinearity from masking the dissociation; then compared via a formal coefficient-difference test
- **Missingness and compliance**: EMA response rate and Garmin wear time (protocol requires mean daily non-wear < 3 h) enter as stratifying variables in sensitivity analyses, not as post-hoc exclusions
- **Multiple comparisons**: correction across the H2.1–H2.4 family

### 4.4 Connection to existing skills

The **EMA sleep diary cleaning tool** I have developed and repeatedly audited over the past six months (R package + skill, near completion; GitHub: cyracaid/sleepdiary-cleaner) is precisely the first stage of H2.4. Integrating it with the lab's existing EMA pipeline would serve the lab while directly constituting the data-preparation foundation for this study.

### 4.5 Feasibility

**Moderate-to-high, contingent on recruitment rate.** EMA data for each participant complete within 2 weeks, so the full longitudinal study need not conclude first. n ≈ 25–30 supports preliminary multilevel analysis. Key risks are baseline recruitment pace and accessibility of Cadtracker data export — both to be confirmed with the PI.

---

## 5. Relationship between the two studies

| | Study 1 | Study 2 |
|---|---------|---------|
| Data | Misophonia study (questionnaire) | Sinjin-gwaje (EMA + biosensing) |
| Design | Cross-sectional, between-person | Intensive repeated measures, within-person |
| Gating level | Not separable | **Separable** (core contribution) |
| Role | Guaranteed deliverable + clinical extreme-group validation | Main line, mechanistic advance |
| Preliminary results expected | 6–9 months | 9–12 months |

Both share the same formal hypothesis, forming a complementary structure of *cross-sectional validation in a clinical extreme group* plus *within-person mechanistic localization in a general sample*. They can be written as two studies in one paper, or as sister papers.

---

## 6. Timeline (12 months)

| Phase | Months | Content |
|-------|--------|---------|
| 1 | M1–M2 | Confirm data access and IRB secondary-analysis procedures; complete literature review; finalize pre-registration |
| 2 | M2–M4 | Build Study 1 analysis pipeline (validated on simulated/partial data); finalize sleepdiary-cleaner and integrate with lab pipeline |
| 3 | M4–M7 | Study 1 preliminary analysis (n ≈ 35–40); first preliminary results |
| 4 | M6–M10 | Study 2 data cleaning and multilevel model construction |
| 5 | M9–M12 | Study 2 preliminary analysis (n ≈ 25–30); integrate both studies into a full draft |

---

## 7. What I can contribute

1. **EMA data engineering**: sleepdiary-cleaner (R package + skill), iteratively audited, near completion, directly deployable to the lab's EMA pipeline.
2. **A complete robustness workflow**: HC3 robust standard errors, Bonferroni correction, six-test stress protocol, discriminant-validity design, and confound exclusion (neuroticism) have all been executed hands-on in the CSS project. This workflow transfers directly to both studies here.
3. **Multilingual literature processing**: an established Chinese/English/Korean close-reading and synthesis system (Zotero-linked workflow and literature note standards already built).
4. **Ongoing lab participation**: continued involvement in lab session duties and assistance work.

---

## 8. Questions for the PI (meeting checklist)

### Data access
1. What is the current n for completed scans/questionnaires in the misophonia study? Projected n in one year?
2. Can the 14 online questionnaires from the misophonia study be accessed for analysis before scanning is fully complete?
3. How many baseline participants have been completed in Sinjin-gwaje? How many have complete EMA datasets?
4. What is the export format for Cadtracker EMA data and Garmin biosensing data? Does a cleaned version already exist?

### Ownership and collaboration
5. Are either of these analysis directions already claimed by another graduate student or researcher?
6. If I proceed, would this be an independent personal project or nested under an existing project? How would authorship be arranged?
7. Does secondary analysis of these data require additional IRB procedures (amendment report / addition of investigator)?

### Tools and contribution
8. Could sleepdiary-cleaner be integrated into the lab's existing EMA pipeline? What format specifications would it need to meet?

### Direction
9. From the PI's perspective, which of Study 1 or Study 2 merits priority? Is there a third dataset I have not seen that would be more suitable?
10. For preliminary results within one year, what does the PI consider a realistic target (conference abstract / full draft / submission)?

---

## 9. Action items and risks

### Internal action items (before the meeting)
- [x] **KGSS sign discrepancy verified and diagnosed** (2026-08-21): not a sign error, but the use of the deprecated v1 analysis (f4c_mean) as the CSS baseline in Section B3. See §1.2.1.
- [ ] **Re-run Section B3 of the KGSS report**: regenerate the CSS simple-slopes table from v2 (f4c_3) and rewrite the "comparison" and "conclusion" paragraphs accordingly. The existing conclusion of "directional inconsistency across samples" must become "conditional consistency, with SES as a second-order moderator."
- [ ] Revise the corresponding "partial replication failure" language in the repository overview (README)
- [ ] Prepare a one-page summary of CSS results for the meeting (using v2 figures)

### Principal risks
| Risk | Mitigation |
|------|------------|
| Recruitment slower than expected; insufficient n | Study 1 as the floor (pool already established); declare minimum analyzable n in advance |
| EMA data quality (response rate, wear time) | Compliance as a stratifying sensitivity variable rather than post-hoc exclusion |
| Data ownership or direction already claimed | Confirm explicitly at the meeting (questions 5–7) |
| Gating effect fails to replicate in lab data | A boundary-condition result is itself informative; and the level-dissociation design of Study 2 yields theoretical information regardless of direction |

---

*v1.0 draft. To be revised following the PI meeting in light of actual data availability.*
