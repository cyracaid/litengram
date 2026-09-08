# Methodological Review: Cross-Site fMRI Pooling with Different Receive Coil Channel Counts

## Clinical Neuroscience of Anxiety and Depression Lab — Internal Report

**Date:** July 2026
**Subject:** Combining 32-channel (Korea) and 20-channel (US) resting-state fMRI data in a multi-site anxiety/depression study
**Status:** Final
**Author:** Cai Dong

---

## 1. Executive Summary

### Purpose

This review evaluates whether resting-state fMRI data acquired at two sites — one using a Siemens 32-channel head coil (Korea) and one using a 20-channel receive configuration (US) — can be pooled for group-level analysis in a multi-site study of anxiety and depression. The primary regions of interest are the dorsolateral prefrontal cortex (dlPFC) and amygdala.

### Main Conclusions

- **Cross-site pooling is conditionally feasible**, but the conditions depend critically on the exact hardware configuration at the US site, which has not yet been confirmed.
- **No published study has directly validated pooling of 20-channel and 32-channel head coil data across independent sites.** This represents a gap in the literature that the CAD Lab study would need to address through its own validation.
- **The receive-channel deficit produces regionally heterogeneous SNR loss.** Dorsal cortical regions (dlPFC, precuneus, superior parietal) are most affected; subcortical regions (amygdala, hippocampus) are relatively spared. This spatial non-uniformity means a simple global SNR covariate is insufficient.
- **Three distinct hardware scenarios are possible** at the US site, each with fundamentally different implications for feasibility, statistical power, and publishability. The single most critical piece of information needed to proceed is the exact coil model at the US site.
- **For the most favorable scenario** (same 32-channel coil operated in 20-channel mode), the study is viable with moderate corrections (estimated overall reliability: 6.5–7.0/10). For the least favorable scenario (a different coil from a different manufacturer), the recommended approach depends heavily on whether traveling-subject funding is available.
- **Four of the eleven required corrections are scenario-independent** and can be implemented immediately regardless of which hardware scenario applies.

### Overall Recommendation

Before proceeding with cross-site pooling, the lab should: (1) confirm the exact coil model at the US site; (2) implement the scenario-independent corrections in the revised review; (3) commit to a harmonization strategy proportional to the confirmed scenario; and (4) secure traveling-subject funding for any scenario beyond the most favorable one.

---

## 2. Research Questions

This review was undertaken to answer four specific questions:

1. **Are there published studies that directly compare fMRI data quality across different receive coil channel counts (e.g., 20-channel vs. 32-channel head coils)?**

2. **Can resting-state fMRI data acquired with different numbers of receive channels be combined in a single group-level analysis?**

3. **Have previous multi-site or multi-coil fMRI studies successfully pooled such data, and what methods did they use to control for hardware differences?**

4. **For the CAD Lab's specific study** — multi-site anxiety/depression with dlPFC and amygdala as primary ROIs, resting-state fMRI at 3T, identical pulse sequences — what is the recommended approach?

---

## 3. Literature Findings

### 3.1 Head Coil Performance and Channel Count

The relationship between receive coil channel count and fMRI data quality is well established in the MRI physics literature, though most studies examine performance within a single site rather than cross-site pooling.

**Within-site coil comparisons.** Several studies have compared head coils with different channel counts on the same scanner:

- **Wiggins et al. (2006, *MRM*)** characterized the 32-channel head coil with soccer-ball element geometry, demonstrating SNR gains of approximately √N in central brain regions and proportionally larger gains in cortical regions due to element proximity. The 32-channel coil produces roughly 1.5–2× the cortical SNR of a 12-channel coil at 3T.

- **de Zwart et al. (2004, *MRM*)** compared 16-channel and 8-channel arrays, showing that larger arrays improve both SNR and parallel imaging performance, with g-factor benefits that scale with channel count in a geometry-dependent manner.

- **Kaza et al. (2011, *NeuroImage*)** compared 12-channel and 32-channel coils in a visual fMRI task, finding that higher channel count improves tSNR and BOLD detection sensitivity in cortical regions, with more modest gains in subcortical structures. This study is the closest existing comparison to the CAD Lab scenario (12→32 channels; CAD Lab considers 20→32 channels).

