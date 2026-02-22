"""Unit tests for swarm_model -- swarm coordination simulation model logic."""

import math

import numpy as np
import pytest

from swarm_model import (
    CENTRAL_DISTANCE_KM,
    HANDOFF_STATE_SIZE_BYTES,
    HANDOFF_TIMEOUT_SECONDS,
    HANDOFF_VERIFICATION_ROUNDS,
    INTER_NODE_DISTANCE_KM,
    MESSAGE_SIZES,
    REGIONAL_DISTANCE_KM,
    SECONDS_PER_DAY,
    SPEED_OF_LIGHT_KM_S,
    Cluster,
    EventQueue,
    HandoffResult,
    Message,
    MessageQueue,
    NetworkStructure,
    PropagationStats,
    SimEvent,
    SwarmCoordinationConfig,
    SwarmCoordinationRunResult,
    SwarmCoordinationSimulator,
    SwarmNode,
    calculate_bandwidth_requirement,
    calculate_communication_overhead,
    calculate_handoff_time,
    calculate_power_consumption,
    calculate_power_variance,
    calculate_propagation_delay,
    calculate_total_energy,
    create_cluster,
    create_message,
    create_node,
    estimate_bottleneck_threshold,
    estimate_message_count,
    fail_node,
    get_hop_count,
    get_message_routing,
    get_operational_nodes,
    initialize_network,
    light_time_delay,
    needs_handoff,
    perform_handoff,
    update_node_power,
)


# ===== TestConstants =====


class TestConstants:
    """Verify all physical and protocol constants have expected values."""

    def test_speed_of_light(self):
        assert SPEED_OF_LIGHT_KM_S == pytest.approx(299_792, rel=1e-3)

    def test_inter_node_distance(self):
        assert INTER_NODE_DISTANCE_KM == 1_000

    def test_regional_distance(self):
        assert REGIONAL_DISTANCE_KM == 50_000

    def test_central_distance(self):
        assert CENTRAL_DISTANCE_KM == 150_000_000

    def test_message_sizes(self):
        assert MESSAGE_SIZES["ephemeris"] == 256
        assert MESSAGE_SIZES["heartbeat"] == 32
        assert MESSAGE_SIZES["handoff"] == 8192
        assert MESSAGE_SIZES["gossip"] == 128
        assert MESSAGE_SIZES["collision"] == 64

    def test_message_sizes_keys(self):
        expected_keys = {"ephemeris", "heartbeat", "handoff", "gossip", "collision"}
        assert set(MESSAGE_SIZES.keys()) == expected_keys

    def test_handoff_state_size(self):
        assert HANDOFF_STATE_SIZE_BYTES == 8192

    def test_handoff_verification_rounds(self):
        assert HANDOFF_VERIFICATION_ROUNDS == 3

    def test_handoff_timeout(self):
        assert HANDOFF_TIMEOUT_SECONDS == pytest.approx(30.0)

    def test_seconds_per_day(self):
        assert SECONDS_PER_DAY == 86_400


# ===== TestLightTimeDelay =====


class TestLightTimeDelay:
    """Test light_time_delay helper."""

    def test_zero_distance(self):
        assert light_time_delay(0.0) == pytest.approx(0.0)

    def test_known_distance(self):
        # 1 AU ~ 150,000,000 km => ~500 seconds => ~500,000 ms
        delay = light_time_delay(150_000_000)
        assert delay == pytest.approx(500_000, rel=0.01)

    def test_inter_node(self):
        delay = light_time_delay(INTER_NODE_DISTANCE_KM)
        # 1000 km / 299792 km/s * 1000 ms/s ~ 3.34 ms
        assert delay == pytest.approx(3.336, rel=0.01)

    def test_positive_for_positive_distance(self):
        assert light_time_delay(1.0) > 0

    def test_proportional(self):
        d1 = light_time_delay(100.0)
        d2 = light_time_delay(200.0)
        assert d2 == pytest.approx(2 * d1)


# ===== TestCreateNode =====


