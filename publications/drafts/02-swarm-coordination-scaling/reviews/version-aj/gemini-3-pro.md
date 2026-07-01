---
paper: "02-swarm-coordination-scaling"
version: "aj"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

## Peer Review: IEEE Transactions on Aerospace and Electronic Systems

**Manuscript ID:** [Version AJ]
**Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Reviewer Expertise:** Distributed systems, swarm robotics, discrete event simulation, satellite network scaling.

---

### 1. Significance & Novelty
**Rating: 5**

This manuscript addresses a critical and forward-looking gap in the aerospace literature: the coordination of autonomous constellations at scales ($10^4$--$10^5$ nodes) where traditional ground-in-the-loop architectures face spectrum and latency bottlenecks. While the swarm robotics literature often deals with idealized agents and the satellite networking literature focuses on routing data planes, this paper uniquely isolates the **control plane** budget.

The novelty lies in the rigorous "byte-level accounting" approach. Rather than relying on asymptotic complexity ($O(N)$ vs $O(\log N)$), the authors quantify the specific bandwidth requirements (e.g., the 21–50 kbps coordinator ingress threshold). The characterization of the "design envelope" between nominal ($\eta \approx 5\%$) and stress-case ($\eta \approx 46\%$) workloads provides actionable sizing data for future system architects. The distinction between processing limits (which are solvable) and spectrum/availability limits (which favor hierarchy) is a significant conceptual contribution.

### 2. Methodological Soundness
**Rating: 4**

The methodology—cycle-aggregated Discrete Event Simulation (DES)—is appropriate for the research questions. Simulating individual packets for $10^5$ nodes over a year is computationally intractable; the cycle-aggregated approach strikes the right balance between fidelity and scale.

**Strengths:**
*   The validation against analytical closed-form solutions (Section IV-E) builds high confidence in the simulation engine.
*   The separation of "offered" vs. "delivered" load is handled with necessary rigor.
*   The "Joint Interaction" verification (Section IV-D) is a sophisticated use of DES to test the independence of failure modes.

**Weaknesses:**
*   **MAC Layer Abstraction:** The assumption of $\gamma \in [0.7, 0.9]$ (MAC efficiency) is reasonable for the Hierarchical topology (which naturally admits TDMA), but potentially optimistic for the Sectorized Mesh comparator. In a shared RF medium, hidden terminal problems and contention could drive $\gamma$ significantly lower for the mesh. While the authors acknowledge this in Section IV-F, the quantitative comparison likely underestimates the performance penalty of the mesh topology.
*   **Collision Alert Rate:** The assumption of $10^{-4}$ events/node/s is justified as "screening alerts," but this is a high-sensitivity parameter. If this rate drops to $10^{-6}$ (closer to actual maneuver rates), the "Stress Case" overhead might collapse, changing the conclusions.

### 3. Validity & Logic
**Rating: 5**

The conclusions are well-supported by the data. The authors are careful not to overclaim; for instance, they explicitly state that centralized architectures do not fail due to compute limits until $N \approx 10^6$, correctly identifying ground station availability and uplink spectrum as the actual binding constraints.

The "Dual-Regime Interpretation" (Section IV-E.3) is excellent logic. It clarifies that the reported overheads are only binding during RF-backup or low-power modes (1 kbps), which is exactly when coordination robustness is most critical. The derivation of the Age-of-Information (AoI) results and their coupling to a simple position error model provides necessary physical context to the abstract data rates.

### 4. Clarity & Structure
**Rating: 5**

The manuscript is exceptionally well-written. The structure is logical, moving from architecture definitions to specific sizing results (bandwidth, AoI, loss), and finally to system-level comparisons.
*   Figures are described clearly in the text.
*   The distinction between "Baseline Telemetry" (topology-invariant) and "Protocol Overhead" is maintained consistently, preventing confusion.
*   Table I (Scalability Sensitivity) and Table X (Topology Comparison) are very effective summaries.

### 5. Ethical Compliance
**Rating: 4**

The authors include an acknowledgment regarding AI-assisted ideation, which complies with emerging standards.
**Note on Anonymity:** The manuscript includes a link to a GitHub repository (`projectdyson/dyson`) and names the "Project Dyson Research Team." If this track requires double-blind review, these details unblind the authors. If the journal allows single-blind or open review, this is acceptable. I have reviewed the content based on merit regardless of affiliation.

