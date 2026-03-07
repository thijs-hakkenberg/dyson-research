---
paper: "02-swarm-coordination-scaling"
version: "dp"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-07"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript targets a real and increasingly important gap: *preliminary sizing* of intra-swarm coordination communications with explicit byte accounting and schedulability constraints. The “two-test” framing (byte budget + TDMA airtime) and the attempt to produce closed-form, practitioner-facing equations are valuable, especially because much of the constellation/satellite networking literature either (i) assumes high-rate ISLs, (ii) focuses on routing rather than coordination workload, or (iii) lacks byte-level accounting tied to a concrete MAC/PHY timing model. The paper’s novelty is strongest in the *engineering synthesis*: mapping a coordination message model into TDMA superframe feasibility with a standards-based slot timing ledger and producing a usable sizing algorithm.

That said, the conceptual novelty is incremental rather than foundational: many components (hierarchical aggregation, TDMA airtime constraints, GE channel, ARQ feasibility) are standard individually. The paper’s contribution is in unifying them into a coherent sizing workflow and validating the key “gamma” conversion.

---

## 2. Methodological Soundness  
**Rating: 4 (Good)**  
The method is generally sound for a preliminary design paper: explicit parameterization, clear separation of information-layer vs. airtime-layer constraints, and sensitivity analyses (slot structures, acquisition/guard timing, GE burstiness). The shift to CCSDS Proximity‑1–based framing and the computed \(\gamma\) values is a meaningful improvement over an ad hoc efficiency constant.

Main methodological weaknesses are: (i) some assumptions are still “hard-binding” (cold-start acquisition each slot; per-cycle GE state) without being justified as worst-case bounds vs. typical operations; (ii) the ARQ treatment mixes correlated-loss claims (“intra-cycle ARQ ineffective”) with a Test‑B ARQ sizing step that appears to assume a distribution of failures that may not match the correlation model; and (iii) the DES is described as a sanity check but is not leveraged to test *off-nominal* behaviors where closed-form equations are weakest (e.g., correlated fades + scheduling jitter + retransmissions).

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internal logic is mostly consistent, but a few places need tightening:

- The “exactly two tests” claim is directionally correct, yet the manuscript effectively introduces sub-constraints (e.g., margin thresholding, ARQ feasibility at P95, unicast staggering) that function like additional acceptance criteria. That’s fine, but it should be presented as *design rules layered on Test B*, not rhetorically dismissed as “not separate tests,” because the reader will treat them as constraints anyway.

- The campaign duty factor \(d\) is a good mechanism to address workload realism, but the mapping from mission phases to \((d,p_{\text{cmd}})\) is only lightly justified and mixes time-fraction (“active windows”) with per-cycle Bernoulli command generation in a way that can confuse interpretation. The claim that the stress bound is “<1% of operational time” is plausible but not rigorously derived from the table as written.

- The GE model is positioned as a “what-if tool,” which is appropriate; however, the specific default parameters (and especially the per-cycle state transitions) must be explicitly tied to an assumed coherence time regime and packetization timescale. Right now the paper alternates between \(\tau_c \ge T_c\) and “per-cycle transitions” without fully reconciling them.

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
The paper is well organized for an engineering sizing contribution: notation table, explicit tests, rate ladder, and a concrete algorithm. The “rate ladder” is particularly effective for readers.

Areas to improve clarity:

- Overhead accounting: baseline 20.5% excluded from \(\eta\) but included in \(\eta_{\text{total}}\) is reasonable, yet it is easy to lose track of which metric is being used in each feasibility claim. Several results cite \(\eta\) and \(\eta_{\text{total}}\) in close proximity; adding a consistent rule (e.g., “Test A always uses \(\eta_{\text{total}}\)”) would reduce ambiguity.

- Some numerical claims are scattered (e.g., “coordinator ingress demands ≈27 kbps PHY-rate at \(\gamma_{30}\)” vs. later “\(R_{\text{PHY,min}}=29.9\) kbps”). These can be reconciled, but the text should explicitly state when half-duplex fraction \(\alpha_{\text{RX}}\) is included.

---

