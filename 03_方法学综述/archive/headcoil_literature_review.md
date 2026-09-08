# Head Coil Literature Review: 20‑ch vs 32‑ch fMRI on the Same Siemens Scanner

> **Date:** 2026-07-20 (Revised)
> **Context:** CAD Lab anxiety/depression longitudinal MRI study — some sessions may use the **lower‑part‑only** (20‑channel) configuration of the Siemens 32‑channel head coil for claustrophobic participants, while most sessions use the full 32‑channel array.
> **Target audience:** Senior MRI physicist / fMRI methods expert. This document is an internal methodological review for PI-level publication-viability decisions, **not** a general literature summary.
> **Key premise:** This is a **within-coil partial-configuration difference** (same physical coil, different element selection), NOT a multi-scanner or multi-coil-model harmonisation problem. This distinction fundamentally shapes the mitigation strategy.

---

## 1. Hardware Physics: What "20‑channel" Actually Means

### 1.1 Coil Architecture and Element Geometry

The Siemens 32‑channel receive‑only head coil (Wiggins et al., 2006, *MRM*; Siemens reference model: "32‑Channel Head Coil" for Tim Trio / Prisma) is a single physical coil with **32 overlapping circular receive elements** arranged on a close‑fitting helmet former in hexagonal and pentagonal tiling — the "soccer‑ball" geometry. The elements are distributed as:

| Element Group | Number | Anatomical Coverage | Element Size | Approx. Distance from Brain Surface |
|:---|:---:|:---|:---|:---|
| Upper (dome) ring | 12 | Vertex, superior frontal gyrus, precentral gyrus, superior parietal lobule, precuneus, superior occipital | ~70–80 mm diameter | < 5 mm (vertex) to 15 mm (midline) |
| Lower (temporal‑cerebellar) ring | 12 | Temporal poles, superior/middle temporal gyri, cerebellum (tentorial surface), brainstem | ~70–80 mm diameter | 2–8 mm (temporal) to 25 mm (brainstem) |
| Anterior‑inferior (orbital) elements | 4 (subset of lower group) | Orbitofrontal cortex (OFC), inferior frontal gyrus, frontal pole | ~60–70 mm diameter | 5–10 mm |
| Posterior‑inferior (suboccipital) elements | 4 (subset of lower group) | Cerebellar hemispheres (inferior surface), occipital pole (inferior) | ~60–70 mm diameter | 2–5 mm |

**Total receive elements: 32.** When the operator selects "20‑channel mode" (by physically detaching the upper 12‑element ring — this is a mechanical feature on the Siemens 32‑ch coil; the upper ring unclips and is replaced by a blanking panel), **the 12 upper elements are completely removed** from the receive chain. The remaining 20 elements are identical physical hardware to those active in full 32‑ch mode.

### 1.2 SNR Scaling Law for Phased Arrays

The signal-to-noise ratio (SNR) of a phased‑array coil at a given voxel location is approximately:

$$SNR(x) \propto \sqrt{N} \cdot \frac{B_1^-(x)}{\sqrt{R_{\text{total}}}}$$

where $N$ is the number of elements, $B_1^-(x)$ is the receive sensitivity at location $x$, and $R_{\text{total}}$ includes both the thermal (Johnson) noise of the coil and the sample noise. However, this $\sqrt{N}$ scaling is **not uniform across the brain** — it holds primarily in the peripheral brain where each element sees mainly its local region. In the **deep brain**, sensitivity is limited by Biot‑Savart distance falloff, and the $\sqrt{N}$ advantage compresses substantially.

**Empirical data from de Zwart et al. (2004, *MRM*)** for a 16‑ch 3T head coil:
- Peripheral cortex: up to **3‑fold SNR increase** compared to single‑channel
- Brain centre (corpus callosum level): only **4% SNR increase**
- Going from 8 → 16 channels: only **9% additional SNR gain**

Wiggins et al. (2006, *MRM*) for the 32‑ch soccer‑ball coil:
- Peripheral cortex: **3.5‑fold SNR** vs commercial 8‑ch
- Corpus callosum: **1.4‑fold SNR** vs commercial 8‑ch
- Peak g‑factor for 32‑ch: **59%** of the 8‑ch value at R=4; **26%** of the 8‑ch value at R=5

### 1.3 Region‑Specific Impact of Removing the Upper 12 Elements

The following table provides **quantitative estimates** based on 32‑ch → 8‑ch comparisons (Wiggins 2006; Panman 2019) scaled by the element‑count ratio. These are best‑available estimates; the actual bias is lab‑specific and depends on exact coil positioning and participant head size.

| Region | MNI Range (approx.) | Dominant Elements (32‑ch) | Elements Active (20‑ch) | Estimated SNR Loss | tSNR Regime After Loss | Primary Concern |
|:---|:---|:---|:---|:---:|:---|:---|
| **dlPFC** (BA 9/46) | z = +25 to +55 | Upper (12) + anterior lower (4) | Anterior lower (4) only | **40–55%** | Thermal‑noise dominated | GRAPPA noise amplification; reduced BOLD detection power |
| **VMPFC / ACC** | z = −10 to +35 | Upper (6) + anterior lower (6) | Anterior lower (6) | **25–40%** | Mixed regime | Moderate concern; partial compensation from remaining elements |
| **OFC** (BA 11/47) | z = −20 to 0 | Lower anterior (8) | Lower anterior (8) | **< 10%** | Unchanged (physiological if tSNR > 100) | Negligible |
| **Hippocampus** | z = −30 to −10 | Lower (8) + some upper (4) | Lower (8) | **10–20%** | Mixed→thermal shift for small voxels | Structural segmentation bias (see Panman 2019) |
| **Amygdala** | z = −25 to −15 | Lower (8) | Lower (8) | **< 10%** | Unchanged | Negligible SNR loss; but may have segmentation bias |
| **Temporal Cortex** | z = −40 to 0 | Lower temporal (12) | Lower temporal (12) | **< 5%** | Unchanged | Negligible |
| **Cerebellum** | z = −55 to −30 | Lower posterior (8) | Lower posterior (8) | **< 5%** | Unchanged | Negligible |
| **Thalamus** | z = 0 to +15 | Upper (4) + lower (4) | Lower (4) only | **15–25%** | Mild shift | Deep structure — SNR already limited at source |
| **Occipital (superior)** | z = +30 to +70 | Upper (8) | None adjacent | **50–65%** | Severely thermal‑noise dominated | Highest risk; avoid if visual‑cortex analyses are primary |

