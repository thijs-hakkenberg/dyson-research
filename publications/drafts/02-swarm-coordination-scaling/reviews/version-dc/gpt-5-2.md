---
paper: "02-swarm-coordination-scaling"
version: "dc"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-05"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript targets a real and under-served gap: *early-phase sizing* of coordination communications for very large autonomous swarms, with explicit byte accounting and a schedulability check that forces the reader to confront burstiness, half-duplex TDMA timing, and overheads. The paper’s strongest novel contribution is the **closed-form, per-cluster “rate ladder”** tying (i) message-layer load, (ii) slot efficiency, and (iii) superframe airtime feasibility, culminating in a practical recommendation (30 kbps min / 35 kbps recommended for the stated assumptions).  

However, the novelty is primarily in **systematization and parameter unification** rather than fundamentally new theory. For a top-tier journal, the contribution can still be publishable if the authors sharpen the *claim boundaries* and strengthen the “independent validation” narrative (see Major Issues).

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The two-test framework (Test A byte budget + Test B TDMA airtime) is methodologically reasonable and aligns with how practitioners actually size such systems. The slot-efficiency derivation from CCSDS Proximity-1 framing is a defensible *standards-based estimate* and is a clear improvement over an arbitrary constant. The DES is positioned appropriately as verification + tail exploration.  

That said, several modeling choices materially affect conclusions (e.g., GE coherence per cycle; fixed per-slot acquisition; deterministic reservation of ARQ slots; static cluster membership). These are not “wrong,” but they need tighter justification and clearer sensitivity treatment—especially where the paper makes design recommendations (35 kbps) that are sensitive to acquisition/guard/ACK handling and to whether ARQ is provisioned.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internal logic is mostly consistent, and the manuscript repeatedly flags “no external validation,” which is good scholarly hygiene. The campaign duty factor **d** is a meaningful knob that directly addresses workload realism concerns, and the stress case (≈46% overhead) is now explicitly framed as a continuous-duty upper bound occurring <1% of time—this is an improvement.  

Remaining validity concerns are mainly about (i) potential double counting / ambiguity in how baseline vs. overhead interacts with TDMA time (bytes vs. airtime), (ii) whether the “three-layer” framing (byte budget, MAC efficiency, TDMA airtime) is consistently presented as *two tests* plus a conversion (you try to do this, but some sections still read like three checks), and (iii) whether the “packet-level validation” is truly independent (it is still largely parameter anchoring).

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
The paper is unusually explicit about notation, assumptions, and what is and is not being claimed. The “Rate Ladder” table and the superframe time budget are particularly clear and useful. The repeated warnings about Model S vs. Model C are helpful.  

Opportunities: reduce repetition (gamma explanations occur in multiple places), and tighten the narrative around validation tiers so readers don’t interpret Tier-2 anchoring as empirical validation.

---

## 5. Ethical Compliance  
**Rating: 5 (Excellent)**  
Strong reproducibility posture: code and tag provided, parameters enumerated, runtime stated. AI disclosure is explicit and appropriately scoped (ideation/editing only). No human-subject or sensitive data issues.

---

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
Citations cover distributed algorithms, AoI, DTN/ISL, CCSDS, and TDMA standards. For T-AES / Adv. Space Res., I would still expect deeper engagement with: (i) satellite TDMA/DAMA scheduling literature beyond DVB-RCS2 (especially deterministic scheduling and burst-mode acquisition overheads), (ii) LEO ISL physical layer / acquisition and tracking studies, and (iii) queueing for bursty arrivals at gateways/coordinators (MMPP results are mentioned but not developed).  

The paper is in-scope, but it should better situate itself relative to existing satellite MAC/TDMA sizing methods and constellation operations literature.

---

# Major Issues

