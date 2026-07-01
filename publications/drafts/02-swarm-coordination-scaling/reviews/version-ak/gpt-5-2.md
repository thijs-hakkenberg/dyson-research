---
paper: "02-swarm-coordination-scaling"
version: "ak"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-27"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 4/5 (Good)**

The manuscript targets a real and increasingly urgent problem: control-plane scaling for autonomous coordination in very large LEO-scale swarms/mega-constellations (10³–10⁵, with discussion toward 10⁶). The paper’s core novelty is not “hierarchy is scalable” (well-known), but the **explicit byte-level control-plane accounting under a strict per-node budget** combined with (i) coordinator ingress sizing under burstiness models, (ii) AoI quantification for exception telemetry, and (iii) correlated-loss effects with intra- vs inter-cycle recovery—validated via a fast cycle-aggregated DES and repeatedly cross-checked analytically. That combination is relatively uncommon in the space-systems literature, and the paper is careful to position the DES as a compositionality/verification tool rather than a discovery engine, which is an honest and appropriate framing.

The work is also valuable in how it **separates workload-driven overhead (commands) from topology-driven overhead (summaries/aggregation)**; Fig. “decomposition” and the discussion in Sec. IV-E are particularly helpful. The “design envelope” idea (nominal/event-driven/stress) is a strong contribution for practitioners: it clarifies that the headline 46% is largely a workload assumption rather than an inherent hierarchy penalty.

That said, some novelty claims are slightly overstated. The statement in the Introduction that “no prior work has systematically compared coordination architectures … using quantitative simulation with explicit byte-level traffic accounting under a fixed per-node coordination budget” is plausible but needs tighter qualification and stronger citation support. Related work on constellation networking/control, DTN control planes, and hierarchical management in large networks exists; your contribution is the specific *combination* of assumptions, scale range, and metrics. I recommend softening the absolute phrasing and explicitly delimiting what “coordination” excludes (e.g., routing, MAC, pointing) to avoid reviewers reading this as a networking paper claiming first-of-kind.

---

## 2. Methodological Soundness — **Rating: 3/5 (Adequate)**

The cycle-aggregated DES is appropriate for the stated goal: message-layer offered-load sizing and scaling comparisons. The manuscript is commendably explicit about what is modeled vs abstracted (Table “Simulation Abstraction Scope”), provides parameters (Table “Simulation Parameters”), and offers code/data availability. The analytic cross-checks (AoI geometric tail in Eq. (AoI_P99), retransmission under Bernoulli/GE, and bandwidth arithmetic) are a strong methodological feature and increase confidence that the DES is not producing numerology.

However, several modeling choices materially affect the headline results and are not yet justified to the level expected for T-AES:

* **Control-plane budget interpretation**: Sec. “Communication Overhead Definition” treats 1 kbps/node as a *budget* rather than a physical link rate, and then introduces coordinator pooling (C_coord) and a MAC efficiency factor γ as a scalar. This is reasonable as a first-order study, but it means the results are **highly sensitive to unmodeled MAC/pointing/acquisition**, and those sensitivities are not quantified beyond γ ∈ [0.7, 0.9] and a brief Slotted ALOHA comparison. For many realistic RF backup regimes, γ and contention are not constants; they depend on offered load and topology. Because several key findings hinge on coordinator ingress thresholds (21–50 kbps) and “independence” of drops vs GE losses, the lack of an explicit MAC/channel model is a bigger methodological gap than the paper currently implies.

* **Queueing and timing consistency**: The paper mixes queueing abstractions (M/D/1 at ground, “pipeline capacity” for coordinators, deterministic per-message processing delay) with cycle-based budget enforcement (Model A/B) and a “vectorized” per-cycle update. This can be consistent, but the manuscript needs a clearer statement of how queueing is actually implemented in the DES for coordinators and regionals. For example: are coordinator arrivals timestamped within-cycle (random phase), queued with service time 5 ms, and then compared to capacity, or is capacity enforced purely by byte budget independent of service? Some results (e.g., latency values in Table “cluster_size”) suggest burst/queue effects at the regional tier, but the implementation description emphasizes per-cycle aggregation and byte drops. A short pseudocode block or more precise algorithmic description would help.

* **Monte Carlo framing**: You run 30 replications but then state overhead SD < 0.001% and that MC mainly confirms low variance. That is fine, but then several tables report counts of drops (Table “joint_interaction”) without confidence intervals and without stating whether those numbers are per-year totals, per-run means, etc. If the system is near-deterministic, report single-run deterministic outputs; if not, provide uncertainty consistently. Right now it reads as “Monte Carlo” without leveraging it rigorously.

