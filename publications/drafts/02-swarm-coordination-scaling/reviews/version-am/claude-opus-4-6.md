---
paper: "02-swarm-coordination-scaling"
version: "am"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a legitimate gap: systematic, byte-level characterization of coordination overhead for hierarchical space swarm architectures across the 10³–10⁵ node range. The framing around mega-constellation growth (Starlink, Kuiper) is timely, and the open-source parametric design tool contribution has practical value for the community. The identification of the RF-backup regime as the binding design point is a useful engineering insight that grounds the work in a concrete operational scenario.

However, the novelty is substantially tempered by the authors' own (commendable) honesty: the $O(1)$ overhead scaling "is an analytical property of the fixed-depth hierarchical message structure" (Section I-D), the AoI result matches a geometric distribution exactly, the GE recovery is a direct calculation, and the joint-independence finding follows from the architecture's point-to-point link assumption. The simulation confirms what the closed-form equations predict, with DES-to-analytical agreement consistently within 0.1–1.5%. While the authors frame this as "verification of compositionality," the reader is left wondering what the simulation *discovered* that was not already known from the design equations. The paper would benefit from a clearer articulation of a scenario where the DES revealed a non-obvious interaction or where analytical predictions broke down—the closest candidate is the cross-domain benefit of exception telemetry on coordinator drops (Section IV-D), but even this is described as a consequence of reduced offered load.

The comparison with centralized baselines is instructive but somewhat undermines the paper's own thesis: a realistically provisioned centralized system does not diverge until $N \approx 10^6$, and the hierarchical architecture's advantages (fault tolerance during ground outages, spectrum independence) are stated qualitatively rather than quantified through simulation. The paper would be stronger if it simulated ground outage scenarios directly rather than computing them analytically in the discussion.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The simulation framework is clearly described, reproducible (open-source code, fixed seeds, explicit parameter tables), and the cycle-aggregated approach is appropriate for the message-layer abstraction level. The Monte Carlo framework (30 replications, bootstrap CIs) is standard, and the authors correctly note that the near-deterministic message model renders MC variance negligible (SD < 0.001%)—which itself raises the question of whether 30 replications were necessary or whether a single deterministic run with analytical error bounds would have sufficed.

Several methodological concerns merit attention:

**The "DES" characterization is generous.** The simulation is described as "vectorized: per-cycle state updates are computed as array operations over $N$ nodes, not as explicit event objects" (Section III-F). This is closer to a cycle-stepped accounting model than a discrete event simulation in the traditional sense. While the authors acknowledge this distinction (Section III-A), the title and abstract prominently feature "Discrete Event Simulation," which may mislead readers expecting packet-level or event-driven modeling. The 7-second wall-clock time at $N = 10^5$ is impressive but also indicative of the abstraction level—a true DES with queueing dynamics would be orders of magnitude slower.

**The coordinator queueing model has internal tension.** Section III-B describes the coordinator as processing messages "continuously in arrival order" with $\mu_c = 200$ msg/s, yielding $\rho_c = 0.05$. But then it correctly notes the within-cycle dynamics resemble a $D[k_c]/D/1$ batch system. The DES cycle mechanics (Section III-F) process all reports in a single vectorized step per cycle, meaning the within-cycle queueing dynamics described analytically are not actually simulated—they are computed from the analytical batch model. This should be stated more explicitly.

**The sectorized mesh comparator has questionable parameterization.** The $\sqrt{N}$ sector sizing follows from a "simple orbital density argument" that the authors acknowledge is "an order-of-magnitude sizing, not a precise orbital mechanics calculation." The capped fanout of 10 neighbors provides only 3.2% sector coverage (Table VII), which the authors note is "likely insufficient for reliable conjunction screening" at cap = 5 but do not establish is sufficient at cap = 10. This weakens the sectorized mesh as a meaningful comparator.

**The Bernoulli link loss model and GE model are applied uniformly across all links.** In reality, link quality varies dramatically with geometry (co-orbital vs. cross-plane), and the GE state transitions should be correlated across links sharing similar geometries. The i.i.d. per-link GE assumption is acknowledged but not explored.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The analytical cross-checks are thorough and the DES-to-analytical agreement is excellent, which simultaneously validates the simulation and raises the question of its necessity. The conclusions are generally well-supported, with appropriate caveats. Several logical issues deserve attention:

**The $\eta \approx 46\%$ headline number requires careful interpretation.** The paper correctly decomposes this: commands contribute >60%, heartbeats ~8%, summaries <1%. Under nominal operations (no per-node commands), $\eta \approx 5\%$. The stress case ($p_{\text{cmd}} = 1.0$) represents "fleet-wide coordinated maneuver campaigns" occurring every 10 seconds—an extreme scenario. The 9× envelope ($5\%$–$46\%$) is useful for design sizing, but the paper's abstract and conclusion lead with the $46\%$ figure, which may give readers an inflated sense of overhead. The nominal $5\%$ is arguably the more operationally relevant number.

**The joint independence result (Section IV-D) is presented as a key DES contribution, but its scope is narrow.** It holds only under point-to-point ISL architectures, and the authors correctly note it would not hold under shared-medium RF. Since the RF-backup regime is precisely the scenario where the 1 kbps budget matters, the independence result may not apply in the most operationally critical scenario. This tension is acknowledged but not resolved.

**The AoI-to-position-error coupling (Eq. 14) is appropriately caveated** as "order-of-magnitude" and "illustrative back-of-the-envelope," but it occupies substantial text for what amounts to multiplying AoI by 0.5 m/s. The 230 m uncertainty figure could be misinterpreted despite the caveats. The authors should consider whether this section adds sufficient value relative to the risk of misinterpretation.

**Table IX (Coordinator Bandwidth Parameterization)** shows 100% drops at $C_{\text{coord}} = 1$ kbps, which is trivially expected since the offered load is ~20.5 kbps. The table would be more informative starting at $C_{\text{coord}} = 15$ kbps.

**The claim that "centralized compute does not diverge until $N \approx 10^6$"** is based on the $M/D/c$ model with $c = N/k_c$ parallel servers. This is a reasonable engineering statement but assumes perfect load balancing across servers, which is non-trivial at scale. The paper should note this assumption.

## 4. Clarity & Structure

**Rating: 3 (Adequate)**

The paper is comprehensive—perhaps excessively so. At approximately 15,000 words of body text (estimated from the LaTeX source), it substantially exceeds typical IEEE TAES limits. The level of detail in parameter justification, analytical cross-checks, and caveats is admirable for reproducibility but creates a dense reading experience that obscures the main contributions.

**Structural issues:**
- The "Roadmap" paragraph at the start of Section IV is helpful, but the results section itself spans 9 subsections with numerous sub-subsections, making it difficult to maintain the narrative thread.
- The paper front-loads extensive methodology (Section III spans ~40% of the paper) before reaching results. Some of this material (e.g., the full sectorized mesh derivation, neighbor discovery discussion) could be moved to appendices.
- The "Baseline Interpretation Note" (Section I-C) and "Operating regime" clarification are important but create an unusual structure where the introduction contains operational caveats before the methodology is presented.

**Positive aspects:**
- Table I (Simulation Parameters) and Table IV (Traffic Accounting) are excellent reference tables that enhance reproducibility.
- The design equations summary (Section V-C) is a valuable practitioner-oriented contribution.
- Figures are generally well-designed, though the reviewer cannot evaluate them from the LaTeX source alone.

**The abstract is overloaded** with specific numbers (21–50 kbps, 440 s, 27%, 95%, 4–7 cycles, $N \approx 10^6$) that are difficult to contextualize without reading the paper. A more focused abstract highlighting 2–3 key findings would be more effective.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an explicit acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) in the Acknowledgment section, with appropriate scoping: the AI tools "generated several architectural concepts" but "this concept is not validated in the current study." This is transparent and appropriate.

The author attribution is unusual: "Project Dyson Research Team" with a note that "Individual author names and affiliations will be provided for final publication per IEEE policy." While this may be acceptable for an AM version, IEEE requires individual author identification for peer review to assess conflicts of interest. The reviewer notes this as a procedural concern rather than an ethical violation.

The open-source data availability statement is commendable and supports reproducibility. The specific repository URL, tag, and software versions are provided.

