"""Swarm coordination simulation model for Dyson swarm elements.

Self-contained discrete-event simulator that models coordination of
large-scale Dyson swarm elements under three network topologies
(centralized, hierarchical, mesh).  Addresses research questions on
architecture at scale, coordinator duty cycling, and fleet coordination
constraints.

Ported from the TypeScript modules in
``src/lib/services/simulation/swarm-coordination/``.
"""

from __future__ import annotations

__version__ = "1.0.0"

import heapq
import math
from dataclasses import dataclass, field
from typing import Any, Literal, Optional

import numpy as np
from numpy.random import Generator

# ---------------------------------------------------------------------------
# Literal types
# ---------------------------------------------------------------------------
CoordinationTopology = Literal["centralized", "hierarchical", "mesh"]
NodeStatus = Literal["operational", "coordinator", "failed", "recovering"]
EventType = Literal[
    "message_send",
    "message_receive",
    "coordinator_handoff",
    "node_failure",
    "node_recovery",
    "collision_warning",
    "gossip_round",
    "state_sync",
]

# ---------------------------------------------------------------------------
# Physical / protocol constants
# ---------------------------------------------------------------------------
SPEED_OF_LIGHT_KM_S: float = 299_792
"""Speed of light used for communication-delay calculations (km/s)."""

INTER_NODE_DISTANCE_KM: float = 1_000
"""Typical inter-node spacing in a Dyson swarm (km)."""

REGIONAL_DISTANCE_KM: float = 50_000
"""Distance to a regional coordinator in the hierarchical topology (km)."""

CENTRAL_DISTANCE_KM: float = 150_000_000
"""Average distance to the central coordinator (~1 AU) (km)."""

MESSAGE_SIZES: dict[str, int] = {
    "ephemeris": 256,
    "heartbeat": 32,
    "handoff": 8192,
    "gossip": 128,
    "collision": 64,
    "cluster_summary": 512,
    "region_summary": 1024,
}
"""Message sizes in bytes by type."""

HANDOFF_STATE_SIZE_BYTES: int = 8192
"""Cluster ephemeris data transferred during coordinator handoff."""

HANDOFF_VERIFICATION_ROUNDS: int = 3
"""Number of verification rounds during coordinator handoff."""

HANDOFF_TIMEOUT_SECONDS: float = 30.0
"""Timeout for a coordinator handoff attempt (seconds)."""

SECONDS_PER_DAY: int = 86_400


# ---------------------------------------------------------------------------
# Core dataclasses
# ---------------------------------------------------------------------------
@dataclass
class SwarmCoordinationConfig:
    """Configuration for a swarm coordination simulation run."""

    node_count: int = 10_000
    """Number of nodes in the swarm (1 000 -- 1 000 000)."""

    coordination_topology: CoordinationTopology = "hierarchical"
    """Network topology for coordination."""

    cluster_size: int = 100
    """Nodes per cluster for hierarchical topology (50--200)."""

    coordinator_duty_cycle_hours: float = 24.0
    """Hours before coordinator handoff (1--168 h)."""

    bandwidth_per_node_kbps: float = 1.0
    """Bandwidth per node in kbps (0.1--10)."""

    node_failure_rate_per_year: float = 0.02
    """Annual failure rate per node (0.01--0.05)."""

    coordinator_power_w: float = 18.0
    """Power consumption when acting as coordinator (W)."""

    base_power_w: float = 5.0
    """Base power consumption for regular nodes (W)."""

    simulation_days: int = 90
    """Simulation duration in days (30--365)."""

    seed: int = 42
    """Random seed for reproducibility."""

    max_events: Optional[int] = None
    """Override maximum events processed (default: node_count * simulation_days * 10)."""


@dataclass
class SwarmNode:
    """Individual swarm node state."""

    id: str
    status: NodeStatus
    cluster_id: str
    is_coordinator: bool
    coordinator_time_seconds: float = 0.0
    power_consumed_wh: float = 0.0
    messages_sent: int = 0
    messages_received: int = 0
    last_update_time: float = 0.0
    failure_time: Optional[float] = None


@dataclass
class Cluster:
    """Cluster state for hierarchical topology."""

    id: str
    node_ids: list[str]
    coordinator_id: str
    regional_coordinator_id: Optional[str] = None
    messages_processed: int = 0
    last_handoff_time: float = 0.0
    failed_handoffs: int = 0


@dataclass
class Message:
    """Message in the coordination network."""

    id: str
    sender_id: str
    receiver_id: str
    size_bytes: int
    send_time: float
    receive_time: Optional[float] = None
    delivered: bool = False
    message_type: str = "ephemeris"


@dataclass
class SimEvent:
    """A single discrete-event simulation event."""

    type: EventType
    time: float
    node_id: str
    cluster_id: Optional[str] = None
    data: Optional[dict[str, Any]] = None

    def __lt__(self, other: SimEvent) -> bool:
        """Comparison for heapq ordering (min-heap on *time*)."""
        return self.time < other.time


@dataclass
class PropagationStats:
    """Propagation statistics for a time window."""

    avg_propagation_ms: float = 0.0
    max_propagation_ms: float = 0.0
    p95_propagation_ms: float = 0.0
    message_count: int = 0


@dataclass
class TierMessageBreakdown:
    """Per-tier message counts for hierarchical topology analysis."""

    intra_cluster_msgs: int = 0
    inter_cluster_msgs: int = 0
    central_msgs: int = 0
    gossip_msgs: int = 0


@dataclass
class SwarmCoordinationRunResult:
    """Result of a single simulation run."""

    run_id: int = 0
    config: Optional[SwarmCoordinationConfig] = None
    communication_overhead_percent: float = 0.0
    bottleneck_threshold_nodes: float = 0.0
    coordinator_availability_percent: float = 100.0
    power_variance_percent: float = 0.0
    avg_update_propagation_ms: float = 0.0
    max_update_propagation_ms: float = 0.0
    failed_handoffs: int = 0
    message_drop_rate: float = 0.0
    total_messages_sent: int = 0
    total_messages_delivered: int = 0
    avg_messages_per_node_per_day: float = 0.0
    total_energy_kwh: float = 0.0
    coordinator_bandwidth_kbps: float = 0.0
    tier_breakdown: Optional[TierMessageBreakdown] = None


