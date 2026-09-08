# MRI Head Coil Channel-Count Differences and Cross-Site fMRI Poolability
### A Methodological Review for Anxiety & Depression Clinical Neuroimaging

**Format:** CAD Lab internal PI memo
**Date:** 2026-07-20
**Status:** Rewrite of prior head coil review after completing citation audit. Every citation below was verified against PubMed / publisher records or vendor documentation at the time of writing. Where the literature cannot answer a question, that is stated explicitly rather than filled by extrapolation.

**Two corrections carried forward from audit (not repeated below):**
- Prior version cited Panman et al. 2019 as *NeuroImage* 2019;186:412–420. **Correct citation: *Frontiers in Neuroscience* 2019;13:729, doi:10.3389/fnins.2019.00729.**
- Prior version cited Kaza et al. 2011 as *JMRI* 34(3):552–562, doi:10.1002/jmri.22644. **Correct citation: *JMRI* 34(1):173–183, doi:10.1002/jmri.22614.**

Throughout this document, the following conventions apply: **[Confirmed]** = shown in published empirical work; **[Inference]** = expected from MRI physics but not directly measured for this specific case; **[No Direct Evidence]** = literature does not address this.

---

## 1. Clinical Research Context

fMRI studies of anxiety and depression increasingly rely on data pooling — across sites, across time, and across hardware — because single-site samples lack statistical power for the typically small, distributed effects in psychiatric neuroimaging. The REST-meta-MDD consortium exemplifies this: it pooled resting-state fMRI from 25 cohorts (17 sites after QC) precisely because single-site depression studies had produced inconsistent, underpowered, and sometimes contradictory results (Yan et al. 2019, *PNAS*).

For CAD Lab, the hardware question is not abstract. The brain regions most central to anxiety/depression models — amygdala, subgenual/ventromedial PFC, ventral striatum, hippocampus, insula, dorsal ACC, and dlPFC — sit at very different depths and therefore have very different sensitivity to receive-coil geometry. If a coil-driven measurement bias happens to fall on one of these regions, it can mimic, amplify, or mask a clinical effect. The risk is highest for **between-group** comparisons when coil correlates with group, and for **longitudinal** comparisons when coil correlates with timepoint. The task of this memo is to clarify what is actually *known* about this risk and what should be *done* about it.

---

## 2. MRI Physics Background (Concise — Only What Matters for the Decision)

- **Receive channels / phased arrays.** Modern head coils are arrays of many small receive elements. Each element is most sensitive to nearby tissue; signals are combined across elements. More channels generally mean higher peripheral SNR and better parallel imaging (GRAPPA/SENSE) performance. **[Confirmed]** (Wiggins et al. 2006; de Zwart et al. 2004).
- **SNR is not uniform.** The multi-element advantage is largest at the cortical surface and decays with depth; deep/central structures benefit far less from increased channel count. **[Confirmed]** (de Zwart et al. 2004; Wiggins et al. 2006).
- **Image SNR (SNR₀) vs temporal SNR (tSNR).** BOLD sensitivity depends on tSNR, which is jointly determined by thermal noise (hardware/coil-related) and physiological noise (signal-dependent). Where physiological noise dominates, increasing coil SNR produces little tSNR improvement; where thermal noise dominates (small voxels, deep regions, high acceleration), coil SNR matters directly. **[Confirmed]** (Triantafyllou, Polimeni & Wald 2011; Krüger & Glover 2001).
- **Why coil differences bias fMRI.** Because coil geometry changes the spatial SNR distribution, it regionally alters tSNR, thereby changing BOLD detection power and potentially shifting connectivity estimates — and does so non-uniformly across the brain. That this *occurs* is **[Confirmed]** ; the exact magnitude for any specific new setup is **[Inference]** and must be measured locally.
- **B₁⁺ (transmit).** At 3T, transmission is performed by the body coil; the receive array does not materially alter the transmit field. Coil channel differences are a **receive-side / SNR** phenomenon, not a flip-angle phenomenon. **[Confirmed / Standard Conclusion]** .

---

## 3. Head Coil Direct Comparison Studies

**Evidence hierarchy, separated by design, where requested:**
**A** = same subjects scanned with different coils (within-subject); **B** = same scanner, different coils, different subjects; **C** = different scanner/site/coil.

### Question 1 Summary Table — Published Coil Comparisons