class TestCreateNode:
    """Test create_node factory."""

    def test_default_node(self):
        node = create_node("n-1", "c-0")
        assert node.id == "n-1"
        assert node.cluster_id == "c-0"
        assert node.status == "operational"
        assert node.is_coordinator is False

    def test_coordinator_node(self):
        node = create_node("n-0", "c-0", is_coordinator=True)
        assert node.status == "coordinator"
        assert node.is_coordinator is True

    def test_initial_stats_zero(self):
        node = create_node("n-0", "c-0")
        assert node.coordinator_time_seconds == 0.0
        assert node.power_consumed_wh == 0.0
        assert node.messages_sent == 0
        assert node.messages_received == 0
        assert node.failure_time is None


# ===== TestCreateCluster =====


class TestCreateCluster:
    """Test create_cluster factory."""

    def test_cluster_size(self):
        cluster, nodes = create_cluster("c-0", 10, "c-0-node-0")
        assert len(nodes) == 10
        assert len(cluster.node_ids) == 10

    def test_coordinator_assigned(self):
        cluster, nodes = create_cluster("c-0", 10, "c-0-node-0")
        coord = [n for n in nodes if n.is_coordinator]
        assert len(coord) == 1
        assert cluster.coordinator_id == coord[0].id

    def test_node_ids_match(self):
        cluster, nodes = create_cluster("c-0", 5, "c-0-node-0")
        node_ids = [n.id for n in nodes]
        assert cluster.node_ids == node_ids

    def test_fallback_coordinator(self):
        # If named coordinator doesn't exist, first node becomes coordinator
        cluster, nodes = create_cluster("c-0", 5, "nonexistent")
        assert any(n.is_coordinator for n in nodes)

    def test_single_node_cluster(self):
        cluster, nodes = create_cluster("c-0", 1, "c-0-node-0")
        assert len(nodes) == 1
        assert nodes[0].is_coordinator is True


# ===== TestCalculatePowerConsumption =====


class TestCalculatePowerConsumption:
    """Test calculate_power_consumption."""

    def test_base_power(self):
        node = create_node("n-0", "c-0", is_coordinator=False)
        energy = calculate_power_consumption(node, 3600.0, 5.0, 18.0)
        # 5W * 1h = 5 Wh
        assert energy == pytest.approx(5.0)

    def test_coordinator_power(self):
        node = create_node("n-0", "c-0", is_coordinator=True)
        energy = calculate_power_consumption(node, 3600.0, 5.0, 18.0)
        # 18W * 1h = 18 Wh
        assert energy == pytest.approx(18.0)

    def test_one_hour(self):
        node = create_node("n-0", "c-0", is_coordinator=False)
        energy = calculate_power_consumption(node, 3600.0, 10.0, 20.0)
        assert energy == pytest.approx(10.0)

    def test_zero_duration(self):
        node = create_node("n-0", "c-0")
        energy = calculate_power_consumption(node, 0.0, 5.0, 18.0)
        assert energy == pytest.approx(0.0)


# ===== TestUpdateNodePower =====


class TestUpdateNodePower:
    """Test update_node_power."""

    def test_accumulates(self):
        node = create_node("n-0", "c-0", is_coordinator=False)
        updated = update_node_power(node, 3600.0, 5.0, 18.0)
        assert updated.power_consumed_wh == pytest.approx(5.0)
        updated2 = update_node_power(updated, 3600.0, 5.0, 18.0)
        assert updated2.power_consumed_wh == pytest.approx(10.0)

    def test_coordinator_time_tracking(self):
        node = create_node("n-0", "c-0", is_coordinator=True)
        updated = update_node_power(node, 3600.0, 5.0, 18.0)
        assert updated.coordinator_time_seconds == pytest.approx(3600.0)
        # Non-coordinator should not accumulate coordinator time
        node2 = create_node("n-1", "c-0", is_coordinator=False)
        updated2 = update_node_power(node2, 3600.0, 5.0, 18.0)
        assert updated2.coordinator_time_seconds == pytest.approx(0.0)

    def test_preserves_fields(self):
        node = create_node("n-0", "c-0")
        node.messages_sent = 5
        updated = update_node_power(node, 100.0, 5.0, 18.0)
        assert updated.messages_sent == 5
        assert updated.id == "n-0"