Overall, the methods are reproducible and mostly appropriate, but the paper needs stronger alignment between the abstractions and the claims, especially where “architecture independence/compositionality” is asserted.

---

## 3. Validity & Logic — **Rating: 3/5 (Adequate)**

Many conclusions are directly supported by arithmetic or by the DES with analytic cross-checks. The AoI result is particularly solid: Eq. (AoI_P99) matches Table “AoI results” tightly, and the manuscript correctly interprets the trade: exception telemetry buys bandwidth at the cost of state staleness. The correlated-loss discussion is also logically consistent: GE bursts reduce intra-cycle ARQ effectiveness, and the paper appropriately distinguishes orbital coordination timescales from real-time collision avoidance.

The main validity concern is that several “system-level” conclusions depend on **structural assumptions that are not fully defended**:

* **Coordinator ingress sizing (21–50 kbps)**: The 50 kbps “deadline model” is described as conservative, but the logic for why a coordinator “cannot use stale partial reports from a previous cycle” (Model A) is application-dependent. Many coordination functions can incorporate late/stale updates with time tags (especially if AoI is already a metric). If Model A is not representative, the upper bound may be misleadingly prominent. Conversely, Model B assumes token-bucket smoothing and carry-over that may not be realizable under strict time-tagging and bounded-latency constraints. You should connect Model A/B to specific coordination tasks: e.g., conjunction screening vs formation keeping vs distributed scheduling.

* **Independence claim (Sec. IV-D)**: The “GE retransmissions add 22% offered load but produce zero additional coordinator drops” result is true under your event ordering (loss occurs before coordinator ingress). But it is not a general property of point-to-point ISLs; it is a property of **non-shared ingress capacity modeling** where each member link loss prevents arrival and the coordinator capacity constraint is enforced only on arrived bytes. In a real coordinator receiver, the bottleneck could be RF front-end time, demod resources, or scheduled receive windows; retransmissions can consume those resources even if they fail decoding. You do acknowledge shared-medium contention, but the claim as written is still somewhat strong; it should be reframed as “independent in this abstraction where coordinator capacity is modeled as an arrival-side byte budget after link loss.”

* **Centralized baseline interpretation**: The “realistically provisioned centralized baseline (c = N/k_c) does not diverge computationally until N≈10⁶” is plausible, but the paper simultaneously says centralized constraints are propagation latency and uplink spectrum. Those are indeed key, but the paper’s centralized model is mostly compute/queueing focused (M/D/1, M/D/c). If the argument is that compute is not binding, then either (i) the centralized baseline should explicitly model spectrum/ground contact constraints, or (ii) the discussion should be clearly labeled as qualitative extrapolation. Right now there is a mismatch between what is simulated and what is used to argue “hierarchical advantage.”

Limitations are acknowledged (Sec. V-B), but several headline statements in the Abstract and Conclusion read stronger than what the abstraction strictly supports. Tightening claim language and explicitly mapping each claim to modeled vs unmodeled phenomena would improve logical validity.

---

## 4. Clarity & Structure — **Rating: 4/5 (Good)**

The manuscript is generally well organized, with a clear roadmap at the start of Results, and strong use of tables to define traffic accounting and parameters. The explicit definition of η (protocol overhead beyond baseline telemetry) and the offered vs delivered distinction are particularly helpful and reduce ambiguity that often plagues control-plane sizing papers.

Figures and tables appear thoughtfully chosen (architecture diagram, overhead scaling, decomposition, AoI, GE comparison, phase staggering). The narrative is mostly readable for a T-AES audience spanning autonomy, comms, and systems engineering. The “Baseline Interpretation Note” early on is a good idea; it anticipates reviewer confusion about the centralized and global-mesh baselines.

Areas needing clarity improvements:

* **Section numbering inconsistencies**: You refer to “Section V-C” in Sec. 3.1 (“discussed in Section V-C”), but the Discussion section is Section V and its subsections are V-A/V-B; there is no V-C unless omitted in the excerpt. There are several “old IV-…” comments in headings (e.g., “merged from old IV-H + IV-K”) which should be removed for submission.

* **Ambiguity about what is in η**: Table “Traffic Accounting” excludes ephemeris status reports from η as topology-invariant baseline. Yet many results and plots discuss η as “fraction of bandwidth consumed by coordination messages beyond baseline telemetry.” This is fine, but the Abstract states “under a 1 kbps per-node control-plane budget” and reports η ranges; a reader may misinterpret η as total utilization. You do later define η_total = baseline + overhead; consider reporting both more consistently, especially when discussing saturation (e.g., link availability table notes offered including baseline exceeds 100% but the footnote labeling is confusing: Table “link_availability” has superscripts that do not match the notes cleanly).

