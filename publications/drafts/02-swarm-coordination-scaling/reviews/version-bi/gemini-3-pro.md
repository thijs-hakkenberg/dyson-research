---
paper: "02-swarm-coordination-scaling"
version: "bi"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Accept"
---

Here is a rigorous academic peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version BI), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Version:** BI
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## Review Criteria

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This manuscript addresses a critical and timely gap in the literature: the scalability of coordination architectures for "mega-constellations" ($10^4$--$10^5$ nodes). While existing literature covers routing (networking) or small-scale formation flying (GNC), there is a distinct lack of rigorous sizing models for the *command and control* (C2) layer at this scale. The derivation of closed-form sizing equations for hierarchical coordination, validated by discrete event simulation (DES), constitutes a significant contribution to the field.

The novelty lies in the specific focus on the "middle ground" between centralized ground control (which scales poorly with latency and spectrum) and full mesh networks (which scale poorly with bandwidth). By quantifying the specific overheads of a four-level hierarchy and identifying the "stress-case" bottlenecks (specifically the unicast command stagger problem), the authors provide a practitioner's toolkit that is currently missing. The distinction between architecture-specific overhead ($\sim$5%) and workload-dependent overhead is a valuable insight that corrects common misconceptions about distributed systems costs.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology combines analytical derivations (queueing theory, TDMA framing) with a custom cycle-aggregated Discrete Event Simulation (DES). The approach is generally robust. The choice of a cycle-aggregated model is appropriate for the scale ($10^5$ nodes) where packet-level simulation would be computationally prohibitive for year-long runs. The cross-verification between the analytical models and the DES (matching within 0.1%) builds strong confidence in the implementation.

However, there is a slight disconnect regarding the Physical Layer (PHY) validation. The authors acknowledge this as "future work" (Section V-A), but the reliance on a fixed $\gamma$ (MAC efficiency) parameter to abstract all PHY/MAC interactions is a strong simplification. While the derivation of $\gamma \approx 0.95$ in Eq. 8 is logically sound based on the slot structure provided, the impact of Doppler shifts and rapid topology changes on *synchronization* (and thus $\gamma$) in LEO is under-discussed. The Gilbert-Elliott (GE) model implementation is sound, particularly the conservative assumption of per-cycle coherence, which rightly bounds the recovery time.

### 3. Validity & Logic
**Rating: 4 (Good)**

The conclusions are well-supported by the data. The identification of the coordinator ingress link as the binding constraint (rather than CPU processing) is logical and consistent with space systems engineering principles. The analysis of the "stress case" (unicast commands) requiring a 22-cycle stagger is a crucial finding that highlights operational constraints often overlooked in theoretical papers.

One area requiring tighter logic is the "Sectorized Mesh" comparison. The authors compare a hierarchical system (full cluster awareness) with a sectorized mesh (local awareness). While they attempt to normalize this by discussing "functional scope" (Table VIII), the comparison feels slightly asymmetric. The mesh is penalized for high overhead, but it is performing a different neighbor-discovery function that the hierarchy delegates to the coordinator. The paper would benefit from explicitly stating that the hierarchy *relies* on the coordinator for neighbor discovery, whereas the mesh does not.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure is logical, moving from problem definition to model description, results, and discussion. The notation is consistent (Table I is very helpful). The distinction between "Protocol Overhead" and "Baseline Telemetry" is maintained rigorously throughout, preventing confusion.

Figures are referenced appropriately, and the tables (particularly Table V on schedulability and Table VI on the superframe budget) are high-value and dense with information. The abstract is quantitative and precise, serving as a model for technical writing.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors include a specific acknowledgment regarding AI-assisted ideation (Claude, Gemini, GPT), citing a specific methodology paper. This transparency is commendable and aligns with emerging best practices in academic publishing. No human subject research is involved. The open-source availability of the simulation code (Section VI) supports reproducibility and ethical transparency.

### 6. Scope & Referencing
**Rating: 5 (Excellent)**

The paper fits perfectly within the scope of *IEEE TAES*, bridging the gap between aerospace systems engineering and electronic communication systems. The references are comprehensive, covering historical foundations (Kleinrock, Reynolds), current operational systems (Starlink, OneWeb), and relevant theoretical work (Age of Information, consensus algorithms). The inclusion of CCSDS standards (Space Packet Protocol, Proximity-1) grounds the work in realistic space engineering constraints.

---

## Major Issues

