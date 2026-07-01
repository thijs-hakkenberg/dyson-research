---
paper: "02-swarm-coordination-scaling"
version: "df"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-05"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The paper targets a real and under-served gap: *parametric, closed-form sizing* for hierarchical coordination traffic in very large swarms, with explicit byte accounting and a schedulability check tied to a concrete TDMA framing model. The two-test framework (Test A byte budget + Test B airtime) is a useful abstraction for early-phase design, and the explicit “rate ladder” from info-rate → PHY-rate → feasibility → recommendation is practitioner-friendly.

Novelty is strongest in (i) the explicit decomposition and coupling of byte-budget vs TDMA airtime, (ii) the rate-dependent \(\gamma(R_{\text{PHY}})\) slot-efficiency treatment grounded in a CCSDS framing interpretation, and (iii) the duty-factor \(d\) campaign model to address workload realism. The work is less novel in the underlying queueing/AoI/GE components individually, but the integration into a sizing workflow is a meaningful contribution.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The modeling stack is coherent for a preliminary sizing study: analytical accounting + cycle-aggregated DES + slot-level TDMA simulator + a standards-based \(\gamma\) parameter estimate. The paper is appropriately explicit about the lack of Tier-3 validation.

However, several methodological choices materially affect the main design conclusion (“30 kbps min, 35 kbps recommended”) and need stronger justification or sensitivity treatment: (a) the per-slot acquisition time applied *per node per cycle*; (b) the half-duplex partition/definition of \(\alpha_{\text{RX}}\) and how it interacts with egress and ARQ; (c) the GE coherence assumption (state constant over a whole cycle) used to argue intra-cycle ARQ ineffectiveness in the “slow mixing” regime; and (d) the way ARQ demand is estimated (“8 concurrent retries”) versus an analytically derived distribution.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internal logic is mostly consistent and the manuscript makes a commendable effort to prevent earlier confusions (e.g., explicitly stating \(\gamma\) is not a separate feasibility layer; \(\alpha_{\text{RX}}\) is computed; Model S is not used for recommendations). The stress-case \(\eta_S \approx 46\%\) is now clearly framed as a continuous-duty upper bound and the duty-factor mixture example helps contextualize it.

Remaining validity concerns are primarily about (i) whether “acquisition per slot” is realistic for centrally scheduled intra-cluster TDMA with stable links, (ii) whether the “three-layer feasibility” narrative is fully consistent everywhere (some passages still read like “byte budget + \(\gamma\) conversion + TDMA” even though you say it’s only two tests), and (iii) whether the DES “tail value” is sufficiently independent of the assumed ON/OFF model to warrant design guidance (even if you disclaim generality).

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
The paper is unusually explicit in definitions, boundary conditions, and what is and is not being claimed. The notation table, “two-test feasibility framework” box, and the rate ladder table are strong. The repeated reminders about Model C vs Model S and the “do not double-apply the heuristic” warning are helpful.

That said, the manuscript is long and occasionally repetitive (multiple places restate the same caveats). Several key quantities (\(\alpha_{\text{RX}}\), \(T_{\text{acq}}\), what exactly is included in “ingress” vs “egress”) appear in many sections; a single consolidated “superframe definition” figure/table early in the Results would reduce cognitive load.

---

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
Data/code availability is provided with a specific tag and environment details—good practice. AI disclosure is present and reasonably specific (ideation + prose editing only). No human/animal subjects.

Reproducibility would be stronger if the repository included: (i) a one-command script to regenerate every figure/table; (ii) archived outputs (CSV) for key plots; (iii) a manifest mapping paper figures to exact config files/commit hashes.

---

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
Citations cover distributed algorithms (Raft, Lamport), AoI, GE, CCSDS standards, and relevant constellation/mega-constellation networking. The CCSDS anchoring is appropriate for T-AES readership.