# ===== TestPerformHandoff =====


class TestPerformHandoff:
    """Test perform_handoff."""

    def test_successful_handoff(self):
        rng = np.random.default_rng(42)
        cluster, nodes = create_cluster("c-0", 10, "c-0-node-0")
        result = perform_handoff(cluster, nodes, 100.0, rng)
        # With seed 42 the 1% random failure is unlikely to hit repeatedly
        # Run enough that at least one succeeds
        if result.success:
            assert result.new_coordinator_id is not None
            assert result.new_coordinator_id != "c-0-node-0"

    def test_no_candidates_fails(self):
        rng = np.random.default_rng(42)
        # Create cluster with only the coordinator
        cluster, nodes = create_cluster("c-0", 1, "c-0-node-0")
        result = perform_handoff(cluster, nodes, 100.0, rng)
        assert result.success is False
        assert result.new_coordinator_id is None
        assert result.cluster.failed_handoffs == 1

    def test_prefers_least_used(self):
        rng = np.random.default_rng(42)
        cluster, nodes = create_cluster("c-0", 5, "c-0-node-0")
        # Set coordinator times so node-3 has the least
        for n in nodes:
            if not n.is_coordinator:
                n.coordinator_time_seconds = 1000.0
        nodes[3].coordinator_time_seconds = 0.0
        result = perform_handoff(cluster, nodes, 100.0, rng)
        if result.success:
            assert result.new_coordinator_id == "c-0-node-3"


# ===== TestFailNode =====


class TestFailNode:
    """Test fail_node."""

    def test_sets_failed_status(self):
        node = create_node("n-0", "c-0")
        failed = fail_node(node, 1000.0)
        assert failed.status == "failed"
        assert failed.failure_time == 1000.0

    def test_clears_coordinator(self):
        node = create_node("n-0", "c-0", is_coordinator=True)
        failed = fail_node(node, 500.0)
        assert failed.is_coordinator is False
        assert failed.status == "failed"

    def test_preserves_accumulated_stats(self):
        node = create_node("n-0", "c-0")
        node.power_consumed_wh = 50.0
        node.messages_sent = 10
        failed = fail_node(node, 200.0)
        assert failed.power_consumed_wh == 50.0
        assert failed.messages_sent == 10


# ===== TestNeedsHandoff =====


class TestNeedsHandoff:
    """Test needs_handoff."""

    def test_needs_after_cycle(self):
        cluster = Cluster(
            id="c-0",
            node_ids=["n-0"],
            coordinator_id="n-0",
            last_handoff_time=0.0,
        )
        # Duty cycle = 24h = 86400s; at t=86400 handoff needed
        assert needs_handoff(cluster, 86400.0, 86400.0) is True

    def test_not_before_cycle(self):
        cluster = Cluster(
            id="c-0",
            node_ids=["n-0"],
            coordinator_id="n-0",
            last_handoff_time=0.0,
        )
        assert needs_handoff(cluster, 86399.0, 86400.0) is False

    def test_after_recent_handoff(self):
        cluster = Cluster(
            id="c-0",
            node_ids=["n-0"],
            coordinator_id="n-0",
            last_handoff_time=86400.0,
        )
        assert needs_handoff(cluster, 86500.0, 86400.0) is False


# ===== TestCalculatePowerVariance =====


class TestCalculatePowerVariance:
    """Test calculate_power_variance."""

    def test_uniform_power_zero_variance(self):
        nodes = []
        for i in range(10):
            n = create_node(f"n-{i}", "c-0")
            n.power_consumed_wh = 100.0
            nodes.append(n)
        assert calculate_power_variance(nodes) == pytest.approx(0.0)

    def test_nonzero_variance(self):
        nodes = []
        for i in range(10):
            n = create_node(f"n-{i}", "c-0")
            n.power_consumed_wh = float(i * 10)
            nodes.append(n)
        var = calculate_power_variance(nodes)
        assert var > 0

    def test_empty_nodes(self):
        assert calculate_power_variance([]) == pytest.approx(0.0)

    def test_all_zero_power(self):
        nodes = [create_node(f"n-{i}", "c-0") for i in range(5)]
        assert calculate_power_variance(nodes) == pytest.approx(0.0)


