---
paper: "02-swarm-coordination-scaling"
version: "cy"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-05"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript targets an important and under-served problem: *parametric sizing* of coordination traffic and MAC/TDMA feasibility for very large spacecraft swarms under tight per-node bandwidth allocations. The strongest contribution is the explicit separation between (i) information-byte budget (Test A) and (ii) TDMA airtime feasibility with a standards-anchored slot-efficiency parameterization (Test B), producing a practical “rate ladder” and sizing workflow (Algorithm 1). The work is more “engineering design equations” than “new theory,” but that is appropriate for T-AES/space systems design audiences.

Novelty is moderate-to-high in the *combination* of: closed-form traffic accounting, explicit coordinator ingress bottleneck identification, and a CCSDS-grounded γ model used consistently to drive a concrete PHY-rate recommendation. The paper is appropriately candid about validation gaps.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The analytical accounting is generally coherent and the two-test framework is a sensible decomposition. The slot-efficiency derivation (Eq. 31 / Eq. 33 in your numbering) is a solid step forward versus an arbitrary constant γ, and the explicit “Model C vs Model S” separation reduces the risk of optimistic conclusions.

However, several methodological choices materially affect conclusions and need strengthening: (a) the GE coherence assumption is set at the cycle level, which predetermines the “ARQ is ineffective” narrative; (b) the TDMA “slot-sim” appears deterministic and single-cluster, with limited exploration of schedule robustness (clock error distributions, acquisition variability per slot, etc.); (c) the DES is primarily a verification tool and its incremental value is narrower than the paper sometimes implies. These are fixable with targeted additional experiments and clearer framing.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internal logic is mostly consistent, and the manuscript explicitly distinguishes verification vs validation—good. The duty-factor model *does* address the earlier “workload realism” concern better than many swarm comms papers: stress-case is clearly labeled as continuous-duty upper bound, and you provide a mixture calculation showing it occurs <1% of time.

Remaining validity concerns are about boundary conditions and double-counting / hidden coupling:  
- The “three-layer feasibility framework” is claimed at times, but the boxed definition correctly states **two tests** (A and B) with γ as a parameter inside B. Elsewhere, the “rate ladder” and “raw conversion” risk being interpreted as a third check. This needs tightening so readers don’t misapply steps.  
- The half-duplex partitioning via α_RX being “derived from schedule” is good, but then it is used again as a multiplicative factor in the heuristic lower bound. You warn against double application, yet the manuscript still mixes “necessary condition” and “minimum sufficient” language in ways that could confuse practitioners.  
- Some numeric statements (e.g., “CCSDS default ~28 kbps” vs Table values showing 30 kbps minimum feasible) need reconciliation: is 28 kbps from the heuristic alone while full schedule says 30? If so, state explicitly.

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
Overall structure is strong: clear notation table, explicit test definitions, and a useful “claim map by evidence tier.” The “Model C primary / Model S bound” disclaimer is prominent and helpful. Tables (rate ladder, feasibility table, γ decomposition) are practitioner-friendly.

Clarity issues are mostly about *narrative consistency* and reducing cognitive load: the paper sometimes repeats the same concept (γ as parameter vs layer; verification vs validation) in multiple places, yet still leaves room for misinterpretation. Also, the paper is long and occasionally reads like a combined report + paper; some trimming or moving material to an appendix would improve readability for T-AES.

---

## 5. Ethical Compliance  
**Rating: 5 (Excellent)**  
Strong reproducibility posture: code and tag provided, environment specified, and AI assistance disclosed with appropriate scope limitations. The manuscript is candid about the lack of external validation and does not overclaim.

One suggestion: include a short “reproducibility checklist” (inputs, scripts to regenerate key figures/tables, random seeds) in the repository README and cite it.

---

## 6. Scope & Referencing  
**Rating: 4 (Good)**  
References cover distributed algorithms, swarm robotics, DTN/space networking, CCSDS, and AoI. For a T-AES audience, you are mostly in-scope. The DVB-RCS2 analogy is a reasonable plausibility bound, but you should more explicitly delineate which aspects transfer (burst framing overhead) and which do not (acquisition dynamics, Doppler regime, terminal classes).

Potential missing/underused literatures:  
- Deterministic real-time scheduling / network calculus applied to TDMA superframes (you cite Le Boudec but don’t leverage it for bounds).  
- Classic satellite TDMA/DAMA analyses (beyond DVB-RCS2) that could support guard/acquisition modeling choices.  
- MAC-level modeling for half-duplex TDMA with retransmissions (even if only to justify why NS-3 is future work).