* **Latency definition vs results**: Latency is defined as end-to-end including propagation and queueing, but the reported latencies (e.g., 340–675 ms in Table “cluster_size”) seem dominated by queueing/burst at regional tier. It would help to show a breakdown (propagation vs processing vs queueing) for at least one configuration so the reader understands what drives those numbers.

Overall, the paper is close to publishable in clarity, but it needs careful polish to remove internal drafting artifacts and tighten definitions.

---

## 5. Ethical Compliance — **Rating: 4/5 (Good)**

The manuscript includes an explicit AI-assisted ideation disclosure in the Acknowledgment, stating that AI tools contributed to concept ideation and that this is described in a companion methodology paper. That is aligned with emerging transparency expectations. The disclosure also appropriately states that the “Shepherd/Flock” concept is not validated here, reducing the risk of overstating AI-derived content.

Two items to address:

1. **Authorship and affiliations**: The author block currently uses a placeholder (“Project Dyson Research Team… names will be provided”). IEEE policy typically requires author identities at submission for peer review (even if blinded review is not used), and T-AES does not generally accept anonymous author placeholders at review stage. This is an administrative/ethical compliance issue rather than technical, but it must be fixed before the paper can proceed.

2. **Potential conflict of interest**: The paper points to Project Dyson and provides a repository and web simulators. That is good for reproducibility, but it also suggests an organizational agenda. A brief conflict-of-interest statement (even “none”) and a statement about funding/support would strengthen compliance norms.

---

## 6. Scope & Referencing — **Rating: 3/5 (Adequate)**

The topic fits T-AES: large-space-system autonomy, coordination architectures, and control-plane scaling with realistic operational constraints. The paper’s emphasis is systems/architecture with quantitative comms/queueing metrics, which is in-scope.

Referencing is broad and includes key classics (Lynch, Demers gossip, Kleinrock, Lamport, Raft, AoI survey) and relevant space networking (Handley, CCSDS BPv7, Proximity-1). However, several citations are **non-archival web pages or program fact sheets** (Starlink ops page, Kuiper overview, DARPA pages). These are acceptable as context but should not be used as primary technical evidence. In particular, claims about Starlink operations scale and ground coordination would benefit from more archival sources (e.g., FCC filings, peer-reviewed/archival analyses, or operator technical papers if available).

Additionally, the paper would benefit from citing more directly relevant work on: (i) constellation control/operations architectures (including autonomy and collision avoidance operations), (ii) control-plane design for large distributed systems (hierarchical monitoring/aggregation literature), and (iii) satellite ISL MAC scheduling and time synchronization constraints (beyond CCSDS Prox-1). Right now, the paper sometimes uses terrestrial distributed systems references to justify space-specific claims; that’s not wrong, but T-AES reviewers will expect stronger anchoring in aerospace comms/ops literature.

---

## Major Issues

1. **Coordinator capacity and “independence” results hinge on an abstraction that may not map to real receiver/MAC constraints.**  
   *Where:* Sec. IV-A (Models A/B/TDMA), Sec. IV-D (joint independence).  
   *Why it matters:* The 21–50 kbps coordinator ingress sizing and the claim that GE retransmissions do not increase coordinator drops depend on modeling coordinator capacity as a post-loss byte budget (arrivals that fail the link never consume coordinator capacity). In real systems, retransmissions consume time/frequency resources and receiver attention even if decoding fails, and capacity is often a function of scheduled receive windows and demod resources.  
   *What to change:* Reframe claims as “within this message-layer abstraction,” and add at least one alternative capacity model where retransmission attempts consume coordinator ingress opportunity (e.g., scheduled slot occupancy), or explicitly justify why the chosen model is appropriate for optical point-to-point ISLs with independent links.

2. **Centralized baseline comparison is not modeled on the actual binding constraints you cite (spectrum/contact), weakening the “hierarchy advantage” argument.**  
   *Where:* Sec. III-B (centralized model), Sec. IV-F (topology comparison), Abstract/Conclusion statements about uplink spectrum and outages.  
   *Why it matters:* The paper argues compute is not limiting (fine), and then claims spectrum and outages are limiting, but those are not simulated or quantified with the same rigor as η and coordinator ingress.  
   *What to change:* Either (i) add a simple ground-contact/spectrum model (duty cycle of ground access, aggregate uplink capacity, outage process) and quantify impact on AoI/availability, or (ii) clearly label those as qualitative considerations and reduce the strength/centrality of those conclusions.

