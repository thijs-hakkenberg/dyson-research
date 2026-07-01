---
paper: "02-swarm-coordination-scaling"
version: "l"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-24"
recommendation: "Minor Revision"
---

# Peer Review: IEEE Transactions on Aerospace and Electronic Systems
**Manuscript ID:** [Version L]
**Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study

## Review Criteria

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This manuscript addresses a critical and rapidly emerging gap in the aerospace engineering literature: the "intermediate regime" of constellation management between current operational scales ($10^3$ nodes) and theoretical futuristic swarms ($10^6+$ nodes). While swarm robotics literature handles small scales and mean-field game theory handles infinite scales, the engineering specifics of the $10^4–10^5$ regime are under-studied.

The novelty lies in the rigorous application of Discrete Event Simulation (DES) with "full participation" (no statistical sampling of nodes) at this specific scale. Quantifying the specific protocol overhead ($\eta \approx 20.66\%$) and establishing the coordinator bandwidth requirements ($\approx 59$ kbps) provides concrete design guidelines for next-generation mega-constellations (e.g., Starlink Gen2/3, Kuiper). This is a highly significant contribution to the *IEEE TAES* readership.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The simulation framework appears robust. The authors are commended for using full-participation simulation rather than extrapolating from small samples, which captures tail behaviors in queueing that might otherwise be missed. The statistical treatment (30 Monte Carlo replications, bootstrap confidence intervals) is rigorous. The explicit definition of "offered load" vs. "delivered overhead" in the link availability analysis (Section IV-F) demonstrates a mature understanding of network engineering.

However, the abstraction of the physical layer (Table IV) is a double-edged sword. While necessary for simulating $10^5$ nodes, the assumption of a "1 kbps coordination channel" abstracts away the complexities of link acquisition, pointing, and Doppler shifts, which are non-trivial in optical inter-satellite links (OISLs). The authors acknowledge this, but the "zero-drop" claims must be read with the understanding that they apply to the message layer, not the physical link layer.

### 3. Validity & Logic
**Rating: 4 (Good)**

The conclusions are generally well-supported by the data. The comparison against "intentional bounds" (Centralized and Global Mesh) is logically sound for bracketing the problem. The derivation of the optimal cluster size ($k_c \approx 100$) and duty cycle (24-48h) is convincing and supported by the trade-off analysis in Figs. 6 and 7.

A minor logical weakness exists in the presentation of the "constant overhead" result. The authors present the constant $\eta$ scaling as a major DES finding. However, given that the hierarchy depth is fixed and the message model is strictly $O(N)$ while total bandwidth is also $O(N)$, a constant ratio is an analytical inevitability, not an emergent simulation property. The DES is valuable for quantifying the *coefficient* (20.66%) and verifying queue stability, but the *scaling trend* itself is mathematically pre-determined by the model inputs.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure is logical, moving from architecture definitions to simulation setup, results, and discussion. The distinction between "Baseline Telemetry" and "Protocol Overhead" (Section III-F) is crucial and explained clearly. Figures are well-referenced, and the "Baseline Interpretation Note" (Section I-C) preemptively answers many potential reviewer objections regarding the strawman nature of the baselines.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a transparent disclosure regarding the use of AI for ideation in the Acknowledgments, which aligns with emerging publication standards. No human subjects are involved. The research appears ethically sound.

### 6. Scope & Referencing
**Rating: 4 (Good)**

The paper fits perfectly within the scope of *IEEE TAES*. The references are a good mix of classical distributed systems theory (Lamport, Lynch), standard space engineering texts (SMAD), and recent mega-constellation literature.

One gap in referencing/scope is the lack of comparison to "Sectorized Mesh" or "Region-Based Gossip" protocols. The authors admit in Section V-C that Global Mesh is a worst-case bound. However, a practical decentralized alternative would be a mesh limited to a few hops. By omitting this, the paper compares a highly optimized Hierarchical model against a "strawman" decentralized model, potentially inflating the relative merit of the hierarchical approach.

---

## Major Issues

1.  **Lack of a Competitive Decentralized Baseline:**
    The paper compares the Hierarchical architecture against two "intentional bounds": Single-Server Centralized (which fails due to processing) and Global-State Mesh (which fails due to $O(N^2)$ bandwidth). This brackets the solution space but fails to compare Hierarchical against its true competitor: a **Sectorized Mesh** (or $k$-hop gossip).
    *   *Critique:* In Section V-C, the authors acknowledge that a sectorized mesh is a "promising intermediate architecture not simulated here." For a paper claiming to characterize coordination scaling, omitting the most viable alternative architecture weakens the conclusion that Hierarchical is the superior choice.
    *   *Requirement:* While a full new simulation sweep might be out of scope for a revision, the authors must provide a stronger analytical comparison or a limited simulation spot-check (e.g., at $N=10^4$) for a Sectorized Mesh to demonstrate where it falls relative to the Hierarchical curve.