## 5. Ethical Compliance  
**Rating: 5 (Excellent)**  
Strong reproducibility posture: code + NS-3 scenarios + datasets + tagged repository. Clear AI disclosure (ideation/editing only; no AI-generated results). This meets and exceeds typical expectations.

---

## 6. Scope & Referencing  
**Rating: 4 (Good)**  
Scope fits IEEE TAES / Adv. Space Res. as a design/sizing methodology paper. Referencing covers distributed algorithms, constellation networking, CCSDS, GE channel foundations, and AoI.

Gaps: you should cite more directly comparable work on (i) TDMA burst efficiency for short packets in space links (beyond DVB-RCS2), (ii) proximity/ISL MAC designs (including CubeSat ISL demonstrations if any public), and (iii) swarm/formation coordination comms sizing papers (even if small-scale) to more sharply position novelty.

---

# Major Issues

1. **Campaign duty factor \(d\): interpretation and quantitative grounding remain too hand-wavy**  
   - **Why it matters:** You explicitly ask the reader to accept that the 46% stress utilization is a “continuous-duty upper bound” occurring <1% of the time. If \(d\) is the mechanism that addresses workload realism (a key reviewer concern), it must be defensible and unambiguous.  
   - **Specific remedy:**  
     - Define \(d\) as *fraction of cycles in which commanding is enabled* vs. *fraction of wall-clock time in campaign state*—and ensure the stochastic model matches that definition.  
     - Provide a short derivation showing how the “<1%” statement follows from plausible mission timelines (e.g., aggregate annual commanding hours / total hours) rather than qualitative assertions.  
     - Consider adding a sensitivity plot showing feasibility metrics vs. \(d\) (not just a table), and explicitly state recommended operational envelopes (e.g., “design for \(d \le 0.1\) nominal; verify safe operation up to \(d=0.5\)”).

2. **\(\gamma\) unification (0.76 CCSDS-based) is improved but not consistently propagated across all computations and narrative claims**  
   - **Why it matters:** The paper’s key design recommendation (30 vs 35 kbps) is highly sensitive to \(\gamma\). Any residual mixing of Model S vs Model C, or of \(\gamma_{24}\) vs \(\gamma_{30}\), undermines trust. I noticed at least one potential inconsistency: Eq. (13) uses \(\gamma_{C,24}=0.761\) while the surrounding discussion and ladder emphasizes \(\gamma_{30}=0.745\). That may be intentional (example at 24 kbps), but it reads like a slip.  
   - **Specific remedy:**  
     - Add a “gamma consistency” checklist table in the main paper (not only supplement) stating: *All feasibility claims use Model C; whenever another \(\gamma\) is used, it is explicitly labeled and not used for design.*  
     - Audit every numeric capacity computed with \(\gamma\) and ensure the subscript matches the PHY rate used in that line (24/30/35).  
     - In the abstract and conclusion, ensure the quoted \(\gamma\) values correspond to the rate used for the quoted kbps numbers (e.g., “≈27 kbps at \(\gamma_{30}\)” should be clearly distinguished from “≈26.7 kbps at \(\gamma_{24}\)”).

3. **Stress-case contextualization is better, but the paper still risks readers treating \(\eta_{\text{total,stress}}\approx 67\%\) as typical**  
   - **Why it matters:** A common critique of coordination sizing papers is pessimistic workload assumptions leading to over-provisioning. You have the right mechanism (\(d\)), but the presentation still foregrounds the 46%/67% numbers repeatedly.  
   - **Specific remedy:**  
     - Reframe stress-case results as *design verification* rather than *expected operation*: e.g., label tables/figures “continuous-duty upper bound” and visually separate from nominal.  
     - Provide expected-value utilization under the mission-phase mixture (weighted by time fractions), not just per-phase values. Even a simple “example annual profile” would help.

