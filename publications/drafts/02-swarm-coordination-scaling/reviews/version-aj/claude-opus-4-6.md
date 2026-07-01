---
paper: "02-swarm-coordination-scaling"
version: "aj"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

**Manuscript Version:** AJ
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuinely important problem: how to coordinate autonomous spacecraft swarms at scales of 10³–10⁵ nodes. The gap identified—the absence of systematic byte-level traffic accounting for hierarchical coordination at these scales—is real. The mega-constellation era is arriving, and design-space characterization studies like this have practical value for systems engineers sizing control-plane budgets.

However, the novelty is more limited than the framing suggests. The authors commendably acknowledge (Section I-D, Section IV-F) that the $O(1)$ overhead scaling is an analytical property of fixed-depth hierarchies, not a discovery. The four headline results—coordinator capacity sizing, AoI geometric-distribution behavior, GE retransmission degradation, and joint independence under point-to-point links—are each individually predictable from first principles. The paper's claimed contribution is the *compositional verification* under joint conditions and the *parametric reference implementation*. While these have value, the DES ultimately confirms what the closed-form equations predict, with the independence result in Section IV-D being the most interesting finding—yet it is also the most architecture-dependent (holding only for point-to-point ISLs, as the authors note). The paper would benefit from more clearly positioning itself as a *design handbook* contribution rather than a scientific discovery paper, which would better match its actual strengths.

The comparison against baselines is carefully framed (intentional bounds), but the practical insight is somewhat thin: the centralized architecture with realistic provisioning ($c = N/k_c$) doesn't diverge until $N \approx 10^6$, and the hierarchical advantage reduces to fault tolerance during ground outages (7–29 min/day) and spectrum independence. This is an honest and useful finding, but it somewhat undermines the motivation for the hierarchical architecture at the scales actually simulated ($\leq 10^5$).

---

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The cycle-aggregated DES approach is well-suited to the research questions and clearly described. The abstraction level (message-layer, not packet-level) is appropriate for a parametric design study, and the authors are transparent about what is and is not modeled (Table 6). The Monte Carlo framework (30 replications, bootstrap CIs) is standard, though the near-deterministic nature of the message model (SD < 0.001%) renders the MC framework largely ceremonial for overhead metrics—a point the authors themselves acknowledge.

**Strengths:**
- Explicit byte-level traffic accounting (Tables 4, 5, 7) is a genuine methodological contribution that enables reproducibility.
- Analytical cross-checks for every headline metric (geometric AoI, Chernoff burst bound, GE retransmission probability) are thorough and build confidence.
- The coordinator capacity analysis (Section IV-A) with four scheduling models (deadline, leaky-bucket, TDMA, phase-stagger) is well-structured and practically useful.

**Concerns:**
- The 1 kbps per-node budget is presented as an RF-backup constraint, but the entire analysis is conducted at this single operating point. While the authors correctly note that $\eta$ is dimensionless and applies at any $C_{\text{node}}$, the *interesting* regime where overhead matters (RF backup) is precisely where the message-layer abstraction is least valid—RF links have fundamentally different MAC characteristics than optical ISLs. The dual-regime interpretation (Section IV-F-3) is helpful but highlights a tension: the binding design point is the one where the abstraction is weakest.
- The "cluster" definition (Section IV-A, physical-layer vignette) assumes co-moving nodes in near-identical orbits. This is a strong assumption that significantly simplifies the communication problem. In practice, mega-constellation clusters would span multiple orbital planes with significant relative velocities, and the TDMA feasibility analysis would change substantially. The 500 km cluster diameter vignette, while useful, may not be representative.
- The sectorized mesh comparator (Section III-B-4) uses $k_s = \lceil\sqrt{N}\rceil$ based on a heuristic orbital density argument. The derivation is acknowledged as "order-of-magnitude sizing," but the $\sqrt{N}$ scaling drives the overhead comparison. A different sector-sizing heuristic could change the relative ranking.
- The GE channel model parameters ($p_{GB} = 0.05$, $p_{BG} = 0.20$ per cycle) are not validated against measured LEO ISL statistics. The steady-state 80% availability is quite pessimistic for optical ISLs (which typically achieve >99% availability when not Earth-occluded) and may be more representative of RF links. The choice of parameters significantly affects the correlated loss results.

---

## 3. Validity & Logic

**Rating: 4 (Good)**

The conclusions are generally well-supported by the analysis, and the authors demonstrate commendable intellectual honesty throughout. The paper consistently distinguishes between what the DES measures, what is analytically predictable, and what remains unvalidated. Several specific examples of good practice:

