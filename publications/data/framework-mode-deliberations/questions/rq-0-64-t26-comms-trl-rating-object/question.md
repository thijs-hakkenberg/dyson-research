---
questionId: "rq-0-64"
slug: "t26-comms-trl-rating-object"
title: "What should the TRL rating of deep-space communications and command (T26) assess?"
questionType: "discussion"
priority: "high"
status: "answered"
answeredDate: "2026-10-17"
sourcePhase: "phase-0"
sourceBOMItemId: "bom-0-7"
sourceBOMItemSlug: "organizational-infrastructure"
sourceBOMItemName: "Organizational Infrastructure"
relatedBOMItems:
  - "bom-0-1"
  - "bom-0-4"
  - "bom-0-7"
relatedResearchQuestions:
  - "rq-0-62"
  - "rq-0-1"
  - "rq-0-8"
  - "rq-0-42"
tags:
  - "trl"
  - "communications"
  - "command-security"
  - "decision-frameworks"
createdDate: "2026-10-17"
---

## Background

The TRL re-baseline of the revised Phase 0 architecture (rq-0-62, work package WP-A, `reconciliation/phase-0/trl/`) rated 26 critical technologies with a three-model panel (Claude Opus 5.5, Gemini 3.1 Pro, GPT-6.1 Sol). The panel agreed within one TRL level on 24 of them. It diverged most on **T26, deep-space communications and resilient command service**, and the synthesis found the divergence comes mainly from rating *different objects*, not from conflicting facts.

The requirement as inventoried: communications, navigation support and authenticated command for roughly 15–29 concurrent deep-space assets (scouts, tugs, site plant), with store-and-forward through solar-conjunction and solar-exclusion outages, 1–25 minute light time, and no safety-critical local action that depends on an Earth response. Phase need is 0A; under owner decision D-02 anything project-ending for Phase 0B needs TRL 6 at the KDP-0B go/no-go.

The three ratings:

| | Claude Opus 5.5 | Gemini 3.1 Pro | GPT-6.1 Sol |
|---|---|---|---|
| Current TRL | 5–7 | 6–7 | 3–4 (integrated service); sub-ratings RF heritage 9, DINET DTN configuration 7, conjunction operations 9, authenticated fleet command 3–4 |
| AD² | 3 | 3 | 4 |
| Risk if it fails | cost-increase | cost-increase | architecture-change |
| Years to TRL 6 | 2–4 | 1–2 | 3–5 |

- **Claude** credits critical functions demonstrated separately in operational environments (Deep Space Network links, the Mars Relay Network, DINET on EPOXI, Mars conjunction operations) and holds authentication with post-outage key recovery at about TRL 4–5. Its upper bound of 7 applies only if the Mars Relay Network plus DSN multiple-spacecraft-per-aperture is accepted as an operational prototype, which it notes ignores a 2–4× node-count gap and the authentication gap.
- **Gemini** treats the subsystem protocols as demonstrated in relevant space environments and so considers TRL 6 met. It states that CCSDS SDLS authenticated commanding has "flown on multiple missions" without naming a mission.
- **GPT** rates the specific integrated service. TRL 4 needs a configuration-controlled integrated breadboard tested against predictions in a documented relevant environment; neither exists, so it records TRL 3 working, 4 conditional, and declines to average sub-ratings.

What the panel agreed: interplanetary RF links are mature; the gap is integration, fleet scale, outage recovery and assurance; authentication and the key-management lifecycle in deep space are the weakest-evidenced element (Claude and GPT); data rates are not yet defined, which blocks quantitative qualification; no integrated precedent exists at this scale.

## Why This Matters

The rating object decides what the KDP-0B gate asks for. If T26 rates heritage components, it is nearly ready and drops off the gate list. If it rates the integrated authenticated service, it is a TRL 3–4 item that needs a funded path to TRL 6 inside Phase 0A, and its failure class (cost-increase vs architecture-change, or project-ending if no trustworthy command service can be shown) changes the gate design in the next work-package step. A licensing state may also make command security a licence condition for high-energy tug operations (D-03), which would tie T26 to the licence gate.

## Key Considerations

- The TRL brief's rules: rate at the scale, environment and duration the architecture requires; multi-model consensus, deliberation conclusions and design studies are not evidence; cite or say unsure.
- NASA TRL exit criteria are defined for a system, subsystem or component in a stated configuration. Rating a composite by its best-demonstrated parts and rating it as the integrated article are both practised; the choice should be explicit.
- The rating object interacts with the gate structure (D-02), the risk lenses on the site, and whether sub-ratings are published alongside one headline number.
- Evidence that would move the ratings: a cited deep-space flight record of SDLS (or equivalent) authenticated commanding with key management; orbit-specific conjunction and solar-exclusion durations for candidate targets and the SEL1 node; a defined traffic budget.

## Research Directions

1. Decide the assessed object for T26 (and, by implication, the rule for other composite technologies in the re-baseline), with the criteria stated first.
2. Say whether one headline TRL or a set of sub-ratings should be carried into the baseline and the gates.
3. Set the risk class and the KDP-0B criterion that follows from the chosen object.
4. Name the evidence and tests that would change the decision.
