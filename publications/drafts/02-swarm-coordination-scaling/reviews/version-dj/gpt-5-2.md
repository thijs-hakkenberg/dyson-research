---
paper: "02-swarm-coordination-scaling"
version: "dj"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-06"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 3 (Adequate)**  
The paper’s main contribution is a *practitioner-oriented sizing workflow* for hierarchical coordination under a tight per-node logical budget, with a clean decomposition into (A) message-layer byte budget and (B) TDMA airtime schedulability, plus a standards-grounded slot-efficiency parameterization. This is useful as an engineering “rate ladder” and early design calculator, especially because many swarm/constellation papers stop at qualitative scaling or asymptotics.  

However, novelty is moderate: most ingredients (byte accounting, TDMA airtime checks, GE what-if loss, AoI tails under sampling, ARQ margining, hierarchical aggregation) are known individually. The incremental value is the *integration* and the explicit identification of the coordinator ingress as the binding constraint at 1 kbps/node, plus the explicit CCSDS-based \(\gamma(R)\) treatment and the campaign duty factor \(d\) framing.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The modeling stack is internally coherent: analytical accounting → DES for distributional effects → slot-level TDMA simulator for deadline misses → packet/framing-based \(\gamma\) anchoring. The three-layer feasibility framing (byte budget, MAC/slot efficiency, TDMA airtime) is mostly sound, and the paper is unusually explicit about what is and is not validated.  

That said, several “engineering choices” are doing heavy lifting (cold-start acquisition per slot; GE coherence assumption; independent per-node GE; fixed cluster membership; half-duplex partitioning and ACK handling). These are defensible as conservative assumptions, but the paper sometimes converts them into crisp feasibility claims (e.g., “30 kbps minimum,” “35 kbps recommended”) without adequately bounding sensitivity to *real modem behavior* (burst-mode reacquisition, preamble detection statistics, coding/interleaving, and whether acquisition time scales with Doppler/SNR). The Monte Carlo replication count is fine for mean metrics but doesn’t address structural model risk.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Core logic is generally consistent, and Version DJ improves clarity on: (i) \(d\) as episodic workload realism; (ii) \(\eta_S\approx 46\%\) as a continuous-duty upper bound; and (iii) “\(\gamma\) is a unit conversion embedded in Test B, not a third test.” The “do not double-apply \(\gamma\)” warnings are helpful.  

Remaining validity risks are mainly *boundary-condition leakage*: the paper’s claims hinge on centrally scheduled TDMA with negligible contention, stable timing, and per-slot reacquisition. The GE/ARQ conclusions depend strongly on the coherence-time regime choice (\(\tau_c \ge T_c\) vs. \(\tau_c \ll T_c\)), but the manuscript sometimes reads as if the slow-mixing regime is the default “likely” case without sufficient empirical justification. Also, the DES “verification” is at times tautological, and the packet-level “validation” is closer to parameter derivation than independent validation.

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
Overall organization is strong: clear notation, explicit feasibility box, rate ladder table, and a reasonably actionable Algorithm 1. The manuscript is candid about limitations and validation gaps (rare and appreciated). The duty-factor mapping table is a good step toward workload realism.  

Opportunities: the paper is dense and occasionally repetitive (multiple places restating “\(\gamma\) is not a separate test,” etc.). Some key quantities (e.g., \(\alpha_{\text{RX}}\)) are described as “computed output” but then used in heuristic equations in ways that can confuse readers about circularity. A single consolidated “end-to-end sizing example” with all steps (byte budget → TDMA schedule → ARQ margin → recommended rate) would reduce cognitive load.

---

## 5. Ethical Compliance  
**Rating: 5 (Excellent)**  
Strong reproducibility posture: code and tag provided, environment stated, and explicit AI disclosure. No human/animal subjects. The paper is transparent about lack of external validation and frames results as preliminary design estimates.

---