1.  **RF-Backup vs. Optical Primary Confusion:**
    The paper focuses heavily on the 1 kbps RF-backup link as the "design-driving case." While this is logically sound for reliability engineering, the manuscript occasionally blurs the line between nominal operations (Optical ISL, >1 Gbps) and backup operations.
    *   *Critique:* If the system spends 99% of its time on Optical ISLs, the "Stress Case" of 46% overhead on the RF link is only relevant during a double-fault scenario (Optical failure + High traffic demand).
    *   *Requirement:* Section III-E needs to be more explicit that the 1 kbps budget is *strictly* for the backup/safe-mode link. The abstract implies these constraints apply generally, which might mislead a reader into thinking the primary control loop is this constrained.

2.  **Coordinator Failure & Election Timing:**
    Section III-B-2 mentions a "3-5s election" via Raft over Optical ISL, but an "RF-backup handoff" taking ~60s.
    *   *Critique:* If the coordinator fails *because* it is tumbling or power-negative (a likely failure mode), the Optical ISL will almost certainly be down. Therefore, the "Nominal Handoff" (3-5s) is unlikely to be the relevant recovery mode for a coordinator failure. The RF-backup mode is the *primary* recovery mode for coordinator failure.
    *   *Requirement:* The authors should revise the "Coordinator failure transient" text to acknowledge that coordinator failure and optical link failure are likely correlated events. The reliability analysis should prioritize the 60s recovery time, not the 3-5s time.

---

## Minor Issues

1.  **Table IV (Bandwidth Breakdown):** The "Global-State Mesh" column lists overhead as ">1 kbps" and "Exceeds." It would be more scientifically rigorous to provide the actual calculated number (e.g., "~73 MB/cycle" as mentioned in the text) rather than just stating it exceeds the budget.
2.  **Eq. 8 (Gamma Derivation):** The derivation assumes a specific slot structure. It would be beneficial to explicitly state the assumed modulation order (e.g., BPSK/QPSK) and coding rate (e.g., rate 1/2 convolutional) that justifies the "Data" vs "Slot" time, or simply state that the bits are "on-the-air" bits.
3.  **Section IV-C (GE Model):** The text states "The assumption is conservative for recovery." This is true, but it is *optimistic* for burst length if physical obstructions last longer than $T_c=10s$. A brief sentence acknowledging that physical shadowing could last minutes (spanning multiple cycles) would strengthen the discussion on "Slow-mixing" regimes.
4.  **Fig. 6 (Latency):** The caption mentions a $10^6$ node curve as an "analytical extrapolation." Please ensure the legend or the plot clearly marks this curve (e.g., dashed line) to distinguish it from DES data.
5.  **Typos/Formatting:**
    *   Section III-B-2: "RequestVote: 100 B x quorum of ~5" — The formatting of "x" should be mathematical $\times$.
    *   Table VII: The column header "Delivered $\eta$ (%)" is slightly ambiguous. Does this mean "Effective Throughput"? Clarify in footnote.

---

## Overall Recommendation

**Accept with Minor Revisions**

This is a high-quality manuscript that provides valuable design tools for the aerospace engineering community. The mathematical derivations are sound, the simulation verification is robust, and the writing is clear. The revisions requested above are primarily clarifications to ensure the operational context (backup vs. primary links) and failure modes are described with maximum precision.

---

## Constructive Suggestions

1.  **Add a "ConOps" Box or Paragraph:** Early in the paper, explicitly define the Concept of Operations: "Nominal ops use Optical ISL (high bandwidth, low latency). The equations derived here size the *Safety Critical RF Backup* link, ensuring the swarm remains controllable during optical outages." This will frame the 1 kbps constraint immediately.
2.  **Refine the Mesh Comparison:** In Section IV-G, explicitly concede that the Sectorized Mesh provides *independent* neighbor discovery, whereas the Hierarchy relies on the Coordinator. This makes the comparison fairer: the Hierarchy is more efficient because it centralizes the expensive discovery task.
3.  **Expand on Doppler/Guard Times:** In Section IV-A (TDMA frame model), add a sentence about Doppler shift at LEO. For a 500km cluster, relative velocity is low, but for the "Regional" links, Doppler could be significant. Acknowledge that the 4.7ms guard time accounts for this.
4.  **Future Work - Physical Layer:** Be more specific in Section V-A. Suggest that "future work should validate the $\gamma=0.85$ assumption against a high-fidelity channel model including multipath and antenna pointing errors."