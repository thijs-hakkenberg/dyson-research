---
paper: "02-swarm-coordination-scaling"
version: "s"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-24"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 4 (Good)**

The manuscript tackles a timely and practically relevant question: how coordination architectures scale for very large autonomous space swarms under a fixed per-node coordination budget. The explicit comparison across (i) a centralized single-server bound, (ii) a global-state mesh upper bound, (iii) a sectorized mesh intermediate comparator, and (iv) the hierarchical architecture is a useful framing. The paper’s emphasis on *byte-level traffic accounting* under a per-node coordination budget is also valuable, because many “scalability” discussions in swarm/constellation literature remain at message-complexity or qualitative levels.

The most novel element, in my view, is the introduction of **AoI as a coordination-quality metric** for hierarchical coordination with exception-based telemetry (Section IV-F / Section “Coordination Quality: Age of Information”). This is a meaningful step beyond pure overhead scaling, and it correctly highlights that bandwidth savings trade against state freshness. The **coordinator bandwidth stress test** and explicit separation between “offered load” and “delivered load” are also practically useful.

That said, some novelty claims are slightly overstated. The DES largely confirms what the closed-form accounting already implies (the authors acknowledge this in Section IV-C and IV-C-2), and several “engineering thresholds” (e.g., 50 kbps unscheduled vs 24 kbps TDMA) are tightly coupled to the authors’ simplified intra-cycle arrival model and the chosen message model. The work is still a good contribution, but it would be stronger if positioned more explicitly as a *message-layer offered-load characterization* with clearly bounded applicability, rather than implying near-hardware-ready design parameters.

---

## 2. Methodological Soundness — **Rating: 3 (Adequate)**

The simulation framework is clearly described as **cycle-aggregated DES at the message-passing layer** (Section III-A, Tables VIII–X). The paper is commendably explicit about what is modeled vs abstracted (Table X), and it provides a consistent traffic accounting definition for the overhead metric (Table XII). The Monte Carlo setup (30 replications, bootstrap CIs) is described, and the authors are transparent that stochastic variance is near-zero because the workload is near-deterministic.

However, the method has several soundness concerns that should be addressed to meet IEEE T-AES expectations for rigor:

1) **Queueing/arrival modeling inconsistencies and burstiness artifacts.** The coordinator bandwidth stress test (Section IV-H) uses a per-cycle byte budget with random-phase arrivals and tail-drop when exceeding \(C_{\text{coord}} T_c\). This creates the “50 kbps unscheduled” threshold, which is then contrasted with a TDMA analytical threshold. But the DES does not actually simulate a MAC, and the burstiness is induced by the model choice (uniform random phase + per-cycle byte cap). If the coordinator link is a continuous-time server with rate \(C_{\text{coord}}\), many of these drops would instead manifest as queueing delay, not loss, unless a finite buffer/deadline is enforced. You need to clarify whether the coordinator constraint is a *hard per-cycle deadline* (must ingest all reports within \(T_c\)) or a *long-term rate constraint* with buffering.

2) **Global-state mesh and sectorized mesh are not comparable at the same functional requirement.** The global-state mesh is explicitly an upper bound requiring full fleet state replication (Section III-C-3), whereas sectorized mesh and hierarchical assume locality/aggregation. This is acceptable as bracketing, but then the paper sometimes reads as if “mesh is infeasible” generally, rather than “global-state replication is infeasible under 1 kbps/node.” The sectorized mesh includes a “sector coordinator” (Section V-C), which makes it closer to hierarchical than a true peer-to-peer alternative; the workload definition (heartbeats capped at 10) is also somewhat arbitrary and not tied to a conjunction-screening fidelity requirement.

3) **Statistical framing.** Using 30 replications and bootstrap CIs is fine, but the manuscript repeatedly reports extremely small SDs and uses this as a correctness check. That is not a substitute for validation against external benchmarks. Since the DES is essentially deterministic accounting plus a few stochastic processes, you should either (i) reduce Monte Carlo emphasis and present results as deterministic offered-load calculations with sensitivity bands, or (ii) introduce stochasticity that actually matters (time-varying link schedules, correlated outages, bursty event arrivals, priority queuing).