## 6. Scope & Referencing  
**Rating: 4 (Good)**  
References are broadly appropriate across distributed algorithms, constellation networking, CCSDS, AoI, and GE channel modeling. The CCSDS grounding for framing/coding is a good choice for an aerospace journal audience.  

Minor gaps: for TDMA/demand-assigned scheduling and burst-mode satellite PHY/MAC, you could cite additional space/return-link TDMA and burst-mode acquisition literature beyond DVB-RCS2 (and possibly CCSDS UHF/S-band Prox-1 implementation notes, if available). For correlated fading and coherence-time arguments, more direct citations (LEO ISL measurement campaigns, CubeSat radio burst performance, or even terrestrial burst-mode acquisition studies) would strengthen claims.

---

# Major Issues

1. **Campaign duty factor \(d\): improved framing, but still under-justified and partially conflated with command probability**  
   **Why it matters:** \(d\) is central to addressing workload realism concerns and to interpreting the “46% stress-case” as an upper bound. If \(d\) is not grounded in plausible operational timelines, readers may still view results as arbitrary. Also, the paper uses both \(d\) and \(p_{\text{cmd}}\); in places, “stress” implicitly sets both to 1, which can mislead practitioners about what “continuous duty” means.  
   **Remedy:**  
   - Add a short subsection that *separates three concepts* with an explicit example timeline: (i) campaign ON/OFF duty \(d\); (ii) conditional per-cycle command probability \(p_{\text{cmd}}\) during ON; (iii) unicast fraction \(q\).  
   - Provide 2–3 mission archetypes with numeric schedules (e.g., station-keeping, orbit-raising, disposal) and compute \((d,p_{\text{cmd}})\) from those schedules.  
   - Make the “<1% of operational time” statement traceable: show the assumed mixture weights and ensure they are consistent across abstract, Table VIII (duty mapping), and the “yearly mixture” calculation.

2. **\(\gamma\) unification (0.76/0.745/0.732): mostly consistent, but still fragile due to ACK treatment and framing assumptions**  
   **Why it matters:** Your feasibility boundary (24 infeasible, 30 minimum, 35 recommended) is highly sensitive to per-slot fixed overheads. If ACK time is excluded from \(\gamma\) but included elsewhere, readers may struggle to reproduce numbers, and small inconsistencies can shift the “minimum rate” conclusion.  
   **Remedy:**  
   - Create a single “authoritative slot-time equation” box that includes *all* per-slot components, explicitly stating which are inside \(\gamma\) and which are outside (ACK mini-slot, turnarounds, sync beacon, etc.).  
   - Add a reproducibility check: for 30 kbps, show the exact arithmetic yielding \(T_{\text{slot}}=91.7\) ms and ingress \(=9078\) ms.  
   - Clarify whether framing includes ASM twice (preamble ASM + frame ASM) or whether the 120-bit “re-sync preamble” is separate from the 104-bit framing overhead. Right now this is easy to misinterpret as double counting, even if your implementation is correct.

3. **Stress-case contextualization (\(\eta_S\sim 46\%\)) is improved but still risks being read as “typical”**  
   **Why it matters:** Reviewers/readers often anchor on the largest headline number. Even with the “<1% time” qualifier, presenting \(\eta_S\) repeatedly without a strong operational anchor can undermine credibility.  
   **Remedy:**  
   - Move the “continuous-duty upper bound” framing earlier and more prominently (e.g., at first introduction of \(\eta_S\)).  
   - Provide a figure or table that shows \(\eta\) vs. \(d\) for multiple \(p_{\text{cmd}}\) values (e.g., 1.0, 0.2, 0.05) so practitioners don’t assume \(p_{\text{cmd}}=1\) during campaigns.

