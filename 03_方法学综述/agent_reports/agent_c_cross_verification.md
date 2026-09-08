# Agent C — Cross-Verification Report

**Role:** Cross-Vendor MRI Physicist  
**Date:** 2026-07-20  
**Status:** Complete

---

## Section 5: Cross-Verification of Agent A (Scenario a — Lower-20 of 32ch)

### 5.1 SNR₀ Uncertainty Gap: ±10–15% vs ±40–60%

**Yes, the 4× gap is physically justified.** These are not the same problem in different magnitudes — they are different problems entirely.

**Sources of uncertainty in (a):**
- Only one variable changes: number of active elements (32 → 20)
- Element geometry is known and fixed (soccer-ball, same housing)
- Noise covariance Ψ is preserved for the 20 active elements (the off-diagonal terms involving inactive elements disappear, but the remaining 20×20 submatrix is identical)
- Same body coil → B₁⁺ is identical
- Same prescan normalize algorithm
- Same preamp noise figure
- Same cable losses

Agent A's uncertainty is dominated by: (1) boundary effects at the active/inactive element transition, (2) imperfect knowledge of how the adaptive coil combination weights change, (3) the ±2–3% measurement variation in the literature they cite. All remaining terms are known to within a small fraction.

**Sources of additional uncertainty in (c) that compound the 4× gap:**
| Source | Uncertainty Contribution |
|--------|------------------------|
| Unknown element geometry and size (AIR vs dStream vs conventional) | ±10–15% |
| Unknown element-to-brain distance (flexible AIR may be 2–5 mm closer; rigid Siemens 5–15 mm; Philips intermediate) | ±5–15% |
| Unknown preamp noise figure (Siemens ~0.3–0.5 dB; GE E-mode unknown; Philips ADC-in-coil eliminates cable loss) | ±5–10% |
| Unknown cable loss (copper coaxial ~0.5–1.5 dB; Philips optical = 0) | ±5–10% |
| Unknown body coil B₁⁺ difference | ±5–15% |
| Unknown noise covariance structure (different mutual inductance, different preamp decoupling) | ±5–15% |
| Unknown parallel imaging reconstruction (GRAPPA vs SENSE/ARC) | ±5–10% |
| Unknown prescan normalize algorithm | ±5–10% |

These are **not additive** because many affect the same term (e.g., element size and element distance both affect B₁⁻). But they are also **not perfectly correlated** — some can constructively sum, some can cancel. The ±40–60% range captures the outer envelope. It is conservative relative to the number of unknowns, not aggressive.

**Bottom line:** The gap between Agent A's ±10–15% and my ±40–60% is the correct representation of two fundamentally different scenarios, separated by the vendor boundary.

---

### 5.2 B₁⁺: Is Negligible Correct for Scenario (a)?

**I agree with Agent A: B₁⁺ < 2% is correct for scenario (a).**

Rationale: Scenario (a) uses the **same scanner** (same body coil, same bore environment) at both sites. The only difference is which receive elements are active. At 3T, receive arrays are receive-only; they do not affect the B₁⁺ transmit field. The loading change from activating 20 vs 32 elements changes the body coil's Q by an immeasurably small amount (<1%). The 2% upper bound Agent A assigns is generous.

**My 5–15% B₁⁺ claim for (c) is not contradictory** — it applies to a different physical situation where the body coil itself differs across vendors. Different body coils have different geometry, different tuning, different Q, and produce measurably different B₁⁺ maps at 3T. Agent A and I agree: same body coil → negligible B₁⁺; different body coil → significant B₁⁺.

---

### 5.3 Prescan Normalize: Same Algorithm at Both Sites for (a)?

**Confirmed: same algorithm.**

For scenario (a): both sites use Siemens scanners running Siemens ICE (Image Calculation Environment). The "Prescan Normalize" filter is the same compiled software module. It will behave differently on 20-element data vs 32-element data (because the coil sensitivity estimate changes), but the algorithm itself — the correction kernel, the regularization, the noise amplification model — is identical.

**This is a major advantage of (a) over (c).** In (c), Siemens "Prescan Normalize" is not GE "Prescan Normalize" is not Philips "CLEAR." Even if all three correct receive-field inhomogeneity, their noise propagation characteristics and edge-behavior differ.

---

