---
paper: "02-swarm-coordination-scaling"
version: "bu"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

**Review of Manuscript (Version BU)**
**Journal:** IEEE Transactions on Aerospace and Electronic Systems

## Review Criteria

### 1. Significance & Novelty
**Rating: 5**

This manuscript addresses a critical and timely gap in the literature regarding the command and control (C2) of mega-constellations and large-scale autonomous swarms ($10^3$--$10^5$ nodes). While existing literature covers routing (ISL) or small-scale formation flying extensively, there is a lack of rigorous, closed-form sizing equations for the hierarchical coordination layer that sits between the physical link and the application logic.

The novelty lies in the derivation of parametric sizing equations that distinguish between byte-level feasibility, MAC efficiency, and time-slot schedulability. The identification of the "Stress Case" (unicast command dissemination) as the binding constraint—requiring multi-cycle staggering despite fitting within the byte budget—is a significant operational insight for constellation designers. This work moves the field from qualitative architectural discussions to quantitative design tools.

### 2. Methodological Soundness
**Rating: 4**

The methodology combines analytical derivation (queueing theory, probability) with a custom Cycle-Aggregated Discrete Event Simulation (DES). The approach is generally robust. The authors are careful to distinguish between what the DES validates (logic, queue dynamics, byte counting) and what it assumes (PHY layer success rates).

However, the reliance on the MAC efficiency parameter $\gamma$ (derived as 0.95, assumed conservatively as 0.85) is a critical pivot point. While the derivation in Section IV-A is logical, it assumes perfect synchronization and minimal control overhead beyond the modeled slots. In a distributed space environment with high relative velocities (Doppler) and potential GNSS denial, achieving $\gamma=0.85$ is non-trivial. The paper would benefit from a more aggressive sensitivity analysis on $\gamma$ to demonstrate system viability if synchronization degrades significantly (e.g., $\gamma < 0.6$).

### 3. Validity & Logic
**Rating: 4**

The conclusions are well-supported by the data presented. The distinction between "Type 1" (broadcast) and "Type 2" (unicast) commands is logically sound and reveals a major scalability bottleneck. The application of the Gilbert-Elliott (GE) model to characterize correlated losses is appropriate for the LEO environment where obstructions (antenna shadowing) are likely bursty.

A minor logical tension exists in the "Static Topology" assumption. While the authors argue that re-association overhead is $<0.5\%$, this assumes a specific orbital configuration. In polar regions of Walker constellations, cluster membership churn could be higher. The validity holds for the general sizing case, but the limitations regarding high-churn geometries should be stated more clearly.

### 4. Clarity & Structure
**Rating: 5**

The manuscript is written with high precision and density. The structure is logical, moving from problem definition to model description, results, and discussion. The use of tables to summarize key parameters (Table I) and feasibility layers (Table VII) is excellent. The distinction between the three feasibility layers (Byte, MAC, Airtime) is communicated clearly. The abstract accurately reflects the content.

### 5. Ethical Compliance
**Rating: 5**

The authors have included an explicit acknowledgment regarding the use of AI-assisted ideation, which aligns with emerging transparency standards. Data availability is provided via a GitHub link. There are no apparent conflicts of interest or ethical concerns regarding the research content.

### 6. Scope & Referencing
**Rating: 5**

The paper is squarely within the scope of *IEEE TAES*, addressing aerospace electronic systems (constellation C2) and system engineering. The referencing is comprehensive, bridging classical distributed systems theory (Lamport, Lynch) with modern space networking (Handley, Fraire) and swarm robotics (Dorigo). The inclusion of recent industry filings (Starlink, Kuiper) grounds the theoretical work in practical reality.

---

## Major Issues

1.  **MAC Efficiency ($\gamma$) Justification:**
    In Section IV-A (Eq. 7), the derivation of $\gamma = 0.949$ relies on a guard time of 4.7 ms. This includes 1 ms for timing jitter and ~2 ms for turnaround. However, this does not explicitly account for Doppler shift compensation time or the potential for "hidden node" collisions if the cluster geometry is not perfectly spherical. While the authors conservatively use $\gamma=0.85$, if the system degrades to CSMA/CA levels ($\gamma \approx 0.4-0.5$) due to synchronization loss, the stress-case workload becomes infeasible (as noted in Fig. 10b).
    *   *Requirement:* Please expand the discussion in Section IV-A to explicitly defend the 4.7 ms guard time against Doppler effects at S-band/UHF frequencies for LEO relative velocities.