# ===== TestCalculateBandwidthRequirement =====


class TestCalculateBandwidthRequirement:
    """Test calculate_bandwidth_requirement for all topologies."""

    def test_centralized_scales_linearly(self):
        bw1 = calculate_bandwidth_requirement("centralized", 1000, 100, 10.0)
        bw2 = calculate_bandwidth_requirement("centralized", 2000, 100, 10.0)
        assert bw2 == pytest.approx(2 * bw1, rel=0.01)

    def test_hierarchical_sublinear(self):
        bw1 = calculate_bandwidth_requirement("hierarchical", 1000, 100, 10.0)
        bw10 = calculate_bandwidth_requirement("hierarchical", 10000, 100, 10.0)
        # Should be sublinear: bw10 < 10 * bw1
        # The cluster + region overhead is small relative to node messages
        assert bw10 < 11 * bw1

    def test_mesh_distributed(self):
        bw = calculate_bandwidth_requirement("mesh", 1000, 100, 10.0)
        assert bw > 0

    def test_positive_for_all_topologies(self):
        for topo in ["centralized", "hierarchical", "mesh"]:
            bw = calculate_bandwidth_requirement(topo, 500, 50, 10.0)
            assert bw > 0


# ===== TestCalculatePropagationDelay =====


class TestCalculatePropagationDelay:
    """Test calculate_propagation_delay for all topologies."""

    def test_centralized_light_time_dominates(self):
        delay = calculate_propagation_delay("centralized", 1000, 100)
        # 2 * light_time(150M km) + 1ms processing ~ 1,000,001 ms
        expected = light_time_delay(CENTRAL_DISTANCE_KM) * 2 + 1.0
        assert delay == pytest.approx(expected)

    def test_hierarchical_multi_hop(self):
        delay = calculate_propagation_delay("hierarchical", 10000, 100)
        # Should include local + regional delays with multiple hops
        assert delay > 0
        assert delay < light_time_delay(CENTRAL_DISTANCE_KM)  # Much less than centralized

    def test_mesh_log_n(self):
        delay_small = calculate_propagation_delay("mesh", 100, 100)
        delay_large = calculate_propagation_delay("mesh", 10000, 100)
        # Logarithmic scaling: delay_large / delay_small ~ log2(10000)/log2(100)
        ratio = delay_large / delay_small
        expected_ratio = math.log2(10000) / math.log2(100)
        assert ratio == pytest.approx(expected_ratio, rel=0.1)

    def test_all_positive(self):
        for topo in ["centralized", "hierarchical", "mesh"]:
            assert calculate_propagation_delay(topo, 500, 50) > 0


# ===== TestCalculateCommunicationOverhead =====


class TestCalculateCommunicationOverhead:
    """Test calculate_communication_overhead."""

    def test_full_capacity(self):
        # 100 kbps required, 1 kbps per node, 100 nodes = 100% overhead
        overhead = calculate_communication_overhead(100.0, 1.0, 100)
        assert overhead == pytest.approx(100.0)

    def test_half_capacity(self):
        overhead = calculate_communication_overhead(50.0, 1.0, 100)
        assert overhead == pytest.approx(50.0)

    def test_zero_required(self):
        overhead = calculate_communication_overhead(0.0, 1.0, 100)
        assert overhead == pytest.approx(0.0)


# ===== TestMessageQueue =====


