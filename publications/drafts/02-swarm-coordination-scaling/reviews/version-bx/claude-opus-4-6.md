---
paper: "02-swarm-coordination-scaling"
version: "bx"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

**Manuscript Version:** BX
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap: there is no published work providing closed-form parametric sizing equations for coordination architectures spanning $10^3$–$10^5$ autonomous spacecraft nodes with byte-level traffic accounting. The authors correctly identify that swarm robotics literature operates at 10–100 agents, constellation management at ~$10^4$, and networking literature treats routing rather than coordination overhead. The three-layer feasibility decomposition (byte budget, MAC efficiency, TDMA airtime) is a useful conceptual contribution that could inform system engineers designing future mega-constellations or large autonomous fleets.

However, the novelty is tempered by several factors. First, the core analytical results are relatively straightforward—the overhead equations are essentially accounting identities (bytes per node per cycle divided by bandwidth budget), and the $O(1)$ scaling of hierarchical overhead is immediate from the $O(N)$ message count with $O(N)$ aggregate bandwidth. The DES "verification" to $<0.1\%$ is expected by construction (as the authors acknowledge) and does not constitute independent validation. Second, the practical applicability is narrow: the design-driving 1 kbps RF-backup regime is described as occupying $<1\%$ of operational lifetime, and at $\geq$10 kbps all message-layer constraints are "non-binding." This raises the question of whether the most extensively analyzed regime is the most important one. Third, the paper's central finding—that architecture-specific overhead is small (~5%) while command traffic dominates (~41%)—is somewhat intuitive for a hierarchical aggregation scheme, and the topology-invariance of command traffic under centralized command generation is definitional rather than discovered.

The fleet-level channel reuse analysis (Eq. 6), the GE inter-cycle recovery characterization with sensitivity sweeps, and the three-layer schedulability framework do add value beyond simple accounting. The TDMA pipeline decoupling result (Table VII) is a genuinely useful insight for practitioners. But overall, the contribution sits closer to a well-executed engineering analysis than a fundamental advance in distributed systems theory or space systems architecture.

---

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The methodology has both notable strengths and significant weaknesses. On the positive side, the authors are commendably transparent about what is and is not modeled. The verification taxonomy (code verification, model verification, model validation) following IEEE 1012 is well-structured, and the explicit acknowledgment that physical-layer validation is absent is appropriate. The claim map (Table X) is an excellent practice that more papers should adopt. The Monte Carlo configuration (30 replications, bootstrap CIs) is adequate for the variance levels observed.

The fundamental methodological concern is that the simulation is essentially a calculator for the closed-form equations rather than an independent verification tool. The cycle-aggregated DES with fluid-server ingress, deterministic processing, and Bernoulli/GE loss models reproduces the analytical formulas because it implements them directly. The $<0.1\%$ agreement (Table VIII) is not evidence of model correctness—it is evidence of correct implementation of the same assumptions. The slot-level TDMA simulator adds genuine value by revealing the ARQ coupling effect invisible to the fluid-server model, but it too operates at an abstraction level far above physical reality.

Several specific methodological concerns arise:

- **Static topology assumption:** The paper claims cluster membership is fixed for 1 year, justified as "exact for co-planar formations." For LEO constellations with multiple orbital planes (the dominant architecture for Starlink, Kuiper, OneWeb), cross-plane relative motion causes continuous topology changes. The claimed $<0.5\%$ re-association overhead is stated without derivation or simulation evidence—it appears in Section V-B as an assertion. For a paper focused on byte-level accounting, this unquantified dynamic overhead is a notable gap.

- **GE model parameterization:** The GE parameters ($p_{GB} = 0.05$, $p_{BG} = 0.50$) are not derived from any physical channel model or measurement campaign. The "physical mapping" paragraph (Section IV-C) provides qualitative associations but no quantitative justification. The sensitivity sweep partially addresses this, but the default parameters drive the headline results.

- **Coordinator failure model:** The exponential failure model with identical rates for coordinators and regular nodes ignores the increased thermal, power, and computational stress on coordinator hardware. The RF-backup handoff recovery time (~160 s, 16 cycles) is a significant vulnerability that deserves more rigorous analysis than the brief treatment in Section III-B.

- **Message size assumptions:** The 256 B status report, 512 B command, 128 B alert, and 64 B heartbeat sizes are stated without justification from any existing space protocol standard. While the paper mentions CCSDS SPP alignment, no mapping is provided. These sizes directly determine all overhead results.

---

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The internal logic of the paper is generally sound—conclusions follow from stated assumptions, and the authors are careful to qualify claims with their scope of validity. The three-layer feasibility framework is logically coherent, and the distinction between byte budget, MAC overhead, and airtime schedulability is well-maintained throughout.

However, several logical issues merit attention:

**Topology comparison fairness.** The paper compares hierarchical coordination against a global-state mesh (intentional worst case), a centralized ground system (compute-queue only, no communication model), and a capped sectorized mesh (functionally different scope). The authors acknowledge these are not apples-to-apples comparisons (Table VI), but the paper's framing still implies the hierarchy is "better" than alternatives. The sectorized mesh comparison is particularly problematic: at cap = 10, it monitors 3.2% of the sector vs. 100% cluster coverage for the hierarchy—these serve fundamentally different functions. The 65–67% vs. 46% overhead comparison is therefore misleading without heavy qualification, which the authors provide in some places but not consistently (e.g., the abstract states the comparison without the functional scope caveat).

**Stress-case interpretation.** The stress-case ($p_{\text{cmd}} = 1.0$, every node receives a 512 B command every cycle) is described as bounding "fleet-wide reconfiguration campaigns." But the paper also shows this is not single-cycle deliverable under unicast (22-cycle stagger required). If the stress-case cannot actually be delivered in one cycle, reporting $\eta_S \approx 46\%$ as a per-cycle metric is somewhat misleading—the effective per-cycle delivered overhead under unicast is much lower, spread over 22 cycles. The paper addresses this in Table VI but the headline $\eta_S$ figure propagates through the abstract and conclusions without this nuance.

**Circular reasoning in the "favorable" cluster size finding.** The paper finds $k_c = 100$–200 is "favorable" (RQ2), but overhead is invariant to $k_c$ (Table IX, $\pm 0.1\%$), and the latency trade-off is driven by the assumed processing rate ($\mu_c = 200$ msg/s). The "favorable" range is therefore an artifact of the assumed processing speed, not a fundamental property of the architecture.

**AoI mission relevance.** The paper correctly notes that AoI P99 = 440 s is $<0.5\%$ of a 24-hour conjunction response window, but this comparison conflates two different operational needs. The RF-backup channel is for safe-mode operations during ISL outages—precisely when situational awareness is most critical. A 7+ minute information gap during an emergency is not obviously acceptable, and the paper does not engage with this operational question.

---

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is generally well-written and well-organized. The roadmap at the beginning of Section IV is helpful, and the notation table (Table I) is a good practice. The progressive disclosure of results—from single-factor analyses to joint interaction verification to the design envelope—follows a logical arc. The design equations summary in Section V-C is valuable for practitioners.

Several aspects of the presentation are particularly effective: the superframe time budget (Table V) provides concrete engineering detail; the claim map (Table X) is exemplary for transparency; and the worked examples (fleet-level reuse, cluster-local Raft consensus) ground abstract equations in concrete scenarios.

However, the paper suffers from excessive length and repetition. The same key numbers ($\eta_0 \approx 5\%$, $\eta_S \approx 46\%$, 24–30 kbps, AoI P99 = 440 s, GE P95 = 4 cycles) are repeated dozens of times across the abstract, introduction, results, discussion, and conclusion. While some repetition aids readability, the current level suggests the paper could be shortened by 20–30% without loss of content. The abstract alone is 250+ words and reads more like an executive summary than an abstract.

The paper also suffers from notation overload. The distinction between $\eta$, $\eta_0$, $\eta_{\text{cmd}}$, $\eta_{\text{total}}$, $\eta_{\text{eff}}$, $\eta_E$, $\eta_S$, $\eta_{\text{sector}}$, $\eta_{\text{sync}}$, and $\eta_{\text{consensus}}$ requires constant cross-referencing. A consolidated notation summary beyond Table I would help.

Figures are referenced but provided as PDF placeholders (not visible in the LaTeX source). Based on captions, they appear appropriate and well-described. The 16 figures may be excessive for a journal paper; some could be consolidated or moved to supplementary material.

---

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) with a citation to a methodology paper and an explicit statement that the AI-generated concepts are "not validated here." This is transparent and follows emerging best practices for AI disclosure in academic publishing.

The author block uses a team name ("Project Dyson Research Team") with a footnote promising individual names for final publication. While this is unusual, it is flagged as per IEEE policy. The data availability statement is exemplary—open-source code, tagged release, specific software versions, and runtime estimates. This supports reproducibility.

One minor concern: the reference to future AI model versions (Claude 4.6, GPT-5.2) that do not exist as of mid-2025 suggests either the paper is set in a near-future context or these are placeholder names. This should be clarified to avoid confusion about the actual tools used.

---

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in its treatment of autonomous spacecraft coordination, though it sits at the boundary between a systems engineering analysis and a communications/networking paper. The AoI framework, GE channel model, and TDMA analysis draw heavily from the communications literature, while the application domain is aerospace.

