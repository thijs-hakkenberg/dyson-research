---
paper: "02-swarm-coordination-scaling"
version: "m"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-24"
recommendation: "Minor Revision"
---

Here is the peer review for the manuscript "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study" (Version M), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## Review Criteria

### 1. Significance & Novelty
**Rating: 4 (Good)**

The manuscript addresses a critical and timely gap in the aerospace literature: the "intermediate regime" of coordination scaling between current constellations ($10^3$ nodes) and future mega-swarms ($10^6$ nodes). While swarm robotics and constellation management are well-studied individually, the specific focus on the transition point where centralized control breaks down is highly relevant to operators like Starlink, Kuiper, and future defense architectures.

The novelty lies in the rigorous quantitative comparison of hierarchical architectures against specific reference bounds using a full-participation Discrete Event Simulation (DES) up to $10^5$ nodes. The explicit quantification of the "protocol coefficient" ($\eta \approx 20.66\%$) and the stress-testing of coordinator bandwidth provide actionable engineering data. However, the significance is slightly tempered by the reliance on somewhat idealized physical layer assumptions (abstracting MAC contention), which means the results represent an upper-bound on performance rather than a field-ready prediction.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology is generally robust. The authors employ a Discrete Event Simulation (DES) with full participation (no sampling), which is computationally impressive for $N=10^5$. The use of 30 Monte Carlo replications to bound stochastic variance is appropriate, and the validation against analytical models (Pollaczek–Khinchine for M/D/1) builds confidence. The clear distinction between "baseline telemetry" and "protocol overhead" is a strong methodological choice that aids clarity.

However, there is a notable tension in the methodology regarding the "Reference Baselines." The authors model the centralized baseline as a single-server ($c=1$) queue. While they acknowledge this is a "worst-case bound" and provide a sensitivity table for $M/D/c$, the comparison in Figure 2 (where the centralized curve explodes at $10^4$) feels somewhat like a straw man. A modern ground system for 10,000 satellites would inherently be distributed. The paper would be methodologically stronger if the baseline comparison used a realistic $c$ value (e.g., $c=100$) to show where the *spectrum* or *latency* limits bind, rather than the processing limit.

### 3. Validity & Logic
**Rating: 3 (Adequate)**

The internal logic of the simulation is sound, and the conclusions regarding the $O(1)$ overhead scaling of hierarchical systems follow directly from the architectural definitions. The analysis of coordinator duty cycles and the power-variance trade-off is logical and well-supported by the data.

The primary validity concern lies in the abstraction of the physical layer (Table III). The conclusion that there are "no queueing-induced nonlinearities" is valid *within the message-passing abstraction*, but the paper risks overstating this as a system-level truth. In reality, TDMA slot contention, link acquisition delays, and Doppler shifts create nonlinearities that the current model explicitly abstracts away. The authors acknowledge this in the "Limitations" section, but the abstract and conclusion are perhaps too confident in the "constant overhead" claim without reiterating the "offered load" qualification.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure is logical, moving from problem definition to simulation framework, results, and discussion. The distinction between "delivered" and "offered" load in the link availability section is crucial and well-explained.

The tables are highly effective, particularly Table I (M/D/c sensitivity) and Table VII (Link Availability). The figures are clear, with appropriate confidence intervals shown. The definitions of metrics in Section III-H are precise, preventing ambiguity regarding what constitutes "overhead."

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a transparent Acknowledgment section detailing the use of AI tools (Claude 4.6, Gemini 3 Pro, GPT-5.2) for ideation, citing a companion methodology paper. This level of disclosure sets a high standard for transparency. There are no apparent conflicts of interest or ethical concerns regarding the research content.

### 6. Scope & Referencing
**Rating: 4 (Good)**

The paper fits well within the scope of *IEEE TAES*, bridging the gap between electronic systems (communications) and aerospace operations. The referencing is comprehensive, covering classical distributed systems theory (Lamport, Lynch), current commercial operations (Starlink, Kuiper), and swarm robotics (Dorigo, Brambilla). The inclusion of recent CCSDS standards (BPv7) and specific military programs (DARPA OFFSET) demonstrates a good grasp of the current landscape.

---

## Major Issues

