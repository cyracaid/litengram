# Agent C Report — Scenario (c): Other Vendor/Model (Non-Siemens 20ch)

## 1. Physics Analysis

### 1.1 Basic Architecture Differences

Scenario (c) removes every shared hardware assumption. The Korea site uses a Siemens 32-channel head coil (soccer-ball geometry, 32 circular overlapping elements, ~70–80 mm diameter, rigid helmet former). The US site uses a 20-channel coil from another vendor entirely. The most likely candidates are:

**GE 20-channel head coil (AIR™ or conventional):**
- GE's AIR coils use flexible, cloth-based element carriers with proprietary E-mode electronics — a fundamentally different preamplifier/decoupling approach than Siemens.
- The AIR elements are smaller, more numerous per unit area, and not rigidly positioned. Their relative positions change with head size and placement.
- GE uses ARC (Autocalibrating Reconstruction for Cartesian Imaging — a GRAPPA variant) or SENSE for parallel imaging, not standard GRAPPA.
- Published data (prototype 16ch AIR vs conventional 32ch on GE C3T): 32ch superior for SNR, structural sharpness, overall IQ; AIR performed between 8ch and 32ch conventional (Ragan et al. 2021, *AJNR*).
- Existing commercial GE head coils include fixed-geometry 8ch and 24–32ch arrays; the "20ch" could be an AIR-series product.

**Philips 20-channel head coil (dStream):**
- Philips dStream architecture is the most fundamentally different: signals are digitized **inside the coil** (ADC at each element) and transmitted optically — eliminating analog cable losses and crosstalk entirely.
- Philips uses SENSE (dS SENSE), not GRAPPA, for parallel imaging. This changes the noise propagation model for accelerated acquisitions.
- The 20ch dStream head coil likely has different element sizing and distribution than either Siemens or GE.
- Philips also uses SmartSelect — automatic coil/element selection based on FOV, which may not activate all 20 elements identically across sessions.

**Physical parameters that differ systematically across vendors:**

| Parameter | Siemens | GE | Philips |
|-----------|---------|-----|---------|
| Architecture | Analog RF chain | Analog + E-mode preamp | **Fully digital (ADC in coil)** |
| Cable type | Copper coaxial (~10–20m) | Copper coaxial | **Optical fiber** |
| Cable loss | Present (signal attenuation) | Present | **Negligible** |
| Crosstalk | Analog bundling unavoidable | Analog bundling | **Eliminated by digital transport** |
| Noise figure dominated by | Preamplifier + cable loss | E-mode electronics | ADC quantization + preamp |
| Parallel imaging | GRAPPA (k-space) | ARC / SENSE | dS SENSE (image-space) |
| Body coil (transmit) | Siemens body coil | GE body coil | Philips body coil |
| Element geometry | Rigid, fixed overlap | Flexible, variable overlap | Rigid, vendor-specific |
| Prescan normalize | Siemens ICE filter | GE Prescan Normalize | Philips CLEAR / PNS |

### 1.2 SNR₀ — Cannot Be Estimated from Siemens Literature

The SNR expression SNR(x) ∝ √N · B₁⁻(x) / √R_total is vendor-dependent through every term:

- **√N scaling**: 32 → 20 is a 20.9% reduction in √N, so if element geometry were identical, SNR₀ would drop by ~21% from count alone. **But element geometry is NOT identical.** A GE 20ch AIR coil with flexible elements that conform more closely to the head could partially offset this. A Philips 20ch with in-coil digitization (lower noise figure) could also offset it. The actual SNR₀ could range from **60–85% of the Siemens 32ch value**, depending on implementation — and this range is **not constrained by any published direct comparison**.

- **Noise figure differences**: The preamplifier decoupling network, cable loss, and ADC noise figure differ. Siemens uses a tuned preamp with ~0.3–0.5 dB noise figure at the element. GE's AIR E-mode electronics claim reduced current noise and improved linearity. Philips dStream eliminates ~10–20m of analog cable loss (~0.5–1.5 dB depending on cable type). **The net SNR₀ impact of these differences is unquantified for the 20ch case** and cannot be reliably estimated from existing literature.

- **Element proximity**: A flexible GE AIR coil may sit 2–5 mm closer to the scalp than a rigid Siemens helmet (which has ~5–15 mm standoff). This proximity gain could offset 10–20% of the SNR loss from fewer elements for cortical regions. Deep brain SNR would not benefit.

**Bottom line for SNR₀:** Unlike Scenario (a) where we could estimate with reasonable confidence (40–55% dorsal loss), for Scenario (c) the **uncertainty range is 2–3× wider** with no direct literature anchor.

