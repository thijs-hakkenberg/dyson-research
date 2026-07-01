---
paper: "02-swarm-coordination-scaling"
version: "at"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

**Review of Manuscript Version AT**
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Journal:** IEEE Transactions on Aerospace and Electronic Systems

---

### 1. Significance & Novelty
**Rating: 4 (Good)**

The manuscript addresses a timely and critical problem: the scalability of command and control (C2) architectures for mega-constellations and large-scale autonomous swarms ($10^3$--$10^5$ nodes). While the networking community has addressed routing in this regime (e.g., Handley, Del Portillo), the specific focus on *coordination protocol overhead* and *byte-level sizing* under constrained RF-backup conditions is a distinct and valuable contribution.

The novelty lies less in the invention of new protocols—hierarchical aggregation is a standard pattern—and more in the rigorous parametric characterization of these architectures specifically for the orbital domain. The derivation of closed-form design equations validated by discrete event simulation (DES) provides a "practitioner’s handbook" utility that is often missing in purely theoretical swarm literature. The distinction between nominal optical operations and the RF-backup "survival mode" is a crucial operational insight that grounds the work in reality.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology combines analytical queueing theory ($M/D/1$, $M/D/c$) with a custom cycle-aggregated DES. The approach is generally robust. The authors are commendable for their transparency regarding assumptions, specifically the abstraction of the MAC layer into a $\gamma$ efficiency factor and the use of a cycle-aggregated time step ($T_c=10$s).

However, the reliance on the "independence" of link loss and coordinator congestion (Section IV-D) rests heavily on the assumption of dedicated point-to-point links. In many practical RF-backup scenarios (e.g., omnidirectional S-band), the medium is shared, and retransmissions *would* increase the noise floor and collision rate, coupling these factors. While the authors acknowledge this in Section V-B, the simulation results in IV-D might be overly optimistic for shared-medium implementations. Additionally, the statistical treatment (30 MC runs, bootstrap CIs) is rigorous.

### 3. Validity & Logic
**Rating: 4 (Good)**

The conclusions are logically derived from the data presented. The analysis of the Gilbert-Elliott (GE) link model is particularly strong; the finding that intra-cycle retransmission is ineffective during bursts while inter-cycle recovery is highly effective (Section IV-C) is a valuable, counter-intuitive result for system designers.

A potential validity gap exists in the "Static Topology" assumption (Section III-B-2). The authors state that cluster membership is static for the 1-year simulation. While true for intra-plane formations, most mega-constellations (Walker-Delta) involve rapid relative motion between orbital planes. If "Regional" or "Cluster" groups span orbital planes, the topology is highly dynamic. If they are strictly intra-plane, the validity holds, but this geometric constraint needs explicit definition.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure is logical, moving from problem definition to model, results, and discussion. The distinction between "offered" and "delivered" overhead is handled with precision. Figures are well-referenced, and the "Design Equations Summary" in Section V is a high-value addition for the reader. The abstract accurately reflects the content.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a clear "Data Availability" statement pointing to an open-source repository, which enhances reproducibility. They also include a specific acknowledgment regarding the use of AI tools for ideation (Section VI), which aligns with emerging transparency standards in academic publishing. No obvious conflicts of interest or ethical lapses are apparent.

### 6. Scope & Referencing
**Rating: 5 (Excellent)**

The paper fits perfectly within the scope of *IEEE TAES*, bridging the gap between electronic systems (comm links), aerospace operations (orbital dynamics), and systems engineering. The references are comprehensive, covering historical foundations (Kleinrock, Lamport), current operational reality (Starlink, OneWeb), and relevant theoretical work (AoI, Mean Field Games).

---

### Major Issues

