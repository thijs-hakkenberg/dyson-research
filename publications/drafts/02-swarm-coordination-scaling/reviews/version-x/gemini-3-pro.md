---
paper: "02-swarm-coordination-scaling"
version: "x"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-24"
recommendation: "Minor Revision"
---

**Review for IEEE Transactions on Aerospace and Electronic Systems**

**Manuscript Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Manuscript Version:** X

---

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This manuscript addresses a critical and timely gap in the aerospace engineering literature: the transition from ground-controlled constellations (current state-of-the-art) to fully autonomous, massive-scale swarms ($10^5$ nodes). While the literature is saturated with small-scale swarm robotics studies ($N<100$) and high-level networking abstractions for mega-constellations, there is a distinct lack of rigorous, byte-level traffic analysis for the coordination layer of systems at this scale.

The novelty lies in the specific "middle-ground" analysis—moving beyond analytical $O(N)$ claims to quantify engineering realities like coordinator ingress saturation (50 kbps vs. 24 kbps) and the specific impact of correlated losses (Gilbert-Elliott model) on retransmission strategies. The quantification of the Age-of-Information (AoI) trade-off against bandwidth savings is a particularly valuable contribution for system architects. This work provides concrete design rules for future constellation management systems.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The use of a cycle-aggregated Discrete Event Simulation (DES) is an appropriate choice for simulating $10^5$ nodes, where packet-level simulation (e.g., NS-3) would be computationally prohibitive. The authors are transparent about the limitations of this approach, specifically the abstraction of the MAC layer.

The validation strategy is strong. Cross-checking the DES results against closed-form analytical predictions (Section IV-E) and validating the exception-based telemetry implementation (Section IV-F) builds confidence in the simulation logic.

However, a notable methodological limitation is the reliance on the MAC efficiency parameter $\gamma$ to capture all physical-layer contention effects. In a real shared-spectrum environment, $\gamma$ is not a static constant but a function of load. While the authors acknowledge this, the linearity of the assumption may understate the risk of congestion collapse in the "Sectorized Mesh" topology specifically.

### 3. Validity & Logic
**Rating: 5 (Excellent)**

The conclusions are logically derived from the data presented. The distinction between "offered load" and "delivered throughput" (Table X) is handled with rigorous precision, avoiding common pitfalls in network simulation reporting.

The use of reference baselines (Centralized and Global-State Mesh) as "intentional bounds" rather than strawman competitors is intellectually honest and helps frame the performance of the hierarchical architecture effectively. The analysis of the Gilbert-Elliott link model (Section IV-K) provides a crucial counter-narrative to the standard i.i.d. Bernoulli assumptions often found in similar literature, correctly identifying that intra-cycle retransmission is structurally ineffective against correlated bursts.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure is logical, moving from architecture definitions to simulation setup, then to results and sensitivity analyses. Tables are dense with information but clearly captioned. The explicit "Traffic Accounting" (Table V) is a model of clarity that allows for reproducibility.

The definitions of metrics (Section III-H) are precise. The distinction between the "1 kbps traffic budget" and the "physical link rate" is made early and reinforced, which is essential for preventing reader confusion regarding optical ISL capabilities.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a clear acknowledgment of AI-assisted ideation in the Acknowledgment section, complying with emerging standards for transparency. No human subjects are involved. The research appears ethically sound.

### 6. Scope & Referencing
**Rating: 5 (Excellent)**

The paper fits perfectly within the scope of *IEEE TAES*, bridging the gap between aerospace systems engineering and electronic communications. The references are comprehensive, covering foundational distributed systems theory (Lynch, Lamport), current constellation operations (Starlink, Kuiper), and relevant networking standards (DTN/BPv7).

---

### Major Issues

1.  **Justification of the 1 kbps Constraint:**
    The entire study is predicated on a "1 kbps per node" coordination budget. While the authors clarify this is a budget allocation from a larger optical ISL capacity, the justification for such a tight constraint in the era of multi-Gbps laser links is somewhat thin. Is this constraint driven by power, spectrum contention, processing limits, or a desire to reserve 99.9% of bandwidth for user data?
    *Critique:* If the optical links are 10 Gbps, a 100 kbps coordination overhead is still negligible. The paper should explicitly argue *why* minimizing coordination overhead to this degree is necessary. Is it to enable operation over low-rate backup RF links (e.g., TT&C S-band) if optical links fail? Clarifying this would strengthen the motivation.

