---
paper: "05-isru-water-extraction"
version: "b"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-18"
recommendation: "Unknown"
---

Here is a comprehensive peer review of the manuscript.

***

**Review of Manuscript:** *ISRU Water Extraction for Space Propellant: Monte Carlo Comparison of Asteroid and Lunar Sources at Industrial Scale (Version B)*
**Target Journal:** *Advances in Space Research*

### 1. Significance & Novelty
**Rating: 4 (Good)**
The paper addresses a critical gap in the ISRU literature: a direct, apples-to-apples economic comparison of lunar vs. asteroid water sources using a consistent stochastic framework. While individual economic models for lunar (Sowers) and asteroid (Sercel) mining exist, this work’s novelty lies in the unified Monte Carlo approach that propagates uncertainty across both architectures simultaneously. The integration of recent OSIRIS-REx findings (Bennu samples) adds timely significance.

### 2. Methodological Soundness
**Rating: 3 (Adequate)**
The move from exogenous transport cost estimates (Version A) to a physics-based derivation (Version B) is a significant improvement. However, the methodology still suffers from a "spherical cow" approach to orbital mechanics. Using a single $\Delta v$ value for NEAs ignores the synodic phasing constraints that dictate launch windows, which heavily impact the "working capital" argument. The financial modeling (NPV) is standard, but the exclusion of launch window wait times in the transit cost calculation is a methodological oversight.

### 3. Validity & Logic
**Rating: 3 (Adequate)**
The logic regarding the payload fraction advantage of Electric Propulsion (EP) is sound and mathematically valid. However, the comparison contains a bias: it assumes NEAs use high-efficiency EP while Lunar sources use low-efficiency chemical propulsion. While this reflects the current TRL landscape (high-thrust EP is hard in gravity wells), it is not a fundamental physical constraint. A fair architectural comparison should arguably consider lunar-derived LOX/LH2 tugs or lunar-based mass drivers, or at least acknowledge that the specific impulse gap is an architectural choice, not just a geographic one.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is well-written, concise, and logically organized. The progression from source characterization to cost modeling to stochastic results is clear. The distinction between deterministic and probabilistic results is well-handled.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors disclose the use of AI-assisted methodology and provide a link to open-source code, which is best practice. There are no apparent conflicts of interest or plagiarism concerns.

### 6. Scope & Referencing
**Rating: 4 (Good)**
The referencing is up-to-date, particularly regarding the Bennu sample analysis (Lauretta et al., 2024; Glavin et al., 2025). The scope is appropriate for *ASR*. However, the exclusion of Near-Earth Object (NEO) population statistics regarding spectral types is a minor gap; the paper relies heavily on Bennu as a proxy for all C-types.

---

### Major Issues

1.  **Asymmetric Propulsion Assumptions (The "Strawman" Lunar Architecture)**
    *   **Issue:** The model compares NEA transport using $I_{sp}=2,500$ s (Electric Propulsion) against Lunar transport using $I_{sp}=450$ s (Chemical). This drives the payload fraction difference (83% vs 57%) and is the primary factor in the NEA cost advantage.
    *   **Why it matters:** This is not a comparison of *sources* (Asteroid vs. Moon), but a comparison of *propulsion modalities*. A lunar architecture could utilize a high-$I_{sp}$ tug from L1/L2 to L4/L5, restricting chemical propulsion only to the ascent phase.
    *   **Remedy:** You must run a sensitivity case where the Lunar architecture utilizes a hybrid approach (Chemical ascent + EP transfer to L4/L5) to isolate the cost of the gravity well from the cost of the propulsion choice.