| Study | Scanner / Vendor | Field | Coils Compared | n | fMRI Type | Key Finding | Level |
|---|---|---|---|---|---|---|---|
| Kaza, Klose & Lotze 2011 (*JMRI* 34(1):173–183) | Siemens | 3T | 12ch vs 32ch | n=36, within-subject | Visual-motor task | 32ch gives higher tSNR and activation in **cortical** regions; benefit for **deep** structures (thalamus, cerebellum) is **not significant**; prescan normalize helps | **A** |
| Paolini et al. 2015 (*Acta Radiol* 56(5):605–613) | Philips | 3T | 8ch vs 32ch | n=26, within-subject, counterbalanced | Resting-state (ICA) | 32ch has higher phantom SNR but **no significant difference in any RSN** at standard parameters | **A** |
| Panman et al. 2019 (*Front Neurosci* 13:729) | Philips | 3T | 8ch vs 32ch | n=77, within-subject | T1 + DTI + Resting-state | Coil-related bias found in GM/WM volume, FA (~4–6%), and **resting-state FC (posterior networks up to ~27.5%)** ; larger n than Paolini, **does** detect FC differences | **A** |
| Schmitt & Rieger 2021 (*Front Neurosci* 15:735290) | Siemens Prisma | 3T | 20ch vs 64ch (head/neck) | n=26, within-subject | Motor / auditory / visual tasks | tSNR and β differences are **region-dependent** and **interact with prescan normalize filter** (opposite direction in cortex vs thalamus) | **A** |
| Triantafyllou, Polimeni & Wald 2011 (*NeuroImage* 55(2):597–606) | Siemens | 3T | 1ch / 12ch / 32ch (SNR benchmark) | Phantom + in-vivo | SNR₀/tSNR characterization | Establishes thermal-physiological noise framework; fewer channels pushes deep/high-resolution regions toward thermal-noise dominance | A (physics benchmark) |
| Wiggins et al. 2006 (*MRM* 56(1):216–223) | Siemens | 3T | 32ch design vs 8ch | Phantom + in-vivo | SNR/g-factor benchmark | 32ch: large peripheral SNR gains, limited central gains, improved parallel imaging | (hardware benchmark) |

### What This Body of Evidence Actually Says

1. Coil channel differences produce **real, measurable effects** on fMRI-derived metrics — this is not in doubt (Panman 2019; Kaza 2011).
2. The effect is **regionally specific** — larger where coil sensitivity differs most (peripheral/cortical, and where acceleration pushes regions toward thermal-noise dominance), relatively smaller in deep structures (where SNR is source-limited to begin with) (Kaza 2011; Schmitt 2021). **[Confirmed]**
3. The effect is **not always detectable at small n**: Paolini (n=26) found no significant RSN differences between 8ch and 32ch, while Panman (n=77) did. This is a statistical power issue, directly refuting the argument that "the difference is negligible" — it may simply have gone undetected in a smaller sample. **[Confirmed]**
4. **Acquisition-side filtering matters and is not neutral:** the prescan normalize filter alters the coil effect in a region-dependent way (Schmitt 2021), so it must be kept constant and not toggled between two sites.

### Critical Gaps (Candid)

- **No published study directly compares the Siemens 32-channel head coil to its own lower-20-element-only configuration for fMRI.** The closest same-vendor same-scanner fMRI comparisons are 12-vs-32 (Kaza) and 20-vs-64 (Schmitt). For the exact 20-vs-32 comparison, this is **[No Direct Evidence]** .
- The 8-vs-32 evidence (Paolini, Panman) uses **Philips** coils of physically different design, not the Siemens 20/32 configuration. Directionally informative; not a substitute.
- **Level B designs (same scanner, different coils, different subjects) are essentially absent** — coil comparisons are almost all within-subject. This matters because Level B is the design most vulnerable to coil–group confounding, and the CAD Lab's cross-site setup partially resembles it.

---

## 4. Multi-Center fMRI Studies with Hardware Differences

When data are pooled across scanner/coil/site, the coil difference is **not** isolated — it is one component of a confounded site/scanner/coil "batch" effect. How major projects handle this:

