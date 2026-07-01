---
paper: "02-swarm-coordination-scaling"
version: "h"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-23"
recommendation: "Reject"
---



# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

**Manuscript Version:** H
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuinely important gap: the systematic characterization of coordination architectures for autonomous space swarms in the $10^4$–$10^6$ node regime, which is indeed underexplored in the literature. The motivation is timely given Starlink's growth trajectory and approved mega-constellation expansions. The framing of the problem across three orders of magnitude, with explicit reference baselines bounding the design space, is a sensible contribution to the architectural trade-space literature.

However, the novelty is diminished by several factors. The core finding—that a fixed-depth hierarchical tree achieves $O(N)$ message complexity—is an elementary consequence of the architecture's definition and is well-established in the distributed systems literature (as the authors themselves acknowledge, citing Lynch [7]). The more interesting empirical finding—the slope change near $N^* \approx 45{,}000$—is potentially novel, but its significance is undermined by the fact that the actual DES overhead values are missing from Table VI (all entries show "---"). Without these numbers, the slope-change analysis cannot be independently verified. The paper reads as a framework description with placeholder results rather than a completed empirical study. The exception-based telemetry validation (Table VII) similarly contains no actual data. The coordinator bandwidth stress test (Table VIII) is likewise empty. This is a fundamental problem: the paper's principal claimed contributions are DES-measured results, but the DES measurements are not presented.

The comparison against intentionally weak baselines (single-server centralized, global-state mesh) limits the practical significance. While the authors are commendably transparent about this (Section I-C), the absence of a realistic decentralized comparator (e.g., the sectorized mesh discussed in Section V-C) means the paper cannot make strong claims about the relative merit of hierarchical coordination versus practical alternatives.

---

## 2. Methodological Soundness

**Rating: 2 (Needs Improvement)**

The DES framework is described at a reasonable level of detail, and the event types, node model, and Monte Carlo configuration are clearly specified. The validation against Pollaczek–Khinchine for $M/D/1$ at low utilization and against gossip bounds for small $N$ is appropriate, though limited. The formal model comparison using AIC for the slope-change analysis is methodologically sound in principle.

**Critical methodological concern: Missing data.** Tables VI, VII, and VIII—which are supposed to contain the paper's primary empirical results—are populated entirely with "---" placeholders. The footnotes state these "will be populated when the updated simulation is run on the full parameter sweep." This is not acceptable for a journal submission. The paper's abstract, contributions list, and conclusions all make specific quantitative claims (e.g., "reduction factors within 15% of analytical predictions," "slope-change breakpoint at $N^* \approx 45{,}000$") that cannot be verified against the presented data. Either the simulation has been run and the results should be included, or it has not been run and the claims should not be made.

**Bernoulli link model.** The link availability analysis (Section IV-F) models link losses as i.i.d. Bernoulli trials, which is a significant simplification for LEO systems where Earth occlusion produces deterministic, correlated outage patterns. The authors acknowledge this (Section V-D, item 7) but the gap between the model and physical reality is large enough to question whether the retransmission analysis provides actionable guidance. Correlated outages could simultaneously affect all links from a cluster coordinator to its regional coordinator, a scenario the Bernoulli model cannot capture.

**Coordinator bandwidth pooling.** The assumption that coordinators can pool the aggregate bandwidth of their cluster members ($k_c \times 1$ kbps) is physically questionable. While the authors now parameterize this (Section III-F-1, Table VIII), the stress test results are missing. The claim that $\beta_{\min} \approx 0.25$ (25 kbps minimum) appears in the conclusions but is not supported by presented data.

**Exception-based telemetry model.** Modeling exception events as a Bernoulli process with fixed $p_{\text{exc}}$ is a significant simplification. In reality, exception probability depends on orbital dynamics, maneuver scheduling, and space weather—factors that introduce temporal correlation and spatial clustering of exceptions. The validation claim ("within 15% of analytical predictions") is circular when the analytical prediction is simply $p_{\text{exc}}$ and the DES implements a Bernoulli draw with the same parameter.

---

## 3. Validity & Logic