2.  **MAC Layer Linearity Assumption:**
    In Section IV-I (Sensitivity Analysis) and throughout the discussion of the Sectorized Mesh, the paper relies on a linear efficiency factor $\gamma \in [0.7, 0.9]$.
    *Critique:* In random access protocols (implied by the "unscheduled" analysis), throughput does not scale linearly; it collapses after a certain load threshold (e.g., Slotted ALOHA at 36%). The DES models "drops" based on a byte budget, which mimics a queue, but it does not model the stochastic collisions of the medium access itself. The paper should more explicitly discuss the risk that the Sectorized Mesh, operating at ~67% utilization, might actually be in a collapse region if $\gamma$ drops below 0.6 due to hidden node problems or high contention, which the current linear model masks.

### Minor Issues

1.  **Extrapolation in Figure 3:**
    Figure 3 includes a curve for $10^6$ nodes. The caption notes this is an "analytical extrapolation." Given the rigor of the rest of the paper, mixing extrapolated data with simulated data in the same plot is slightly risky.
    *Suggestion:* Make the $10^6$ line dashed or distinctively different to visually separate simulation from projection, or move the extrapolation to the discussion text.

2.  **Collision Avoidance Rate Justification:**
    The rate of $10^{-4}$/node/s for collision avoidance messages is explained in the text as including "screening alerts." However, this is a high-impact parameter.
    *Suggestion:* A brief sentence in Section III-E citing the typical ratio of screening messages to actual maneuvers (e.g., from ESA or NASA CARA reports) would bolster this assumption.

3.  **Author Anonymity (Procedural):**
    The manuscript lists "Project Dyson Research Team" and a URL. If this review process is double-blind, this effectively unblinds the authors if the URL is active or if the team name is searchable. Ensure this complies with the specific submission policy of the journal edition.

4.  **Table X (Link Availability) Clarification:**
    In Table X, the "Offered" load for $p_{link}=0.5$ exceeds 100% when baseline is included. The footnote explains this well, but the table body could benefit from bolding or marking these "infeasible" cells to draw the reader's eye to the failure mode immediately.

---

### Overall Recommendation
**Minor Revision**

**Justification:**
This is a high-quality manuscript that makes a significant contribution to the field of autonomous spacecraft coordination. The methodology is sound, the validation is rigorous, and the writing is clear. The issues identified (justification of the bandwidth constraint and the linearity of the MAC abstraction) require textual clarification and perhaps a paragraph of expanded discussion, but do not require re-running the core simulations.

---

### Constructive Suggestions

1.  **Expand the "Why 1 kbps?" Motivation:** Add a paragraph in the Introduction or System Model explaining that while optical ISLs are fast, the coordination protocol must be robust enough to run on low-rate omnidirectional RF backup links (e.g., during tumbling or initial acquisition), hence the strict 1 kbps budget. This makes the constraint an engineering requirement for resilience, not just an arbitrary slice of a laser link.

2.  **Refine the MAC Discussion:** In Section V (Discussion), explicitly acknowledge that while the DES uses a linear $\gamma$, real-world RF contention at >60% utilization (as seen in the Sectorized Mesh) often leads to non-linear throughput degradation. This reinforces the argument for the Hierarchical topology (which keeps utilization lower) and TDMA (which avoids contention).

3.  **Visualize the "Design Envelope":** Figure 12 (Workload Comparison) is good, but a new figure or an overlay on Figure 8 showing the "Safe Operating Area" (bounded by Latency < X, Overhead < Y, and Link Margin > Z) would be a powerful visual summary for system engineers.

4.  **AoI Context:** In Section IV-G, explicitly link the 400s AoI to a specific orbital uncertainty metric (e.g., "At 400s staleness, the along-track error grows to $X$ km, which exceeds the typical conjunction screening volume of $Y$ km"). This connects the abstract metric to physical mission safety. (The text currently does this, but ensuring the numbers are derived from a cited propagator or standard approximation would strengthen it).