### 1.3 g-Factor — Entirely Vendor-Dependent

The g-factor depends on the sensitivity matrix S and noise covariance Ψ:

g(R) = sqrt[ ((S^H Ψ^{-1} S)^{-1})_{jj} · (S^H Ψ^{-1} S)_{jj} ]

In Scenario (c), **both S and Ψ are completely different**:

- **S (sensitivity profiles)**: Determined by element geometry, size, and overlap. Siemens soccer-ball geometry produces a specific pattern of sensitivity overlap optimized for GRAPPA. GE's element arrangement (different diameters, different spacing, possibly non-overlapping in the AIR design since E-mode reduces the need for critical overlap) produces a fundamentally different S matrix. Philips dStream elements may have different dimensions and spacing.

- **Ψ (noise covariance)**: Determined by mutual inductance between elements, preamp noise correlation, and cable coupling. With different preamp design, different cable routing, and (for Philips) optical digital transmission that eliminates cable cross-talk, Ψ is completely restructured.

- **Empirical data point**: Ragan et al. (2021) measured g-factors for a prototype 16ch GE AIR coil vs conventional 32ch on the same GE scanner. At R=4, median g was ~1.2 (AIR 16ch) vs ~1.1 (conventional 32ch), but **maximum g for the AIR coil reached ~5.0** in small focal regions (vs ~1.5 for 32ch). This is critical: **vendor-specific element placement can create localized g-factor "hot spots"** that would unpredictably affect specific brain regions.

**Consequences for GRAPPA/SENSE protocol:**
- At R=2: most vendors' coils show acceptable g < 1.15 throughout. GRAPPA R=2 is likely safe regardless of vendor.
- At R=3: g penalty becomes vendor- and region-dependent. Cannot assume it is acceptable.
- At R=4: the 16ch AIR data shows median g ~1.2 but maximum g ~5.0 — effectively unusable if the hot spot falls on a primary ROI.

**Recommendation:** For Scenario (c), **limit acceleration to R=2** regardless of vendor, unless the exact g-factor maps are empirically measured for the specific US coil on its scanner.

### 1.4 B₁⁺ Effects — Not Negligible in Cross-Vendor Scenario

In Scenario (a) (within-Siemens, same body coil), B₁⁺ effects are <2% and negligible. **In Scenario (c), this assumption fails.**

- The **body coil** is a separate hardware component and differs by vendor in geometry, length, tuning, and Q.
- Siemens Prisma body coil: 70 cm bore, birdcage design, 2-port CP mode.
- GE MR750 body coil: 70 cm bore, different birdcage geometry, different tuning.
- Philips Ingenia body coil: same-bore designs, but with dStream integration affecting loading.
- Different body coils produce **measurably different B₁⁺ maps at 3T** — especially at the superior-inferior edges of the FOV (vertex and neck). Differences of **5–15% in flip angle** have been reported across vendors at 3T in the inferior cerebellum and frontal pole (Chung et al. 2010, *JMRI*; Bijnsdorp et al. 2019, *MRM*).

**This changes the interpretation**: B₁⁺ is no longer a negligible confound. A 5–10% B₁⁺ difference alone can alter BOLD sensitivity by 3–8% even if coil SNR were identical. In Scenario (c), B₁⁺ differences are **additive** to receive-side SNR differences.

### 1.5 Prescan Normalize — Vendor- and Implementation-Specific

The prescan normalize filter exists on all vendors but with different algorithms:

- **Siemens**: "Prescan Normalize" — applies a sensitivity map correction based on coil reference scan. Reduces intensity inhomogeneity. Interacts with coil choice region-dependently (Schmitt 2021).
- **GE**: "Prescan Normalize" (different algorithm) — applies a B₁ correction derived from a calibration scan. May use ASSET/ARC calibration data.
- **Philips**: "CLEAR" (Coil rEduction of ARtifacts) or "PNS" (Prescan Normalize) — uses SENSE reference scans for homogeneity correction.

Each has different behavior for: (1) intensity correction at brain edges, (2) noise amplification in corrected regions, (3) interaction with parallel imaging. **The Schmitt & Rieger (2021) prescan normalize × coil findings are Siemens-specific and do NOT generalize to GE or Philips.** The specific interaction pattern (auditory/thalamus benefits, visual/motor penalties) may differ entirely.

**Critical implication:** You cannot use "prescan normalize ON for both sites" as a harmonization guarantee. Even if both sites enable the filter, they use **different algorithms** that may introduce different spatial biases.

