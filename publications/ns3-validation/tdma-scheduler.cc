/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * tdma-scheduler.cc — TDMA slot assignment implementation
 *
 * Computes TDMA slot timing entirely from first principles:
 *   payload bytes -> framing overhead -> FEC expansion -> PHY rate -> airtime
 *   + guard time (propagation + turnaround + jitter)
 *   + acquisition time (fixed or stochastic LogNormal)
 *
 * The resulting gamma (slot efficiency) is EMERGENT — it is not set
 * to match the analytical model.  Any agreement between NS-3's gamma
 * and the Python model's gamma validates the analytical derivation.
 *
 * Physical motivation for each timing component:
 *
 * Guard time (4.7 ms default):
 *   - Propagation uncertainty: 1.7 ms.  For a 500 km cluster radius,
 *     the worst-case round-trip propagation difference between the
 *     nearest and farthest member is ~3.3 ms.  We use half (1.7 ms)
 *     because TDMA is one-way.
 *   - TX/RX turnaround: 2.0 ms.  Standard for CCSDS Proximity-1
 *     transceivers (switching between transmit and receive mode).
 *   - Timing jitter: 1.0 ms.  Clock drift + scheduling jitter
 *     accumulated over a T_c = 10s cycle at ~100 ppm TCXO accuracy.
 *
 * Acquisition time (5.0 ms default):
 *   - Antenna pointing dwell time for phased-array beam acquisition.
 *   - In cold-start (Config A), every slot pays this penalty.
 *   - In tracking mode (Config C), consecutive same-member slots
 *     skip acquisition (beam is already pointed).
 *   - LogNormal stochastic model captures real-world variability:
 *     median ~5 ms, but occasional 10-15 ms events from pointing
 *     transients, thermal distortion, or multi-path.
 */

#include "tdma-scheduler.h"

#include "ns3/log.h"
#include "ns3/double.h"
#include "ns3/uinteger.h"

#include <cmath>
#include <cassert>