**Rating: 2 (Needs Improvement)**

The logical structure of the argument is generally sound: establish baselines, characterize hierarchical scaling, identify optimization opportunities. The authors are commendably honest about the limitations of their baselines and the distinction between DES-validated and analytically-projected results. The correction note regarding Versions A–G (Section IV-D) demonstrates intellectual honesty.

However, several validity concerns arise:

**Empty results tables invalidate conclusions.** The abstract states "DES-measured overhead that scales linearly with $N$" and "slope-change analysis using AIC-based model comparison identifies a gradual increase... near $N^* \approx 45{,}000$." These claims require the data in Table VI, which is absent. The conclusion states "$\beta_{\min} \approx 0.25$" based on Table VIII, which is also empty. Claims in the abstract and conclusions that are not supported by presented data represent a serious validity concern.

**Circular validation of exception-based telemetry.** If the DES implements exceptions as Bernoulli($p_{\text{exc}}$) draws, then the expected message reduction is exactly $p_{\text{exc}}$ by construction. Validating that the DES produces reduction factors "within 15% of $p_{\text{exc}}$" does not validate the exception-based telemetry concept—it validates that the random number generator works. A meaningful validation would require modeling the physical process that generates exceptions (orbital prediction errors, perturbation magnitudes) and measuring the resulting exception rate.

**Global-state mesh $O(N^2)$ derivation.** The argument in Section III-B-3 that full-fleet trajectory awareness is required for collision avoidance is debatable. In practice, conjunction screening uses spatial filtering (e.g., the "conjunction screening volume" the authors themselves mention in Section V-C) to reduce the pairwise comparison space from $O(N^2)$ to $O(N \cdot k_{\text{local}})$. The $O(N^2)$ characterization is therefore an upper bound on an upper bound, which weakens its utility as a reference baseline.

**Queueing model mismatch.** The centralized baseline uses $M/D/1$ (Poisson arrivals, deterministic service), but the hierarchical topology's cluster coordinator also receives Poisson-like arrivals from $k_c$ nodes reporting at rate $r$. The paper assigns $M/D/1$ to the cluster coordinator as well, but the arrival process from $k_c$ independent Poisson sources is itself Poisson only in the limit—for $k_c = 100$ with $r = 0.1$, the superposition is well-approximated as Poisson, but this should be stated explicitly.

---

## 4. Clarity & Structure

**Rating: 3 (Adequate)**

The paper is well-organized with a logical flow from introduction through framework, results, discussion, and conclusion. The use of explicit research questions (RQ1–RQ3) provides structure, and the baseline interpretation note (Section I-C) is a valuable addition that manages reader expectations. The traffic accounting table (Table IV) and metric definitions (Section III-G) demonstrate attention to precision.

However, the paper is excessively long for its actual empirical content. At approximately 12,000 words with 8 figures and 9 tables, it would be a substantial journal paper even if all results were present. With three key tables empty, the paper contains extensive methodological description for results that are not shown. The repeated caveats about "Version H corrections" and "Versions A–G" create a revision-history narrative that is appropriate for reviewer communication but should be removed from a journal submission.

The abstract is problematic: it makes specific quantitative claims ("within 15% of analytical predictions," "$N^* \approx 45{,}000$," "$p_{\text{link}} \geq 0.5$") that are either unsupported by presented data or derived from analytical calculations rather than DES measurements. The abstract should accurately reflect what is demonstrated versus what is projected.

Several passages are unnecessarily defensive or repetitive. For example, the explanation that the U-shape in cluster size optimization is driven by communication topology effects rather than processing saturation appears three times (Sections III-B-2, IV-B, and the caption discussion). The paper would benefit from consolidation.

---

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2), clearly stating that the AI tools were used for "exploratory ideation" rather than analysis or writing, and that the concepts generated are "not validated in the current study." This level of transparency exceeds current norms and is commendable.

The data availability statement provides a repository URL, though the commit hash is listed as "[PENDING]," which should be resolved before publication. The author attribution uses a team name with a note that individual names will be provided per IEEE policy—this is acceptable for review but must be resolved for publication.