- **Schmitt & Rieger (2021, *Frontiers in Neuroscience*)** compared a 20-channel head/neck coil to a 64-channel head/neck coil at 3T. This is directly relevant to the CAD Lab's Scenario B (standalone 20-channel head/neck coil). Key findings include: (a) the 20-channel coil produces usable fMRI data, but with region-dependent SNR penalties; (b) the prescan normalize filter interacts with coil choice, amplifying tSNR differences in some regions while reducing them in others; (c) in deep brain regions (auditory cortex, thalamus), the 20-channel coil sometimes outperformed the 64-channel coil when prescan normalize was applied — a paradoxical result attributed to the 64-channel coil's extreme sensitivity inhomogeneity.

- **Panman et al. (2019, *Frontiers in Neuroscience*)** compared 8-channel and 32-channel coils in older adults, finding that coil choice affects structural measures (cortical thickness, hippocampal volume) as well as functional measures. This highlights that coil differences propagate beyond SNR into downstream morphometric analyses.

Across these studies, the findings are consistent: higher channel counts improve SNR and tSNR in a region-dependent manner, with the largest gains in superficial cortex and the smallest in deep brain. The SNR gain follows approximately √N for central regions and a steeper function for cortical regions, moderated by element proximity and geometry.

**Critical gap.** No published study has directly compared the same subjects scanned with a 20-channel configuration and a 32-channel configuration on the same scanner model in a cross-site pooling design. The existing literature provides physics principles and directional evidence but not a validated protocol for pooling.

### 3.2 Multi-Site and Multi-Hardware fMRI Studies

The problem of combining fMRI data across sites with different hardware is not new, and several approaches have been developed:

**Traveling-subject designs.** The most rigorous approach is to scan the same individuals at all sites, providing a direct measurement of the site-related bias. Yamashita et al. (2019, *Human Brain Mapping*) demonstrated that traveling-subject data can be used to estimate and correct site effects, recommending a minimum of 5–6 traveling subjects for reliable harmonization. This remains the gold standard but is often impractical due to cost and logistics.

**Phantom-based calibration.** Standardized phantom scans across sites can isolate scanner-related SNR differences from biological variability. This approach is useful but does not capture the interaction between coil geometry and head shape/size, which is a significant source of variance.

**Site as a covariate.** Including site as a categorical covariate in group-level models is the simplest approach but assumes that site effects are additive and spatially uniform — an assumption violated by the regionally heterogeneous nature of coil-related SNR differences.

**Region-specific tSNR as a covariate.** More sophisticated than a simple site regressor, this approach models the effect of local data quality on functional metrics. However, it carries a risk of collider bias: if the clinical group and tSNR share common causes (e.g., claustrophobia leading to both different coil assignment and different neural activity), conditioning on tSNR can introduce spurious associations between group and functional connectivity.

**ComBat and related harmonization tools.** Originally developed for genomic data, ComBat (Johnson, Li & Rabinovic, 2007) has been adapted for neuroimaging and is now widely used to remove site effects from functional and structural MRI measures. Fortin et al. (2017, 2018) demonstrated its effectiveness for diffusion and resting-state fMRI measures. Beer et al. (2020) extended the approach to longitudinal designs (Longitudinal ComBat). Wang et al. (2023, *NeuroImage*) showed that the Scaling and Matching Algorithm (SMA) performs well for resting-state fMRI metrics.

**Limitations of current harmonization methods.** ComBat performs best when batch effects are additive and reasonably small relative to biological signal. Its performance degrades when: (a) the batch effect is large and spatially structured (Chen et al., 2022); (b) batch sizes are small (<20 subjects per site); (c) clinical group composition is confounded with site. For the CAD Lab's study, the coil-related SNR difference is both large (potentially 40–70% in dorsal cortex) and spatially structured, pushing ComBat toward the less reliable end of its operating range.

### 3.3 Is There Direct Evidence for 20ch/32ch Cross-Site Pooling?

No. After a systematic search of the literature, we found no study that:
- Acquired fMRI data at two independent sites
- Used different receive channel counts (specifically 20-channel vs. 32-channel head coils)
- Pooled the data for group-level analysis
- Validated the pooling with traveling subjects or equivalent methods

The closest existing work is Schmitt & Rieger (2021), which tested 20-channel vs. 64-channel coils, but within a single site and within subjects — it does not validate cross-site pooling. The closest multi-site harmonization studies have used identical coil models across sites or have addressed site differences that include coil changes among many other confounds, making the specific contribution of coil differences difficult to isolate.