One minor concern: the references to future AI model versions (Claude 4.6, GPT-5.2) that do not exist as of the reviewer's knowledge cutoff suggest either the paper is set in a near-future context or these are speculative attributions. This should be clarified.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE TAES in its focus on space systems coordination, though the heavy networking/queueing theory content might also fit IEEE Transactions on Networking or JSAC. The reference list (48 citations) is adequate in breadth, covering constellation operations, swarm robotics, distributed systems theory, and queueing theory.

**Referencing concerns:**
- Several references are non-archival (DARPA program pages, Amazon corporate pages, DoD fact sheets, magazine articles). While understandable for emerging programs, these weaken the scholarly foundation. At least 6 of 48 references are explicitly noted as "non-archival."
- The self-citation to [42] (companion methodology paper) is to a URL with no publication venue, raising questions about its availability and peer review status.
- Key related work is missing: the paper does not cite the substantial literature on DTN performance evaluation in LEO constellations (e.g., Fraire et al., IEEE TAES, multiple papers on contact graph routing), nor the CCSDS Spacecraft Onboard Interface Services (SOIS) standards relevant to intra-cluster communication. The Telesat Lightspeed and SDA Transport Layer programs, which implement autonomous ISL mesh networking, are not discussed.
- The Starlink operational reference [1] is an FCC filing supplemented by a non-peer-reviewed personal website. More authoritative references on Starlink's operational architecture would strengthen the motivation.

---

## Major Issues

1. **The simulation's value proposition is insufficiently demonstrated.** The DES agrees with analytical predictions to within 0.1–1.5% across all primary metrics. The joint-independence verification (Section IV-D) is the strongest candidate for DES-specific value, but it holds only under point-to-point ISL assumptions that may not apply in the RF-backup regime where the 1 kbps budget is binding. The authors should either (a) identify and present a scenario where the DES reveals behavior not predicted by the design equations, or (b) more explicitly reframe the contribution as a validated reference implementation and parametric tool rather than a simulation study that generates new findings.

2. **The RF-backup vs. optical operating regime creates a fundamental tension.** The paper's overhead analysis is conducted at 1 kbps (RF backup), but the joint-independence result assumes point-to-point optical ISLs. The most operationally critical scenario—RF-backup mode during optical link outage—would involve shared-medium RF where the independence result does not hold and MAC contention (not modeled) would dominate. The paper should either simulate the shared-medium RF scenario or more prominently caveat that its key results may not apply in the regime where they matter most.

3. **The paper substantially exceeds reasonable length for a journal article.** The extensive parameter justification, multiple analytical cross-checks, and detailed caveats—while individually valuable—collectively produce a paper that is difficult to read in a single sitting. A significant restructuring is needed: move the sectorized mesh details, sensitivity analyses, and physical-layer vignettes to appendices or supplementary material, and tighten the main text to focus on the three primary contributions (coordinator sizing, AoI characterization, correlated loss recovery).