### 1.6 Noise Covariance — Completely Different Architecture

- Siemens 32ch: 32 element noise covariance matrix measured at the analog receiver. Mutual inductance minimized by geometric overlap + preamp decoupling.
- GE 20ch AIR: 20 elements, E-mode decoupling that does not require geometric critical overlap. The noise covariance structure is fundamentally different — potentially lower off-diagonal terms because elements need not be critically overlapped.
- Philips 20ch dStream: 20 elements, ADC in coil, optical fiber transport. **Noise from cable coupling is eliminated.** The noise covariance is determined almost entirely by mutual inductance between elements plus sample noise, without cable noise contribution.

**The noise covariance Ψ is the least portable quantity across vendors.** Even if two coils had identical element positions (impossible), their Ψ matrices would differ due to preamp and cable differences.

---

## 2. Harmonization & Statistical Analysis

### 2.1 This Is the Hardest Case — No Single-Vendor Literature Applies

Every published coil comparison study (Kaza 2011, Panman 2019, Schmitt 2021, Paolini 2015) compares coils **within the same vendor**. Scenario (c) has **no direct literature precedent**. The following claims are *all* [No Direct Evidence] or at best weak [Inference]:

- SNR₀ ratio between coils in any brain region
- tSNR difference magnitude and spatial pattern
- g-factor penalty at any acceleration factor
- Prescan normalize interaction direction
- FC bias pattern and magnitude
- Structural segmentation bias (Panman was Philips 8ch vs 32ch — provides directional insight but applies to a different comparison)

### 2.2 ComBat/SMA Is the ONLY Option, Not a Choice

In Scenario (a), harmonization was optional — acquisition control + covariates + sensitivity analysis was defensible. In Scenario (b), harmonization was recommended. **In Scenario (c), harmonization is mandatory.**

**Why covariates alone fail in Scenario (c):**
- Site + coil + scanner are perfectly confounded. A binary `coil_mode` regressor captures the **entire site difference**, not just the coil component. This removes biological between-site variance along with hardware variance.
- Region-specific tSNR as covariate is still useful but cannot correct for different B₁⁺-induced flip-angle effects on BOLD sensitivity, or for different noise covariance structure affecting connectivity estimates.
- The bias is **not additive** — it includes multiplicative (scale) and possibly non-linear components from different parallel imaging algorithms, different reconstruction pipelines, and different intensity normalization approaches.

**ComBat/SMA requirements specific to Scenario (c):**
- **Sufficient scans per batch**: ComBat's empirical Bayes shrinkage requires ~20+ scans per batch for stable parameter estimates. If the US site has <20 sessions, ComBat estimates will be unreliable. With <10 sessions, ComBat can actually **increase** bias rather than reduce it.
- **SMA (Wang 2023)**: Requires distributional matching across sites. For Scenario (c), the distributional shift includes both coil effects AND scanner effects AND site effects. SMA's distribution-matching works best when the shift is mainly additive; large multiplicative shifts (likely here) may require ComBat-GAM or tailored approaches.
- **Both methods assume batch effects are independent of biological variables** — a critical assumption that fails if clinical group composition differs between sites.

### 2.3 Traveling Subjects Become ESSENTIAL, Not Optional

In Scenario (a), traveling subjects were "nice to have" (aspirational Tier III). In Scenario (c), they are **mandatory for any publishable result**.

**The traveling-subject design must address:**
1. **Within-scanner, within-subject, same-vendor test-retest** (Korea site, Siemens 32ch twice): measures intrinsic scanner/test-retest variance for that site.
2. **Within-scanner, within-subject, cross-vendor** (US site, US 20ch twice): same for US site.
3. **Cross-scanner, cross-vendor, same-subject** (subject scanned at both sites): the actual site+scanner+coil bias.

Yamashita et al. (2019) recommends **minimum 5–6 traveling subjects** for multi-site harmonization. For Scenario (c), given the additional complexity (different vendor, different coil, different parallel imaging), **I would recommend 8–10 traveling subjects minimum** to estimate the site×subject interaction variance.

### 2.4 Additional MF Items That Scenario (c) Would Require

The Must Fix (MF) items from the Integration Report were written primarily for Scenarios (a) and (b). Scenario (c) requires **additional MF items**:

| ID | Issue | Specific to Scenario (c) |
|----|-------|-------------------------|
| **MF12** | **B₁⁺ mapping required**: Declare B₁⁺ negligible is wrong for cross-vendor. Must measure B₁⁺ maps at both sites. | Cross-vendor body coil differences are 5–15%, not <2%. |
| **MF13** | **Parallel imaging protocol harmonization**: GRAPPA→SENSE algorithm difference. Must align on SENSE (if both support) or accept different noise propagation. | Cannot assume same R factor gives same g-penalty. |
| **MF14** | **Intensity normalization across vendors**: Different reconstruction pipelines produce different intensity scaling. Must verify unified intensity scaling works across vendor-native reconstructions. | Standard SPM "grand mean scaling" or FSL `-ing 10000` may not suffice across vendors. |
| **MF15** | **Prescan normalize algorithm documentation**: Document exact algorithm used at each site. Do not assume "prescan normalize ON" means the same correction at both sites. | Siemens: ICE filter; GE: PNS; Philips: CLEAR. Three different algorithms. |
| **MF16** | **Minimum traveling-subject sample size**: Explicitly state required n with power justification (recommend 8–10). | Scenario (a): Tier III optional. Scenario (c): mandatory. |
| **MF17** | **Vendor-specific g-factor measurement**: Measure g-factor maps for both coils at their respective R factors. | R=2 may be acceptable; R=3 may not be; depends on vendor. |

---

## 3. Publishability Assessment

### 3.1 Risk Level: VERY HIGH — Highest of All Three Scenarios

**Publication viability by journal tier:**

| Journal Tier | Verdict | Rationale |
|-------------|---------|-----------|
| *NeuroImage* / *HBM* | **Major Revision → Likely Reject** without traveling subjects | Reviewer will demand direct evidence that cross-vendor effects are controlled. "No published study validates this" is a fatal gap unless filled by local data. |
| *Biological Psychiatry* | **Major Revision → Possible Accept** with strong clinical rationale | Clinical focus shifts weight toward statistical control and away from physics perfection. But the clinical reviewer will be concerned about systematic measurement error mimicking group differences. |
| *Translational Psychiatry* | **Moderate Revision → Possible Accept** | Lower bar for physics rigor; clinical relevance primary. Requires at minimum ComBat + sensitivity analysis + strong limitation statement. |
| *Frontiers in Neuroscience* | **Minor Revision** with strong safeguards | More tolerant of measurement heterogeneity. |

### 3.2 Key Reviewer Criticism Specific to Scenario (c)

**Criticism 1: "You have no idea what your SNR₀ difference actually is."**
This is fatal without local measurement. The existing literature (Panman, Kaza, Schmitt) uses same-vendor comparisons. No published study provides SNR₀ or tSNR ratio for Siemens 32ch vs GE 20ch (or Philips 20ch). The reviewer will correctly point out that all numerical estimates in the revised review are invalid for this scenario.

**Required response:** Provide empirical SNR₀ ratio maps and tSNR maps from traveling subjects scanned at both sites. Acknowledging "we don't know" without supplying local evidence will not satisfy reviewers.

**Criticism 2: "Your prescan normalize filter is not the same thing at both sites."**
The reviewer with MRI hardware expertise will know that Siemens "Prescan Normalize," GE "Prescan Normalize," and Philips "CLEAR" are different algorithms with different noise propagation characteristics. The Schmitt (2021) prescan normalize findings are Siemens-specific and do not apply.

**Required response:** Document each vendor's algorithm explicitly. If possible, acquire traveling-subject data both with and without the filter at each site.

**Criticism 3: "You are pooling across fundamentally different parallel imaging architectures."**
GRAPPA (Siemens) and SENSE (Philips/GE) propagate noise differently. GRAPPA noise is correlated in k-space; SENSE noise is spatially varying in image space. Even at the same R factor, the spatial noise distribution differs. Connectivity estimates based on correlation metrics (Pearson r) will be affected differently.

**Required response:** Standardize on either GRAPPA or SENSE if both sites' scanners support both. If not, the method difference must be explicitly modeled.

**Criticism 4: "Your group difference could be a body-coil B₁⁺ difference."**
The clinical reviewer may not raise this, but the methods reviewer will. If the US site has lower B₁⁺ in the dlPFC (common cross-vendor difference), the apparent "group difference in dlPFC activation" could be a 5–10% flip-angle effect producing a 3–8% BOLD sensitivity difference.

**Required response:** B₁⁺ maps from both sites. Demonstrate that B₁⁺ differences do not coincide with the reported group effects.

### 3.3 When Should the PI Just Say "No" to Pooling?

Pooling is **not recommended** (and the PI should consider abandoning pooling) if **any** of the following apply:

1. **No traveling subjects available** (most common case in clinical research). Without traveling subjects, the bias cannot be measured and the harmonization methods cannot be validated. The analysis would rest entirely on untestable assumptions.