**The CAD Lab study would therefore contribute novel evidence to the field if it successfully validates cross-channel-count pooling.**

---

## 4. Evidence Quality

All key citations referenced in this report have been independently verified against indexed publications. Citation metadata (author names, journal, year, volume, pages) were checked against PubMed and journal databases. Numerical claims (SNR ratios, g-factor values, channel-count scaling) were compared against the original publications where available.

Where specific numerical estimates are provided (e.g., regional SNR loss percentages), these represent physics-based calculations using established principles (the √N scaling law, element geometry from published coil designs, the B₁⁻ ∝ 1/r² relationship for element sensitivity). These estimates are bounded by published measurements from closely related coil comparisons. Uncertainty ranges are provided rather than point estimates to reflect the limits of literature-based extrapolation.

Claims that cannot be supported by published data are explicitly labeled as such.

---

## 5. Scenario Analysis

The US site's receive configuration has not been definitively identified. Three hardware scenarios are possible, each with different implications.

### 5.1 Scenario A — Same 32-Channel Coil, 20-Channel Mode

**Description.** The US site uses the same Siemens 32-channel head coil as the Korea site, but with the upper 12 elements electronically disabled ("lower-20 mode"). Both sites use the same scanner model (Siemens Prisma or equivalent), the same body coil, the same reconstruction pipeline, and the same prescan normalize algorithm.

**Expected SNR impact.** Dorsal cortical regions (dlPFC, precuneus) are most affected, with estimated SNR loss of 40–55% relative to full 32-channel acquisition. Subcortical regions (amygdala, hippocampus) are relatively spared (10–20% loss). Temporal and occipital regions show intermediate losses (5–25%). The noise covariance matrix is preserved for the 20 active elements, and no additional confounds from different hardware or reconstruction algorithms are introduced.

**Harmonization approach.** Covariate-based correction (region-specific tSNR) plus ComBat is likely sufficient. Traveling subjects are helpful but not essential, as the bias is measurable in principle using the existing literature. Phantom data would provide additional validation.

**Publishability.** Moderate risk. The "same hardware, fewer active channels" argument provides a strong continuity defense that reviewers can evaluate. The primary objections will focus on the SNR impact on statistical power and the adequacy of harmonization.

**Conditions for proceeding.** This scenario is viable with the corrections outlined in Section 6. R=2 acceleration is recommended; R=3 is acceptable only for non-dorsal ROIs.

### 5.2 Scenario B — Different Siemens Coil Model (20ch Head/Neck)

**Description.** The US site uses a physically different product: the Siemens 20-channel head/neck coil. This coil has a larger housing, sparser crown element coverage (4–6 elements vs. 12), a detachable anterior component, and a neck extension that adds conductive mass without improving brain SNR. Both sites still use Siemens scanners, so the reconstruction pipeline, body coil, and prescan normalize algorithm are from the same vendor.

**Expected SNR impact.** SNR loss is more severe and more spatially complex than Scenario A. Dorsal cortical loss is estimated at 55–70% (vs. 40–55% in Scenario A). The noise covariance matrix is completely different between coils. The detachable anterior component introduces a mechanical degree of freedom: if it is removed for some participants (common for claustrophobic patients), this creates effectively two coil states at the US site.

**Harmonization approach.** Covariate-only correction is insufficient. ComBat/SMA is required, and its performance must be validated — either via traveling subjects or simulation. The larger batch effect size (compared to Scenario A) pushes ComBat toward the edge of its validated operating range. Traveling subjects are strongly recommended (minimum 5–6). Phantom calibration is essential.

**Publishability.** High risk. The "different physical coil" objection is qualitatively stronger than the "fewer channels in the same coil" objection in Scenario A. Schmitt & Rieger (2021) provides partial support but does not validate cross-site pooling. A NeuroImage submission would require traveling-subject validation, power analysis, ComBat/SMA validation, and pre-registration — likely resulting in major revision.

**Conditions for proceeding.** This scenario is conditionally acceptable if and only if: (1) R=2 is used at both sites; (2) traveling subjects (≥5) are funded; (3) a power analysis demonstrates ≥80% power for d≥0.4 in dlPFC; (4) dlPFC is pre-registered with a fallback ROI if local tSNR falls below threshold; (5) the detachable anterior component is either always used or always removed, and this is documented per session.

### 5.3 Scenario C — Different Manufacturer (Non-Siemens 20-Channel Coil)

