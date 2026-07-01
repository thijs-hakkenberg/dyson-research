---
paper: "02-swarm-coordination-scaling"
version: "cp"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-03"
recommendation: "Unknown"
---

Here is a rigorous peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CP), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript ID:** [Assigned by Editor]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## 1. Significance & Novelty
**Rating: 4 (Good)**
The paper addresses a critical gap in the literature: the specific sizing of coordination channels for mega-constellations ($10^3$--$10^5$ nodes). While routing and networking for such constellations are well-studied, the specific interplay between hierarchical control overhead, byte-level budgeting, and TDMA slot timing is under-explored. The derivation of closed-form sizing equations that link message-layer constraints to physical-layer parameters is a significant contribution for system architects. The novelty lies in the integrated "two-layer" feasibility framework rather than in new fundamental control theory or modulation techniques.

## 2. Methodological Soundness
**Rating: 5 (Excellent)**
The methodology is robust. The authors employ a multi-tiered approach: analytical derivation, discrete event simulation (DES) for message-layer statistics, and a specific slot-level simulation for TDMA timing verification. The explicit separation of "Model S" (simplified) and "Model C" (CCSDS-grounded) is a strong methodological choice that prevents over-optimistic conclusions. The use of Gilbert-Elliott (GE) models for correlated loss is appropriate for the domain, and the sensitivity sweeps (Fig. 4) add necessary rigor given the lack of empirical ISL channel data.

## 3. Validity & Logic
**Rating: 4 (Good)**
The internal logic is consistent. The transition from the byte budget (Layer 1) to airtime schedulability (Layer 2) is handled correctly without double-counting overheads. The identification of the ARQ $\times$ TDMA coupling failure mode at 24 kbps is a high-validity finding that justifies the simulation effort. The assumptions are clearly stated. *However*, the reliance on a static topology for the primary analysis, while justified for co-planar clusters, limits the immediate validity for cross-plane architectures without further caveats (addressed in Major Issue #2).

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally well-structured. The distinction between "information rate" and "PHY rate" is maintained with discipline throughout. Tables are dense but informative, particularly the "Rate Ladder" (Table 4) and the "Superframe Time Budget" (Table 6). The notation is standard and well-defined.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement with a GitHub link (though obviously a placeholder for review). The acknowledgment of AI assistance in *ideation* and *editing* (but not data generation) is transparent and aligns with emerging IEEE policies.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The scope fits TAES perfectly (Aerospace Systems/Space Systems). The referencing is adequate, covering CCSDS standards, classical queueing theory, and recent swarm robotics literature. The connection to existing constellations (Starlink, Kuiper) provides good context.

---

## Major Issues

1.  **Contextualization of the "Stress Case" (46% Overhead)**
    *   **Issue:** The abstract and introduction highlight the 46% stress-case overhead ($\eta_S$). While Section IV-E clarifies this is episodic ($d \ll 1$), a casual reader might interpret 46% as a steady-state requirement, which would imply the architecture is inefficient.
    *   **Why it matters:** If the system is perceived as requiring 46% overhead continuously, it appears non-viable for power-constrained CubeSats.
    *   **Remedy:** In the Abstract and Conclusion, explicitly qualify the 46% figure as a "worst-case transient" or "episodic bound" alongside the steady-state 5-10%. The current phrasing is slightly alarmist regarding the overhead.

2.  **Re-association Overhead in Cross-Plane Geometries**
    *   **Issue:** Section V-C mentions that static membership is assumed and re-association is negligible for co-planar formations. However, for Walker-Delta or polar constellations (common for global coverage), relative velocities between planes are high, leading to frequent topology changes if clusters are defined by proximity.
    *   **Why it matters:** If $k_c$ is maintained via proximity in a cross-plane constellation, the "negligible" re-association overhead might actually dominate the byte budget.
    *   **Remedy:** Expand the limitations section to explicitly bound the $\Delta V$ or orbital regimes where the static cluster assumption holds. Provide a first-order approximation of the overhead if a node switches clusters every $X$ minutes (e.g., crossing the pole).

3.  **Lack of Sensitivity Analysis for $T_{guard}$**
    *   **Issue:** The feasibility of the 30 kbps link relies heavily on the calculated margin (730 ms). This margin depends on $T_{guard} = 4.7$ ms. This assumes precise timing. If GNSS is denied or degraded (a common defense scenario), clock drift could necessitate much larger guard bands.
    *   **Why it matters:** If $T_{guard}$ doubles due to clock drift requirements, the 30 kbps link might become infeasible, pushing the requirement to 35 or 40 kbps immediately.
    *   **Remedy:** Add a sensitivity line to Table 6 or text discussion: "If $T_{guard}$ increases to 10ms (e.g., GNSS denial), margin reduces to $X$."

## Minor Issues

1.  **Table 1 (Notation):** The definition of $\gamma$ cites Eq. 3, but Eq. 3 is the simplified Model S. It should likely cite Eq. 12 (the generalized form) or clarify that Model C values are used.
2.  **Section III-B-2 (Coordinator Failure):** The "Thundering Herd" problem during Raft election is mentioned. Please clarify if the simulation models the random backoff explicitly or just adds a fixed penalty time.
3.  **Fig. 3 (Recovery):** The caption mentions "DES bars" but the visual representation might be clearer as points or a stepped line to distinguish from the analytical curve.
4.  **Eq. 10 (AoI):** The logarithmic derivation assumes independent Bernoulli trials. The text acknowledges this is an upper bound for memoryless sampling, but it might be worth noting that correlated losses (GE) would cluster updates, potentially increasing the *worst-case* AoI even if the mean remains similar.
5.  **Typos:** Check the unit consistency in Table 3 (Processing capacity). $\mu_s$ is in msg/s, but later text refers to ms/msg. (Consistency is generally good, just a spot check recommended).

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality, rigorous engineering paper. It moves beyond vague discussions of "swarm coordination" to provide concrete, standards-grounded sizing equations. The authors have successfully anticipated most reviewer objections (e.g., by separating Model S and Model C, and by performing the GE sensitivity sweep). The "Two-Layer Feasibility" framework is a valuable tool for the community. The revisions requested above are primarily to prevent misinterpretation of the results (specifically the stress case and topology constraints) and do not require new simulations.

## Constructive Suggestions

1.  **Strengthen the "Practitioner's Guide":** Algorithm 1 is excellent. I suggest adding a "Lookup Table" for common radio types (e.g., "If using S-band Proximity-1, use $\gamma=0.76$"; "If using X-band high-rate, use $\gamma \approx 0.5$ due to acquisition overhead"). This would make the paper immediately citable by systems engineers.
2.  **Clarify "Information Rate":** In the abstract, you mention "20 kbps information-rate". It might be helpful to explicitly define this as "Layer 2 payload throughput" early on, to distinguish it from Layer 1 application throughput (which is lower due to headers).
3.  **Visualizing the Margin:** A simple bar chart showing the breakdown of the 10-second cycle at 30 kbps (Data vs. Overhead vs. Margin) would be very effective for visually demonstrating why 24 kbps fails and 30 kbps succeeds.