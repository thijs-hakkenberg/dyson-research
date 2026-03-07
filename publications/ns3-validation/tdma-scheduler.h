/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * tdma-scheduler.h — TDMA slot assignment for swarm cluster coordination
 *
 * Implements fixed-assignment TDMA scheduling for intra-cluster
 * communication.  Each cluster member is assigned a deterministic
 * slot within the T_c cycle, eliminating contention and enabling
 * predictable ingress timing.
 *
 * Four slot configurations model different protocol maturity levels:
 *
 * Config A (Cold-Start): Each member gets one slot with full acquisition
 *   overhead per slot.  Baseline worst case — every slot pays the
 *   antenna pointing/acquisition penalty.
 *
 * Config B (Multi-Packet Burst): Members send multiple packets per slot
 *   (e.g., 3 ephemeris updates) but only pay acquisition once.  Models
 *   batched reporting at lower duty cycles.
 *
 * Config C (Tracking Mode): Consecutive slots from the same member skip
 *   acquisition entirely (T_acq=0) because the antenna is already
 *   pointed.  Models mature flight software with tracking loops.
 *
 * Config D (Bitmap ACK): The coordinator sends a 13-byte aggregate
 *   bitmap ACK instead of individual per-member ACKs.  Reduces egress
 *   overhead from O(N) to O(1) per cycle.
 *
 * IMPORTANT: Slot timing is computed from first principles (payload
 * size, FEC rate, PHY rate, framing bits) — NOT copied from the Python
 * analytical model.  Any agreement with the analytical gamma is
 * emergent, not assumed.
 */

#ifndef TDMA_SCHEDULER_H
#define TDMA_SCHEDULER_H

#include "ns3/object.h"
#include "ns3/nstime.h"
#include "ns3/random-variable-stream.h"

#include <vector>
#include <cstdint>

namespace ns3 {

/**
 * \brief Slot configuration mode for TDMA scheduling.
 */
enum TdmaSlotConfig
{
    TDMA_COLD_START    = 0,  //!< Config A: single packet, full acquisition each slot
    TDMA_MULTI_PACKET  = 1,  //!< Config B: 3 packets/slot, single acquisition
    TDMA_TRACKING      = 2,  //!< Config C: T_acq=0 for consecutive same-member slots
    TDMA_BITMAP_ACK    = 3   //!< Config D: 13-byte aggregate ACK
};

/**
 * \brief Structure holding computed slot timing parameters.
 *
 * All durations are in seconds (NS-3 convention), computed from first
 * principles using the physical-layer parameters.
 */
struct TdmaSlotTiming
{
    double payloadBits;          //!< Raw payload bits = S_eph * 8
    double framingOverheadBits;  //!< ASM + addr + ctrl + FCS = 88 bits
    double uncodedTotalBits;     //!< payload + framing overhead
    double codedTotalBits;       //!< ceil(uncoded / fecRate)
    double dataTimeSec;          //!< codedTotalBits / phyRateBps
    double guardTimeSec;         //!< Guard interval
    double acquisitionTimeSec;   //!< Antenna acquisition time (stochastic or fixed)
    double totalSlotSec;         //!< data + guard + acquisition
    double gammaSlot;            //!< payloadBits / (phyRateBps * totalSlotSec)
};

/**
 * \brief TDMA slot scheduler for a single swarm cluster.
 *
 * Computes slot assignments and timing for N-1 member nodes within
 * a T_c cycle.  The coordinator does not transmit during ingress
 * (half-duplex constraint) and uses the egress phase for downlink.
 */
class TdmaScheduler : public Object
{
public:
    static TypeId GetTypeId (void);

    TdmaScheduler ();
    virtual ~TdmaScheduler ();