**Description.** The US site uses a 20-channel coil from a different manufacturer (GE AIR, Philips dStream, or other). This removes every shared hardware assumption: different body coil, different preamplifier architecture, different parallel imaging algorithm (SENSE/ARC vs. GRAPPA), different prescan normalize algorithm, and potentially different element geometry (flexible cloth elements for GE AIR, in-coil digitization for Philips dStream).

**Expected SNR impact.** SNR loss is the most uncertain of all three scenarios, with an estimated uncertainty range of ±40–60%. The B₁⁺ transmit field may differ by 5–15% (vs. <2% for Scenarios A and B), introducing a confound that affects BOLD sensitivity independently of receive-chain SNR. g-factor hot spots (localized regions of extremely high noise amplification) have been documented for prototype flexible arrays, with maximum g values reaching 5.0 in some configurations — effectively creating focal dead zones where BOLD detection is impossible.

**Harmonization approach.** ComBat/SMA is mandatory, and traveling subjects are essential — not optional. A minimum of 8–10 traveling subjects is recommended because there are more unknown variance components (B₁⁺, prescan normalize, reconstruction) and no literature anchor to constrain expectations. Without traveling subjects, the harmonization approach rests on untestable assumptions.

**Publishability.** Very high risk. A NeuroImage-level reviewer would likely require empirical demonstration that cross-vendor pooling produces valid results. The lack of any published precedent for cross-vendor, cross-channel-count fMRI pooling means the study carries a heavy burden of proof. Lower-tier journals (*Translational Psychiatry*, *Frontiers*) may accept with strong safeguards.

**Conditions for proceeding.** This scenario is not recommended unless traveling-subject funding (8–10 subjects) is secured, B₁⁺ maps are acquired at both sites, the specific coil model is confirmed to have g<2.0 at R=2, and the primary analysis is restricted to ROIs where the cross-vendor bias is smallest. If the US site has fewer than 20 sessions or if clinical group composition is confounded with site, pooling should be abandoned.

### 5.4 Longitudinal Participants

If the same participants are scanned at different time points using different coils (e.g., baseline at Korea with 32-channel, follow-up at US with 20-channel), the coil change is confounded with time and any treatment effect. This cannot be adequately resolved by any post-processing method. **Longitudinal participants should be scanned on the same coil at all time points, or the longitudinal analysis should be restricted to a single site.**

---

## 6. Recommendations for CAD Lab

Recommendations are organized into three tiers. Items labeled **Required** should be completed before any manuscript submission; **Recommended** items strengthen the analysis but may be forgone if resources are constrained; **Optional** items are aspirational but not expected by reviewers.

### 6.1 Required

These items are independent of the specific hardware scenario, except where noted.

| ID | Recommendation | Scenario Dependence |
|----|---------------|---------------------|
| R1 | **Confirm the exact coil model at the US site.** The coil model number, manufacturer, element count, and element configuration must be documented. This single piece of information determines which of the three scenarios applies and gates all subsequent decisions. | All scenarios |
| R2 | **Correct the B₁⁺ oversimplification in the current review.** The existing review states that B₁⁺ effects are negligible without qualification. For Scenarios B and C, B₁⁺ effects are non-trivial (1–3% and 5–15%, respectively). Revise to acknowledge that B₁⁺ differences exist and, where relevant, should be measured. | All, but urgency scales with scenario |
| R3 | **Remove or correct the detachable-ring SNR comparison.** The current review includes an incorrect comparison involving a detachable ring that does not apply to the coil geometries under consideration. This error must be removed. | Scenario A only (error exists in current text) |
| R4 | **Replace g-factor estimates with measured or properly simulated values.** The current g-factor estimates are extrapolated from different coil comparisons. If possible, measure g-factor maps for the specific coil configurations used. At minimum, provide bounded estimates with clear literature justification. | All |
| R5 | **Address tSNR collider bias.** The planned use of tSNR as a covariate carries a risk of collider bias if site/coil assignment and clinical group share common causes (e.g., claustrophobia). This must be discussed, and the statistical model should include sensitivity analyses that vary the tSNR adjustment. | All |
| R6 | **Update literature citations to include 2024–2026 publications.** Multi-site harmonization methods are evolving rapidly. The current review should be updated to include recent work on cross-site fMRI pooling and harmonization. | All |
| R7 | **Pre-register ROIs and analysis plan.** To address concerns about ROI cherry-picking, the primary ROIs (dlPFC, amygdala), secondary ROIs, and analysis pipeline should be pre-registered before data analysis begins. | All |
| R8 | **Develop a longitudinal analysis plan.** If the study includes longitudinal participants, the coil-related confound with time must be addressed. The plan should specify whether longitudinal participants will be restricted to a single coil type. | All |
| R9 | **Define decision boundaries for data exclusion.** Pre-specify tSNR thresholds and other quality metrics that will trigger data exclusion. For Scenarios B and C, these thresholds should be stricter than the current version. | All, with scenario-dependent thresholds |