4. **Three-layer feasibility framework: conceptually sound, but the “MAC efficiency” layer is underspecified and could be misapplied**  
   **Why it matters:** You position feasibility as two tests (A and B), yet you also discuss “MAC efficiency” and “\(\gamma\) is not contention.” Practitioners may still confuse \(\gamma\) with MAC throughput under collisions, especially because you mention Slotted ALOHA fallback and “contention margin.”  
   **Remedy:**  
   - Explicitly define the *contract*: Test B assumes centrally scheduled TDMA with zero collisions; \(\gamma\) captures *deterministic* overhead only.  
   - Add a short “if contention exists” extension: e.g., replace \(\gamma\) with \(\gamma \cdot \rho_{\text{MAC}}\) where \(\rho_{\text{MAC}}\in(0,1]\) is an empirical MAC utilization factor (from NS-3 or measurements). This keeps your framework intact and prevents misinterpretation.

5. **DES verification value: currently too close to “confirming its own equations”**  
   **Why it matters:** In a top-tier journal, simulation should either (i) validate against independent data/tools, or (ii) reveal emergent behaviors not captured analytically. You do the latter partially (buffer tails under ON/OFF), but many DES results are essentially mean accounting checks.  
   **Remedy:**  
   - Elevate the distributional results into a clearer contribution: quantify how much buffer factor \(M\) must increase under ON/OFF vs. Bernoulli, across a sweep of \(L_{\text{on}}\) and \(d\).  
   - Alternatively, reduce emphasis on Tier-1 “DES matches means” and present DES primarily as a tail-risk estimator for coordinator buffering/handoffs.

6. **Packet-level “validation” of \(\gamma\) (Section IV-J) is not independent validation; it is standards-based parameter derivation**  
   **Why it matters:** The paper says “packet-level validation provides independent validation,” but the method is not independent of the assumed overhead model; it’s an instantiation of the same timing equation with CCSDS constants. This is fine, but it should be framed as *parameter anchoring*, not validation.  
   **Remedy:**  
   - Rename IV-J to “Standards-grounded parameterization” (you already do, mostly) and remove/avoid the word “validation” for \(\gamma\).  
   - Add a concrete plan for true validation: e.g., bench test measuring acquisition time distribution and effective throughput for burst-mode Prox-1-like frames at 24/30/35 kbps.

7. **GE/ARQ conclusions depend strongly on coherence-time regime; current treatment risks over-generalization**  
   **Why it matters:** The headline “ARQ structurally ineffective when \(\tau_c \ge T_c\)” is correct, but the assumed GE state transition once per cycle is a very coarse abstraction. Real burst errors can occur at sub-slot timescales; interleaving and coding can change the effective packet erasure process.  
   **Remedy:**  
   - Add a sensitivity subsection that varies the GE transition granularity (per-slot vs per-cycle) or models coherence with a parameter \(m\) = number of independent fades per cycle; show how ARQ effectiveness changes with \(m\).  
   - Clarify that your GE model is at the *packet-erasure layer*, after FEC, and that \(p_G,p_B\) should be interpreted as post-decoding erasure probabilities.

8. **Generalized \(\gamma\) expression: useful, but practitioner guidance needs one more step (how to measure each term and avoid double counting)**  
   **Why it matters:** Eq. (33) is only useful if engineers can map their modem’s behavior into \(T_{\text{acq}},T_{\text{guard}},O_{\text{frame}},R_{\text{FEC}}\) without ambiguity. The manuscript partially provides this, but it’s scattered.  
   **Remedy:**  
   - Consolidate the measurement protocol into a single checklist (you have it) plus a worked example with hypothetical measured P95 acquisition time and turnaround, producing \(\gamma\) and then \(R_{\text{PHY,min}}\).  
   - Explicitly warn about “effective code rate” vs nominal LDPC rate (puncturing, padding, interleaver fill).

---

# Minor Issues