@dataclass
class NetworkStructure:
    """Network structure produced by topology initialization."""

    nodes: list[SwarmNode]
    clusters: list[Cluster]
    central_coordinator_id: str
    mesh_neighbors: Optional[dict[str, list[str]]] = None

    def __post_init__(self) -> None:
        self.rebuild_indices()

    def rebuild_indices(self) -> None:
        """Build O(1) lookup dicts for nodes and clusters."""
        self._node_map: dict[str, int] = {
            n.id: i for i, n in enumerate(self.nodes)
        }
        self._cluster_map: dict[str, int] = {
            c.id: i for i, c in enumerate(self.clusters)
        }

    def get_node(self, node_id: str) -> Optional["SwarmNode"]:
        """O(1) node lookup by ID."""
        idx = self._node_map.get(node_id)
        return self.nodes[idx] if idx is not None else None

    def get_cluster(self, cluster_id: str) -> Optional["Cluster"]:
        """O(1) cluster lookup by ID."""
        idx = self._cluster_map.get(cluster_id)
        return self.clusters[idx] if idx is not None else None


@dataclass
class HandoffResult:
    """Result of a coordinator handoff attempt."""

    success: bool
    cluster: Cluster
    nodes: list[SwarmNode]
    new_coordinator_id: Optional[str] = None


# ---------------------------------------------------------------------------
# Message-passing helpers
# ---------------------------------------------------------------------------
def light_time_delay(distance_km: float) -> float:
    """Return one-way light-time delay in milliseconds."""
    return (distance_km / SPEED_OF_LIGHT_KM_S) * 1_000


def calculate_bandwidth_requirement(
    topology: CoordinationTopology,
    node_count: int,
    cluster_size: int,
    update_interval_seconds: float,
) -> float:
    """Return required bandwidth in kbps for the given topology and node count."""
    ephemeris_size = MESSAGE_SIZES["ephemeris"]

    if topology == "centralized":
        messages_per_second = node_count / update_interval_seconds
        bits_per_second = messages_per_second * ephemeris_size * 8
        return bits_per_second / 1_000

    if topology == "hierarchical":
        num_clusters = math.ceil(node_count / cluster_size)
        num_regions = math.ceil(num_clusters / 10)
        # Intra-cluster: each member sends 256-byte ephemeris to coordinator
        cluster_msgs = node_count / update_interval_seconds
        cluster_bps = cluster_msgs * ephemeris_size * 8
        # Cluster->Region: coordinator sends a single compressed cluster summary
        region_msgs = num_clusters / update_interval_seconds
        region_bps = region_msgs * MESSAGE_SIZES["cluster_summary"] * 8
        # Region->Central: regional coordinator sends a single region summary
        central_msgs = num_regions / update_interval_seconds
        central_bps = central_msgs * MESSAGE_SIZES["region_summary"] * 8
        total_bps = cluster_bps + region_bps + central_bps
        return total_bps / 1_000

    # mesh
    gossip_fanout = min(5, math.ceil(math.log2(node_count)))
    gossip_rounds = math.ceil(math.log2(node_count))
    messages_per_round = node_count * gossip_fanout
    rounds_per_second = 1.0 / update_interval_seconds
    messages_per_second = messages_per_round * rounds_per_second / gossip_rounds
    bits_per_second = messages_per_second * MESSAGE_SIZES["gossip"] * 8
    return bits_per_second / 1_000


def calculate_propagation_delay(
    topology: CoordinationTopology,
    node_count: int,
    cluster_size: int,
    processing_delay_ms: float = 1.0,
) -> float:
    """Return expected message propagation delay in milliseconds."""
    if topology == "centralized":
        return light_time_delay(CENTRAL_DISTANCE_KM) * 2 + processing_delay_ms

    if topology == "hierarchical":
        num_clusters = math.ceil(node_count / cluster_size)
        hops = 1 + math.ceil(math.log10(max(1, num_clusters)))
        local_delay = light_time_delay(INTER_NODE_DISTANCE_KM)
        regional_delay = light_time_delay(REGIONAL_DISTANCE_KM)
        return local_delay + regional_delay * (hops - 1) + processing_delay_ms * hops

    # mesh
    gossip_rounds = math.ceil(math.log2(node_count))
    round_delay = light_time_delay(INTER_NODE_DISTANCE_KM) + processing_delay_ms
    return gossip_rounds * round_delay


def calculate_communication_overhead(
    required_kbps: float,
    bandwidth_per_node_kbps: float,
    node_count: int,
) -> float:
    """Return communication overhead as a percentage of total capacity."""
    total_capacity_kbps = bandwidth_per_node_kbps * node_count
    return (required_kbps / total_capacity_kbps) * 100


def per_coordinator_bandwidth_kbps(
    cluster_size: int,
    update_interval_seconds: float = 10.0,
) -> float:
    """Return the peak bandwidth required by a single cluster coordinator (kbps).

    A coordinator receives *cluster_size* ephemeris messages per interval from
    its members and sends one compressed cluster summary upstream.  This
    function returns the peak inbound + outbound rate.
    """
    ephemeris_size = MESSAGE_SIZES["ephemeris"]
    # Inbound: cluster_size ephemeris messages per interval
    inbound_bps = (cluster_size * ephemeris_size * 8) / update_interval_seconds
    # Outbound: one compressed cluster summary per interval
    outbound_bps = (MESSAGE_SIZES["cluster_summary"] * 8) / update_interval_seconds
    return (inbound_bps + outbound_bps) / 1_000


def create_message(
    sender_id: str,
    receiver_id: str,
    message_type: str,
    send_time: float,
) -> Message:
    """Create a new network message."""
    return Message(
        id=f"msg-{sender_id}-{receiver_id}-{send_time:.3f}",
        sender_id=sender_id,
        receiver_id=receiver_id,
        size_bytes=MESSAGE_SIZES.get(message_type, MESSAGE_SIZES["ephemeris"]),
        send_time=send_time,
        delivered=False,
        message_type=message_type,
    )


def estimate_message_count(
    topology: CoordinationTopology,
    node_count: int,
    cluster_size: int,
    duration_seconds: float,
    update_interval_seconds: float,
) -> int:
    """Estimate total message count for the given topology over *duration_seconds*."""
    updates = math.ceil(duration_seconds / update_interval_seconds)

    if topology == "centralized":
        return node_count * updates

    if topology == "hierarchical":
        num_clusters = math.ceil(node_count / cluster_size)
        num_regions = math.ceil(num_clusters / 10)
        return (node_count + num_clusters + num_regions) * updates

    # mesh
    gossip_fanout = min(5, math.ceil(math.log2(node_count)))
    gossip_rounds = math.ceil(math.log2(node_count))
    return node_count * gossip_fanout * gossip_rounds * updates