4. **Three-layer feasibility framing (“byte budget, MAC efficiency, TDMA airtime”) is conceptually right but currently rhetorically inconsistent**  
   - **Why it matters:** You emphasize “exactly two tests,” yet also present \(\gamma\) as a quasi-layer (and provide lookup tables, alternative slot structures, NS-3 validation). Reviewers will ask: is \(\gamma\) merely a conversion factor, or a third feasibility gate? In practice it behaves like a third gate because it embeds hardware timing assumptions.  
   - **Specific remedy:**  
     - Explicitly present a *three-layer model* but keep *two acceptance inequalities*:  
       1) information bytes \(\rightarrow\) Test A,  
       2) time budget \(\rightarrow\) Test B,  
       with \(\gamma\) as the mapping from bytes to time under a specified slot design.  
     - Add a short paragraph: “\(\gamma\) is not a separate feasibility criterion, but it is a design-dependent parameter whose uncertainty must be bounded; we treat it via (i) CCSDS ledger, (ii) NS-3 validation, (iii) sensitivity.”

5. **DES “verification” provides limited incremental value as currently positioned**  
   - **Why it matters:** Stating “DES reproduces analytical means (<0.1%)” can read as self-validation because the DES shares assumptions and aggregation level. The paper claims independent validation via NS-3, which is stronger; the DES portion should either be leveraged for something the equations cannot do, or de-emphasized.  
   - **Specific remedy:**  
     - Either (a) remove/shorten the DES verification claim in the main text and move details to supplement, or (b) use DES to test scenarios where closed-form is weak: correlated burst losses across cycles, queueing at coordinator under variable arrivals, election/re-association bursts, or command unicast staggering interactions.  
     - If kept, clearly state what the DES checks that equation-level review would not (e.g., implementation errors in accounting, scheduling edge cases).

6. **Packet-level validation (Section IV-J) is a good step, but the independence and mapping need sharper articulation**  
   - **Why it matters:** The NS-3 results are central to credibility of \(\gamma\) and the 35 kbps recommendation. However, NS-3 still uses timing you prescribe (guard, acquisition distribution, framing bits), and the channel model is NS-3’s BurstErrorModel rather than a physical model. The validation is still meaningful, but you should be explicit about what is and is not independently “emergent.”  
   - **Specific remedy:**  
     - Add a concise mapping table: analytical parameters ↔ NS-3 implementation knobs (payload size, FEC expansion, framing bits, guard, acquisition, turnaround).  
     - Clarify whether NS-3 “deadline miss” is measured as event overrun of the superframe schedule, or as packet not delivered by end-of-cycle, and ensure the definition matches Test B’s miss concept.  
     - Consider adding one additional validation point that is less “parameter-matched”: e.g., vary packet size (128/256/512 B) and show \(\gamma\) scaling trend matches, not just absolute values.

7. **ARQ sizing under GE correlation: potential mismatch between stated channel regime and Binomial/P95 computation**  
   - **Why it matters:** Algorithm 1 line 10 uses “Binomial\((k_c-1, \pi_B p_B)\)” for P95 failed members. Under strongly correlated losses with \(\tau_c \ge T_c\), failures are not i.i.d. Bernoulli across nodes unless nodes experience independent fades (which is not discussed). Also, if the GE state is shared cluster-wide (e.g., coordinator interference or geometry), the distribution is closer to a mixture model, not Binomial.  
   - **Specific remedy:**  
     - State explicitly whether GE is per-link independent across members or a shared cluster state.  
     - If independent per-link: justify Binomial approximation and define \(\pi_B\).  
     - If shared: replace Binomial with a two-mode mixture: with prob \(\pi_B\) many fail; with prob \((1-\pi_B)\) few fail, and recompute P95 retx demand accordingly (likely much worse).  
     - This is important because the “ARQ infeasible at 30 kbps, feasible at 35 kbps” hinge depends on tail demand.

8. **Generalized \(\gamma\) expression usefulness: good idea, but needs a clearer “how to use” recipe and bounds**  
   - **Why it matters:** Practitioners will want to plug in their own framing/FEC/guard/acquisition. Eq. (10) is fine, but the paper should provide a robust procedure and highlight dominant terms and typical ranges, otherwise the lookup table becomes the only usable artifact.  
   - **Specific remedy:**  
     - Provide a short step-by-step “gamma computation recipe” in the main text (inputs, units, rounding/ceiling rules, what is FEC-encoded).  
     - Add bounds: e.g., “for 256 B packets at 30–35 kbps, \(\gamma\in[0.66,0.81]\) for \(T_g\in[4.7,8]\) ms and \(T_a\in[0,10]\) ms.”  
     - Clarify rounding/ceiling: you use a ceiling in the table footnote but not in Algorithm 1 line 5; unify.

