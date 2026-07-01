---
paper: "02-swarm-coordination-scaling"
version: "z"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-24"
recommendation: "Accept"
---

Here is a rigorous peer review of the manuscript "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study," prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

***

# Peer Review Report

**Manuscript ID:** Version Z
**Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## Review Criteria

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This paper addresses a critical and timely gap in the aerospace engineering literature: the specific scaling behaviors of coordination architectures for "mega-constellations" and future autonomous swarms in the $10^3$ to $10^5$ node regime. While existing literature covers small-scale swarms ($<100$ nodes) or traditional centralized constellation management, the "middle ground" of massive autonomous fleets is under-explored. The shift from ground-in-the-loop to autonomous hierarchical coordination is inevitable for future architectures (e.g., Starlink Gen2+, Kuiper, Dyson precursors), making this work highly relevant to the *IEEE TAES* readership.

The novelty lies in the methodological rigor applied to this specific problem. The authors move beyond simple analytical Big-O notation to provide a "parametric design-space characterization" using cycle-aggregated Discrete Event Simulation (DES). The specific quantification of the "zero-drop threshold" for coordinators (50 kbps vs. 24 kbps TDMA) and the Age-of-Information (AoI) trade-offs for exception-based telemetry provide actionable engineering data that closed-form analysis cannot easily capture. The distinction between "stress-case" and "nominal" workloads is particularly valuable for system architects.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The simulation framework is generally robust. The choice of a cycle-aggregated DES is appropriate for the scale ($10^5$ nodes) where packet-level simulation would be computationally prohibitive. The authors are transparent about their abstractions (Table V is excellent practice). The use of Monte Carlo methods to bound stochastic variance is sound, and the validation against analytical models (Section IV-E) builds confidence in the simulation results.

However, there is a slight disconnect regarding the physical layer abstraction. While the authors acknowledge that MAC-layer effects are abstracted into an efficiency factor $\gamma$, the interaction between the "1 kbps per-node budget" and the physical reality of optical ISLs (Inter-Satellite Links) vs. RF backups needs tighter justification. The paper assumes a logical bandwidth cap, but in reality, topology changes (relative motion) drive link availability more than just "Bernoulli" or "Gilbert-Elliott" loss models. The assumption that $N/k_c$ coordinators can simply "pool" bandwidth via TDMA without discussing the antenna beamforming or slewing implications is a minor weakness in the physical realism, though acceptable for a network-layer study if clearly caveated.

### 3. Validity & Logic
**Rating: 5 (Excellent)**

The conclusions are logically derived from the data presented. The paper does an excellent job of distinguishing between *fundamental* scaling limits (analytical) and *practical* engineering limits (burstiness, queueing). The finding that protocol overhead is dominated by workload assumptions (9x spread) rather than architecture choice is a significant insight that challenges the common academic focus on purely topological optimization.

The comparison against "intentional bounds" (Centralized and Global-State Mesh) is logically sound. The authors correctly identify these as reference points rather than strawmen. The introduction of the "Sectorized Mesh" as a realistic intermediate comparator strengthens the validity of the hierarchical architecture's performance claims. The logic regarding correlated losses (Gilbert-Elliott model) rendering intra-cycle retransmission ineffective is mathematically sound and practically vital.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure is logical, following a standard progression from introduction to method, results, and discussion. The use of tables to define parameters (Table IV) and traffic accounting (Table VII) ensures reproducibility. The distinction between "Baseline Telemetry" and "Protocol Overhead" is defined clearly in Section III-F, preventing ambiguity in the results.

The figures are well-referenced, and the captions are descriptive. The "Roadmap" paragraph at the start of Section IV is a helpful touch for navigating the dense results section. The abstract is quantitative and impactful, summarizing the key engineering takeaways effectively.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a specific "Acknowledgment" section detailing the use of AI tools (Claude 4.6, Gemini 3 Pro, GPT-5.2) for ideation, citing a companion methodology paper. This level of transparency regarding AI-assisted research meets and exceeds current ethical standards. There are no apparent conflicts of interest or ethical concerns regarding the subject matter.

### 6. Scope & Referencing
**Rating: 4 (Good)**