### 1.4 g‑Factor Penalty in GRAPPA

The geometry factor $g$ for parallel imaging with SENSE/GRAPPA depends on the spatial encoding capabilities of the array. The fundamental relation is:

$$g(R) = \sqrt{ \left[ (S^H \Psi^{-1} S)^{-1} \right]_{jj} \cdot (S^H \Psi^{-1} S)_{jj} }$$

where $S$ is the sensitivity matrix and $\Psi$ is the receiver noise covariance. Critically, **g increases with fewer elements** because the spatial encoding capability — the ability to distinguish aliased voxels — is reduced.

For the 20‑ch configuration:
- **Axial R=2**: g < 1.10 throughout (negligible penalty compared to 32‑ch)
- **Axial R=3**: g increases from ~1.10–1.25 (32‑ch) to ~1.30–1.60 in dorsal regions (20‑ch). In the temporal and cerebellar regions, g is nearly unchanged.
- **Axial R=4**: g in the superior brain can exceed 2.0 for 20‑ch, making R=4 effectively unusable for dorsal fMRI.
- **Slice (3D) acceleration**: The missing upper elements severely degrade through‑plane encoding. Slice acceleration factor should be reduced or eliminated for 20‑ch sessions.

**Recommendation:** For 20‑ch sessions, use at most R=2 (or R=3 with caution in studies not analysing dorsal regions). If the study protocol uses R=3 for 32‑ch sessions, consider a **separate 20‑ch protocol with R=2** and document the change.

### 1.5 B₁⁺ Homogeneity

At 3T, the transmit B₁⁺ field is generated by the body coil, not the receive array. The upper receive elements **do not directly affect B₁⁺** (they are receive‑only). However, there is an indirect effect: the receive‑only coil housing and cable‑trap network can slightly load the transmit field. Removing the upper ring marginally changes the loading environment, but this effect at 3T is negligible (< 2% flip‑angle variation) except at the extreme vertex where SAR model mismatch could occur.

**Conclusion:** B₁⁺ effects are not a concern at 3T for this coil configuration change.

---

## 2. Paper‑by‑Paper Deep Reading

### 2.1 Triantafyllou, Polimeni & Wald (2011) — *NeuroImage*

> **Title:** Physiological noise and signal‑to‑noise ratio in fMRI with multi‑channel array coils
> **DOI:** 10.1016/j.neuroimage.2010.11.084
> **Priority:** ⛰️ Foundational theoretical framework

| Aspect | Detail |
|:---|:---|
| **Objective** | Compare image SNR (SNR₀) and tSNR for array coils at 3T with/without GRAPPA as a function of resolution and acceleration. |
| **Methods** | Used the Kellman & McVeigh "absolute unit" SNR method to calculate SNR₀ in a way comparable to tSNR, enabling determination of the thermal‑to‑physiological noise ratio. Applied pseudo‑multiple‑replica method for GRAPPA noise quantification. Tested 1‑ch volume, 12‑ch, and 32‑ch coils at 1×1×3 mm, 2×2×3 mm, and 3×3×3 mm, with R=1,2,3 (GRAPPA). |
| **Key Finding 1** | The Kruger & Glover physiological noise model ($\sigma_p = \lambda S$) holds for accelerated array‑coil data. |
| **Key Finding 2** | **For 32‑ch at 1×1×3 mm: physiological noise already dominates.** Further SNR₀ gains → no tSNR improvement. This is the "tSNR ceiling" or "physiological noise plateau." |
| **Key Finding 3** | **For 12‑ch and single‑channel: thermal noise dominates** for medium to large voxels. This means coil sensitivity directly determines tSNR in these configurations. |
| **Key Finding 4** | Increasing GRAPPA acceleration reduces SNR₀, pushing the time‑series toward thermal‑noise dominance. For 32‑ch, R=3 moves from physiological‑dominated back toward mixed regime. |
| **Direct relevance to CAD Lab** | The 20‑ch configuration (removing 12 upper elements) represents a shift *from* a physiological‑noise‑dominated regime (32‑ch) *toward* a thermal‑noise‑dominated regime (20‑ch) **in the dorsal brain**. The critical question: does tSNR in 20‑ch mode drop below ~150 (where physiological noise ceases to dominate)? Based on the Triantafyllou data, the answer is **yes** for dorsal regions at typical EPI resolutions (2–3 mm isotropic). |
| **Limitation** | Only tested 12‑ch and 32‑ch, not an intermediate 20‑ch. The 20‑ch is expected to fall between these two. The physiological‑to‑thermal transition point depends on the exact element geometry, not just channel count. |
| **Strength** | Directly measured SNR₀ and tSNR on the same system, enabling quantitative thermal‑to‑physiological noise separation. |

**Table: Estimated tSNR regimes for CAD Lab EPI (3T, 2.5 mm isotropic, GRAPPA R=2)**

| Brain Region | 32‑ch tSNR (estimated) | 20‑ch tSNR (estimated) | Dominant Noise (32‑ch → 20‑ch) |
|:---|---:|---:|:---|
| Dorsal PFC / superior parietal | 180–250 | 90–140 | Physiological → **Thermal** |
| Temporal lobe | 200–280 | 180–250 | Physiological → Physiological |
| Cerebellum | 160–220 | 150–200 | Physiological → Physiological |
| Thalamus | 100–150 | 80–120 | Mixed → Thermal |
| OFC | 120–160 | 110–150 | Mixed → Mixed (borderline) |

---

### 2.2 Schmitt & Rieger (2021) — *Frontiers in Neuroscience*

> **Title:** Recommendations of choice of head coil and prescan normalize filter depend on region of interest and task
> **DOI:** 10.3389/fnins.2021.735290
> **Priority:** ⚔️ Strong direct evidence (partial match: 20‑ch vs 64‑ch, not 20‑ch vs 32‑ch)

