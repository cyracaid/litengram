# Misophonia Indieproj — 1:1 Update (Clean Version)

> For: 1:1 update with Prof. Juyoen Hur. Format: talking points / leave-behind document, not slides.
> Full technical version: `proposals/v3/v3_proposal_reviewed_EN.md`. Literature detail: `literature/NOVELTY_AUDIT_ADDENDUM_20260903.md`.
>
> AUTHOR: Cai Dong and the AI Claude Sonnet

---



## The question

**Does misophonia severity depend more on how strongly bodily sensations are registered, or on how threateningly they are appraised — and does appraisal *gate* the conversion of registration into severity, rather than just add to it?**

## Why this is a real gap, not a rediscovery

Three things are already known separately in the literature:
- Bodily-sensitivity measures (ASI-3 Physical Concerns) are elevated in misophonia (N=628 community sample, 2018).
- Anxiety sensitivity relates to misophonia and aggression (2021; extended to youth, 2026).
- **The closest precedent** (Wang, Vitoratou et al., 2022, N=703): when appraisal-type variables (emotional threat appraisal, externalising appraisal) are modeled *alongside* anxiety sensitivity and interoception, the appraisal variables predict outcomes (outbursts, functional impact) and **anxiety sensitivity and interoception drop out as significant independent predictors.**

**No study has entered registration and appraisal as a single competing model against misophonia *severity*, confirmed the two are separable constructs, and tested whether appraisal gates the conversion — that combination is the gap this project fills.**

**Recent (2026) neuroimaging is broadly consistent with this direction**: two 2026 papers (Ajmera/Khan, *Hearing Research*; Jain/Ajmera, *Cognitive, Affective, & Behavioral Neuroscience* — same lab, not independent lines) report altered connectivity/activation in misophonia beyond simple auditory processing. Cited as background support only — their exact findings weren't independently re-verified against full text, so I'm not leaning on specifics from them yet.

**External validation resource**: MATA (Misophonia Audiovisual Trigger Archive — Oh, Palmer et al., bioRxiv preprint, 2025; 1,300 standardized trigger clips, validated on 26 misophonia + 26 control participants) is cited in the full proposal (§4.6) as independent construct-validity support that trigger-specific distress replicates across stimulus sets/labs — not used as a stimulus set or data source, so it doesn't touch the zero-new-collection constraint.

## Conceptual model vs. what's actually tested

Kept these two diagrams separate on purpose — an earlier self-review caught that a single combined figure risked implying a temporal/causal chain that isn't what's being tested this year.

**(a) Conceptual model** — shows how the constructs relate, not a causal or temporal claim:

```
              Bodily sensation
             /                \
            ▼                  ▼
   Registration (S)      Appraisal (A)
   MAIA-2 / BPQ-SF-A         ASI-3
             \                  /
              \                /
               ▼              ▼
     Does A gate the S→M conversion,
        or just add to it independently?
                     |
                     ▼
          Misophonia Severity (M)
               AMISOS-R
```

**(b) Empirical test structure** — what each layer actually tests, this year:

```
Layer 1 · Questionnaire (N=80, cross-sectional)
  MAIA-2/BPQ (S), ASI-3 (A)  →  regression on AMISOS-R (M)
  [discriminant-validity check runs first: are S and A even separable?]

Layer 2 · Trial-level (~3,360 observations)
  42-sound auditory task
  A × trigger-type interaction  →  aversion rating
  [this is where the gating functional form is powered to be tested]

Layer 3 · Neural (scheduled into this year's plan)
  Interoceptive attention task
  anterior insula vs. posterior/mid insula ROI activation ~ S, A
  [individual-differences design, not group-average]
```

No arrow in (b) is a temporal or causal test — all are correlational, cross-sectional, or trial-level associations.

## Design (uses only existing CAD Lab data — zero new collection)

| Layer | Data | Status |
|---|---|---|
| 1 · Questionnaire | MAIA-2/BPQ (registration) vs. ASI-3 (appraisal) → AMISOS-R (severity), with SPSQ/OCI-R discriminant controls | Ready; runs on current n |
| 2 · Trial-level | 42-sound auditory task, ≈3,360 trial observations, carries the gating test at adequate power | Ready; needs trial-level log format confirmed |
| 3 · Neural | Interoceptive attention task (heart/gut/visual), anterior vs. posterior/mid insula dissociation | Designed, pre-registered, **scheduled into this year's plan** — see "what I need from you" |

**Before any confirmatory analysis runs**: a discriminant-validity check (are MAIA/ASI-3 actually separable constructs, or measuring the same thing twice?) — this is now step zero, added after self-review.

## What I need from you

1. **Data access questions** (unchanged from before): complete trial-level log format/access for Layer 2; current n and projection; IRB status for secondary analysis.
2. **Layer 3 coordination**: the neural layer is fully designed (ROI method now specified — anterior/posterior insula coordinates from a published meta-analysis and a term-based literature map, not selected from our own contrast, to avoid circularity) and is scheduled into this year's plan. The one thing I need from you is how it should be coordinated with the lab's own interoceptive-imaging work. fMRI analysis is new to me, so I'm learning the pipeline (SPM, preprocessing) alongside the timeline — I'm glad to put in that time; I just want the coordination with your team's work settled early.

## Bottom line

Layers 1–2 are executable now, inside the original constraints (no new data, no fMRI-preprocessing dependency for the primary deliverable). Layer 3 is scheduled in and fully designed; I'd like your input on how it's coordinated with the lab's own interoceptive-imaging work.
