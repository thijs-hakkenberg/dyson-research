---
paper: "02-swarm-coordination-scaling"
version: "by"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-28"
recommendation: "Major Revision"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap: the absence of closed-form parametric sizing relationships for coordination architectures at the $10^3$–$10^5$ node scale with byte-level traffic accounting. The three-layer feasibility decomposition (byte budget, MAC efficiency, TDMA airtime) is a useful conceptual contribution that could serve as a practical engineering framework. The separation of topology-dependent ($\eta_0$) and workload-dependent ($\eta_{\text{cmd}}$) overhead is clean and potentially valuable for system architects.

However, the novelty is more limited than the framing suggests. The core finding—that architecture-specific overhead is small (~5%) while command traffic dominates (~41%)—is, upon reflection, somewhat predictable: in any hierarchical system with $O(1)$ aggregation messages per coordinator per cycle, the coordination overhead will be dwarfed by payload-level traffic at sufficient command rates. The closed-form equations themselves (Eqs. 2–8) are relatively straightforward applications of queueing theory, geometric distributions, and Markov chains. The GE channel analysis, while well-executed, applies standard two-state Markov models without methodological innovation.

The paper's claim of being the first to provide such sizing relationships (Section I-A) is difficult to fully verify. While the specific combination of byte-level accounting + hierarchical coordination + $10^4$–$10^5$ scale may indeed be novel, the individual components draw heavily on well-established techniques. The LEACH-inspired clustering, Raft-based election, SWIM failure detection, and GE channel model are all existing building blocks assembled here rather than fundamentally new contributions. The paper would benefit from more precisely delineating what is novel in the *assembly* versus the *components*.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The methodology has notable strengths in its transparency and multi-level verification approach. The IEEE 1012 verification taxonomy (Section III-A) is commendable, and the honest acknowledgment that physical-layer validation is absent (Table VII) is refreshing. The slot-level TDMA simulator provides genuine model verification beyond the cycle-aggregated DES, and the joint interaction analysis (Table V) reveals the ARQ-coupling phenomenon that the fluid-server DES cannot capture.

Several methodological concerns warrant attention:

**Circular verification.** The DES-to-analytical match of $<0.1\%$ (Table VI) is presented as verification, but the authors correctly note this is "expected by construction." When the DES implements the same equations it is verifying, agreement confirms only code correctness, not model validity. This distinction is stated but could be more prominently flagged—readers may over-interpret the $<0.1\%$ agreement as evidence of model fidelity rather than implementation consistency.

**Static topology assumption.** The fixed cluster membership over one year is a significant simplification. The $<0.5\%$ re-association overhead estimate (Section V-B) accounts only for byte cost, not for the transient degradation in coordination quality during re-association events. In a Walker constellation with ~72 planes, cross-plane encounters are frequent and the assumption that "AoI transient during state rebuild: +30 s" is modest requires more rigorous justification—particularly for the conjunction screening use case where precisely these orbital geometry changes drive the coordination need.

**Monte Carlo adequacy.** 30 replications with SD $< 0.001\%$ for overhead metrics suggests the variance is dominated by the deterministic message model rather than stochastic effects. This raises the question of what the MC replications are actually testing. The tail statistics (AoI P99, GE recovery P95) are more meaningful MC targets, but the reporting of "mean of 30 per-run P99 values" conflates within-run and between-run variability. A more rigorous approach would report the distribution of per-run P99 values explicitly.

**$\gamma$ as an abstraction.** While pragmatic, absorbing all physical-layer effects into a single scalar parameter $\gamma$ is a strong assumption. Real MAC protocols exhibit state-dependent efficiency (e.g., contention-based protocols degrade nonlinearly with offered load), and the interaction between $\gamma$ and GE loss states could be significant. The paper acknowledges this (Section V-A) but the degree to which the results depend on this independence assumption is not quantified.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The internal logic of the paper is generally sound within its stated assumptions. The three-layer feasibility framework is logically coherent, and the progression from byte budget through MAC efficiency to airtime scheduling is well-motivated. The analytical cross-checks (AoI P99 via geometric distribution, GE recovery via Markov chain) provide appropriate independent verification of the DES.