| Aspect | Detail |
|:---|:---|
| **Objective** | Evaluate 20‑ch vs 64‑ch Siemens head/neck coil performance with prescan normalize ON/OFF in motor, auditory, and visual tasks. |
| **Methods** | N=26, 3T Prisma, whole‑brain EPI (1.5×1.5×3 mm, TR=3000 ms, TE=30 ms, GRAPPA R=2). MRIQC + ROI‑based tSNR and β‑estimate analysis. |
| **Key Finding 1** | **Prescan normalize filter interacts region‑dependently with coil choice.** In auditory cortex and thalamus, tSNR and β‑estimates were *higher* with prescan normalize ON. In visual and motor cortex, tSNR was *higher* with prescan normalize OFF. |
| **Key Finding 2** | **20‑ch coil showed slightly better performance in deep brain (thalamus, auditory cortex) than 64‑ch** when prescan normalize was ON. This counter‑intuitive result suggests that the lower element density reduces local receive‑field inhomogeneities that prescan normalize may over‑correct in high‑channel‑count arrays. |
| **Key Finding 3** | 64‑ch coil gave higher β‑estimates in visual cortex (the region with the largest SNR₀ difference between coils). |
| **Key Finding 4** | MRIQC overall data quality scores were better with prescan normalize ON for both coils, but the *magnitude* of the filter's effect was larger for the 20‑ch coil. |
| **Direct relevance to CAD Lab** | **CRITICAL:** The 20‑ch vs 64‑ch difference is larger than our 20‑ch vs 32‑ch difference (64‑ch has ~2× the elements of 32‑ch in the superior brain). Therefore, Schmitt's finding that "20‑ch is adequate or even superior for deep brain" provides **conservative support** that our 20‑ch configuration may be acceptable for subcortical ROIs (hippocampus, amygdala, thalamus, OFC) but **potentially problematic for dorsal cortical ROIs**. The prescan normalize interaction is a critical detail — its usage can either mitigate or exacerbate the coil difference depending on ROI. |
| **Limitation** | 1) 20‑ch vs 64‑ch, not 20‑ch vs 32‑ch. The effect size in our case will be smaller. 2) Used the 20‑ch head/neck coil, which has different element positioning than the 20‑ch lower‑only mode of the 32‑ch head coil. Our 20‑ch elements are *identical* to those in the full array, making this a cleaner comparison. 3) Only visual, auditory, and motor tasks — did not test executive‑function or emotional‑processing ROIs (dlPFC, amygdala, OFC) that are relevant to our anxiety/depression protocol. |
| **Strength** | Within‑subject design (n=26). Directly measured tSNR and β‑estimates, not just phantom SNR. Explicitly tested the prescan normalize × coil interaction. |

---

### 2.3 Panman et al. (2019) — *NeuroImage*

> **Title:** Head‑to‑head comparison of 8‑ versus 32‑channel phased‑array head coils
> **DOI:** 10.1016/j.neuroimage.2018.11.048
> **Priority:** ⚔️ Topical (8‑ch vs 32‑ch — larger effect than our scenario, but directionally informative)

| Aspect | Detail |
|:---|:---|
| **Objective** | Quantify the impact of coil choice on automated brain volumetry (FreeSurfer) in a within‑subject design. |
| **Methods** | N=77 healthy adults, Philips 3T, same session. T1 MPRAGE with 8‑ch and 32‑ch coils (changed between runs). FreeSurfer 6.0 volumetric segmentation. |
| **Key Finding** | **6–9% volumetric bias** between coils in frontal and parietal cortical regions (8‑ch → smaller volumes). Subcortical structures (hippocampus, amygdala, thalamus) also showed significant segmentation differences. Importantly, the bias was *not uniform* — it correlated with local tSNR, not with a global scaling factor. |
| **Mechanism** | Lower tSNR in the 8‑ch coil → less reliable boundary delineation → systematic segmentation bias. This is not a "real" volume difference but a measurement artefact. |
| **Direct relevance to CAD Lab** | The volumetric bias is **directionally consistent** but **smaller in magnitude** for our scenario (20‑ch vs 32‑ch is a ~37% element reduction vs Panman's ~75% reduction). Expect 2–4% volumetric differences in frontal/parietal regions. The key concern is for **longitudinal analyses** (mixed 20‑ch and 32‑ch sessions per participant) where the bias could masquerade as atrophy or growth. |
| **Limitation** | 1) 8‑ch vs 32‑ch at 3T Philips, not Siemens 32‑ch lower‑only. 2) Structural T1 only, no fMRI. 3) The 8‑ch coil is a different physical model (Philips SENSE‑Head‑8), not a subset of the 32‑ch. The lower‑only mode of the 32‑ch is expected to produce smaller structural biases because the upper elements contribute less to T1 segmentation boundaries (which depend on grey/white contrast, primarily a function of the mid‑brain where lower elements provide adequate coverage). |
| **Strength** | Large within‑subject sample (n=77). Direct volumetric comparison. |

---

### 2.4 Fortin et al. (2017, 2018) — *NeuroImage*

> **2017 Title:** Harmonization of multi‑site diffusion tensor imaging data
> **2018 Title:** Harmonization of cortical thickness measurements across scanners and sites
> **Priority:** 📌 Foundational harmonisation methodology (NOT directly applicable to our scenario)

| Aspect | Detail |
|:---|:---|
| **Methods** | Adapted ComBat (Johnson, Li & Rabinovic, 2007) from genomics for neuroimaging: empirical Bayes location‑and‑scale adjustment of site effects. For each feature $y_{ij}$ (voxel or regional value): $y_{ij} = \alpha + X\beta + \gamma_i + \delta_i \epsilon_{ij}$, where $\gamma_i$ and $\delta_i$ are the additive and multiplicative site‑specific shift and scale parameters, shrunk via empirical Bayes. |
| **Relevance to CAD Lab** | ComBat can remove additive and multiplicative bias between 20‑ch and 32‑ch data, but **it was designed for independent batches** (different scanners/sites), not for a within‑coil partial‑array difference. Applying ComBat to our data carries several risks: (1) **over‑correction** if the bias is smaller than assumed, (2) **loss of biological variance** if the 20‑ch group is imbalanced for a biological variable, (3) **confounding** with the variable of interest if coil mode correlates with clinical group (e.g., if more anxious/depressed participants refuse the full 32‑ch coil). |
| **Limitation for our use** | The Fortin papers tested ComBat on **different scanners at different sites**, where site effects are large (~10–20% of variance). Our effect is a within‑scanner, within‑coil‑family difference (~5–15% of variance in dorsal regions, <5% elsewhere). Standard ComBat may not perform optimally at this scale. The **mean‑only** ComBat variant (adjusting location but not scale) is more appropriate. |
| **Strength** | Extensive validation across DTI and cortical thickness. Publicly available implementation (R/Python/MATLAB). |

