---
paper: "02-swarm-coordination-scaling"
version: "ap"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-27"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 4/5 (Good)**

The manuscript targets a practically important and timely problem: how to *size* coordination/telemetry architectures for very large autonomous spacecraft swarms (10³–10⁵, with discussion toward 10⁶) under a constrained “RF-backup” communications budget. The paper’s most distinctive contribution is not proposing a new coordination algorithm per se, but providing *closed-form sizing equations* (overhead, coordinator ingress capacity, AoI quantiles under exception telemetry, and loss recovery behavior) and showing that these factors “compose” under a point-to-point ISL abstraction. For T-AES readership, the emphasis on engineering design equations plus a reproducible simulation tool is valuable.

The novelty claim (“No prior work has systematically compared … using byte-level traffic accounting under a fixed per-node budget,” Introduction) is directionally plausible, but currently stated too strongly. There is extensive related work in constellation ops, DTN/space networking, and distributed estimation/consensus that touches parts of this space; your novelty is really the *combination* of (i) explicit byte accounting with (ii) hierarchical aggregation and (iii) parametric sizing across 10³–10⁵ with (iv) AoI and (v) correlated-loss stress tests. Reframing the novelty around this integrated sizing framework (rather than “no prior work”) would be more defensible and would preempt reviewer pushback.

A further strength is the explicit acknowledgment that hierarchical advantages are mainly *fault tolerance during ground outages and spectrum independence*, not latency (Section IV-G). That is an important and honest positioning relative to centralized architectures, especially given current Starlink/Kuiper operational realities.

---

## 2. Methodological Soundness — **Rating: 3/5 (Adequate)**

The methodology is generally appropriate for the stated RQs, and the manuscript is unusually explicit about traffic accounting (Tables 3–5, 8–9) and about what is and is not modeled (Table 7). The cycle-aggregated DES is a reasonable choice to reach 10⁵ nodes quickly, and you provide several analytical cross-checks (Palm–Khintchine convergence for centralized arrivals; AoI P99 geometric tail Eq. (23); overhead agreement within 0.1%). The open-source release and parameter table (Table 6) support reproducibility.

However, several modeling choices materially affect key conclusions and need tighter justification or sensitivity analysis:

* **Coordinator ingress sizing vs. physical radio constraint.** You assume each node has a 1 kbps “budget” but then require every node transceiver to “support the coordinator ingest rate (≥24 kbps)” (Section III-F, end). This is a major architectural assumption: it effectively changes the RF design point from “1 kbps per node” to “1 kbps average but 20–50 kbps peak when acting as coordinator (and possibly when sending to coordinator under TDMA).” That may be reasonable, but it must be made explicit as a *hardware requirement* and reconciled with the stated motivation (S-band TT&C-like rates). Right now it reads like a contradiction rather than a deliberate peak/average provisioning model.

* **Queueing/latency modeling is internally inconsistent in places.** Centralized is modeled as M/D/1 with deterministic service (Eq. (2)), while hierarchical within-cycle coordinator behavior is described as a batch D[k]/D/1 system (Section III-B, “Within-cycle dynamics resemble…”), and later latency includes “cycle-alignment (T_c/2)” (Table 18 caption). It’s not always clear which latencies include waiting-to-cycle-boundary, which include queueing, and which include serialization. Since latency is used in comparisons (Section IV-G; Figs. 16–17), you should standardize latency definitions and ensure the DES and analytical components are aligned.

* **Correlated loss recovery is not simulated.** Section IV-C’s “inter-cycle store-and-forward recovery” is explicitly analytical extrapolation, not in DES. Yet it is used as a key design outcome (“95% within 4–7 cycles”). That may still be publishable, but it needs either (i) inclusion in DES, or (ii) a more formal derivation with clear assumptions about retry policy, buffering, and independence across cycles, and a sensitivity study over GE parameters (pGB, pBG, pB) because “4–7 cycles” will vary substantially with burst length.

Statistically, 30 Monte Carlo replications are fine for stable metrics like mean overhead, but for tail metrics (P99 AoI, maximum AoI, rare failure cascades) you should justify adequacy (or use more replications / longer runs / analytical tails). The bootstrap CI for AoI P99 is a good start, but similar uncertainty quantification is missing for other tail claims (drops under capacity stress; availability under coordinator failures).

