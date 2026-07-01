---
paper: "02-swarm-coordination-scaling"
version: "bh"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

**Manuscript Version:** BH
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap: the absence of closed-form sizing equations for hierarchical coordination architectures at the $10^3$–$10^5$ node scale with byte-level traffic accounting. The claim in Section I-A that "no prior work provides closed-form parametric sizing relationships for coordination architectures across $10^3$–$10^5$ nodes with byte-level traffic accounting under a fixed per-node budget" is plausible, and the practitioner-toolkit framing is appealing. The design equations collected in Section V-C are potentially useful for systems engineers sizing coordination links for mega-constellations.

However, the novelty is tempered by the nature of the results. The core finding—that architecture-specific overhead is ~5% and command traffic dominates—is, upon reflection, somewhat predictable from first principles. The overhead equations are essentially byte-counting exercises (sum of message sizes divided by bandwidth budget), and the $O(1)$ scaling of per-node overhead in a hierarchical tree is a well-known property. The GE inter-cycle recovery analysis and AoI characterization add value, but these are relatively straightforward applications of existing Markov chain and AoI theory (Kaul et al., Yates et al.) to a specific parameter regime. The paper would benefit from a clearer articulation of what is *surprising* or *counterintuitive* in the results, beyond confirming that hierarchical aggregation works as expected.

The scope of applicability is also narrower than the title suggests. The "design equations" are specific to a particular message model (fixed 256/512/64/128-byte messages, fixed reporting rates) and a particular hierarchy (four-level, fixed fan-out). The generalizability to alternative message semantics, adaptive reporting, or heterogeneous node types is not explored. The paper acknowledges that command traffic is "topology-invariant given the assumed workload semantics," which significantly limits the comparative value of the topology analysis.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The methodology is internally consistent but operates at a high level of abstraction that limits its practical applicability. The cycle-aggregated DES is well-described (Section III-A), and the authors are commendably transparent about what is and is not modeled. The explicit enumeration of modeled vs. not-modeled phenomena is good practice.

**Strengths:** The TDMA frame analysis (Section IV-A) is thorough, with the superframe budget (Table VI) providing a concrete time-domain accounting. The three coordinator ingress models (TDMA, hard-deadline, token-bucket) converging to 20–50 kbps is a useful cross-check. The GE parameter sensitivity sweep (Fig. 5b) providing design curves across $p_{BG}$ and $p_B$ is the most genuinely useful contribution for practitioners. The joint interaction verification (Section IV-D, Table VIII) demonstrating pipeline decoupling is a valuable DES-specific result.

**Concerns:** The DES "verification" of closed-form equations to <0.1% (Table X) is not surprising—both the DES and the equations implement the same byte-counting logic at the same abstraction level. This is implementation consistency checking, not validation. The authors acknowledge this ("checks implementation consistency," Section III-A), but the paper's framing sometimes conflates consistency with validation. The 30 MC replications with SD < 0.001% for overhead (Section III-D) further confirms that the variance is essentially zero because the system is deterministic at this abstraction level—there is no stochastic element affecting the overhead calculation beyond the (negligible) collision alert rate.

The static topology assumption is a significant methodological limitation for LEO constellations. The authors bound re-association overhead at <0.5% (Section V-B), but the transient AoI impact during cluster handoffs—which could affect conjunction screening precisely when orbital geometry is changing—is acknowledged as unmodeled. For cross-plane configurations, this is not a minor omission.