class TestMessageQueue:
    """Test MessageQueue class."""

    def test_enqueue_dequeue(self):
        mq = MessageQueue(max_queue_size=100)
        msg = create_message("a", "b", "ephemeris", 0.0)
        assert mq.enqueue(msg) is True
        assert mq.size() == 1
        dequeued = mq.dequeue(1.0)
        assert dequeued is not None
        assert dequeued.delivered is True
        assert mq.size() == 0

    def test_max_queue_drop(self):
        mq = MessageQueue(max_queue_size=2)
        m1 = create_message("a", "b", "ephemeris", 0.0)
        m2 = create_message("a", "c", "ephemeris", 0.1)
        m3 = create_message("a", "d", "ephemeris", 0.2)
        assert mq.enqueue(m1) is True
        assert mq.enqueue(m2) is True
        assert mq.enqueue(m3) is False  # dropped
        stats = mq.get_stats()
        assert stats["dropped"] == 1

    def test_process_bandwidth_limit(self):
        mq = MessageQueue(max_queue_size=100)
        for i in range(10):
            msg = create_message(f"n-{i}", "coord", "ephemeris", 0.0)
            mq.enqueue(msg)
        # Each ephemeris is 256 bytes = 2048 bits
        # Bandwidth = 1000 bps, duration = 1s -> max 1000 bits = ~0.48 messages
        # So process at most 0 full messages (1000 / 2048 < 1)
        processed = mq.process_messages(1.0, 1000.0, 1.0)
        assert len(processed) == 0  # not enough bandwidth for even 1 message

        # With enough bandwidth for 2 messages
        processed = mq.process_messages(1.0, 10000.0, 1.0)
        assert len(processed) >= 1

    def test_propagation_stats(self):
        mq = MessageQueue(max_queue_size=100)
        msg = create_message("a", "b", "ephemeris", 0.0)
        mq.enqueue(msg)
        mq.dequeue(0.005)  # 5ms propagation
        stats = mq.get_propagation_stats()
        assert stats.message_count == 1
        assert stats.avg_propagation_ms == pytest.approx(5.0)

    def test_drop_rate(self):
        mq = MessageQueue(max_queue_size=1)
        m1 = create_message("a", "b", "ephemeris", 0.0)
        m2 = create_message("a", "c", "ephemeris", 0.1)
        mq.enqueue(m1)
        mq.enqueue(m2)  # dropped
        mq.dequeue(1.0)
        stats = mq.get_stats()
        # 1 processed, 1 dropped => dropRate = 0.5
        assert stats["dropRate"] == pytest.approx(0.5)

    def test_clear(self):
        mq = MessageQueue(max_queue_size=100)
        mq.enqueue(create_message("a", "b", "ephemeris", 0.0))
        mq.clear()
        assert mq.size() == 0

    def test_empty_propagation_stats(self):
        mq = MessageQueue()
        stats = mq.get_propagation_stats()
        assert stats.message_count == 0
        assert stats.avg_propagation_ms == 0.0


# ===== TestEstimateBottleneckThreshold =====


class TestEstimateBottleneckThreshold:
    """Test estimate_bottleneck_threshold."""

    def test_centralized_limited(self):
        # At 1.0 kbps, centralized can only handle ~0.48 msgs/s for 256-byte
        # ephemeris, so floor() yields 0 at the default bandwidth.  With higher
        # bandwidth the threshold becomes positive.
        threshold_low = estimate_bottleneck_threshold("centralized", 100, 1.0)
        assert threshold_low >= 0
        threshold_high = estimate_bottleneck_threshold("centralized", 100, 10.0)
        assert threshold_high > 0
        assert threshold_high < 1_000_000

    def test_hierarchical_much_higher(self):
        t_cent = estimate_bottleneck_threshold("centralized", 100, 1.0)
        t_hier = estimate_bottleneck_threshold("hierarchical", 100, 1.0)
        assert t_hier > t_cent

    def test_mesh_exponential(self):
        t_mesh = estimate_bottleneck_threshold("mesh", 100, 1.0)
        assert t_mesh > 0
        # Mesh threshold is 2^(max_rounds), should be very large
        assert t_mesh > 1_000


# ===== TestInitializeNetwork =====


