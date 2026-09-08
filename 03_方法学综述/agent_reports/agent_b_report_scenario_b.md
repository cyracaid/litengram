# Agent B Report — Scenario (b): Standalone Siemens 20ch Head/Neck Coil

**Role:** MRI Physicist + fMRI Methodologist
**Date:** 2026-07-20
**Status:** Complete — awaiting Agents A and C for cross-verification

---

## 1. Physics Analysis

### 1.1 Coil Architecture: 20ch Head/Neck vs 32ch Head Coil

**The two coils are fundamentally different physical products.** This is not a scenario (a) partial-array situation. The differences span every level of the receive chain:

| Property | Siemens 32ch Head Coil | Siemens 20ch Head/Neck Coil | Physics Impact |
|----------|----------------------|---------------------------|----------------|
| Element geometry | Soccer-ball (hexagonal/pentagonal tiling), 32 overlapping ~75mm circular elements | Anterior-posterior paired arrangement, ~14-16 head elements + 4-6 neck elements, ~85-100mm diameters | Different sensitivity profiles; 20ch elements are larger, fewer, and positioned differently |
| Crown/dome coverage | 12 densely packed elements covering vertex to ~z=+40 | ~4-6 larger elements in the dome region; gaps may exist between elements | **Major** — dorsal/vertex sensitivity is qualitatively different, not just reduced |
| Temporal coverage | 12-element lower ring (temporal-cerebellar), close-fitting | ~6-8 temporal elements; housing is larger (accommodates neck extension) | Moderate temporal SNR loss (10-20%) vs scenario (a) negligible |
| Neck extension | None — coil ends at foramen magnum | 4-6 elements extend to C3-C4; housing flares outward at the base | Neck elements do **not** improve brain SNR; housing geometry changes loading |
| Detachable anterior | No — monolithic helmet | Yes — anterior head/neck portion can be unclipped | **Critical:** Anterior element position varies if the anterior portion is detached; SNR changes in OFC, temporal poles |
| Preamplifier decoupling | Optimized for 32-element mutual inductance matrix | Optimized for independent 20-element matrix with different overlap | Noise covariance matrix Ψ is **completely different** between coils |
| Housing diameter | Tight-fitting (~25 cm inner diameter) | Larger (~28-30 cm at the neck) | **SNR penalty from distance:** B₁⁻ ∝ 1/r²; larger housing → ~15-30% reduced sensitivity at the same brain location |
| Element-to-brain distance (crown) | ~5-15 mm | ~15-30 mm (larger housing + gap between elements) | **Major:** Vertex SNR₀ reduction from distance alone is ~50-70% |

**Key conclusion — why this is NOT scenario (a):** In scenario (a), the lower-20 elements are *identical* hardware operating in their designed electromagnetic environment. The only variable is which elements are turned on. In scenario (b), **every element is physically different**, positioned differently, and coupled to a different decoupling/preamp network. The sensitivity matrix S and noise covariance Ψ share **no common basis** between coils.

### 1.2 SNR₀ Loss — Regional Breakdown

Estimates assume 3T, 2.5 mm isotropic EPI, GRAPPA R=2. Scenario (a) values from the literature review are shown for comparison.

| Region | Scenario (a) SNR₀ Loss (lower-20 mode) | Scenario (b) SNR₀ Loss (20ch H/N) | Difference & Mechanism |
|--------|:---:|:---:|-------|
| **dlPFC (BA 9/46), z=+25 to +55** | 40-55% | **55-70%** | **Worse.** 20ch H/N has fewer crown elements, larger housing, greater element-brain distance. |
| **Vertex / superior parietal (BA 5/7)** | 50-65% | **60-75%** | **Worst-case region.** Almost no dedicated crown elements; the 4-6 dome elements are >20 mm from brain surface. |
| **VMPFC / ACC, z=-10 to +35** | 25-40% | **35-50%** | **Worse.** Anterior elements of 20ch H/N are part of detachable structure; position variability. |
| **OFC (BA 11/47), z=-20 to 0** | <10% | **15-30%** | **Worse.** Detachable anterior component may not achieve the same close fit as the fixed 32ch; the 20ch H/N has fewer dedicated OFC elements. |
| **Hippocampus, z=-30 to -10** | 10-20% | **15-25%** | Similar. Both coils have adequate inferior coverage, but the 20ch H/N elements are farther from the medial temporal lobe. |
| **Amygdala** | <10% | **10-20%** | Moderate difference. Amygdala is deep and benefits less from the 20ch H/N's inferior extension. |
| **Temporal cortex** | <5% | **10-20%** | **Worse.** The 20ch H/N temporal elements are fewer and larger; close fit is less reliable. |
| **Cerebellum** | <5% | **5-15%** | The 20ch H/N's neck elements are positioned inferior to the cerebellum but at greater distance. |
| **Thalamus** | 15-25% | **20-35%** | **Worse.** Deep structure; reduced element count AND greater element distance compound. |
| **Occipital (superior), z=+30 to +70** | 50-65% | **60-80%** | **Critical.** Nearly all occipital crown sensitivity is lost in the 20ch H/N. |