The choice of 1 kbps as the design-driving case is well-justified as an S-band RF backup scenario, but the paper spends enormous effort analyzing a regime that applies <1% of operational time (by the authors' own admission). Table II showing that at ≥10 kbps "the coordinator bottleneck vanishes" somewhat undermines the practical relevance of much of the analysis.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The internal logic is generally sound, and the authors are careful about qualifying their claims. The distinction between protocol overhead ($\eta$) and total utilization ($\eta_{\text{total}}$), and the separation of topology-dependent from topology-invariant components, is well-handled throughout.

**Logical strengths:** The identification that per-node unicast commands require 22-cycle staggering (Eq. 11, Table IX) is an important practical finding that honestly reveals a limitation of the architecture. The coherence-time analysis for the GE model (Section IV-C) correctly identifies the regime boundaries and acknowledges that the GE model is inappropriate for deterministic Earth occultation—a refreshingly honest assessment.

**Logical concerns:** The comparison framework has structural issues. The centralized baseline models only compute-queue scalability (M/D/c), not communication overhead, making direct overhead comparisons with the hierarchical architecture invalid—as the authors acknowledge in Table XII footnote (d). The global-state mesh is an intentional worst case that no practitioner would implement. The sectorized mesh provides different functional scope (Table XIV). This means the paper's comparative claims rest on comparing architectures that are not functionally equivalent, which the authors handle through the capability matrix but which still weakens the comparative narrative.

The AoI analysis (Section IV-B) correctly derives P99 = 440s for $p_{\text{exc}} = 0.10$ and contextualizes it against conjunction screening timescales. However, the claim that this is "within conjunction screening tolerances" deserves more scrutiny. The 441s AoI corresponds to ~230m along-track uncertainty, which may be acceptable for initial screening but the paper does not address the compound effect across a fleet of $10^5$ nodes where multiple conjunction events may be evolving simultaneously. The single-pair AoI analysis does not capture fleet-level conjunction assessment workload.

The claim of "linear scaling with bandwidth" (abstract) is trivially true for the overhead fraction but obscures the fact that the *absolute* overhead in bytes is bandwidth-independent—it is the budget that scales, not the traffic.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized and generally well-written. The roadmap at the beginning of Section IV is helpful. The notation table (Table I) is placed appropriately. The progressive disclosure from architecture-specific overhead (~5%) to workload-dependent total (5–46%) is pedagogically effective.

**Strengths:** The design equations summary (Section V-C) is excellent—collecting all key relationships in one place with worked examples is exactly what a practitioner needs. The superframe budget (Table VI) is a model of concrete engineering specification. The explicit treatment of broadcast vs. unicast command models (Section IV-A) and the schedulability table (Table IX) are clear and useful.

**Weaknesses:** The paper is very long for its core content. Much of the text is devoted to qualifying, contextualizing, and cross-referencing results that could be stated more concisely. For example, the sectorized mesh model (Section III-B.4) receives extensive treatment despite being a comparator with acknowledged functional-scope differences. The repeated reminders that "physical-layer validation is future work" (appearing in at least 5 locations) could be consolidated.

Some passages are dense to the point of obscuring the key message. The coordinator failure transient discussion (Section III-B.2) mixes optical ISL and RF-backup scenarios, Raft election details, and fleet-wide failure rate calculations in a single paragraph that would benefit from restructuring.

The figures are referenced but not provided for review (as expected in LaTeX source), so I cannot assess their quality directly. The figure captions are generally informative, though Fig. 8's caption noting the $10^6$-node curve is "analytical extrapolation, not DES-measured" is an important caveat that should be more prominent.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The AI-assistance disclosure in the Acknowledgment section is appropriate and specific ("Claude 4.6, Gemini 3 Pro, GPT-5.2"), with the important qualifier that the AI-motivated architecture "is not validated here." The data availability statement with a specific repository tag is commendable. The anonymous authorship ("Project Dyson Research Team") with a note about final publication is acceptable for review but must be resolved.

One minor concern: the reference to the AI methodology paper [dyson_multimodel] is self-referential and appears to be a non-peer-reviewed online publication. If the AI tools influenced the architecture design, more detail about what specifically was AI-generated vs. human-designed would strengthen transparency.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in scope, addressing autonomous spacecraft coordination at scale. The reference list is comprehensive (50+ references) and covers the relevant domains: constellation operations, swarm robotics, distributed systems, queueing theory, and AoI.

**Concerns:** Several references are non-archival (SpaceX FCC filings, Amazon web pages, DARPA program pages, DoD fact sheets), which is somewhat unavoidable for current mega-constellation programs but weakens the scholarly foundation. The Starlink operations reference [1] cites an FCC filing and a "non-archival" personal website—this is the paper's primary motivating example and deserves a stronger reference.

Notable omissions: The paper does not cite recent work on autonomous satellite operations by ESA's OPS-SAT mission, which has demonstrated onboard autonomous decision-making. The DTN/BPv7 discussion could reference more recent delay-tolerant networking work specific to mega-constellations. The CCSDS Proximity-1 reference [ccsds_prox1] is from 2013; more recent proximity link standards exist. There is no reference to the substantial literature on TDMA scheduling for satellite networks (e.g., Bertsekas and Gallager's treatment, or more recent LEO-specific TDMA work).