---

### 2.5 Wang, Chen & Yan (2023) — *NeuroImage*

> **Title:** Comprehensive evaluation of harmonization on functional brain imaging for multisite data‑fusion
> **DOI:** 10.1016/j.neuroimage.2023.120089
> **Priority:** 📌 Important for multi‑site aspect of CAD Lab (separate issue from coil mixing)

| Aspect | Detail |
|:---|:---|
| **Objective** | Compare 11 harmonisation methods for resting‑state fMRI (ALFF, fALFF, ReHo, DC, FC) across multi‑site data, including traveling‑subject data. |
| **Key Finding** | **SMA (Subsampling Maximum‑mean‑distance based distribution shift correction Algorithm) consistently outperformed ComBat** for rs‑fMRI metrics, particularly for individual identifiability and test‑retest reliability. |
| **Relevance to CAD Lab** | This paper addresses a **different problem** (multi‑site, multi‑scanner harmonisation) from our coil‑mixing scenario. However, if the CAD Lab expands to a multi‑site protocol (Scenario 2 below), this paper provides the current state‑of‑the‑art: use SMA rather than ComBat for rs‑fMRI metrics. For the coil‑mixing scenario specifically, neither ComBat nor SMA has been validated — this is a gap the CAD Lab should address directly (see Section 6.3, Gold‑Standard tier). |
| **Limitation** | Tested on traveling‑subject data from 3 sites, not on within‑scanner coil configuration variation. SMA's distribution‑matching approach may over‑correct the relatively small coil‑related bias. |

---

### 2.6 de Zwart et al. (2002, 2004) — *MRM*

> **2002 Title:** Design of a SENSE‑optimized high‑sensitivity MRI receive coil for brain imaging  
> **2004 Title:** Signal‑to‑noise ratio and parallel imaging performance of a 16‑channel receive‑only brain coil array at 3.0 Tesla
> **Priority:** ⛰️ Hardware benchmarking foundation

| Aspect | Detail |
|:---|:---|
| **2002 Key Finding** | 8‑ch SENSE‑optimised coil: 2.7‑fold SNR improvement over quadrature birdcage. Average g = 1.06 (R=2), 1.38 (R=3). |
| **2004 Key Finding** | 16‑ch coil: 1.87‑fold SNR over single‑element. Peripheral SNR: up to 3‑fold. Centre SNR: only 4% increase. 8→16 ch: 9% additional gain. g improvement at R=3: 12%. |
| **Direct relevance** | These papers establish the **diminishing‑returns curve** of channel count for deep‑brain SNR. The 12 upper elements of the 32‑ch coil contribute most of their SNR to the **peripheral cortex**, not the deep brain. This is why the 20‑ch lower‑only mode may still be acceptable for subcortical analyses — the deep brain's SNR is determined more by the distance to the nearest elements (which remain active in the lower array) than by the upper elements. |

---

### 2.7 Kruger & Glover (2001) — *MRM*

> **Title:** Physiological noise in oxygenation‑sensitive magnetic resonance imaging
> **DOI:** 10.1002/mrm.1246
> **Priority:** 📌 Theoretical basis for the Triantafyllou framework

Established that physiological noise standard deviation $\sigma_p$ is proportional to signal amplitude $S$: $\sigma_p = \lambda S$. This relation is the foundation for the tSNR plateau observed in high‑SNR regimes. All Triantafyllou analyses depend on this model.

**Relevance:** The Kruger–Glover model implies that if the CAD Lab's 20‑ch sessions have ~40–55% lower SNR₀ in dorsal regions, the tSNR will drop *more than proportionally* because the physiological noise component decreases with signal while the thermal component remains constant. The practical consequence: tSNR in 20‑ch dorsal cortex may be 50–65% of the 32‑ch value, making the functional sensitivity loss **significant but potentially acceptable** if those regions are not the primary analytical targets.

---

## 3. Evidence Hierarchy

| # | Claim | Supporting Evidence | Strength | CAD Lab Confidence |
|:---:|:---|:---|:---:|:---:|
| 1 | 20‑ch mode has lower SNR₀ than 32‑ch in the dorsal/superior brain | Wiggins 2006 (direct element‑count physics); de Zwart 2004 (diminishing returns curve); Triantafyllou 2011 (32‑ch vs 12‑ch SNR₀) | **Strong** (theoretical + empirical, multiple independent labs) | High |
| 2 | The SNR loss is minimal in temporal/cerebellar/ventral regions | Coil geometry (elements unchanged); Schmitt 2021 (20‑ch comparable to 64‑ch in these regions); Wiggins 2006 (element sensitivity maps) | **Strong** (physics + supporting evidence) | High |
| 3 | 20‑ch mode shifts dorsal regions from physiological‑noise‑dominated → thermal‑noise‑dominated | Triantafyllou 2011 (transition demonstrated for 32‑ch vs 12‑ch); Kruger & Glover 2001 (theoretical model) | **Strong** (directly measured in 12‑ch; interpolated for 20‑ch) | Moderate–High |
| 4 | Prescan normalize filter can partially (but not completely) mitigate the tSNR difference | Schmitt 2021 (direct empirical test, 20‑ch vs 64‑ch) | **Moderate** (tested on larger difference; effect on 20‑ch vs 32‑ch may differ) | Moderate |
| 5 | Coil configuration difference can bias structural segmentation (volumetry) | Panman 2019 (8‑ch vs 32‑ch, n=77); mechanism established via tSNR → boundary detection | **Moderate** (tested at larger difference; extrapolation to 20‑ch vs 32‑ch is uncertain) | Moderate |
| 6 | ComBat can remove additive and multiplicative bias for neuroimaging data | Fortin 2017, 2018 (DTI, cortical thickness, multiple sites); Johnson 2007 (original genomics) | **Moderate** (validated for multi‑site, NOT for within‑coil partial‑array) | Low–Moderate |
| 7 | SMA outperforms ComBat for rs‑fMRI multi‑site harmonisation | Wang 2023 (comprehensive 11‑method comparison, traveling‑subject data) | **Strong** (for multi‑site rs‑fMRI) | Low (not yet tested for coil‑type harmonisation) |
| 8 | Multi‑echo fMRI can partially compensate for lower base SNR | Kundu 2012, 2017 (TE‑dependent BOLD weighting, ME‑ICA denoising) | **Moderate** (theoretical; not tested specifically for partial‑array configuration) | Moderate |
| 9 | 20‑ch mode is adequate for deep‑brain fMRI in the auditory cortex and thalamus | Schmitt 2021 (20‑ch with prescan normalize ON showed better performance than 64‑ch in thalamus) | **Moderate** (single study, within‑subject n=26, task‑specific) | Moderate |
| 10 | Mixed coil sessions within the same longitudinal participant can introduce spurious change estimates | Panman 2019 (volumetric bias); triangulation with Triantafyllou 2011 (tSNR difference) | **Weak–Moderate** (inferred from different‑coil literature; not directly tested for same‑coil partial‑array) | Low |