    /**
     * \brief Initialize the scheduler with cluster parameters.
     *
     * Must be called before GetSlotStart/GetSlotTiming.
     *
     * \param nMembers Number of member nodes (N-1, excluding coordinator)
     * \param cycleDurationSec Total cycle duration T_c in seconds
     * \param phyRateBps Physical layer bit rate in bps
     * \param payloadBytes Ephemeris payload size in bytes (S_eph)
     * \param fecRate FEC code rate (e.g. 7/8 = 0.875)
     * \param slotConfig Slot configuration mode
     * \param packetsPerSlot Packets per slot for Config B (default 1)
     * \param nRetransmissionSlots Reserved retransmission slots M_r
     */
    void Initialize (uint32_t nMembers,
                     double cycleDurationSec,
                     double phyRateBps,
                     uint32_t payloadBytes,
                     double fecRate,
                     TdmaSlotConfig slotConfig,
                     uint32_t packetsPerSlot = 1,
                     uint32_t nRetransmissionSlots = 0);

    /**
     * \brief Get the start time of member i's slot within a cycle.
     *
     * \param memberIdx Zero-based member index [0, nMembers)
     * \return Start time offset from cycle start in seconds
     */
    Time GetSlotStart (uint32_t memberIdx) const;

    /**
     * \brief Get the computed slot timing for a standard ephemeris slot.
     *
     * The timing is computed from first principles:
     *   1. Payload bits = payloadBytes * 8
     *   2. Framing overhead = ASM(32) + addr(8) + ctrl(16) + FCS(32) = 88 bits
     *   3. Uncoded total = payload + framing
     *   4. Coded total = ceil(uncoded / fecRate)
     *   5. Data time = codedBits / phyRate
     *   6. Guard = configurable (default 4.7 ms)
     *   7. Acquisition = stochastic LogNormal or fixed
     *   8. Total slot = data + guard + acquisition
     *   9. gamma = payloadBits / (phyRate * totalSlot)
     */
    TdmaSlotTiming GetSlotTiming (void) const;

    /**
     * \brief Get the start time of the egress phase.
     *
     * Egress begins after all ingress slots + turnaround time.
     */
    Time GetEgressStart (void) const;

    /**
     * \brief Get the total ingress duration for all members.
     */
    Time GetIngressDuration (void) const;

    /**
     * \brief Get the computed MAC efficiency gamma.
     *
     * gamma = payload_bits / (phy_rate * slot_duration)
     * This emerges from the physical-layer parameters, not assumed.
     */
    double GetGamma (void) const;

    /**
     * \brief Get the cycle deadline margin (T_c - total_used_time).
     *
     * A negative margin means the cycle is infeasible.
     */
    double GetMarginSec (void) const;

    /**
     * \brief Check if the current configuration is schedulable.
     *
     * Returns true if all N-1 ingress slots + turnaround + egress
     * fit within T_c.
     */
    bool IsSchedulable (void) const;

    /**
     * \brief Get the number of member nodes.
     */
    uint32_t GetNMembers (void) const;

    /**
     * \brief Get the cycle duration.
     */
    double GetCycleDurationSec (void) const;

    /**
     * \brief Draw a stochastic acquisition time from LogNormal distribution.
     *
     * Models the real-world variability in antenna acquisition:
     *   T_acq ~ LogNormal(mu=ln(5ms), sigma=0.3)
     *
     * This produces a right-skewed distribution centered near 5 ms
     * with occasional long tails (modeling pointing errors, thermal
     * distortion, etc.).
     */
    double DrawAcquisitionTimeSec (void);

    /**
     * \brief Get the fixed guard time in seconds.
     */
    double GetGuardTimeSec (void) const;

    /**
     * \brief Set the guard time in seconds.
     */
    void SetGuardTimeSec (double guardSec);

    /**
     * \brief Set fixed acquisition time (disables stochastic mode).
     */
    void SetFixedAcquisitionTimeSec (double acqSec);

    /**
     * \brief Enable stochastic acquisition time (LogNormal).
     */
    void SetStochasticAcquisition (double muLnMs, double sigmaLn);