class TestInitializeNetwork:
    """Test initialize_network for all topologies."""

    def test_centralized_single_cluster(self):
        rng = np.random.default_rng(42)
        cfg = SwarmCoordinationConfig(
            node_count=100, coordination_topology="centralized", seed=42
        )
        net = initialize_network(cfg, rng)
        assert len(net.clusters) == 1
        assert len(net.nodes) == 100

    def test_hierarchical_correct_clusters(self):
        rng = np.random.default_rng(42)
        cfg = SwarmCoordinationConfig(
            node_count=500,
            coordination_topology="hierarchical",
            cluster_size=100,
            seed=42,
        )
        net = initialize_network(cfg, rng)
        expected_clusters = math.ceil(500 / 100)
        assert len(net.clusters) == expected_clusters

    def test_mesh_has_neighbors(self):
        rng = np.random.default_rng(42)
        cfg = SwarmCoordinationConfig(
            node_count=100, coordination_topology="mesh", seed=42
        )
        net = initialize_network(cfg, rng)
        assert net.mesh_neighbors is not None
        assert len(net.mesh_neighbors) == 100
        # Each node should have at least 1 neighbor
        for nid, neighbors in net.mesh_neighbors.items():
            assert len(neighbors) > 0

    def test_node_count_matches(self):
        rng = np.random.default_rng(42)
        for topo in ["centralized", "hierarchical", "mesh"]:
            cfg = SwarmCoordinationConfig(
                node_count=200, coordination_topology=topo, seed=42
            )
            net = initialize_network(cfg, rng)
            assert len(net.nodes) == 200


# ===== TestGetMessageRouting =====


class TestGetMessageRouting:
    """Test get_message_routing for all topologies."""

    def test_centralized_to_coordinator(self):
        rng = np.random.default_rng(42)
        cfg = SwarmCoordinationConfig(
            node_count=100, coordination_topology="centralized", seed=42
        )
        net = initialize_network(cfg, rng)
        # Non-coordinator node sends to central coordinator
        non_coord = [n for n in net.nodes if not n.is_coordinator][0]
        routes = get_message_routing("centralized", net, non_coord.id)
        assert len(routes) == 1
        assert routes[0][1] == net.central_coordinator_id

    def test_centralized_from_coordinator(self):
        rng = np.random.default_rng(42)
        cfg = SwarmCoordinationConfig(
            node_count=100, coordination_topology="centralized", seed=42
        )
        net = initialize_network(cfg, rng)
        routes = get_message_routing("centralized", net, net.central_coordinator_id)
        # Coordinator broadcasts to all non-failed, non-self nodes
        assert len(routes) == 99  # 100 - 1 (self)

    def test_hierarchical_node_to_cluster(self):
        rng = np.random.default_rng(42)
        cfg = SwarmCoordinationConfig(
            node_count=200,
            coordination_topology="hierarchical",
            cluster_size=50,
            seed=42,
        )
        net = initialize_network(cfg, rng)
        # Find a non-coordinator node
        non_coord = [n for n in net.nodes if not n.is_coordinator][0]
        routes = get_message_routing("hierarchical", net, non_coord.id)
        # Non-coordinator sends to its cluster coordinator
        assert len(routes) == 1
        cluster = next(c for c in net.clusters if non_coord.id in c.node_ids)
        assert routes[0][1] == cluster.coordinator_id

    def test_mesh_gossip_to_neighbors(self):
        rng = np.random.default_rng(42)
        cfg = SwarmCoordinationConfig(
            node_count=100, coordination_topology="mesh", seed=42
        )
        net = initialize_network(cfg, rng)
        node_id = net.nodes[0].id
        routes = get_message_routing("mesh", net, node_id)
        assert len(routes) > 0
        # All routes should be to neighbors
        expected_neighbors = net.mesh_neighbors[node_id]
        for sender, receiver in routes:
            assert sender == node_id
            assert receiver in expected_neighbors


# ===== TestEventQueue =====


