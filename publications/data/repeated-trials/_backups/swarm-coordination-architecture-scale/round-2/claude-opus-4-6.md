---
questionId: "rq-1-24"
questionSlug: "swarm-coordination-architecture-scale"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
roundNumber: 2
generated: "2026-02-08"
type: "discussion-response"
---

# Swarm Coordination Architecture at Scale: Round 2 Assessment

## Opening Position

The Round 1 discussion converged on hierarchical architecture as the correct foundation—I agree completely. But all three responses, while excellent, danced around what I consider the **hardest unsolved problem**: how do you maintain coherent swarm-wide state when the swarm itself becomes larger than any single communication horizon can span in operationally relevant timescales?

I want to push the architecture from "hierarchical topology validated by simulation" to **a concrete protocol and authority framework that handles the ugly edge cases**. I'll build directly on the strongest elements from Round 1: Opus's insight that orbital mechanics and coordination topology are inseparable, Gemini's Federated Constellation operational model, and GPT's five-layer hierarchy with explicit authority boundaries.

## The Core Architectural Problem Nobody Has Fully Solved

At 10⁶ units spread across heliocentric orbits near 1 AU, the swarm's spatial extent could span tens of millions of kilometers. Light-time across the swarm itself becomes non-trivial—potentially 30-100 seconds for widely separated orbital shells. This means:

1. **No single entity can have a real-time global view of swarm state.** Not the ANH, not Earth ground control, not any coordinator node.
2. **"Eventual consistency" is not just a software pattern—it's a physical law.** The swarm state is always a reconstruction from delayed observations.
3. **Collision avoidance at the swarm boundary between clusters is harder than collision avoidance within clusters**, because cross-cluster coordination has higher latency and lower bandwidth.

This is fundamentally different from Starlink or any terrestrial mega-constellation, where ground stations maintain near-real-time global catalogs. We have no such luxury.

## Proposed Architecture: Hierarchical Federated Consensus with Predictive State

### Layer Structure

I adopt GPT's five-layer model but redefine the interfaces with explicit state-management semantics:

**L0 – Unit (reflexive, <100ms loop)**
Each unit maintains its own ephemeris propagator, attitude controller, and collision avoidance reflex. The critical design requirement: **every unit must be able to safe itself indefinitely with zero external communication.** This means onboard orbit propagation accurate to ±10m over 72 hours, sufficient to maintain separation from predicted neighbor trajectories cached locally.

**L1 – Cell (10-50 units, ~1s loop)**
Cells are defined by orbital proximity—units whose relative velocities are <1 m/s and separations <100 km. Cell membership is **self-organizing**: units detect neighbors via local RF beacon and form cells autonomously using a lightweight consensus protocol. Cell coordinator is elected by lowest-ID tiebreaker (deterministic, no negotiation overhead). The cell coordinator aggregates health telemetry, resolves intra-cell collision threats, and maintains a shared ephemeris table for all cell members.

**Key design choice**: Cell size is capped at 50 units because collision avoidance pairwise checks within a cell must complete within the 1-second loop. At 50 units, that's 1,225 pairs—trivially computable.

**L2 – Sector (100-500 cells, ~60s loop)**
Sectors correspond to orbital arc segments, roughly 1-5° of heliocentric longitude. Sector coordinators are **dedicated relay/compute nodes**, not repurposed collectors. This is where I diverge from the cost-optimization instinct: trying to run sector coordination on collector hardware is a false economy. A sector coordinator needs ~10x the compute and ~100x the communication bandwidth of a collector unit. Budget for purpose-built sector coordinator satellites—perhaps 2,000-5,000 across the full swarm, each managing 200-2,000 cells.

Sector coordinators perform:
- **Cross-cell collision prediction** using propagated ephemerides from all constituent cells
- **Power beam coordination** for units within the sector's angular span
- **Maintenance scheduling and dispatch** for the sector's units
- **Upward telemetry aggregation** (compress 10,000-25,000 unit states into sector summary)

**L3 – Ring (all sectors at similar orbital radius, ~600s loop)**
Ring coordinators manage the interface between sectors in the same orbital shell. Their primary function is **boundary management**: ensuring that units transitioning between sectors are handed off cleanly, and that sector-boundary collision avoidance is coordinated. Ring coordination can be distributed across sector coordinators using a rotating-chair protocol—no additional hardware tier needed.

**L4 – Swarm (all rings, ~3600s loop)**
Swarm-level coordination is **policy-based, not real-time.** The ANH and Earth ground jointly maintain:
- Master ephemeris catalog (updated hourly from sector aggregations)
- Deployment scheduling and orbital slot allocation
- Power routing optimization across the full swarm
- Long-term collision risk assessment and orbital maintenance campaigns

### The Critical Innovation: Predictive State Sharing

The key protocol innovation that makes this work at scale is **predictive state sharing rather than real-time state sharing.**

Instead of continuously transmitting current positions, each unit broadcasts its **osculating orbital elements plus planned maneuver schedule** at low frequency (once per orbit, or ~every 365 days for circular 1 AU orbits—but more practically, once per day or upon any maneuver). Any node in the hierarchy can propagate any other unit's position forward with bounded error.

This transforms the bandwidth problem:

| Approach | Per-unit bandwidth | 10⁶ units aggregate |
|----------|-------------------|---------------------|
| Continuous state (1 Hz) | ~500 bps | 500 Mbps |
| Predictive state (1/day) | ~0.5 bps | 500 kbps |
| Predictive + event-driven maneuvers | ~2 bps | 2 Mbps |

The predictive approach reduces aggregate bandwidth by **over two orders of magnitude**, making million-unit coordination feasible within the ANH's specified communication capacity.

**Error budget**: Keplerian propagation at 1 AU with solar radiation pressure perturbation modeling should yield position accuracy of ±1 km over 24 hours for a known-area collector. This is adequate for L2+ coordination. L1 cells use local ranging to maintain ±10m relative knowledge for close-proximity operations.

## Addressing the Hard Edge Cases

### Edge Case 1: Cluster Boundary Collisions
This was correctly identified by Opus as the critical failure mode. My solution: **sector coordinators maintain overlap zones.** Each sector's collision avoidance volume extends 5% beyond its nominal boundary into adjacent sectors. Sector coordinators exchange boundary-zone ephemerides at 10x the normal rate. Units in overlap zones are tracked by both sectors simultaneously.

Cost: ~10% increase in sector coordinator compute load. Acceptable.

### Edge Case 2: Cascade Failure of Sector Coordinators
If a sector coordinator fails, its cells revert to L1 autonomous operation (safe, but no cross-cell coordination). Adjacent sector coordinators detect the gap within one loop cycle (60s) and **expand their boundary zones to cover the orphaned cells.** If multiple adjacent coordinators fail simultaneously, cells enter a "hold and drift" mode—maintaining current orbits with maximum separation margins—while L3/L4 coordination dispatches replacement coordinators or reassigns coverage.

**Design requirement**: The swarm must carry 10-15% spare sector coordinator capacity, either as cold spares or as dual-capable units that normally serve as relay stations.

### Edge Case 3: Swarm-Wide Communication Disruption
Solar storm, CME, or other event disrupts RF/optical communication across a large swarm segment. Every unit falls back to L0 autonomy. The predictive state model is the savior here: because every unit's trajectory is predictable from its last-broadcast orbital elements, **collision risk remains bounded even without communication**, as long as no unplanned maneuvers occur. The "pause and safe" philosophy from the ANH specification extends naturally: units hold their orbits, cease non-essential maneuvers, and wait for communication restoration.

**Critical constraint**: Units must NOT attempt autonomous collision avoidance maneuvers during communication blackout unless a collision is imminent within their onboard propagation accuracy horizon (72 hours at ±10m). Uncoordinated avoidance maneuvers are more dangerous than holding position, because they invalidate other units' predictive models.

### Edge Case 4: Heterogeneous Unit Integration
Later-phase units with different sizes, capabilities, and orbital characteristics join the swarm. The architecture handles this through **typed cell membership**: maintenance vehicles and relay stations participate in cells but with different roles and different telemetry profiles. The sector coordinator's collision avoidance treats all physical objects identically (they all have ephemerides and collision cross-sections), while power coordination and tasking use type-specific protocols.

## Quantified Resource Requirements

For a 1,000,000-unit swarm:

- **Sector coordinators**: ~3,000 dedicated satellites (one per ~333 cells of ~50 units each ≈ 16,650 units per sector... let me recalculate). With 20,000 cells of 50 units, and 100 cells per sector, that's 200 sector coordinators. At 15% redundancy: **~230 sector coordinator satellites.**
- **Aggregate coordination bandwidth**: ~2-5 Mbps swarm-internal, ~50 Mbps to ANH, ~10 Mbps to Earth
- **Per-unit compute for L0**: ~1 MFLOPS (orbital propagation + attitude control)
- **Per-sector-coordinator compute**: ~10 GFLOPS (cross-cell collision avoidance for 5,000 unit pairs in overlap zones + beam coordination)
- **Swarm-level catalog maintenance**: ~1 TFLOPS (manageable with 2030s-era radiation-hardened processors)

## Key Recommendation Differences from Round 1

1. **Purpose-built sector coordinators are non-negotiable.** Do not try to run sector coordination on collector hardware. The mass and power penalty is small relative to the reliability gain.
2. **Predictive state sharing is the enabling protocol innovation.** Without it, bandwidth requirements are unmanageable. With it, the problem is tractable.
3. **Uncoordinated collision avoidance maneuvers must be prohibited except for imminent-impact scenarios.** This is counterintuitive but essential—the predictability of the swarm is its primary safety mechanism.
4. **The ANH is a logistics and policy hub, never a real-time controller.** This should be codified in the specification as a hard architectural constraint, not just a preference.

## Open Issues for Future Work

- **Spatial partitioning algorithm selection** (Research Direction #3) remains critical for sector coordinator efficiency
- **Inter-shell coordination** for multi-radius swarm configurations needs dedicated analysis
- **Graceful scaling from hundreds to millions**: the architecture must work at every intermediate scale during buildup, not just at the target scale

The architecture I've described is not speculative—every component has terrestrial analogs in distributed systems, satellite operations, or autonomous vehicle coordination. The novelty is in their integration at heliocentric scale, and the predictive state model that makes that integration physically feasible.