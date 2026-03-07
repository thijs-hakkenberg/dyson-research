---
paper: "02-swarm-coordination-scaling"
version: "dn"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-07"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript tackles a practically important and under-served problem: *parametric, closed-form sizing* of coordination traffic and TDMA schedulability for large autonomous swarms, with explicit byte accounting and standards-based framing. The two-test feasibility framing (byte budget + TDMA airtime) is a useful engineering abstraction that can be applied early in design. The explicit separation of “information rate” vs “PHY rate via γ” is valuable for avoiding common confusion in early link/MAC sizing.

Novelty is strongest in (i) the explicit per-cluster design equations with a clear “rate ladder,” (ii) the standards-grounded γ computation and sensitivity, and (iii) the attempt at independent packet-level validation. The work is less novel in the underlying ingredients (TDMA airtime accounting, GE channel, ARQ feasibility), but the combination and packaging as a practitioner-oriented sizing method is a meaningful contribution.

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The analytical framework is generally sound for a first-order sizing study, and the paper is careful to state that DES agreement validates implementation rather than truth. The campaign duty factor \(d\) is a reasonable mechanism to address workload realism *if* anchored to mission scenarios and if its mapping to command processes is internally consistent.

However, several modeling choices remain somewhat ad hoc or insufficiently justified for top-tier archival publication: (a) the definition and constancy of the 1 kbps “per-node allocation” as a policing abstraction while the physical channel is a shared 35 kbps burst channel; (b) the GE parameterization and especially the per-cycle transition assumption; (c) the ARQ modeling as “\(M_r\) extra slots” without a clearly derived mapping from loss process → expected retransmission demand distribution under the actual schedule and ACK policy; and (d) the fleet-level reuse factor \(R\) being asserted as “provisional” but then used to claim non-binding fleet scaling.

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internal logic is mostly consistent, and the paper now explicitly contextualizes the stress case (46% overhead) as a continuous-duty upper bound occurring <1% of time, which is an improvement over earlier “stress-case realism” concerns.

That said, there are still logical pressure points:
- The “three-layer feasibility” narrative is slightly unstable: the manuscript says there are two tests, yet repeatedly introduces derived checks/transformations (raw conversion via \(1/\gamma\), half-duplex via \(\alpha_{\text{RX}}\), ARQ time) that function like additional constraints. This is not fatal, but the boundary between “test” and “derived bound” needs to be made unambiguous and consistently reflected in the algorithm and results.
- The AoI tail argument tied to \(\epsilon\) is not fully coherent: the text uses \(\epsilon^m\) but then states \(P(\text{AoI}>3T_c)=\epsilon^2\) (off-by-one style ambiguity). More importantly, the AoI requirement is not cleanly connected to the *deadline miss definition* used in Test B (miss rate ≤1%) under correlated loss.
- The half-duplex factor \(\alpha_{\text{RX}}\) is treated as both an output and an input to PHY sizing (Eq. 15), which risks circularity unless the computation procedure is explicitly fixed-point/iterative and shown to converge.

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
The paper is well organized, notation is mostly clear, and the “rate ladder” table is effective. The explicit statement that Model C is primary and that Model S is “not for design” is good. The manuscript is also commendably transparent about what DES V&V does and does not mean.

Areas needing improvement: some definitions are scattered (e.g., what exactly constitutes the “baseline 20.5%” and how it is encoded in Test A vs Test B), and a few key equations/parameters (e.g., exact \(T_{\text{cmd}}, T_{\text{hb}}, T_{\text{sync}}\), ACK structure) are referenced but not fully specified in the main text, making it hard to reproduce the superframe budget without the supplement.

## 5. Ethical Compliance  
**Rating: 5 (Excellent)**  
Strong data/code availability statement with a tagged repository, toolchain versions, and explicit AI disclosure. This meets (and exceeds) typical reproducibility expectations, assuming the repository indeed contains the scripts to regenerate all figures/tables and the NS-3 scenario is runnable as claimed.