### 1.3 SNR₀ Loss — Quantified Physics

The SNR₀ ratio between coils at a location r is:

$$ \frac{\text{SNR}_{20ch}(r)}{\text{SNR}_{32ch}(r)} = \sqrt{\frac{20}{32}} \cdot \frac{B^-_{1,20ch}(r)}{B^-_{1,32ch}(r)} \cdot \sqrt{\frac{R_{\text{total},32ch}}{R_{\text{total},20ch}}} $$

The first factor ($\sqrt{20/32} \approx 0.79$) is a 21% reduction from channel count alone. The second factor (receive sensitivity ratio) is region-dependent and includes the $\sim 1/r^2$ distance penalty. The third factor (noise resistance ratio) depends on each coil's loading and geometry.

For the **dorsal cortex**, the dominant term is $B^-_1$: the 20ch H/N's larger housing and sparser crown elements reduce sensitivity by an additional factor of $\sim 0.4-0.5$, giving a combined SNR₀ ratio of $0.79 \times 0.45 = 0.36$ — i.e., **~36% of 32ch SNR₀**, or **~64% loss** relative to 32ch. This is approximately 15-20 percentage points worse than scenario (a).

### 1.4 g-Factor / GRAPPA Implications

The g-factor for parallel imaging depends on the coil sensitivity matrix S **and** its conditioning. The 20ch H/N has:

- **Fewer elements** → reduced spatial encoding degrees of freedom → higher g
- **Different geometry** → the coil's encoding functions occupy a different subspace of the spatial-frequency domain
- **No relationship** between the 20ch and 32ch sensitivity matrices → g-factor maps cannot be predicted from 32ch data

| Acceleration | 32ch Head Coil | 20ch H/N Coil | 20ch lower-20 mode (Sc. a) |
|:---:|:---:|:---:|:---:|
| **R=2 axial** | g < 1.05 | g < 1.15 | g < 1.10 |
| **R=3 axial** | g = 1.05-1.15 | **g = 1.25-1.80** (dorsal worse) | g = 1.15-1.50 (dorsal) |
| **R=4 axial** | g = 1.15-1.40 | g > 2.0 (most regions) | g = 1.50-2.20 (dorsal) |
| **Slice accel 2** | g < 1.10 | g = 1.15-1.35 | g = 1.10-1.25 |

**Key difference from scenario (a):** In scenario (a), the lower-20 elements retained the optimal decoupling/overlap designed for the full 32-element array, but with a boundary at the transition between active and inactive elements that creates a zone of increased mutual inductance. In scenario (b), the 20ch H/N has **self-consistent** decoupling (no boundary artifact), but its elements are **intrinsically larger and sparser**, providing worse spatial encoding per element. The g-factor penalty in the **superior brain at R≥3 is severe** — potentially worse than scenario (a) due to the distance from crown elements.

**Recommendation:** For 20ch H/N sessions, **use R=2 maximum**. R=3 is only acceptable if dorsal cortex is excluded from analysis. Document GRAPPA factor per session.

### 1.5 Noise Correlation — Complete Redesign

The noise covariance matrix Ψ is determined by:

1. **Element geometry** (overlap → mutual inductance → correlated noise)
2. **Preamplifier decoupling** (each preamp has a specific input impedance that affects noise matching)
3. **Sample loading** (the 20ch H/N loads differently — it contacts the neck and shoulders differently than the 32ch)