### 5.4 Agent A's g-Factor Estimates: Trustworthy for Within-Siemens?

**I would trust Agent A's g-factor numbers for scenario (a).**

The soccer-ball geometry (Wiggins 2006) is the most well-characterized head coil geometry in the fMRI literature. Its noise covariance and sensitivity matrix have been measured, simulated, and validated in multiple independent publications (de Zwart 2004, Kaza 2011, Triantafyllou 2011). For scenario (a), the 20-element subset of this geometry retains the same overlap relationships among the active elements (except at the boundary).

**Caveat I would add:** The boundary between active and inactive elements creates a local region where mutual inductance to a neighboring inactive element exists but that neighbor's contribution is missing. This can increase g locally in the brain region closest to the transition zone. Agent A's range (R=2: g<1.10; R=3: g=1.15–1.50; R=4: g=1.50–2.20) appropriately captures this but may be slightly optimistic for the specific transition zone boundary. I would add a ±0.05 uncertainty to the upper end of their R=2 range.

**For (c), these numbers are not portable.** My report's recommendation to limit acceleration to R=2 with explicit g-factor measurement stands independently.

---

### 5.5 Harmonization Gap: "Optional" vs "Mandatory"

**This is the widest gap between any two agents, and it is justified.**

Agent A's "optional" is correct for (a) because:
- The hardware difference is quantitative (fewer active channels), not qualitative (different hardware)
- A single covariate (coil_mode) captures the effect because it's predominantly a global SNR scaling
- The bias is approximately additive in log-space → easy to model
- Site is NOT confounded with coil: both sites have the same 32ch coil, just operating in different modes

My "mandatory" for (c) is correct because:
- The bias is NOT additive — it includes multiplicative (scale) and spatially non-uniform components
- Site IS confounded with coil + scanner + vendor: a single `coil_mode` regressor captures the entire site difference, not just the coil component
- Different prescan normalize algorithms → different spatially varying intensity corrections
- Different parallel imaging algorithms → different noise propagation at the same R
- Different B₁⁺ → different BOLD sensitivity independent of SNR

**The gap exists because the scenarios are qualitatively different.** Agent A is not being optimistic; I am not being conservative. We are describing different problems.

---

### 5.6 Would a Reviewer Confuse (a) with (c)?

**If the manuscript is clear, no. If unclear, yes — and they would reject.**

Agent A's "moderate risk" assessment assumes the reviewer knows (or believes) that the same 32ch Siemens coil is used at both sites. If the methods section says:
- "Site A: Siemens Prisma 3T with 32ch head coil"
- "Site B: Siemens Prisma 3T with 20 of 32 channels active on the same 32ch head coil"

...a knowledgeable reviewer will recognize scenario (a) and the objection about cross-vendor confounds will not apply. The reviewer may still object to pooling different channel counts, but with a different line of argument (SNR, not vendor incompatibility).

**However, if the methods are ambiguous** (e.g., "Site B used a 20-channel configuration"), a reviewer could assume scenario (c). Under that assumption, the manuscript would be rejected because no cross-vendor controls are in place.

**Recommendation to CAD Lab:** Regardless of which scenario applies, the methods section must state explicitly: *"Both sites used the same Siemens 32-channel head coil (Siemens Healthineers, Erlangen). At the US site, the lower 20 of 32 elements were selected to match the channel count of the historical data acquired at the Korea site."* This single sentence prevents the scenario (a)→(c) misclassification.

---

### 5.7 What from Agent A Would I Adopt for (c)?

Agent A's "lighter touch" is specifically calibrated to the low uncertainty of (a). Most of it does not transfer. But three elements are worth adopting:

1. **tSNR as a continuous covariate (not a threshold).** Agent A uses region-specific tSNR as a covariate rather than a binary exclusion threshold. This is smart for (c) too — but with the important caveat that tSNR differences in (c) may reflect B₁⁺ + prescan normalize + reconstruction effects, not just SNR. The covariate must be applied per-region.

2. **"Some regions are less affected than others" as an analysis strategy.** Agent A correctly identifies that cerebellum, temporal cortex, and OFC are minimally affected in (a). For (c), the same statement is true but with different regions and wider confidence intervals. The strategy of focusing primary analysis on less-affected regions while including more-affected regions as secondary/sensitivity analyses is sound for any scenario.