Reproducibility is promising (code repository promised, though commit hash is pending). For T-AES, you should provide a fixed archival tag/DOI or at least a concrete commit hash at submission, and ideally include a minimal configuration file in an appendix/supplement.

---

## 3. Validity & Logic — **Rating: 3 (Adequate)**

Many conclusions are logically consistent with the defined model. In particular, the statement that \(O(1)\) overhead ratio is an analytical consequence of \(O(N)\) messaging under \(O(N)\) total fleet bandwidth is correct and appropriately acknowledged (Section IV-C). The AoI results under Bernoulli exception reporting are also consistent with geometric inter-report times, and the paper correctly interprets heavy tails (Table XVI, Fig. 9).

The main validity risk is **over-interpreting message-layer offered-load results as engineering “thresholds.”** For example, the coordinator capacity bounds (50 kbps unscheduled / 24 kbps TDMA) depend on: (i) the definition of “zero-drop” as a per-cycle cap rather than queue stability, (ii) lack of explicit MAC/PHY overhead beyond a scalar \(\gamma\), (iii) ignoring half-duplex turnaround, acquisition, and pointing, and (iv) assuming coordinator egress is unconstrained (optical ISL separate plane). These may be fine as a first-order offered-load study, but the paper should tighten the language: these are *model-conditional* thresholds, not general coordinator sizing rules.

There are also internal consistency issues that should be corrected. One example: the text states for the global-state mesh at \(N=100{,}000\) that gossip consumes “over 25% of available bandwidth” and “leaving insufficient capacity” (Section IV-A), but Table VI’s accounting indicates tens of MB/node/cycle, i.e., **orders of magnitude beyond** a 1 kbps/node budget. That discrepancy suggests either a mistaken sentence or an inconsistent normalization (per-node vs fleet). Similar potential confusion appears in Table XI vs the later statement that hierarchical total utilization is ~41% (baseline + overhead): the table’s “per-node breakdown” is labeled as an analytical estimate but does not align with the later “dominant term is one 512 B command per node per cycle” stress-case.

Limitations are discussed candidly (Section V-E), which is a strength. Still, several key claims (e.g., “queue stability confirmation across \(10^3\)–\(10^5\)”) are true only because the DES enforces a particular service model and does not include several mechanisms that would create instability (MAC contention, correlated outages, deadline misses). Those conclusions should be re-scoped to “within the message-layer abstraction and the imposed service constraints.”

---

## 4. Clarity & Structure — **Rating: 4 (Good)**

The manuscript is generally well organized, with clear separation between assumptions, models, metrics, and results. The “Baseline Interpretation Note” (Section I-C) is helpful, and the abstraction table (Table X) is an excellent practice for avoiding misinterpretation. The overhead definition (Section III-F) is also unusually explicit and appreciated.

The abstract is information-dense and largely accurate, though it mixes results that are DES-validated with analytically derived statements and model-form uncertainty adjustments. Consider distinguishing explicitly in the abstract which numbers are (i) DES outputs, (ii) analytical extrapolations, and (iii) post-hoc adjustments via \(\gamma\).

Some sections are longer than necessary and occasionally repetitive, particularly where the manuscript repeatedly emphasizes that centralized \(c=1\) is a bound and that \(O(1)\) scaling is analytically guaranteed. This could be streamlined to improve readability. Also, a few captions and paragraphs include strong claims that are not fully consistent with the tables (noted above), which affects clarity.

Figures/tables are generally well chosen. However, several key plots are referenced but not shown in the provided LaTeX (e.g., the exact forms of Fig. 10/TDMA comparisons). Ensure that each figure is self-contained with axes labels and units; for T-AES, plots of overhead should clearly state whether they include baseline telemetry or only protocol overhead.