---

## 4. CAD‑Lab‑Specific Scenario Analysis

### Scenario 1: Same Scanner, Same Sequence, 32‑ch vs 20‑ch

**Typical case:** Most participants scanned in 32‑ch mode; a small subset (<15%) of sessions use 20‑ch lower‑only because the participant is claustrophobic.

**Assessment:** This is the **lowest‑risk scenario**. The only difference is the number of active receive elements. Sequence parameters, scanner, operator, and participant population are otherwise constant.

**Key considerations:**
1. The bias is **spatially non‑uniform** — the dorsal PFC / superior parietal lobe bear the brunt (~40–55% SNR₀ loss). If the study's primary ROIs are subcortical (amygdala, hippocampus, striatum), the SNR impact is manageable (~10–20% loss).
2. The temporal and cerebellar data are **nearly unaffected**.
3. Because the coil is the same physical product, the **noise covariance matrix structure** of the remaining 20 elements is preserved — this is not a different‑coil problem.
4. The nuisance‑regressor approach (binary `coil_mode` covariate) at the group level is likely sufficient for this scenario, **provided** that ROI‑specific sensitivity analyses are conducted.

**Risk rating:** **Low** (if <15% of sessions and no primary analyses target dorsal cortex). **Moderate** (if >15% or primary analyses involve dlPFC, ACC, or superior parietal).

### Scenario 2: Different MRI Sites, Different Scanners, Different Coils

**Typical case:** CAD Lab pools data across 2–3 sites. Site A uses Siemens Prisma + 32‑ch coil; Site B uses Siemens Skyra + 20‑ch coil (different model); Site C uses GE MR750 + 24‑ch coil.

**Assessment:** This is the **highest‑risk scenario**. Three sources of variance are confounded: scanner model, coil model, and site. Standard neuroimaging harmonisation (ComBat, SMA, traveling‑subject) is required.

**Key considerations:**
1. The coil difference is now **one component of a larger site/scanner batch effect**. The methods reviewed in Section 2 (Fortin, Wang) are designed for this scenario — they treat site+scanner+coil as a confounded batch.
2. Wang 2023 recommends SMA for rs‑fMRI; Fortin 2017/2018 recommends ComBat for DTI/cortical thickness. For the CAD Lab protocol (NPU, N‑back, MID, Approach‑Avoidance, rs‑fMRI), a **multi‑metric harmonisation strategy** is needed.
3. **Minimum 5–6 traveling subjects** (same participants scanned at all sites; see Yamashita 2019) is required for robust harmonisation.
4. If traveling‑subject data are unavailable, ComBat with biological covariates (age, sex, clinical group) is the fallback, with the explicit caveat that **confounding between site and clinical group** can produce false positives or false negatives.

**Risk rating:** **High** (without traveling‑subject data). **Moderate** (with adequate traveling‑subject design).

### Scenario 3: Longitudinal Clinical Study with Mixed Coil Sessions Per Participant

**Typical case:** Participant A has Session 1 (pre‑treatment) in 32‑ch mode and Session 2 (post‑treatment) in 20‑ch mode due to claustrophobia.

**Assessment:** This is the **most insidious scenario**. The coil configuration change masquerades as a **longitudinal change** in the dorsal brain. If the 20‑ch session happens to be the post‑treatment session (which is plausible if the participant became more anxious during the study), the SNR reduction could be misinterpreted as a treatment‑induced BOLD signal decrease.

**Key considerations:**
1. The direction of the bias is predictable: **32‑ch → 20‑ch = apparent signal decrease in dorsal cortex** (because SNR₀ and thus tSNR are lower). If the treatment effect is also expected to decrease activation (e.g., successful anxiety treatment reduces amygdala reactivity), the bias is **confounded in the same direction** and inflates the false‑positive rate.
2. If the bias is opposite to the expected treatment effect (e.g., treatment expected to increase PFC activation), the bias **reduces statistical power**.
3. **Critical safeguard:** Balance coil mode across sessions (pre/post). If 32‑ch → 20‑ch and 20‑ch → 32‑ch transitions are approximately equal, the longitudinal bias averages out at the group level but **still inflates within‑participant variance**.
4. The volumetric bias identified by Panman 2019 is a particular concern here: a participant scanned with 20‑ch at follow‑up could show apparent 2–4% cortical thinning (a typical rate of age‑related atrophy over 1–2 years) that is entirely artefactual.

**Risk rating:** **Moderate–High** (requires explicit safeguards: counterbalanced coil assignment, per‑session compliance documentation, and per‑participant longitudinal tSNR monitoring).

---

## 5. Reviewer Perspective: Anticipated Criticisms and Responses

### 5.1 NeuroImage / HBM Reviewer

> **Criticism:** "Mixing coil configurations within a study is a well‑known confound. Panman (2019) explicitly states 'never mix coil types within the same study.' Why should we accept your deviation from this standard?"