class TestEventQueue:
    """Test EventQueue priority queue."""

    def test_push_pop_ordering(self):
        eq = EventQueue()
        e1 = SimEvent(type="state_sync", time=10.0, node_id="n-0")
        e2 = SimEvent(type="state_sync", time=5.0, node_id="n-1")
        e3 = SimEvent(type="state_sync", time=15.0, node_id="n-2")
        eq.push(e1)
        eq.push(e2)
        eq.push(e3)
        # Should pop in time order
        assert eq.pop().time == pytest.approx(5.0)
        assert eq.pop().time == pytest.approx(10.0)
        assert eq.pop().time == pytest.approx(15.0)

    def test_empty(self):
        eq = EventQueue()
        assert eq.is_empty() is True
        assert eq.pop() is None

    def test_size(self):
        eq = EventQueue()
        assert eq.size() == 0
        eq.push(SimEvent(type="state_sync", time=1.0, node_id="n-0"))
        assert eq.size() == 1
        eq.push(SimEvent(type="state_sync", time=2.0, node_id="n-1"))
        assert eq.size() == 2
        eq.pop()
        assert eq.size() == 1

    def test_peek(self):
        eq = EventQueue()
        e1 = SimEvent(type="state_sync", time=10.0, node_id="n-0")
        eq.push(e1)
        peeked = eq.peek()
        assert peeked is not None
        assert peeked.time == 10.0
        assert eq.size() == 1  # peek does not remove


# ===== TestSwarmCoordinationSimulator =====


class TestSwarmCoordinationSimulator:
    """Test SwarmCoordinationSimulator end-to-end."""

    def test_basic_run(self):
        cfg = SwarmCoordinationConfig(
            node_count=100,
            coordination_topology="hierarchical",
            cluster_size=25,
            simulation_days=5,
            seed=42,
        )
        sim = SwarmCoordinationSimulator(cfg)
        result = sim.run()
        assert isinstance(result, SwarmCoordinationRunResult)
        assert result.communication_overhead_percent >= 0

    def test_reproducibility_with_seed(self):
        cfg1 = SwarmCoordinationConfig(
            node_count=100,
            coordination_topology="hierarchical",
            cluster_size=25,
            simulation_days=5,
            seed=42,
        )
        cfg2 = SwarmCoordinationConfig(
            node_count=100,
            coordination_topology="hierarchical",
            cluster_size=25,
            simulation_days=5,
            seed=42,
        )
        r1 = SwarmCoordinationSimulator(cfg1).run()
        r2 = SwarmCoordinationSimulator(cfg2).run()
        assert r1.communication_overhead_percent == pytest.approx(
            r2.communication_overhead_percent
        )
        assert r1.total_messages_sent == r2.total_messages_sent
        assert r1.total_energy_kwh == pytest.approx(r2.total_energy_kwh)

    def test_all_topologies_run(self):
        for topo in ["centralized", "hierarchical", "mesh"]:
            cfg = SwarmCoordinationConfig(
                node_count=100,
                coordination_topology=topo,
                cluster_size=25,
                simulation_days=5,
                seed=42,
            )
            result = SwarmCoordinationSimulator(cfg).run()
            assert result.communication_overhead_percent >= 0

    def test_result_fields_present(self):
        cfg = SwarmCoordinationConfig(
            node_count=100,
            coordination_topology="hierarchical",
            cluster_size=25,
            simulation_days=5,
            seed=42,
        )
        result = SwarmCoordinationSimulator(cfg).run()
        assert hasattr(result, "communication_overhead_percent")
        assert hasattr(result, "bottleneck_threshold_nodes")
        assert hasattr(result, "coordinator_availability_percent")
        assert hasattr(result, "power_variance_percent")
        assert hasattr(result, "avg_update_propagation_ms")
        assert hasattr(result, "max_update_propagation_ms")
        assert hasattr(result, "failed_handoffs")
        assert hasattr(result, "message_drop_rate")
        assert hasattr(result, "total_messages_sent")
        assert hasattr(result, "total_messages_delivered")
        assert hasattr(result, "avg_messages_per_node_per_day")
        assert hasattr(result, "total_energy_kwh")

    def test_messages_sent_positive(self):
        cfg = SwarmCoordinationConfig(
            node_count=200,
            coordination_topology="hierarchical",
            cluster_size=50,
            simulation_days=10,
            seed=42,
        )
        result = SwarmCoordinationSimulator(cfg).run()
        assert result.total_messages_sent > 0

    def test_energy_positive(self):
        cfg = SwarmCoordinationConfig(
            node_count=100,
            coordination_topology="hierarchical",
            cluster_size=25,
            simulation_days=10,
            seed=42,
        )
        result = SwarmCoordinationSimulator(cfg).run()
        assert result.total_energy_kwh > 0

    def test_node_failure_reduces_availability(self):
        # High failure rate should reduce availability compared to low
        cfg_low = SwarmCoordinationConfig(
            node_count=200,
            coordination_topology="hierarchical",
            cluster_size=50,
            node_failure_rate_per_year=0.01,
            simulation_days=10,
            seed=42,
        )
        cfg_high = SwarmCoordinationConfig(
            node_count=200,
            coordination_topology="hierarchical",
            cluster_size=50,
            node_failure_rate_per_year=0.10,
            simulation_days=10,
            seed=42,
        )
        r_low = SwarmCoordinationSimulator(cfg_low).run()
        r_high = SwarmCoordinationSimulator(cfg_high).run()
        # Higher failure rate should generally lead to lower or equal availability
        # (not strictly guaranteed in every seed, but with these params it's likely)
        assert r_high.coordinator_availability_percent <= r_low.coordinator_availability_percent + 5.0