---

## 3. Validity & Logic — **Rating: 3/5 (Adequate)**

Many conclusions are well supported for the *model you implemented*. In particular: (i) overhead invariance vs N under O(N) messaging is consistent and convincingly validated (Table 14; Fig. 12); (ii) exception telemetry producing geometric AoI tails is correct and the P99 match (Eq. (23) vs Table 12) is a strong internal validation; (iii) the claim that stress-case overhead is command-dominated is clearly demonstrated (Fig. 14).

The principal validity risk is that several headline results depend on stage ordering and abstraction choices that may not hold in realistic RF-backup operations:

* **“Independence” result is conditional on loss occurring before coordinator ingress.** Section IV-D concludes GE retransmissions do not increase coordinator drops because losses are applied before ingress. This is logically correct in your pipeline, but it is not a property of hierarchical coordination per se; it is a property of *where you place contention and buffering*. In many RF architectures, retransmissions and access contention occur at the same bottleneck (shared medium, half-duplex radios, scheduling overhead), which would couple loss and saturation. You do acknowledge this caveat, but the paper currently elevates “compositionality” as a core contribution; it should be framed more narrowly as “compositionality under point-to-point, non-contention links with pre-ingress loss.”

* **Centralized baseline comparisons mix dimensions.** You argue centralized processing doesn’t diverge until ~10⁶ with realistic provisioning (Section IV-G; Table 19), but then also state centralized constraints are spectrum and contact availability. That is fair, but then the paper’s baseline overhead for centralized (Table 9) appears to assume per-node command rate ~100 bps, while hierarchical stress-case assumes 512 B commands every cycle (~406 bps). If the point is to compare architectures under the *same coordination workload*, then command workload should be held constant across architectures (or explicitly justified as architecture-dependent). As written, readers may infer hierarchical is “more expensive” partly because it is assigned a heavier command model.

* **Sectorized mesh model is heuristic and possibly optimistic.** The capped-fanout sectorized mesh becomes O(N) by imposing a constant neighbor cap (Eq. (12)); that may be operationally plausible, but then the “state completeness” comparison (Table 4) and “sector coverage” in Table 2 become central to interpreting what capability is being traded away. The paper should more explicitly state what coordination functions remain feasible under capped fanout (e.g., conjunction screening quality, formation keeping, task allocation) and which do not, otherwise the overhead comparison risks being apples-to-oranges.

Overall, the logic is coherent, but several comparisons and “design point” implications require clearer scoping: what is being held constant (workload, reliability target, state accuracy), and what is allowed to vary with architecture.

---

## 4. Clarity & Structure — **Rating: 4/5 (Good)**

The paper is well organized, with a clear roadmap (start of Section IV) and consistent use of tables/figures to support claims. The abstract is information-dense and largely accurate, though it contains several quantitative claims that are highly conditional (e.g., “simulation verifies composition without cross-factor correction”)—I suggest adding a phrase like “under point-to-point ISL and pre-ingress loss modeling assumptions” to avoid overgeneralization.

Strengths in presentation include: explicit traffic accounting tables; a “modeled vs abstracted” table (Table 7); and the design-equations summary in Discussion. The figures appear well chosen (phase staggering, AoI curve, workload envelope, scaling plots). The practitioner-oriented intent comes through.

Main clarity issues:

* **Terminology around “1 kbps per-node RF-backup budget” vs coordinator link capacity.** This is currently confusing (Section III-F and Section IV-A). You need a crisp statement early: e.g., “Each spacecraft allocates 1 kbps *average* to coordination, but the radio supports higher instantaneous rates when scheduled (TDMA) and when acting as coordinator.” Without that, readers will question feasibility.

* **Some equations/claims need tighter definitions.** Example: Eq. (17) TDMA capacity uses “(k_c − 1) × S_eph” but earlier you state k_c members each send 256 B/cycle; why “−1”? If excluding coordinator’s own report, say so explicitly. Similarly, the “Fleet-wide TDMA cost is 0.28 kbps/node (1% coordinators)” (Section IV-A) is not immediately derivable; show the arithmetic or cite an equation.

