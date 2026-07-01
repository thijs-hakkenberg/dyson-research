---
paper: "02-swarm-coordination-scaling"
version: "ak"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms"

**Manuscript Version:** AK
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuinely important problem: how to coordinate autonomous spacecraft swarms at scales of 10³–10⁵ nodes. The gap identified—the absence of systematic byte-level traffic accounting for hierarchical coordination at these scales—is real. The literature review correctly identifies that swarm robotics work rarely exceeds hundreds of agents, constellation management literature stops at ~10⁴ nodes, and networking literature focuses on routing rather than coordination overhead. The combination of these perspectives is valuable.

However, the novelty claim is significantly weakened by the authors' own candid admissions. The $O(1)$ overhead scaling is described as "an analytical property of the fixed-depth hierarchical message structure" (Section I-D), and the DES-to-analytical agreement is within 0.1% at all fleet sizes. The four headline results—coordinator capacity sizing, AoI geometric tail, GE retransmission degradation, and the workload envelope—are each analytically tractable and confirmed by closed-form expressions. The DES's unique contribution is narrowed to verifying "compositionality under joint conditions" (Section IV-D), where the independence result (Table 8) is itself explained by the architectural separation of link loss and coordinator ingress stages. This is a useful engineering verification, but it is not a discovery—it is a confirmation of what the architecture's structure already implies. The paper reads more as a thorough parametric design handbook than a research contribution revealing new phenomena.

The practical significance is further diluted by the dual-regime interpretation (Section IV-F-3): under normal optical ISL operation (100 kbps allocation), overhead is 0.46%—"engineering-irrelevant" by the authors' own words. The 1 kbps regime that makes overhead matter is entered <1% of operational time. While the authors correctly argue this is the critical design point, it limits the operational impact of the findings.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The simulation framework is clearly described and the parameter choices are generally well-justified. The cycle-aggregated DES approach is appropriate for the message-layer abstraction, and the authors are commendably transparent about what is and is not modeled (Table 5). The Monte Carlo framework (30 replications, bootstrap CIs) is standard, though the near-zero variance (SD < 0.001%) renders it largely ceremonial—a point the authors acknowledge.

**Strengths:** The traffic accounting (Table 6) is meticulous. The separation of baseline telemetry from protocol overhead is clean. The coordinator capacity analysis (Section IV-A) with four scheduling models (deadline, leaky-bucket, TDMA, phase-stagger) is thorough and provides actionable engineering guidance. The TDMA feasibility vignette grounds the abstract capacity numbers in physical parameters.

**Concerns:**

First, the "cycle-aggregated DES" is described as "vectorized array operations over N nodes" (Section III-F) with ~7s wall-clock at N=10⁵. This is essentially a Monte Carlo spreadsheet calculation, not a discrete event simulation in the traditional sense. There is no event queue driving asynchronous interactions; all nodes act synchronously within each 10s cycle. The 1-second resolution for collision avoidance events is mentioned but its implementation within the vectorized framework is unclear. Calling this a "DES" may mislead readers expecting packet-level or event-driven simulation fidelity.

Second, the centralized baseline with c=1 is acknowledged as an "intentional worst-case bound," but it still appears in the topology comparison table (Table 10) and Figure 7 as a primary comparator. The realistic centralized baseline (c=N/k_c) is discussed textually but not given equal visual prominence. This creates a misleading impression in figures that the hierarchical architecture dramatically outperforms centralized coordination, when in fact the realistic centralized system "does not diverge computationally until N ≈ 10⁶."

Third, the sectorized mesh comparator uses a $\sqrt{N}$ sector size justified by a "simple orbital density argument" that is acknowledged as "an order-of-magnitude sizing, not a precise orbital mechanics calculation." The capped fanout of 10 neighbors is a design parameter whose sensitivity is explored (Table 4) but whose operational adequacy for conjunction screening is explicitly left unresolved. This makes the 1.4–1.5× overhead ratio between sectorized mesh and hierarchical architectures dependent on an unvalidated parameterization.

Fourth, the GE channel model parameters ($p_{GB}=0.05$, $p_{BG}=0.20$) are stated without justification from empirical LEO link data. The steady-state availability of 80% seems pessimistic for optical ISLs (>99% cited elsewhere in the paper) and optimistic for RF backup during the anomaly conditions where it would be used. The mismatch between the GE parameterization and the operational scenarios where it applies undermines the quantitative specificity of the correlated loss results.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The internal consistency of the paper is strong. Analytical cross-checks match DES results throughout (AoI P99: 440s analytical vs. 441s DES; overhead: 46.1% analytical vs. 46.0% DES). The logic of each individual analysis is sound. The authors are unusually forthright about limitations—the discussion of what the DES does and does not contribute is among the most honest I have seen in a simulation paper.