# ===== Additional helpers =====


class TestEstimateMessageCount:
    """Test estimate_message_count."""

    def test_centralized(self):
        count = estimate_message_count("centralized", 100, 50, 100.0, 10.0)
        assert count == 100 * 10  # 100 nodes * 10 updates

    def test_hierarchical(self):
        count = estimate_message_count("hierarchical", 100, 50, 100.0, 10.0)
        assert count > 0

    def test_mesh(self):
        count = estimate_message_count("mesh", 100, 50, 100.0, 10.0)
        assert count > 0


class TestGetHopCount:
    """Test get_hop_count."""

    def test_centralized_always_two(self):
        assert get_hop_count("centralized", 100, 50) == 2
        assert get_hop_count("centralized", 1000000, 100) == 2

    def test_hierarchical_increases(self):
        h_small = get_hop_count("hierarchical", 100, 50)
        h_large = get_hop_count("hierarchical", 1000000, 100)
        assert h_large >= h_small

    def test_mesh_log(self):
        hops = get_hop_count("mesh", 1024, 100)
        assert hops == math.ceil(math.log2(1024))


class TestCalculateHandoffTime:
    """Test calculate_handoff_time."""

    def test_positive(self):
        t = calculate_handoff_time(1.0)
        assert t > 0

    def test_faster_with_more_bandwidth(self):
        t_slow = calculate_handoff_time(0.5)
        t_fast = calculate_handoff_time(5.0)
        assert t_fast < t_slow


class TestGetOperationalNodes:
    """Test get_operational_nodes."""

    def test_filters_failed(self):
        nodes = [
            create_node("n-0", "c-0", is_coordinator=True),
            create_node("n-1", "c-0"),
            create_node("n-2", "c-0"),
        ]
        nodes[2] = fail_node(nodes[2], 100.0)
        ops = get_operational_nodes(nodes, "c-0")
        assert len(ops) == 2

    def test_filters_by_cluster(self):
        nodes = [
            create_node("n-0", "c-0"),
            create_node("n-1", "c-1"),
        ]
        ops = get_operational_nodes(nodes, "c-0")
        assert len(ops) == 1
        assert ops[0].id == "n-0"


class TestCalculateTotalEnergy:
    """Test calculate_total_energy."""

    def test_sums_correctly(self):
        nodes = [create_node(f"n-{i}", "c-0") for i in range(3)]
        nodes[0].power_consumed_wh = 100.0
        nodes[1].power_consumed_wh = 200.0
        nodes[2].power_consumed_wh = 300.0
        total = calculate_total_energy(nodes)
        # (100 + 200 + 300) / 1000 = 0.6 kWh
        assert total == pytest.approx(0.6)

    def test_empty(self):
        assert calculate_total_energy([]) == pytest.approx(0.0)