The reference list (55 entries) is comprehensive and generally appropriate. Key works in constellation management (Starlink, Kuiper, OneWeb), distributed systems (Lamport, Raft, SWIM), swarm robotics (Brambilla, Dorigo), and AoI theory (Kaul, Yates, Kadota) are cited. The CCSDS standards references (SPP, Proximity-1, BPv7) ground the work in space communications practice.

However, several gaps exist:

- **No references to actual LEO ISL link budgets or channel measurements.** The 1 kbps S-band RF backup and the GE parameters are assumed without reference to any published link budget analysis or channel measurement campaign. Works by Leyva-Mayorga et al. on LEO ISL characterization, or ITU-R propagation models, would strengthen the physical-layer grounding.

- **Missing references on cluster-based satellite networking.** The LEACH citation is appropriate but dated (2000); more recent work on cluster-head selection in satellite networks (e.g., by Liu et al., 2020s) would be relevant.

- **No reference to existing TDMA standards for satellite networks.** DVB-RCS2, CCSDS USLP, or MF-TDMA standards used in operational systems would provide context for the TDMA frame model.

- **Several non-archival references** (Amazon Kuiper overview, DARPA program pages, DoD fact sheets) are acknowledged as such but weaken the scholarly foundation. The Starlink FCC filing is appropriate; the others could be replaced with peer-reviewed sources where available.

- **Self-citation [dyson_multimodel]** to an unpublished methodology paper at projectdyson.org is not independently verifiable.

---

## Major Issues

1. **Lack of physical-layer validation undermines the practical utility of the sizing equations.** The paper repeatedly acknowledges this gap but still presents results as "design equations" suitable for engineering use. The $\gamma = 0.85$ assumption absorbs all unmodeled physical-layer effects into a single parameter, but the paper provides no evidence that this value is achievable in practice for the described RF-backup scenario (S-band, LEO, half-duplex, 500 km cluster diameter). The sensitivity analysis (Section IV-F) shows that at $\gamma = 0.70$, stress-case overhead reaches 66%, and at $\gamma < 0.50$ the system fails—yet no physical-layer analysis constrains which $\gamma$ values are realistic. The recommended next step (NS-3 simulation) should arguably have been completed before publication of "design equations."

2. **The topology comparison is structurally unfair and potentially misleading.** The four architectures compared serve different functions, operate at different abstraction levels, and are modeled with different fidelity. The centralized baseline has no communication model; the global-state mesh is an intentional strawman; the sectorized mesh provides fundamentally different functionality. Only the hierarchical architecture receives full treatment. While the authors acknowledge this (Table VI, various footnotes), the paper's structure—including the abstract and conclusions—still frames the comparison as evidence of hierarchical superiority. A fairer approach would be to compare the hierarchy against a properly designed decentralized alternative with equivalent functional scope, or to explicitly frame the paper as a single-architecture sizing study rather than a comparative analysis.

3. **The DES provides implementation verification, not model validation, yet the paper's claims extend to system design recommendations.** The $<0.1\%$ DES-analytical agreement demonstrates that the code correctly implements the equations—nothing more. The slot-level TDMA simulator adds value but still operates at a high abstraction level. The gap between "message-layer prediction" and "design equation" is significant: practitioners using these equations need confidence that the message-layer model captures the dominant effects, which requires at least one level of physical-layer validation. The paper should either downgrade its claims from "design equations" to "message-layer scaling relationships" or provide physical-layer evidence.

4. **Static topology assumption is inadequately justified for the target application.** LEO mega-constellations have continuous relative motion between orbital planes. The claim that re-association adds "$<0.5\%$ overhead" (Section V-B) is unsupported by analysis or simulation. For a paper that performs byte-level accounting to 0.1% precision, an unquantified 0.5% dynamic overhead is a significant gap. The co-orbital case (static for hours) applies only to a subset of cluster configurations; cross-plane clusters—which may be necessary for conjunction screening—would experience continuous membership changes.

---

## Minor Issues

1. **Abstract length:** At 250+ words, the abstract exceeds typical IEEE T-AES guidelines (~150–200 words) and contains excessive detail (specific equation references, numerical values to three significant figures). Consider condensing to key findings and scope.

2. **Eq. (4), mesh message count:** The notation $O(N \cdot f \cdot \log N) = O(N^2)$ with $f = N/\log N$ is correct but the intermediate step is confusing. Write directly: $M_{\text{mesh}} = O(N^2)$ with the fanout choice noted separately.

3. **Table II, "AoI P99 (exception)" row:** The footnote states AoI is unchanged across bandwidth regimes, but this assumes $p_{\text{exc}}$ and $T_c$ are held constant. If higher bandwidth enables full reporting ($p_{\text{exc}} = 1.0$), AoI drops to 10 s. The table should note this conditional.

4. **Section III-B, coordinator processing rate:** $\mu_c = 200$ msg/s (5 ms/msg) is stated as "including integrity check" but no justification is provided for this processing time on representative spacecraft processors. A reference to RAD750 or similar flight processor benchmarks would help.