The scope is perfectly aligned with *IEEE TAES*. The references are a good mix of classical distributed systems theory (Lamport, Lynch), standard astrodynamics texts (Wertz), and recent developments in mega-constellations (Starlink, Kuiper).

One minor gap is the lack of reference to specific CCSDS standards regarding *file delivery* protocols beyond BPv7. While BPv7 is mentioned, CFDP (CCSDS File Delivery Protocol) is the standard for reliable file transfer in space and is relevant to the "handoff state transfer" discussion. Additionally, referencing specific optical ISL hardware capabilities (e.g., Mynaric, Tesat) would ground the "1-10 Gbps" assumption in current commercial reality.

---

## Major Issues

*None.* The paper is technically sound and ready for publication subject to the minor improvements listed below.

## Minor Issues

1.  **Coordinator Election Overhead (Section III-H):** The paper states that coordinator election traffic is negligible ($<0.01\%$) and thus lumped into "Heartbeat/ACK." However, in a failure scenario (as opposed to a scheduled rotation), the *latency* of election is critical. Does the simulation account for the "dead time" during an election after a coordinator failure? A brief sentence clarifying if the system is "unavailable" during the election phase would be beneficial in Section III-H.
2.  **TDMA Guard Time (Section IV-A):** The paper assumes a TDMA guard-time efficiency $\gamma = 0.85$. In LEO, propagation delays vary continuously. For a cluster of 100 km radius, light time is small ($<1$ ms), but for larger sparse clusters, it could be significant. Please clarify if $\gamma = 0.85$ is an empirical estimate or derived from a specific slot-size/distance assumption.
3.  **Power Budget Calculation (Eq. 13):** The calculation $\Delta P_{avg} = 15W / 100 = 0.15W$ assumes perfect load balancing over time. In reality, thermal subsystems must be sized for the *peak* load (20W), not the average. While the *energy* budget is low, the *thermal* design constraint is high. The text mentions this briefly, but it should be emphasized that every node carries the "mass penalty" of coordinator capability, even if used only 1% of the time.
4.  **Table VI (Bandwidth Breakdown):** The "Global-State Mesh" column lists ">1 kbps" and "Exceeds." It would be more impactful to list the actual calculated requirement (e.g., "~73 MB/cycle" as derived in Table II) to emphasize the magnitude of the disparity.
5.  **Reference Format:** Reference [1] and [3] are non-archival websites. While necessary for current constellations, ensure the access dates are consistent and consider adding a "snapshot" or archival link (e.g., Wayback Machine) if allowed by IEEE style, to ensure long-term validity.

## Overall Recommendation

**Accept with Minor Revisions**

This is a high-quality paper that contributes significant quantitative insights to the design of future large-scale space systems. The methodology is rigorous, the writing is clear, and the results are non-trivial. The minor revisions suggested above will clarify physical-layer assumptions and strengthen the practical engineering applicability of the findings.

## Constructive Suggestions

1.  **Enhance the "Physical Layer Abstraction" discussion:** Explicitly mention that while the DES models the *network* capacity, the *pointing and acquisition* challenges of optical ISLs for dynamic clustering are a separate, non-trivial mechanical constraint. This protects the paper from criticism regarding the feasibility of "switching" coordinators instantly.
2.  **Expand on the "Sectorized Mesh" Logic:** In Section V-A, explicitly state that the Sectorized Mesh is essentially a "static hierarchy" (fixed geographic/orbital sectors) vs. the "dynamic hierarchy" (logic-based clusters) of the main architecture. This conceptual framing helps readers understand why the overheads differ.
3.  **Visualizing the "Zero-Drop" Threshold:** Figure 5 (TDMA comparison) is excellent. Consider adding a small subplot or overlay showing the "Burstiness Factor" (Peak Rate / Mean Rate) as a function of $N$ or $k_c$. This would visually prove why the 50 kbps threshold is necessary despite low mean utilization.
4.  **Future Work - Edge Computing:** In the discussion (Section V), briefly mention that "Coordinator Processing" ($\mu_c$) might not just be message routing but also *distributed orbit determination*. If the coordinator performs OD for the cluster, the CPU load increases significantly. Acknowledging this would connect the comms analysis to the compute analysis.