3. **Keeping identical pulse sequence parameters.** Agent A emphasizes matching TR/TE/resolution/flip angle across sites. For (c), this is even more important — but (c) may need additional B₁⁺ calibration to achieve identical effective flip angles. Agent A's assumption that "same scanner → same flip angle" is correct; for (c), this must be empirically verified.

**What I emphatically cannot adopt:** Agent A's optional harmonization, Agent A's disregard for B₁⁺ effects, and Agent A's confidence in g-factor estimates. These depend on the within-Siemens assumption that (a) enjoys and (c) does not.

---

## Section 6: Cross-Verification of Agent B (Scenario b — Siemens 20ch Head/Neck)

### 6.1 Which Is Actually Worse: (b) Receive Penalty or (c) Combined Penalty?

**It depends on the brain region. For dorsal cortex: (b) is worse. For deep brain: (c) is worse.**

**Dorsal cortex (dlPFC, precuneus, superior parietal):**
| Component | (b) Penalty | (c) Penalty |
|-----------|:-----------:|:-----------:|
| Receive SNR₀ loss vs 32ch | 55–70% | 15–40% |
| Equivalent SNR₀ fraction | 30–45% of 32ch | 60–85% of 32ch |
| B₁⁺ penalty | 1–3% | 5–15% |
| Combined BOLD sensitivity (multiplicative) | ~29–44% of 32ch | ~50–80% of 32ch |

**(b) is worse for dorsal cortex** — the 55–70% receive-side loss in (b) dwarfs the additional B₁⁺ penalty in (c). The net BOLD sensitivity in (b) is roughly half that of (c) in this region.

**Deep brain (hippocampus, amygdala, thalamus):**
| Component | (b) Penalty | (c) Penalty |
|-----------|:-----------:|:-----------:|
| Receive SNR₀ loss vs 32ch | 10–25% | 15–40% |
| B₁⁺ penalty | 1–3% | 5–15% |
| Combined BOLD sensitivity | ~73–89% of 32ch | ~50–80% of 32ch |

**(c) may be worse for deep brain** because (b)'s receive penalty is much smaller in deep regions (the 20ch H/N still has good inferior coverage), while (c)'s receive penalty is uniform + the B₁⁺ penalty from a different body coil can be significant at depth.

**Key insight for CAD Lab:** If the primary ROI is dlPFC (anxiety/depression protocols), (b) is unambiguously more damaging to statistical power. But (c)'s B₁⁺ confound is an additional concern that (b) does not face — (b)'s SNR can be partially compensated by longer acquisition or more subjects; (c)'s B₁⁺ confound may introduce systematic bias that no amount of additional subjects can fix.

---

### 6.2 Is Schmitt 2021 Relevant to Scenario (b)?

**Yes, partially. A reviewer would accept it as directional evidence but would note the gap.**

**For the receive side:** Schmitt (2021) tested the exact same Siemens 20ch head/neck coil on the same scanner platform. This is the closest existing literature match for (b)'s receive physics. Agent B correctly cites it.

**For the prescan normalize interaction:** Schmitt's findings (region-dependent tSNR effects of prescan normalize × coil) are directly applicable because both the algorithm and the coils are Siemens.

**Why a reviewer would push back:**
- Schmitt compared 20ch H/N to **64ch**, not 32ch. The channel-count gap is 44 vs 12 channels. Agent B's commentary about "attenuated magnitude" is correct in direction but unsupported by dose-response data.
- Schmitt was **single-site, within-subject**. It validates that the 20ch H/N produces usable fMRI data, but it does **not** validate cross-site pooling.
- Schmitt's tasks (visual, motor, auditory) did not probe emotional/executive function (CAD Lab's primary domains).

**Verdict:** Schmitt 2021 provides a useful anchor for the receive-side physics and prescan normalize behavior, but **not** for the harmonization question. A reviewer would accept Schmitt as evidence that the coil works, not as evidence that two-site pooling is valid.

---

### 6.3 Is "Siemens Product with Published Data" a Defense for (b)?

**It is a partial defense. The same vendor-dependency criticism applies but with less force.**

Agent B's defense is that the 20ch H/N is a known Siemens product with known specifications. This helps because:
- The element geometry, decoupling approach, and preamplifier design are documented
- The noise covariance structure follows Siemens design principles (analog bundling, critical overlap)
- The body coil and transmit chain are Siemens → smaller B₁⁺ concern
- The reconstruction pipeline (GRAPPA) is the same