# ---------------------------------------------------------------------------
# MessageQueue
# ---------------------------------------------------------------------------
class MessageQueue:
    """FIFO message queue with congestion modelling and drop tracking."""

    def __init__(self, max_queue_size: int = 10_000) -> None:
        self._queue: list[Message] = []
        self._total_processed: int = 0
        self._total_dropped: int = 0
        self._propagation_times: list[float] = []
        self._max_queue_size: int = max_queue_size

    # -- mutators ----------------------------------------------------------
    def is_full(self) -> bool:
        """Return ``True`` if the queue has reached its capacity."""
        return len(self._queue) >= self._max_queue_size

    def enqueue(self, message: Message) -> bool:
        """Add *message* to the queue.  Returns ``False`` if dropped."""
        if len(self._queue) >= self._max_queue_size:
            self._total_dropped += 1
            return False
        self._queue.append(message)
        return True

    def dequeue(self, current_time: float) -> Optional[Message]:
        """Dequeue the oldest message, mark it delivered at *current_time*."""
        if not self._queue:
            return None
        self._queue.sort(key=lambda m: m.send_time)
        message = self._queue.pop(0)
        message.receive_time = current_time
        message.delivered = True
        self._total_processed += 1
        propagation_ms = (current_time - message.send_time) * 1_000
        self._propagation_times.append(propagation_ms)
        return message

    def process_messages(
        self,
        current_time: float,
        bandwidth_bps: float,
        duration_seconds: float,
    ) -> list[Message]:
        """Process messages up to the bandwidth limit over *duration_seconds*."""
        processed: list[Message] = []
        bytes_processed = 0.0
        max_bytes = (bandwidth_bps * duration_seconds) / 8.0

        while self._queue and bytes_processed < max_bytes:
            front = self._queue[0]
            if bytes_processed + front.size_bytes > max_bytes:
                break
            msg = self.dequeue(current_time)
            if msg is not None:
                processed.append(msg)
                bytes_processed += msg.size_bytes
        return processed

    # -- queries -----------------------------------------------------------
    def size(self) -> int:
        """Return the current queue depth."""
        return len(self._queue)

    def get_stats(self) -> dict[str, float]:
        """Return processed / dropped / dropRate statistics."""
        total = self._total_processed + self._total_dropped
        return {
            "processed": self._total_processed,
            "dropped": self._total_dropped,
            "dropRate": self._total_dropped / total if total > 0 else 0.0,
        }

    def get_propagation_stats(self) -> PropagationStats:
        """Return propagation-time statistics across delivered messages."""
        if not self._propagation_times:
            return PropagationStats()
        sorted_times = sorted(self._propagation_times)
        total = sum(sorted_times)
        p95_idx = int(len(sorted_times) * 0.95)
        return PropagationStats(
            avg_propagation_ms=total / len(sorted_times),
            max_propagation_ms=sorted_times[-1],
            p95_propagation_ms=sorted_times[p95_idx],
            message_count=len(sorted_times),
        )

    def clear(self) -> None:
        """Remove all messages from the queue (stats are kept)."""
        self._queue.clear()


# ---------------------------------------------------------------------------
# Coordinator model helpers
# ---------------------------------------------------------------------------
def create_node(
    node_id: str,
    cluster_id: str,
    is_coordinator: bool = False,
) -> SwarmNode:
    """Create a new :class:`SwarmNode`."""
    return SwarmNode(
        id=node_id,
        status="coordinator" if is_coordinator else "operational",
        cluster_id=cluster_id,
        is_coordinator=is_coordinator,
    )


def create_cluster(
    cluster_id: str,
    node_count: int,
    coordinator_node_id: str,
) -> tuple[Cluster, list[SwarmNode]]:
    """Create a :class:`Cluster` with *node_count* nodes.

    Returns a ``(cluster, nodes)`` tuple.
    """
    nodes: list[SwarmNode] = []
    for i in range(node_count):
        nid = f"{cluster_id}-node-{i}"
        is_coord = nid == coordinator_node_id
        nodes.append(create_node(nid, cluster_id, is_coord))

    # Ensure at least one coordinator exists
    if not any(n.is_coordinator for n in nodes) and nodes:
        nodes[0].is_coordinator = True
        nodes[0].status = "coordinator"

    coord_id = next(
        (n.id for n in nodes if n.is_coordinator),
        nodes[0].id if nodes else coordinator_node_id,
    )
    cluster = Cluster(
        id=cluster_id,
        node_ids=[n.id for n in nodes],
        coordinator_id=coord_id,
    )
    return cluster, nodes


def calculate_power_consumption(
    node: SwarmNode,
    duration_seconds: float,
    base_power_w: float,
    coordinator_power_w: float,
) -> float:
    """Return energy consumed (Wh) by *node* over *duration_seconds*."""
    hours = duration_seconds / 3600.0
    power = coordinator_power_w if node.is_coordinator else base_power_w
    return power * hours


def update_node_power(
    node: SwarmNode,
    duration_seconds: float,
    base_power_w: float,
    coordinator_power_w: float,
) -> SwarmNode:
    """Return a copy of *node* with updated power and coordinator time."""
    power_wh = calculate_power_consumption(
        node, duration_seconds, base_power_w, coordinator_power_w
    )
    new = SwarmNode(
        id=node.id,
        status=node.status,
        cluster_id=node.cluster_id,
        is_coordinator=node.is_coordinator,
        coordinator_time_seconds=(
            node.coordinator_time_seconds + duration_seconds
            if node.is_coordinator
            else node.coordinator_time_seconds
        ),
        power_consumed_wh=node.power_consumed_wh + power_wh,
        messages_sent=node.messages_sent,
        messages_received=node.messages_received,
        last_update_time=node.last_update_time,
        failure_time=node.failure_time,
    )
    return new


def calculate_coordinator_availability(
    cluster: Cluster,
    nodes: list[SwarmNode],
    simulation_duration_seconds: float,
) -> float:
    """Return coordinator availability as a percentage (0--100)."""
    total_coord_time = sum(
        n.coordinator_time_seconds
        for n in nodes
        if n.cluster_id == cluster.id
    )
    expected_time = simulation_duration_seconds
    handoff_gap_seconds = cluster.failed_handoffs * HANDOFF_TIMEOUT_SECONDS
    effective = min(total_coord_time - handoff_gap_seconds, expected_time)
    return (effective / expected_time) * 100.0