1. **“Independent validation” is still overstated; packet-level γ is parameter anchoring, not validation.**  
   - **Why it matters:** The central design recommendation (30 kbps min, 35 kbps recommended) is driven by γ and slot timing. If γ is not empirically validated, then the recommendation is a conditional estimate. The manuscript says this, but Section IV-J can still be read as stronger than it is (“validated via CCSDS”).  
   - **Remedy:** Reword consistently: use “**standards-based parameterization**” or “**standards-anchored estimate**,” not “validated.” Add a short paragraph explicitly stating what *would* constitute validation (e.g., measured acquisition-time distribution, measured turnaround, measured PHY framing overhead in the actual modem).

2. **Campaign duty factor d helps realism, but the mapping from operations → (d, p_cmd, q) remains too ad hoc for design use.**  
   - **Why it matters:** The main realism critique of earlier versions (implied continuous heavy command load) is now addressed via **d**, but practitioners will ask: “How do I pick d and p_cmd without handwaving?” Your Table V (duty mapping) is a start, but it mixes event-driven and campaign-driven notions and uses single-point values.  
   - **Remedy:** Provide a *procedural* mapping: define “campaign” formally (ON duration distribution, inter-campaign distribution), and show at least one **end-to-end example** turning a plausible ops timeline into d and p_cmd with uncertainty bounds. Include sensitivity: e.g., show η_total and required R_PHY for d ∈ [0.01, 0.2] and p_cmd ∈ [0.01, 0.1] (within campaigns), to demonstrate robustness.

3. **The “three-layer feasibility framework” needs crisper formalization: MAC efficiency is a conversion, not a third feasibility layer, but the text sometimes treats it as separate.**  
   - **Why it matters:** Reviewers/readers will look for a clean separation: (A) byte budget feasibility, (B) airtime feasibility. Introducing C_raw = C_info/γ is fine, but it must not read like an additional independent constraint, otherwise it invites double counting and confusion about what is actually tested.  
   - **Remedy:** In the Results/Discussion, enforce one canonical statement: *Test A uses information bytes only; Test B uses time with slot timing; γ enters only through T_slot or equivalently through C_raw conversion.* Remove or relocate Eq. (mac_efficiency) unless it is explicitly labeled “unit conversion used inside Test B.”

4. **ARQ provisioning model is overly conservative and structurally coupled to the per-cycle GE coherence assumption; conclusions about ARQ “infeasibility” are therefore conditional and partly tautological.**  
   - **Why it matters:** You correctly note that 27% intra-cycle recovery is a direct consequence of assuming channel state constant over the cycle. Similarly, reserving **M_r fixed slots per node per cycle** is a worst-case provisioning that can dominate airtime feasibility and drive the 35 kbps recommendation. A reader could conclude “ARQ is infeasible at 30 kbps,” but that depends strongly on (i) coherence time, and (ii) ARQ scheduling policy (reserved vs. on-demand).  
   - **Remedy:** Add an alternative ARQ scheduling analysis: e.g., **shared retransmission pool** sized to a percentile of expected losses (binomial/Markov), or a bounded “NACK list + selective repeat next cycle.” Quantify how much margin is recovered compared to per-node reservation. Even a simple analytic bound (e.g., Chernoff bound on number of losses per cycle) would strengthen the argument and reduce dependence on a single conservative policy.

5. **Half-duplex and ACK handling assumptions need to be made fully consistent across γ, superframe budgeting, and Algorithm 1.**  
   - **Why it matters:** The paper discusses ACK mini-slots and possibly embedding ACK in guard time. Depending on which is assumed, γ and/or T_slot changes, as does the superframe margin. Small changes matter near the 30 kbps boundary.  
   - **Remedy:** Choose one ACK model for “primary results” and propagate it everywhere (tables, algorithm, γ decomposition). If you keep both, present them as two explicit configurations and show the delta in R_PHY,min and margin.

6. **Coordinator ingress bottleneck and “1 kbps per-node budget” relationship is conceptually subtle; the manuscript risks confusing logical allocation vs. physical channel rate.**  
   - **Why it matters:** Some readers will interpret 1 kbps/node as a physical per-node link, while you intend it as a logical share of a cluster channel. This affects how they interpret feasibility and scalability.  
   - **Remedy:** Add a single schematic (even a simple figure) showing: one cluster channel at R_PHY, partitioned into ingress/egress time, supporting k_c nodes each with average C_node = 1 kbps info allocation. This would prevent misinterpretation and reduce repeated prose.