The paper does not engage with the growing literature on digital twins for constellation management, which is directly relevant to the state-maintenance problem addressed here.

---

## Major Issues

1. **Validation gap is too large for the claims made.** The paper derives "design equations" but validates them only against a DES that implements the same byte-counting logic. The <0.1% agreement is a tautology, not evidence of correctness. The absence of any physical-layer or packet-level validation means the equations are unverified against realistic channel conditions. The authors should either (a) include at least a single-cluster NS-3 simulation as proposed in Section V-A, or (b) significantly downgrade the claims from "design equations" to "preliminary sizing estimates pending physical-layer validation." As written, the gap between the claimed contribution (practitioner toolkit) and the validation level (self-consistent message-layer accounting) is too wide.

2. **The 1 kbps regime dominates the analysis but has limited practical relevance.** By the authors' own statement, this regime applies during S-band RF backup (<1% of operational time). Most of the paper's complexity (TDMA frame analysis, coordinator bottleneck, unicast staggering) vanishes at ≥10 kbps. The paper should either (a) reframe the 1 kbps analysis as a corner-case study rather than the primary contribution, or (b) provide equally detailed analysis of the 10–100 kbps regimes where most operations occur. Table II acknowledges this but the paper's structure does not reflect it.

3. **Topology comparison is structurally unfair.** The four architectures compared have different functional scopes (Table XIV), different modeling fidelity (centralized: compute-queue only; mesh: bandwidth only; hierarchical: full communication layer), and different design intents (global-state mesh as intentional worst case). The paper acknowledges these differences but still presents comparative figures (Fig. 10) and tables (Table XII) that invite direct comparison. Either the comparisons should be restricted to functionally equivalent configurations, or the comparative framing should be abandoned in favor of standalone characterization of the hierarchical architecture.

4. **Static topology assumption undermines LEO applicability.** For the target application (LEO mega-constellations), cluster membership changes on 45–90 minute timescales for cross-plane configurations. The <0.5% overhead bound for re-association addresses steady-state bandwidth but not the transient coordination quality degradation during handoffs—precisely when conjunction geometry may be changing. This needs at minimum a quantitative worst-case analysis, not just a qualitative acknowledgment.

---

## Minor Issues

1. **Abstract:** "Protocol overhead is $\eta_E \approx 6\%$" appears before the notation is defined; consider adding "(beyond baseline telemetry)" for clarity.

2. **Eq. (2):** The M/D/1 waiting time formula $W_q = \rho / (2\mu_s(1-\rho))$ is the Pollaczek-Khinchine result for deterministic service, but the standard form is $W_q = \rho^2 / (2\lambda(1-\rho))$ or equivalently $\rho / (2\mu_s(1-\rho))$. Please verify the form used matches the intended model.

3. **Section III-B.2:** "Coordinator rotation: state transfer (10–50 MB) over optical ISL (80–400 ms), excluded from $\eta$." The exclusion rationale should be stated explicitly—is it because optical ISL has separate bandwidth, or because it's infrequent?

4. **Table III (Simulation Parameters):** The collision avoidance rate footnote references "see text" but the text discussion is in Section III-D, several pages later. Consider a forward reference.

5. **Section III-B.4:** "$k_s = \lceil\sqrt{N}\rceil$ orbital neighbors per sector" — the $\sqrt{N}$ scaling justification ("conjunction screening volume contains $O(\sqrt{N})$ nodes") is described as an "order-of-magnitude heuristic." This deserves a citation or derivation.

6. **Table V (Sector Cap Sweep):** The $\eta_{\text{sector}}$ formula in the footnote includes commands (stress-case) but this is not immediately obvious from the table header. Clarify whether these are stress-case or nominal values.