Several logical concerns arise:

**Topology comparison fairness.** Despite extensive caveats (Section III-B-4, Table IV), the paper still presents overhead numbers for the sectorized mesh alongside the hierarchical architecture in figures and tables (Fig. 6, Table VIII). The repeated disclaimers about "different functional scope" are necessary precisely because the comparison is structurally unfair—yet the visual juxtaposition inevitably invites the reader to conclude the hierarchy is superior. If the comparison is truly not meaningful (as stated), the sectorized mesh results should be presented in a clearly separated section or appendix rather than interleaved throughout the results.

**Stress-case dominance by commands.** The central finding that $\eta_{\text{cmd}} \gg \eta_0$ under stress conditions is valid but somewhat tautological: the stress case is *defined* as $p_{\text{cmd}} = 1.0$ with 512 B commands, which by construction dominates the 64 B heartbeats and 512 B summaries (shared among $k_c$ nodes). The more operationally relevant question—how often does the stress case actually occur, and for how long—is not addressed. The paper would benefit from a temporal workload model showing the fraction of operational time spent in each regime.

**Coordinator failure analysis.** The compound probability calculation ($6.3 \times 10^{-12}$ s$^{-1}$) for simultaneous ISL outage and coordinator failure assumes independence between these events. However, the scenarios most likely to cause ISL outages (solar particle events, debris impacts) are precisely those that could also cause coordinator failures. The correlated failure mode is acknowledged as future work (Section V-B) but the independence-based probability is presented as a design number, which could be misleading.

**AoI interpretation.** The claim that AoI P99 = 441 s is acceptable because it is "$< 0.5\%$ of a 24 h response window" (Section IV-B) conflates two different operational contexts. The 24 h window applies to ground-based conjunction assessment; the in-orbit coordination system presumably exists because faster response is needed. The paper should more carefully distinguish between the AoI requirements for different operational functions.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is generally well-organized and clearly written. The notation table (Table I) is helpful, the roadmap paragraph at the start of Section IV provides useful orientation, and the design equations summary (Section V-C) is a practical reference. The three-layer feasibility framework provides a clear conceptual scaffold.

Several structural issues reduce readability:

**Length and repetition.** The paper is extremely long for a journal article, with substantial repetition. The caveats about sectorized mesh functional scope appear at least 5 times (Sections I-C, III-B-4, IV-G, Table VIII, and the conclusion). The $\gamma$ absorption disclaimer appears similarly often. While thoroughness is appreciated, this repetition suggests the paper could be significantly condensed without loss of content—perhaps by 25-30%.

**Table density.** The paper contains 14 tables, many with extensive footnotes that carry critical information. Table III (Simulation Parameters) alone spans nearly a full column with three levels of footnotes. While comprehensive, this density makes it difficult to identify the key parameters versus secondary details. A hierarchical presentation—core parameters in the main table, secondary parameters in an appendix—would improve readability.

**Figure references.** Several figures are referenced but their content must be inferred from captions alone (as the actual image files are not available for review). The captions are generally descriptive, but Fig. 1 (architecture diagram) is critical for understanding the hierarchy and should be verified for clarity.

**Abstract accuracy.** The abstract is accurate but dense. The parenthetical parameter instantiation reads more like a results table than an abstract summary. Consider leading with the conceptual contribution and providing one or two key numbers rather than the full parameter set.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper makes appropriate disclosures regarding AI assistance in the Acknowledgment section, noting that "Claude 4.6, Gemini 3 Pro, GPT-5.2" were used for ideation but that the results are "not validated here." The data availability statement is exemplary, providing a specific GitHub repository with tagged release, environment specifications, and runtime estimates. The open-source commitment for both the DES and TDMA simulator supports reproducibility.

The author attribution is unusual ("Project Dyson Research Team" with a footnote promising individual names for final publication). While this may comply with IEEE policy, it prevents assessment of author qualifications and potential conflicts of interest. The reference to the team's own multi-model AI deliberation paper [dyson_multimodel] as a self-citation should be noted.