- **HCP** (Van Essen et al. 2013, *NeuroImage* 80:62–79): Controls hardware variance through **standardized acquisition** (custom scanners, fixed protocol, identical preprocessing). The philosophy is "prevent, don't correct" — at the opposite end of the spectrum from CAD Lab's situation.
- **ABIDE** (Autism Brain Imaging Data Exchange; consortium dataset): Sites vary widely in scanner/coil/protocol; downstream users typically model **site** as a factor or apply **ComBat** to derived metrics. *(HCP, ENIGMA, and REST-meta-MDD citations have been verified in this memo; the specific ABIDE citation should be confirmed against the version you cite before it goes in a manuscript.)*
- **ENIGMA** (Thompson et al. 2014, *Brain Imaging Behav* 8(2):153–182): Distributes standardized analysis protocols to each site and performs meta/mega-analysis, explicitly treating **site** as the unit of harmonization.
- **REST-meta-MDD** (Yan et al. 2019, *PNAS* 2019, doi:10.1073/pnas.1900390116): The most relevant clinical precedent. 17 sites, resting-state fMRI, depression. Handles heterogeneity through (i) a **standardized local preprocessing pipeline** run identically at each site, and (ii) statistical treatment of **site** in group analysis. It does **not** ignore hardware differences.

### Question 3 Table — Whether Each Study Pooled Across Hardware, and How

| Study / Project | Hardware Difference | Analysis Approach | Control Method | Result |
|---|---|---|---|---|
| Paolini 2015 | 8ch vs 32ch, same subjects | Comparison (not pooled) | Within-subject, counterbalanced | No significant RSN differences at n=26 |
| Panman 2019 | 8ch vs 32ch, same subjects | Comparison (not pooled) | Within-subject | Significant coil bias in volume/FA/FC at n=77 |
| Yu et al. 2018 (*HBM* 39:4213–4227) | Multi-site scanners | Pooled FC metrics | **ComBat** on connectivities, site=batch, biology=covariates | ComBat removes site effects, preserves/enhances age effects |
| Yan et al. 2019 (REST-meta-MDD) | 17 sites, mixed scanner/coil | Mega-analysis | Standardized pipeline + site modeling | Reproducible DMN finding (recurrent MDD) |
| Wang, Chen & Yan 2023 (*NeuroImage* 274:120089) | Multi-site + traveling subjects | Benchmarked 11 methods | **SMA** vs ComBat etc. | SMA best overall for rs-fMRI, including identifiability |

**Takeaway:** In credible multi-site work, **nobody pools across hardware without addressing it.** They either standardize acquisition/preprocessing, model site/scanner/coil as a factor, or apply harmonization methods (typically on *derived* metrics). Direct, uncontrolled pooling is not an accepted practice, and there is **[No Direct Evidence]** that it is safe.

---

## 5. Statistical & Technical Control Methods

### Question 4 — Organized by Level of Control

**Acquisition-level:**
- Same scanner model / same sequence / matched TR, TE, resolution, GRAPPA, bandwidth. This is **prevention** not correction of bias, and is the strongest control available. That it works in principle is **[Confirmed]** (HCP).
- **Prescan normalize filter kept constant** — because it interacts with coil in a region-dependent way (Schmitt 2021). Toggling it between sites would *create* bias.
- **Traveling-subject design** (same people scanned on both setups): The only way to directly measure the actual local coil/site effect, and the most valuable input for harmonization methods. That this is valuable is **[Confirmed]** (Wang 2023; Yamashita 2019).
- Phantom calibration: useful for SNR/QC baselines; cannot capture in-vivo BOLD/FC effects on its own.

**QC-level:**
- **Per-session tSNR maps** (regional, especially dlPFC and subcortical ROIs).
- **Framewise displacement / motion** — must be matched across coil/site groups, because motion confounds FC and may correlate with claustrophobia (hence coil choice).
- **MRIQC-like metrics** and **signal dropout / coverage checks** (especially OFC and temporal poles).
- Log and record the exact coil/configuration per session in the analysis database.

**Statistical control:**
- **Site / scanner / coil as covariates** in group models: captures only *global* mean shifts. It is the necessary floor but **not sufficient** for the spatially non-uniform bias that coil differences produce. The limitation is **[Confirmed]** .
- **Region-specific tSNR as a covariate**: better, because it allows the nuisance to vary by region.
- **Mixed-effects models** (random effects of site/subject): appropriate for longitudinal/multi-site structure.

**Harmonization methods:**

