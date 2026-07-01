---
paper: "02-swarm-coordination-scaling"
version: "m"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-24"
recommendation: "Major Revision"
---



# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuinely important gap: the coordination scaling regime between current constellation management (~10⁴ nodes) and aspirational mega-swarm concepts (~10⁶ nodes). The motivation is timely given Starlink's expansion trajectory and emerging mega-constellation programs. The identification of favorable cluster sizes, duty cycles, coordinator bandwidth thresholds, and the exception-based telemetry bandwidth reduction are practically useful design parameters.

However, the novelty is substantially limited by the nature of the central result. The authors commendably acknowledge (Section IV-D) that the O(1) overhead scaling "is a direct mathematical consequence of the hierarchical message structure—not a surprising emergent property." When the total message volume is O(N) by construction and the available bandwidth is O(N) by definition, the ratio is trivially O(1). The DES contribution is then reduced to (1) quantifying the protocol coefficient at η = 20.66%, and (2) confirming no queueing-induced nonlinearities emerge. But finding (2) is weak because the simulation abstracts away precisely the physical-layer phenomena (MAC contention, correlated outages, priority queueing) most likely to introduce such nonlinearities—a circularity the authors acknowledge in Section V-E but which fundamentally undermines the claim's value. The coefficient quantification (finding 1) is useful but incremental; one could compute it analytically from the message sizes in Table III with a back-of-envelope calculation.

The absence of a realistic decentralized comparator is a significant gap. The two reference baselines are intentionally extreme (single-server centralized, global-state mesh), and the authors repeatedly note this. While the analytical discussion of sectorized mesh (Section V-C) is thoughtful, the paper's comparative claims rest on bounds that no practitioner would implement. The paper would be substantially more impactful if even a simplified sectorized mesh were simulated.

## 2. Methodological Soundness

**Rating: 2 (Needs Improvement)**

The DES framework is clearly described and the parameter space is well-documented (Tables III–V). The Monte Carlo framework with 30 replications and bootstrap confidence intervals is appropriate in principle. The validation against M/D/1 analytical solutions (Section III-A) and the Poisson arrival verification (CV = 0.98 ± 0.03) are good practices.

However, several methodological concerns are significant:

**Near-tautological simulation.** The extremely low variance (SD < 0.001%) across 30 MC replications reveals that the simulation is essentially deterministic for the primary metric. The only stochastic component is the 2%/year failure process, which affects a negligible fraction of nodes per cycle. The authors acknowledge this ("the MC framework serves primarily to confirm this low-variance property"), but this raises the question of what the DES adds beyond an analytical calculation. The message model is so stylized—fixed sizes, fixed rates, perfect links (in the primary results), no MAC contention—that the overhead ratio could be computed in closed form from Table III parameters. The 30-replication MC framework, while methodologically correct, is solving a problem that doesn't exist: there is no meaningful stochastic uncertainty to characterize.

**Abstraction level concerns.** The message-passing abstraction (Table IV) excludes MAC scheduling, link acquisition, pointing constraints, half-duplex turnaround, Doppler effects, priority queueing, correlated failures, and store-and-forward networking. These are not minor details for space communication systems—they are the dominant engineering challenges. The paper's central claim about "no queueing-induced nonlinearities" is unfalsifiable within this abstraction because the mechanisms that would produce such nonlinearities are not modeled. The MAC efficiency factor γ ≈ 0.85 applied post-hoc to the coordinator bandwidth analysis (Eq. 8) is a rough correction that does not capture the scale-dependent nature of MAC contention.

**Bernoulli link model.** The i.i.d. Bernoulli link loss model (Section IV-F) is a poor approximation for LEO inter-satellite links, where outages are dominated by deterministic Earth occlusion geometry producing correlated, periodic link failures. The authors acknowledge this (Section V-E, item 7 in unresolved questions) but the gap is significant because correlated outages could simultaneously affect multiple nodes in a cluster, potentially causing coordinator isolation—a failure mode the Bernoulli model cannot capture.

