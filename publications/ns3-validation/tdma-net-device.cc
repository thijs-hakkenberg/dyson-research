/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * tdma-net-device.cc — TDMA MAC implementation for swarm cluster
 *
 * This file implements the per-cycle TDMA discipline:
 *
 * Each T_c = 10s cycle proceeds in three phases:
 *
 *   1. INGRESS (members -> coordinator):
 *      - Each of the N-1 members transmits in its assigned slot
 *      - Per-slot timing: data + guard + acquisition (stochastic)
 *      - GE channel determines per-link loss
 *      - Failed packets may be retransmitted (ARQ, stop-and-wait)
 *
 *   2. TURNAROUND (2 ms):
 *      - Coordinator switches from RX to TX mode
 *      - Models real hardware switching delay
 *
 *   3. EGRESS (coordinator -> members):
 *      - Coordinator broadcasts summary + heartbeat
 *      - Optional bitmap ACK (Config D)
 *
 * The cycle deadline is enforced: if ingress + turnaround + egress
 * exceeds T_c, the cycle is marked as a deadline miss.
 *
 * Key difference from analytical model: acquisition times are drawn
 * from a LogNormal distribution per-slot, creating timing jitter that
 * the analytical model handles with a fixed mean.  This produces
 * a distribution of per-cycle ingress times even without channel loss.
 */

#include "tdma-net-device.h"

#include "ns3/log.h"
#include "ns3/simulator.h"
#include "ns3/packet.h"
#include "ns3/uinteger.h"
#include "ns3/boolean.h"

#include <algorithm>
#include <numeric>
#include <cmath>

