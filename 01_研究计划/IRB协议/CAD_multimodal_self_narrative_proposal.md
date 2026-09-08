# Proposal Note: Release-Safe Multimodal Self-Narrative Pilot for CAD Lab

Date: 2026-05-27
Prepared by: Cyra Dong

## Working Title

Release-Safe Multimodal Markers of Depressive Symptoms and Interoceptive Awareness in Brief Self-Narrative Videos

## Core Idea

This project would develop a small, IRB/DRC-approved pilot study testing whether privacy-preserving multimodal features extracted from brief self-narrative videos are associated with self-reported depressive symptoms, anxiety symptoms, and interoceptive awareness.

The project is not intended to diagnose depression or replace clinical assessment. Instead, it asks whether structured self-narrative videos can provide measurable affective, linguistic, acoustic, and behavioral signals that align with validated self-report measures.

## Motivation

Clinical and affective neuroscience increasingly uses naturalistic data to understand how affective vulnerability appears in daily life. However, raw video, audio, and transcript data are difficult to share because they contain identifiable and sensitive information. A release-safe multimodal pipeline could help bridge clinical measurement and computational analysis by extracting aggregate, auditable features without releasing raw participant media.

This pilot would connect three themes relevant to CAD lab:

- depressive and anxiety symptoms
- interoception and bodily awareness
- affective expression in naturalistic self-report

## Research Questions

1. Are acoustic, facial/behavioral, and linguistic features from brief self-narrative videos associated with self-reported depressive symptoms?
2. Are body-focused narrative features associated with interoceptive awareness?
3. Do multimodal feature combinations explain symptom or interoception scores better than single-modality features?
4. Can a privacy-preserving feature-extraction protocol produce usable data while avoiding raw video/audio/text release?

## Proposed Participant Task

Participants would record short videos, ideally 2-3 minutes each, responding to standardized prompts.

Example prompts:

- Stress/body prompt: "Please describe how your body usually feels when you are stressed."
- Difficult-day prompt: "Please describe a recent emotionally difficult day and how you responded to it."
- Interoception prompt: "Please describe how you notice changes in your heartbeat, breathing, fatigue, appetite, or sleep."
- Neutral control prompt: "Please describe a typical daily routine."

The task should avoid asking participants to disclose traumatic details. Participants should be told they can skip any question or stop recording at any time.

## Proposed Measures

Primary self-report measures:

- PHQ-9: depressive symptoms
- GAD-7: anxiety symptoms
- MAIA or BPQ: interoceptive awareness / body awareness

Optional measures:

- PSS: perceived stress
- DASS-21: depression, anxiety, stress
- sleep quality or fatigue item set

If PHQ-9 item 9 is included, the study must include a clear risk-response protocol. For a minimal pilot, it may be safer to discuss with the PI/IRB whether to include item 9, use a modified screening procedure, or provide crisis resources without making clinical interventions.

## Data and Privacy Design

Raw data:

- video files
- audio tracks
- automatic transcripts
- questionnaire responses

Release-safe derived data:

- acoustic feature summaries
- facial/behavioral feature summaries
- language feature summaries
- quality-control flags
- window-level multimodal alignment features
- deidentified participant IDs

The project should not release raw videos, raw audio, identifiable transcripts, names, faces, or any direct identifiers.

Participants should not upload their real names as study data. The protocol should use participant IDs and a separate consent/contact file if contact information is needed.

## Candidate Multimodal Features

Acoustic/prosodic features:

- pitch mean and variability
- intensity mean and variability
- speech rate
- pause duration and pause frequency
- voice-quality features where appropriate
- OpenSMILE feature sets

Facial/behavioral features:

- face detection confidence
- facial action unit summaries
- expression variability
- head movement proxy
- gaze/head orientation proxy
- low-confidence frame rate

Language features:

- first-person pronouns
- negative affect and positive affect words
- bodily sensation words
- sleep/fatigue/appetite terms
- uncertainty and cognitive-processing words
- hopelessness or burden terms, handled cautiously
- narrative coherence or temporal organization features

Alignment features:

- synchrony between affective words and acoustic intensity
- synchrony between affective words and facial expression change
- within-video variability across time windows
- contrast between neutral and emotion/body prompts

## Minimal Analysis Plan

Pilot sample:

- Feasibility pilot: N = 30-50
- Stronger pilot: N = 80-120
- More complete validation study: N = 150-250

Analysis:

1. Generate QC report for each modality.
2. Summarize feature distributions and missingness.
3. Correlate multimodal features with PHQ-9, GAD-7, and MAIA/BPQ scores.
4. Fit regularized regression models predicting continuous symptom scores.
5. Compare modality sets: language only, acoustic only, facial/behavioral only, combined.
6. Use cross-validation or permutation testing for exploratory predictive analysis.

Claims should remain modest:

- association with self-reported symptoms
- feasibility of release-safe multimodal measurement
- not clinical diagnosis
- not individual-level deployment

## Ethical and IRB/DRC Notes

This project involves human participants, identifiable media, and sensitive mental-health information. It should not begin data collection before IRB/DRC approval or formal confirmation from the lab/department that the study is exempt or approved.

Important safeguards:

- informed consent for video/audio recording
- clear explanation that the study is not a diagnostic service
- option to skip prompts and withdraw
- no collection of real names in the analysis dataset
- secure storage of raw media
- restricted access to raw video/audio
- no public release of raw media or transcripts
- crisis-resource language for participants
- risk protocol if suicidality items are collected

## Possible Paper Contribution

The paper would not claim to diagnose depression from video. Its contribution would be:

1. a standardized brief self-narrative video protocol
2. a release-safe multimodal feature pipeline
3. a measurement framework connecting features to affective/interoceptive constructs
4. a pilot association analysis with PHQ-9/GAD-7/MAIA or BPQ
5. an ethical discussion of privacy, bias, and limits of clinical prediction

## Fit With Future PhD Narrative

This project supports a broader research identity:

I study how affective and interoceptive vulnerability appears across language, body signals, and daily-life dynamics, using computational and psychophysiological methods while preserving clinical caution and participant privacy.

## Immediate Next Steps

1. Discuss feasibility with CAD PI and confirm whether this could be developed as an independent pilot or thesis-adjacent project.
2. Decide whether the first version should be a small feasibility study or a larger validation study.
3. Draft a one-page IRB/DRC pre-protocol.
4. Select validated questionnaires.
5. Define data storage and access rules.
6. Build a minimal pipeline using synthetic or public non-clinical sample videos before collecting participant data.
7. Prepare a feature dictionary and QC report template.

