---
paper: "02-swarm-coordination-scaling"
version: "co"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-03"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript’s core contribution—closed-form “rate ladder” sizing equations that decompose feasibility into (i) message-layer byte budget and (ii) TDMA airtime schedulability, and that explicitly surfaces the *coordinator ingress* bottleneck—is valuable and relatively uncommon in the swarm/constellation literature. The paper is also unusually explicit about what is and is not validated, which is commendable.  

That said, the novelty is partly *packaging and synthesis* rather than fundamentally new theory: much of the queueing/AoI/GE machinery is standard, and the DES largely verifies its own accounting. The strongest “new” engineering insight is the identification of the 24→30→35 kbps transition *when CCSDS-grounded framing is included* and the explicit ARQ×TDMA coupling result. To reach top-tier “high impact,” the paper needs clearer practitioner-facing generalization (what a designer can do with the equations beyond this one parameter set) and stronger independence in validation.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The two-layer framework is methodologically sensible: separating byte budget feasibility (Layer 1) from time-domain schedulability (Layer 2) is the right decomposition, and the manuscript repeatedly warns against double-counting via \(1/\gamma\), which addresses a common pitfall. The CCSDS Proximity-1 anchoring of \(\gamma\) is a methodological improvement over earlier “assumed” efficiencies.

However, several modeling choices remain only weakly justified for a sizing paper that makes a concrete 35 kbps recommendation: (i) the cycle-aggregated DES treats within-cycle dynamics in a way that can mask deadline effects; (ii) the GE model is explicitly not calibrated to ISL data (fine), but then ARQ feasibility conclusions depend heavily on the coherence assumption “GE transitions once per \(T_c\)” and the chosen \(p_{BG}\); (iii) the coordinator ingress “fluid server” abstraction plus drop-tail buffer is not obviously aligned with a TDMA service discipline that is deterministic and deadline-driven.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internal logic is generally consistent and improved relative to typical sizing manuscripts: the paper clearly distinguishes info-rate, PHY-rate, \(\gamma\), and half-duplex partitioning \(\alpha_{\text{RX}}\). The stress-case contextualization as a continuous-duty upper bound is stated explicitly and repeated, which helps.

Remaining validity concerns are mostly about *interpretation* and *coupling*:
- The paper sometimes mixes “RF-backup” motivation for the 1 kbps per-node budget with a “coordination channel S-band 35 kbps TDMA” design point; this is defensible (lowest-common-denominator design philosophy), but the mapping between these modes can be confusing and risks misinterpretation that 1 kbps nodes somehow “have” a 35 kbps radio.  
- The ARQ infeasibility statement at 30 kbps is contingent on a particular GE parameterization and on the assumed retransmission-slot structure; it should be framed more conditionally (and/or quantified across a parameter sweep), otherwise it reads stronger than warranted.

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
The manuscript is unusually explicit about definitions (baseline vs \(\eta\), Model C vs Model S, evidence tiers, etc.). Tables like the “rate ladder” and the superframe budget are strong. The repeated “do not double-count” guidance is helpful and indicates the authors understand how readers may misuse the framework.

Clarity issues remain:
- The paper is long and occasionally repetitive; several paragraphs restate the same feasibility narrative (24 infeasible, 30 minimum, 35 recommended). Condensing repetition would create space for deeper explanation of the generalized equations and how to apply them.  
- Some claims are “decision-relevant” (e.g., “100% deadline misses at 24 kbps causes complete situational awareness loss”) but the operational definition of “situational awareness loss” in this architecture (given safe-hold modes, exception telemetry, etc.) is not rigorously defined.

---

## 5. Ethical Compliance  
**Rating: 5 (Excellent)**  
Strong reproducibility posture: code and datasets are provided with a tag, environment is specified, and the manuscript clearly states “no external validation.” AI disclosure is explicit and appropriately scoped (ideation/editing only). No ethical red flags.

One suggestion: include a permanent archival option (Zenodo DOI) in addition to GitHub to meet long-term reproducibility expectations.

---

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
The paper is broadly in-scope for IEEE TAES / space systems networking and coordination. References cover swarm robotics, distributed algorithms, AoI, CCSDS, and some constellation networking.

Gaps:
- TDMA/DAMA and satellite return-link scheduling literature is only lightly connected to the derived superframe feasibility conditions. DVB-RCS2 is mentioned, but the paper would benefit from citing and contrasting with classic DAMA/TDMA sizing and guard/acquisition treatments (even if not CCSDS).  
- For GE/channel modeling, the paper cites Lutz/ITU-R, but does not connect to more recent LEO ISL empirical/channel modeling work (even if sparse) or to optical/pointing outage models that might dominate in the “coordination channel” mode.

---

# Major Issues