1. **Potential confusion about baseline vs. \(\eta\):** You define baseline 20.5% excluded from \(\eta\), but some narrative statements compare “\(\eta\)” to “41% centralized” etc. Ensure every comparison uses either \(\eta\) consistently or \(\eta_{\text{total}}\) consistently.  
2. **Equation labeling/consistency:** In Algorithm 1, line references to “line 4” etc. don’t match the algorithmic numbering as printed; verify.  
3. **AoI statement:** “mean \(\approx T_c/2\)” is true for periodic updates with uniform observation time; for deterministic periodic sampling and immediate delivery, average AoI is exactly \(T_c/2\). Consider stating conditions (no misses, negligible delay).  
4. **Reuse factor \(R=7\):** The C/I aggregation argument is plausible but very geometry-specific; consider labeling as “order-of-magnitude” and moving detailed C/I arithmetic to an appendix.  
5. **Terminology:** “MAC efficiency” is used informally; since you are not modeling contention, consider consistently calling \(\gamma\) “slot efficiency” or “burst efficiency.”  
6. **Table VIII (duty mapping):** “Collision avoidance: \(d=1.0\) during event” is fine, but readers may misread it as typical. Consider writing \(d_{\text{event}}=1\) and \(d_{\text{year}}\ll 1\).  
7. **Thundering herd section:** Interesting, but currently disconnected from the two-test framework; either tie it to feasibility (extra traffic + airtime) or shorten.  
8. **Units/precision:** Several margins (e.g., 1,891 vs 1,888 ms) vary slightly across sections; align rounding to avoid suspicion of inconsistency.

---

## Overall Recommendation  
**Recommendation:** **Major Revision**

The manuscript is promising as an engineering sizing paper and is notably transparent about assumptions and validation gaps. Version DJ meaningfully improves workload realism via the campaign duty factor \(d\), clarifies \(\eta_S\) as a continuous-duty upper bound, and tightens the CCSDS-based \(\gamma\) parameterization. The two-test feasibility framework and the “rate ladder” are practical and likely useful to system designers working in the “low kbps per node” regime.

The main reasons for Major Revision are (i) the need to further de-risk interpretability and reproducibility of the \(\gamma\)/slot-time accounting (especially ACK/framing/acquisition decomposition), (ii) the need to strengthen the workload realism argument with more explicit operational grounding of \((d,p_{\text{cmd}})\), and (iii) the need to adjust the validation narrative so that standards-based \(\gamma\) derivation is not presented as independent validation, and the DES is positioned as tail-risk estimation rather than equation confirmation. Addressing these points would substantially increase credibility and practitioner uptake without requiring new flight data.

---

## Constructive Suggestions (ordered by impact)

1. **Add a single consolidated “Timing & \(\gamma\) contract” table/box** that lists every per-slot and per-cycle component, explicitly marking: included in \(\gamma\) vs excluded; ingress vs egress; per-slot vs per-cycle. Provide one line of arithmetic reproducing \(T_{\text{slot}}\), \(\gamma_{30}\), and 9,078 ms ingress.  
2. **Strengthen the duty-factor realism argument** with 2–3 concrete mission timelines and computed \((d,p_{\text{cmd}},q)\), plus a small sensitivity plot of \(\eta\) vs \(d\) for multiple \(p_{\text{cmd}}\).  
3. **Reframe “validation” language:** call IV-J “standards-grounded parameterization,” and explicitly label DES Tier-1 as implementation verification; elevate the tail/buffer results as the DES’s main value.  
4. **Extend GE/ARQ analysis with a coherence-granularity parameter** (e.g., GE transitions per-slot vs per-cycle, or \(m\) independent fades per cycle) to show when ARQ becomes effective and how that interacts with the 30 vs 35 kbps recommendation.  
5. **Introduce an explicit “contention factor” placeholder** (\(\rho_{\text{MAC}}\)) so practitioners can fold in NS-3 or measured utilization without breaking your framework.  
6. **Tighten consistency of \(\eta\) vs \(\eta_{\text{total}}\)** in comparisons, and reduce repetition by consolidating the feasibility explanation into one canonical location.