def perform_handoff(
    cluster: Cluster,
    nodes: list[SwarmNode],
    current_time: float,
    rng: Generator,
) -> HandoffResult:
    """Attempt a coordinator handoff.  Returns a :class:`HandoffResult`."""
    # Find eligible candidates
    candidates = [
        n
        for n in nodes
        if n.cluster_id == cluster.id
        and n.status == "operational"
        and n.id != cluster.coordinator_id
    ]

    if not candidates:
        new_cluster = Cluster(
            id=cluster.id,
            node_ids=list(cluster.node_ids),
            coordinator_id=cluster.coordinator_id,
            regional_coordinator_id=cluster.regional_coordinator_id,
            messages_processed=cluster.messages_processed,
            last_handoff_time=current_time,
            failed_handoffs=cluster.failed_handoffs + 1,
        )
        return HandoffResult(
            success=False, cluster=new_cluster, nodes=nodes, new_coordinator_id=None
        )

    candidates.sort(key=lambda n: n.coordinator_time_seconds)
    new_coord = candidates[0]

    # 1 % random handoff failure
    if rng.random() < 0.01:
        new_cluster = Cluster(
            id=cluster.id,
            node_ids=list(cluster.node_ids),
            coordinator_id=cluster.coordinator_id,
            regional_coordinator_id=cluster.regional_coordinator_id,
            messages_processed=cluster.messages_processed,
            last_handoff_time=current_time,
            failed_handoffs=cluster.failed_handoffs + 1,
        )
        return HandoffResult(
            success=False, cluster=new_cluster, nodes=nodes, new_coordinator_id=None
        )

    # Successful handoff
    updated_nodes: list[SwarmNode] = []
    for n in nodes:
        if n.id == cluster.coordinator_id:
            updated_nodes.append(
                SwarmNode(
                    id=n.id,
                    status="operational",
                    cluster_id=n.cluster_id,
                    is_coordinator=False,
                    coordinator_time_seconds=n.coordinator_time_seconds,
                    power_consumed_wh=n.power_consumed_wh,
                    messages_sent=n.messages_sent,
                    messages_received=n.messages_received,
                    last_update_time=n.last_update_time,
                    failure_time=n.failure_time,
                )
            )
        elif n.id == new_coord.id:
            updated_nodes.append(
                SwarmNode(
                    id=n.id,
                    status="coordinator",
                    cluster_id=n.cluster_id,
                    is_coordinator=True,
                    coordinator_time_seconds=n.coordinator_time_seconds,
                    power_consumed_wh=n.power_consumed_wh,
                    messages_sent=n.messages_sent,
                    messages_received=n.messages_received,
                    last_update_time=n.last_update_time,
                    failure_time=n.failure_time,
                )
            )
        else:
            updated_nodes.append(n)

    new_cluster = Cluster(
        id=cluster.id,
        node_ids=list(cluster.node_ids),
        coordinator_id=new_coord.id,
        regional_coordinator_id=cluster.regional_coordinator_id,
        messages_processed=cluster.messages_processed,
        last_handoff_time=current_time,
        failed_handoffs=cluster.failed_handoffs,
    )
    return HandoffResult(
        success=True,
        cluster=new_cluster,
        nodes=updated_nodes,
        new_coordinator_id=new_coord.id,
    )


def calculate_power_variance(nodes: list[SwarmNode]) -> float:
    """Return the coefficient of variation of power consumption (percent)."""
    if not nodes:
        return 0.0
    powers = [n.power_consumed_wh for n in nodes]
    mean_p = sum(powers) / len(powers)
    if mean_p == 0.0:
        return 0.0
    variance = sum((p - mean_p) ** 2 for p in powers) / len(powers)
    std_dev = math.sqrt(variance)
    return (std_dev / mean_p) * 100.0


def fail_node(node: SwarmNode, failure_time: float) -> SwarmNode:
    """Return a copy of *node* in ``failed`` status."""
    return SwarmNode(
        id=node.id,
        status="failed",
        cluster_id=node.cluster_id,
        is_coordinator=False,
        coordinator_time_seconds=node.coordinator_time_seconds,
        power_consumed_wh=node.power_consumed_wh,
        messages_sent=node.messages_sent,
        messages_received=node.messages_received,
        last_update_time=node.last_update_time,
        failure_time=failure_time,
    )


def needs_handoff(
    cluster: Cluster,
    current_time: float,
    duty_cycle_seconds: float,
) -> bool:
    """Return ``True`` if the cluster's coordinator needs to hand off."""
    return current_time - cluster.last_handoff_time >= duty_cycle_seconds


def get_operational_nodes(
    nodes: list[SwarmNode],
    cluster_id: str,
) -> list[SwarmNode]:
    """Return operational or coordinator-status nodes in the given cluster."""
    return [
        n
        for n in nodes
        if n.cluster_id == cluster_id and n.status in ("operational", "coordinator")
    ]


def calculate_handoff_time(bandwidth_kbps: float) -> float:
    """Return handoff duration in seconds given *bandwidth_kbps*."""
    transfer_time = (HANDOFF_STATE_SIZE_BYTES * 8) / (bandwidth_kbps * 1_000)
    verification_time = HANDOFF_VERIFICATION_ROUNDS * 0.1
    return transfer_time + verification_time


def calculate_total_energy(nodes: list[SwarmNode]) -> float:
    """Return total energy consumed by all nodes in kWh."""
    return sum(n.power_consumed_wh for n in nodes) / 1_000.0


# ---------------------------------------------------------------------------
# Topology initialization and routing
# ---------------------------------------------------------------------------
def _initialize_centralized(node_count: int) -> NetworkStructure:
    """Build a centralized network where all nodes talk to one coordinator."""
    nodes: list[SwarmNode] = []
    cluster_id = "central"
    central_id = "central-coordinator"
    nodes.append(create_node(central_id, cluster_id, True))
    for i in range(node_count - 1):
        nodes.append(create_node(f"node-{i}", cluster_id, False))
    cluster = Cluster(
        id=cluster_id,
        node_ids=[n.id for n in nodes],
        coordinator_id=central_id,
    )
    return NetworkStructure(
        nodes=nodes, clusters=[cluster], central_coordinator_id=central_id
    )


def _initialize_hierarchical(
    node_count: int, cluster_size: int, rng: Generator
) -> NetworkStructure:
    """Build a hierarchical network with cluster and regional coordinators."""
    nodes: list[SwarmNode] = []
    clusters: list[Cluster] = []
    num_clusters = math.ceil(node_count / cluster_size)
    regional_coordinators: list[str] = []

    node_index = 0
    for c in range(num_clusters):
        region_id = c // 10
        cid = f"cluster-{c}"
        n_in_cluster = min(cluster_size, node_count - node_index)
        coord_id = f"{cid}-node-0"
        cluster, cluster_nodes = create_cluster(cid, n_in_cluster, coord_id)

        if c % 10 == 0:
            regional_coordinators.append(coord_id)
            cluster.regional_coordinator_id = coord_id
        else:
            if region_id < len(regional_coordinators):
                cluster.regional_coordinator_id = regional_coordinators[region_id]

        nodes.extend(cluster_nodes)
        clusters.append(cluster)
        node_index += n_in_cluster

    central_id = regional_coordinators[0] if regional_coordinators else (
        nodes[0].id if nodes else "central-0"
    )
    return NetworkStructure(
        nodes=nodes, clusters=clusters, central_coordinator_id=central_id
    )