**Where the criticism still applies:**
- Different scanner model → different body coil tuning → some B₁⁺ uncertainty (Agent B's 1–3%, which I agree with)
- Different prescan normalize tuning (Siemens ICE version may differ between scanner models)
- Different housing → different loading and coil losses
- The detachable anterior component introduces a within-coil variability that Schmitt did not characterize

**Same criticism as (c)?** No — the criticism is less severe because scanner and coil are from the same vendor, sharing most of the receive and transmit chain design philosophy. But (b) cannot claim the hardware continuity that (a) can.

---

### 6.4 Traveling Subjects: 5–6 vs 8–10

**Both recommendations are defensible; the gap reflects scenario-specific risk, not disagreement.**

Agent B's 5–6 is appropriate for (b) because:
- The bias is better characterized (Schmitt 2021, known Siemens coil)
- Fewer unknown sources of variance → fewer subjects needed to estimate the site+coil effect
- The bias is predominantly in the receive chain → easier to estimate

My 8–10 for (c) is driven by:
1. **Larger expected effect size:** Requires more subjects to estimate with adequate precision
2. **More variance components:** B₁⁺, prescan normalize, reconstruction differences → more dimensions of variability
3. **No literature anchor:** Cannot borrow strength from prior measurements; must estimate everything from the traveling-subject sample
4. **Wider confidence intervals:** With fewer traveling subjects, the between-site bias estimate will be too imprecise to usefully constrain the harmonization model

**If I were analyzing (b) as a cross-vendor expert, what would I recommend?** Probably 6–8 — splitting the difference. Agent B's 5–6 is on the lower end of what I would consider acceptable for (b); I would be more comfortable at 7–8 for a NeuroImage-level submission. But Agent B's number is not unreasonable.

---

### 6.5 When Would Agent B's "ComBat Validation Recommended" Be Sufficient?

Agent B says "ComBat validation recommended" (implying validation alone may suffice). I say "ComBat/SMA mandatory, traveling subjects essential." Agent B's lighter approach would be sufficient under these conditions:

1. **Small SNR difference between coils in the primary ROI.** If the primary analysis targets regions where (b) vs (a) SNR loss is <15% (e.g., cerebellum, temporal cortex if using the lower ring), the ComBat validation may adequately address the remaining bias.

2. **Large per-site sample size (>80).** ComBat's empirical Bayes shrinkage performs better with larger samples. With >80 subjects per site, the estimated batch effect converges even without traveling subjects.

3. **Strong a priori biological signal.** If the expected effect size is large (d > 0.8), the added variance from the coil difference is a smaller fraction of the total. A sensitivity analysis showing the effect survives coil-mode adjustment would be more convincing.

4. **Clinical/translational journal target.** Lower-tier journals (e.g., *Translational Psychiatry*, *Frontiers*) are more tolerant of imperfect hardware matching if the clinical story is strong.

5. **The PI is willing to call the finding "exploratory."** If the manuscript presents the pooled analysis as hypothesis-generating with explicit caveats, the "validation recommended" bar may satisfy reviewers. If the claim is "these data can be pooled for confirmatory analysis," traveling subjects become essential.

**I would still recommend traveling subjects even under these conditions** — but I would acknowledge that (b) without traveling subjects is a closer call than (c) without traveling subjects.

---

### 6.6 Publishability Gap: (b)→(c) vs (a)→(b)

**The (b)→(c) gap is narrower than the (a)→(b) gap.**

| Transition | Risk Change | Key Differences |
|------------|:-----------:|----------------|
| (a) → (b) | Moderate → High | Continuity argument lost; SNR loss 15–20 pp worse; harmonization complexity increases significantly |
| (b) → (c) | High → Very High | Vendor independence lost; no literature precedent; parallel imaging may differ; B₁⁺ becomes material |

**Why (a)→(b) is wider:**
- (a) has a unique defense that neither (b) nor (c) can claim: "same physical hardware, fewer active channels." This is qualitative, not quantitative.
- Once that defense is lost (at (b)), the remaining step to (c) adds additional concerns but of a similar kind (more unknowns, bigger uncertainties, no literature anchor).
- (b) and (c) are on the same side of the fundamental divide — they both involve different physical coils. (a) is on the other side.

**Why (b)→(c) is non-trivial:**
Cross-vendor issues (different body coil, different PI algorithm, different prescan normalize) add dimensions of bias that (b) does not face. Even though the uncertainty magnitude increase is smaller than (a)→(b), the character of the uncertainty changes in (c) — some terms are no longer correctable by post-processing (e.g., B₁⁺ requires prospective correction).

---

### 6.7 Strongest Argument from Agent B That (c) Could Borrow

**Agent B's strongest argument is the existence of ANY published literature for the specific coil.**

For (b), Agent B leverages Schmitt 2021 — studies using the exact same coil model. For (c), we have no such direct match. But the **strategy** is borrowable:

1. **Identify the closest published study for the specific US coil vendor.** If the US coil is GE 20ch AIR → Ragan et al. 2021 (structural IQ, 16ch AIR vs 32ch conventional on GE). If Philips dStream → Panman et al. 2019 (8ch vs 32ch on Philips, giving directional evidence for vendor-specific channel-count effects).

2. **Use the published study to anchor the directional expectation, then use local data (traveling subjects, phantom) to quantify the magnitude.** The published study replaces the "wild guess" with an "educated guess bounded by local measurement."

3. **Frame the narrative: "Our US coil is [vendor] [model], which has been characterized in [citation]. We extend this characterization to the cross-vendor pooling context via [traveling subjects, phantom, ComBat validation]."**

This is weaker than Schmitt for (b) because no study directly tests the same coil across vendors. But it is stronger than saying "no evidence exists at all" — which is the current state of (c)'s defense.

---

## Section 7: Final Statement from Agent C

The three scenarios form a clear continuum of increasing uncertainty, harmonization burden, and publication risk. At one end, Scenario (a) — same Siemens 32ch coil, different channel counts — retains hardware continuity, making harmonization optional and reviewer defense straightforward. At the other end, Scenario (c) — entirely different vendor coil — removes every shared hardware assumption, demanding mandatory harmonization, traveling subjects, and empirical measurement of terms that cannot be estimated from literature. Scenario (b) sits in the middle: a different coil model but same vendor, with partial literature support but no hardware continuity.

**Robust findings across all scenarios:** The dorsal PFC and superior parietal cortex are consistently the most vulnerable regions, regardless of which coil substitution is involved. The cerebellum and temporal cortex are consistently the most robust. R=2 acceleration is acceptable in all scenarios (with vendor-specific caveats for (c)); R=3 or higher is inadvisable without direct g-factor measurement. B₁⁺ is a negligible confound only when the body coil is identical — as soon as the scanner vendor or model differs, B₁⁺ must be measured. **Fragile findings:** Any quantitative SNR₀ or g-factor estimate not supported by local measurement should be treated as approximate; in (c), they should be treated as placeholder values that must be replaced before analysis.

If the US coil turns out to be Scenario (c), CAD Lab should proceed **only** under three strict conditions: (1) traveling-subject funding is secured for a minimum of 8 subjects scanned on both coils; (2) the US coil vendor is identified and its specific parallel imaging and prescan normalize algorithms are documented and harmonizable (both sites must use the same acceleration algorithm if possible); (3) the primary analysis avoids regions where cross-vendor bias is largest (dorsal cortex) or includes a pre-registered sensitivity analysis that excludes the US site entirely. **Critical deal-breaker:** If the US site has fewer than 20 sessions or if group composition is confounded with site, pooling should be abandoned.

The single most cost-effective investment CAD Lab can make to rescue pooling in ANY scenario — including (a) — is to implement a **standardized traveling-subject protocol** and **phantom acquisition protocol** now, before data collection begins. A 10-minute phantom scan (the same ACR or NIST phantom at both sites, with both coils) provides the only vendor-independent anchor for coil SNR comparison. A 15-minute traveling-subject resting-state scan (same subject, both coils, both sites) provides the only direct measurement of the site+coil bias. These two acquisitions, costing perhaps $3,000–5,000 in scanner time and subject stipend, would reduce the uncertainty in ALL three scenarios by 50–75% and would provide the defense that scenario (c) most critically lacks. Without them, the cross-vendor objection — the most likely reviewer criticism across all scenarios — cannot be adequately answered.