2.  **Coordinator Bandwidth "Free Lunch" Assumption:**
    In Section III-F, the paper states: "we resolve this by assuming coordinators... use the combined coordination bandwidth of their cluster." While Section IV-G stress-tests this with parameter $\beta$, the baseline assumption that a coordinator node can instantly utilize 100x the bandwidth of a normal node (without a corresponding increase in antenna aperture, power, or spectrum allocation) is a significant hardware assumption.
    *   *Critique:* This implies a heterogeneous swarm (specialized coordinators) or a massive over-provisioning of transceivers on all nodes to support rotation.
    *   *Requirement:* The text needs to be more explicit that this architecture *requires* either heterogeneous hardware or significant over-provisioning. The "Power Budget Impact" section (IV-H) addresses power, but not the physical link dimension (aperture/spectrum) of this 100x throughput increase.

---

## Minor Issues

1.  **Abstract, Line 12:** "confirms the absence of scale-dependent second-order effects." This is a strong claim. It would be more precise to say "confirms the absence of queueing-induced non-linearities under the modeled conditions."
2.  **Section III-B-1 (Centralized Model):** The assumption of $c=1$ (single server) for the centralized baseline is extremely conservative. As noted in Table I, a cloud-based ground system could easily have $c=1000$. The paper acknowledges this, but the abstract and conclusion focus heavily on the failure of the centralized model at $10^4$ nodes. The text should clarify that the *primary* failure mode of centralized control is spectrum/propagation latency, not the processing queue (which is easily parallelizable).
3.  **Table IV (Abstraction Scope):** "Link acquisition and pointing" are listed as abstracted. For a hierarchical system involving coordinator handoffs (topology churn), link acquisition times (often seconds for OISL) could significantly impact the "Handoff Success" metrics in Table VI. A brief discussion of how link acquisition latency would degrade the effective duty cycle is warranted.
4.  **Fig. 5 (Latency):** The $10^6$-node curve is labeled as an "analytical extrapolation." This should be marked more clearly in the figure legend itself, not just the caption, to prevent readers from mistaking it for simulation data.
5.  **Equation 10 (Power Overhead):** The calculation $\Delta P_{avg} = 15W / 100 = 0.15W$ assumes the power cost is perfectly amortized. This is true for the *swarm average*, but the *thermal design* of the individual spacecraft must handle the peak load (20W vs 5W). The text should mention that thermal subsystems must be sized for the peak, not the average.

---

## Overall Recommendation
**Minor Revision**

**Justification:**
This is a high-quality paper that makes a substantive contribution to the field of large-scale space systems engineering. The methodology is sound, and the results are valuable. The primary criticism—the lack of a realistic decentralized competitor (Sectorized Mesh)—is acknowledged by the authors as future work. Given the depth of the current study on the Hierarchical aspect, asking for a full Sectorized Mesh simulation would be an unreasonable scope creep for this specific manuscript. However, the manuscript requires revisions to contextualize the "constant overhead" finding as an analytical expectation rather than a simulation discovery, and to more rigorously qualify the hardware implications of the coordinator bandwidth requirements.

---

## Constructive Suggestions

1.  **Refine the "Constant Overhead" Claim:** In the Abstract and Conclusion, rephrase the finding regarding the 20.66% overhead. Instead of framing it as a discovery of scaling behavior (which is analytically $O(1)$), frame it as a **quantification of the protocol coefficient**. The value of the DES is that it proves this coefficient holds up under jitter and failures, not that it exists.
2.  **Expand the Sectorized Mesh Analytical Comparison:** In Section V-C, expand the analytical estimate of Sectorized Mesh overhead. Provide a graph or a theoretical curve in Figure 8 (labeled "Analytical Sectorized Mesh") to show where it would likely sit between the Global Mesh and Hierarchical curves. This would satisfy the reader's need for a realistic comparison without requiring new simulation code.
3.  **Clarify "Offered Load" vs. "Link Budget":** In Section IV-G (Coordinator Bandwidth), explicitly link the 59 kbps requirement to link budget parameters. For example, "This implies that for a standard OISL link margin, the symbol rate must support at least 60 kbps of effective throughput after coding overhead."
4.  **Strengthen the Centralized Argument:** In the Introduction/Discussion, pivot the argument against Centralized control *away* from processing limits (which are solvable via cloud computing) and *toward* the spectrum bottleneck (uplink capacity) and latency. This makes the case for Hierarchical control much stronger and less susceptible to "just buy more servers" counter-arguments.