## 6. Scope & Referencing  
**Rating: 4 (Good)**  
The paper is in-scope for IEEE TAES / space networking/avionics autonomy audiences. Referencing is generally appropriate (CCSDS, DVB-RCS2, DTN/CGR, AoI). A gap remains in citing prior analytical TDMA sizing work in satellite return links and short-burst efficiency studies beyond DVB-RCS2, and in citing CCSDS Proximity-1 implementation guidance/mission usage examples (if available publicly) to strengthen the “CCSDS-grounded” claim.

---

# Major Issues

1) **Test A vs Test B vs “derived checks” needs formal tightening (currently reads like 2 tests + implicit third).**  
**Why it matters:** The central claimed contribution is a “two-test feasibility framework.” If readers perceive three independent constraints (byte budget, MAC efficiency, TDMA airtime), the conceptual clarity and novelty are diluted, and practitioners may misapply the method.  
**Remedy:**  
- Add a short formal subsection that defines *exactly* what is a feasibility test and what is a unit conversion or derived bound.  
- Consider explicitly naming the layers as:  
  - **Layer 1 (Information budget):** \(\eta_{\text{total}}\le 1\).  
  - **Layer 2 (Airtime schedulability):** time inequality with \(T_{\text{slot}}(\gamma)\).  
  Then state unambiguously that “MAC efficiency via \(\gamma\)” is *part of Layer 2* because it defines \(T_{\text{slot}}\).  
- Update Algorithm 1 to reflect this: compute \(T_{\text{slot}}\) directly; do not present \(C_{\text{TDMA}}=C_{\text{info}}/\gamma\) as a quasi-independent feasibility gate.

2) **Campaign duty factor \(d\) is helpful but still under-anchored; mapping in Table III mixes two different notions (duty vs command probability) without a clear stochastic model.**  
**Why it matters:** A key reviewer concern you explicitly flag is “workload realism.” If \(d\) is not tied to an explicit process model, the same \((d,p_{\text{cmd}})\) can correspond to very different burstiness and hence different TDMA/ARQ feasibility and AoI tails.  
**Remedy:**  
- Define a simple workload process: e.g., a two-state mission process (campaign active/inactive) with duty factor \(d\) as steady-state fraction of active state, and within active state commands occur Bernoulli per cycle with probability \(p_{\text{cmd}}\).  
- Then derive expected command bytes per cycle and variance (or at least clarify whether you assume smoothing across cycles).  
- For the “<1% of operational time” claim for stress-case: provide a defensible argument (e.g., based on representative mission timelines) or rephrase as an illustrative assumption rather than a result.

3) **Gamma unification (0.76 CCSDS-based) appears mostly consistent, but there are still multiple γ values and rate points used inconsistently (24/30/35) and one place where the narrative risks confusion.**  
**Why it matters:** Your PHY recommendation hinges on γ. Any inconsistency (even just presentation-wise) undermines confidence.  
**Remedy:**  
- Create a single table in the main text listing \(\gamma_C(R_{\text{PHY}})\) for the discrete rates used (24/30/35) and the assumed \(S\), \(R_{\text{FEC}}\), \(O_{\text{frame}}\), \(T_{\text{guard}}\), \(T_{\text{acq}}\).  
- Ensure every computed quantity uses the matching γ: e.g., Eq. (16) uses \(\gamma_{C,24}\) but Table VI rate ladder uses \(\gamma_{30}\). That is fine, but explicitly state why (e.g., “Eq. 16 illustrates conversion at 24 kbps; design point uses 30/35”).  
- Remove or further quarantine Model S so it cannot be mistaken as a viable design assumption (you already warn, but it still occupies equation real estate).