* **Latency reporting mixes ms-scale processing with cycle-scale alignment.** Table 18 gives ~260 ms mean, while Table 20 reports 340–675 ms “Latency includes cycle-alignment (T_c/2).” This inconsistency will confuse readers unless you separate (i) within-cycle processing latency and (ii) update-to-availability latency including cycle phasing.

---

## 5. Ethical Compliance — **Rating: 4/5 (Good)**

The manuscript includes an explicit disclosure that AI-assisted ideation influenced aspects of the coordinator architecture but is not validated (Acknowledgment). That is a positive step and aligns with emerging transparency expectations.

Two improvements are advisable for IEEE/T-AES norms:

* **Clarify authorship and responsibility.** The acknowledgment names specific AI systems; consider adding one sentence that AI tools did not generate final results/code and that authors take responsibility for correctness. This is increasingly expected and reduces ambiguity.

* **Conflict-of-interest / affiliation transparency.** The author block is “Project Dyson Research Team” with deferred individual names. That may be acceptable for review, but for ethical compliance you should ensure the final version includes full author identities and any funding/organizational interests (especially because the project hosts interactive simulators and a public website that could be perceived as promotional).

No human-subjects or sensitive-data concerns are apparent.

---

## 6. Scope & Referencing — **Rating: 3/5 (Adequate)**

The topic fits IEEE Transactions on Aerospace and Electronic Systems: spacecraft constellation operations, autonomous coordination architectures, and comms/queueing-based sizing. The paper is more “systems engineering + networking/queueing” than “aerospace electronics,” but still well within scope, especially given mega-constellation relevance.

Referencing is broad and generally appropriate (queueing, AoI, gossip, constellation networking, DTN, reliability). That said, several citations are non-archival or grey literature (Kuiper overview page; DARPA program pages; McDowell; NRL magazine). Some are unavoidable for operational context, but for a T-AES paper you should bolster archival support where possible, particularly for (i) Starlink ops claims, (ii) RF backup rate assumptions, (iii) ground contact availability, and (iv) conjunction event rates.

Also, the paper would benefit from citing more directly relevant work on:
* hierarchical/federated constellation autonomy and distributed space tasking (beyond F6/Golkar),
* LEO ISL MAC/scheduling constraints (TDMA/beam scheduling/half-duplex effects),
* “Age of Information” under periodic-with-skips and under erasures correlated with scheduling (to connect AoI with link outages more rigorously).

Finally, the “global position oracle” for sectorized neighbor discovery (Section III-D) is a strong assumption; citing operational approaches (e.g., ADS-B-like beacons, ephemeris broadcast, or onboard SSA methods) would help frame feasibility.

---

## Major Issues

1. **Peak-rate vs average-rate inconsistency at the RF-backup design point (Section III-F; Section IV-A).** The manuscript frames 1 kbps as the per-node RF-backup budget, but then requires coordinator ingress of 21–50 kbps and states “every node’s transceiver must support … ≥24 kbps.” This is a fundamental feasibility point and must be resolved explicitly (peak vs average, separate channels, different radios, buffering/scheduling assumptions, or revised budget definition).

2. **Inter-cycle recovery under correlated loss is a key conclusion but is not implemented/validated in DES (Section IV-C).** Either implement cross-cycle ARQ/store-and-forward in the simulation (even in aggregated form) or provide a more rigorous analytical model with sensitivity to GE parameters and retry policy. As is, “95% within 4–7 cycles” is plausible but insufficiently substantiated for a headline design claim.

3. **Architecture comparisons do not consistently hold workload constant (notably command traffic).** Centralized vs hierarchical overhead and capacity comparisons risk being confounded by different implied command dissemination models (Table 9 vs stress-case hierarchical). You should define a common workload vector (reports, commands, alerts) and apply it uniformly to all topologies, or clearly justify why workload differs by architecture.

4. **Latency definitions are inconsistent across tables/sections (Table 18 vs Table 20; Section IV-G).** Separate and standardize: (i) processing/queueing latency, (ii) cycle-induced staleness (AoI), and (iii) end-to-end command effect latency. Otherwise, readers cannot interpret “340–675 ms” vs “~260 ms” totals.