namespace ns3 {

NS_LOG_COMPONENT_DEFINE ("TdmaScheduler");
NS_OBJECT_ENSURE_REGISTERED (TdmaScheduler);

TypeId
TdmaScheduler::GetTypeId (void)
{
    static TypeId tid = TypeId ("ns3::TdmaScheduler")
        .SetParent<Object> ()
        .SetGroupName ("Network")
        .AddConstructor<TdmaScheduler> ()
        ;
    return tid;
}

TdmaScheduler::TdmaScheduler ()
    : m_nMembers (0),
      m_cycleDurationSec (10.0),
      m_phyRateBps (30000.0),
      m_payloadBytes (256),
      m_fecRate (0.875),
      m_slotConfig (TDMA_COLD_START),
      m_packetsPerSlot (1),
      m_nRetransmissionSlots (0),
      m_guardTimeSec (0.0047),    // 4.7 ms
      m_stochasticAcquisition (false),
      m_fixedAcqTimeSec (0.005),  // 5.0 ms
      m_acqMuLnMs (std::log (5.0)),  // ln(5.0) for median 5 ms
      m_acqSigmaLn (0.3),
      m_turnaroundSec (0.002),    // 2.0 ms
      m_egressDurationSec (0.0),
      m_ingressDurationSec (0.0),
      m_marginSec (0.0),
      m_initialized (false)
{
    NS_LOG_FUNCTION (this);
    m_acqRng = CreateObject<LogNormalRandomVariable> ();
    m_acqRng->SetAttribute ("Mu", DoubleValue (m_acqMuLnMs));
    m_acqRng->SetAttribute ("Sigma", DoubleValue (m_acqSigmaLn));
}

TdmaScheduler::~TdmaScheduler ()
{
    NS_LOG_FUNCTION (this);
}

void
TdmaScheduler::Initialize (uint32_t nMembers,
                            double cycleDurationSec,
                            double phyRateBps,
                            uint32_t payloadBytes,
                            double fecRate,
                            TdmaSlotConfig slotConfig,
                            uint32_t packetsPerSlot,
                            uint32_t nRetransmissionSlots)
{
    NS_LOG_FUNCTION (this << nMembers << cycleDurationSec << phyRateBps
                     << payloadBytes << fecRate << slotConfig);

    m_nMembers = nMembers;
    m_cycleDurationSec = cycleDurationSec;
    m_phyRateBps = phyRateBps;
    m_payloadBytes = payloadBytes;
    m_fecRate = fecRate;
    m_slotConfig = slotConfig;
    m_packetsPerSlot = (slotConfig == TDMA_MULTI_PACKET) ? packetsPerSlot : 1;
    m_nRetransmissionSlots = nRetransmissionSlots;

    ComputeSlotTiming ();
    ComputeEgressTiming ();

    // Compute total ingress: (N-1) member slots + M_r retransmission slots
    uint32_t totalIngressSlots = m_nMembers + m_nRetransmissionSlots;
    m_ingressDurationSec = totalIngressSlots * m_slotTiming.totalSlotSec;

    // Margin = T_c - ingress - turnaround - egress
    m_marginSec = m_cycleDurationSec - m_ingressDurationSec
                  - m_turnaroundSec - m_egressDurationSec;

    m_initialized = true;

    NS_LOG_INFO ("TdmaScheduler initialized:"
                 << " N=" << m_nMembers
                 << " T_c=" << m_cycleDurationSec << "s"
                 << " R_PHY=" << m_phyRateBps << " bps"
                 << " S=" << m_payloadBytes << " B"
                 << " FEC=" << m_fecRate
                 << " slot=" << (m_slotTiming.totalSlotSec * 1000.0) << " ms"
                 << " gamma=" << m_slotTiming.gammaSlot
                 << " margin=" << (m_marginSec * 1000.0) << " ms"
                 << " schedulable=" << (m_marginSec >= 0 ? "YES" : "NO"));
}

void
TdmaScheduler::ComputeSlotTiming (void)
{
    // === Step 1: Payload bits ===
    double payloadBits = static_cast<double>(m_payloadBytes) * 8.0;

    // === Step 2: Framing overhead ===
    // CCSDS Proximity-1 inspired:
    //   ASM: 32 bits (Attached Sync Marker for frame synchronization)
    //   Address: 8 bits (link address)
    //   Control: 16 bits (protocol control)
    //   FCS: 32 bits (CRC-32 for error detection)
    double framingBits = static_cast<double>(FRAMING_OVERHEAD_BITS);  // 88 bits

    // === Step 3: Total uncoded bits ===
    double uncodedBits = payloadBits + framingBits;

    // === Step 4: FEC expansion ===
    // ceil(uncoded / fecRate) models the redundancy added by LDPC encoding
    // Rate 7/8: 1/0.875 = 1.143x expansion
    // Rate 1/2: 1/0.5 = 2.0x expansion
    double codedBits = std::ceil (uncodedBits / m_fecRate);

    // For multi-packet burst (Config B): multiply data by packets per slot
    // but only pay acquisition once
    double burstCodedBits = codedBits * static_cast<double>(m_packetsPerSlot);

    // === Step 5: Data airtime ===
    double dataTimeSec = burstCodedBits / m_phyRateBps;

    // === Step 6: Guard time ===
    // Already set in m_guardTimeSec (default 4.7 ms)
    double guardSec = m_guardTimeSec;

    // === Step 7: Acquisition time ===
    double acqSec;
    if (m_slotConfig == TDMA_TRACKING)
    {
        // Config C: tracking mode — acquisition is skipped for
        // consecutive slots.  In practice, the first slot in a burst
        // pays acquisition, subsequent slots don't.  For the
        // single-packet-per-slot case, we model this as T_acq = 0
        // (the scheduler handles tracking state externally).
        acqSec = 0.0;
    }
    else if (m_stochasticAcquisition)
    {
        // Stochastic: draw from LogNormal at initialization
        // The actual per-slot draw happens in DrawAcquisitionTimeSec()
        // For timing computation, use the median (= exp(mu))
        acqSec = std::exp (m_acqMuLnMs) / 1000.0;  // convert ms to sec
    }
    else
    {
        acqSec = m_fixedAcqTimeSec;
    }

    // === Step 8: Total slot duration ===
    double totalSlotSec = dataTimeSec + guardSec + acqSec;

    // === Step 9: Slot efficiency gamma ===
    // gamma = useful_payload_bits / (phy_rate * total_slot_time)
    // This captures ALL overheads: framing, FEC, guard, acquisition
    double gamma = (payloadBits * static_cast<double>(m_packetsPerSlot))
                   / (m_phyRateBps * totalSlotSec);

    // Store results
    m_slotTiming.payloadBits = payloadBits;
    m_slotTiming.framingOverheadBits = framingBits;
    m_slotTiming.uncodedTotalBits = uncodedBits;
    m_slotTiming.codedTotalBits = codedBits;
    m_slotTiming.dataTimeSec = dataTimeSec;
    m_slotTiming.guardTimeSec = guardSec;
    m_slotTiming.acquisitionTimeSec = acqSec;
    m_slotTiming.totalSlotSec = totalSlotSec;
    m_slotTiming.gammaSlot = gamma;

    NS_LOG_DEBUG ("Slot timing from first principles:"
                  << " payload=" << payloadBits << " bits"
                  << " framing=" << framingBits << " bits"
                  << " uncoded=" << uncodedBits << " bits"
                  << " coded=" << codedBits << " bits"
                  << " data=" << (dataTimeSec * 1000.0) << " ms"
                  << " guard=" << (guardSec * 1000.0) << " ms"
                  << " acq=" << (acqSec * 1000.0) << " ms"
                  << " total=" << (totalSlotSec * 1000.0) << " ms"
                  << " gamma=" << gamma);
}

double
TdmaScheduler::ComputePacketSlotSec (uint32_t payloadBytes) const
{
    double payloadBits = static_cast<double>(payloadBytes) * 8.0;
    double uncodedBits = payloadBits + static_cast<double>(FRAMING_OVERHEAD_BITS);
    double codedBits = std::ceil (uncodedBits / m_fecRate);
    double dataTimeSec = codedBits / m_phyRateBps;
    return dataTimeSec + m_guardTimeSec;
}

void
TdmaScheduler::ComputeEgressTiming (void)
{
    // Egress phase: coordinator downlink
    double summarySlotSec = ComputePacketSlotSec (SUMMARY_BYTES);
    double hbSlotSec = ComputePacketSlotSec (HEARTBEAT_BYTES);

    m_egressDurationSec = summarySlotSec + hbSlotSec;

    // Config D: bitmap ACK replaces per-member individual ACKs
    if (m_slotConfig == TDMA_BITMAP_ACK)
    {
        m_egressDurationSec += ComputePacketSlotSec (BITMAP_ACK_BYTES);
    }

    NS_LOG_DEBUG ("Egress timing: " << (m_egressDurationSec * 1000.0) << " ms"
                  << " (summary=" << (summarySlotSec * 1000.0) << " ms"
                  << " hb=" << (hbSlotSec * 1000.0) << " ms)");
}

Time
TdmaScheduler::GetSlotStart (uint32_t memberIdx) const
{
    assert (m_initialized);
    assert (memberIdx < m_nMembers);

    // Fixed assignment: member i gets slot i
    double offsetSec = static_cast<double>(memberIdx) * m_slotTiming.totalSlotSec;
    return Seconds (offsetSec);
}

TdmaSlotTiming
TdmaScheduler::GetSlotTiming (void) const
{
    assert (m_initialized);
    return m_slotTiming;
}

Time
TdmaScheduler::GetEgressStart (void) const
{
    assert (m_initialized);
    double egressStartSec = m_ingressDurationSec + m_turnaroundSec;
    return Seconds (egressStartSec);
}

Time
TdmaScheduler::GetIngressDuration (void) const
{
    assert (m_initialized);
    return Seconds (m_ingressDurationSec);
}

double
TdmaScheduler::GetGamma (void) const
{
    assert (m_initialized);
    return m_slotTiming.gammaSlot;
}

double
TdmaScheduler::GetMarginSec (void) const
{
    assert (m_initialized);
    return m_marginSec;
}

bool
TdmaScheduler::IsSchedulable (void) const
{
    assert (m_initialized);
    return m_marginSec >= 0.0;
}

uint32_t
TdmaScheduler::GetNMembers (void) const
{
    return m_nMembers;
}

double
TdmaScheduler::GetCycleDurationSec (void) const
{
    return m_cycleDurationSec;
}

double
TdmaScheduler::DrawAcquisitionTimeSec (void)
{
    if (!m_stochasticAcquisition)
    {
        return m_fixedAcqTimeSec;
    }
    // LogNormal draw: result is in ms, convert to sec
    double acqMs = m_acqRng->GetValue ();
    return acqMs / 1000.0;
}

double
TdmaScheduler::GetGuardTimeSec (void) const
{
    return m_guardTimeSec;
}

void
TdmaScheduler::SetGuardTimeSec (double guardSec)
{
    m_guardTimeSec = guardSec;
}

void
TdmaScheduler::SetFixedAcquisitionTimeSec (double acqSec)
{
    m_stochasticAcquisition = false;
    m_fixedAcqTimeSec = acqSec;
}

void
TdmaScheduler::SetStochasticAcquisition (double muLnMs, double sigmaLn)
{
    m_stochasticAcquisition = true;
    m_acqMuLnMs = muLnMs;
    m_acqSigmaLn = sigmaLn;
    m_acqRng->SetAttribute ("Mu", DoubleValue (muLnMs));
    m_acqRng->SetAttribute ("Sigma", DoubleValue (sigmaLn));
}

uint32_t
TdmaScheduler::GetNRetransmissionSlots (void) const
{
    return m_nRetransmissionSlots;
}

double
TdmaScheduler::GetEgressDurationSec (void) const
{
    assert (m_initialized);
    return m_egressDurationSec;
}

double
TdmaScheduler::GetTurnaroundSec (void) const
{
    return m_turnaroundSec;
}

} // namespace ns3