**However, several logical issues deserve attention:**

The joint independence result (Section IV-D, Table 8) is presented as a key DES contribution, but the explanation reveals it is architecturally determined: "lost messages never contend for coordinator capacity, and retransmission attempts that also fail likewise never arrive." The authors correctly note this holds only for point-to-point ISLs and not shared-medium architectures. But since the entire paper assumes point-to-point ISLs, the independence is a structural property of the model, not an empirical finding. The DES confirms what the model definition implies. The claim that "the magnitude of the relief (three orders of magnitude fewer drops) would not be straightforward to predict from separate single-factor models" is debatable—the offered load reduction from $p_{exc}=0.10$ is a factor of 10, and the nonlinear relationship between offered load and drops in a finite-buffer queue is well-characterized by Erlang-B formulas.

The AoI-to-position-error coupling (Eq. 12) is appropriately caveated as "order-of-magnitude," but the 230m figure at P99 is then compared to the 1km conjunction screening threshold—a comparison the authors themselves warn against drawing conclusions from. This creates a tension: either the coupling is too approximate to be useful (in which case why include it?) or it provides meaningful operational context (in which case the caveats are excessive). A clearer framing would help.

The paper claims the hierarchical architecture's advantages are "fault tolerance during ground outages (7–29 min/day)" and "spectrum independence (100 Mbps aggregate uplink at N=10⁵)." The ground outage analysis (0.5–2% per station) does not account for multi-station ground networks with geographic diversity, which is standard practice for operational constellations. Starlink, for instance, operates hundreds of ground stations. The spectrum argument (100 Mbps at 10⁵ nodes) is valid but applies to the coordination channel only; the same nodes presumably require far more bandwidth for their primary mission data.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is exceptionally well-organized for its length and complexity. The roadmap at the beginning of Section IV is helpful. The consistent use of traffic accounting tables, the clear separation of offered vs. delivered overhead, and the systematic presentation of analytical cross-checks alongside DES results all aid comprehension. The design equations summary (Section V-C) is a valuable practitioner-oriented addition.

**Strengths:** Table 5 (Simulation Abstraction Scope) is an exemplary disclosure of modeling boundaries. The dual-column format of "Modeled" vs. "Abstracted" should be adopted more widely. The footnotes throughout the tables provide essential context without cluttering the main text. The figures are well-captioned with appropriate caveats (e.g., Figure 8 noting the 10⁶ curve is extrapolated).

**Weaknesses:** The paper is very long for a journal article—likely exceeding IEEE TAES page limits even in two-column format. There is substantial redundancy: the 46% overhead figure is stated at least 15 times; the $1/\gamma$ MAC correction is mentioned in the abstract, introduction, multiple results subsections, and conclusion. The coordinator capacity analysis alone spans ~2.5 pages with four models, a TDMA vignette, and a phase-stagger experiment—thorough but potentially condensable.

The notation is generally consistent but occasionally confusing: $r$ is used for both reporting rate and screening radius (Eq. 7 context); $\mu_s$ vs. $\mu_c$ vs. $\mu_r$ for different processing capacities could benefit from a notation table. The distinction between $\eta$ (offered protocol overhead), $\eta_{delivered}$, $\eta_{eff}$, $\eta_{total}$, $\eta_{sector}$, and $\eta_S/\eta_N/\eta_E$ requires careful tracking.

Section III is disproportionately long (~60% of the paper) relative to the results and discussion. Much of the sectorized mesh development (Section III-B-4) could be condensed or moved to an appendix.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The AI assistance disclosure in the Acknowledgment section is transparent: Claude 4.6, Gemini 3 Pro, and GPT-5.2 were used for "exploratory AI-assisted ideation" with a companion methodology paper cited. The disclosure that the Shepherd/Flock concept "is not validated in the current study but motivated aspects of the coordinator hardware discussion" is appropriately scoped.

The data availability statement is strong, with specific repository URLs, version tags, and software environment details. The Monte Carlo seed strategy (sequential, 42–71) enables exact replication.