1.  **The "Straw Man" Centralized Baseline:**
    In Section III-B-1 and Figure 2, the centralized baseline is modeled as a single-server queue ($c=1$), causing it to fail at $N=10^4$ due to processing latency. As the authors admit in Table I, real systems use parallel processing ($c \gg 1$). By forcing the centralized system to fail on *processing* grounds, the paper obscures the more interesting comparison: when does the centralized system fail due to *bandwidth* or *speed-of-light latency*?
    *   *Requirement:* The authors should ideally plot a "Realistic Centralized" curve in Figure 2 (e.g., using $c=100$) alongside the "Single-Server Bound." This would likely show the centralized system surviving processing loads at $10^5$, thereby highlighting that the *true* advantage of the hierarchy is latency reduction and spectrum reuse, not just CPU offloading.

2.  **Physical Layer Abstraction vs. "Constant Overhead" Claim:**
    The abstract states the DES "confirms the absence of queueing-induced nonlinearities." This is technically true for the *message queue*, but potentially misleading for the *system*. In a real TDMA system with $k_c=100$, guard times and synchronization overhead often scale non-linearly as the number of slots increases.
    *   *Requirement:* The abstract and conclusion must qualify the "constant overhead" and "no nonlinearities" claims. They should explicitly state these are "message-layer" findings and that MAC-layer inefficiencies are treated as a linear efficiency factor ($\gamma$).

---

## Minor Issues

1.  **Section III-F (Coordinator Bandwidth):** The assumption that "radio subsystem is sized for the coordinator role on every node" (homogeneity) is a significant hardware driver. The paper mentions this briefly, but it deserves more emphasis. If every node needs a 59 kbps receiver (vs 1 kbps transmitter), that impacts the cost model of the swarm significantly.
2.  **Table IV (Topology Comparison):** The "Failure Mode" for Centralized is listed as "Single point (99.0%)." This seems arbitrary compared to the calculated values for other rows. Is this 99.0% derived from the simulation or an assumption? Please clarify in the table footer or text.
3.  **Figure 4 (Failure Resilience):** The x-axis range or the specific degradation curve for the hierarchical topology seems to lack a "cliff." Does the hierarchical system eventually collapse if enough coordinators fail simultaneously before reelection? The current graph suggests a very smooth degradation, which implies highly efficient reelection. A brief sentence explaining the reelection latency assumption in the context of this figure would be helpful.
4.  **Equation 5 (Hierarchy):** The equation lists $N/(k_c \cdot k_r)$ for the regional level. Ensure the text clearly defines if $k_r$ is "clusters per region" or "nodes per region." The text says "clusters per regional coordinator," which is consistent, but the variable naming convention ($k$ usually implies fan-out) can be tricky.
5.  **Typos/Formatting:**
    *   Section IV-F: "The DES-measured reduction factors match the Bernoulli expectation to within 1%..." - This is expected, but is it a result or a verification? It reads more like code verification.
    *   References: Ensure all URLs (Starlink, Kuiper) have access dates (currently listed as "accessed February 2026" - please update to current date if this is a template).

---

## Overall Recommendation

**Minor Revision**

The manuscript is strong, rigorous, and well-presented. The simulation work is substantial. The primary reason for requesting a revision is to ensure the comparison against the centralized baseline is intellectually fair (by acknowledging parallel processing more prominently in the visual results) and to ensure the claims regarding "linear scaling" are properly scoped to the message-passing layer to avoid misleading readers regarding physical layer constraints.

---

## Constructive Suggestions

1.  **Enhance Figure 2:** Add a third curve for "Centralized (Parallelized, $c=100$)" to Figure 2. This curve will likely stay flat (low latency) much longer. This will visually demonstrate that the *processing* bottleneck is solvable, forcing the reader to realize that the *bandwidth* (spectrum) bottleneck discussed in the text is the real killer for centralized architectures.
2.  **Refine the Abstract:** Change "confirms the absence of queueing-induced nonlinearities" to "confirms the absence of queueing-induced nonlinearities *at the message-passing layer*."
3.  **Expand on MAC Efficiency:** In Section IV-G, the paper introduces $\gamma \approx 0.85$. It would be valuable to briefly mention how $\gamma$ might degrade as $k_c$ increases (e.g., more guard bands). This would add nuance to the cluster size optimization section (IV-B).
4.  **Sectorized Mesh Future Work:** The discussion on Sectorized Mesh (Section V-C) is excellent. Consider moving the "Information completeness vs. coordination capability" comparison (Table II) to the Discussion section to anchor this comparison, as it conceptually bridges the gap between the simulated bounds.