- The explicit statement that centralized compute doesn't diverge until $N \approx 10^6$ (Section IV-G), which works against the paper's own motivation, demonstrates scientific integrity.
- The AoI-to-position-error coupling (Eq. 14) is carefully qualified as "order-of-magnitude" and "illustrative back-of-the-envelope," with appropriate caveats about full covariance propagation.
- The joint independence result (Section IV-D) correctly identifies the architectural condition (point-to-point ISLs) under which it holds and explicitly states it would not hold under shared-medium contention.

**Concerns:**
- The claim that the DES "verifies compositionality" (abstract, Section I-D) is somewhat overstated. The DES confirms that three specific mechanisms don't interact under one specific architecture. This is useful but narrower than "compositionality" implies. A more precise claim would be that the DES confirms *pairwise independence of coordinator saturation and link-layer losses under point-to-point ISL assumptions*.
- Table 10 (Joint Interaction) shows identical drop counts under "No Loss" and "GE Only" columns. The explanation (lost messages never reach the coordinator queue) is correct but also means the GE model is essentially invisible to the coordinator—the two mechanisms operate on completely separate stages. This is less a "finding" and more a consequence of the architectural assumption. The paper should more clearly distinguish between *testing* independence and *assuming* it through the model structure.
- The latency values in Table 11 show discrete jumps (340 ms vs. 508 ms vs. 675 ms) that suggest quantized behavior rather than smooth scaling. This likely reflects the cycle-aggregated simulation resolution but is not discussed.

---

## 4. Clarity & Structure

**Rating: 3 (Adequate)**

The paper is technically thorough but suffers from excessive length and repetition. At approximately 12,000 words of body text plus extensive tables, it significantly exceeds typical IEEE TAES limits. The "Version AJ" designation suggests extensive revision history, and the manuscript reads as if successive revisions added material without sufficient pruning.

**Structural issues:**
- The abstract is 250+ words and reads more like an executive summary than an abstract. Key results are buried in qualifications. A tighter abstract focusing on the three most important findings would be more effective.
- Section III (Simulation Framework) is disproportionately long (~40% of the paper). The sectorized mesh model (Section III-B-4), while useful, could be condensed. Tables 2, 3, 5, 6, and 7 contain overlapping information about traffic accounting.
- The "Roadmap" paragraph at the start of Section IV is helpful, but the section ordering (IV-A through IV-I) is complex. The paper would benefit from a clearer narrative arc: present the design envelope first (IV-E), then drill into the three mechanisms (IV-A–C), then verify composition (IV-D).
- Multiple definitions are repeated: $\eta$ is defined in the abstract, Section III-E, Section III-F, and Section III-G. The MAC efficiency caveat ($\times 1/\gamma$) appears at least 8 times.

**Positive aspects:**
- Table 6 (Simulation Abstraction Scope) is an excellent addition that clearly communicates the model's boundaries.
- The Design Equations Summary (Section V-C) is a valuable practitioner-oriented contribution.
- Figures are generally well-designed, though I cannot evaluate them from the LaTeX source alone.

---

## 5. Ethical Compliance

**Rating: 4 (Good)**

The Acknowledgment section discloses AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) with appropriate specificity about what was AI-generated (architectural concepts) versus what was human-validated (the current study). The reference to a companion methodology paper [47] is appropriate. The "Project Dyson Research Team" authorship with a note about individual names for final publication is unusual but acceptable if resolved before publication.

Data availability is excellent: source code, configuration files, and output datasets are referenced with a specific repository tag. The simulation parameters are comprehensively documented (Table 4), supporting reproducibility.

One minor concern: the AI model versions cited (Claude 4.6, GPT-5.2) do not correspond to any publicly released models as of my knowledge cutoff, suggesting either future models or version numbering discrepancies. This should be verified.

---

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE TAES in topic, though the contribution leans more toward communication systems engineering than traditional aerospace content. The reference list (52 items) is comprehensive and spans the relevant domains: distributed systems, queueing theory, swarm robotics, constellation management, and space communication standards.