**Collision avoidance rate.** The 10⁻⁴/node/s rate is justified as representing screening events rather than maneuvers, with a claimed 1,000:1 screening-to-maneuver ratio. While the sensitivity analysis (varying from 10⁻⁵ to 10⁻³) is appreciated, the rate is not derived from any conjunction assessment model and the 1,000:1 ratio is stated without citation. For a paper targeting IEEE T-AES, this parameter should be better grounded.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The authors demonstrate commendable intellectual honesty throughout. The repeated caveats about baseline interpretation (Section I-C), the circularity acknowledgment in Section V-E, the explicit distinction between DES-measured and analytically projected results, and the careful separation of "delivered" vs. "offered" overhead in Table IX are all examples of transparent reporting that strengthens credibility.

The internal consistency of results is good. The overhead values in Tables VI and VII are consistent (η ≈ 20.66% for k_c = 100 in both). The exception-based telemetry validation (Table VIII) correctly confirms the Bernoulli expectation, and the authors appropriately note this is expected by the law of large numbers rather than a surprising finding. The coordinator bandwidth stress test (Table X) provides genuinely useful engineering data.

However, several logical issues deserve attention. First, the claim that hierarchical coordination "scales" to 10⁵ nodes is technically correct but potentially misleading. What scales is the message-passing overhead ratio under idealized conditions. Whether the *coordination quality*—the ability to actually coordinate collision avoidance, orbit maintenance, and task allocation—scales is not addressed. The paper measures bandwidth consumption, not coordination effectiveness. Second, the duty cycle analysis (Table VII) presents results without sufficient explanation of the underlying model. The inverse relationship between duty cycle and handoff success rate is asserted but the reliability model generating these numbers is not specified. Why does a 1-hour cycle have 95% handoff success while a 48-hour cycle has 99.8%? The explanation about cumulative daily failure probability is qualitative; the quantitative model should be stated. Third, the extrapolation to 10⁶ nodes in Fig. 2 is appropriately flagged as analytical, but its inclusion in a figure alongside DES-validated results risks misinterpretation despite the caption note.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized and clearly written. The progressive disclosure of information—from research questions (Section I-B) through framework description (Section III) to results (Section IV) and discussion (Section V)—follows a logical arc. The extensive use of tables (11 tables) provides good reference material, and the explicit traffic accounting (Table V) and abstraction scope (Table IV) are particularly valuable for reproducibility.

The writing quality is generally high, with precise technical language and appropriate use of mathematical notation. The "Baseline Interpretation Note" (Section I-C) is an excellent structural choice that preempts misinterpretation. The metric definitions (Section III-F) are thorough and well-placed.

Some areas could be improved. The paper is quite long for a journal article (approximately 12,000 words of body text plus extensive tables), and some material is repetitive. The constant overhead result (η = 20.66%) is stated at least eight times across the abstract, introduction, results, and conclusion. The discussion of why this is analytically expected appears in both Section IV-D and the abstract. Some consolidation would improve readability. The figures are referenced but not provided (as expected for a LaTeX source review); the captions are descriptive and appropriate. The bandwidth breakdown table (Table II) has a useful footnote system but the relationship between the analytical per-node estimate (~9% overhead) and the DES fleet-level measurement (~21% overhead) could be explained more clearly in the table itself rather than requiring the reader to parse footnote b.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate acknowledgment of AI-assisted ideation (Acknowledgment section), specifying the models used (Claude 4.6, Gemini 3 Pro, GPT-5.2) and the scope of their contribution (architectural concept generation, not validated in the current study). This is transparent and follows emerging best practices for AI disclosure. The reference to a companion methodology paper [dyson_multimodel] provides additional context.

The data availability statement is commendable, with a specific GitHub repository URL and commitment to releasing source code and datasets. The commit hash placeholder ([PENDING]) should be filled before publication. The anonymous authorship ("Project Dyson Research Team") with a note about final publication is acceptable for review but must be resolved per IEEE policy.

One minor concern: the paper references future model versions (Claude 4.6, GPT-5.2) that do not exist as of the review date, suggesting either the paper is set in a near-future context or these are placeholder names. This should be clarified to avoid confusion about the actual tools used.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in its focus on autonomous spacecraft coordination, though the contribution leans more toward communication systems engineering than traditional aerospace content. The connection to mega-constellation operations (Starlink, Kuiper) grounds the work in current relevance.