Gaps: (i) more direct engagement with satellite MAC/TDMA literature beyond DVB-RCS2 (e.g., DAMA/BoD return links, satellite ISL MAC studies, or CCSDS Proximity-1 operational experiences); (ii) more explicit comparison to existing smallsat swarm comms demonstrations (even if not at scale) to justify message models and timing assumptions; (iii) if claiming “no prior work provides closed-form sizing across \(10^3\)–\(10^5\) nodes,” tighten the claim and cite any near-miss works to avoid overreach.

---

# Major Issues

1. **Acquisition time applied per slot is likely the dominant hidden assumption behind the 35 kbps recommendation.**  
   **Why it matters:** In Model C, \(T_{\text{acq}}=5\) ms is included per node per cycle. With 99 member slots, that’s ~495 ms/cycle of fixed overhead. If in a realistic centrally scheduled TDMA superframe the receiver stays in a tracking state across many consecutive bursts (common in TDMA systems), “acquisition” may be amortized per *superframe* or per *burst group*, not per slot. This would materially increase \(\gamma\), reduce required rate, and change the “30 min / 35 rec” conclusion.  
   **Remedy:**  
   - Introduce at least two explicit acquisition models: **per-slot** (cold-start), **per-superframe** (one acquisition + tracking), and optionally **per-burst-group** (e.g., reacquire every \(m\) slots).  
   - Recompute Table 13 (rate feasibility), Table 6 (rate ladder), and the 35 kbps recommendation under these models.  
   - Tie each model to plausible radio behavior (Prox-1 typical operations, burst-mode demod constraints, tracking loop holdover). Right now “Prox-1 implies cold-start” is asserted but not convincingly justified for intra-cluster TDMA.

2. **\(\gamma\) “unification” is improved, but consistency and numerics still look fragile across rate tables/claims.**  
   **Why it matters:** The paper’s central design output depends on \(\gamma_{30}=0.745\), \(\gamma_{35}=0.732\), etc. Small inconsistencies (rounding, whether framing bits are FEC-encoded, whether ACK fits inside guard, whether turnaround is double-counted) can move margins by hundreds of milliseconds across 99 slots. Reviewers and practitioners need confidence that *every* place \(\gamma\) is used matches Eq. (31).  
   **Remedy:**  
   - Provide a single authoritative “\(\gamma\) ledger” table (you partly do this in Table 12 note) but make it enforceable: list \(R_{\text{PHY}}\), \(T_{\text{slot}}\), \(\gamma\), and each time component for each rate used (24/30/35/50), with unrounded intermediate values and a checksum (e.g., total slot time).  
   - Ensure all downstream tables use the same \(T_{\text{slot}}\) values (e.g., Table 8’s 91.7 ms slot at 30 kbps should be derivable exactly from the ledger).  
   - Explicitly state whether ACK time is included in \(\gamma\) or separately in Test B (currently it is “conservative optional,” which is fine, but then it must be consistently excluded from \(\gamma\) everywhere).

3. **The “three-layer feasibility framework” messaging remains slightly inconsistent with the declared “two-test” framework.**  
   **Why it matters:** The paper repeatedly says there are two tests and \(\gamma\) is only a parameter inside Test B, but parts of the narrative (and some tables) still read as if there are three separate checks: byte budget, MAC efficiency (\(\gamma\)), and TDMA airtime. This risks reader confusion and misapplication.  
   **Remedy:**  
   - Standardize terminology: call it **two tests** everywhere; treat “\(\gamma\) conversion” as a *step* inside Test B (as you already state in the boxed text).  
   - Where you present “byte budget / MAC efficiency / TDMA airtime” (or similar phrasing), rewrite as: “Test A (bytes) and Test B (airtime), where Test B uses \(\gamma\) to map bytes to slot time.”

4. **DES verification value is still limited; the “tail” result is conditional and not yet turned into a transferable design rule.**  
   **Why it matters:** You correctly admit Tier-1 DES agreement is tautological. The only incremental DES value claimed is tail/buffer sizing multipliers (1.3×, 1.5×), but those are highly dependent on the assumed ON/OFF campaign model and correlation scope. Without an analytical characterization or robustness check, this can be misleading.  
   **Remedy:**  
   - Either (a) elevate the DES tail result by providing **robustness** across multiple burst models (e.g., geometric ON durations, heavy-tailed ON durations, different correlation structures), or (b) demote it: present it strictly as an illustrative example and avoid quoting specific multipliers as if they were recommendations.  
   - Consider adding an analytical bound/approximation (e.g., Markov-modulated arrival with deterministic service; even a conservative Chernoff/Kingman-style bound) to complement the DES tails.

