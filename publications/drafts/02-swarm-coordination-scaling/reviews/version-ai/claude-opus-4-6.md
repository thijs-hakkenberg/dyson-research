---
paper: "02-swarm-coordination-scaling"
version: "ai"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuinely important problem: how to coordinate very large autonomous spacecraft swarms at scales beyond current operational experience. The gap identified—systematic comparison of coordination architectures at $10^3$–$10^5$ nodes with byte-level traffic accounting—is real and timely given the trajectory of mega-constellation deployments. The framing around a fixed 1 kbps per-node control-plane budget is a useful engineering constraint that grounds the analysis.

However, the novelty claim is significantly weakened by the paper's own admissions. The authors repeatedly acknowledge that individual metrics are "analytically tractable in isolation" (abstract, Section I-D), that the DES matches closed-form predictions to within 0.1% (Table VII), and that Monte Carlo variance is SD < 0.001%. The $O(1)$ overhead scaling is explicitly stated to be "a direct mathematical consequence of the hierarchical structure" (Section IV-F). The DES thus functions primarily as a calculator for known equations rather than as a tool that reveals new phenomena. The claimed DES contribution—validating "compositional use of single-factor design equations" (Section IV-D)—is interesting but narrow: the independence of GE retransmission and coordinator drops under point-to-point ISLs is intuitive (lost messages never reach the queue) and the paper acknowledges this would not hold under shared-medium architectures, which are arguably more realistic for omnidirectional RF backup links.

The paper would benefit from a sharper articulation of what a practitioner learns from this work that they could not derive from back-of-the-envelope calculations. The coordinator capacity sizing (21–50 kbps) and the AoI geometric-distribution result are useful engineering reference points, but they are not surprising. The most novel contribution is arguably the GE correlated-loss inter-cycle recovery analysis (Section IV-C), which provides actionable design guidance (4–7 cycles to 95% coverage) that is less obvious from first principles.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The simulation framework is clearly described and the parameter space is well-documented (Table III). The cycle-aggregated DES approach is appropriate for the message-layer abstraction, and the authors are commendably transparent about what is and is not modeled (Table IV). The Monte Carlo framework (30 replications, bootstrap CIs) is standard, though the near-zero variance renders it largely ceremonial.

Several methodological concerns arise:

**The centralized baseline is a straw man despite disclaimers.** The $c=1$ single-server model is acknowledged as an "intentional worst-case bound" (Section I-C, III-B.1), but it occupies substantial paper real estate and drives the visual narrative in Fig. 5. The realistic $c = N/k_c$ baseline is introduced almost as an afterthought and reveals that centralized processing "does not diverge computationally until $N \approx 10^6$"—undermining the paper's primary motivation. The authors deserve credit for including this analysis, but the paper's structure still leads with the misleading comparison.

**The global-state mesh upper bound assumes full trajectory replication.** While acknowledged as worst-case, the $O(N^2)$ mesh is not a realistic decentralized architecture. The sectorized mesh (Section III-B.4) partially addresses this, but its $\sqrt{N}$ sector sizing is described as "an order-of-magnitude sizing, not a precise orbital mechanics calculation." The capped-fanout variant (10 neighbors) produces $O(N)$ scaling—the same as hierarchical—making the comparison less about architecture than about the constant factor in front of $N$.

**The collision avoidance event rate ($10^{-4}$/node/s) is questionable.** The authors justify this as 1000× the maneuver rate, but the sensitivity analysis (varying from $10^{-5}$ to $10^{-3}$) shows only ±1.5 percentage points impact on overhead, suggesting this parameter is not actually important to the results. If so, why devote a full paragraph to justifying it?