4) **Stress-case \(\eta_S\approx 46\%\) is now contextualized as continuous-duty, but its *operational interpretation* remains unclear: does it represent cluster-wide broadcast commanding every cycle? If so, why is that a meaningful upper bound?**  
**Why it matters:** The paper’s conclusions about feasibility under “stress” are only meaningful if the stress case corresponds to a plausible worst-case safety scenario (e.g., conjunction avoidance) rather than an artificial saturation workload.  
**Remedy:**  
- Explicitly define the stress workload in operational terms: command size, recipients (broadcast/unicast), frequency, and duration.  
- Provide at least one “safety-critical burst” scenario (e.g., CA event) and show its implied \(d\) and time-window, contrasting it with the continuous-duty bound.

5) **DES verification is honest about its limitations, but it still consumes space without adding much scientific value beyond sanity-checking.**  
**Why it matters:** In a top-tier journal, simulation should either (i) validate assumptions against a higher-fidelity model, (ii) explore regimes not analytically tractable, or (iii) quantify distributions/tails that matter to requirements. “Matches the mean” is not strong.  
**Remedy:**  
- Either compress DES V&V to a brief statement and move details to supplement, *or* leverage DES to produce something the equations do not: e.g., distribution of coordinator queueing delay under bursty command arrivals, or tail probability of cycle overrun under stochastic acquisition and losses.  
- If coordinator processing capacity \(\mu_c\) is included, show at least one result where it binds (or remove it from the main model).

6) **Packet-level validation (Section IV-J) is a step forward, but it is not fully “independent validation” of the key claim unless the TDMA mechanism itself is implemented independently (not just timing additions around PointToPoint).**  
**Why it matters:** The main risk is that NS-3 is being used as a time-accounting engine rather than as a MAC/PHY model. If the TDMA schedule is externally enforced and losses are injected, NS-3 may simply reproduce the same accounting with minor discretization differences.  
**Remedy:**  
- Clarify exactly what is implemented in NS-3: how slots are scheduled, how half-duplex turnaround is modeled, whether packets can overlap, and how guard/acquisition are enforced (e.g., via event scheduling).  
- Add one validation metric that is not a direct restatement of γ, such as: observed inter-arrival jitter at coordinator, fraction of slots that collide/overrun due to acquisition jitter, or measured “effective slot time” distribution vs analytical deterministic assumption.  
- If feasible, implement (or at least describe) a minimal custom TDMA NetDevice/MAC in NS-3 to demonstrate independence at the MAC level, not only at the packet-event level.

7) **Generalized γ expression: usefulness is plausible, but practitioners need a clear recipe and boundaries (what changes γ vs what changes payload size vs what changes slot count).**  
**Why it matters:** The paper claims practitioner utility; γ is central. Without a clear “how to plug in your radio,” readers may not translate the method.  
**Remedy:**  
- Provide a concise “γ worksheet” in the main text: list required radio/standard parameters and how to compute each term in Eq. (13).  
- State boundary conditions: single-packet-per-slot assumption, cold-start vs tracking, whether framing is FEC-coded, and how multi-packet slots alter \(T_{\text{acq}}\) amortization.

---

# Minor Issues

1) **AoI tail derivation:** clarify the exponent and off-by-one: if deadline miss probability per cycle is \(\epsilon\), then \(P(\text{no update for }m\text{ cycles})\) is \(\epsilon^m\) (or \(\epsilon^{m-1}\)) depending on definition. Make consistent with the stated \(P(\text{AoI}>3T_c)=\epsilon^2\).  

2) **Algorithm 1 circularity:** \(\alpha_{\text{RX}}\) is computed from \(T_{\text{ing}}\), but Eq. (15) uses \(\alpha_{\text{RX}}\) to compute \(R_{\text{PHY,min}}\). Explicitly state that you iterate on \(R_{\text{PHY}}\) and recompute \(\gamma\), \(T_{\text{slot}}\), \(T_{\text{ing}}\), \(\alpha_{\text{RX}}\) until feasible.  