---

# Major Issues

1) **γ “unification” and consistent application still has a few leak paths**  
**Why it matters:** Your primary decision (30 kbps minimum, 35 kbps recommended) is sensitive to γ and to whether Model S results are accidentally used as evidence. Even with strong disclaimers, any inconsistency will undermine trust.  
**Where it shows:** Table IV-D (ARQ×TDMA coupling) is *Model S only* yet is used to argue about coupling generally; elsewhere, 24 kbps infeasibility is a Model C conclusion. The text sometimes blends these.  
**Remedy:**  
- Add a short “γ usage audit” table listing every place γ appears and which model (C/S) is used, and confirm all design claims use Model C.  
- For Table IV-D, either (a) replicate the coupling experiment under Model C at 30/35 kbps to show coupling under the **recommended** timing model, or (b) reframe Table IV-D as purely pedagogical and avoid using it as supporting evidence for recommendations.

2) **The GE coherence-time assumption makes the ARQ conclusion partly tautological**  
**Why it matters:** You correctly state “27% intra-cycle recovery is a direct consequence of per-cycle GE coherence assumption,” but then ARQ infeasibility is used to motivate the 35 kbps recommendation under slow-mixing. Readers may view this as circular unless you explore intermediate coherence regimes.  
**Remedy:**  
- Extend the channel model to allow GE transitions at sub-cycle granularity or introduce a parameter \(m\) = number of independent channel states per cycle. Show delivery vs airtime margin for \(m \in \{1,2,5,10\}\).  
- Alternatively, keep GE per-cycle but add a second model: i.i.d. per retransmission attempt (fast mixing) vs per-cycle (slow mixing), and quantify the boundary in terms of \(\tau_c/T_c\). You already discuss this qualitatively; add quantitative curves.

3) **Three-layer feasibility wording conflicts with the (correct) two-test framework**  
**Why it matters:** Practitioners will apply the sizing procedure. If they interpret “byte budget, MAC efficiency, TDMA airtime” as three independent checks, they may double-count γ or apply the heuristic incorrectly.  
**Remedy:**  
- Standardize language: explicitly define **two tests** only; present “MAC efficiency (γ)” as a conversion inside Test B.  
- In Algorithm 1 and the boxed framework, add a one-line warning: “Do not apply \(C_{\text{coord,info}}/\gamma\) as a separate feasibility test; it is embedded in the airtime computation.”

4) **Campaign duty factor \(d\) is improved, but workload realism still depends on unvalidated command model parameters**  
**Why it matters:** The central claim “routine η ≈ 5–10%” depends on assumed command size (512 B), \(p_{\text{cmd}}\), and whether commands are broadcast vs unicast. The mapping table is helpful, but it is still largely speculative.  
**Remedy:**  
- Provide a sensitivity plot: η vs \((d, S_{\text{cmd}}, p_{\text{cmd}})\) for a few realistic regimes (e.g., orbit raising vs station keeping vs CA) and explicitly show ranges where η crosses key thresholds (e.g., 30%, 50%, 100%).  
- Clarify whether \(p_{\text{cmd}}=1\) during “on” cycles is realistic for each phase, or whether command batching is more likely.

5) **DES “distributional value” is plausible but under-quantified and not clearly separated from traffic model assumptions**  
**Why it matters:** You state the DES’s “sole non-tautological contribution” is tail/buffer sizing under correlated campaigns. But the buffer rule (1.30× etc.) is highly dependent on the chosen ON/OFF process and correlation scope.  
**Remedy:**  
- Add at least one additional burstiness model (e.g., heavy-tailed ON durations or Markov-modulated with different \(L_{on}\) distributions) to show robustness—or explicitly label the buffer multipliers as *example outputs for one assumed process*, not a general rule.  
- Provide the actual overflow probability vs buffer size curves (not only CDF of ingress bytes).

6) **Packet-level validation (Section IV-J) is still not independent validation; strengthen what it *does* validate**  
**Why it matters:** You are careful in wording, but reviewers will still ask: “What is validated?” Currently it is “standards-based parameter estimate,” which is essentially a deterministic calculation.  
**Remedy:**  
- Recast IV-J as “standards-anchored parameterization” and remove any “validation” language from headings.  
- If feasible, add a minimal independent check: e.g., implement a bit-level framing encoder/decoder for the Prox-1-like structure and measure achieved γ in simulation including preamble detect/acquisition timing distributions. Even a synthetic acquisition distribution would be more “independent” than algebra.

