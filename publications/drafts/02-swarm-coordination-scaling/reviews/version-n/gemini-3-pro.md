---
paper: "02-swarm-coordination-scaling"
version: "n"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-24"
recommendation: "Major Revision"
---

## Peer Review: IEEE Transactions on Aerospace and Electronic Systems

**Manuscript Title:** Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study
**Authors:** Project Dyson Research Team

---

### 1. Significance & Novelty
**Rating: 4 / 5**

The manuscript addresses a timely and critical challenge in aerospace engineering: the scalability of command and control (C2) architectures for mega-constellations and future autonomous swarms ($10^3$–$10^5$ nodes). As commercial constellations like Starlink and Kuiper expand, and future architectures (like sparse aperture arrays) are proposed, the transition from human-in-the-loop ground control to autonomous coordination is inevitable.

The paper’s novelty lies in its rigorous quantitative characterization of the "middle ground" architecture—hierarchical coordination—operating between the well-understood extremes of centralized control and fully distributed mesh. While the theoretical $O(N)$ scaling of hierarchical trees is known, the specific quantification of protocol overhead ($\eta \approx 20.66\%$) via full-participation Discrete Event Simulation (DES) provides valuable engineering data. The inclusion of practical engineering constraints, such as coordinator duty cycles, power variance, and exception-based telemetry, significantly enhances the paper's utility for system designers.

### 2. Methodological Soundness
**Rating: 3 / 5**

The DES framework appears robust. The use of full-participation simulation (no sampling) for up to $10^5$ nodes is computationally impressive and adds confidence to the results. The statistical treatment (30 Monte Carlo replications, bootstrap confidence intervals) is excellent.

However, there is a significant methodological weakness regarding the **Reference Baselines**, specifically the "Centralized Ground Processing" model. The authors model the centralized baseline as a single-server $M/D/1$ queue ($c=1$). As acknowledged in Table I, this creates an artificial processing bottleneck at $N \approx 10^4$. In reality, modern ground segments utilize hyperscale cloud computing (effectively $M/D/c$ where $c \to \infty$), meaning the bottleneck for centralized control is almost never *processing* latency, but rather *spectrum availability* (uplink bandwidth) and *propagation latency*. By focusing on the processing bottleneck (Fig. 2, Fig. 3), the paper sets up a "strawman" argument. The comparison would be much sounder if the centralized baseline failed due to bandwidth saturation rather than CPU saturation.

Additionally, the abstraction of the MAC layer (Table III) is a limitation. The paper claims "no queueing-induced nonlinearities," but this applies only to the message-layer queue. At offered loads of 40%+ (Table VIII), physical layer contention (ALOHA collisions or TDMA scheduling overhead) would introduce significant nonlinearities that the DES does not capture.

### 3. Validity & Logic
**Rating: 4 / 5**

The conclusions regarding the hierarchical architecture itself are logically sound and supported by the data. The finding that overhead scales constantly with $N$ is mathematically consistent with the fixed-depth hierarchy model. The analysis of cluster size ($k_c$) trade-offs is nuanced, correctly identifying that the optimization is driven by latency (regional queueing) rather than overhead.

The validation of exception-based telemetry (Section IV-F) is a strong addition, demonstrating a clear path to bandwidth reduction. The coordinator bandwidth stress test (Section IV-G) provides a critical "reality check," correctly identifying that while fleet-average bandwidth is low, the coordinator node requires significantly higher ingress capacity ($\geq 50$ kbps).

The primary validity concern remains the framing of the comparative results against the baselines. The statement that centralized architectures "diverge" at $10^4$ nodes (Fig. 2) is an artifact of the specific simulation parameters ($c=1$) rather than a fundamental property of centralized architectures, whereas the bandwidth saturation of the Global Mesh is a fundamental physical limit.

### 4. Clarity & Structure
**Rating: 5 / 5**

The manuscript is exceptionally well-written. The structure is logical, following a standard progression from problem definition to model description, results, and discussion. The distinction between "Baseline Telemetry" and "Protocol Overhead" is defined clearly in Section III-F, which is crucial for interpreting the results.

Figures are high-quality and informative. Tables are dense but well-organized; Table I (Scalability Sensitivity) and Table III (Abstraction Scope) are particularly helpful for contextualizing the study's boundaries. The writing style is appropriate for *IEEE TAES*, striking a balance between academic rigor and engineering practicality.

### 5. Ethical Compliance
**Rating: 5 / 5**

The authors provide a clear acknowledgment of AI-assisted ideation in the Acknowledgment section, citing specific models used, which aligns with emerging transparency standards. No human subjects are involved. The research appears ethically sound.

### 6. Scope & Referencing
**Rating: 4 / 5**

The scope is well-aligned with *TAES*. The referencing is adequate, covering standard texts in queueing theory (Kleinrock), distributed algorithms (Lynch), and swarm robotics (Brambilla, Dorigo).

The paper would benefit from stronger referencing regarding **Sectorized/Partitioned Mesh** approaches. The authors mention this as a "practical decentralized alternative" in the introduction and discussion, but given that this is the true competitor to hierarchical systems (rather than the $O(N^2)$ global mesh), more literature on distributed hash tables (DHTs) or spatial gossip protocols in ad-hoc networks would strengthen the context.