**The physical-layer TDMA vignette (Section IV-A) conflates cluster geometry with coordination architecture.** The "string of pearls" cluster definition (same shell, RAAN band <2°, true anomaly spread <5°) is highly specific and may not generalize to the diverse orbital geometries in a 100,000-node swarm spanning multiple shells and inclinations. The 500 km cluster diameter assumption deserves more scrutiny.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The analytical cross-checks are thorough and the DES-to-closed-form agreement is excellent (Table VII). The authors are generally careful about qualifying their claims—the AoI-to-position-error coupling (Eq. 12) is explicitly labeled as "order-of-magnitude" and "illustrative back-of-the-envelope." The GE loss analysis correctly identifies the structural ineffectiveness of intra-cycle retransmission during correlated bursts.

However, several logical issues deserve attention:

**The "9× design envelope" framing is misleading.** The spread from $\eta \approx 5\%$ (nominal) to $\eta \approx 46\%$ (stress) is entirely driven by workload assumptions (commanding rate), not architecture properties. The paper acknowledges this (Section IV-E: "dominated by workload assumptions rather than architecture choice") but still leads with it in the abstract. This conflates the protocol's overhead with the application's traffic demand.

**The joint independence result (Section IV-D, Table VI) is less informative than presented.** The finding that "GE retransmissions produce zero additional coordinator drops" follows directly from the architecture: under point-to-point links, a message lost at the link layer never reaches the coordinator queue. The DES confirms this, but the confirmation is trivial given the model structure. The paper would be more honest to state this as a model verification rather than a "key finding."

**The hierarchical advantage quantification is incomplete.** The paper claims the hierarchical advantage is "continuous coordination during ground outages (~9 unhandled events per 15-min outage at $N = 10^5$)" and "elimination of 100 Mbps aggregate uplink demand." The first number (9 events) is derived from the $10^{-4}$/node/s screening rate, which is itself uncertain. The second (100 Mbps) assumes all coordination must flow through ground—but a hybrid architecture with ISL-based collision avoidance and ground-based planning would capture most of the hierarchical benefit without the full hierarchical overhead.

**Extrapolation beyond validated range.** Fig. 6 includes a $10^6$-node curve labeled as "analytical extrapolation, not DES-measured." While the caption is clear, the visual impression may mislead readers about the validated range.

## 4. Clarity & Structure

**Rating: 3 (Adequate)**

The paper is extremely long for a journal article (estimated 12,000+ words of body text plus extensive tables). The level of detail is impressive but borders on exhaustive, with multiple tables and figures that convey overlapping information. The "roadmap" paragraph at the start of Section IV is helpful, but the overall structure could be tightened considerably.

**Strengths:** The traffic accounting tables (Tables V, VI) are excellent and support reproducibility. The design equations summary (Section V-C) is a valuable practitioner reference. The abstraction scope table (Table IV) is unusually transparent for a simulation paper.

**Weaknesses:** The paper reads as if it was written to preemptively address every possible reviewer objection, resulting in extensive footnotes, caveats, and parenthetical qualifications that interrupt the narrative flow. For example, the coordinator bandwidth section (IV-A) presents four different scheduling models, a Chernoff bound heuristic, a TDMA analysis, a physical-layer vignette, and a phase-stagger experiment—any two of which would suffice. The sectorized mesh (Section III-B.4) receives disproportionate attention for what is ultimately a secondary comparator. Table I ($M/D/c$ sensitivity) makes an important point but could be a single sentence: "With $c$ parallel servers, the processing limit shifts to $N_{max} = c \cdot \mu_s / r$."

The abstract is dense but accurate. Figures are referenced appropriately but several (Figs. 1, 5, 6, 7, 8, 9, 10, 11, 12, 13) are described but presumably generated from the code repository—their quality cannot be assessed from the LaTeX source alone.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an explicit acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) in the Acknowledgment section, with a reference to a companion methodology paper. The disclosure is appropriately scoped: the AI tools contributed to "architectural concepts" but the simulation and analysis are attributed to the research team. The data availability statement provides repository links and version tags.