One concern: the author block lists "Project Dyson Research Team" with a note that "Individual author names and affiliations will be provided for final publication per IEEE policy." IEEE requires author identification for peer review; anonymous team submissions are not standard practice for TAES. The reviewers and editors should verify compliance with IEEE authorship policies.

The references to future AI model versions (Claude 4.6, GPT-5.2) that do not exist as of the review date raise questions about the manuscript's provenance and timeline. This should be clarified.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is within scope for IEEE TAES, which publishes work on space systems, autonomous systems, and communication architectures. The combination of distributed systems theory, queueing analysis, and space systems engineering is appropriate for the journal's readership.

The reference list (50 entries) is comprehensive and spans the relevant domains: constellation operations (Starlink, Iridium, OneWeb), distributed algorithms (Lamport, Raft, SWIM), swarm robotics (Brambilla, Dorigo), queueing theory (Kleinrock), AoI (Kaul, Yates, Kadota), and space standards (CCSDS). The mix of archival and non-archival sources is appropriate given the rapidly evolving operational landscape.

**Gaps:** The paper does not cite recent work on distributed spacecraft autonomy from the small-sat community, particularly CubeSat swarm demonstrations (e.g., NASA's Starling mission, 2023) that have begun to address coordination at small scales with real hardware. The CCSDS DTN working group's recent publications on store-and-forward for LEO constellations are relevant to the inter-cycle recovery discussion but not cited beyond BPv7. The AoI literature has expanded significantly since 2021; more recent scheduling-theoretic results (e.g., Bedewy et al., Maatouk et al.) on AoI optimization under resource constraints would strengthen Section IV-B.

Several references are non-archival (SpaceX website, Amazon website, DARPA program pages, DoD fact sheets). While understandable for operational programs, these should be minimized in a journal publication. The self-citation to the "companion methodology paper" [43] hosted on the project website is not peer-reviewed and should be noted as such.

---

## Major Issues

1. **The DES adds minimal value beyond analytical verification.** The paper's own cross-checks show <0.1% disagreement between closed-form predictions and DES results for overhead, <1 cycle for AoI, and exact agreement for retransmission success. The joint independence result (Section IV-D) is architecturally determined. The paper should either (a) identify a specific result that the DES produces which analytical methods cannot, or (b) reframe the contribution as a validated parametric design tool rather than a simulation study. Currently, the title promises a "Discrete Event Simulation Study" but the DES confirms what the equations already predict.

2. **The centralized baseline comparison is misleading as presented.** The realistic centralized baseline (c=N/k_c) does not diverge until N≈10⁶, yet figures and the topology comparison table give visual prominence to the c=1 bound. The hierarchical architecture's quantified advantages (ground outage tolerance, spectrum independence) are real but modest: 7–29 min/day of lost coordination and 100 Mbps aggregate uplink. These should be the lead comparison, not the artificial c=1 divergence. Figures 7 and 8 should include the realistic centralized baseline as a curve.

3. **The GE channel parameters lack empirical grounding.** The steady-state 80% availability, $p_{GB}=0.05$, $p_{BG}=0.20$ per 10s cycle are stated without reference to measured LEO link statistics. Given that the correlated loss characterization is a headline contribution, the channel model parameters should be justified from published link measurement campaigns or at minimum subjected to broader sensitivity analysis.

4. **The "DES" terminology is misleading.** A vectorized, synchronous, cycle-level computation with ~7s runtime at 10⁵ nodes is not a discrete event simulation in the standard sense (no asynchronous event queue, no packet-level modeling, no MAC-layer interaction). The paper should use a more accurate term—e.g., "cycle-level Monte Carlo simulation" or "message-layer parametric model"—to set appropriate expectations.

5. **Missing validation against any real or high-fidelity system.** The DES is validated only against its own analytical predictions. There is no comparison to operational constellation data (even aggregate statistics from Starlink's published conjunction avoidance cadence), no packet-level simulation cross-check (acknowledged as future work), and no hardware-in-the-loop validation. For a journal publication claiming to provide "design-space characterization," at least one external validation point is expected.

---

## Minor Issues

1. **Abstract length:** At ~280 words, the abstract exceeds IEEE TAES guidelines (typically 150–200 words). The parenthetical qualifications and specific numeric values could be condensed.

2. **Eq. 4 (mesh messages):** The derivation jumps from $f = O(N/\log N)$ to $O(N^2)$ without showing the intermediate step. The choice of this specific fanout to produce the $O(N^2)$ bound should be motivated—standard gossip uses $f = O(\log N)$.

3. **Table 1 (M/D/c sensitivity):** The "Hyperscale data center" row ($c=1000$, $N_{max}=10^7$) is unrealistic for space coordination and dilutes the table's relevance. Consider removing or replacing with a more plausible provisioning level.

4. **Section III-B-4, Eq. 8:** The sector overhead formula omits the inter-sector relay component mentioned in the text (512 B × ≤2 for boundary nodes). The analytical $\eta_{sector}$ in Table 4 footnote includes commands but the equation does not.

5. **Table 7 (coordinator bandwidth):** The $C_{coord}=1$ kbps row showing 100% drops and 0% delivery is trivially obvious and wastes table space. Consider starting at 5 kbps.

6. **Section IV-A, TDMA vignette:** "Counter-rotating or crossing-orbit nodes would belong to different clusters" is stated without justification. How are clusters assigned in practice? The paper assumes cluster membership is given but never discusses the cluster formation problem.

7. **Figure references:** Several figures (Fig. 1, architecture diagram) reference PDF files that cannot be verified in review. The paper should confirm all figures are generated from the cited repository scripts.

8. **Section III-E (Communication Overhead Definition):** The statement "confirms that deterministic scheduling (TDMA) is required" based on exceeding Slotted ALOHA throughput is correct but applies only to the stress-case workload. Under nominal workloads ($\eta \approx 5\%$), total utilization is ~25%, which is below the ALOHA limit.

9. **Typo/formatting:** In Table 2, footnote marker "a" appears twice with different meanings. Table 9 footnote markers are inconsistent (a, b, c used but b appears in two different contexts).

10. **Reference [43] (dyson_multimodel):** This is a self-hosted, non-peer-reviewed publication. It should be clearly marked as a preprint/technical report, not presented alongside peer-reviewed references.

---

## Overall Recommendation

**Major Revision**

This is a carefully executed parametric study with meticulous traffic accounting and commendable transparency about limitations. The engineering content—coordinator capacity sizing, AoI characterization, workload envelope—is useful for practitioners designing large-constellation coordination systems. However, the paper's contribution as a *research* paper is undermined by the near-perfect agreement between analytical predictions and DES results, which raises the question of what the simulation adds beyond verification. The centralized baseline comparison needs rebalancing to avoid overstating the hierarchical architecture's advantages. The GE channel model requires empirical grounding. The paper would benefit from either (a) identifying a genuinely emergent result that only the DES can produce (e.g., by adding MAC contention or correlated failures), or (b) repositioning as a design handbook/tool paper with reduced novelty claims. In its current form, the gap between the ambitious framing ("characterizing hierarchical coordination scaling") and the actual findings (confirming analytical predictions with a fast numerical model) is too large for a top-tier journal publication without revision.

---

## Constructive Suggestions

1. **Add a MAC-contention experiment for at least one cluster.** Even a simplified CSMA model within a single 100-node cluster would provide a result that analytical methods cannot easily predict and would ground the $\gamma$ parameter. This would transform the joint-interaction analysis (Section IV-D) from confirming architectural independence to discovering contention-dependent coupling—a genuinely novel finding.

2. **Reframe the centralized comparison around the realistic baseline.** Lead with c=N/k_c in all figures and tables. Present the hierarchical advantage as a quantified trade-off: +46% overhead and +300ms latency in exchange for continuous coordination during 7–29 min/day ground outages and elimination of 100 Mbps aggregate uplink requirement. This honest framing is more compelling than the artificial c=1 divergence.

3. **Ground the GE model in published LEO link data.** Cite measured burst-error statistics from operational ISL systems (e.g., EDRS, Starlink v2 optical ISL performance reports) or atmospheric scintillation measurements. Alternatively, sweep GE parameters over a wider range and present results as a function of steady-state availability and mean burst duration, allowing readers to map to their own link conditions.

4. **Condense the paper by ~30%.** Move the sectorized mesh development and the full TDMA vignette to appendices. Consolidate the overhead verification (Section IV-F) with the workload envelope (Section IV-E)—both confirm scale-invariance. Reduce repetition of the 46% and $1/\gamma$ qualifications to first mention plus a forward reference.

5. **Add one external validation point.** Even a rough comparison to published Starlink conjunction avoidance statistics (e.g., ESA's reported ~3,000 close approaches per year requiring assessment, maneuver cadence of ~1/day) would anchor the collision avoidance event rate ($10^{-4}$/node/s) and provide a reality check on the coordination traffic model.