---

### Major Issues

1.  **The "Single-Server" Strawman (Section III-B-1 & Figs. 2-3):**
    The paper argues that centralized architectures fail at $10^4$ nodes based on a single-server ($c=1$) processing model. This is a weak argument in the era of cloud computing. A centralized system for $10^5$ satellites would undoubtedly use parallel processing.
    *   *Required Revision:* The authors must reframe the failure mode of the centralized baseline. The argument should focus on **Uplink Bandwidth Saturation** (spectrum scarcity) and **Propagation Latency** (speed of light), which are physical invariants, rather than processing queues which can be arbitrarily scaled. Figures 2 and 3 should ideally be annotated or modified to reflect that the "Centralized" curve divergence is a parameter choice ($c=1$), or the baseline should be adjusted to assume infinite processing capacity ($c=\infty$) to highlight the *true* bottlenecks (bandwidth/latency).

2.  **Physical Layer/MAC Abstraction Implications (Section V-E):**
    The paper reports an offered load of up to 42% (Table VIII) and claims robust operation. In a real shared medium (RF or Optical), 42% utilization is dangerously high for random access protocols (Slotted ALOHA maxes at 36%) and requires significant overhead for scheduled protocols (TDMA).
    *   *Required Revision:* The authors need to qualify the "robustness" claims. A discussion or analytical estimation of MAC overhead must be added. For example, if a TDMA guard-band efficiency of 80% is assumed, the "effective" utilization is much higher. The claim of "no queueing-induced nonlinearities" must be explicitly restricted to the *network/application layer*, acknowledging that the physical layer *will* exhibit nonlinearities at these loads.

### Minor Issues

1.  **Figure 3 Extrapolation:** The figure includes a dashed line for $10^6$ nodes labeled "Analytical extrapolation." Given the nonlinearities in regional coordinator queueing mentioned in the text, visual extrapolation is risky. Please ensure the caption heavily emphasizes that this specific curve is *not* DES-validated.
2.  **Power Variance (Section IV-D):** The discussion on power variance is good, but Eq. 10 calculates the *average* power overhead. For spacecraft thermal design, the *peak* power dissipation (when acting as coordinator) is the sizing driver, not the average. The text mentions this, but it should be emphasized that every node must carry the thermal mass for the "Coordinator Mode" worst-case, which is a non-trivial spacecraft design penalty.
3.  **Table II (Collision Avoidance Rate):** The rate $10^{-4}$/node/s seems very high for actual maneuvers. The footnote explains this includes screening alerts, but it would be helpful to explicitly state the ratio of "alerts" (messages) to "maneuvers" (delta-v) to avoid confusing readers familiar with debris operations.
4.  **Abstract:** "Total coordination-channel utilization including baseline is ~41%." This is a key number. It should be made clear that this is *per node* average, but the coordinator node sees $k_c$ times this traffic (as detailed later in the paper).

### Overall Recommendation
**Major Revision**

*Justification:* While the simulation work on the hierarchical architecture is excellent, the comparative analysis relies on a "strawman" representation of centralized control (processing-limited rather than bandwidth-limited). This framing significantly distorts the comparative results in the Abstract, Introduction, and Figures 2/3. The paper needs to pivot its argument to compare Hierarchical vs. Centralized (Bandwidth Limited) vs. Mesh to be technically defensible. Once this framing is corrected and the physical layer limitations are more explicitly bounded, the paper will be a strong contribution.

### Constructive Suggestions

1.  **Pivot the Centralized Baseline:** In Section III-B-1, calculate the aggregate uplink bandwidth required for $10^5$ nodes (e.g., $10^5 \times 1 \text{ kbps} = 100 \text{ Mbps}$). Compare this against the capacity of a single ground station antenna (e.g., S-band or X-band limits). Use *this* as the saturation point for centralized control, rather than the artificial $M/D/1$ queue limit. This strengthens the argument for hierarchical/distributed systems significantly.
2.  **Add a "MAC Efficiency Factor":** In the results (specifically Table VIII and the Coordinator Bandwidth section), introduce a parameter $\gamma$ (MAC efficiency, e.g., 0.8 for TDMA). Scale the required bandwidths by $1/\gamma$. This acknowledges the physical layer reality without requiring a full PHY simulation.
3.  **Strengthen the "Sectorized Mesh" Discussion:** Since the Global Mesh is an upper bound, explicitly discuss how a Sectorized Mesh (gossiping only with $k$ nearest neighbors) would likely perform. It would likely have $O(N)$ total overhead (like hierarchical) but higher latency due to multi-hop propagation. This places the Hierarchical architecture in better context: it optimizes for *latency* via the tree structure compared to the flat mesh.
4.  **Clarify "Offered Load" vs. "Throughput":** In Table VIII, clearly distinguish that "Offered Load" is the metric for Link Budgeting, while "Delivered $\eta$" is the metric for Coordination Quality. Explicitly state that link budgets must close at the Offered Load level.