1) **Ambiguity/inconsistency in the “1 kbps per-node budget” motivation vs the 35 kbps S-band TDMA coordinator channel**  
**Why it matters:** A reader can reasonably conclude the architecture is “sized for RF-backup,” yet the actual Layer-2 schedulability and \(\gamma\) analysis is for a 24–35 kbps S-band coordination channel, while RF-backup is 2.5 kbps and “hierarchical coordination is suspended.” This undermines the central narrative that the lowest-common-denominator link drives design.  
**Remedy:** Add a single, definitive “link/mode model” figure and a short formal statement:  
- Which link(s) carry baseline status, hierarchical coordination ingress/egress, and safe-mode beacons.  
- Which feasibility layers apply to which mode.  
- Whether the 1 kbps “budget” is (a) a logical allocation within the 35 kbps shared channel, (b) a design requirement for UHF backup, or (c) both (if so, explain how).  
Also adjust wording in §3.6 and elsewhere to avoid implying that the 35 kbps channel is the RF-backup channel.

2) **Campaign duty factor \(d\) is a good addition, but the workload realism argument is still not fully closed**  
**Why it matters:** Prior versions likely faced “46% overhead is unrealistic” critiques. You now contextualize \(\eta_S\approx46\%\) as an upper bound and introduce \(d\), but the mapping from real operations to \(d\) remains somewhat ad hoc (e.g., “conservative default \(d=0.10\)”). Without a stronger operational grounding, reviewers may still view the stress-case as contrived and the “routine 5–10%” as asserted rather than demonstrated.  
**Remedy:**  
- Provide a compact derivation for each row in Table IX (duty mapping): show how many commands, over how many cycles, per year, yields that \(d\).  
- Include at least one alternative workload model besides ON/OFF geometric (e.g., bounded burst model or self-exciting/Hawkes-like burstiness) and report how the buffer multipliers change. Even a sensitivity statement (“if burstiness is heavier-tailed, multiply buffer by X”) would help.  
- Explicitly distinguish *command generation* (drives \(\eta_{\text{cmd}}\)) from *telemetry sampling* (drives AoI) in the duty-factor narrative, so readers don’t conflate \(d\) with \(p_{\text{exc}}\).

3) **\(\gamma\) “unification” to ~0.76 is mostly consistent, but there are still places where Model S results risk being interpreted as decision-relevant**  
**Why it matters:** The manuscript says “all feasibility claims use Model C,” yet Model S appears in rate discussions and in ARQ coupling examples (e.g., the 52.7% miss example is described “Model S 24 kbps” earlier, while Table VIII uses “24 kbps” without always restating which \(\gamma\)/slot model is applied). Confusion about which \(\gamma\) underlies which conclusion is a common failure mode for sizing papers.  
**Remedy:**  
- Add a prominent label in every table/figure caption that uses Model S, and add a one-line “NOT FOR RECOMMENDATIONS” note in those captions.  
- In Table VIII (joint interaction), explicitly state the slot model used to compute slot time and whether it corresponds to Model C at each PHY rate. If Table VIII is Model S, say so; if it is Model C, reconcile with the earlier narrative that 24 kbps Model C is infeasible even without ARQ (yet Table VIII shows 0% misses at 24 kbps with \(M_r=0\)). Right now, that looks contradictory unless the reader carefully infers different models.

4) **Three-layer framing vs two-layer framing: the “mapping \(\eta/\gamma\) to airtime” remains conceptually slippery**  
**Why it matters:** You correctly warn against double-counting, but several passages effectively introduce a quasi-third layer (“MAC efficiency”) and readers may still conflate byte utilization and airtime feasibility. In particular, Eq. (34) \(C_{\text{raw}}=C_{\text{coord,info}}/\gamma\) plus later superframe checks can be interpreted as two independent constraints when they are not.  
**Remedy:**  
- Tighten the formalism: define Layer 1 purely in bits/cycle at the message layer; define Layer 2 purely in time-domain slots/superframe. Present \(\eta/\gamma\) only as an *intuition* metric (optional) and not as part of the feasibility test.  
- Consider renaming “two-layer feasibility” to “byte-feasibility + schedule-feasibility,” and move Eq. (34) into a “useful conversion” box.

5) **DES “verification value” remains limited; distributional tails are useful but need clearer linkage to design decisions**  
**Why it matters:** The paper is candid that DES matches closed-form means “by construction.” The incremental value is tail/buffer sizing under campaigns, but the manuscript does not translate those tails into concrete engineering requirements (buffer size in bytes/messages for given overflow probability, or required coordinator ingress headroom).  
**Remedy:**  
- Add a table: for \(k_c=100\), \(d\in\{0.01,0.10,0.50\}\), give recommended buffer size (messages and bytes) for <1% overflow, and show sensitivity to correlation scope (node/cluster/regional).  
- Explicitly connect buffer sizing to the “20 kbps info-rate” claim: if buffer is finite, what peak-to-mean factor is assumed when selecting the 35 kbps recommendation?

6) **Packet-level/standards anchoring in §IV-J anchors \(\gamma\) but does not provide independent validation of the *overall* framework; the manuscript should avoid implying it does**  
**Why it matters:** The paper largely handles this correctly, but there are still moments where “packet-level validation” language could be read as validating the scheduling conclusions, when it only anchors parameter values.  
**Remedy:** Rename §IV-J to “Standards-based parameter anchoring of \(\gamma\)” (you already do similar wording) and remove/avoid the term “validation” in that subsection title and surrounding text. Keep “validation” reserved for Tier-3 external comparisons.