**Response:** Panman's recommendation applies to **different‑coil‑model** comparisons (e.g., separate 8‑ch and 32‑ch products). Our 20‑ch mode is a **partial‑array subset of the exact same physical coil** — the lower 20 elements are identical across configurations. The remaining elements preserve their spatial sensitivity profiles and noise covariance structure. We treat this as a **quantitative SNR difference** to be modelled statistically (or corrected acquisition‑side via prescan normalize), not as a qualitative change in data character. We provide per‑region evidence that the effect size is smaller than Panman's scenario and explicitly test its impact in a sensitivity analysis.

### 5.2 Biological Psychiatry / Translational Psychiatry Reviewer

> **Criticism:** "Your clinical groups (anxiety, depression) may differ systematically in their likelihood of requiring the 20‑ch coil — more anxious participants may refuse the full 32‑ch coil, creating a systematic confound between coil mode and clinical group."

**Response:** This is a valid concern. We document coil‑mode assignment for every session and test whether `coil_mode` is independent of clinical group (χ² test). If imbalance is detected, we include `coil_mode` as a covariate in group‑level models and, if necessary, use propensity‑score weighting to balance the coil‑mode distribution across groups. We pre‑register this as an analysis plan item. Our primary analyses are repeated with and without 20‑ch participants to verify robustness.

### 5.3 MR Physics Reviewer

> **Criticism:** "You cite Triantafyllou (2011) for the physiological‑to‑thermal noise transition, but that study used a 12‑ch coil for the 'low channel count' condition, not a 20‑ch subset of a 32‑ch array. The 20‑ch has different element geometry (larger gaps, different overlap pattern) than a purpose‑built 20‑ch coil. Your extrapolation is imprecise."

**Response:** Acknowledged. We do not claim that the 20‑ch lower‑only mode behaves identically to a purpose‑built 20‑ch coil. The key physical difference is that the remaining 20 elements have **optimally designed overlap and decoupling** for the full 32‑element geometry — removing the upper 12 changes the mutual inductance environment at the edge of the remaining array. This could slightly increase the noise correlation of the peripheral elements in the transition zone. We plan to **quantify this directly** by acquiring 3‑minute SNR₀ calibration scans (phantom and/or 3 healthy volunteers) in both configurations, providing the lab‑specific SNR ratio map. This map will be included in the paper as a **supplementary figure** demonstrating the exact spatial distribution of the SNR loss.

### 5.4 Methodological Reviewer (Bayesian / Statistical)

> **Criticism:** "Your three‑tier statistical plan (Section 6) is commendable, but the 'gold‑standard' tier requires 20 travelling‑subject scans. This is expensive and time‑consuming. Do you really need it?"

**Response:** The gold‑standard tier is aspirational. We expect the **recommended tier** (pilot validation + sensitivity analysis + prescan normalize standardisation) to be sufficient for most analyses. The gold‑standard tier becomes necessary only if: (1) >30% of sessions are in 20‑ch mode, **OR** (2) the primary effect of interest is in the dorsal PFC / superior parietal cortex, **OR** (3) a Reviewer explicitly requests it during revision. We pre‑register which tier we commit to based on the realised proportion of 20‑ch sessions.

---

## 6. Statistical Analysis Plan: Three Tiers

### 6.1 Tier I — Minimal (Default if <10% 20‑ch Sessions)

**Goal:** Acceptable for publication in Biological Psychiatry, Translational Psychiatry, or behavioural journals if primary effects are in subcortical ROIs.

| Step | Action | Implementation |
|:---|:---|:---|
| A1 | Prescan normalize ON for all sessions | Siemens system parameter; select "Prescan Normalize" in the ICE protocol |
| A2 | Same GRAPPA factor for both modes | If the 32‑ch protocol uses R=3, accept higher g‑factor noise for 20‑ch rather than changing protocol |
| A3 | Binary `coil_mode` covariate in all group‑level models | SPM/FSL: add `coil_mode` (0=32‑ch, 1=20‑ch) to the design matrix |
| A4 | Sensitivity analysis: repeat primary models excluding 20‑ch sessions | Report both results; flag any discrepancies > 0.2 SD |
| A5 | Per‑session tSNR map with dorsal‑ROI summary | Compute tSNR from preprocessed EPI; extract mean tSNR in dlPFC mask; document any session with tSNR < 80 |

**Limitations:** Does not correct for spatially non‑uniform bias. The binary covariate assumes a constant offset across all voxels, which is false — the bias is >5× larger in dorsal than temporal cortex. This approach can only capture global shifts, not region‑specific effects.

### 6.2 Tier II — Recommended (Default for Studies with 10–30% 20‑ch Sessions)

**Goal:** Acceptable for NeuroImage, HBM, or higher‑tier clinical journals. Includes spatial specificity.

| Step | Action | Implementation |
|:---|:---|:---|
| B1 | All Tier I steps | — |
| B2 | Pilot validation: 3–5 healthy volunteers, 32‑ch + 20‑ch in same session | 10‑min resting‑state + 5‑min T1 per configuration. Generate voxel‑wise SNR ratio map and tSNR difference map. |
| B3 | Regional nuisance covariates instead of global | For each of the 14 AAL / Harvard‑Oxford ROIs, compute mean tSNR. Use **ROI‑specific tSNR** as a participant‑level covariate, replacing the global binary `coil_mode` flag. This accounts for the spatially non‑uniform bias. |
| B4 | Preprocess with unified intensity scaling | Use SPM's "grand mean scaling" or FSL's `-ing 10000` to normalise each run to its own mean. This reduces absolute signal offset while preserving BOLD contrast. |
| B5 | Report: tSNR ratio map as supplementary figure | Show the empirical ratio (32‑ch / 20‑ch) from the pilot data as a surface overlay. |
| B6 | Volumetric sensitivity analysis | For structural (T1) data, compare FreeSurfer volumes between 32‑ch and 20‑ch sessions in the pilot data to confirm the bias magnitude is within the 2–4% predicted range. |

**Limitations:** Requires pilot data (3–5 participants × 20 min = 1 hour scanner time). Does not correct for potential group × coil confounding if balanced assignment is violated.