The reference list (47 citations) covers the major relevant areas: distributed systems theory (Lynch, Lamport, Ongaro), swarm robotics (Brambilla, Dorigo, Reynolds), constellation management (Handley, del Portillo), queueing theory (Kleinrock), and space standards (CCSDS). However, several gaps exist:

- No citation of the substantial literature on satellite constellation autonomous operations, particularly work by Bonnet, Bussy-Virat et al. on distributed satellite systems coordination.
- The mean-field game references (Lasry & Lions, Huang et al.) are mentioned but not connected to the methodology; they appear as name-drops rather than substantive engagement.
- Missing references to recent work on LEO mega-constellation collision avoidance coordination (e.g., Virgili et al., Lewis et al. on conjunction assessment scaling).
- The GNN-based controller references (Tolstaya, Li) are cited but their relevance to the message-passing abstraction used here is not explained.
- Several references are non-archival web pages (SpaceX, Amazon, DARPA, DoD) that may not persist. While unavoidable for some sources, the paper should minimize reliance on these for substantive claims.

The related work section (Section II) is comprehensive but somewhat encyclopedic—it catalogs prior work without clearly articulating how each body of literature informs or contrasts with the present study's specific methodological choices.

---

## Major Issues

1. **The central result is near-tautological within the chosen abstraction.** The O(1) overhead scaling is a mathematical identity (O(N)/O(N) = O(1)) given the hierarchical message model, and the DES confirms this identity under conditions that exclude the physical-layer phenomena most likely to perturb it. The paper needs either (a) a substantially richer physical-layer model (at minimum, TDMA slot scheduling within T_c) to make the "no nonlinearities" claim meaningful, or (b) a reframing that positions the contribution as protocol coefficient quantification and parameter space exploration rather than scaling validation.

2. **Absence of a realistic decentralized comparator.** The global-state mesh is acknowledged as an intentional upper bound, but without a sectorized mesh simulation, the paper cannot make meaningful comparative claims about hierarchical vs. decentralized architectures. The analytical discussion in Section V-C is helpful but insufficient for a simulation paper. At minimum, a simplified sectorized mesh DES (even with the same message-passing abstraction) should be implemented to demonstrate the overhead gap quantitatively.

3. **Coordination quality is not measured.** The paper measures bandwidth consumption but not coordination effectiveness. Exception-based telemetry reduces overhead from 21% to 2.5%, but the impact on collision avoidance timeliness, state estimation accuracy, and maneuver coordination quality is entirely unaddressed. For a paper targeting aerospace systems engineers, this is a critical gap. The acknowledgment that "coordination quality impact [is] deferred" (abstract) does not resolve the concern—it means the most practically important question is unanswered.

4. **The Bernoulli link model is inadequate for LEO ISL.** Earth occlusion produces deterministic, correlated, periodic outages that can simultaneously affect multiple cluster members. The i.i.d. assumption fundamentally mischaracterizes the link environment. A geometric occlusion model (even simplified) is necessary to validate the link availability results.

5. **Duty cycle analysis lacks a formal reliability model.** Table VII presents specific numerical values (e.g., 95.0% handoff success at 1h, 99.8% at 48h) without specifying the mathematical model that generates them. The qualitative explanation about cumulative failure probability is insufficient; the reader cannot reproduce these results.

## Minor Issues

1. **Section III-A:** "one-second resolution applies only to collision avoidance events"—the interaction between 1-second and 10-second event resolutions in the priority queue should be described more precisely. Are collision avoidance events preemptive?

2. **Eq. (4):** The hierarchical message count $M_{\text{total}} = N + N/k_c + N/(k_c \cdot k_r)$ counts only uplink messages. The text notes bidirectional overhead is "approximately 1.5–2×" but this factor is not used consistently in subsequent calculations.

3. **Table VI:** The latency values show discrete jumps (508→340 ms between k_c = 75 and k_c = 100) rather than smooth variation. This suggests quantization effects in the simulation that should be explained—are these artifacts of the 10-second cycle discretization or the regional coordinator queue model?

4. **Section IV-D, "Full-Participation Simulation Note":** This subsection could be merged with the earlier description in Section III-D to avoid redundancy.