7) **Generalized γ expression usefulness: good start, but practitioners need a clearer recipe and typical ranges**  
**Why it matters:** Eq. (γ_time) is one of the most reusable contributions, but only if users can plug in correct parameters.  
**Remedy:**  
- Add a short “parameter sourcing” table: where to obtain \(T_{acq}\), \(T_{turn}\), framing overhead, whether framing is FEC-coded, etc., for CCSDS Prox-1 and for a generic custom modem.  
- Provide a small worked example for two alternative modem architectures (burst reacquire vs continuous tracking) showing resulting γ and recommended rate.

---

# Minor Issues

1) **Numeric consistency:** “CCSDS default ~28 kbps” vs rate-feasibility table showing 30 kbps minimum—clarify that 28 kbps is heuristic-only and schedule-level minimum is 30.  
2) **Notation clarity:** α_RX is described as “derived from schedule” but also given as 0.908 “rate-dependent” in the notation table; consider removing the fixed value from notation table or explicitly stating it is for 30 kbps, \(M_r=0\).  
3) **Guard/ACK accounting:** Footnote in Table “superframe” claims ACK fits in jitter sub-slot; this is a subtle and important timing claim—either justify with a diagram or move to an appendix with explicit timing offsets.  
4) **Cluster diameter assumption:** 500 km drives propagation uncertainty; provide a short justification or sensitivity (e.g., 200/500/1000 km).  
5) **Mesh baselines:** sectorized mesh “3.2% coverage” is unclear—coverage of what metric? Define precisely.  
6) **Centralized baseline:** the M/D/c capacity bound is compute-only; explicitly state that comms constraints dominate in real systems so this baseline is illustrative.  
7) **Figure references:** ensure all figures compile with correct extensions (one figure lacks .pdf in includegraphics).  
8) **Typos/wording:** several places use “validated” where “anchored/parameterized” is more accurate (esp. IV-J, abstract).  
9) **Algorithm 1:** line computing \(L_{cmd}\) uses \(T_c - T_{ing}\) but earlier you use \(T_c(1-\alpha_{RX})\) including egress overhead; ensure consistent inclusion of egress components.  
10) **Repository tag:** include a DOI/Zenodo archive if possible for long-term access (common in IEEE expectations now).

---

## Overall Recommendation  
**Recommendation:** **Major Revision**

The manuscript is promising and closer to publishable than many large-swarm coordination papers because it (i) makes explicit feasibility tests, (ii) anchors TDMA slot efficiency to CCSDS framing rather than assuming optimistic MAC efficiency, (iii) introduces a duty-factor \(d\) that meaningfully addresses workload realism, and (iv) is unusually transparent about verification vs validation. The “rate ladder” and γ-conditional lookup are particularly valuable for early design sizing.

The main blockers are not formatting but *scientific defensibility and practitioner safety*: the ARQ conclusions are too dependent on a modeling choice (cycle-coherent GE), the “two tests vs three layers” messaging needs to be made unambiguous to prevent misapplication, and the evidence for coupling/35 kbps recommendation should be demonstrated under Model C (not only Model S pedagogical cases). Tightening these elements would substantially improve credibility and impact.

---

## Constructive Suggestions (ordered by impact)

1) **Re-run the ARQ×TDMA coupling study under Model C at 30 and 35 kbps**, and report miss rates and margin consumption for \(M_r \in \{0,1,2\}\) under at least two coherence regimes (slow vs fast).  
2) **Add a coherence-granularity parameter** (states-per-cycle) or a sub-cycle GE transition model and show where intra-cycle ARQ becomes beneficial.  
3) **Unify feasibility language**: two tests only; γ is inside Test B. Add a prominent “common misapplication” box.  
4) **Strengthen duty-factor realism** with a compact sensitivity analysis over \(d, p_{cmd}, S_{cmd}\) and broadcast/unicast fraction \(q\), and tie each regime to one mission phase example.  
5) **Make IV-J a parameterization section, not “validation,”** or add an actually independent check (even synthetic acquisition-time distributions) to justify γ variability and its impact.  
6) **Quantify DES tail value** by adding overflow probability vs buffer size curves and at least one alternative burst model; otherwise downgrade claims about general buffer sizing rules.  
7) **Add a practitioner “how to measure γ” recipe** with explicit measurement points and logging requirements, aligned with your validation roadmap.

If these are addressed, the paper could become a strong design-equations reference for hierarchical swarm coordination under constrained RF coordination channels.