Two minor concerns: (1) The author block uses "Project Dyson Research Team" with a footnote promising individual names for final publication—this is unusual for IEEE and should be resolved before acceptance. (2) The references to future AI models (Claude 4.6, GPT-5.2) that do not exist as of the review date suggest this manuscript may itself be AI-generated or is set in a fictional future timeline. If the former, this should be disclosed per IEEE policy on AI-generated content. The paper's version tag "paper-02-v-ai" in the data availability section reinforces this concern.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is broadly appropriate for IEEE T-AES, though it sits at the intersection of communication systems, distributed computing, and space systems engineering. The reference list (50+ entries) is comprehensive and includes foundational works (Kleinrock, Lamport, Lynch) alongside recent surveys (Dorigo 2021, Yates AoI survey). The related work section adequately positions the contribution.

Several referencing concerns: (1) Multiple references are non-archival (SpaceX website, Amazon website, DARPA program pages, DoD fact sheets)—these should be minimized in a journal publication. (2) The NRL swarm reference [22] is explicitly noted as "non-peer-reviewed." (3) The companion methodology paper [38] is self-published on the project website without peer review. (4) Some important related work is missing: the DTN community has published extensively on store-and-forward protocols for LEO constellations (e.g., Fraire et al., IEEE T-AES 2021); the CCSDS has published scheduling protocols beyond Proximity-1; and the satellite networking community has recent work on ISL topology optimization (e.g., Bhattacherjee and Singla, IMC 2019) that is relevant to the cluster formation assumptions.

The paper does not cite any prior work on hierarchical coordination specifically for satellite constellations, which either means the gap is genuine or the literature search was incomplete. A search for "hierarchical satellite constellation management" or "clustered LEO coordination" would likely surface relevant work from the small satellite and formation flying communities.

---

## Major Issues

1. **The contribution is primarily a parameterized calculator, not a simulation study.** The DES matches closed-form predictions to 0.1% with SD < 0.001%. The paper should either (a) introduce physical-layer or stochastic phenomena that break analytical tractability (MAC contention, orbital geometry, correlated failures) to justify the simulation approach, or (b) reframe the contribution explicitly as a "design handbook" with validated equations, de-emphasizing the DES. Currently, the paper claims DES novelty while demonstrating analytical sufficiency.

2. **The baseline comparisons are structurally unfair.** The $c=1$ centralized and global-state mesh baselines are acknowledged as intentional bounds, but they dominate the visual narrative (Fig. 5) and abstract framing. The realistic centralized baseline ($c = N/k_c$) shows comparable performance to hierarchical up to $N \approx 10^6$. The paper needs to restructure its argument around the *actual* hierarchical advantages (autonomy during ground outages, spectrum independence) rather than processing scalability, which is not the binding constraint.

3. **No orbital mechanics or realistic link geometry.** The paper models communication as abstract message passing with Bernoulli or GE loss, ignoring deterministic Earth occlusion, time-varying ISL topology, and orbital-plane-dependent cluster geometry. For a paper targeting $10^5$ nodes in LEO, the absence of even a simplified orbital model (e.g., Walker constellation geometry) is a significant gap. The "cluster" concept assumes co-moving nodes, but at $10^5$ nodes across multiple shells and inclinations, many clusters will span large angular separations with time-varying visibility.

4. **Questionable AI provenance.** The references to future AI models (Claude 4.6, GPT-5.2) and the version tag "paper-02-v-ai" raise concerns about whether this manuscript was substantially generated by AI tools. If so, this must be disclosed per IEEE's policy on AI-generated content, and the intellectual contribution of the human authors must be clearly delineated.

---

## Minor Issues

1. **Eq. 4 ($M_{\text{total}}$):** Counts only uplink reporting; the text notes bidirectional traffic "approximately doubles" overhead, but the equation should either include both directions or be clearly labeled as uplink-only.

2. **Table III footnote (d):** States $\mu_c = 1/s_{\text{proc}} = 1/0.005 = 200$ msg/s, but this assumes single-threaded processing. The text should note whether multi-threading at the coordinator level is considered.

3. **Section III-B.3:** The convergence time formula $R_{\text{conv}} = \max(\lceil\log_2 N\rceil, \lceil N/(bf)\rceil)$ conflates two different bottlenecks (epidemic spread vs. throughput) without formal justification. A brief derivation or reference would strengthen this.