5. **Table IX:** The "Offered" column formula in the footnote ($\eta_{\text{delivered}} \times (1 + (1-p)(1 + (1-p)))$) should be simplified and verified. For M_r = 2, the expected number of attempts per message is $1 + (1-p) + (1-p)^2$, so offered = delivered × $(1 + (1-p) + (1-p)^2) / p_{\text{success}}$. The current formula appears to be an approximation.

6. **Abstract:** At 350+ words, the abstract exceeds typical IEEE T-AES guidelines (~200 words). Consider condensing.

7. **Section I-A:** "approximately 7,000 active satellites (as of mid-2024)"—the paper's access dates suggest 2026; this figure should be updated or the temporal reference clarified.

8. **Eq. (6):** The convergence time $T_{\text{converge}} = D \cdot \tau_{\text{gossip}}$ is stated for a random geometric graph with $D = O(N^{1/3})$, but LEO constellations are distributed on a thin spherical shell (2D surface), where $D = O(N^{1/2})$ for a random geometric graph. The dimensionality assumption should be justified.

9. **Section III-E:** The collision avoidance rate sensitivity analysis ("overhead increases by approximately 1.5 percentage points" at 10⁻³) should be presented in a table or figure rather than inline text.

10. **References:** [s2geometry] is cited in the bibliography but I cannot find where it is referenced in the text.

---

## Overall Recommendation

**Major Revision**

The paper addresses a relevant problem and demonstrates careful, transparent engineering analysis with commendable intellectual honesty about limitations. However, the central contribution—confirming an analytically predictable O(1) scaling ratio within a message-passing abstraction that excludes the phenomena most likely to perturb it—is insufficient for a top-tier journal in its current form. The absence of a realistic decentralized comparator, the lack of coordination quality metrics, and the inadequacy of the Bernoulli link model for LEO environments are significant gaps. The paper reads more as a well-executed parameter study of a hierarchical message model than as a validation of coordination scaling for real space systems. A major revision incorporating at minimum a TDMA scheduling layer, a sectorized mesh comparator, and a geometric link outage model would substantially strengthen the contribution and bring it to the level expected by IEEE T-AES.

---

## Constructive Suggestions

1. **Add a minimal TDMA scheduling model within T_c.** Implement k_c time slots with realistic guard intervals (e.g., 1–5 ms) within each 10-second coordination cycle. This would allow the DES to detect whether slot contention introduces scale-dependent overhead—directly addressing the circularity concern and substantially strengthening the "no nonlinearities" claim. This is the single highest-impact addition possible.

2. **Implement a simplified sectorized mesh DES.** Even using the same message-passing abstraction, a sectorized mesh with locality-limited gossip (k_neighbors = O(√N)) would provide a realistic decentralized comparator. The analytical framework in Section V-C already defines the model; implementing it in the existing DES framework should be tractable and would transform the comparative analysis from "hierarchical vs. intentional bounds" to "hierarchical vs. practical alternative."

3. **Replace the Bernoulli link model with a geometric occlusion model.** For LEO at ~550 km altitude, Earth occlusion geometry is well-characterized. A simplified model where links between nodes separated by more than ~120° (Earth limb angle) are deterministically blocked, with orbital motion producing periodic outages, would capture the correlated nature of LEO link failures and test whether the topology ranking holds under realistic intermittency patterns.

4. **Add a coordination quality metric.** Define a metric such as "state estimation staleness" (time since last update from each cluster member) or "conjunction detection latency" (time from conjunction geometry onset to coordinator awareness). Even without coupling to a full orbital mechanics simulator, tracking how exception-based telemetry and link losses affect state freshness at the coordinator would provide a first-order coordination quality assessment.

5. **Reframe the contribution around the parameter study.** The paper's strongest content is the coordinator bandwidth stress test (Table X), the exception-based telemetry validation (Table VIII), the link availability analysis with retransmission (Table IX), and the duty cycle trade-off characterization (Table VII). Reframing the paper as "Engineering Design Parameters for Hierarchical Space Swarm Coordination" rather than "Characterizing Scaling" would better match the actual contribution and reduce the burden of proving scaling claims that the abstraction level cannot fully support.