**Concerns:**
- Several references are non-archival (SpaceX website, Amazon website, DARPA program pages, DoD fact sheets). While understandable for operational systems, the paper relies on these for motivational claims about constellation scale that are central to the argument. At minimum, peer-reviewed sources characterizing Starlink operations (e.g., McDowell's orbital analysis papers) should supplement the SpaceX website reference.
- The related work section (Section II) is adequate but could better position the paper relative to recent DTN/ISL routing work for mega-constellations (e.g., Bhattacherjee & Singla, SIGCOMM 2019; Handley's follow-up work). The ISL routing literature has advanced significantly since the cited 2003 Akyildiz paper and 2018 Handley paper.
- The paper does not cite any prior work on hierarchical coordination specifically for satellite constellations (e.g., Radhakrishnan et al.'s work on hierarchical satellite networks, or the CCSDS Mission Operations framework). If such work exists, it should be discussed; if not, this gap should be explicitly noted.
- Reference [47] (companion methodology paper) is self-published on the project website and not peer-reviewed. While acceptable as supplementary material, claims about AI-assisted methodology should not depend on it.

---

## Major Issues

1. **The DES adds limited value beyond closed-form analysis.** The paper repeatedly acknowledges that individual metrics are "analytically tractable" and the DES matches closed-form predictions to within 0.1–1.5%. The joint independence result (Section IV-D) is the strongest DES-specific contribution, but as discussed above, it is largely a consequence of the point-to-point ISL model structure rather than an emergent finding. The authors should either (a) identify scenarios where the DES reveals behavior not predictable from single-factor analysis, or (b) more forthrightly position the paper as providing a *validated parametric design tool* rather than a simulation study that discovers new phenomena. The current framing oscillates between these positions.

2. **Absence of orbital geometry.** The paper models "space swarms" without any orbital mechanics beyond a heuristic cluster diameter. Cluster membership, inter-cluster connectivity, and link availability in LEO are fundamentally driven by orbital geometry (RAAN, inclination, altitude). The Bernoulli and GE link models are placeholders for what is actually a deterministic, periodic, geometry-dependent process. The paper should either (a) incorporate a simplified orbital model (e.g., Walker constellation geometry with Earth occlusion) to validate that the topology ranking holds under realistic connectivity patterns, or (b) more explicitly scope the contribution as a *communication protocol analysis* that requires orbital geometry coupling before application to real systems. The current "physical-layer vignette" (Section IV-A) is insufficient.

3. **The 1 kbps budget creates an artificial bottleneck that drives most results.** The stress-case overhead of 46% is meaningful only at 1 kbps. At 10 kbps (still conservative for optical ISLs), overhead drops to 4.6%—engineering-irrelevant, as the authors note. The paper's practical value depends on how often the 1 kbps RF-backup mode is actually the binding constraint. If optical ISLs achieve >99% availability (as current Starlink ISLs suggest), the RF-backup regime may be too rare to drive architecture selection. The paper should quantify the expected fraction of operational time in the RF-backup regime and assess whether the overhead differences between architectures matter during that fraction.

4. **Incomplete validation of the sectorized mesh comparator.** The sectorized mesh is presented as a "realistic decentralized comparator," but its parameterization ($k_s = \sqrt{N}$, cap = 10 neighbors) is heuristic. The $\sqrt{N}$ sector sizing, the 32-byte heartbeat size (vs. 64 bytes for hierarchical), and the cap of 10 neighbors are all design choices that directly affect the overhead comparison. A sensitivity analysis varying these parameters (partially provided in Table 8) is helpful but does not address the fundamental question: is the sectorized mesh a fair comparator, or is it parameterized to look worse than the hierarchical architecture?

---

## Minor Issues

1. **Abstract, line 3:** "byte-level traffic accounting under a 1 kbps per-node control-plane budget" — should clarify this is message-layer, not physical-layer, byte accounting.

2. **Section I-A, paragraph 2:** "proposed space infrastructure concepts...contemplate fleets of $10^5$ to $10^6$ autonomous units in the near term" — this is a strong claim. The cited references (O'Neill 1976, Badescu 2006) are aspirational, not "near term." Suggest rewording.

3. **Eq. (4), Section III-B-2:** $M_{\text{total}} = N + N/k_c + N/(k_c \cdot k_r)$ counts uplink only, as noted, but the text immediately following says "the DES models the full bidirectional traffic." The equation should either be expanded to include bidirectional traffic or more clearly labeled as "uplink only."

4. **Table 4 (Simulation Parameters):** The collision avoidance rate footnote (a) explains the $10^{-4}$/node/s rate well, but the 1,000:1 screening-to-maneuver ratio should be cited. Is this from ESA Space Debris Office data?

5. **Section III-B-4:** "Sectorized mesh heartbeats (32 B) are smaller than hierarchical heartbeats (64 B) because they carry only a node-alive flag and timestamp" — this asymmetry in heartbeat size favors the hierarchical architecture in the overhead comparison. Consider using equal heartbeat sizes for a fairer comparison, or explicitly quantify the impact.

6. **Table 9 (Coordinator Bandwidth):** At $C_{\text{coord}} = 1$ kbps, "100.0% drops" and "0.0% delivery" — this is trivially expected since 1 kbps < 20.5 kbps demand. Including this row adds no information.

7. **Section IV-B:** The AoI cross-check (Eq. 12) matches the DES to within one cycle (440 vs. 441 s). This is *exact* agreement given the discrete-time model. Stating "within one cycle" understates the agreement.

8. **Section IV-C:** "Inter-cycle store-and-forward recovers to 95% within 4–7 cycles" — the text derives this from the geometric series $P_n = 1 - (1-p_s)^n$, which assumes independence across cycles. Under GE, consecutive cycles may be in the same bad state, violating this assumption. The "accounting for GE state transitions" qualifier is vague; please provide the explicit Markov chain calculation.

9. **Section V-B:** "Priority queueing" is listed as a limitation but collision avoidance messages (128 B) are already modeled with 1-second resolution vs. 10-second for routine traffic. Clarify whether this constitutes implicit prioritization.

10. **References:** [1] and [3] are website URLs that may not persist. Consider citing archival sources (FCC filings, ITU filings) for constellation sizes.

11. **Notation:** $p_{\text{link}}$ is used both as link *availability* (probability of successful transmission) and as a Bernoulli success probability. In Table 13, $p_{\text{link}} = 0.5$ means 50% per-attempt success, but in the GE model, the steady-state availability is 80%. Clarify the relationship between these parameters.

12. **Section III-E:** The statement "total utilization...exceeds the normalized throughput limit of Slotted ALOHA ($1/e \approx 36\%$), confirming that deterministic scheduling (TDMA) is required" is correct but applies only to the stress case. Under nominal workloads ($\eta \sim 5\%$), total utilization is ~25%, which is below the ALOHA limit. This nuance should be noted.

---

## Overall Recommendation

**Major Revision**

This paper addresses a relevant problem and demonstrates careful engineering analysis with commendable transparency about limitations. The byte-level traffic accounting, coordinator capacity sizing, and design equations summary have genuine practical value for systems engineers. However, the paper suffers from three fundamental issues that require substantial revision: (1) the DES contribution beyond closed-form analysis is insufficiently demonstrated—the paper needs either a scenario where the DES reveals non-obvious behavior or a repositioning as a design-tool paper; (2) the absence of orbital geometry undermines the "space swarm" framing and limits the applicability of the link availability results; and (3) the paper is significantly too long, with substantial repetition that obscures the core contributions. A focused revision addressing these issues—particularly condensing the paper by ~30%, incorporating even a simplified orbital connectivity model, and sharpening the DES value proposition—would produce a strong contribution suitable for IEEE TAES.

---

## Constructive Suggestions

1. **Incorporate a Walker constellation connectivity model.** Even a simplified model (e.g., Walker-delta with Earth occlusion producing deterministic periodic link outages) would dramatically strengthen the paper. Replace the Bernoulli/GE link models with geometry-driven outage patterns for at least one validation case. This would address Major Issue #2 and provide a scenario where the DES may reveal non-obvious behavior (e.g., correlated link outages across an orbital plane simultaneously orphaning multiple clusters).

2. **Restructure as a design handbook.** Lean into the paper's actual strength: a validated parametric design tool. Lead with the Design Equations Summary (currently buried in Section V-C), present the DES as the validation engine, and organize results around the three design decisions a systems engineer faces (cluster sizing, coordinator capacity, telemetry rate). This would address Major Issue #1 and naturally reduce length.

3. **Quantify the RF-backup operating fraction.** Estimate the fraction of operational time each node spends in the 1 kbps RF-backup regime (based on optical ISL availability statistics from Starlink or similar). If this is <1% of operational time, the overhead comparison at 1 kbps—while technically correct—may not drive architecture selection. This context is essential for the paper's practical relevance (Major Issue #3).

4. **Condense the paper by ~30%.** Specific targets: merge Tables 2/3/5/7 into a single comprehensive traffic accounting table; reduce Section III-B-4 (sectorized mesh) to one paragraph plus one table; eliminate repeated definitions of $\eta$ and the $1/\gamma$ caveat; move the physical-layer vignette to an appendix. The current length (~14 pages estimated) significantly exceeds typical TAES papers.

5. **Add one MAC-contention experiment.** The paper repeatedly identifies MAC contention as the key unmodeled effect. Even a simplified contention model (e.g., Slotted ALOHA with capture effect for a single cluster) would partially address this gap and demonstrate the DES's extensibility. This would strengthen the "foundation for future extensions" claim in Section I-D.