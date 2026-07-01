---
paper: "02-swarm-coordination-scaling"
version: "bx"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

Here is a comprehensive peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version BX), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

***

# Peer Review Report

**Manuscript ID:** [Version BX]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## Review Criteria

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This paper addresses a critical and timely gap in the literature: the specific scaling properties of coordination architectures for mega-constellations ($10^3$--$10^5$ nodes). While existing literature covers swarm robotics (small scale) and traditional constellation management (centralized, medium scale), the "middle ground" of massive, autonomous fleets remains under-explored, particularly regarding the specific byte-level constraints of RF backup links.

The derivation of closed-form sizing equations (specifically the distinction between byte-budget, MAC efficiency, and TDMA airtime feasibility layers) is a significant contribution. The identification of the "stress-case" command traffic as the dominant factor over topology-specific overhead challenges the common assumption that maintenance traffic (heartbeats/election) is the primary scaler. This work will likely serve as a reference for systems engineers sizing future autonomous constellations.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology combines analytical derivation, Cycle-Aggregated Discrete Event Simulation (DES), and a slot-level TDMA simulator. This triangulation is robust. The authors clearly distinguish between what is modeled (message-layer events, queueing) and what is abstracted (physical layer, antenna pointing). The use of Gilbert-Elliott (GE) models to capture correlated channel losses is appropriate for the LEO environment.

However, there is a slight disconnect regarding the "Sectorized Mesh" baseline. The paper acknowledges it is a "local-neighborhood baseline" rather than a full coordination architecture, yet compares its overhead directly to the hierarchical model. While the authors are transparent about this difference in functional scope (Table VI), the direct overhead comparison in Figure 10 could be misleading without stronger caveats that the mesh is performing a *different* job than the hierarchy.

### 3. Validity & Logic
**Rating: 5 (Excellent)**

The logic is rigorous. The authors systematically dismantle the problem into three layers (Byte, MAC, Airtime) and validate each. The "Validation Gap" section (V-A) is particularly refreshing; the authors honestly map which claims are supported by which verification method (Analytical vs. DES vs. Slot-sim).

The conclusion regarding ARQ infeasibility under slow-mixing GE channels is well-supported by the data. The distinction between broadcast (Type 1) and unicast (Type 2) command dissemination is crucial, and the derivation of the 22-cycle stagger requirement for unicast is a strong, logical finding that dictates operational constraints.

### 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is dense but well-structured. The progression from Introduction $\to$ Simulation Framework $\to$ Results $\to$ Discussion is logical. The use of "Design Equations" summaries in the Discussion is very helpful for practitioners.

*Minor critique:* The density of acronyms and variables in the Abstract is high. It reads more like a results summary than a high-level overview. Additionally, the distinction between "Coordinator Ingress" (RX) and "Coordinator Egress" (TX) could be made sharper in the early sections, as the bottleneck shifts between them depending on the workload profile (ingress-limited for status reports, egress-limited for unicast commands).

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors include a specific acknowledgment regarding AI-assisted ideation (Claude, Gemini, GPT), citing a specific internal report/policy. This transparency meets and exceeds current ethical standards for AI disclosure in academic publishing. No conflicts of interest are apparent.

### 6. Scope & Referencing
**Rating: 5 (Excellent)**

The paper fits perfectly within the scope of *IEEE TAES*, bridging the gap between aerospace systems engineering and electronic communications. The references are comprehensive, covering historical foundations (Kleinrock, Lamport), current operational systems (Starlink, OneWeb), and relevant protocols (CCSDS, DTN). The inclusion of recent "mega-constellation" networking papers (Handley, del Portillo) ensures the work is situated in the current state-of-the-art.

---

## Major Issues

1.  **Sectorized Mesh Comparability:**
    In Section III-B-4 and Table VI, the authors define the Sectorized Mesh as having a "capped" neighbor count (approx. 10 neighbors). However, the Hierarchical architecture provides 100% cluster coverage ($k_c=100$). The paper compares the overhead ($\eta$) of these two approaches, concluding the hierarchy is more efficient. This is an "apples-to-oranges" comparison because the functional output (state awareness) differs by an order of magnitude.
    *   *Requirement:* The authors should explicitly label the overhead comparison as "Cost per Unit of State Awareness" or otherwise normalize the metric. Alternatively, explicitly state that the Mesh overhead is *higher* despite providing *lower* awareness, which strengthens the argument for hierarchy but requires careful phrasing to avoid attacking a strawman.