5. **Packet-level “validation” in Section IV-J is not independent validation; it is parameter anchoring. That’s fine, but the manuscript sometimes leans on it too strongly.**  
   **Why it matters:** The paper’s key empirical-seeming claim is “CCSDS anchors \(\gamma\approx 0.70-0.76\).” This is not a measurement and not even necessarily representative of an ISL modem implementation. Overstating this undermines credibility.  
   **Remedy:**  
   - Tighten language: consistently call it “standards-based parameter estimate” (you do in places) and avoid phrases that could be read as “validated.”  
   - Add a short subsection explicitly separating: **(i) normative standard fields**, **(ii) engineering assumptions (acquisition/guard/turnaround)**, and **(iii) implementation-dependent behavior (tracking, burst demod, ranging)**, with a sensitivity tornado chart showing which term dominates \(R_{\text{PHY,min}}\).

6. **ARQ demand and the “8 concurrent retries” claim need a clearer derivation.**  
   **Why it matters:** The conclusion that 30 kbps is “marginally infeasible” for ARQ under GE hinges on retransmission slot demand (726 ms) compared to margin (730 ms). If the concurrency estimate is off, the 35 kbps recommendation could be over- or under-conservative.  
   **Remedy:**  
   - Provide an explicit calculation for expected number (and distribution) of failed packets per cycle under the GE model (given \(\pi_G,\pi_B,p_G,p_B\)), then map that to required retransmission slots under your ARQ policy.  
   - Report not just mean ARQ time but a high percentile (e.g., P95 ARQ demand) since schedulability is a tail event.  
   - Clarify whether retransmissions are scheduled only for packets that failed in the current cycle (intra-cycle) and whether the coordinator has timely knowledge of failures given ACK placement.

7. **Campaign duty factor \(d\) is a good addition, but its mapping to real operations remains under-justified and somewhat conflated with \(p_{\text{cmd}}\).**  
   **Why it matters:** The manuscript emphasizes that the 46% stress bound occurs <1% of time, but the mapping depends on assumed mission phase durations and command rates. Practitioners will ask: what telemetry/ops data supports \(d=0.10\) as a “conservative default”?  
   **Remedy:**  
   - Provide at least one worked example with plausible numbers from an existing constellation ops cadence (even if approximate): station-keeping burns per week, software updates per quarter, etc., to justify typical \(d\) ranges.  
   - Make the separation between \(d\) (fraction of cycles in “campaign mode”) and \(p_{\text{cmd}}\) (per-cycle probability during campaign) more explicit in all tables (some tables implicitly assume \(p_{\text{cmd}}=1\) when discussing \(d\)).

8. **Fleet-level reuse/interference analysis is too thin for the strength of the recommendation \(R=7\), \(F=8\).**  
   **Why it matters:** While you label it analytical and call for NS-3, the paper still makes a fairly concrete recommendation that could be interpreted as a design requirement. The aggregate interference calculation is simplified (antenna pattern, geometry, scheduling synchronicity).  
   **Remedy:**  
   - Reframe as a preliminary sizing example and provide parameterized formulas (C/I vs reuse distance, antenna pattern assumptions, number of interferers) with sensitivity.  
   - If keeping \(R=7\) as a “recommendation,” bound it with clear conditions (antenna F/B, cluster density, co-channel synchronization) and present alternative feasible points (e.g., \(R=3\) with 15 dBi antennas; \(R=4\) with additional guard).

---

# Minor Issues