2.  **Coordinator Failure & RF-Backup Latency:**
    Section III-B-2 notes that RF-backup handoff takes ~160s. This is a significant vulnerability. If a coordinator fails during a conjunction event (which requires rapid command dissemination), the cluster is effectively leaderless for 16 cycles.
    *   *Requirement:* The paper should explicitly discuss the operational risk of this 160s gap. Is the system safe if a conjunction alert arrives during an RF-based election? The "Double-fault scenario" is mentioned, but the operational consequence (potential collision due to command latency) needs to be quantified or acknowledged as a critical risk.

3.  **Simulation Abstraction Level:**
    The "Cycle-Aggregated" DES (Section III-A) abstracts away intra-cycle packet collisions. While this is necessary for speed, it means the simulation does not validate the TDMA schedule—it only validates the byte budget.
    *   *Requirement:* The authors must be more explicit in the Abstract and Conclusion that the simulation validates *traffic flow and queueing*, not *physical layer schedulability*. The current phrasing "implementation consistency to <0.1%" could mislead a reader into thinking the PHY layer was simulated.

---

## Minor Issues

1.  **Table VII Clarity:** The column "Layer 3: Airtime" is excellent, but the distinction between "Stress (bcast)" and "Stress (unicast)" relies heavily on the text. Adding a footnote or brief parenthetical to the table explaining *why* unicast fails (i.e., "Requires $k_c$ serial TX slots") would improve standalone readability.
2.  **Eq. 11 (AoI):** The analytic approximation for AoI P99 is given. It would be helpful to briefly mention if this assumes independent packet arrivals or if it accounts for the GE burstiness. (It appears to assume geometric inter-arrival, which implies independence).
3.  **Section IV-C (GE Model):** The assumption that "intra-cycle retransmissions... all face the same channel state" is a strong modeling choice. While conservative for recovery, it might be pessimistic for very short obstructions (e.g., tumbling satellite antenna nulls). A brief sentence acknowledging this conservatism would be beneficial.
4.  **Typos/Formatting:**
    *   Table I: "Status report size (256 B)" is listed, but later text mentions "Status reports (256 B) + Heartbeats (64 B)". Ensure consistency in whether "Status" implies the aggregate telemetry or just the payload.
    *   Section IV-A: "Zero-drop ingress at 21--50 kbps" — clarify if this range refers to the sweep performed or the result found.

---

## Overall Recommendation
**Minor Revision**

This is a high-quality paper that makes a significant contribution to the field of space systems engineering. The analytical derivations are sound, and the simulation framework, while abstracted, is appropriate for the scale of the problem ($10^5$ nodes). The revisions requested are primarily to ensure that the assumptions regarding MAC efficiency and physical layer abstraction are transparently bounded, preventing readers from interpreting the results as fully validated PHY-layer performance.

---

## Constructive Suggestions

1.  **Add a "Degraded Mode" Analysis:** In the sensitivity analysis (Fig. 10), explicitly mark a "Safe Mode" floor where the system reverts to exception-only reporting if $\gamma$ drops below a critical threshold (e.g., 0.4). This would strengthen the operational utility of the paper.
2.  **Visualizing the Superframe:** A simple diagram of the TDMA superframe (visualizing the data in Table VI) showing Ingress vs. Egress vs. Guard times would make the "Airtime Feasibility" argument much more intuitive for readers less familiar with TDMA structures.
3.  **Expand on "Unmodeled Constraints":** In the Discussion, briefly list the specific unmodeled constraints that are most likely to bite in a real implementation (e.g., antenna pointing settling time, specific orbital perturbations affecting cluster geometry). This reinforces the "Design Equations" nature of the paper—providing a baseline that real-world friction will erode.