    /**
     * \brief Get the number of retransmission slots.
     */
    uint32_t GetNRetransmissionSlots (void) const;

    /**
     * \brief Get the computed egress duration in seconds.
     */
    double GetEgressDurationSec (void) const;

    /**
     * \brief Get the TX/RX turnaround time in seconds.
     */
    double GetTurnaroundSec (void) const;

private:
    /**
     * \brief Compute the slot duration for a packet with the given payload.
     *
     * Applies the standard framing pipeline: payload + overhead -> FEC -> PHY rate,
     * then adds guard time. Does NOT include acquisition time.
     *
     * \param payloadBytes Payload size in bytes
     * \return Slot duration in seconds (data + guard)
     */
    double ComputePacketSlotSec (uint32_t payloadBytes) const;
    /**
     * \brief Compute slot timing from first principles.
     *
     * CCSDS Proximity-1 inspired framing:
     *   ASM: 32 bits (Attached Sync Marker)
     *   Address: 8 bits
     *   Control: 16 bits
     *   Payload: S_eph * 8 bits
     *   FCS: 32 bits (CRC-32)
     *   Total uncoded: ASM + addr + ctrl + payload + FCS
     *   Coded: ceil(uncoded / fecRate)
     *
     * Guard time budget:
     *   Propagation uncertainty: 1.7 ms (500 km cluster radius)
     *   TX/RX turnaround: 2.0 ms (CCSDS Proximity-1)
     *   Timing jitter margin: 1.0 ms
     *   Total: 4.7 ms (default)
     *
     * Acquisition time:
     *   Fixed: 5.0 ms (default)
     *   Stochastic: LogNormal(mu=ln(5ms), sigma=0.3)
     */
    void ComputeSlotTiming (void);

    /**
     * \brief Compute egress phase timing.
     *
     * Egress includes:
     *   - Coordinator summary (512 bytes)
     *   - Heartbeat (64 bytes)
     *   - Bitmap ACK if Config D (13 bytes)
     *   - TX/RX turnaround (2.0 ms)
     */
    void ComputeEgressTiming (void);

    // Configuration
    uint32_t m_nMembers;
    double   m_cycleDurationSec;
    double   m_phyRateBps;
    uint32_t m_payloadBytes;
    double   m_fecRate;
    TdmaSlotConfig m_slotConfig;
    uint32_t m_packetsPerSlot;
    uint32_t m_nRetransmissionSlots;

    // Framing constants (CCSDS Proximity-1 inspired)
    static const uint32_t ASM_BITS = 32;
    static const uint32_t ADDR_BITS = 8;
    static const uint32_t CTRL_BITS = 16;
    static const uint32_t FCS_BITS = 32;
    static const uint32_t FRAMING_OVERHEAD_BITS = ASM_BITS + ADDR_BITS + CTRL_BITS + FCS_BITS;

    // Guard time (default 4.7 ms = 1.7 propagation + 2.0 turnaround + 1.0 jitter)
    double m_guardTimeSec;

    // Acquisition time
    bool   m_stochasticAcquisition;
    double m_fixedAcqTimeSec;   //!< Fixed acquisition (default 5.0 ms)
    double m_acqMuLnMs;         //!< LogNormal mu parameter (ln(5.0))
    double m_acqSigmaLn;        //!< LogNormal sigma parameter (0.3)
    Ptr<LogNormalRandomVariable> m_acqRng;

    // Egress parameters
    static const uint32_t SUMMARY_BYTES = 512;
    static const uint32_t HEARTBEAT_BYTES = 64;
    static const uint32_t BITMAP_ACK_BYTES = 13;
    double m_turnaroundSec;     //!< TX/RX turnaround (2.0 ms)

    // Computed timing
    TdmaSlotTiming m_slotTiming;
    double m_egressDurationSec;
    double m_ingressDurationSec;
    double m_marginSec;

    bool m_initialized;
};

} // namespace ns3

#endif // TDMA_SCHEDULER_H