5. **Table III, collision avoidance rate:** $10^{-4}$/node/s yields ~0.86 alerts/node/day. The footnote says these are "screening notifications," but no reference supports this rate. ESA's conjunction screening generates far fewer actionable alerts per satellite per day.

6. **Eq. (12), AoI P99 analytical:** The ceiling function makes this a step function in $p_{\text{exc}}$, but the DES produces continuous values. The 441 s DES value vs. 440 s analytical is within one $T_c$ step—this agreement is trivial, not a meaningful cross-check.

7. **Section IV-A, "Raft election completes in $\ll 1$ ms":** This assumes no message loss during election. Under the GE model with $p_B = 0.90$, election could require multiple rounds. The 113 s RF-backup estimate accounts for this but the optical-ISL claim does not.

8. **Table V, superframe budget:** The "unallocated margin" of 623 ms is 6.2% of $T_c$. The paper calls this adequate but does not account for clock drift accumulation over multiple cycles without re-sync, or for the ranging overhead mentioned as ~50 ms.

9. **Section III-E, "Baseline telemetry excluded from $\eta$":** This accounting choice makes the headline $\eta \approx 46\%$ appear lower than the actual channel utilization ($\eta_{\text{total}} \approx 67\%$). While internally consistent, it could mislead readers who expect $\eta$ to represent total overhead.

10. **Typo/formatting:** In Table III footnotes, superscript labels jump from (a) to (c) to (d), skipping (b).

11. **Section IV-H, Table IX:** Latency values for $k_c = 100, 200, 500$ at $N = 10^4$ are all identical (340 ms), which seems unlikely unless the model is insensitive to $k_c$ above some threshold. This deserves explanation.

12. **Reference [nrl_swarm]:** Cited in the bibliography but does not appear to be referenced in the text.

---

## Overall Recommendation

**Major Revision**

This paper addresses a legitimate gap in the literature and provides a well-structured analytical framework for sizing hierarchical coordination in large autonomous space swarms. The three-layer feasibility decomposition, the TDMA pipeline decoupling result, and the GE inter-cycle recovery characterization are useful contributions. The transparency about limitations (claim map, validation gap acknowledgment, open-source tools) is commendable and above average for the field.

However, the paper requires major revision for three reasons: (1) the absence of any physical-layer validation makes the "design equations" label premature—the results are message-layer scaling relationships that need at least one level of physical-layer grounding before they can guide engineering practice; (2) the topology comparison is structurally unfair and should either be reframed as a single-architecture study or supplemented with a properly scoped decentralized alternative; and (3) the static topology assumption is inadequately justified for the LEO mega-constellation application domain. Additionally, the paper is overlength and repetitive, and would benefit from significant condensation. With these issues addressed, the paper could make a solid contribution to IEEE T-AES.

---

## Constructive Suggestions

1. **Conduct a single-cluster NS-3 simulation** (the authors' own stated priority) and include results in the revised paper. Even a simplified physical-layer model (e.g., TDMA with realistic guard times, propagation loss, and half-duplex constraints at S-band) would dramatically strengthen the "design equations" claim. This need not be a full mega-constellation simulation—a single 100-node cluster at 24–30 kbps would suffice to validate or calibrate $\gamma$.

2. **Reframe the paper as a single-architecture sizing study** rather than a four-way comparison. The hierarchical analysis is thorough and self-contained; the centralized and global-mesh baselines add little beyond obvious bounds. The sectorized mesh comparison is the most interesting but is undermined by the functional scope mismatch. Either develop the sectorized mesh to equivalent functional scope (e.g., with multi-hop gossip for cluster-equivalent awareness) or present it explicitly as a "local monitoring only" alternative with clearly different use cases.

3. **Derive or reference GE parameters from physical channel models.** Map the S-band LEO inter-satellite link to a specific propagation scenario (e.g., structural shadowing statistics from ISS or similar platforms, antenna pattern measurements, or ITU-R P.618 rain attenuation models). Even order-of-magnitude physical grounding would transform the GE analysis from a parametric exercise into a predictive tool.

4. **Quantify dynamic topology overhead** through a dedicated simulation experiment. Model a Walker constellation (e.g., 72 planes × 22 satellites/plane ≈ 1,584 satellites) with realistic relative motion, trigger cluster re-associations when inter-plane distance exceeds a threshold, and measure the actual overhead including state transfer, election, and AoI transients. This directly addresses the $<0.5\%$ claim.

5. **Shorten the paper by 25–30%** by eliminating repetitive restatements of key numbers, consolidating the 16 figures (several could become subfigures or move to supplementary material), and tightening the abstract to ~150 words. The design equations summary (Section V-C) is excellent and could serve as the primary results presentation, with the detailed derivations in an appendix or supplementary document.