7. **Section IV-A:** "Fleet-wide TDMA cost is 0.28 kbps/node (1% coordinators)" — this calculation is not shown. Please provide the derivation or a reference to where it appears.

8. **Eq. (7):** The AoI P99 formula uses $\lceil \cdot \rceil$ (ceiling), which is correct for discrete geometric distributions, but the notation should clarify that this gives AoI in units of $T_c$.

9. **Section IV-C:** "Maximum observed streaks are 10–13 cycles" — over how many MC replications and what total observation time? This tail statistic needs sample-size context.

10. **Table VIII (Joint Interaction):** The "GE Only" and "No Loss" columns are identical, which is the paper's point about pipeline decoupling, but the table caption should explicitly note this is expected behavior, not a data error.

11. **Section V-C (Design Equations Summary):** The geometric approximation for inter-cycle recovery P95 is described as "conservative" but overestimates by 0–1 cycles. "Conservative" typically means it produces a safer (larger) estimate, which is correct here, but the language could be clearer.

12. **References:** [1] and [3] rely on non-archival sources. Consider whether more stable references exist for the Starlink and Kuiper constellation parameters.

13. **Acknowledgment:** "Claude 4.6, Gemini 3 Pro, GPT-5.2" — these version numbers do not correspond to any publicly released models as of my knowledge. If these are internal designations, clarify; if they are future versions, this raises questions about the timeline.

---

## Overall Recommendation

**Major Revision**

The paper addresses a legitimate gap in the literature and provides a well-structured set of sizing equations for hierarchical coordination in large space swarms. The TDMA superframe analysis, GE parameter sensitivity curves, and AoI characterization are useful contributions. However, the validation gap between message-layer self-consistency and physical-layer reality is too large for the "design equations" framing; the practical relevance is undermined by the focus on a corner-case bandwidth regime; and the topology comparison framework has structural fairness issues. A major revision should include at minimum a packet-level single-cluster validation (or explicit downgrading of claims), rebalancing of the analysis toward operationally relevant bandwidth regimes, and resolution of the topology comparison issues. The core analytical contributions are sound and, with appropriate reframing and additional validation, could constitute a solid contribution to IEEE T-AES.

---

## Constructive Suggestions

1. **Add a single-cluster packet-level simulation.** Even a simplified NS-3 or MATLAB Simulink model of one cluster ($k_c = 100$) with TDMA PHY, realistic guard times, and GE channel would dramatically strengthen the validation. The superframe budget in Table VI provides the specification. This single addition would address the most critical reviewer concern and elevate the paper from "self-consistent accounting exercise" to "validated design methodology."

2. **Restructure around the operationally relevant regime.** Present the 10–100 kbps optical ISL regime as the primary case (where most operations occur) and the 1 kbps RF-backup as the stress case. This reframing would make the paper more useful to practitioners while retaining the detailed 1 kbps analysis as a corner-case study. The current structure inverts the practical importance.

3. **Replace the four-topology comparison with a focused hierarchical characterization.** The centralized and global-state mesh bounds add little insight (one is compute-only, the other is an intentional worst case). Instead, deeply characterize the hierarchical architecture across parameter regimes and compare only with the sectorized mesh (which is fully modeled at the same abstraction level and provides a meaningful alternative). This would shorten the paper and strengthen the comparative claims.

4. **Quantify the dynamic topology impact.** Add a simplified analytical model of cluster re-association: assume Poisson re-association events at a rate derived from orbital mechanics, model the AoI transient during handoff (1–3 cycles), and compute the fleet-level probability that any node is in a handoff transient at any given time. This would address the static-topology limitation without requiring a full dynamic simulation.

5. **Provide a worked design example.** Add a section showing how a practitioner would use the design equations for a specific mission (e.g., sizing the coordination architecture for a 10,000-node LEO constellation at 550 km). Walk through the parameter selection ($k_c$, $T_c$, $C_{\text{node}}$, $p_{\text{exc}}$), compute the required coordinator link capacity, verify AoI meets conjunction screening requirements, and size buffers for GE recovery. This would make the "practitioner toolkit" claim concrete and demonstrate the equations' utility.