1.  **Static Topology Assumption vs. Orbital Dynamics:**
    In Section III-B-2, the authors assume static cluster membership for the simulation duration. For LEO mega-constellations, this holds only if clusters are strictly defined as "co-moving nodes within the same orbital plane." If a cluster is defined geographically (e.g., "all satellites over North America"), membership churn is extreme (${\sim}10$ minutes). If the cluster includes cross-plane links, the relative velocities are high, and link topology changes frequently.
    *   *Requirement:* The authors must explicitly state that the hierarchical clusters are formed *intra-plane* to justify the static assumption. If the architecture assumes cross-plane clustering, the static assumption is invalid, and the overhead of cluster re-association (handoffs) must be modeled or at least analytically estimated as an additional overhead term.

2.  **MAC Layer Abstraction and Contention Coupling:**
    In Section IV-D, the paper claims "pipeline independence" between GE losses and coordinator drops. This is valid *only* for Frequency Division (FDMA) or dedicated beam links. However, the target application is "RF backup" (Section I-C), which often implies shared-medium usage (e.g., omni-directional antennas for telemetry). In a shared medium, GE retransmissions increase channel load, directly degrading $C_{\text{coord}}$ via collisions.
    *   *Requirement:* The authors should qualify the "Independence" finding in the abstract and Section IV-D. It should be clearly stated that this holds for *non-contention-based* or *channelized* architectures, and that for shared-medium RF, a cross-factor correction would likely be required.

### Minor Issues

1.  **Section III-B-1 (Centralized Baseline):** The authors use an $M/D/1$ model. While they introduce $M/D/c$ later, the initial comparison often implies a single server. It would be fairer to emphasize that the centralized bottleneck is rarely CPU cycles ($\mu_s$), but rather TT\&C uplink contact time and spectrum availability. The text mentions this briefly, but the mathematical comparison focuses heavily on queueing delay, which is likely negligible compared to propagation and contact scheduling delays.
2.  **Section IV-A (TDMA Guard Times):** The derivation of $\gamma = 0.85$ is stated as consistent with CCSDS Proximity-1. However, at $N=10^5$, synchronization jitter might require larger guard times. A brief sentence justifying the timing precision required to maintain $\gamma=0.85$ across a distributed swarm would strengthen this.
3.  **Figure 5 (Recovery):** The distinction between the analytical Markov model and the DES data points is slightly hard to read in grayscale. Ensure markers are distinct.
4.  **Equation 5 (Mesh Messages):** The notation $O(N \cdot f \cdot \log N)$ is used. Please clarify if $f$ (fanout) is constant or scales with $N$. If $f$ is constant, it is $O(N \log N)$.

### Overall Recommendation
**Minor Revision**

The paper is high-quality, rigorous, and relevant. The "Major Issues" identified above represent necessary clarifications regarding the physical applicability of the model (orbital geometry and MAC contention) rather than fundamental flaws in the derivation or simulation code. With these clarifications, the paper will make a strong contribution to the literature.

### Constructive Suggestions

1.  **Add a "Geometry Note":** In Section III-B, explicitly define the orbital geometry of a "Cluster." State that clusters are formed of co-moving intra-plane satellites to justify the static topology assumption. Briefly mention that cross-plane coordination would likely require the "Regional" tier to handle high-churn links.
2.  **Refine the Independence Claim:** In Section IV-D, add a sentence explicitly contrasting the modeled architecture with a CSMA/CA (shared medium) approach, noting that in CSMA, the "Independence" result would likely collapse due to retransmission-induced collisions.
3.  **Expand the "Safe Mode" Discussion:** The observation in Section IV-F (Topology Comparison) regarding the "Degraded-synchronization floor" is excellent. Consider moving this point to the Conclusion or Abstract, as the inability to support command campaigns under Slotted ALOHA ($\gamma=0.36$) is a critical operational finding for constellation safety.
4.  **AoI Context:** In Section IV-B, when discussing the 440s AoI, briefly reference the typical "validity time" of an ephemeris. If an ephemeris is valid for 24 hours (standard SGP4), a 440s delay is negligible. If it is for real-time formation flying (valid for seconds), it is critical. Contextualizing this helps the reader judge the severity of the delay.