### 6. Scope & Referencing
**Rating: 5**

The paper is well-scoped for *IEEE TAES*. It bridges the gap between orbital mechanics (conjunction screening), networking (DTN/protocols), and systems engineering. The references are comprehensive, covering foundational distributed systems theory (Lamport, Lynch), current mega-constellation literature (Handley, Del Portillo), and relevant swarm robotics work.

---

### Major Issues

1.  **MAC Layer Fairness in Topology Comparison:**
    In Section IV-F and Figure 11, the Sectorized Mesh is compared to the Hierarchical topology using similar bandwidth scaling assumptions. However, the Hierarchical topology structurally supports scheduled access (TDMA) within a cluster, whereas a Mesh topology relies on random access or complex distributed scheduling.
    *   *Critique:* You apply a generic $\gamma$ factor. In reality, the Mesh topology would likely suffer from a much lower $\gamma$ due to contention collisions as density increases, whereas the Hierarchy isolates collision domains.
    *   *Requirement:* Please add a specific sensitivity analysis or a dedicated paragraph in the Discussion quantifying how a degradation of $\gamma$ (e.g., to Slotted ALOHA levels of 0.36) specifically impacts the Sectorized Mesh viability compared to Hierarchy. This will likely strengthen your argument for Hierarchy.

2.  **Coordinator Ingress "Zero-Drop" Thresholds:**
    In Section IV-A, you present 21 kbps (Leaky Bucket) vs. 50 kbps (Deadline).
    *   *Critique:* The distinction is clear, but the operational recommendation is slightly ambiguous. If a designer chooses 21 kbps, they *must* implement buffering that spans cycle boundaries.
    *   *Requirement:* Explicitly state the buffer size requirement (in bytes) for the 21 kbps solution to work. Is it $1 \times$ Cycle or $2 \times$ Cycle? This is a critical hardware sizing parameter that is currently implicit.

### Minor Issues

1.  **Table II (Representative System):** The labels "Multi-threaded ground station" vs "Hyperscale data center" are somewhat colloquial. Consider using more precise terms like "High-performance computing cluster" or "Distributed cloud infrastructure."
2.  **Equation 11 (Chernoff Bound):** The text mentions this is a heuristic for the burstiness. Please clarify if the $\alpha$ parameter in the equation corresponds directly to the $\beta$ parameter in Table V, or if they are distinct scaling factors.
3.  **Section IV-B (AoI):** The result of 440s P99 AoI at 10% reporting is significant. In the text, you mention this provides an input to screening studies. It would be beneficial to explicitly state if 440s is generally considered *acceptable* or *dangerous* for typical LEO shells, referencing the ESA conjunction assessment cadence (usually hours/days, implying 440s is acceptable, but this should be explicit).
4.  **Typos/Formatting:**
    *   Section IV-G: "The 24--48 hour duty cycles occupy the Pareto frontier" - Ensure Figure 12 clearly marks the frontier.
    *   References: Ensure all URLs have access dates (some do, some don't).

### Overall Recommendation
**Minor Revision**

The manuscript represents a high-quality, rigorous contribution to the field of autonomous space systems. The simulation framework is robust, and the results are non-trivial and actionable. The revisions requested are primarily to clarify physical-layer assumptions (MAC fairness) and hardware sizing specifics (buffer depth), which will strengthen the paper's utility for system designers.

### Constructive Suggestions

1.  **Strengthen the MAC Argument:** Explicitly argue that the Hierarchical architecture's primary advantage over Mesh is not just message complexity, but the ability to enforce TDMA scheduling without global clock synchronization (local cluster sync is sufficient). This is a strong physical-layer argument that complements your message-layer data.
2.  **Visualizing the "Design Envelope":** Figure 6 (Workload Comparison) is good, but a figure plotting "Required Bandwidth per Node" vs. "Reporting Frequency" with shaded regions for "Sustainable Region" (where $\eta < 100\%$) would be a powerful visual summary for engineers.
3.  **Expand on "Project Dyson":** If the repository is live, ensure the `README` explicitly maps the paper's Figure numbers to the generation scripts. This significantly enhances reproducibility.
4.  **Clarify "Handoff" Impact:** You mention handoff uses a separate optical ISL. Briefly discuss what happens if the optical ISL fails. Does the system fall back to the 1 kbps channel for handoff? If so, does the system deadlock? A one-sentence clarification on fallback modes would be valuable.