4. **The sectorized mesh comparator needs stronger justification or should be removed.** The $\sqrt{N}$ sector sizing is acknowledged as a heuristic, the capped fanout of 10 provides minimal sector coverage, and the neighbor discovery overhead is assumed negligible without validation. As currently parameterized, it is unclear whether the sectorized mesh represents a realistic decentralized architecture or an arbitrary intermediate point. Either ground the parameterization in orbital mechanics (e.g., using actual conjunction screening volumes from ESA's CREAM database) or remove it in favor of a cleaner two-architecture comparison.

## Minor Issues

1. **Eq. (4):** The message count $M_{\text{total}}$ counts only uplink reporting; the text immediately notes this but the equation should be labeled accordingly or expanded to include bidirectional traffic.

2. **Table IX:** The $C_{\text{coord}} = 1$ kbps row (100% drops) and $C_{\text{coord}} = 100$ kbps row (identical to 50 kbps) add no information. Consider replacing with more informative capacity points (e.g., 15, 20, 22, 25, 30, 50 kbps).

3. **Section III-B (Centralized model):** The Palm-Khintchine theorem reference is to Kleinrock [26], which discusses the theorem but is not the primary source. Consider citing Palm (1943) or Khintchine (1960) directly.

4. **Table V (State Completeness):** The hierarchical row states "aggregated summaries for $O(N)$ fleet" but the summaries are aggregated at two levels (cluster → regional → ground), so each node receives only its cluster coordinator's summary, not fleet-wide summaries. Clarify the information flow.

5. **Section IV-A, Eq. (9):** The Chernoff bound is described as a "heuristic" and the authors note it bounds a fixed window, not the scan statistic. This is correct but the equation's presence may confuse readers who expect it to produce the 50 kbps threshold. Consider moving to an appendix or removing in favor of the direct DES result.

6. **The collision avoidance rate of $10^{-4}$/node/s** is described as "proximity monitoring events" with a 1000:1 screening-to-maneuver ratio. The footnote in Table I clarifies this, but the main text (Section III-A) should state this more prominently to avoid confusion with actual conjunction rates.

7. **Section III-E:** "We report $\eta = O_{\text{protocol}}$ as the primary metric because baseline telemetry is topology-invariant." This is a reasonable choice but means the reported $\eta$ excludes 20.5% of channel utilization. Some readers may find total utilization ($\eta_{\text{total}}$) more intuitive. Consider reporting both consistently.

8. **Typographical/formatting:** The acknowledgment references "Claude 4.6" and "GPT-5.2"—model versions that do not exist as of the reviewer's knowledge. If these are fictional/projected, this should be noted; if real, the paper's timeline should be clarified.

9. **Table XII (Cluster Size):** Latency values show discrete jumps (508 → 340 ms between $k_c = 75$ and $k_c = 100$) that suggest quantization artifacts from the cycle-level simulation rather than smooth physical behavior. This should be explained.

## Overall Recommendation

**Major Revision**

This paper addresses a relevant problem—sizing coordination architectures for large autonomous space swarms—and provides a well-documented, reproducible parametric tool with thorough analytical cross-checks. However, three issues prevent acceptance in its current form: (1) the simulation's added value over closed-form analysis is not convincingly demonstrated; (2) the RF-backup/optical ISL tension undermines the applicability of key results in the most operationally critical regime; and (3) the paper is substantially too long, with the core contributions buried in extensive parameter justification and sensitivity analysis. A major revision that restructures the paper around its strongest contributions (coordinator capacity sizing, AoI characterization, and the design equations summary), addresses the shared-medium RF gap, and reduces length by ~40% through appendix migration would produce a strong contribution to IEEE TAES.

## Constructive Suggestions

1. **Simulate the shared-medium RF scenario directly.** Even a simplified CSMA/CA model within a single cluster would ground the MAC efficiency parameter $\gamma$ and test whether the joint-independence result holds in the RF-backup regime. This would address the paper's most significant gap and provide genuine DES-specific value beyond analytical predictions.

2. **Restructure around a "design handbook" format.** The paper's strongest contribution is the design equations summary (Section V-C) and the parametric tool. Consider reorganizing with the design equations as the central contribution, the DES as the validation vehicle, and the detailed derivations/sensitivity analyses in appendices. This would reduce main-text length by ~40% and sharpen the narrative.

3. **Add a ground-outage simulation scenario.** The hierarchical architecture's primary advantage over centralized systems is fault tolerance during ground outages. Simulate a 15-minute ground outage at $N = 10^5$ and quantify the coordination degradation (missed screening events, AoI growth, recovery time) for both architectures. This would provide the most compelling evidence for the hierarchical approach and is straightforward to implement in the existing framework.

4. **Replace the global-state mesh upper bound with a more realistic decentralized comparator.** The $O(N^2)$ mesh is acknowledged as an intentional worst case that saturates at $N > 10^3$. Either strengthen the sectorized mesh parameterization (ground it in actual conjunction screening volumes) or adopt a well-studied decentralized protocol (e.g., contact graph routing from the DTN literature) as the comparator.

5. **Tighten the abstract to 150 words.** Focus on the three primary contributions and the design envelope ($\eta \in [5\%, 46\%]$), omitting the detailed numerical results that require context to interpret. The current abstract reads more like an executive summary than a concise problem-method-result statement.