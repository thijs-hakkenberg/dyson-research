/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * tdma-net-device.h — Custom TDMA MAC for swarm cluster coordination
 *
 * Implements a TDMA medium access control layer on top of NS-3's
 * PointToPointNetDevice.  Each member node transmits its ephemeris
 * report in an assigned slot; the coordinator receives during the
 * ingress phase and transmits during the egress phase (half-duplex).
 *
 * Key design decisions:
 *
 * 1. NOT a full NetDevice replacement — we wrap PointToPointNetDevice
 *    and add TDMA timing discipline.  This leverages NS-3's proven
 *    link-layer implementation while adding our scheduling logic.
 *
 * 2. Half-duplex enforcement: the coordinator physically cannot
 *    transmit while receiving.  The TX/RX turnaround time models
 *    the hardware switching delay in real CCSDS Proximity-1 radios.
 *
 * 3. Stochastic acquisition: each slot's acquisition time is drawn
 *    from a LogNormal distribution, modeling real-world variability
 *    in antenna beam acquisition.  This is a key source of timing
 *    jitter that the analytical model approximates with a fixed mean.
 *
 * 4. Per-slot GE channel transitions: the link error model transitions
 *    independently for each member's link, modeling the physical
 *    reality that different nodes experience different propagation
 *    conditions.
 *
 * This implementation deliberately does NOT use the Python model's
 * equations.  Slot timing emerges from the physical parameters.
 */

#ifndef TDMA_NET_DEVICE_H
#define TDMA_NET_DEVICE_H

#include "ns3/net-device.h"
#include "ns3/packet.h"
#include "ns3/nstime.h"
#include "ns3/event-id.h"
#include "ns3/traced-callback.h"
#include "ns3/data-rate.h"
#include "ns3/ptr.h"
#include "ns3/mac48-address.h"

#include "tdma-scheduler.h"
#include "ge-channel-model.h"

#include <vector>
#include <map>

namespace ns3 {

class Node;
class Channel;
class PointToPointNetDevice;

/**
 * \brief Role of a node in the TDMA cluster.
 */
enum TdmaNodeRole
{
    TDMA_COORDINATOR = 0,  //!< Cluster coordinator (receives ingress, sends egress)
    TDMA_MEMBER      = 1   //!< Cluster member (sends ephemeris in assigned slot)
};

/**
 * \brief Per-cycle statistics collected by the TDMA device.
 */
struct TdmaCycleStats
{
    uint32_t cycleNumber;
    uint32_t reportsSent;
    uint32_t reportsReceived;
    uint32_t reportsLost;
    uint32_t retransmissions;
    double   ingressDurationSec;
    double   egressDurationSec;
    double   marginSec;
    bool     deadlineMiss;
    double   actualGamma;  //!< Measured gamma for this cycle
};

/**
 * \brief TDMA MAC layer for swarm cluster coordination.
 *
 * This is not a full NS-3 NetDevice — it is a coordination layer
 * that sits on top of PointToPointNetDevice links and enforces
 * TDMA slot discipline.  It manages:
 *
 * - Slot timing and scheduling
 * - Half-duplex ingress/egress phasing
 * - GE channel error model per link
 * - Stochastic acquisition time per slot
 * - Deadline tracking and cycle statistics
 * - ARQ (stop-and-wait) within cycle margin
 */
class TdmaNetDevice : public Object
{
public:
    static TypeId GetTypeId (void);

    TdmaNetDevice ();
    virtual ~TdmaNetDevice ();

    /**
     * \brief Set this device's role (coordinator or member).
     */
    void SetRole (TdmaNodeRole role);

    /**
     * \brief Get this device's role.
     */
    TdmaNodeRole GetRole (void) const;

    /**
     * \brief Set the member index (0-based) for slot assignment.
     *
     * Only meaningful for TDMA_MEMBER role.
     */
    void SetMemberIndex (uint32_t idx);

    /**
     * \brief Get the member index.
     */
    uint32_t GetMemberIndex (void) const;

    /**
     * \brief Attach the TDMA scheduler.
     */
    void SetScheduler (Ptr<TdmaScheduler> scheduler);

    /**
     * \brief Get the attached scheduler.
     */
    Ptr<TdmaScheduler> GetScheduler (void) const;

    /**
     * \brief Attach a GE channel error model for this link.
     */
    void SetGeChannel (Ptr<GeChannelModel> geModel);

    /**
     * \brief Get the GE channel model.
     */
    Ptr<GeChannelModel> GetGeChannel (void) const;

    /**
     * \brief Set the NS-3 node this device belongs to.
     */
    void SetNode (Ptr<Node> node);

