---
paper: "02-swarm-coordination-scaling"
version: "dk"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-06"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript targets an important gap: providing *closed-form, per-cluster sizing equations* for hierarchical coordination traffic under a strict per-node logical budget, and explicitly tying message-layer accounting to TDMA airtime feasibility. The “rate ladder” and the two-test framing are practically useful for early-phase swarm/constellation architecture trades. The explicit separation of (i) information-byte budget and (ii) TDMA schedulability is a meaningful contribution because many papers conflate these layers or assume “throughput” without accounting for burst-mode reacquisition/guard.

Novelty is moderate-to-good rather than excellent because many individual ingredients are standard (TDMA efficiency factor, GE channel, AoI tails, Raft traffic forms). The novelty is in the *integration* and the “design equations” packaging, not in new theory. The paper is honest about the lack of external validation, which is good scholarly practice but also limits impact claims.

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The modeling stack (byte accounting → TDMA slot-time model via γ → slot-level simulator for deadline misses → DES for burstiness tails) is generally coherent and appropriate for preliminary sizing. The manuscript improved by anchoring γ to CCSDS Proximity-1 framing (0.73–0.76) and by clearly labeling Model S as non-design.

However, the methodology still has weak points for a top-tier aerospace systems journal: (i) some “verification” steps are largely self-referential (shared equations across tools), (ii) the GE model is explicitly a what-if tool but is used to support a fairly crisp 30 vs 35 kbps recommendation, and (iii) the TDMA/ARQ policy and ACK timing assumptions materially influence margins yet are not explored as a design space (beyond brief alternatives).

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internal logic is mostly consistent, and the paper is much clearer than typical sizing papers about what is assumed vs derived (e.g., α_RX as an output, not a knob). The campaign duty factor **d** is now used appropriately to address “continuous stress” realism, and the stress-case (~46%) is contextualized as an upper bound (<1% time), which is an improvement.

Key validity concerns remain:
- The feasibility framework is described as “two tests,” but there are moments where the narrative risks reintroducing a third implicit layer (“MAC efficiency”) via γ. The manuscript tries to prevent this (“unit conversion embedded in Test B”), but the presentation is still easy to misread.
- Some numerical claims depend sensitively on specific timing contracts (cold-start acquisition per slot, explicit ACK mini-slots, turnaround accounting). Small changes can move the 30 kbps “minimum” boundary; you acknowledge this, but the consequence is that the “30 infeasible, 35 recommended” conclusion is less universal than it reads.

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
Overall structure is strong: notation table, explicit definitions of η vs baseline, clear separation of Test A vs Test B, and a helpful algorithm. The “rate ladder” table is particularly effective for practitioners.

Clarity issues: (i) the manuscript is long and occasionally repetitive (γ disclaimers appear many times), (ii) several “tables” are referenced as if they were formal LaTeX tables but appear as labeled paragraphs (e.g., “Unmodeled overhead margin.”), and (iii) a few sections mix message-layer and physical-layer rates in ways that require careful reading (e.g., “1 kbps logical allocation within 35 kbps burst channel” is correct but should be reinforced with a single unambiguous diagram).

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
Good: code/data availability with a specific tag; explicit AI disclosure; clear statement that AI did not generate results/figures/data. Reproducibility seems plausible given the repository statement and parameter tables.

Remaining concerns: the paper should specify what is *actually* in the repository (e.g., does it include the packet/slot simulator and scripts to regenerate every figure/table?), and provide a minimal “reproduce paper” command sequence. Also, clarify licensing and long-term archival (Zenodo DOI would be better than GitHub-only).

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
Citations cover constellation ops, DTN/CCSDS, gossip, AoI, queueing, and GE. CCSDS anchoring is appropriate. However, for IEEE TAES / Adv. Space Res., the paper should more directly engage:
- Satellite TDMA return-link and DAMA literature beyond DVB-RCS2 (even if not directly ISL).
- Cross-layer scheduling for half-duplex burst links and short-packet satellite links.
- Any published smallsat ISL modem timing/acquisition measurements (even if partial/analogous) to reduce the “no external validation” gap.

---

# Major Issues

1) **The “three-layer feasibility framework” is not fully stabilized in exposition (byte budget vs γ vs airtime).**  
**Why it matters:** The paper repeatedly states “two tests,” but also talks about “MAC efficiency” and uses γ as a unifier. Readers can interpret γ as a separate feasibility layer (or confuse it with contention utilization), undermining the main conceptual contribution.  
**Remedy:**  
- Add a single figure early (maybe in Section I or at the Test A/B box) showing *exactly* where each factor lives:  
  - **Test A (bytes/info-rate)**: message generation and byte accounting → η_total ≤ 1.  
  - **Test B (time/airtime)**: TDMA schedule with slot time model → T_ing + T_egr + T_ARQ ≤ T_c.  
  - **γ**: maps payload bits to slot time within Test B only.  