def _initialize_mesh(
    node_count: int, rng: Generator
) -> NetworkStructure:
    """Build a mesh network with random gossip neighbours."""
    nodes: list[SwarmNode] = []
    for i in range(node_count):
        nid = f"mesh-node-{i}"
        nodes.append(create_node(nid, "mesh", False))

    gossip_fanout = min(5, math.ceil(math.log2(node_count)))
    mesh_neighbors: dict[str, list[str]] = {}

    for node in nodes:
        candidates = [n.id for n in nodes if n.id != node.id]
        k = min(gossip_fanout, len(candidates))
        chosen_indices = rng.choice(len(candidates), size=k, replace=False)
        mesh_neighbors[node.id] = [candidates[idx] for idx in chosen_indices]

    central_id = nodes[0].id if nodes else "mesh-node-0"
    cluster = Cluster(
        id="mesh",
        node_ids=[n.id for n in nodes],
        coordinator_id=central_id,
    )
    return NetworkStructure(
        nodes=nodes,
        clusters=[cluster],
        central_coordinator_id=central_id,
        mesh_neighbors=mesh_neighbors,
    )


def initialize_network(
    config: SwarmCoordinationConfig,
    rng: Generator,
) -> NetworkStructure:
    """Dispatch to the appropriate topology initializer."""
    topo = config.coordination_topology
    if topo == "centralized":
        return _initialize_centralized(config.node_count)
    if topo == "hierarchical":
        return _initialize_hierarchical(config.node_count, config.cluster_size, rng)
    return _initialize_mesh(config.node_count, rng)


# -- routing ---------------------------------------------------------------
def _centralized_routing(
    network: NetworkStructure,
    source_node_id: str,
) -> list[tuple[str, str]]:
    """Centralized: all messages go to / from the central coordinator."""
    if source_node_id == network.central_coordinator_id:
        return [
            (source_node_id, n.id)
            for n in network.nodes
            if n.id != source_node_id and n.status != "failed"
        ]
    return [(source_node_id, network.central_coordinator_id)]


def _hierarchical_routing(
    network: NetworkStructure,
    source_node_id: str,
) -> list[tuple[str, str]]:
    """Hierarchical: node -> cluster coordinator -> regional -> central."""
    routes: list[tuple[str, str]] = []
    source = network.get_node(source_node_id)
    if source is None:
        return routes
    cluster = network.get_cluster(source.cluster_id) if source.cluster_id else None
    if cluster is None:
        return routes

    if source_node_id == cluster.coordinator_id:
        if (
            cluster.regional_coordinator_id
            and cluster.regional_coordinator_id != source_node_id
        ):
            routes.append((source_node_id, cluster.regional_coordinator_id))
        for nid in cluster.node_ids:
            if nid == source_node_id:
                continue
            node = network.get_node(nid)
            if node and node.status != "failed":
                routes.append((source_node_id, nid))
    else:
        routes.append((source_node_id, cluster.coordinator_id))
    return routes


def _mesh_routing(
    network: NetworkStructure,
    source_node_id: str,
) -> list[tuple[str, str]]:
    """Mesh: gossip to neighbours."""
    neighbors = (network.mesh_neighbors or {}).get(source_node_id, [])
    return [
        (source_node_id, nid)
        for nid in neighbors
        if (lambda n: n is not None and n.status != "failed")(network.get_node(nid))
    ]


def get_message_routing(
    topology: CoordinationTopology,
    network: NetworkStructure,
    source_node_id: str,
) -> list[tuple[str, str]]:
    """Return ``(sender, receiver)`` pairs for an update from *source_node_id*."""
    if topology == "centralized":
        return _centralized_routing(network, source_node_id)
    if topology == "hierarchical":
        return _hierarchical_routing(network, source_node_id)
    return _mesh_routing(network, source_node_id)


def get_hop_count(
    topology: CoordinationTopology,
    node_count: int,
    cluster_size: int,
) -> int:
    """Return the number of hops for message propagation."""
    if topology == "centralized":
        return 2
    if topology == "hierarchical":
        num_clusters = math.ceil(node_count / cluster_size)
        levels = 1 + math.ceil(math.log10(max(1, num_clusters)))
        return levels * 2
    # mesh
    return math.ceil(math.log2(node_count))


def estimate_bottleneck_threshold(
    topology: CoordinationTopology,
    cluster_size: int,
    bandwidth_per_node_kbps: float,
) -> float:
    """Estimate the node count at which latency exceeds 1 second."""
    target_latency_ms = 1_000.0
    processing_delay_ms = 1.0

    if topology == "centralized":
        msgs_per_sec = (bandwidth_per_node_kbps * 1_000) / (
            MESSAGE_SIZES["ephemeris"] * 8
        )
        return math.floor(msgs_per_sec * (target_latency_ms / 1_000))

    if topology == "hierarchical":
        msgs_per_sec = (bandwidth_per_node_kbps * 1_000) / (
            MESSAGE_SIZES["ephemeris"] * 8
        )
        coordinator_capacity = msgs_per_sec * (target_latency_ms / 1_000)
        return coordinator_capacity * cluster_size * 100

    # mesh
    round_time_ms = 10.0 + processing_delay_ms
    max_rounds = target_latency_ms / round_time_ms
    return 2.0 ** max_rounds


# ---------------------------------------------------------------------------
# EventQueue (min-heap on event.time)
# ---------------------------------------------------------------------------
class EventQueue:
    """Priority queue of :class:`SimEvent` objects backed by a binary heap."""

    def __init__(self) -> None:
        self._heap: list[SimEvent] = []

    def push(self, event: SimEvent) -> None:
        """Add an event to the queue."""
        heapq.heappush(self._heap, event)

    def pop(self) -> Optional[SimEvent]:
        """Remove and return the earliest event, or ``None`` if empty."""
        if not self._heap:
            return None
        return heapq.heappop(self._heap)

    def peek(self) -> Optional[SimEvent]:
        """Return the earliest event without removing it."""
        return self._heap[0] if self._heap else None

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def size(self) -> int:
        return len(self._heap)