One concern: the acknowledgment references "Claude 4.6," "Gemini 3 Pro," and "GPT-5.2" with an "accessed February 2026" date, and several references cite access dates in 2026. If this paper is being submitted in 2024–2025, these forward-dated references raise questions about the manuscript's provenance and timeline. This should be clarified.

---

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in scope, addressing space systems coordination with simulation methodology. The reference list is comprehensive (46 references) and covers the relevant literature in constellation management, swarm robotics, distributed systems theory, and queueing theory. Key foundational works (Lamport, Olfati-Saber & Murray, Ren & Beard, Demers et al.) are appropriately cited.

However, several important gaps exist. The paper does not cite recent work on distributed space situational awareness (SSA) architectures, which directly address the conjunction screening problem that motivates the global-state mesh baseline. Work by Frueh, Jah, and others on distributed orbit determination and catalog maintenance is relevant. The IETF work on Information-Centric Networking (ICN) and Named Data Networking (NDN), which has been proposed for space networks, is not discussed despite its relevance to the gossip-based state dissemination model. Recent work on software-defined networking (SDN) for satellite constellations (e.g., by Papa et al., 2020) addresses hierarchical control planes that are directly comparable to the architecture studied here.

Several references are non-archival (SpaceX website, Amazon website, DARPA program pages, DoD fact sheets) and may not be accessible long-term. While some of these are unavoidable for current operational systems, the paper should minimize reliance on non-archival sources where peer-reviewed alternatives exist.

---

## Major Issues

1. **Tables VI, VII, and VIII contain no data.** This is the single most critical flaw. The paper's principal contributions—DES-measured overhead scaling, exception-based telemetry validation, and coordinator bandwidth parameterization—are claimed in the abstract and conclusions but the supporting data tables are empty. The paper cannot be evaluated as an empirical contribution without these results. **Action required:** Populate all tables with actual simulation results, or remove claims that depend on unpresented data.

2. **Circular validation of exception-based telemetry.** The DES implements exceptions as Bernoulli($p_{\text{exc}}$) draws, then "validates" that the measured reduction matches $p_{\text{exc}}$. This tests the simulator's random number generation, not the physical validity of exception-based telemetry. **Action required:** Either (a) implement a physics-based exception model (e.g., based on orbital prediction error distributions) and measure the resulting exception rate, or (b) reframe the contribution as "DES confirmation that the hierarchical architecture correctly propagates telemetry reduction through the aggregation hierarchy" rather than "validation of exception-based telemetry."

3. **Absence of a realistic decentralized comparator.** The global-state mesh is acknowledged as an intentional upper bound, and the sectorized mesh is identified as future work. Without at least one realistic decentralized architecture for comparison, the paper cannot support claims about the relative merit of hierarchical coordination. **Action required:** Either implement the sectorized mesh variant described in Section V-C, or substantially temper all comparative claims to acknowledge that the hierarchical architecture is compared only against intentional bounds, not against practical alternatives.

4. **Bernoulli link model inadequacy for LEO systems.** Earth occlusion produces deterministic, periodic, correlated link outages that fundamentally differ from i.i.d. Bernoulli losses. The retransmission analysis (Section IV-F) may be qualitatively misleading because correlated outages can simultaneously disable all links from a coordinator to its parent, a failure mode that retransmission cannot address. **Action required:** At minimum, add a deterministic occlusion model for a representative orbital geometry and compare results with the Bernoulli model. If this is infeasible, add explicit caveats that the retransmission results apply only to random (non-correlated) link losses.

---

## Minor Issues

1. **Section III-B-3, Eq. 5:** The derivation of fanout $f = O(N/\log N)$ from the global convergence requirement is stated but not proven. The claim "each round must cover $N/(\log N)$ new entries per node" needs more rigorous justification—this assumes uniform dissemination progress across rounds, which gossip protocols do not guarantee.

2. **Table II ($M/D/c$ sensitivity):** The $c = 1000$ row ($N_{\max} = 10^7$) exceeds the simulated range and is speculative. Consider removing or marking as extrapolation.