3. **Unclear implementation/definition of latency and queueing in the DES.**  
   *Where:* Sec. III-A, Table “cluster_size,” Fig. “latency distribution.”  
   *Why it matters:* Latency is a key metric in RQ1/RQ2, but it’s not clear how the cycle-aggregated model produces sub-second latency distributions when most events are cycle-based, nor how regional bursts are queued.  
   *What to change:* Provide a precise algorithmic description (or pseudocode) for latency computation and queue servicing at coordinators/regionals, and include a latency component breakdown for one representative case.

4. **Manuscript contains submission-blocking drafting artifacts and policy issues.**  
   *Where:* Section headings with “merged from old…”, placeholder authorship, internal cross-references (“Section V-C”).  
   *Why it matters:* These will trigger immediate desk rejection or major revision requests in an IEEE journal workflow.  
   *What to change:* Remove internal notes, fix cross-references, provide full author list/affiliations (even if later anonymized is desired, which is not typical for T-AES), and ensure all figures/tables referenced exist and are consistent.

---

## Minor Issues

- **Table “link_availability” footnotes/superscripts appear inconsistent**: The table references superscripts a/b/c but the footnote text labels do not match cleanly (e.g., “\textsuperscript{b}” used twice with different meanings; “\textsuperscript{c}” referenced but not in header consistently).  
- **Eq. (mesh_convergence) and diameter scaling**: You state for a random geometric graph in 3D orbital space, \(D = O(N^{1/3})\). For satellites on (approximately) 2D shells with constrained neighbor relations, the effective dimension may be closer to 2; at least qualify this or cite a relevant result.  
- **Sector size heuristic** (Sec. “Sectorized Mesh”): The derivation mixes shell geometry and screening radius scaling. It’s fine as a heuristic, but the text should more clearly separate “assumed scaling” from “derived.”  
- **Handoff transfer time arithmetic**: In “Handoff” metric definition, you state 10–50 MB at 1 Gbps completes in 80–400 ms; later in Sec. “Hierarchical Topology” you say 1–10 seconds. These should be reconciled (perhaps 1–10 s includes election + pointing/acquisition + protocol overhead).  
- **Use of non-archival citations in technical claims**: Starlink ops web page, DARPA program pages, etc. Keep them for context but avoid using them to support quantitative claims.  
- **Remove internal commentary** like “merged from old IV-…” and ensure IEEE style consistency (e.g., “Section~V-C” vs actual structure).

---

## Overall Recommendation — **Major Revision**

The paper is promising and has several strong, publishable components (byte-level accounting, AoI trade curves with analytic validation, correlated-loss implications, and coordinator ingress sizing under different smoothing assumptions). However, key claims—especially the coordinator capacity guidance and the “independence/compositionality” conclusion—depend on abstractions that are not yet convincingly tied to realistic MAC/receiver constraints, and the centralized baseline comparison relies on constraints that are not modeled with comparable rigor. Combined with several submission-blocking presentation/policy issues, the manuscript requires substantial revision to meet T-AES standards.

---

## Constructive Suggestions

1. **Strengthen the mapping from abstraction to physical/MAC reality (one concrete validation).**  
   Add a small “single-cluster MAC sanity check” section: even a simplified TDMA slot model where retransmission attempts consume slot opportunities (success or fail) would let you test whether the IV-D “independence” still holds under scheduled access. Alternatively, explicitly state that coordinator capacity is *post-decoding goodput* rather than *airtime capacity* and adjust language accordingly.

2. **Quantify the centralized baseline’s true bottlenecks with a minimal ground-contact/spectrum model.**  
   Introduce a simple model: ground contact windows, aggregate uplink capacity cap, outage process, and resulting AoI/command delay. Then compare hierarchical vs centralized on *availability/AoI under outages* quantitatively, not just narratively. This would directly support the claims in Sec. IV-F and the Abstract/Conclusion.

3. **Clarify DES mechanics for latency and queueing with pseudocode and a breakdown figure/table.**  
   Provide an algorithm box describing how arrivals are timestamped within-cycle, how service is applied (deterministic 5 ms), how regional bursts are handled, and how end-to-end latency is computed. Add one table: propagation vs processing vs queueing contributions for \(N=10^5, k_c=100\).

4. **Reframe Model A vs Model B around application requirements (deadline semantics).**  
   Tie Model A (“discard after cycle”) to tasks requiring strict cycle-consistent snapshots; tie Model B (“carry-over”) to tasks tolerant of time-tagged updates. Then present the 50 kbps as “strict snapshot” and 21–25 kbps as “time-tagged state estimation,” reducing ambiguity.

5. **Polish to IEEE submission readiness.**  
   Remove internal merge notes, fix cross-references, reconcile handoff timing numbers, correct table footnotes, and replace/augment non-archival citations for key factual claims. Provide full author list/affiliations and a brief funding/COI statement.