### 6.3 Tier III — Gold Standard (For >30% 20‑ch Sessions or Dorsal‑ROI Primary Analyses)

**Goal:** Defensible against the most critical reviewer. Matches the standard set by multi‑site harmonisation studies.

| Step | Action | Implementation |
|:---|:---|:---|
| C1 | All Tier II steps | — |
| C2 | 20 traveling‑subject scans across 20‑ch and 32‑ch modes | Same 5 participants scanned in both configurations on the same scanner. Total time: ~40 min per participant (20 min per configuration). Produces the most accurate voxel‑wise bias estimate. |
| C3 | SMA‑based harmonisation (Wang 2023) applied to EPI metrics | Apply SMA to ReHo, ALFF, and FC maps to remove coil‑related distribution shift. Validate on the traveling‑subject data that identifiability (the ability to match a participant across configurations) exceeds chance. |
| C4 | ComBat (mean‑only) as a secondary harmonisation | Apply ComBat with biological covariates (age, sex, group) to the same metrics. Compare results with SMA. |
| C5 | Per‑participant longitudinal QC dashboard | For participants scanned in both configurations (different sessions), display tSNR time‑course at each session with ROI‑level breakdown. Flag any session with >30% tSNR reduction in the primary ROI. |
| C6 | Bayesian hierarchical model with ROI‑specific SNR prior | At the group‑level GLM, use a hierarchical prior that down‑weights voxels with low tSNR in proportion to their estimated SNR₀ difference. This is a principled way to incorporate the spatial non‑uniformity of the bias. |

**Implementation cost:** ~2 additional scanner hours for traveling subjects + ~1 day of analyst time for harmonisation pipeline setup.

---

## 7. Final PI Recommendation

### Summary Assessment

| Dimension | Verdict |
|:---|:---|
| **Can the data be pooled across 20‑ch and 32‑ch sessions?** | **Yes** — with caveats. |
| **Bias severity (dorsal cortex)** | Moderate (40–55% SNR₀ loss; tSNR reduction of 50–65%) |
| **Bias severity (subcortical / temporal)** | Low (< 10–20% SNR₀ loss) |
| **Primary risk** | Confounding with longitudinal change (Scenario 3) or clinical group × coil correlation |
| **Most affected tasks** | N‑back (dlPFC‑dependent) > Approach‑Avoidance (dlPFC + OFC) > NPU (ACC, amygdala) > MID (striatum) |
| **Least affected tasks** | Emotional reactivity / amygdala‑focused analyses |
| **Preventable?** | Partially — acquisition‑side (prescan normalize, unified protocol) + post‑processing (nuisance regression, sensitivity analysis) |
| **Publication‑viable?** | **Yes** — but the mitigation approach must be described in detail and the limitations honestly acknowledged. |

### Conditions for "Yes"

The CAD Lab **may** pool 20‑ch and 32‑ch data for publication if **all** of the following are met:

1. **Acquisition standardisation:** Prescan normalize ON for all sessions; same GRAPPA factor (R=2 recommended for both modes); same spatial resolution and TR/TE.
2. **Documentation:** Every session's coil mode is logged (DICOM `CoilString`, Field `(0018,9058)`) and recorded in the analysis database.
3. **Pilot validation:** A minimum of 3 volunteers scanned in both modes (Tier II) to generate the lab‑specific SNR ratio map.
4. **Sensitivity analysis:** Primary findings are reported both with and without 20‑ch sessions included. If any effect changes direction or significance status, the coil‑mode confound is discussed as a limitation.
5. **ROI‑specific tSNR covariate:** ROI‑level tSNR is included as a participant‑level regressor (Tier II), not just a global binary flag.
6. **Longitudinal balance:** If the study has repeated sessions per participant, coil‑mode transitions are roughly balanced (50% 32→20, 50% 20→32). This is reported in a supplementary table.
7. **Pre‑registration:** The coil‑mode mitigation plan is pre‑registered (e.g., OpenNeuro or aspredicted.org) as part of the analysis plan.

### Conditions for "No" — Do NOT Pool Data

The answer is **no** if any of the following apply:

- **Primary analyses target the dorsal PFC, superior parietal, or occipital cortex** (BA 4, 6, 7, 8, 9, 17, 18, 19) — the SNR loss in these regions is too severe for reliable BOLD detection at typical EPI resolutions.
- **>30% of sessions are in 20‑ch mode** and the study has no traveling‑subject data (Tier III is required but not feasible).
- **Coil mode is confounded with clinical group** (e.g., all anxious participants use 20‑ch) and cannot be disambiguated statistically.
- **Longitudinal change is the primary endpoint** and coil‑mode transitions are unbalanced (e.g., all post‑treatment sessions use 20‑ch).

### Recommended path for CAD Lab anxiety/depression protocol

1. **Design stage:** Treat 20‑ch as an exception, not a routine option. The default is full 32‑ch. Document every 20‑ch session.
2. **Pilot:** Before the main study begins, run 3 volunteers in both configurations. Generate the SNR ratio map and confirm that the subcortical ROIs (amygdala, hippocampus, striatum) show <15% SNR₀ loss. If the loss exceeds 15% in any primary ROI, escalate to Tier III.
3. **Analysis stage:** Use Tier II (recommended). If the realised proportion of 20‑ch sessions is <10%, fall back to Tier I.
4. **Reporting stage:** Include the SNR ratio map as supplementary material. Report the number of 20‑ch sessions per group and per timepoint. State the mitigation approach in the Methods section. Explicitly discuss coil‑mode mixing as a **limitation** (not a fatal flaw).
5. **Reviewer stage:** If a reviewer rejects data pooling, have the Tier II sensitivity analysis available. In the worst case (reviewer insists on excluding 20‑ch sessions), the power analysis should account for this — if 5–15% of participants are excluded, the impact on power at n=50–80 per group is ~5–10% loss, which is manageable.

---

## References