---

# Minor Issues

1. **Terminology:** Replace “validated via CCSDS” with “anchored/parameterized using CCSDS framing” everywhere (abstract, notation table, Section IV-J).  
2. **Consistency check:** Abstract says γ ≈ 0.70–0.76; notation table lists γ24=0.761, γ30=0.745, γ35=0.732. Consider stating the range as “0.73–0.76 for 24–35 kbps under Model C (cold-start).”  
3. **Table IV (rate feasibility):** The row order (30, 35, 24, 50) is non-monotonic; reorder by rate for readability.  
4. **AoI framing:** Clarify that AoI P99=440 s result is for exception reporting with independent Bernoulli sampling; it is not a network delay metric. You mostly do this—consider moving the “sampling tail” warning into the first paragraph of IV-B.  
5. **Fleet reuse:** The reuse factor R=3 argument is a single-interferer bound; you already warn about multi-interferer. Consider adding a short equation or reference for aggregate interference scaling (even a back-of-envelope) to justify the “3–6 dB” statement.  
6. **Algorithm 1:** Line 3 uses η0 fixed at 5% but later notes it shrinks with k_c. Either accept η0(k_c) or explicitly state Algorithm 1 uses conservative η0=5% regardless of k_c.  
7. **GE parameter mapping:** You state p_BG ≈ T_c / \bar{T}_B; dimensionally this is only approximate for small probabilities. Consider stating p_BG ≈ 1 − exp(−T_c/\bar{T}_B).  
8. **Model S table (ARQ×TDMA coupling):** Since Model S is “not for design,” emphasize why it is included and what insight transfers to Model C (qualitative coupling) vs. what does not (numerical thresholds).

---

## Overall Recommendation  
**Recommendation:** **Major Revision**

The manuscript is promising and closer to publishable than many “mega-constellation coordination” papers because it is explicit, quantitative, and reproducible. The campaign duty factor **d** meaningfully addresses workload realism, and the stress-case (η ≈ 46%) is now appropriately contextualized as a continuous-duty upper bound rather than an expected operating point. The move from an earlier fixed γ to a **CCSDS-anchored, rate-dependent γ(R_PHY)** is also a substantial improvement, and the “rate ladder” presentation is genuinely useful to practitioners.

The primary remaining barrier is evidentiary and interpretive: the paper must more cleanly separate **parameter anchoring** from **validation**, and it must reduce dependence of key conclusions (e.g., ARQ infeasibility at 30 kbps; 35 kbps recommendation) on a single conservative ARQ provisioning policy and a particular GE coherence assumption. Addressing these issues does not require external flight data, but it does require clearer conditional claims and at least one alternative ARQ scheduling/sizing analysis to show robustness.

---

## Constructive Suggestions (ordered by impact)

1. **Recast Section IV-J and all mentions of “validated” γ** as “standards-anchored estimate,” and add a concise “what would falsify this” measurement plan (you already have a roadmap—tighten and elevate it).  
2. **Add an alternative ARQ sizing policy** (shared retransmission pool or inter-cycle selective repeat) and quantify how it changes required margin / R_PHY,min.  
3. **Strengthen the operational mapping for d (and p_cmd, q)** with a procedural method and uncertainty bounds; show robustness plots for plausible ranges.  
4. **Unify the feasibility narrative**: two tests only; γ is a conversion inside Test B. Remove any lingering “third layer” ambiguity.  
5. **Standardize ACK/guard/acquisition assumptions** into 1–2 explicit configurations and propagate consistently through γ, superframe tables, and Algorithm 1.  
6. **Add one clarifying figure** showing the logical 1 kbps/node allocation within a single cluster TDMA channel and how ingress/egress partitioning produces α_RX.