2.  **Oversimplification of NEA Accessibility (Synodic Phasing)**
    *   **Issue:** The model treats NEA accessibility as a continuous function of $\Delta v$ and transit time. In reality, low-$\Delta v$ NEAs have infrequent launch windows (often years apart).
    *   **Why it matters:** The "Working Capital" calculation (Eq. 5) accounts for transit time but ignores *wait time*. If a return window opens only every 3 years, the inventory holding cost is significantly higher than modeled.
    *   **Remedy:** Introduce a "Window Wait Time" parameter into the NEA Monte Carlo loop, or explicitly state that the model assumes a fleet large enough to stagger arrivals (which would increase Capital Expenditure, $K$).

3.  **Correlated Parameter Distributions**
    *   **Issue:** The Monte Carlo simulation treats parameters as independent. Specifically, `Water Fraction` and `Extraction Yield` are likely correlated (higher water content often implies different mineralogy, potentially easier or harder to process). Furthermore, `Delta-v` and `Trip Time` are physically coupled for low-thrust trajectories.
    *   **Why it matters:** Assuming independence may artificially narrow the variance of the cost distribution, making the "90.4% probability" claim overconfident.
    *   **Remedy:** If full covariance modeling is out of scope, add a disclaimer in the Discussion section about the independence assumption and how correlations might skew the tail risks.

### Minor Issues

1.  **Eq. 5 (Transit Cost):** The formula $c_{transit} = c_{water} \cdot [(1+r)^\tau - 1]$ applies the discount rate to the *delivered* cost. It should strictly apply to the *production* cost (COGS) tied up in transit, not the profit margin included in the final price. Please clarify if $c_{water}$ represents cost or price.
2.  **Phobos/Deimos Dismissal:** The dismissal of Phobos/Deimos solely on $\Delta v$ grounds ($\sim 6$ km/s) is abrupt. While likely uneconomical, they offer aerocapture opportunities at Earth return that NEAs do not. A sentence acknowledging aerocapture potential would be more rigorous.
3.  **Table 2 (Vehicle Parameters):** The NEA vehicle lifetime is listed as 10 trips with a 5.35-year transit. This implies a vehicle life of >50 years. This is technically unrealistic for current hardware. Please justify the replacement rate or lower the trip count.
4.  **Reference 1 (Hakkenberg 2026):** Citing an "in preparation" paper as the source of the methodology is weak. Please ensure the methodology is sufficiently described in *this* paper so it stands alone.

---

### Overall Recommendation
**Recommendation: Major Revision**

This manuscript presents a valuable, timely, and methodologically interesting comparison of ISRU sources. The integration of Bennu sample data is a strong selling point. However, the economic conclusion—that NEAs are cheaper 90% of the time—rests heavily on an asymmetric comparison of propulsion technologies (EP for asteroids, Chemical for Moon) rather than the intrinsic physical differences of the sources.

To be published in *Advances in Space Research*, the authors must disentangle the propulsion choice from the source location. The paper needs to demonstrate that NEAs remain competitive even if the Lunar architecture is optimized (e.g., using EP tugs for the cislunar leg). Additionally, the assumption of a >50-year vehicle lifespan for NEA miners needs immediate correction or robust justification.

### Constructive Suggestions

1.  **Add a "Hybrid Lunar" Case:** Rerun the Monte Carlo with a third architecture: Lunar Chemical Ascent to NRHO/L1, followed by EP transfer to L4. This will likely narrow the cost gap and provide a more honest assessment of the "Gravity Well Penalty."
2.  **Refine the NEA Fleet Model:** Adjust the vehicle lifetime constraints. If a round trip is ~11 years, a vehicle cannot perform 10 trips. It will likely perform 2 or 3. This will increase the amortization cost per kg significantly and may alter the winner.
3.  **Expand Sensitivity Analysis:** Include "Discount Rate" in the sensitivity ranking. Given the long time horizons (5+ years transit), the cost of capital should be a dominant driver, potentially outweighing extraction yield.
4.  **Clarify "Water":** Explicitly state if the cost is for "dirty water," "pure water," or "LOX/LH2." The energy costs for electrolysis are massive; if one source delivers ice and the other propellant, the comparison is invalid. (The text implies water, but "propellant" is used in the title).