3. **Section III-E:** The collision avoidance rate of $10^{-4}$/node/s is justified by a "1,000:1 ratio of screening events to actual maneuvers," but this ratio is stated without a supporting reference. The ESA reference [46] reports maneuver rates, not screening rates.

4. **Eq. 8 (power overhead):** $\Delta P_{\text{avg}} = 15\text{ W}/100 = 0.15\text{ W}$ assumes uniform coordinator rotation. If some nodes fail and are removed from the rotation pool, the duty fraction increases for surviving nodes. This second-order effect should be noted.

5. **Section IV-D, "Correction from prior versions":** This revision-history narrative is appropriate for reviewer communication but should be removed or condensed to a single sentence for the published version.

6. **Data Availability:** The commit hash is "[PENDING]." This must be resolved before publication.

7. **Acknowledgment section:** References to "Claude 4.6," "Gemini 3 Pro," and "GPT-5.2" with 2026 access dates need clarification regarding the manuscript timeline.

8. **Table I (Simulation Parameters):** The "Clock resolution" row lists "1 s / 10 s" for collision/routine events, but the text states $T_c = 10$ s. Clarify that the 1-s resolution applies only to collision avoidance event scheduling, not to the coordination cycle.

9. **Fig. 1 (architecture diagram):** Referenced but presumably not included in the LaTeX source. Ensure the figure clearly shows message flow directions and aggregation ratios as described in the caption.

10. **Section II-D:** The SWIM protocol reference [40] is introduced but never connected to the simulation framework. Either integrate it into the hierarchical failure detection model or remove the reference.

---

## Overall Recommendation

**Reject (with encouragement to resubmit)**

This manuscript presents a well-motivated research framework for an important problem, and the authors demonstrate commendable transparency about limitations and prior-version corrections. However, the paper cannot be accepted in its current form because its principal empirical contributions—the DES-measured overhead scaling data, exception-based telemetry validation, and coordinator bandwidth parameterization—are claimed in the abstract and conclusions but the supporting data tables (VI, VII, VIII) are entirely empty. A journal paper in IEEE T-AES must present the data that supports its claims. Additionally, the circular nature of the exception-based telemetry "validation," the absence of a realistic decentralized comparator, and the inadequacy of the Bernoulli link model for LEO systems represent methodological concerns that require substantive revision. The framework itself is sound and the research questions are well-posed; with completed simulations, populated tables, and a more realistic decentralized baseline, this could become a solid contribution.

---

## Constructive Suggestions

1. **Complete the simulation and populate all tables before resubmission.** This is non-negotiable. Tables VI, VII, and VIII must contain actual DES measurements. If computational constraints prevent running the full parameter sweep, reduce the scope (e.g., fewer Monte Carlo runs, fewer intermediate scales) rather than submitting with placeholder data.

2. **Implement the sectorized mesh variant** described in Section V-C, even in simplified form. This would transform the paper from a comparison against intentional bounds into a genuine architectural trade study. A sectorized mesh with $k_{\text{sector}} = 100$ nodes and inter-sector summary exchange would be directly comparable to the hierarchical architecture and would substantially strengthen the paper's contributions.

3. **Replace the Bernoulli exception model with a physics-informed model.** Use published orbital prediction error distributions (e.g., from Vallado & Cefola, or the ESA conjunction assessment literature) to derive exception probabilities as a function of prediction horizon and perturbation environment. This would make the exception-based telemetry validation genuinely informative rather than tautological.

4. **Add a deterministic Earth occlusion model** for at least one representative orbital geometry (e.g., 550 km circular, 53° inclination—Starlink's shell 1). Compare the coordination success results under deterministic occlusion with the Bernoulli model to assess whether correlated outages alter the topology ranking.

5. **Condense the paper by 25–30%.** Remove revision-history narratives, consolidate repeated explanations (e.g., the U-shape mechanism), and tighten the related work section. The paper's length is disproportionate to its current empirical content. A focused 8,000-word paper with complete results would be more impactful than a 12,000-word paper with placeholder tables.