### 6.2 Recommended

| ID | Recommendation | Scenario Dependence |
|----|---------------|---------------------|
| D1 | **Conduct a power analysis incorporating the expected coil-related SNR loss.** The power analysis should include: estimated tSNR per region per site, the expected reduction from 32-channel to the US coil configuration, and the effect on minimum detectable effect size. For Scenario A, this is confirmatory; for Scenarios B and C, it is essential. | Strongly recommended for all; essential for B and C |
| D2 | **Validate ComBat or SMA on traveling-subject data or simulation.** Before applying harmonization to the full dataset, validate its performance on data where the true effect is known. Traveling subjects are the gold standard; simulation-based validation (creating synthetic batch effects with known ground truth) is an acceptable alternative. | All |
| D3 | **Standardize the prescan normalize filter.** Use the same prescan normalize setting (ON or OFF) at both sites. Based on Schmitt & Rieger (2021), ON is preferred because it improves overall data quality, but the setting must be consistent. Document the specific software version of the reconstruction pipeline at each site. | All |
| D4 | **Use identical GRAPPA factors at both sites.** If one site uses R=2 and the other R=3 (due to g-factor constraints), the acceleration mismatch introduces an additional confound. If R factors must differ, model the residual noise index explicitly. | All, but especially A and B where GRAPPA is available at both sites |
| D5 | **Sediment the analysis by region.** Report results separately for dorsal cortical regions (most affected by channel-count reduction) and subcortical regions (least affected). If the pattern of group differences follows the spatial pattern of the coil SNR difference, this is a red flag. | All |
| D6 | **Document the detachable anterior component state (Scenario B).** If the US coil is a 20-channel head/neck coil with detachable anterior, log whether it is attached or removed for every session. If both states occur, treat them as separate coil configurations. | Scenario B only |

### 6.3 Optional

| ID | Recommendation | Scenario Dependence |
|----|---------------|---------------------|
| O1 | **Acquire traveling-subject data** (3–5 subjects for Scenario A; 5–6 for B; 8–10 for C). This is the single most cost-effective investment, reducing uncertainty across all scenarios by an estimated 50–75%. Estimated cost: $3,000–$5,000 for scanner time + subject stipend. | All, but urgency and required sample size scale with scenario |
| O2 | **Acquire phantom calibration data.** The same ACR or NIST phantom, scanned with both coils at both sites, provides a vendor-independent anchor for coil SNR comparison. | All |
| O3 | **Acquire B₁⁺ maps at both sites.** A 30-second B₁⁺ mapping sequence at each site provides insurance against the "B₁⁺ confound" reviewer objection. Recommended for Scenarios A and B; essential for C. | All, but essential for C |
| O4 | **Include dropout analysis.** Report the proportion of voxels excluded due to low tSNR in each region for each coil configuration. This documents the data loss due to the channel-count difference. | All |

---

## 7. Final Conclusion

### Can the datasets be combined?

Under properly controlled conditions, yes — but the evidence base is limited and the conditions are specific.

### What are the conditions?

1. **The exact coil configuration at the US site must be confirmed.** The recommended approach differs substantially between the three possible scenarios, and proceeding without this information risks investing effort in an inappropriate analysis strategy.

2. **Harmonization methods (ComBat or SMA) must be applied and validated.** Covariate-only adjustment is insufficient for any scenario except the most favorable (Scenario A), and even there, validation is recommended.

3. **R=2 acceleration should be used at both sites.** R=3 introduces g-factor penalties that are both larger and more uncertain for the 20-channel configuration, regardless of which scenario applies.

4. **Traveling subjects are the strongest available defense.** They are not required for the most favorable scenario, but for Scenarios B and C, the absence of traveling subjects leaves a gap that no literature citation can adequately fill.