| Method | Purpose | Evidence Base | Specifically Validated for *Coil* Differences? |
|---|---|---|---|
| **ComBat / NeuroComBat** (Johnson 2007; Fortin 2017, 2018) | Empirical Bayes removal of additive + multiplicative site/batch effects on derived features | Strong for cross-site DTI, cortical thickness | **[Inference]** — validated for *site/scanner* batches, not specifically for coil channel differences; reasonable if coil is treated as (part of) batch with sufficient scans per batch |
| **ComBat for functional connectivity** (Yu et al. 2018, *HBM*) | Site correction for FC/network metrics | Confirmed for multi-site rs-FC | **[Inference]** for coil specifically; closest evidence at the FC level |
| **Longitudinal ComBat** (Beer et al. 2020, *NeuroImage* 220:117129) | Harmonization when same subject is scanned on different scanners over time | Confirmed on longitudinal/traveling data | Correct variant **if** CAD Lab sessions mix coil/site within subject over time (Scenario C) |
| **SMA — Subsampling Maximum mean-distance distribution shift correction** (Wang, Chen & Yan 2023) | Distribution-shift correction for rs-fMRI | Best overall for rs-fMRI vs ComBat, including identifiability | **[Inference]** for coil; currently the best choice if the problem is multi-site rs-fMRI |
| **ComBat-GAM** (Pomponio et al. 2020) | Harmonization with non-linear (e.g., age) covariates | Confirmed on lifespan structural data | **[Inference]** ; relevant if non-linear covariates are important |

**Honest caveat for all harmonization methods in this use case:** Each of the above methods was validated on **site/scanner** batch effects. There is **[No Direct Evidence]** that any has been specifically validated on a *20ch-vs-32ch coil* difference. They are reasonable, defensible tools — but they are inference for coil-channel harmonization, not confirmation; and they require sufficient scans per batch to estimate batch parameters. They also risk removing true biological signal if coil is confounded with group.

---

## 6. Direct Answers to the CAD Lab Question

**Situation:** Korea site — 32-channel head coil; US site — 20-channel head coil.

**First, a prerequisite for the answer.** Establish what the US "20-channel" coil physically *is*: (a) a lower-20-element-only mode of a Siemens 32-channel head coil, (b) a standalone Siemens 20-channel head/neck coil, or (c) another vendor/model. This changes the physics. **Do not assume it is the lower-20 mode of a 32-channel coil** — that was a flaw in the prior review.

### Question 2 — Can Data from Different Channel Counts Be Pooled?

**Scenario A — Same scanner model + same sequence + different coil channel count (e.g., 32ch vs 20ch on the same scanner model):**
- **Pooling: conditionally acceptable.** The only isolated variable is coil sensitivity.
- **Bias:** Regional tSNR/BOLD sensitivity differences (largest in peripheral/dorsal cortex; smaller but non-zero in deep structures); FC shifts detectable at adequate sample size (Panman 2019). That the effect exists is **[Confirmed]** ; the exact magnitude here is **[Inference]** .
- **Risk:** Low-to-moderate if coil is balanced across groups/timepoints and primary ROIs are subcortical; moderate-to-high if primary analyses target dorsal/superior cortex, or if coil correlates with group or timepoint.
- **Required:** Matched sequence + prescan normalize kept constant; coil covariate (preferably regional tSNR); sensitivity analysis with and without minority-coil sessions.

**Scenario B — Different sites + different scanners + different coils (the actual CAD Lab situation):**
- **Pooling: acceptable only with active harmonization; covariate-adjustment alone is insufficient.** Here the coil difference is inseparable from scanner and site.
- **Bias:** Full site/scanner/coil batch effect — larger and less predictable than coil alone.
- **Risk:** **High** without traveling-subject data; moderate with them.
- **Required:** Standardized acquisition and preprocessing across sites (REST-meta-MDD model); modeling of site/scanner; harmonization on derived metrics (SMA or ComBat for rs-FC; longitudinal ComBat if within-subject over time); ideally a few traveling subjects to quantify the actual effect. There is **[No Direct Evidence]** that Korea-32ch and US-20ch data can be pooled *without* these controls, and no published study isolates "cross-site 20-vs-32-channel" as a solved case.

### Recommendations by Hardware Match

- **If both sites have the same scanner model:** Treat as Scenario A. Conditional pooling with "acquisition + covariate + sensitivity analysis" package is reasonable.
- **If scanner models differ:** Scenario B. Harmonization required; covariate alone is insufficient.
- **If sites differ (actual situation):** Scenario B. Prioritize standardized pipeline + harmonization + (ideally) traveling subjects. Consider restricting primary hypotheses to subcortical/limbic ROIs where coil effects are smallest, and treating dorsal-cortical findings as secondary.

---

## 7. Reviewer Perspective (NeuroImage / HBM / Biological Psychiatry)