Because the 20ch H/N has:
- Different element positions → different mutual inductances
- Different preamplifier design → different noise figure and correlation
- Different housing → different sample loading and coil losses

**Ψ_20ch is not even approximately proportional to Ψ_32ch.** This means:
- The effective number of independent noise degrees of freedom differs
- Coil combination weights (adaptive vs fixed) will produce different effective sensitivity profiles
- Prescan normalize (which uses coil sensitivity estimates) will produce different spatial intensity normalization
- **Prewhitening approaches must be coil-specific**

### 1.6 B₁⁺ Effects — Slightly Larger in Scenario (b)

At 3T, the body coil transmits; receive arrays are receive-only. However:

- **Housing loading:** The 20ch H/N housing extends onto the shoulders and neck. This places more conductive structure in the transmit field, which can perturb B₁⁺ via induced currents in cable traps and the housing itself. Estimated effect: **1-3% flip-angle variation**, concentrated in the lower brainstem/cerebellum.
- **Cable routing:** The 20ch H/N has different cable routing; cable trap placement differs. This can create asymmetric B₁⁺ perturbation.
- **Vertex B₁⁺:** The 20ch H/N has a more open vertex (larger gap between crown elements), which may slightly reduce B₁⁺ at the vertex due to reduced conductive structure. This is a **small effect** (<2%).

**Net assessment:** The B₁⁺ difference between coils is **small** (1-3%) and unlikely to materially affect BOLD contrast. This is consistent with the standard conclusion that body-coil transmit at 3T dominates. **However**, if quantitative B₁⁺ maps are used in preprocessing (e.g., for BOLD calibration), the small difference should be characterized, not assumed zero.

### 1.7 Prescan Normalize Interaction

Schmitt & Rieger 2021 provides **directly relevant** data for this scenario — they used the Siemens 20ch head/neck coil vs the 64ch head/neck. Their key findings for our case:

1. **Prescan normalize interacts region-dependently with coil choice.** The filter amplifies tSNR differences in visual and motor cortex but reduces them in thalamus and auditory cortex.