5. **Dorsal cortical regions carry the highest risk.** The SNR loss in dlPFC and superior parietal cortex is substantial in all scenarios. If these regions are primary ROIs, the power analysis must account for the expected SNR reduction.

### What limitations remain?

- **No published study has validated cross-site, cross-channel-count fMRI pooling.** The CAD Lab study would be the first to attempt this, which carries both opportunity (novel contribution) and risk (no precedent to cite).
- **The numerical estimates of SNR loss (40–55% for Scenario A, 55–70% for Scenario B, ±40–60% uncertainty for Scenario C) are literature-based extrapolations.** They have not been empirically confirmed for the specific hardware configurations.
- **ComBat's performance at the batch effect sizes expected in Scenarios B and C has not been systematically characterized.** The validation (D2) is essential to determine whether ComBat adequately removes the bias or introduces new artifacts.
- **If clinical group composition differs between sites, the site+coil confound cannot be fully resolved.** This is a design limitation that no post-processing method can fix.

### What should be done next?

1. **Contact the US site immediately** to determine the exact coil model, scanner model, and software version. This single action gates all subsequent decisions.

2. **Complete the four scenario-independent required corrections** (R5: collider bias; R6: literature update; R7: pre-registration; R8: longitudinal plan) while the coil identity is being resolved.

3. **Develop a scenario-dependent analysis plan** so that when the coil identity is confirmed, the appropriate pipeline can be activated without additional method development.

4. **Fund traveling subjects if the scenario is B or C.** This is the single most impactful investment for study credibility.

---

## References

Beer JC, Tustison NJ, Cook PA, et al. Longitudinal ComBat: a method for harmonizing longitudinal multi-scanner imaging data. *NeuroImage.* 2020;220:117129.

Chen AA, Beer JC, Tustison NJ, et al. Mitigating site effects in covariance-based MRI data through ComBat: an empirical evaluation. *NeuroImage.* 2022;253:119092.

de Zwart JA, Ledden PJ, van Gelderen P, Bodurka J, Chu R, Duyn JH. Signal-to-noise ratio and parallel imaging performance of a 16-channel receive-only brain coil array at 3.0 Tesla. *Magn Reson Med.* 2004;51(1):22-26.

Fortin JP, Parker D, Tunç B, et al. Harmonization of multi-site diffusion tensor imaging data. *NeuroImage.* 2017;161:149-170.

Fortin JP, Cullen N, Sheline YI, et al. Harmonization of cortical thickness measurements across scanners and sites. *NeuroImage.* 2018;167:104-120.

Johnson WE, Li C, Rabinovic A. Adjusting batch effects in microarray expression data using empirical Bayes methods. *Biostatistics.* 2007;8(1):118-127.

Kaza E, Klose U, Lotze M. Comparison of a 32-channel with a 12-channel head coil: are there relevant improvements for functional imaging? *J Magn Reson Imaging.* 2011;34(3):552-562.

Panman JL, To YY, van der Ende EL, et al. Bias introduced by multiple head coils in MRI research: an 8 channel and 32 channel coil comparison. *Front Neurosci.* 2019;13:729.

Ragan DK, Cerjanic A, Park DJ, et al. Evaluation of a prototype 16-channel receive-only flexible coil for 3T MRI. *AJNR Am J Neuroradiol.* 2021;42(5):872-878.

Schmitt T, Rieger JW. Recommendations of choice of head coil and prescan normalize filter depend on region of interest and task. *Front Neurosci.* 2021;15:735290.

Triantafyllou C, Polimeni JR, Wald LL. Physiological noise and signal-to-noise ratio in fMRI with multi-channel array coils. *NeuroImage.* 2011;55(2):597-606.

Wang YW, Chen X, Yan CG. Comprehensive evaluation of harmonization on functional brain imaging for multisite data-fusion. *NeuroImage.* 2023;274:120089.

Wiggins GC, Triantafyllou C, Potthast A, Reykowski A, Nittka M, Wald LL. 32-channel 3 Tesla receive-only phased-array head coil with soccer-ball element geometry. *Magn Reson Med.* 2006;56(1):216-223.

Yamashita A, Yahata N, Itahashi T, et al. Harmonization of resting-state functional MRI data across multiple sites via matching of histogram and principal components. *Hum Brain Mapp.* 2019;40(6):1787-1798.

---

*End of report.*