- Remove/avoid “MAC efficiency” phrasing unless you explicitly define a separate multiplicative factor ρ_MAC for contention (you do mention it), and keep γ strictly “scheduled TDMA slot efficiency.”

2) **Campaign duty factor d: improved, but still not convincingly anchored to real operational timelines and command semantics.**  
**Why it matters:** The main realism critique of earlier versions (continuous full-load) is addressed by d, but the mapping from mission operations to (d, p_cmd, q, L_on) remains largely illustrative. If d is the key knob, it needs stronger justification and clearer interpretation (especially because stress-case η_S ~46% is central).  
**Remedy:**  
- Provide 2–3 concrete mission archetypes with numbers that are traceable: e.g., station-keeping cadence, orbit-raising sessions, software update campaigns, contingency operations.  
- Clarify whether “command every cycle” means *a single broadcast command per cluster per cycle* or something else. If commands are sometimes multi-message transactions (e.g., upload + verify + commit), represent that as an effective S_cmd multiplier or a burst model.  
- Include sensitivity of η and Test B margin to p_cmd < 1 during ON periods (you mention p_cmd=0.2 briefly—promote this to a figure/table).

3) **γ unification (0.76 CCSDS-based) is mostly consistent, but there are still risks of inconsistency and double-counting across slot timing, ACKs, and turnaround.**  
**Why it matters:** The 30 vs 35 kbps boundary is margin-driven. Any inconsistency in what is included in γ vs separately budgeted (ACK, resync preamble, turnaround, sync beacon) can shift feasibility. Reviewers will scrutinize this.  
**Remedy:**  
- Add a “timing ledger” table (single authoritative list) for Model C at each rate used (24/30/35 kbps) showing: payload, framing bits, FEC parity, preamble/sync, acquisition, guard, turnaround, ACK—each clearly marked as “in γ” or “outside γ but in Test B.”  
- Ensure the *same* ledger is used in Algorithm 1 line 4, Table VII (superframe), and the γ decomposition table. Right now the narrative asserts consistency, but it’s hard to audit.

4) **DES verification value is limited; it often confirms its own equations, and the “tail value-add” is not fully separated from assumed burst models.**  
**Why it matters:** For TAES-level contribution, simulation should either (i) validate against independent models/measurements, or (ii) demonstrate nontrivial emergent behavior not captured analytically. Your Tier-1/Tier-2/Tier-3 discussion is honest, but the paper still leans on DES results (buffer sizing factors) that are artifacts of assumed ON/OFF structure.  
**Remedy:**  
- Reframe DES tail results explicitly as *conditional on burst model class*, and provide at least one alternative heavy-tail ON-duration case (e.g., Pareto or lognormal ON times) to show robustness or to bound buffer factor M.  
- Alternatively, provide an analytical approximation (MMPP/D/1 or fluid bound) to corroborate the 1.30× buffer factor, so DES is not the only source.

5) **Packet-level validation (Section IV-J) is not truly independent validation; it is parameter anchoring.**  
**Why it matters:** The manuscript sometimes reads as if CCSDS-based γ “validates” feasibility. But it is still a modeling choice without hardware timing. This is fine if positioned as such; problematic if used to justify crisp design recommendations.  
**Remedy:**  
- Rename Section IV-J to something like “Standards-anchored parameterization (γ)” consistently (you already say this, but make it unmistakable).  
- Add a short subsection: “What would falsify our conclusion?” e.g., if measured T_acq P95 is 25 ms, or if half-duplex turnaround is 10 ms, or if additional PHY/MAC overhead reduces γ by >0.1—then 35 kbps may not suffice. This improves scientific posture.

6) **GE model coupling to ARQ and coherence-time assumptions: good discussion, but the operational implication is underdeveloped.**  
**Why it matters:** You correctly note intra-cycle ARQ is ineffective when τ_c ≥ T_c. But the paper then uses a single illustrative GE parameter set to argue 35 kbps is needed for ARQ margin. Practitioners will ask: should we provision ARQ slots at all? Should we instead rely on inter-cycle recovery? Should we use FEC adaptation?  
**Remedy:**  
- Add a design decision chart: choose (R_PHY, M_r, reliance on inter-cycle recovery) based on measured τ_c/T_c and p_B.  
- Consider including an alternative: eliminate intra-cycle ARQ (M_r=0) and accept inter-cycle recovery; quantify AoI penalty vs regained TDMA margin.

7) **Fleet-level reuse (R=7, F=8) is a major assumption with limited backing and could dominate feasibility at scale.**  
**Why it matters:** Even though the paper is “per-cluster,” the moment you discuss f_RF, reuse, and polar convergence, fleet feasibility becomes contingent on interference geometry. For large N, this can be the real bottleneck, not per-cluster TDMA.  
**Remedy:**  
- Tighten the scope: either (i) keep fleet reuse as a clearly labeled sketch and remove any “non-binding” claims without a more rigorous interference analysis, or (ii) add a simple stochastic geometry / worst-case co-channel occupancy bound and show sensitivity to latitude clustering.  
- At minimum, provide a table showing G as a function of (N, f_RF, F, R, k_c) for a few plausible regimes, and explicitly state that R=7 is a placeholder pending RF simulation.