2. For our 20ch H/N vs 32ch head coil comparison (where the coil difference is **smaller** than Schmitt's 20ch vs 64ch), the interaction is expected to be similar in **direction** but **attenuated in magnitude**.

3. **Critical protocol rule:** Prescan normalize must be set identically (ON or OFF) at both sites. Toggling it would create a coil × filter interaction that cannot be easily disentangled. **ON is preferred** because it improves overall data quality for both coils (Schmitt 2021, MRIQC results).

4. **Schmitt's paradoxical finding** (20ch sometimes outperforming 64ch in deep brain with prescan normalize ON) may partially carry over: the 32ch head coil has more element density, which creates more local receive-field inhomogeneities that prescan normalize can over-correct. The 20ch H/N, with its sparser element distribution, may produce a more spatially uniform receive field at depth, and prescan normalize may handle it more favorably in subcortical regions.

---

## 2. Harmonization & Statistical Analysis

### 2.1 Scenario Classification

**This is definitively Scenario B: different sites + different scanners + different coils.**

Scenario (a)'s argument — "the elements are identical hardware" — does **not** apply. This is a different coil model with no hardware commonality. Therefore:

| Aspect | This Scenario | Scenario (a) Equivalent |
|--------|--------------|------------------------|
| Coil relationship | Different physical product | Same coil, different element selection |
| Noise covariance | Ψ completely different | Ψ similar (subset preserved) |
| Sensitivity matrix | S completely different | S partially preserved (lower elements) |
| Harm. approach | Full multi-site harmonization | SNR-difference modeling |
| Traveling subjects | **Essential** | Helpful but not essential |
| "Same hardware" argument | Unavailable | Available |

### 2.2 Is Harmonization More Difficult Than Scenario (a)?

**Yes — substantially more difficult.** Five reasons:

1. **No common sensitivity basis.** In scenario (a), the remaining 20 elements have identical sensitivity profiles. In scenario (b), every element is different. The spatial SNR distribution is unpredictably different.

2. **Coil × sample interaction differs.** The 20ch H/N loads differently for different head/neck sizes. The SNR penalty for a large-necked participant may be different from a small-necked one. This introduces a participant×coil interaction that scenario (a) does not have.

3. **No continuity argument for reviewers.** In scenario (a), one can argue that the elements are the same physical hardware. In scenario (b), no such continuity exists. A reviewer will correctly identify this as a between-coil comparison.

4. **Detachable anterior component introduces position variability.** If the US site sometimes uses the 20ch H/N with and sometimes without the anterior portion, there are effectively **two coil states** at the US site. This is a within-site, within-coil heterogeneity that scenario (a) does not face.

5. **Harmonization methods must work at a larger effect size.** The physical bias between coils is larger than scenario (a). ComBat/SMA performance degrades as batch effect size increases relative to biological signal (Fortin 2018; Wang 2023). Simulation validation (MF8 from the integration report) is particularly important here.

### 2.3 Specific Harmonization Requirements

| Tool | Required? | Notes |
|------|-----------|-------|
| **Prevention** (matched protocol) | **Yes** | Same TR/TE/resolution/GRAPPA/prescan normalize. Prevention is strongest. |
| **Site/coil as covariate** | **Yes** (floor only) | Captures global shifts but insufficient for spatially non-uniform bias |
| **Region-specific tSNR covariate** | **Yes** | Better than global covariate but **watch for collider bias** (MF4) |
| **ComBat on FC/ALFF/ReHo** | **Yes** | Mean-only variant preferred; validate with simulation (MF8) |
| **SMA (Wang 2023)** | **Yes** | Best for rs-fMRI metrics; validate on effect size of this scenario |
| **Traveling subjects (≥5-6)** | **Strongly recommended** | The only way to directly measure the site+coil bias. Essential for NeuroImage-level defense (R2-SA2, Yamashita 2019). |
| **Longitudinal ComBat** | **If mixed-coil per subject** | Beer 2020; needed if individual subjects are scanned on both coils |
| **Phantom calibration** | **Yes** | Useful for isolating coil SNR from site/system effects. Same phantom scanned at both sites with both coils. |

**Homogenization of GRAPPA is particularly critical.** If the US site uses a different GRAPPA factor (e.g., R=3 on the 32ch at Korea, R=2 on the 20ch at US due to g-factor constraints), the acceleration mismatch introduces a separate, additive confound that interacts with the coil difference. **If GRAPPA must differ, this must be explicitly modeled** (e.g., as a separate nuisance dimension or by matching RNI = residual noise index).

### 2.4 Power and Sensitivity Implications

The larger SNR₀ loss in scenario (b) compared to scenario (a) has direct statistical consequences:

| Metric | Scenario (a) | Scenario (b) |
|--------|:---:|:---:|
| Dorsal tSNR reduction (20ch vs 32ch) | ~50-65% of 32ch | ~35-55% of 32ch |
| Subcortical tSNR reduction | ~80-95% of 32ch | ~65-85% of 32ch |
| Statistical power loss (dorsal, d=0.3, n=80/group, 30% 20ch) | ~5-10% | ~15-25% |
| ComBat false-positive rate at this batch effect size | ~3-5% (estimated) | ~5-10% (estimated; needs simulation) |
| Minimum detectable effect (dorsal, 80% power) | d ≈ 0.35-0.40 | **d ≈ 0.45-0.55** |

The power loss in scenario (b) is **meaningfully larger**. If 30% of sessions are from the 20ch H/N, the study's effective n for dorsal analyses is reduced by the equivalent of ~15-25 participants compared to a single-coil design.

---

## 3. Publishability Assessment

### 3.1 Risk Level for NeuroImage Submission

**Higher risk than scenario (a).** The integration report gave an overall 6.5/10 for the revised review (which describes scenario (b) as one of three cases). For scenario (b) specifically:

| Domain | Risk Level | Rationale |
|--------|:----------:|-----------|
| Reviewer physics objection | **High** | "You compared two fundamentally different receive arrays" — this is harder to defend than scenario (a)'s "same coil, fewer elements" |
| Existing literature support | **Moderate** | Schmitt 2021 is directly relevant but tested vs 64ch, not 32ch. Gap remains. |
| Harmonization defense | **Moderate** | Multi-site harmonization is standard practice; but the coil difference adds a novel dimension |
| Clinical confound concern | **High** | If coil choice correlates with anxiety/claustrophobia, the confound with clinical group is stronger than scenario (a) |
| Overall to NeuroImage | **Major Revision likely** | Would need: traveling subjects + ComBat/SMA validation + power analysis + pre-registration |

### 3.2 How Schmitt & Rieger 2021 Helps and Hurts

**Helps:**
- Directly tests the 20ch H/N coil (same physical model)
- Shows the coil produces usable fMRI data
- Demonstrates prescan normalize can partially compensate for channel-count differences
- Provides a citation for the region-dependent interaction

**Hurts:**
- Schmitt compared to **64ch**, not 32ch. A reviewer may say: "Your 32ch vs 20ch difference is 12 fewer channels; the difference Schmitt tested was 44 fewer channels. Your effect is proportionally smaller but same direction — yet Schmitt still found region-specific effects. These effects will not disappear simply because your channel-count gap is smaller."
- Schmitt's paradoxical finding (20ch outperforming 64ch in deep brain) was for **auditory cortex and thalamus** — not the amygdala, hippocampus, or PFC that CAD Lab targets
- None of Schmitt's tasks probed emotional processing or executive function (the domains most relevant to anxiety/depression)
- Schmitt's study was single-site, within-subject — it does **not** validate cross-site pooling

### 3.3 Anticipated Reviewer Criticisms Specific to Scenario (b)

1. **"You are comparing fMRI data acquired with two completely different receive arrays. Any observed group differences could reflect hardware differences in coil geometry, element sensitivity, and noise structure — not just channel count. The Schmitt 2021 paper does not rescue this because it was a within-subject comparison, not a cross-site pooling study."**

2. **"The Siemens 20-channel head/neck coil has a detachable anterior component. Was this removed for any participants? If so, you have effectively three coil configurations (20ch + anterior, 20ch - anterior, 32ch), not two."**

3. **"Your SNR₀ estimates for the 20ch H/N appear to be extrapolated from Wiggins 2006 and de Zwart 2004, which tested different coils. The 20ch H/N's element geometry is not a scaled version of the 32ch soccer-ball array. Without local SNR measurements, your quantitative claims are speculative."**

4. **"The noise covariance matrices of these two coils are unrelated. Any denoising step that depends on noise structure (e.g., ICA, ME-ICA, prewhitening) will behave differently for each coil. Could this create systematic differences in the number of retained components or the noise floor of connectivity estimates?"**

5. **"A 'conditionally acceptable' verdict without traveling-subject validation is insufficient for a journal claiming cross-site poolability. At minimum, provide 5-6 traveling subjects scanned on both coils to demonstrate that the bias is measurable and correctable."**

### 3.4 Comparison to Scenario (a) Publishability

| Factor | Scenario (a) | Scenario (b) | Impact |
|--------|:---:|:---:|:-------:|
| Same hardware continuity | Yes | **No** | Scenario (b) loses the strongest defense |
| SNR loss magnitude | Moderate | **Large** | More power loss, harder to defend |
| Existing lit. support | Indirect (extrapolation) | **Partly direct (Schmitt)** | Scenario (b) has one directly relevant paper |
| Harmonization complexity | Simple | **Complex** | More methods needed |
| Confound with clinical group | Possible | **More likely** (claustrophobia) | Higher risk with anxious populations |
| **Overall submission risk** | **Moderate** | **High** | Scenario (b) is riskier |

---

## 4. Comparison to Scenarios (a) and (c)

### 4.1 Scenario (a) — Same coil, lower-20 mode

**Key differences:**
- **Scenario (a):** Elements are physically identical; only the number of active channels varies. SNR loss is purely quantitative.
- **Scenario (b):** Elements are physically different; SNR loss is both quantitative AND qualitative (different sensitivity profiles).
- Scenario (a) can use the "partial-array subset" argument; scenario (b) cannot.
- Scenario (a) has ~40-55% dorsal SNR loss; scenario (b) has ~55-70% loss — approximately 15-20 percentage points worse.
- Scenario (a)'s noise covariance matrix is preserved for the remaining elements; scenario (b)'s is completely different.

### 4.2 Scenario (c) — Third party / unknown vendor coil

**Key differences:**
- Scenario (c) introduces unknown element geometry, preamp specs, and compatibility with Siemens body coil.
- Scenario (b) is at least a known Siemens product with published data.
- Scenario (c) may have B₁⁺ issues if the coil includes integrated transmit or if the body-coil matching is different.
- Scenario (b) is safer than (c) but riskier than (a).

### 4.3 MF Items — Differential Applicability

From the integration report's Must Fix list:

| MF # | Applies to Sc. (b)? | Difference from Sc. (a) |
|------|:---:|------------------------|
| **MF1** (B₁⁺ oversimplified) | **Yes, more strongly** | The 20ch H/N's housing extends onto neck/shoulders, creating more B₁⁺ perturbation than the 32ch's tight housing |
| **MF2** (detachable-ring error) | **N/A** | No error to correct — but the detachable **anterior component** of the 20ch H/N introduces a similar ambiguity |
| **MF3** (g-factor estimates) | **Yes, critically** | g-factor for the 20ch H/N cannot be estimated from 32ch data; requires separate measurement or simulation |
| **MF4** (tSNR collider bias) | **Yes, equally** | Same risk |
| **MF5** (2024-2026 citations) | **Yes, equally** | Same gap |
| **MF6** (covariate modeling) | **Yes, more strongly** | The larger, more complex bias in Sc. (b) makes the fixed-covariate limitation more severe |
| **MF7** (power analysis) | **Yes, with larger effect** | Power loss is ~15-25% (vs ~5-10% in Sc. a); power analysis is more critical |
| **MF8** (ComBat/SMA validation) | **Yes, with larger batch effect** | The batch effect is larger; ComBat/SMA performance may degrade; simulation validation more important |
| **MF9** (ROI cherry-picking) | **Yes, equally** | Same pre-registration requirement |
| **MF10** (longitudinal plan) | **Yes, equally** | Same need |
| **MF11** (decision boundaries) | **Yes, with tighter thresholds** | tSNR thresholds should be stricter (e.g., dlPFC tSNR < 100 for Sc. b vs < 80 for Sc. a) |

---

## 5. Cross-Verification of Agent A

**[Awaiting Agent A's output]**

## 6. Cross-Verification of Agent C

**[Awaiting Agent C's output]**

## 7. Final Consensus Statement

**[To be completed after cross-verification]**

---

## References Cited in This Report

1. Schmitt T, Rieger JW. Recommendations of choice of head coil and prescan normalize filter depend on region of interest and task. *Front Neurosci.* 2021;15:735290.
2. Wiggins GC, Triantafyllou C, Potthast A, Reykowski A, Nittka M, Wald LL. 32-channel 3 Tesla receive-only phased-array head coil with soccer-ball element geometry. *Magn Reson Med.* 2006;56(1):216-223.
3. Triantafyllou C, Polimeni JR, Wald LL. Physiological noise and signal-to-noise ratio in fMRI with multi-channel array coils. *NeuroImage.* 2011;55(2):597-606.
4. de Zwart JA, Ledden PJ, van Gelderen P, Bodurka J, Chu R, Duyn JH. Signal-to-noise ratio and parallel imaging performance of a 16-channel receive-only brain coil array at 3.0 Tesla. *Magn Reson Med.* 2004;51(1):22-26.
5. Panman JL, To YY, van der Ende EL, et al. Bias introduced by multiple head coils in MRI research: an 8 channel and 32 channel coil comparison. *Front Neurosci.* 2019;13:729.
6. Fortin JP, Parker D, Tunç B, et al. Harmonization of multi-site diffusion tensor imaging data. *NeuroImage.* 2017;161:149-170.
7. Wang YW, Chen X, Yan CG. Comprehensive evaluation of harmonization on functional brain imaging for multisite data-fusion. *NeuroImage.* 2023;274:120089.
8. Yamashita A, Yahata N, Itahashi T, et al. Harmonization of resting-state functional MRI data across multiple sites via matching of histogram and principal components. *Hum Brain Mapp.* 2019;40(6):1787-1798.
9. Beer JC, Tustison NJ, Cook PA, et al. Longitudinal ComBat: a method for harmonizing longitudinal multi-scanner imaging data. *NeuroImage.* 2020;220:117129.
10. Krüger G, Glover GH. Physiological noise in oxygenation-sensitive magnetic resonance imaging. *Magn Reson Med.* 2001;46(4):631-637.