# ---------------------------------------------------------------------------
# Discrete-event simulator
# ---------------------------------------------------------------------------
class SwarmCoordinationSimulator:
    """Discrete-event simulator for swarm coordination.

    Instantiate with a :class:`SwarmCoordinationConfig` and call
    :meth:`run` to execute the simulation, which returns a
    :class:`SwarmCoordinationRunResult`.
    """

    def __init__(self, config: SwarmCoordinationConfig) -> None:
        self.config = config
        self.rng: Generator = np.random.default_rng(config.seed)
        self.event_queue = EventQueue()
        self.simulation_duration_seconds: float = (
            config.simulation_days * SECONDS_PER_DAY
        )
        self.duty_cycle_seconds: float = config.coordinator_duty_cycle_hours * 3600.0

        # Initialize network
        self.network: NetworkStructure = initialize_network(config, self.rng)
        self.message_queue = MessageQueue(config.node_count * 10)
        self.current_time: float = 0.0
        self.total_messages_sent: int = 0
        self.total_messages_delivered: int = 0
        self.propagation_times: list[float] = []
        self._tier_breakdown = TierMessageBreakdown()

        self._initialize_simulation()

    # -- initialization helpers --------------------------------------------
    def _initialize_simulation(self) -> None:
        """Schedule all starting events."""
        self._schedule_state_sync_events(0.0)
        if self.config.coordination_topology == "hierarchical":
            self._schedule_handoff_events(0.0)
        self._schedule_failure_events()
        if self.config.coordination_topology == "mesh":
            self._schedule_gossip_rounds(0.0)

    def _schedule_state_sync_events(self, start_time: float) -> None:
        """Schedule the first batch of state sync events (lazy scheduling).

        Instead of pre-scheduling events for the entire simulation, schedule
        only the first round.  Each handled ``state_sync`` event re-schedules
        the next round for its node via :meth:`_reschedule_state_sync`.
        """
        self._sync_interval = 60.0 if self.config.coordination_topology == "mesh" else 10.0
        self._sync_sample_rate = min(1.0, 1_000 / self.config.node_count)
        t = start_time
        for node in self.network.nodes:
            if node.status != "failed" and self.rng.random() < self._sync_sample_rate:
                self.event_queue.push(
                    SimEvent(
                        type="state_sync",
                        time=t,
                        node_id=node.id,
                        cluster_id=node.cluster_id,
                    )
                )

    def _reschedule_state_sync(self, node: Node, current_time: float) -> None:
        """Schedule the next state_sync for *node* after the sync interval."""
        next_time = current_time + self._sync_interval
        if next_time < self.simulation_duration_seconds:
            if self.rng.random() < self._sync_sample_rate:
                self.event_queue.push(
                    SimEvent(
                        type="state_sync",
                        time=next_time,
                        node_id=node.id,
                        cluster_id=node.cluster_id,
                    )
                )

    def _schedule_handoff_events(self, start_time: float) -> None:
        """Schedule only the first coordinator handoff per cluster (lazy)."""
        t = start_time + self.duty_cycle_seconds
        if t < self.simulation_duration_seconds:
            for cluster in self.network.clusters:
                self.event_queue.push(
                    SimEvent(
                        type="coordinator_handoff",
                        time=t,
                        node_id=cluster.coordinator_id,
                        cluster_id=cluster.id,
                    )
                )

    def _reschedule_handoff(self, cluster_id: str, current_time: float) -> None:
        """Schedule the next coordinator handoff for *cluster_id*."""
        next_time = current_time + self.duty_cycle_seconds
        if next_time < self.simulation_duration_seconds:
            cluster = self.network.get_cluster(cluster_id)
            if cluster is not None:
                self.event_queue.push(
                    SimEvent(
                        type="coordinator_handoff",
                        time=next_time,
                        node_id=cluster.coordinator_id,
                        cluster_id=cluster.id,
                    )
                )

    def _schedule_gossip_rounds(self, start_time: float) -> None:
        """Schedule only the first gossip round (lazy)."""
        self._gossip_interval = 60.0
        t = start_time
        if t < self.simulation_duration_seconds:
            self.event_queue.push(
                SimEvent(
                    type="gossip_round",
                    time=t,
                    node_id="mesh-coordinator",
                    data={"round": 0},
                )
            )

    def _reschedule_gossip(self, current_time: float, current_round: int) -> None:
        """Schedule the next gossip round."""
        next_time = current_time + self._gossip_interval
        if next_time < self.simulation_duration_seconds:
            self.event_queue.push(
                SimEvent(
                    type="gossip_round",
                    time=next_time,
                    node_id="mesh-coordinator",
                    data={"round": current_round + 1},
                )
            )

    def _schedule_failure_events(self) -> None:
        annual_rate = self.config.node_failure_rate_per_year
        seconds_per_year = 365.0 * 24.0 * 3600.0
        rate_per_second = annual_rate / seconds_per_year

        for node in self.network.nodes:
            if node.is_coordinator:
                continue
            failure_time = self.rng.exponential(1.0 / rate_per_second)
            if failure_time < self.simulation_duration_seconds:
                self.event_queue.push(
                    SimEvent(
                        type="node_failure",
                        time=failure_time,
                        node_id=node.id,
                        cluster_id=node.cluster_id,
                    )
                )

    # -- event loop --------------------------------------------------------
    def run(self) -> SwarmCoordinationRunResult:
        """Execute the full simulation and return the result."""
        events_processed = 0
        max_events = (
            self.config.max_events
            if self.config.max_events is not None
            else self.config.node_count * self.config.simulation_days * 10
        )
        # Batch power updates: only update when >=60s have elapsed
        last_power_time: float = 0.0
        power_update_interval = 60.0

        while not self.event_queue.is_empty() and events_processed < max_events:
            event = self.event_queue.pop()
            if event is None:
                break
            if event.time > self.simulation_duration_seconds:
                break

            # Batch power updates at intervals instead of every event
            if event.time - last_power_time >= power_update_interval:
                elapsed = event.time - last_power_time
                self._update_power_consumption(elapsed)
                last_power_time = event.time

            self.current_time = event.time
            self._process_event(event)
            events_processed += 1

        # Final power update for remaining time
        remaining_power = self.simulation_duration_seconds - last_power_time
        if remaining_power > 0:
            self._update_power_consumption(remaining_power)

        return self._generate_result()

    def _process_event(self, event: SimEvent) -> None:
        handlers = {
            "state_sync": self._handle_state_sync,
            "message_send": self._handle_message_send,
            "message_receive": self._handle_message_receive,
            "coordinator_handoff": self._handle_coordinator_handoff,
            "node_failure": self._handle_node_failure,
            "node_recovery": self._handle_node_recovery,
            "gossip_round": self._handle_gossip_round,
            "collision_warning": self._handle_collision_warning,
        }
        handler = handlers.get(event.type)
        if handler:
            handler(event)

    # -- event handlers ----------------------------------------------------
    def _handle_state_sync(self, event: SimEvent) -> None:
        node = self._find_node(event.node_id)
        if node is None or node.status == "failed":
            return

        routes = get_message_routing(
            self.config.coordination_topology, self.network, event.node_id
        )
        for sender_id, receiver_id in routes:
            msg = create_message(sender_id, receiver_id, "ephemeris", self.current_time)
            if self.message_queue.enqueue(msg):
                self.total_messages_sent += 1
                sender = self._find_node(sender_id)
                if sender:
                    sender.messages_sent += 1
                # Classify message by tier for hierarchical topology
                self._classify_tier_message(sender_id, receiver_id)
                delay_ms = calculate_propagation_delay(
                    self.config.coordination_topology,
                    self.config.node_count,
                    self.config.cluster_size,
                )
                delay_s = delay_ms / 1_000.0
                self.event_queue.push(
                    SimEvent(
                        type="message_receive",
                        time=self.current_time + delay_s,
                        node_id=receiver_id,
                        data={"messageId": msg.id},
                    )
                )
        node.last_update_time = self.current_time
        # Lazy reschedule: queue the next state_sync for this node
        self._reschedule_state_sync(node, self.current_time)

    def _handle_message_send(self, event: SimEvent) -> None:
        # Sending is handled inline in state_sync
        pass

    def _handle_message_receive(self, event: SimEvent) -> None:
        node = self._find_node(event.node_id)
        if node is None or node.status == "failed":
            return

        bandwidth_bps = self.config.bandwidth_per_node_kbps * 1_000
        processed = self.message_queue.process_messages(
            self.current_time, bandwidth_bps, 0.1
        )
        for msg in processed:
            self.total_messages_delivered += 1
            if msg.receive_time is not None:
                prop_ms = (msg.receive_time - msg.send_time) * 1_000
                self.propagation_times.append(prop_ms)
            receiver = self._find_node(msg.receiver_id)
            if receiver:
                receiver.messages_received += 1
                receiver.last_update_time = self.current_time

    def _handle_coordinator_handoff(self, event: SimEvent) -> None:
        cluster = self._find_cluster(event.cluster_id)
        if cluster is None:
            return
        if not needs_handoff(cluster, self.current_time, self.duty_cycle_seconds):
            return
        result = perform_handoff(
            cluster, self.network.nodes, self.current_time, self.rng
        )
        idx = next(
            (i for i, c in enumerate(self.network.clusters) if c.id == cluster.id),
            -1,
        )
        if idx >= 0:
            self.network.clusters[idx] = result.cluster
        self.network.nodes = result.nodes
        # Lazy reschedule next handoff for this cluster
        self._reschedule_handoff(event.cluster_id, self.current_time)

    def _handle_node_failure(self, event: SimEvent) -> None:
        idx = self._find_node_index(event.node_id)
        if idx < 0:
            return
        node = self.network.nodes[idx]
        if node.status == "failed":
            return

        self.network.nodes[idx] = fail_node(node, self.current_time)

        if node.is_coordinator:
            cluster = next(
                (c for c in self.network.clusters if c.coordinator_id == node.id),
                None,
            )
            if cluster:
                self.event_queue.push(
                    SimEvent(
                        type="coordinator_handoff",
                        time=self.current_time + 1.0,
                        node_id=node.id,
                        cluster_id=cluster.id,
                    )
                )

        # Schedule recovery (MTTR 1--7 days)
        mttr_seconds = (self.rng.integers(1, 8)) * SECONDS_PER_DAY
        if self.current_time + mttr_seconds < self.simulation_duration_seconds:
            self.event_queue.push(
                SimEvent(
                    type="node_recovery",
                    time=self.current_time + mttr_seconds,
                    node_id=event.node_id,
                    cluster_id=event.cluster_id,
                )
            )

    def _handle_node_recovery(self, event: SimEvent) -> None:
        idx = self._find_node_index(event.node_id)
        if idx < 0:
            return
        node = self.network.nodes[idx]
        if node.status != "failed":
            return
        self.network.nodes[idx] = SwarmNode(
            id=node.id,
            status="operational",
            cluster_id=node.cluster_id,
            is_coordinator=False,
            coordinator_time_seconds=node.coordinator_time_seconds,
            power_consumed_wh=node.power_consumed_wh,
            messages_sent=node.messages_sent,
            messages_received=node.messages_received,
            last_update_time=node.last_update_time,
            failure_time=None,
        )

    def _handle_gossip_round(self, event: SimEvent) -> None:
        if self.config.coordination_topology != "mesh":
            return
        mesh_neighbors = self.network.mesh_neighbors or {}
        n_nodes = len(self.network.nodes)
        # Sample a fixed number of node indices directly
        n_sample = min(1_000, n_nodes)
        indices = self.rng.choice(n_nodes, size=n_sample, replace=False)
        max_gossip_msgs = min(1_000, n_nodes)
        msgs_this_round = 0

        queue_has_space = not self.message_queue.is_full()
        for idx in indices:
            if msgs_this_round >= max_gossip_msgs or not queue_has_space:
                break
            node = self.network.nodes[idx]
            if node.status == "failed":
                continue
            neighbors = mesh_neighbors.get(node.id, [])
            for nid in neighbors:
                if msgs_this_round >= max_gossip_msgs:
                    break
                neighbor = self.network.get_node(nid)
                if neighbor is None or neighbor.status == "failed":
                    continue
                msg = create_message(node.id, nid, "gossip", self.current_time)
                if self.message_queue.enqueue(msg):
                    self.total_messages_sent += 1
                    node.messages_sent += 1
                    self._tier_breakdown.gossip_msgs += 1
                    msgs_this_round += 1
                else:
                    queue_has_space = False
                    break
            if not queue_has_space:
                break
        # Lazy reschedule next gossip round
        current_round = (event.data or {}).get("round", 0)
        self._reschedule_gossip(self.current_time, current_round)

    def _handle_collision_warning(self, event: SimEvent) -> None:
        self.total_messages_sent += 1

    # -- power update ------------------------------------------------------
    def _update_power_consumption(self, elapsed_seconds: float) -> None:
        if elapsed_seconds <= 0:
            return
        base_w = self.config.base_power_w
        coord_w = self.config.coordinator_power_w
        hours = elapsed_seconds / 3600.0
        for node in self.network.nodes:
            power = coord_w if node.is_coordinator else base_w
            node.power_consumed_wh += power * hours
            if node.is_coordinator:
                node.coordinator_time_seconds += elapsed_seconds

    # -- result generation -------------------------------------------------
    def _generate_result(self) -> SwarmCoordinationRunResult:
        queue_stats = self.message_queue.get_stats()
        prop_stats = self.message_queue.get_propagation_stats()

        required_kbps = calculate_bandwidth_requirement(
            self.config.coordination_topology,
            self.config.node_count,
            self.config.cluster_size,
            10.0,
        )
        overhead = calculate_communication_overhead(
            required_kbps, self.config.bandwidth_per_node_kbps, self.config.node_count
        )
        bottleneck = estimate_bottleneck_threshold(
            self.config.coordination_topology,
            self.config.cluster_size,
            self.config.bandwidth_per_node_kbps,
        )

        coord_availability = 100.0
        if self.config.coordination_topology == "hierarchical":
            avails = [
                calculate_coordinator_availability(
                    c, self.network.nodes, self.simulation_duration_seconds
                )
                for c in self.network.clusters
            ]
            if avails:
                coord_availability = sum(avails) / len(avails)

        power_var = calculate_power_variance(self.network.nodes)
        total_failed = sum(c.failed_handoffs for c in self.network.clusters)

        avg_prop = prop_stats.avg_propagation_ms
        max_prop = prop_stats.max_propagation_ms
        if self.propagation_times:
            avg_prop = sum(self.propagation_times) / len(self.propagation_times)
            max_prop = max(self.propagation_times)
        if avg_prop == 0.0:
            avg_prop = calculate_propagation_delay(
                self.config.coordination_topology,
                self.config.node_count,
                self.config.cluster_size,
            )
            max_prop = avg_prop * 2.0

        return SwarmCoordinationRunResult(
            run_id=0,
            config=self.config,
            communication_overhead_percent=overhead,
            bottleneck_threshold_nodes=bottleneck,
            coordinator_availability_percent=coord_availability,
            power_variance_percent=power_var,
            avg_update_propagation_ms=avg_prop,
            max_update_propagation_ms=max_prop,
            failed_handoffs=total_failed,
            message_drop_rate=queue_stats["dropRate"],
            total_messages_sent=self.total_messages_sent,
            total_messages_delivered=self.total_messages_delivered,
            avg_messages_per_node_per_day=(
                self.total_messages_sent
                / max(1, self.config.node_count)
                / max(1, self.config.simulation_days)
            ),
            total_energy_kwh=calculate_total_energy(self.network.nodes),
            coordinator_bandwidth_kbps=per_coordinator_bandwidth_kbps(
                self.config.cluster_size, 10.0
            ),
            tier_breakdown=TierMessageBreakdown(
                intra_cluster_msgs=self._tier_breakdown.intra_cluster_msgs,
                inter_cluster_msgs=self._tier_breakdown.inter_cluster_msgs,
                central_msgs=self._tier_breakdown.central_msgs,
                gossip_msgs=self._tier_breakdown.gossip_msgs,
            ),
        )

    # -- helpers -----------------------------------------------------------
    def _classify_tier_message(self, sender_id: str, receiver_id: str) -> None:
        """Classify a message by tier and update the breakdown counters."""
        if self.config.coordination_topology != "hierarchical":
            # For non-hierarchical topologies, all sync messages are intra-cluster
            self._tier_breakdown.intra_cluster_msgs += 1
            return

        sender = self._find_node(sender_id)
        receiver = self._find_node(receiver_id)
        if sender is None or receiver is None:
            self._tier_breakdown.intra_cluster_msgs += 1
            return

        # Check if receiver is the central coordinator
        if receiver_id == self.network.central_coordinator_id and sender_id != receiver_id:
            # Check if sender is a regional coordinator (i.e. it is a cluster
            # coordinator that also serves as regional coordinator and is sending
            # to central) -- treat as central tier message
            sender_cluster = self._find_cluster(sender.cluster_id)
            if sender_cluster and sender_cluster.regional_coordinator_id == sender_id:
                self._tier_breakdown.central_msgs += 1
                return

        # Check if receiver is a regional coordinator (inter-cluster message)
        sender_cluster = self._find_cluster(sender.cluster_id)
        if sender_cluster is not None:
            regional_id = sender_cluster.regional_coordinator_id
            if regional_id and receiver_id == regional_id and sender_id != receiver_id:
                # Sender is a cluster coordinator sending to regional coordinator
                if sender.is_coordinator:
                    self._tier_breakdown.inter_cluster_msgs += 1
                    return

        # Default: intra-cluster message (member <-> coordinator)
        self._tier_breakdown.intra_cluster_msgs += 1

    def _find_node(self, node_id: str) -> Optional[SwarmNode]:
        return self.network.get_node(node_id)

    def _find_node_index(self, node_id: str) -> int:
        return self.network._node_map.get(node_id, -1)

    def _find_cluster(self, cluster_id: Optional[str]) -> Optional[Cluster]:
        if cluster_id is None:
            return None
        return self.network.get_cluster(cluster_id)


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import time

    print("=" * 72)
    print("Swarm Coordination Model -- single-run demo")
    print("=" * 72)

    cfg = SwarmCoordinationConfig(
        node_count=1_000,
        coordination_topology="hierarchical",
        cluster_size=100,
        coordinator_duty_cycle_hours=24,
        bandwidth_per_node_kbps=1.0,
        node_failure_rate_per_year=0.02,
        coordinator_power_w=18.0,
        base_power_w=5.0,
        simulation_days=30,
        seed=42,
    )

    print(f"\nConfig: {cfg.node_count} nodes, {cfg.coordination_topology} topology, "
          f"{cfg.simulation_days} days")

    t0 = time.perf_counter()
    sim = SwarmCoordinationSimulator(cfg)
    result = sim.run()
    elapsed = time.perf_counter() - t0

    print(f"\nSimulation completed in {elapsed:.2f} s")
    print(f"  Communication overhead : {result.communication_overhead_percent:.2f} %")
    print(f"  Bottleneck threshold   : {result.bottleneck_threshold_nodes:,.0f} nodes")
    print(f"  Coordinator availability: {result.coordinator_availability_percent:.2f} %")
    print(f"  Power variance         : {result.power_variance_percent:.2f} %")
    print(f"  Avg propagation delay  : {result.avg_update_propagation_ms:.2f} ms")
    print(f"  Max propagation delay  : {result.max_update_propagation_ms:.2f} ms")
    print(f"  Failed handoffs        : {result.failed_handoffs}")
    print(f"  Message drop rate      : {result.message_drop_rate:.4f}")
    print(f"  Total messages sent    : {result.total_messages_sent:,}")
    print(f"  Total messages delivered: {result.total_messages_delivered:,}")
    print(f"  Avg msgs/node/day      : {result.avg_messages_per_node_per_day:.2f}")
    print(f"  Total energy           : {result.total_energy_kwh:.2f} kWh")