7) **Generalized \(\gamma\) expression is potentially useful, but it is not yet packaged as a practitioner tool (inputs/outputs/typical ranges)**  
**Why it matters:** Eq. (38) is a key deliverable. Practitioners will ask: what are realistic \(T_{\text{acq}}\), \(T_{\text{guard}}\), \(O_{\text{frame}}\), and \(R_{\text{FEC}}\) ranges for typical radios? Without that, the equation is correct but hard to apply.  
**Remedy:** Add a short “parameter table for \(\gamma\)” with typical ranges and what drives them (e.g., half-duplex turnaround, ranging, acquisition architecture). Also add one worked example beyond Prox-1 (you briefly mention CLTU/Ka-band in a footnote; make one of these a full worked example with computed \(\gamma\) and resulting \(R_{\text{PHY,min}}\)).

---

# Minor Issues

1) **Potential contradiction to resolve:** Table XIII (“PHY Rate Feasibility”) shows 24 kbps infeasible (negative margin), but Table VIII shows 0% misses at 24 kbps for “No Loss” and “GE \(M_r=0\)”. This is likely Model S vs Model C, but it must be made explicit.  

2) **Terminology:** “RF-backup” vs “coordination channel” vs “per-node budget” needs consistent phrasing throughout; consider always pairing “UHF backup (2.5 kbps)” and “S-band coordination channel (35 kbps TDMA)” with those exact labels.  

3) **AoI interpretation:** You state AoI P99 is “sampling policy tail, not network-induced latency.” True under the geometric model, but in practice exception reporting is often thresholded and correlated; consider adding a sentence that Eq. (19) is an upper bound or a baseline under memoryless sampling.  

4) **Coordinator summary payload accounting:** The 512-byte breakdown includes “metadata/CRC (371 B)” which seems unusually large and may raise eyebrows. Either justify why metadata is that large or present it as “padding/implementation overhead” and show sensitivity to summary size.  

5) **Guard/acquisition accounting:** In Table XI you state ACK mini-slots are “absorbed within the 4.7 ms guard interval.” That is a strong assumption; ACK timing is not guard time. If you keep it, justify why ACK can be embedded without increasing slot time (e.g., by allocating a fixed postamble within the slot).  

6) **Evidence tier table:** Table XIV is helpful; consider adding a row explicitly for the “35 kbps recommendation” and mark which tier supports it (it’s currently spread across multiple rows).  

7) **References:** Several “non-archival accessed Feb 2026” web references are acceptable as context, but for TAES you may want more archival sources for constellation operations and TDMA/DAMA scheduling.

---

## Overall Recommendation  
**Recommendation:** **Major Revision**

The paper is close to being publishable as a design/sizing contribution, and Version CO shows meaningful improvements: the campaign duty factor \(d\) directly addresses workload realism concerns; the \(\gamma\approx0.76\) CCSDS anchoring is a clear step up from an assumed 0.85; and the stress-case \(\eta_S\approx46\%\) is now more appropriately framed as a continuous-duty upper bound rather than a typical operating point. The two-layer feasibility framework (byte budget + TDMA airtime) is conceptually sound and, if clarified, can be a useful practitioner reference.

The primary blockers are (i) residual confusion about which link/mode the “1 kbps per-node budget” actually constrains versus where the 35 kbps recommendation applies, (ii) insufficiently explicit separation of Model C vs Model S results leading to apparent contradictions (notably the 24 kbps feasibility/miss-rate story), and (iii) the need to translate DES tail results into concrete engineering sizing guidance rather than “DES matches equations.” Strengthening these aspects would materially improve the manuscript’s credibility and usability for TAES readers.

---

## Constructive Suggestions (ordered by impact)

1) **Add a single “system modes and links” diagram + tighten the narrative around 1 kbps vs 35 kbps** (eliminate reader confusion; ensure claims map cleanly to modes).  
2) **Make Model C vs Model S usage unmistakable** (especially where 24 kbps appears). Resolve the Table VIII vs Table XIII inconsistency explicitly.  
3) **Upgrade the duty-factor realism argument**: show worked \(d\) calculations, add at least one heavier-burstiness sensitivity, and clearly separate \(d\) (commands) from \(p_{\text{exc}}\) (sampling).  
4) **Turn DES tail results into explicit buffer/headroom recommendations** (tables with buffer sizes for overflow targets; link to coordinator capacity sizing).  
5) **Reframe §IV-J as “parameter anchoring,” not “validation,” and avoid implying independent validation** beyond anchoring \(\gamma\).  
6) **Package Eq. (38) as a practitioner tool**: add a parameter range table and at least one full worked example beyond Prox-1, showing how \(\gamma\) changes and how the rate ladder shifts.  
7) **Clarify ARQ conclusions**: present ARQ feasibility as conditional on coherence time and provide a small sweep (e.g., required margin vs \(p_{BG}\), \(p_B\), \(M_r\)) so the “30 kbps insufficient for ARQ” statement is not overly dependent on a single assumed GE setting.