2. **Primary ROIs include dorsal PFC, superior parietal, or occipital cortex**, AND the US coil is a GE 20ch AIR or similar flexible array. The combination of: (a) lower element count, (b) vendor-specific noise figure differences, and (c) variable element positioning from the flexible array, makes the expected SNR loss too high and too unpredictable for reliable BOLD detection.

3. **Unequal group composition across sites** (e.g., Korea site has 80% controls, US site has 80% patients). Site+coil is then confounded with clinical group, and any harmonization method risks removing biological signal or failing to remove hardware bias.

4. **<15 sessions at the US site.** ComBat batch parameter estimates require ~20 scans for stability. With <15, the harmonization may perform worse than no correction.

5. **Longitudinal design with unbalanced coil transitions.** If all post-treatment sessions are at the US site (or all pre-treatment at Korea), the coil change is inseparable from treatment effect.

**In practice, for a typical CAD Lab scenario** (2 sites, 50–80 subjects/site, no travel fund, anxiety/depression protocol with dlPFC and amygdala ROIs), **I would advise against pooling** unless traveling-subject funding is secured. The risk of an irreproducible finding is too high.

---

## 4. Comparison to Scenarios (a) and (b)

### 4.1 Differences TABLE

| Dimension | Scenario (a): Same Siemens, lower-20 | Scenario (b): Different Siemens models | Scenario (c): Different vendor entirely |
|-----------|---------------------------------------|----------------------------------------|----------------------------------------|
| **Shared hardware** | Same scanner, same body coil, same coil model, same preamp | Different scanner model, different coil model | Nothing shared |
| **SNR₀ uncertainty** | ±10–15% (constrained by known geometry) | ±20–30% (different coil design, same vendor) | ±40–60% (different vendor, technology, geometry) |
| **B₁⁺ concern** | <2% (negligible) | <5% (small) | 5–15% (significant) |
| **Prescan normalize** | Same algorithm | Same algorithm family, different tuning | Different algorithm entirely |
| **Parallel imaging** | Same (GRAPPA) | Same (GRAPPA) | Different (GRAPPA vs SENSE) |
| **Noise covariance** | Preserved (same elements) | Related (same vendor design philosophy) | Unrelated (different architecture) |
| **Literature anchor** | Kaza 2011 (12v32), Schmitt 2021 (20v64) | Kaza 2011, Schmitt 2021 | **None** (no Siemens-vs-other 20ch fMRI study exists) |
| **Harmonization** | Optional (covariates sufficient) | Recommended (ComBat/SMA helpful) | **Mandatory** (ComBat/SMA required, traveling subjects essential) |
| **Publishability** | Moderate risk | High risk | **Very high risk** |
| **Overall confidence** | Moderate | Low | **Very low** |

### 4.2 Which MF Items Are Most Critical for Scenario (c)?

From the Integration Report MF list:

| MF ID | Description | Criticality for (c) | Rationale |
|-------|-------------|:-------------------:|-----------|
| MF1 | B₁⁺ caveat | **CRITICAL** | Amplified from <2% to 5–15% error |
| MF2 | Coil type determination | **CRITICAL** | Gating issue: vendor identity determines everything |
| MF3 | g-factor estimates | **CRITICAL** | Cannot be estimated from literature; must be measured |
| MF4 | tSNR collider bias | High | Still applies but less relevant than larger cross-vendor issues |
| MF5 | 2024–2026 literature | High | Cross-vendor harmonization is rapidly evolving |
| MF6 | Covariate modeling | High | In (c), no single model suffices |
| MF7 | Power analysis | **CRITICAL** | Must account for traveling-subject costs and potential exclusion |
| MF8 | ComBat validation | **CRITICAL** | ComBat untested on cross-vendor coil differences |
| MF9 | ROI cherry-picking | High | Pre-registration even more important here |
| MF10 | Longitudinal plan | High | Cross-vendor longitudinal is worst-case scenario |
| MF11 | Decision boundaries | **CRITICAL** | Need explicit "stop pooling" thresholds |

### 4.3 Additional MF Items Unique to Scenario (c)

As listed in Section 2.4: **MF12 through MF17** are *additional* requirements specific to this scenario that do not appear in the Integration Report (which was written with Scenarios a/b primarily in mind).

---

## 5. Cross-Verification of Agent A

*[To be completed after receiving Agent A's analysis]*

## 6. Cross-Verification of Agent B

*[To be completed after receiving Agent B's analysis]*

---

## 7. Final Consensus Statement

*[To be completed after reviewing Agents A and B]*