**Concern:** "Your coil/site is confounded with group or timepoint; the effect could be hardware not psychopathology."
→ **Response:** Report the coil/site × group (and × timepoint) cross-tabulation and test for imbalance; model site/coil; run primary analyses with and without minority-configuration sessions.
→ **Analysis:** χ²/logistic regression test of coil–group independence; re-analysis with covariates + harmonization; full reporting of sensitivity analyses.

**Concern:** "You pooled across different coils — how do we know group effects aren't measurement bias?" (Reviewer will cite Panman 2019's 27.5% FC difference.)
→ **Response:** Acknowledge and cite that coil bias is real; show that effects survive harmonization and lie in regions/edges different from the coil-bias map.
→ **Analysis:** ComBat/SMA on FC (Yu 2018; Wang 2023); overlay findings on empirically measured (traveling-subject or pilot) coil-difference maps.

**Concern:** "Covariate adjustment cannot fix spatially non-uniform bias."
→ **Response:** Agreed; this is exactly why a global covariate is a floor, not a solution.
→ **Analysis:** Region-specific tSNR covariate and/or feature-level harmonization, not a single binary regressor.

**Concern:** "For the longitudinal arm, coil switching will mimic change."
→ **Response:** Balance coil/site across timepoints where possible; use longitudinal harmonization models.
→ **Analysis:** Longitudinal ComBat (Beer 2020); per-subject tSNR QC; report transition balance.

**Concern (Structural):** "There is no direct literature validating cross-site 20-vs-32-channel pooling."
→ **Response:** Correct — state this explicitly, and provide your own local evidence (pilot/traveling-subject coil difference maps) rather than claiming literature support that does not exist.

---

## 8. Final Recommendation

**Verdict:** **Conditionally acceptable** — provided (1) the exact hardware of the US coil is established, and (2) site/coil harmonization is implemented, not just covariate adjustment. Downgraded to **not recommended** for specific analyses if primary hypotheses require dorsal/superior cortex fMRI and traveling-subject data are unavailable.

**Confidence level:** **Low-to-moderate.** The general phenomenon (coil differences produce regional, sample-size-dependent biases in fMRI) is well confirmed. The specific cross-site 20-vs-32 situation is **not** directly studied; this recommendation rests on adjacent evidence plus standard multi-site practice, and must be backed by lab-specific measurements.

**Required steps:**
1. **Acquisition documentation:** Identify and record the exact scanner model, coil model/configuration, sequence, and prescan normalize state per session; keep sequence and prescan normalize constant across sites.
2. **Quality control:** Per-session regional tSNR (dlPFC + subcortical ROIs), matched framewise displacement across sites/coils, coverage/dropout checks (OFC, temporal poles), MRIQC-like metrics.
3. **Local evidence (substituting for missing literature):** Acquire a small traveling-subject/pilot dataset scanned on both setups to measure the actual site+coil difference map. This is the single most valuable action item.
4. **Preprocessing:** Identical pipeline at both sites (REST-meta-MDD model); unified intensity scaling.
5. **Statistical control:** Model site/scanner/coil; prefer region-specific tSNR covariates over a single binary flag; mixed effects for longitudinal/multi-site structure.
6. **Harmonization:** For rs-fMRI derived metrics, use ComBat (Yu 2018) or SMA (Wang 2023); for within-subject over time with switching coil/site, use longitudinal ComBat (Beer 2020) — and include biological covariates to protect true effects.
7. **Sensitivity analysis:** Report all primary findings before and after harmonization, and with and without the minority-coil site included; test coil–group and coil–timepoint independence; discuss site/coil as a limitation regardless of outcome.

**Explicit limitation that should appear in any paper arising from this work:** No published study directly validates combining 32-channel and 20-channel head-coil fMRI data across sites; the conclusions rest on adjacent coil-comparison and multi-site harmonization literature supported by locally measured coil-difference estimates.

---

## Verified References

1. Wiggins GC, Triantafyllou C, Potthast A, Reykowski A, Nittka M, Wald LL. 32-channel 3 Tesla receive-only phased-array head coil with soccer-ball element geometry. *Magn Reson Med.* 2006;56(1):216–223. doi:10.1002/mrm.20925
2. Triantafyllou C, Polimeni JR, Wald LL. Physiological noise and signal-to-noise ratio in fMRI with multi-channel array coils. *NeuroImage.* 2011;55(2):597–606. doi:10.1016/j.neuroimage.2010.11.084
3. Krüger G, Glover GH. Physiological noise in oxygenation-sensitive magnetic resonance imaging. *Magn Reson Med.* 2001;46(4):631–637. doi:10.1002/mrm.1246
4. de Zwart JA, Ledden PJ, van Gelderen P, Bodurka J, Chu R, Duyn JH. Signal-to-noise ratio and parallel imaging performance of a 16-channel receive-only brain coil array at 3.0 Tesla. *Magn Reson Med.* 2004;51(1):22–26. doi:10.1002/mrm.10678
5. **Kaza E, Klose U, Lotze M.** Comparison of a 32-channel with a 12-channel head coil: are there relevant improvements for functional imaging? *J Magn Reson Imaging.* 2011;34(1):173–183. doi:10.1002/jmri.22614 *(Corrected from prior version)*
6. Paolini M, Keeser D, Ingrisch M, Werner N, Kindermann N, Reiser M, Blautzik J. Resting-state networks in healthy adult subjects: a comparison between a 32-element and an 8-element phased array head coil at 3.0 Tesla. *Acta Radiol.* 2015;56(5):605–613. (PMID 25585849)
7. **Panman JL, To YY, van der Ende EL, et al.** Bias introduced by multiple head coils in MRI research: an 8 channel and 32 channel coil comparison. *Front Neurosci.* 2019;13:729. doi:10.3389/fnins.2019.00729 *(Corrected from prior version)*
8. Schmitt T, Rieger JW. Recommendations of choice of head coil and prescan normalize filter depend on region of interest and task. *Front Neurosci.* 2021;15:735290. doi:10.3389/fnins.2021.735290
9. Yan CG, Chen X, Li L, et al. (REST-meta-MDD). Reduced default mode network functional connectivity in patients with recurrent major depressive disorder. *Proc Natl Acad Sci USA.* 2019. doi:10.1073/pnas.1900390116
10. Yu M, Linn KA, Cook PA, et al. Statistical harmonization corrects site effects in functional connectivity measurements from multi-site fMRI data. *Hum Brain Mapp.* 2018;39(11):4213–4227. doi:10.1002/hbm.24241
11. Fortin JP, Parker D, Tunç B, et al. Harmonization of multi-site diffusion tensor imaging data. *NeuroImage.* 2017;161:149–170. doi:10.1016/j.neuroimage.2017.08.047
12. Fortin JP, Cullen N, Sheline YI, et al. Harmonization of cortical thickness measurements across scanners and sites. *NeuroImage.* 2018;167:104–120. doi:10.1016/j.neuroimage.2017.11.024
13. Beer JC, Tustison NJ, Cook PA, et al. Longitudinal ComBat: a method for harmonizing longitudinal multi-scanner imaging data. *NeuroImage.* 2020;220:117129. doi:10.1016/j.neuroimage.2020.117129
14. Wang YW, Chen X, Yan CG. Comprehensive evaluation of harmonization on functional brain imaging for multisite data-fusion. *NeuroImage.* 2023;274:120089. doi:10.1016/j.neuroimage.2023.120089
15. Pomponio R, Erus G, Habes M, et al. Harmonization of large MRI datasets for the analysis of brain imaging patterns. *NeuroImage.* 2020;208:116450. doi:10.1016/j.neuroimage.2019.116450
16. Yamashita A, Yahata N, Itahashi T, et al. Harmonization of resting-state functional MRI data across multiple sites via matching of histogram and principal components. *Hum Brain Mapp.* 2019;40(6):1787–1798. doi:10.1002/hbm.24490
17. Johnson WE, Li C, Rabinovic A. Adjusting batch effects in microarray expression data using empirical Bayes methods. *Biostatistics.* 2007;8(1):118–127. doi:10.1093/biostatistics/kxj037
18. Van Essen DC, Smith SM, Barch DM, Behrens TEJ, Yacoub E, Ugurbil K; WU-Minn HCP Consortium. The WU-Minn Human Connectome Project: an overview. *NeuroImage.* 2013;80:62–79. doi:10.1016/j.neuroimage.2013.05.041
19. Thompson PM, Stein JL, Medland SE, et al. The ENIGMA Consortium: large-scale collaborative analyses of neuroimaging and genetic data. *Brain Imaging Behav.* 2014;8(2):153–182. doi:10.1007/s11682-013-9269-5

*Not independently re-verified this round (confirm before manuscript submission): specific ABIDE citation (Di Martino et al., ABIDE I *Mol Psychiatry* 2014 / ABIDE II *Sci Data* 2017) — discussed at consortium level only.*