    /**
     * \brief Get the NS-3 node.
     */
    Ptr<Node> GetNode (void) const;

    /**
     * \brief Start TDMA operation — begin cycling.
     *
     * Must be called after all configuration is complete.
     * Schedules the first cycle start event.
     */
    void Start (void);

    /**
     * \brief Get all collected cycle statistics.
     */
    const std::vector<TdmaCycleStats>& GetCycleStats (void) const;

    /**
     * \brief Get aggregate statistics across all cycles.
     */
    struct AggregateStats
    {
        uint32_t totalCycles;
        uint32_t totalReportsSent;
        uint32_t totalReportsReceived;
        uint32_t totalDeadlineMisses;
        uint32_t totalRetransmissions;
        double   meanGamma;
        double   meanMarginSec;
        double   minMarginSec;
        double   deliveryRate;
        double   deadlineMissRate;
    };

    AggregateStats GetAggregateStats (void) const;

    /**
     * \brief Set the number of cycles to simulate.
     */
    void SetNumCycles (uint32_t nCycles);

    /**
     * \brief Set the payload size for ephemeris reports (bytes).
     */
    void SetPayloadBytes (uint32_t bytes);

    /**
     * \brief Get the payload size.
     */
    uint32_t GetPayloadBytes (void) const;

    /**
     * \brief Set the number of ARQ retransmission attempts.
     */
    void SetMaxRetransmissions (uint32_t maxRetx);

    /**
     * \brief Enable stochastic acquisition time.
     */
    void SetStochasticAcquisition (bool enable);

    /**
     * \brief Callback signature for per-cycle reports.
     */
    typedef void (*CycleCompleteCallback)(TdmaCycleStats stats);

private:
    /**
     * \brief Start a new TDMA cycle.
     *
     * Called at the beginning of each T_c interval.  Schedules:
     * - Member slot transmissions (ingress phase)
     * - GE state transitions per member link
     * - Turnaround delay
     * - Egress phase
     * - Next cycle start
     */
    void StartCycle (void);

    /**
     * \brief Handle a member's slot transmission.
     *
     * Called at member i's assigned slot time.  Draws stochastic
     * acquisition time, applies GE channel, creates and "sends"
     * the ephemeris packet.
     *
     * \param memberIdx The 0-based member index
     */
    void HandleMemberSlot (uint32_t memberIdx);

    /**
     * \brief Handle a retransmission attempt for a failed slot.
     *
     * Called when ARQ is enabled and a previous transmission was lost.
     *
     * \param memberIdx The 0-based member index
     * \param retryNum Current retry attempt number (1-based)
     */
    void HandleRetransmission (uint32_t memberIdx, uint32_t retryNum);

    /**
     * \brief Handle the egress phase (coordinator -> members).
     *
     * The coordinator sends summary + heartbeat after turnaround.
     */
    void HandleEgressPhase (void);

    /**
     * \brief Complete the current cycle and record statistics.
     */
    void CompleteCycle (void);

    /**
     * \brief Draw acquisition time for a slot (stochastic or fixed).
     */
    double DrawSlotAcquisitionSec (void) const;

    // Configuration
    TdmaNodeRole m_role;
    uint32_t     m_memberIndex;
    uint32_t     m_numCycles;
    uint32_t     m_payloadBytes;
    uint32_t     m_maxRetransmissions;
    bool         m_stochasticAcq;

    // Components
    Ptr<TdmaScheduler>   m_scheduler;
    Ptr<GeChannelModel>  m_geChannel;
    Ptr<Node>            m_node;

    // Cycle tracking
    uint32_t m_currentCycle;
    double   m_cycleStartTime;     //!< Absolute time of current cycle start
    double   m_currentIngressTime; //!< Accumulated ingress time this cycle
    uint32_t m_reportsReceived;    //!< Reports received this cycle
    uint32_t m_reportsSent;        //!< Reports sent this cycle
    uint32_t m_reportsLost;        //!< Reports lost this cycle
    uint32_t m_retransmissions;    //!< Retransmissions this cycle

    // Per-member GE states (coordinator only)
    std::vector<Ptr<GeChannelModel>> m_memberGeChannels;

    // Per-member loss tracking for ARQ (coordinator only)
    std::vector<bool> m_memberSlotSuccess;

    // Statistics
    std::vector<TdmaCycleStats> m_cycleStats;

    // Traced callbacks
    TracedCallback<TdmaCycleStats> m_cycleCompleteTrace;
};

} // namespace ns3

#endif // TDMA_NET_DEVICE_H