4. **Table VIII (cluster size):** Latency values show only two discrete levels (340 ms and 508/675 ms) across seven cluster sizes, suggesting the latency model has coarse granularity. This should be explained.

5. **Section IV-A:** The Chernoff bound (Eq. 9) is described as bounding load in a "fixed window" but the actual zero-drop condition requires a scan-statistic maximum. The text acknowledges this but the equation is still presented prominently—consider moving it to an appendix or reducing its prominence.

6. **Notation inconsistency:** $p_{\text{link}}$ is used both as link availability (probability of successful transmission) and as its complement in different contexts. Standardize.

7. **Section III-E:** "Offered vs. delivered distinction" is important but introduced late. Consider moving to Section III-D (metric definitions).

8. **The paper uses "kbps" inconsistently**—sometimes as kilobits per second, sometimes ambiguously. Confirm all instances use SI-consistent notation.

9. **Table IX (duty cycle):** The "Handoff Success" column decreases with longer duty cycles (95% at 1h to 99.9% at 7d), which is counterintuitive since longer cycles mean fewer handoffs. The text explains this is cumulative over 24h, but the table header should clarify.

10. **Fig. 6 caption:** States the $10^6$-node curve is analytical extrapolation, but this caveat should also appear in the figure legend itself.

---

## Overall Recommendation

**Major Revision**

The paper addresses a timely and important problem with commendable transparency about assumptions and limitations. The traffic accounting framework, design equations, and coordinator capacity sizing provide useful engineering reference points. However, the contribution is undermined by three structural issues: (1) the DES adds negligible value beyond closed-form calculations, requiring either more complex phenomena to justify simulation or reframing as a design handbook; (2) the baseline comparisons, while honestly caveated, still create a misleading narrative about hierarchical advantages; and (3) the complete absence of orbital mechanics or realistic link geometry limits applicability to the target domain. The AI provenance question must also be resolved. A major revision addressing these issues—particularly adding at least a simplified orbital model and restructuring the argument around the genuine hierarchical advantages—would substantially strengthen the paper.

---

## Constructive Suggestions

1. **Add a simplified orbital geometry layer.** Even a Walker-delta constellation model with deterministic Earth-occlusion link outages would dramatically increase the paper's relevance to the space systems community. This would also break the analytical tractability of the current model, providing genuine justification for the DES approach. The cluster formation algorithm could then be evaluated against realistic ISL visibility windows.

2. **Restructure the narrative around the genuine hierarchical advantage.** Lead with autonomy during ground outages and spectrum independence (the real binding constraints), not processing scalability. Move the $c=1$ centralized baseline to an appendix or reduce it to a single paragraph. Make the realistic $c = N/k_c$ baseline the primary comparator and frame the hierarchical architecture's value proposition around fault tolerance and ISL-native operation.

3. **Introduce MAC-layer contention for at least one scenario.** The paper repeatedly acknowledges that MAC contention is abstracted away and that the $1/\gamma$ factor "likely understates" the sectorized mesh disadvantage. Implementing even a simple Slotted ALOHA or CSMA model for a single 100-node cluster would validate (or invalidate) the $\gamma$ assumption and provide the "analytical tractability breakdown" that justifies the DES.

4. **Tighten the paper by 30–40%.** Consolidate the four coordinator scheduling models into two (recommended baseline + conservative bound). Merge Tables VII and VIII. Move the sectorized mesh neighbor-cap sweep (Table II) to supplementary material. Reduce the physical-layer vignette to a paragraph. The paper's thoroughness is admirable but the length-to-novelty ratio is too high for a journal article.

5. **Resolve and clearly disclose AI involvement.** If the manuscript was substantially drafted by AI tools, this must be stated per IEEE policy. If the AI references (Claude 4.6, GPT-5.2) are fictional/aspirational, they should be removed or clearly marked as such. The current disclosure in the Acknowledgment section is ambiguous about the extent of AI contribution to the manuscript text itself (as opposed to the ideation exercise).