5. **“Compositionality/independence” is overclaimed (Section IV-D).** The independence result is contingent on point-to-point links and the ordering of loss vs ingress. It should be reframed as a property of the specific modeled pipeline and not generalized as a design principle without stronger justification.

---

## Minor Issues

- **Eq. (17) TDMA capacity uses (k_c − 1)** without explanation. If excluding coordinator’s own report, state it; otherwise use k_c.
- **Table 18 latency decomposition** totals (~260 ms) appear to omit cycle alignment and possibly serialization; clarify what is included.
- **Section III-B “propagation latency (10–240 ms round-trip)”** for centralized: provide a reference or a short derivation (LEO-to-ground geometry, gateway routing).
- **Table 6 “Clusters per region k_r = ceil(N/(k_c * n_r))”**: this makes k_r a derived quantity but earlier k_r is described as “clusters per region” with configurable fan-out. Clarify which parameters are free vs derived.
- **Global-state mesh accounting**: the derivation of redundancy factor “~1.4×” is not explained (Table 3 footnote). Provide a citation or a short rationale.
- **Failure/availability modeling**: Section IV-H states MTTR ≈ 35 s including SWIM and Raft; show the components or cite typical SWIM detection times and election timeouts.
- **Overhead definition**: you exclude baseline status reports from η (reasonable), but then sometimes discuss “total utilization” as η + 20.5%. Consider consistently reporting both “protocol overhead η” and “total channel utilization u” in results plots/tables to reduce confusion.
- **Reference quality**: replace or supplement non-archival citations where possible (Kuiper/OneWeb ops, DARPA pages, McDowell).

---

## Overall Recommendation — **Major Revision**

The paper has strong potential and contains several publishable ideas (byte-level sizing equations; AoI quantiles under exception telemetry; coordinator ingress capacity bracketing; reproducible tooling). However, there are foundational clarity/feasibility issues around the RF-backup rate assumptions versus required peak coordinator link capacity, and at least one headline resilience result (inter-cycle recovery under GE loss) is not validated in the simulation. In addition, cross-architecture comparisons need a more consistent workload definition, and latency metrics require normalization. Addressing these points would substantially strengthen credibility and make the design equations more actionable for T-AES readers.

---

## Constructive Suggestions

1. **Resolve the “1 kbps budget vs 21–50 kbps coordinator ingress” by introducing an explicit peak/average radio model.** For example: define (i) average allocated coordination throughput per spacecraft (1 kbps), (ii) instantaneous PHY rate supported (e.g., 32/64 kbps S-band burst), (iii) duty factor under TDMA, and (iv) buffering requirements. Then restate coordinator capacity results in terms of *required PHY rate* and *duty cycle* rather than only kbps.

2. **Implement cross-cycle retry/store-and-forward in the DES (even as an aggregated Markov/buffer model).** This would allow you to validate the “4–7 cycles to 95%” claim under GE loss, and to quantify buffer growth, delay distributions, and coupling with coordinator capacity when losses occur post-ingress (a more pessimistic but realistic case).

3. **Define a single workload vector and apply it uniformly across centralized/hierarchical/sectorized mesh comparisons.** Create a table: per node per cycle—status reports, commands (probability p_cmd), heartbeats/ACKs, alerts. Then compute η for each topology under identical workload and show where topologies force additional traffic (e.g., neighbor heartbeats, summaries). This will make Table 19/Fig. 16 comparisons more defensible.

4. **Standardize latency/AoI reporting into three clearly separated metrics.** Suggested: (i) message transport latency (prop + serialization + queueing), (ii) update staleness/AoI at decision point, (iii) command actuation latency. Ensure every table/figure states which metric it uses and whether cycle alignment (T_c/2) is included.

5. **Tighten the “independence/compositionality” claim with a small counterexample experiment.** Add one additional DES mode where retransmissions occur *after* ingress (or where a shared-medium contention model approximates coupling). Even a simplified contention model (slotted ALOHA with backoff) would demonstrate when independence fails and would sharpen the paper’s main conditional insight.