---

# Minor Issues

1) **Table formatting:** Several items labeled with `\label{tab:...}` are not actual LaTeX tables (e.g., “Unmodeled overhead margin.”, “Mission phase mapping.”). Convert them to proper tables or remove `tab:` labels.

2) **Notation overload:** η, η_total, η_cmd, η0, η_S: consider adding a one-line “at a glance” box near Eq. (1) with numeric defaults at k_c=100.

3) **Command size realism:** 512 B is plausible, but commands often include authentication, sequence control, and sometimes multi-packet transactions. Clarify whether 512 B is payload or total message at the coordination layer.

4) **AoI interpretation:** You correctly identify the AoI P99 tail as sampling-limited under exception reporting. Consider explicitly stating that network latency is ~O(T_c) and does not drive AoI in that regime.

5) **Coordinator summary composition:** The “371 B metadata/CRC” breakdown includes “authentication 256 B.” If auth is present on every message, it should also appear in node reports/commands unless you assume link-layer security. Clarify security layer placement.

6) **Failure rates:** 2%/yr with MTTF 50 years is fine for “operational phase,” but for CubeSat-class swarms this might be optimistic depending on environment and radiation. A one-sentence sensitivity note would help.

7) **Threshold for feasibility (≤1% misses):** Justify the 1% deadline-miss threshold (mission requirement? control stability? buffering?), or present results as a curve of miss-rate vs rate.

8) **Algorithm 1:** Line 13 `L_cmd <- ceil(k_c T_cmd / (T_c - T_ing))` seems to ignore the (1-α_RX) partition and turnaround/sync overhead already in egress. Ensure it matches Eq. (27) exactly, or explain the approximation.

9) **Units:** Be consistent with kbps meaning 1000 bps vs 1024; you appear to use 1000, but state it once.

10) **References:** Some citations are non-archival (Kuiper overview, DARPA pages). That’s acceptable for context, but key technical assumptions (e.g., acquisition times, burst demod behavior) should rely on archival standards or technical reports where possible.

---

# Overall Recommendation  
**Recommendation:** **Major Revision**

The manuscript is promising and closer to publishable than many “sizing equation” papers because it (i) cleanly separates byte budget from airtime schedulability, (ii) acknowledges validation limits, (iii) provides practitioner-friendly artifacts (rate ladder, algorithm), and (iv) addresses workload realism via the campaign duty factor **d** and properly frames the ~46% case as a continuous-duty upper bound.

The main reasons for major revision are not formatting but *scientific positioning and auditability*: the γ-based timing contract and what is included/excluded (ACK, turnaround, preamble) must be made fully auditable in one place; the DES “value-add” must be strengthened beyond self-consistency; and the operational mapping of **d** (and p_cmd) should be anchored more convincingly to real mission timelines/semantics. Finally, Section IV-J is useful as standards-based anchoring, but it should not read like validation; the paper should more explicitly show how conclusions change under plausible deviations in acquisition/guard/γ.

---

# Constructive Suggestions (ordered by impact)

1) **Add a single authoritative “Model C timing ledger”** (per rate) that explicitly partitions: in-γ vs out-of-γ but in Test B. Ensure every numeric margin and feasibility claim references this ledger.

2) **Strengthen the duty-factor realism argument:** add mission archetypes with traceable schedules; elevate p_cmd sensitivity (not just d) into a table/figure; clarify command transaction semantics.

3) **Recast DES results as conditional and broaden burst models:** include at least one heavy-tailed ON-duration case or an analytical corroboration so buffer factor recommendations are not tied to one ON/OFF assumption.

4) **Clarify the feasibility framework visually:** a block diagram showing Test A and Test B and where γ sits; remove remaining language that could be read as “three tests.”

5) **Turn ARQ into a design choice rather than a fixed assumption:** present a small design space trade (M_r=0 vs 1 vs 2) under slow vs fast mixing, with explicit AoI penalty and required rate.

6) **Tighten fleet-level reuse claims:** either scope them down or provide a more rigorous sensitivity table; clearly label R=7 as provisional.

7) **Make Section IV-J explicitly “parameter anchoring”:** rename accordingly and add a “falsification conditions / measurement requirements” paragraph.

8) **Reproducibility upgrade:** add a “Reproduce all figures” script entrypoint and consider archiving the repository snapshot with a DOI.

If the authors implement (1)–(4) well, the paper would likely move into “accept with major/minor revisions” territory for a top-tier aerospace systems venue, even without external hardware validation, because it would read as a careful, auditable preliminary design methodology rather than a potentially brittle set of point conclusions.