namespace ns3 {

NS_LOG_COMPONENT_DEFINE ("TdmaNetDevice");
NS_OBJECT_ENSURE_REGISTERED (TdmaNetDevice);

TypeId
TdmaNetDevice::GetTypeId (void)
{
    static TypeId tid = TypeId ("ns3::TdmaNetDevice")
        .SetParent<Object> ()
        .SetGroupName ("Network")
        .AddConstructor<TdmaNetDevice> ()
        .AddTraceSource ("CycleComplete",
                         "Traced callback fired at the end of each TDMA cycle.",
                         MakeTraceSourceAccessor (&TdmaNetDevice::m_cycleCompleteTrace),
                         "ns3::TdmaNetDevice::CycleCompleteCallback")
        ;
    return tid;
}

TdmaNetDevice::TdmaNetDevice ()
    : m_role (TDMA_MEMBER),
      m_memberIndex (0),
      m_numCycles (100),
      m_payloadBytes (256),
      m_maxRetransmissions (0),
      m_stochasticAcq (false),
      m_currentCycle (0),
      m_cycleStartTime (0.0),
      m_currentIngressTime (0.0),
      m_reportsReceived (0),
      m_reportsSent (0),
      m_reportsLost (0),
      m_retransmissions (0)
{
    NS_LOG_FUNCTION (this);
}

TdmaNetDevice::~TdmaNetDevice ()
{
    NS_LOG_FUNCTION (this);
}

void TdmaNetDevice::SetRole (TdmaNodeRole role) { m_role = role; }
TdmaNodeRole TdmaNetDevice::GetRole (void) const { return m_role; }

void TdmaNetDevice::SetMemberIndex (uint32_t idx) { m_memberIndex = idx; }
uint32_t TdmaNetDevice::GetMemberIndex (void) const { return m_memberIndex; }

void TdmaNetDevice::SetScheduler (Ptr<TdmaScheduler> scheduler) { m_scheduler = scheduler; }
Ptr<TdmaScheduler> TdmaNetDevice::GetScheduler (void) const { return m_scheduler; }

void TdmaNetDevice::SetGeChannel (Ptr<GeChannelModel> geModel) { m_geChannel = geModel; }
Ptr<GeChannelModel> TdmaNetDevice::GetGeChannel (void) const { return m_geChannel; }

void TdmaNetDevice::SetNode (Ptr<Node> node) { m_node = node; }
Ptr<Node> TdmaNetDevice::GetNode (void) const { return m_node; }

void TdmaNetDevice::SetNumCycles (uint32_t nCycles) { m_numCycles = nCycles; }
void TdmaNetDevice::SetPayloadBytes (uint32_t bytes) { m_payloadBytes = bytes; }
uint32_t TdmaNetDevice::GetPayloadBytes (void) const { return m_payloadBytes; }
void TdmaNetDevice::SetMaxRetransmissions (uint32_t maxRetx) { m_maxRetransmissions = maxRetx; }
void TdmaNetDevice::SetStochasticAcquisition (bool enable) { m_stochasticAcq = enable; }

void
TdmaNetDevice::Start (void)
{
    NS_LOG_FUNCTION (this);

    if (m_role != TDMA_COORDINATOR)
    {
        NS_LOG_WARN ("Start() called on non-coordinator node; only coordinator drives cycles.");
        return;
    }

    // Create per-member GE channel models
    uint32_t nMembers = m_scheduler->GetNMembers ();
    m_memberGeChannels.resize (nMembers);
    m_memberSlotSuccess.resize (nMembers, false);

    if (m_geChannel && m_geChannel->IsEnabled ())
    {
        for (uint32_t i = 0; i < nMembers; ++i)
        {
            Ptr<GeChannelModel> ge = CreateObject<GeChannelModel> ();
            // Copy parameters from template GE model
            ge->SetPgb (m_geChannel->GetPgb ());
            ge->SetPbg (m_geChannel->GetPbg ());
            ge->SetPLossGood (m_geChannel->GetPLossGood ());
            ge->SetPLossBad (m_geChannel->GetPLossBad ());
            ge->SetFecRate (m_geChannel->GetFecRate ());
            ge->SetPerSlotTransitions (m_geChannel->GetPerSlotTransitions ());
            ge->ResetToSteadyState ();
            m_memberGeChannels[i] = ge;
        }
    }
    else
    {
        // GE disabled: create disabled models to avoid null checks in hot path
        for (uint32_t i = 0; i < nMembers; ++i)
        {
            Ptr<GeChannelModel> ge = CreateObject<GeChannelModel> ();
            ge->SetPLossGood (0.0);
            ge->SetPLossBad (0.0);
            ge->Disable ();
            m_memberGeChannels[i] = ge;
        }
    }

    // Schedule first cycle
    m_currentCycle = 0;
    Simulator::Schedule (Seconds (0.0), &TdmaNetDevice::StartCycle, this);
}

void
TdmaNetDevice::StartCycle (void)
{
    NS_LOG_FUNCTION (this << m_currentCycle);

    if (m_currentCycle >= m_numCycles)
    {
        NS_LOG_INFO ("All " << m_numCycles << " cycles completed.");
        return;
    }

    // Reset per-cycle counters
    m_cycleStartTime = Simulator::Now ().GetSeconds ();
    m_currentIngressTime = 0.0;
    m_reportsReceived = 0;
    m_reportsSent = 0;
    m_reportsLost = 0;
    m_retransmissions = 0;
    std::fill (m_memberSlotSuccess.begin (), m_memberSlotSuccess.end (), false);

    // === GE state transitions (per-cycle) ===
    // Each member's link independently transitions
    for (uint32_t i = 0; i < m_memberGeChannels.size (); ++i)
    {
        m_memberGeChannels[i]->DoTransition ();
    }

    // === Schedule ingress slots ===
    // Each member i transmits at its assigned slot time
    double slotDurationSec = m_scheduler->GetSlotTiming ().totalSlotSec;

    for (uint32_t i = 0; i < m_scheduler->GetNMembers (); ++i)
    {
        Time slotStart = m_scheduler->GetSlotStart (i);
        Simulator::Schedule (slotStart, &TdmaNetDevice::HandleMemberSlot, this, i);
    }

    // Schedule egress phase after all ingress slots + turnaround
    Time egressStart = m_scheduler->GetEgressStart ();
    Simulator::Schedule (egressStart, &TdmaNetDevice::HandleEgressPhase, this);

    // Schedule cycle completion at T_c
    double cycleDuration = m_scheduler->GetCycleDurationSec ();
    Simulator::Schedule (Seconds (cycleDuration), &TdmaNetDevice::CompleteCycle, this);
}

void
TdmaNetDevice::HandleMemberSlot (uint32_t memberIdx)
{
    NS_LOG_FUNCTION (this << memberIdx);

    TdmaSlotTiming timing = m_scheduler->GetSlotTiming ();

    // === Stochastic acquisition time ===
    // If enabled, draw from LogNormal distribution.  This is the key
    // source of per-slot timing jitter that makes NS-3 results
    // naturally differ from the analytical model's fixed-mean assumption.
    double acqTimeSec = DrawSlotAcquisitionSec ();

    // Actual slot duration for this transmission
    double actualSlotSec = timing.dataTimeSec + timing.guardTimeSec + acqTimeSec;
    m_currentIngressTime += actualSlotSec;
    m_reportsSent++;

    // === GE channel: determine if packet is lost ===
    // Create a dummy packet for the error model interface
    Ptr<Packet> pkt = Create<Packet> (m_payloadBytes);
    bool lost = m_memberGeChannels[memberIdx]->DoCorrupt (pkt);

    if (lost)
    {
        m_reportsLost++;
        m_memberSlotSuccess[memberIdx] = false;

        NS_LOG_DEBUG ("Cycle " << m_currentCycle << " member " << memberIdx
                      << ": LOST (GE=" << (m_memberGeChannels[memberIdx]->IsGoodState () ? "G" : "B")
                      << " acq=" << (acqTimeSec * 1000.0) << " ms)");

        // === ARQ: stop-and-wait retransmission ===
        if (m_maxRetransmissions > 0)
        {
            // Schedule first retransmission after the current slot ends
            // The retransmission uses a reserved slot at the end of ingress
            Time retxDelay = Seconds (actualSlotSec * 0.1); // small delay
            Simulator::Schedule (retxDelay,
                                 &TdmaNetDevice::HandleRetransmission,
                                 this, memberIdx, 1);
        }
    }
    else
    {
        m_reportsReceived++;
        m_memberSlotSuccess[memberIdx] = true;

        NS_LOG_DEBUG ("Cycle " << m_currentCycle << " member " << memberIdx
                      << ": OK (GE=" << (m_memberGeChannels[memberIdx]->IsGoodState () ? "G" : "B")
                      << " acq=" << (acqTimeSec * 1000.0) << " ms)");
    }
}

void
TdmaNetDevice::HandleRetransmission (uint32_t memberIdx, uint32_t retryNum)
{
    NS_LOG_FUNCTION (this << memberIdx << retryNum);

    if (retryNum > m_maxRetransmissions)
    {
        return; // No more retries allowed
    }

    if (m_memberSlotSuccess[memberIdx])
    {
        return; // Already succeeded on a previous retry
    }

    m_retransmissions++;

    // GE state may transition between retries
    m_memberGeChannels[memberIdx]->DoTransition ();

    TdmaSlotTiming timing = m_scheduler->GetSlotTiming ();
    double acqTimeSec = DrawSlotAcquisitionSec ();

    double retxSlotSec = timing.dataTimeSec + timing.guardTimeSec + acqTimeSec;
    m_currentIngressTime += retxSlotSec;

    // Retry transmission
    Ptr<Packet> pkt = Create<Packet> (m_payloadBytes);
    bool lost = m_memberGeChannels[memberIdx]->DoCorrupt (pkt);

    if (lost)
    {
        NS_LOG_DEBUG ("Cycle " << m_currentCycle << " member " << memberIdx
                      << " retry " << retryNum << ": LOST");

        if (retryNum < m_maxRetransmissions)
        {
            Time retxDelay = Seconds (retxSlotSec * 0.1);
            Simulator::Schedule (retxDelay,
                                 &TdmaNetDevice::HandleRetransmission,
                                 this, memberIdx, retryNum + 1);
        }
    }
    else
    {
        m_reportsReceived++;
        m_reportsLost--;  // Correct the loss count
        m_memberSlotSuccess[memberIdx] = true;

        NS_LOG_DEBUG ("Cycle " << m_currentCycle << " member " << memberIdx
                      << " retry " << retryNum << ": OK");
    }
}

void
TdmaNetDevice::HandleEgressPhase (void)
{
    NS_LOG_FUNCTION (this);

    // Egress phase: coordinator broadcasts summary + heartbeat.
    // The actual duration is computed by the scheduler.
    // We don't model packet-level egress in detail since the paper
    // focuses on ingress feasibility.  The egress time is budgeted
    // deterministically.

    NS_LOG_DEBUG ("Cycle " << m_currentCycle << " egress phase started"
                  << " at T=" << Simulator::Now ().GetSeconds () << "s");
}

void
TdmaNetDevice::CompleteCycle (void)
{
    NS_LOG_FUNCTION (this << m_currentCycle);

    double cycleDuration = m_scheduler->GetCycleDurationSec ();
    double egressDuration = m_scheduler->GetEgressDurationSec ();
    TdmaSlotTiming timing = m_scheduler->GetSlotTiming ();

    // Total used time
    double turnaroundSec = m_scheduler->GetTurnaroundSec ();
    double totalUsedSec = m_currentIngressTime + turnaroundSec + egressDuration;
    double marginSec = cycleDuration - totalUsedSec;

    // Compute actual gamma for this cycle
    // gamma_measured = (total_payload_bits_received) / (phy_rate * ingress_time)
    double phyRate = timing.codedTotalBits / timing.dataTimeSec;
    double totalPayloadBitsReceived = static_cast<double>(m_reportsReceived)
                                      * timing.payloadBits;
    double actualGamma = (m_currentIngressTime > 0)
                         ? totalPayloadBitsReceived / (phyRate * m_currentIngressTime)
                         : 0.0;

    // Record statistics
    TdmaCycleStats stats;
    stats.cycleNumber = m_currentCycle;
    stats.reportsSent = m_reportsSent;
    stats.reportsReceived = m_reportsReceived;
    stats.reportsLost = m_reportsLost;
    stats.retransmissions = m_retransmissions;
    stats.ingressDurationSec = m_currentIngressTime;
    stats.egressDurationSec = egressDuration;
    stats.marginSec = marginSec;
    stats.deadlineMiss = (marginSec < 0.0);
    stats.actualGamma = actualGamma;

    m_cycleStats.push_back (stats);
    m_cycleCompleteTrace (stats);

    NS_LOG_INFO ("Cycle " << m_currentCycle
                 << ": recv=" << m_reportsReceived << "/" << m_reportsSent
                 << " lost=" << m_reportsLost
                 << " retx=" << m_retransmissions
                 << " ingress=" << (m_currentIngressTime * 1000.0) << " ms"
                 << " margin=" << (marginSec * 1000.0) << " ms"
                 << " gamma=" << actualGamma
                 << (stats.deadlineMiss ? " DEADLINE_MISS" : ""));

    // Schedule next cycle
    m_currentCycle++;
    if (m_currentCycle < m_numCycles)
    {
        // Next cycle starts at the next T_c boundary
        Simulator::Schedule (Seconds (0.0), &TdmaNetDevice::StartCycle, this);
    }
}

const std::vector<TdmaCycleStats>&
TdmaNetDevice::GetCycleStats (void) const
{
    return m_cycleStats;
}

double
TdmaNetDevice::DrawSlotAcquisitionSec (void) const
{
    TdmaSlotTiming timing = m_scheduler->GetSlotTiming ();
    if (m_stochasticAcq)
    {
        return m_scheduler->DrawAcquisitionTimeSec ();
    }
    return timing.acquisitionTimeSec;
}

TdmaNetDevice::AggregateStats
TdmaNetDevice::GetAggregateStats (void) const
{
    AggregateStats agg;
    agg.totalCycles = m_cycleStats.size ();
    agg.totalReportsSent = 0;
    agg.totalReportsReceived = 0;
    agg.totalDeadlineMisses = 0;
    agg.totalRetransmissions = 0;
    agg.meanGamma = 0.0;
    agg.meanMarginSec = 0.0;
    agg.minMarginSec = 1e9;

    for (const auto& s : m_cycleStats)
    {
        agg.totalReportsSent += s.reportsSent;
        agg.totalReportsReceived += s.reportsReceived;
        agg.totalDeadlineMisses += (s.deadlineMiss ? 1 : 0);
        agg.totalRetransmissions += s.retransmissions;
        agg.meanGamma += s.actualGamma;
        agg.meanMarginSec += s.marginSec;
        agg.minMarginSec = std::min (agg.minMarginSec, s.marginSec);
    }

    if (agg.totalCycles > 0)
    {
        agg.meanGamma /= agg.totalCycles;
        agg.meanMarginSec /= agg.totalCycles;
    }

    agg.deliveryRate = (agg.totalReportsSent > 0)
                       ? static_cast<double>(agg.totalReportsReceived) / agg.totalReportsSent
                       : 0.0;
    agg.deadlineMissRate = (agg.totalCycles > 0)
                           ? static_cast<double>(agg.totalDeadlineMisses) / agg.totalCycles
                           : 0.0;

    return agg;
}

} // namespace ns3