2.  **Coordinator Failure & Recovery Latency:**
    Section III-B-2 mentions a "Nominal handoff" of 3-5s via Optical ISL, but an "RF-backup handoff" of ~160s. The results section (IV) focuses heavily on the RF-backup regime (1 kbps). If a coordinator fails during an RF-backup event (e.g., a solar storm disabling ISLs), the system is blind for 160s (16 cycles).
    *   *Requirement:* The impact of this 160s gap on the "Stress Case" needs to be addressed. If a command campaign is active and the coordinator fails, does the 22-cycle stagger reset? Does the fleet enter a safe hold? A brief discussion on the *operational impact* of this recovery latency during the critical RF-backup mode is needed.

---

## Minor Issues

1.  **Abstract Density:** The abstract contains too many parenthetical numerical results (e.g., "$\eta_S \approx 46\%$", "$\gamma = 0.85$", "24 kbps"). Consider smoothing the text to focus on the *trends* and *implications*, leaving the specific numeric values for the body or a "Highlights" bullet list.
2.  **Table I (Notation):** The definition of $\eta$ is given as "Protocol overhead... beyond baseline." Later, $\eta_{total}$ is defined. In some figures (Fig. 10), the axis is just "Overhead." Please ensure strict consistency in usage between $\eta$ (protocol only) and $\eta_{total}$ (protocol + baseline) throughout all figures and captions.
3.  **Section IV-A (TDMA Frame):** The derivation of $\gamma = 0.949$ is presented, but then the paper reverts to $\gamma = 0.85$ for conservatism. This is good engineering practice, but the justification "control-channel overhead" is vague. Explicitly mentioning "guard bands for clock drift" or "ranging slots" here would strengthen the justification for the 0.85 value.
4.  **Figure 5 (Fleet Reuse):** The caption mentions "Frequency x Spatial reuse products." The axes or legend should clearly indicate that the curves represent different $F \times R$ values. Currently, it requires inferring from the text.
5.  **Typos/Grammar:**
    *   Section III-A: "DES cycle update... (5) coordinator ingress: fluid server..." -> Clarify that this is the *model* behavior, distinct from the *physical* TDMA behavior.
    *   Section IV-E: "Topology-invariance of $\eta_{cmd}$ is therefore specific to centralized command generation..." -> This is a crucial sentence; consider italicizing "centralized command generation" for emphasis.

---

## Overall Recommendation

**Minor Revision**

This is a high-quality manuscript that offers significant contributions to the field of autonomous spacecraft coordination. The analytical derivations are sound, and the simulation strategy is robust. The "Major Issues" identified above relate primarily to the framing of comparisons and the operational interpretation of failure modes, rather than fundamental flaws in the data or mathematics. With these clarifications, the paper will be an excellent addition to *IEEE TAES*.

---

## Constructive Suggestions

1.  **Add a "Cost-Benefit" Plot for Topology:** To address Major Issue #1, consider a plot with "State Awareness (Nodes monitored)" on the X-axis and "Bandwidth Overhead ($\eta$)" on the Y-axis. This would visually demonstrate that the Hierarchical model sits at a much more favorable operating point than the Sectorized Mesh, resolving the "apples-to-oranges" concern by showing the efficiency frontier.
2.  **Expand the "Safe Mode" Discussion:** Since the 1 kbps regime is the "design-driving edge case" (Section III-E), explicitly list the "Load Shedding" priority. If the system enters RF backup, does it automatically drop the "Event" profile and switch to "Nominal"? This operational logic would complete the sizing picture.
3.  **Clarify "Unicast Stagger" Implications:** The 22-cycle stagger for unicast commands is a standout result. Suggest adding a sentence to the Abstract or Conclusion explicitly stating: *"Operators must rely on broadcast-addressed commands for emergency safing; individual node retasking is not real-time feasible in the RF-backup band."* This is a vital takeaway for mission designers.