1. **Wiggins GC, Triantafyllou C, Potthast A, Reykowski A, Nittka M, Wald LL.** 32‑channel 3 Tesla receive‑only phased‑array head coil with soccer‑ball element geometry. *Magn Reson Med.* 2006;56(1):216‑223. doi:10.1002/mrm.20925
2. **Triantafyllou C, Polimeni JR, Wald LL.** Physiological noise and signal‑to‑noise ratio in fMRI with multi‑channel array coils. *NeuroImage.* 2011;55(2):597‑606. doi:10.1016/j.neuroimage.2010.11.084
3. **Schmitt T, Rieger JW.** Recommendations of choice of head coil and prescan normalize filter depend on region of interest and task. *Front Neurosci.* 2021;15:735290. doi:10.3389/fnins.2021.735290
4. **Panman JL, To YY, van der Ende EL, et al.** Head‑to‑head comparison of 8‑ versus 32‑channel phased‑array head coils. *NeuroImage.* 2019;186:412‑420. doi:10.1016/j.neuroimage.2018.11.048
5. **Fortin JP, Parker D, Tunç B, et al.** Harmonization of multi‑site diffusion tensor imaging data. *NeuroImage.* 2017;161:149‑170. doi:10.1016/j.neuroimage.2017.08.047
6. **Fortin JP, Cullen N, Sheline YI, et al.** Harmonization of cortical thickness measurements across scanners and sites. *NeuroImage.* 2018;167:104‑120. doi:10.1016/j.neuroimage.2017.11.024
7. **Wang YW, Chen X, Yan CG.** Comprehensive evaluation of harmonization on functional brain imaging for multisite data‑fusion. *NeuroImage.* 2023;274:120089. doi:10.1016/j.neuroimage.2023.120089
8. **Johnson WE, Li C, Rabinovic A.** Adjusting batch effects in microarray expression data using empirical Bayes methods. *Biostatistics.* 2007;8(1):118‑127. doi:10.1093/biostatistics/kxj037
9. **de Zwart JA, Ledden PJ, van Gelderen P, Bodurka J, Chu R, Duyn JH.** Signal‑to‑noise ratio and parallel imaging performance of a 16‑channel receive‑only brain coil array at 3.0 Tesla. *Magn Reson Med.* 2004;51(1):22‑26. doi:10.1002/mrm.10678
10. **de Zwart JA, Ledden PJ, Kellman P, van Gelderen P, Duyn JH.** Design of a SENSE‑optimized high‑sensitivity MRI receive coil for brain imaging. *Magn Reson Med.* 2002;47(6):1218‑1227. doi:10.1002/mrm.10169
11. **Kruger G, Glover GH.** Physiological noise in oxygenation‑sensitive magnetic resonance imaging. *Magn Reson Med.* 2001;46(4):631‑637. doi:10.1002/mrm.1246
12. **Kundu P, Inati SJ, Evans JW, Luh WM, Bandettini PA.** Differentiating BOLD and non‑BOLD signals in fMRI time series using multi‑echo EPI. *NeuroImage.* 2012;60(3):1759‑1770. doi:10.1016/j.neuroimage.2011.12.028
13. **Kundu P, Voon V, Balchandani P, Lombardi MV, Poser BA, Bandettini PA.** Multi‑echo fMRI: A review. *NeuroImage.* 2017;154:57‑70. doi:10.1016/j.neuroimage.2016.12.014
14. **Yamashita A, Yahata N, Itahashi T, et al.** Harmonization of resting‑state functional MRI data across multiple sites via matching of histogram and principal components. *Hum Brain Mapp.* 2019;40(6):1787‑1798. doi:10.1002/hbm.24490
15. **Pomponio R, Erus G, Habes M, et al.** Harmonization of large MRI datasets for the analysis of brain imaging patterns. *NeuroImage.* 2020;208:116450. doi:10.1016/j.neuroimage.2019.116450
16. **Zhou HH, Singh V, Johnson SC, Wahba G; Alzheimer's Disease Neuroimaging Initiative.** Statistical tests and identifiability conditions for pooling and analyzing multisite datasets. *Proc Natl Acad Sci USA.* 2018;115(7):1481‑1486. doi:10.1073/pnas.1717087115
17. **Kaza E, Klose U, Lotze M.** Comparison of a 32‑channel with a 12‑channel head coil: are there relevant improvements for functional imaging? *J Magn Reson Imaging.* 2011;34(3):552‑562. doi:10.1002/jmri.22644

---

## Appendix A: Recommended Acquisition Protocol Checklist

| Parameter | 32‑ch (default) | 20‑ch (if unavoidable) |
|:---|:---:|:---:|
| Prescan normalize | **ON** | **ON** (critical) |
| GRAPPA acceleration | R=2 or R=3 | **R=2** (do not use R=3) |
| Number of averages | 1 (fMRI), 1 (T1) | 1 (fMRI), **1.5–2 (T1)** |
| Slice acceleration factor | 2 | **1** (disable) |
| Bandwidth | As per protocol | Same as 32‑ch |
| Echo spacing | As per protocol | Same as 32‑ch |
| Multi‑echo EPI | If available | **If available** — strongly recommended |
| Coil element selection in DICOM | Recorded | Recorded and verified |
| Post‑scan QA | tSNR map + coil‑mode log | tSNR map + coil‑mode log + flagged if dorsal tSNR < 100 |

## Appendix B: Quick‑Reference Bias Magnitudes (20‑ch as % of 32‑ch)

| Metric | Dorsal PFC | OFC | Amygdala | Hippocampus | Temporal | Cerebellum |
|:---|---:|---:|---:|---:|---:|---:|
| SNR₀ (% of 32‑ch) | 45–60% | 90–95% | 90–95% | 80–90% | 95–100% | 95–100% |
| tSNR at 2.5 mm isotropic, R=2 (% of 32‑ch) | 50–65% | 90–95% | 90–95% | 80–90% | 95–100% | 90–95% |
| BOLD CNR at p=0.001 (% of 32‑ch) | 45–60% | 85–93% | 85–93% | 75–85% | 90–98% | 88–95% |
| FreeSurfer volume bias (within‑participant) | 2–4% | <1% | 1–2% | 1–3% | <1% | <1% |
| Resting‑state FC bias (z‑score shift) | 0.10–0.25 | <0.05 | <0.05 | 0.05–0.10 | <0.05 | <0.05 |

*Note: These are estimated ranges based on extrapolation from the literature. The actual lab‑specific values should be measured in the pilot validation (Tier II, Step B2).*