---

# Minor Issues

1. **Potential inconsistency:** Eq. (13) labels \(\gamma_{C,24}=0.761\) while the computed example is presented near 30 kbps contexts; ensure the subscript and value match the intended rate.  
2. **Algorithm 1:**  
   - Line 10 uses \(\pi_B p_B\) without defining \(\pi_B\) in the algorithm inputs (it appears later in text).  
   - Line 12 “Fallback to inter-cycle recovery” should specify what feasibility criterion becomes (e.g., allowed AoI tail / maximum consecutive misses).  
3. **Definition of “deadline miss”:** you define it as ingress phase overrun causing coordinator to miss that cycle’s reports entirely. In NS-3, confirm this is exactly what is measured (not simply packet error/loss).  
4. **Turnaround times:** Table 7 includes “TX/RX turnaround ×2 = 4 ms” but earlier guard/acquisition dominate; clarify whether turnaround is included in guard or separate and whether it is hardware-dependent.  
5. **Fleet-level reuse:** the reuse factor \(R=7\) is repeatedly called “conservative,” but without an interference/geometric derivation it reads aspirational. Consider softening language (“plausible under directional antennas”) and keep “conditional” prominent (you do state conditionality, which is good).  
6. **Typographic/LaTeX:** Fig. 8 includegraphics missing extension in `fig-cross_cycle_recovery` (no `.pdf`), may break compilation depending on settings.  
7. **Baseline telemetry (20.5%)**: give one sentence on where 20.5% comes from (status size/rate math) to avoid it feeling like a magic constant.

---

## Overall Recommendation  
**Recommendation:** **Major Revision**

The paper is close to publishable in spirit: it offers a clear sizing framework, a credible standards-based \(\gamma\) ledger, and a meaningful independent validation attempt via NS-3. The main reasons for Major Revision are not formatting; they are about tightening the logical contract between assumptions and conclusions—especially around (i) workload realism via \(d\), (ii) consistent and audited application of the CCSDS-based \(\gamma\), and (iii) ARQ tail sizing under correlated loss and whether the Binomial P95 step is valid under the stated GE regime.

If the authors address the above with a focused consistency audit, clearer definitions, and one or two additional validation/sensitivity results that reduce dependence on “matched assumptions,” the manuscript could become a strong, practitioner-relevant design reference.

---

## Constructive Suggestions (ordered by impact)

1. **Add a one-page “Assumptions → Outputs” contract**: a table listing the assumptions (slot structure, acquisition model, per-link vs shared GE, half-duplex model, definition of miss) and which outputs depend critically on each (30/35 kbps boundary, margin, ARQ viability).  
2. **Audit and unify \(\gamma\) usage**: ensure every numeric result cites the exact \(\gamma_R\) used; align Algorithm 1 rounding with Eq. (10) and Table 5 footnote; remove any lingering “0.85-era” language if present in supplement.  
3. **Strengthen \(d\) grounding**: provide a quantitative example mission timeline and compute implied \(d\); separate “continuous-duty bound” from “expected duty.”  
4. **Fix ARQ tail modeling under GE**: explicitly define correlation structure across members; replace Binomial if needed; show sensitivity of P95 retx demand to correlation assumptions (this can be a small figure).  
5. **Make NS-3 validation harder to dismiss**: add one additional independent sweep (packet size or guard/acquisition) and show the analytical trend matches; add a parameter mapping table and exact miss definition alignment.  
6. **Reposition DES**: either shorten it or use it to test a scenario the equations don’t cover (e.g., bursty command campaigns + election bursts + correlated fades).  
7. **Clarify the “two tests vs three layers” narrative**: present \(\gamma\) as the byte→time mapping with uncertainty bounds rather than arguing it is “not a third check,” which can read defensive.

If you want, I can also provide a targeted “consistency checklist” for all places where \(\gamma\), \(R_{\text{PHY}}\), \(\alpha_{\text{RX}}\), and margins are computed, to help you systematically eliminate internal mismatches before resubmission.