3) **Define \(T_{\text{cmd}}, T_{\text{hb}}, T_{\text{sync}}\) in the main text** (even if values are in supplement), because Table VIII and Eq. (21) depend on them.  

4) **GE model timing:** you state “per-cycle state transitions” and discuss coherence time \(\tau_c\). Provide an explicit mapping: when \(\tau_c\ge T_c\), you hold state fixed for the cycle; when \(\tau_c\ll T_c\), you approximate iid per packet. Right now it reads like a conceptual aside rather than a defined model switch.  

5) **NS-3 framing difference:** you say NS-3 uses 88 bits and your model uses 104 bits; briefly enumerate the 104-bit fields in Model C in the main text (or cite CCSDS section) so readers can audit the ledger without the supplement.  

6) **Fleet reuse factor \(R\):** since it is provisional, tone down “non-binding” claims or explicitly label them as conditional on \(R\) validated by RF analysis.  

7) **Table II architecture levels:** Fig. 1 caption says Cluster (10–100) then Node (50–100) which is confusing (nodes per cluster vs nodes per coordinator). Ensure consistent fan-out terminology.  

8) **Units and rounding:** a few places mix kbps and ms with rounded values (e.g., 91.7 ms slot) without showing the underlying computation; minor, but add one line indicating the exact slot-time formula used for Table VIII.

---

# Overall Recommendation  
**Recommendation:** **Major Revision**

The manuscript is promising and closer to publishable form than many early-stage “design equation” papers: it is explicit about assumptions, provides a clear sizing narrative, and (importantly) includes code/data availability and an AI disclosure. The campaign duty factor \(d\) is a constructive mechanism to address workload realism concerns, and the updated CCSDS-based γ (0.73–0.76) with explicit decomposition is a substantive improvement that makes the PHY recommendation more defensible. The stress-case is also better contextualized as a continuous-duty upper bound rather than a typical operating point.

However, for a top-tier archival venue, the paper still needs tightening in three critical areas: (1) formal clarity of the feasibility framework (two tests vs implicit third layer), (2) a more rigorous and explicit stochastic workload model underpinning \(d\) and command processes, and (3) strengthening the claim of “independent validation” by clarifying what NS-3 truly validates beyond time accounting and by adding at least one additional validation metric or MAC-level independence. Addressing these will materially improve credibility and practitioner utility without requiring an entirely new study.

---

# Constructive Suggestions (ordered by impact)

1) **Rewrite the feasibility framework section to be formally watertight**: two tests only; show where γ and \(\alpha_{\text{RX}}\) enter Test B; present the “rate ladder” as an explanatory decomposition, not additional constraints.

2) **Define an explicit stochastic model for workload and for \(d\)** (campaign on/off + per-cycle command Bernoulli), and use it to justify Table III values and the “<1% time” stress contextualization.

3) **Strengthen NS-3 validation** by (i) fully specifying the TDMA enforcement mechanism, (ii) adding a metric that probes distributional effects (slot overrun probability, effective slot-time distribution, or coordinator receive-time jitter), and (iii) clarifying what parts are truly independent of the analytical model.

4) **Provide a practitioner “γ worksheet”** in the main text: required parameters, how to compute each time component, and common variants (tracking acquisition, multi-packet slots). This will directly increase the paper’s utility.

5) **Use DES to produce at least one non-trivial distributional result** (tail of cycle margin consumption under stochastic acquisition/loss; or coordinator queue delay if \(\mu_c\) is kept). Otherwise, compress DES discussion.

6) **Audit and standardize γ usage throughout** with a single main-text table and consistent references (γ24/γ30/γ35), ensuring no feasibility claim relies on Model S.

7) **Clarify AoI/deadline-miss linkage** and correct exponent/off-by-one issues; explicitly address correlated loss in GE when interpreting \(\epsilon\) as a safety metric.

If the authors implement the above, the work has a credible path to acceptance as a practical, standards-aware sizing methodology for hierarchical swarm coordination links.