1. **Baseline vs overhead terminology:** At times “\(\eta\)” is called “protocol overhead beyond baseline,” but some readers will interpret “overhead” as including baseline telemetry. Consider renaming to \(\eta_{\text{proto}}\) and \(\eta_{\text{total}}\) consistently in captions.  
2. **Equation (Algorithm line 3):** Test A expression uses \(C_{\text{node}}\) but Algorithm inputs omit \(C_{\text{node}}\) in the REQUIRE line.  
3. **AoI equation interpretation:** Eq. (14) is correct for geometric sampling, but calling it an “upper bound” under i.i.d. sampling is fine; clarify it is *not* an upper bound under adversarial or correlated sampling (could be worse).  
4. **Model S table placement:** Table 9 (joint interaction) is clearly labeled “Model S only,” but it still risks being cherry-picked by readers. Consider moving it to an appendix or pairing it immediately with the Model C analog results in the same table format.  
5. **Units and rounding:** Several ms values (e.g., 91.7 ms slot, 160 ms command) should be derived from the same ledger with consistent rounding; provide either 1 decimal everywhere or keep more precision in intermediate computations.  
6. **Coordinator summary size breakdown:** The 371 B “metadata/CRC” appears large; a short justification (headers, padding, security/auth tags?) would help.  
7. **Failure/election transient:** The “thundering herd” footnote is interesting but long and somewhat orthogonal; consider shortening and moving to appendix.  
8. **Explicitly define \(T_{\text{cmd}}, T_{\text{hb}}, T_{\text{sync}}\)** in one place (currently scattered).  
9. **Reference hygiene:** Several references are non-archival web pages; acceptable as context, but key technical claims (e.g., Starlink operational practices) should be supported where possible by archival sources.

---

## Overall Recommendation  
**Recommendation:** **Major Revision**

The manuscript is promising and closer to publishable than many sizing/architecture papers because it is explicit about assumptions, provides closed-form equations, and supplies a reproducible codebase. The duty-factor \(d\) addition meaningfully addresses workload realism concerns, and the updated \(\gamma\) treatment (0.70–0.76 CCSDS-grounded, replacing the earlier higher value) is a substantive improvement that directly affects feasibility conclusions. The stress-case \(\eta_S \approx 46\%\) is now appropriately contextualized as a continuous-duty bound rather than a typical operating point.

The primary blocker is that the central quantitative recommendation (30 kbps minimum, 35 kbps recommended) is highly sensitive to the *per-slot acquisition* assumption and to how ARQ demand is computed. These are not yet justified or stress-tested enough for a top-tier aerospace systems journal, even with caveats. Strengthening the acquisition/tracking model, tightening the \(\gamma\) ledger consistency, and providing a clearer analytical derivation of ARQ slot demand (with percentiles) would significantly improve technical defensibility.

---

## Constructive Suggestions (ordered by impact)

1. **Add acquisition/tracking variants and re-run the rate ladder:** per-slot cold-start vs per-superframe tracking (and maybe per-\(m\)-slot reacquire). Show how \(R_{\text{PHY,min}}\) shifts.  
2. **Publish a single authoritative \(\gamma\) ledger** (per rate) and ensure every table/figure derives from it; include ACK handling explicitly.  
3. **Replace the “8 concurrent retries” narrative with an analytical ARQ-demand distribution** (mean + P95) under GE; use that to justify “30 kbps no-ARQ / 35 kbps ARQ-capable.”  
4. **Clarify the feasibility framework language everywhere** to avoid any residual “three-layer test” interpretation; keep \(\gamma\) strictly inside Test B.  
5. **Strengthen the practical meaning of \(d\):** add one or two realistic ops cadence examples and clarify the \(d\)–\(p_{\text{cmd}}\) separation in all workload tables.  
6. **Either broaden or demote the DES tail/buffer sizing claim:** show robustness across burst models or remove numeric multipliers from the mainline narrative.  
7. **Soften and parameterize fleet reuse recommendations** and explicitly bound when \(R=7\) is needed; move hard recommendations behind conditions and sensitivity.

If these are addressed, the work could become a strong “design equations + sizing workflow” paper suitable for T-AES, with clear practitioner value despite the acknowledged lack of external validation.