---

## 5. Ethical Compliance — **Rating: 4 (Good)**

The manuscript includes an explicit disclosure about AI-assisted ideation tools in the Acknowledgment and clarifies that the concept is not validated in the current study. This is appropriate and aligns with emerging transparency norms.

Potential conflicts of interest are not explicitly addressed. The authorship is listed as “Project Dyson Research Team” with affiliations deferred. For IEEE publication, this will need to be resolved, and any funding sources, organizational interests, or commercialization intent (given the project website and tools) should be disclosed.

No human/animal subjects issues apply. Data/code availability is promised, but the commit hash is pending; for ethical/reproducibility compliance, provide a fixed artifact at submission or at least upon revision.

---

## 6. Scope & Referencing — **Rating: 3 (Adequate)**

The topic fits IEEE Transactions on Aerospace and Electronic Systems, particularly in autonomy, constellation operations, and communication/coordination architectures. The paper also touches queueing theory, distributed algorithms, and DTN, which is appropriate for the journal audience.

Referencing is broad and includes relevant classics (Lynch, Kleinrock, Demers gossip, Lamport, Raft) and constellation networking (Handley, del Portillo, Akyildiz). However, several citations are non-archival or web pages (Starlink ops, Kuiper overview, DARPA program pages). These can be used sparingly for context, but core technical claims should rely more on archival sources. Also, the paper would benefit from citing more recent work on:
- LEO ISL MAC/scheduling and link intermittency models (deterministic contact plans, Earth occlusion),
- AoI in networks with scheduling (AoI under TDMA/queueing),
- constellation operations/autonomy literature on distributed SSA/conjunction screening.

Finally, the manuscript sometimes blends “space swarms” (deep future) with “mega-constellations” (near-term LEO broadband). That’s fine, but you should be explicit about which assumptions correspond to which regime (e.g., optical ISLs are plausible for Starlink-like systems; 1 kbps/node as a budget may be too small/large depending on mission).

---

## Major Issues

1. **Coordinator bandwidth stress test model needs re-formulation or clearer interpretation (Section IV-H, Tables XVIII–XIX).**  
   The current “byte-budget per cycle with tail-drop” effectively imposes a hard deadline and no buffering across cycles. If that is intended (must receive all reports within \(T_c\)), say so and define the deadline formally. If not intended, replace with a continuous-time service process (rate \(C_{\text{coord}}\)) plus finite buffer and/or per-message deadlines. The 50 kbps “unscheduled” threshold is otherwise a model artifact and may not generalize.

2. **Internal inconsistency in global-state mesh bandwidth statements (Section IV-A vs Table VI).**  
   The text claims mesh consumes “over 25%” at \(N=10^5\), but the table implies consumption vastly exceeding capacity. Correct the statement and ensure all mesh overhead comparisons use consistent normalization (per-node budget vs fleet aggregate).

3. **Comparability of architectures under a consistent coordination requirement.**  
   The hierarchical architecture is evaluated under one 512 B command per node per cycle (“stress-case”), while sectorized mesh uses heartbeats capped at 10 and a different command model. The global-state mesh assumes full-state replication. To support strong comparative claims, define a small set of *coordination tasks* (e.g., periodic ephemeris reporting, cluster tasking, local conjunction screening, cross-sector alerts) and ensure each architecture implements the same task semantics, differing only in routing/aggregation.

4. **MAC/PHY abstraction and the use of \(\gamma\) needs stronger grounding.**  
   \(\gamma\in[0.7,0.9]\) is used as a major uncertainty band, but without justification tied to a specific MAC/PHY. Either (i) cite specific ISL MAC studies and justify \(\gamma\), or (ii) implement a minimal TDMA schedule model in the DES (you already flag this as future work) and report sensitivity to guard time, synchronization error, and half-duplex constraints.