One minor concern: the AI tools referenced (Claude 4.6, GPT-5.2) appear to be future versions not yet publicly available as of mid-2025, which raises questions about the timeline of this work. This should be clarified.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in its treatment of autonomous spacecraft coordination, though it sits at the boundary between systems engineering and communications engineering. The reference list is comprehensive (55 references) and covers the relevant domains: constellation operations, swarm robotics, distributed systems, queueing theory, and channel modeling.

Several referencing gaps exist:

**Missing key references.** The paper does not cite recent work on distributed space systems coordination from the SmallSat and CubeSat communities, where actual multi-spacecraft coordination has been demonstrated (e.g., Planet Labs operations, Spire Global). The CCSDS Spacecraft Onboard Interface Services (SOIS) standards, which address intra-spacecraft and inter-spacecraft communication architectures, are also absent. Recent work on LEO mega-constellation interference and spectrum management (relevant to the RF-backup channel) is not discussed.

**Non-archival sources.** Several references are non-archival (SpaceX FCC filings, Amazon web pages, DARPA program pages, DOD fact sheets). While some are unavoidable for current operational systems, the paper relies on these for key claims about current constellation sizes and operational approaches. Where possible, peer-reviewed or standards-body sources should be substituted.

**GE model grounding.** The Lutz et al. [1991] reference for GE parameterization is appropriate but dated. More recent LEO channel measurement campaigns (e.g., from ESA's ARTES program or recent ISL characterization studies) would strengthen the parameter justification. The analogy between terrestrial mobile shadowing and ISL self-blockage (Section IV-C) is acknowledged as approximate but deserves more careful treatment—the physical mechanisms are quite different.

---

## Major Issues

1. **Validation gap is too large for the claims made.** The paper derives sizing equations and verifies them against a simulation that implements those same equations. The slot-level TDMA simulator adds value but still operates at an abstracted level. No comparison against any real system data, hardware-in-the-loop test, or high-fidelity packet-level simulation is provided. The paper should either (a) include at least a single-cluster NS-3 validation for the most critical result (coordinator ingress sizing), or (b) substantially temper the claims to "analytical framework pending validation" rather than "design equations."

2. **The 1 kbps constraint drives all interesting results but is poorly justified.** The paper states this is an "RF-backup channel for ISL outages (<1% of lifetime)" yet devotes the majority of analysis to this regime. The justification for 1 kbps specifically (vs. 2, 5, or 10 kbps) is not provided—is this based on a link budget? A regulatory constraint? A heritage system? Since Table II shows that at ≥10 kbps "all constraints [are] non-binding," the entire analytical framework collapses to trivial feasibility for the primary (optical ISL) operating mode. The paper needs to either (a) provide a rigorous link budget justifying 1 kbps, or (b) reframe the contribution as characterizing the design space across bandwidth regimes rather than anchoring on a specific value.

3. **Static topology invalidates the most operationally relevant scenarios.** The conjunction screening use case—arguably the primary motivation for autonomous coordination—requires coordination precisely when orbital geometries are changing (close approaches between different orbital planes). Fixed cluster membership cannot capture this dynamic. The 0.22% re-association overhead estimate is a steady-state average that ignores the transient coordination degradation during the events that matter most.

4. **The sectorized mesh comparison is structurally flawed and should be restructured.** Despite extensive disclaimers, the paper repeatedly juxtaposes hierarchical and sectorized mesh overhead numbers. If the architectures serve different functions (as stated), the comparison is meaningless and should not appear in the same figures/tables. If they serve overlapping functions (as implied by including both), the comparison should be on equal functional footing. The current treatment tries to have it both ways.

## Minor Issues

1. **Eq. 1** is not really an equation—it's a label for the hierarchy levels. Consider replacing with a figure reference or removing the equation number.

2. **Table III** footnote (c): "$\mu_c = 200$ msg/s (5 ms/msg including integrity check)"—the integrity check time should be justified. Is 5 ms realistic for a space-grade processor? CRC-16 computation on 256 B is microseconds on modern hardware.

3. **Section IV-A**, "Fleet-wide TDMA cost is 0.28 kbps/node (1% coordinators at $k_c = 100$)"—this amortization assumes uniform coordinator distribution, which may not hold during failure transients.

4. **Table V** column headers: "GE+Exc" is not immediately clear; expand to "GE $M_r=0$ + Exception" or similar.

5. **Section IV-B**: The AoI analytic cross-check (Eq. 6) uses a ceiling function on a continuous expression, but the DES reports 441 s vs. analytical 440 s. The 1 s difference is within the ceiling discretization—state this explicitly.

6. **Section III-B-2**: "Coordinator rotation: state transfer (10–50 MB) over optical ISL, excluded from $\eta$"—this exclusion should be justified more carefully. At 10 MB, this is a significant traffic burst that could affect other nodes' coordination during the transfer.

7. **Acknowledgment section**: The AI model versions cited (Claude 4.6, GPT-5.2) do not correspond to publicly known releases. Clarify whether these are internal designations or future versions.

8. **Bibliography**: Reference [1] cites both an FCC filing and a non-archival website in the same entry. These should be separated.

9. **Section IV-A**, Eq. 5 ($L_{\text{cmd}}$): The denominator uses $T_c \cdot (1 - \alpha_{\text{RX}})$ but $\alpha_{\text{RX}}$ is defined only implicitly through the superframe budget. Define $\alpha_{\text{RX}}$ explicitly in the notation table or at first use.

10. **Table IX**: "Handoff Success" percentages (95.0%–99.9%) are presented without derivation or reference. How are these computed?

## Overall Recommendation

**Major Revision**

The paper presents a well-structured analytical framework for a relevant problem, with commendable transparency about limitations and open-source commitment. However, three fundamental issues prevent acceptance in the current form: (1) the validation gap between message-layer equations and physical reality is too large to support "design equation" claims for IEEE T-AES readership; (2) the 1 kbps anchor point that drives all non-trivial results lacks rigorous justification; and (3) the static topology assumption undermines the operational relevance of the results for the conjunction screening use case that motivates the work. The sectorized mesh comparison needs restructuring. With a focused NS-3 validation of the coordinator ingress bottleneck, a link budget justifying the bandwidth regime, and honest reframing of the static-topology limitation's impact, this could become a solid contribution.

## Constructive Suggestions

1. **Add a single-cluster NS-3 validation.** Even a simplified model (100 nodes, TDMA, GE channel, one coordinator) would dramatically strengthen the paper. Focus on validating the coordinator ingress sizing equation and the ARQ infeasibility finding—these are the most impactful claims. The superframe budget (Table VI) provides an excellent specification for this validation.

2. **Provide a link budget for the RF-backup channel.** Derive the 1 kbps (or whatever value emerges) from first principles: transmit power, antenna gain, path loss at representative ISL distances, noise figure, required $E_b/N_0$, and available bandwidth. This grounds the entire analysis in physical reality and allows readers to assess whether 1 kbps is conservative, aggressive, or representative.

3. **Restructure the topology comparison.** Move the sectorized mesh to a self-contained appendix or separate subsection clearly labeled "Reference Baseline for Local Monitoring." Remove it from comparative figures (Fig. 6) and tables (Table VIII) that invite direct overhead comparison with the hierarchical architecture. Instead, present a clear statement of when each architecture is appropriate based on functional requirements.

4. **Add a temporal workload model.** Characterize the expected fraction of operational time in each workload regime (nominal, event-driven, stress). Even a simple estimate (e.g., "stress conditions occur during orbit-raising campaigns lasting ~2 weeks per year") would help practitioners assess whether the stress-case overhead matters for their mission.

5. **Quantify the dynamic topology impact more rigorously.** For a Walker constellation, compute the re-association frequency per cluster, the distribution of simultaneous re-associations across the fleet, and the resulting AoI transient distribution. This could be done analytically from orbital mechanics without requiring a full dynamic DES, and would significantly strengthen the operational relevance claims.