5. **AoI analysis should be tied to a decision requirement or at least a stylized conjunction screening model.**  
   AoI is a good metric, but currently it stops short of connecting to operational risk. Even a simplified mapping (e.g., miss probability vs AoI threshold; or “time-to-contact” distribution) would make the AoI results actionable and reduce the risk that the AoI section reads as an isolated metric demonstration.

---

## Minor Issues

- **Equation/notation clarity:**  
  - Eq. (3) uses \(\mu_s\) as messages/s; later bandwidth \(C_{\text{node}}\) is bits/s. Consider a consistent unit table and avoid reusing \(C\) for both capacity and coefficient.  
  - Eq. (21) “offered load” approximation in Table XVII footnote is unclear; provide the exact expected retransmission multiplier \(E[\text{attempts}]=\sum_{i=0}^{M_r}(1-p)^i\) and compute offered load accordingly.

- **Mesh traffic accounting mismatch:** Table XII lists “Gossip exchange (mesh) size \(256\times f\)” but Table VI uses \(256\times b\) with batch size \(b\). Make Table XII consistent with the batch model or explicitly separate “entry size” from “message payload size.”

- **Sectorized mesh definition:** Section III-C-4 defines sector size \(k_s=\lceil\sqrt{N}\rceil\) but then caps fanout to 10, which breaks the “full state for \(O(\sqrt{N})\) sector peers” claim in Table VII. For capped fanout, per-node state awareness is not “full sector peers”; revise Table VII accordingly.

- **Centralized baseline interpretation:** The paper repeatedly emphasizes that \(c=1\) is a bound. Consider moving most of this to a short paragraph and relying on Table I; it is currently verbose and distracts from the main contribution.

- **Data availability:** “commit hash: [PENDING]” should be replaced with an actual hash/tag in a revision.

- **Non-archival citations:** Several web citations are fine for context but should not underpin key numerical claims. Where possible, replace with archival sources or operator filings/technical papers.

---

## Overall Recommendation — **Major Revision**

The manuscript has strong potential and contains several valuable contributions (AoI framing, explicit traffic accounting, sectorized mesh comparator, coordinator capacity stress testing). However, key results—especially the coordinator bandwidth thresholds and some comparative statements—depend on modeling choices that are currently either inconsistent (mesh bandwidth statements) or insufficiently justified (per-cycle byte-cap drop model, \(\gamma\) values). Addressing the major issues above would substantially improve rigor, comparability, and interpretability, bringing the paper closer to IEEE T-AES standards.

---

## Constructive Suggestions

1. **Recast the coordinator capacity study as a deadline/queueing problem with explicit service discipline.**  
   Provide two models: (i) hard deadline within \(T_c\) (loss if late), and (ii) buffered service with finite queue and lateness penalty. Report thresholds under both; this will make the 50 kbps vs 24 kbps story robust and interpretable.

2. **Define a “coordination task suite” and ensure all architectures satisfy the same suite.**  
   For example: periodic ephemeris delivery to whoever is responsible for conjunction screening; command dissemination; local alerts; cross-sector alerts. Then implement each architecture’s mechanism for the same tasks. This will make the sectorized vs hierarchical comparison much stronger than comparing different traffic recipes.

3. **Tighten and correct the global-state mesh discussion and normalization.**  
   Align the narrative with Table VI: at \(N=10^5\) it is not “25%,” it is many multiples of the 1 kbps budget. If you want a “25%” statement, specify a different fanout/batch/round interval or define a different normalization (e.g., fraction of a hypothetical >Mbps ISL).

4. **Ground MAC efficiency \(\gamma\) with either citations or a minimal simulated TDMA.**  
   Even a simple slot/guard-time model inside the cycle (no packet-level PHY) would let you compute \(\gamma\) from first principles and explore sensitivity to synchronization error and guard sizing.

5. **Extend AoI to an operationally interpretable metric (even stylized).**  
   Add a simple mapping: e.g., assume orbital prediction error grows with time since last update and compute probability that a conjunction is detected before a time-to-contact threshold. This can be a lightweight model but would make the AoI results directly actionable for constellation operations.