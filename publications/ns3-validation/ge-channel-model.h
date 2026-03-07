/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * ge-channel-model.h — Gilbert-Elliott two-state burst error model
 *
 * Wraps NS-3's BurstErrorModel to provide correlated link losses that
 * match the Gilbert-Elliott (GE) channel used in the analytical TDMA
 * model.  The GE channel captures the bursty nature of space-link
 * outages caused by solar scintillation, Earth occultation, and
 * attitude-pointing transients.
 *
 * State machine:
 *   GOOD  --[p_GB]--> BAD
 *   BAD   --[p_BG]--> GOOD
 *
 * In GOOD state: BER ~ 1e-6 (effectively lossless after FEC)
 * In BAD  state: BER ~ 1e-2 (most packets lost after FEC)
 *
 * Transitions can occur per-cycle or per-slot, controlled by the
 * TransitionGranularity attribute.
 *
 * IMPORTANT: This model is implemented from first principles using
 * NS-3 primitives.  It does NOT import or call the Python analytical
 * model — the whole point is independent validation.
 */

#ifndef TDMA_GE_CHANNEL_MODEL_H
#define TDMA_GE_CHANNEL_MODEL_H

#include "ns3/error-model.h"
#include "ns3/random-variable-stream.h"
#include "ns3/nstime.h"

namespace ns3 {

/**
 * \brief Gilbert-Elliott two-state burst error model for space links.
 *
 * Each link maintains an independent GE state machine.  On each packet
 * arrival, the model:
 *   1. Optionally transitions state (per-slot granularity)
 *   2. Draws a Bernoulli loss using the current state's loss probability
 *   3. Returns corrupt=true if lost (triggering NS-3 packet drop)
 *
 * This provides correlated burst losses that an i.i.d. Bernoulli model
 * cannot capture, matching the space-link physics where outages persist
 * for multiple consecutive slots.
 */
class GeChannelModel : public ErrorModel
{
public:
    /**
     * \brief Register this type with the NS-3 type system.
     */
    static TypeId GetTypeId (void);

    GeChannelModel ();
    virtual ~GeChannelModel ();

    /**
     * \brief Force a GE state transition (call once per cycle or slot).
     *
     * Draws a uniform random and applies the Markov transition:
     *   GOOD -> BAD  with probability p_GB
     *   BAD  -> GOOD with probability p_BG
     */
    void DoTransition (void);

    /**
     * \brief Get current state (true = Good, false = Bad).
     */
    bool IsGoodState (void) const;

    /**
     * \brief Get the steady-state probability of being in BAD state.
     *
     * pi_B = p_GB / (p_GB + p_BG)
     */
    double GetSteadyStateBadProb (void) const;

    /**
     * \brief Reset to a random state drawn from steady-state distribution.
     */
    void ResetToSteadyState (void);

    // Attribute accessors
    void SetPgb (double p);
    double GetPgb (void) const;

    void SetPbg (double p);
    double GetPbg (void) const;

    void SetPLossGood (double p);
    double GetPLossGood (void) const;

    void SetPLossBad (double p);
    double GetPLossBad (void) const;

    void SetFecRate (double rate);
    double GetFecRate (void) const;

    void SetPerSlotTransitions (bool enable);
    bool GetPerSlotTransitions (void) const;

private:
    /**
     * \brief NS-3 ErrorModel interface: decide whether to corrupt a packet.
     */
    virtual bool DoCorrupt (Ptr<Packet> p) override;
    virtual void DoReset (void) override;

    // GE state
    bool m_inGoodState;          //!< true = Good state, false = Bad state

    // Transition probabilities
    double m_pGoodToBad;         //!< P(Good -> Bad) per transition
    double m_pBadToGood;         //!< P(Bad -> Good) per transition

    // Per-state packet loss probability (after FEC)
    double m_pLossGood;          //!< Packet loss in Good state (default 0.01)
    double m_pLossBad;           //!< Packet loss in Bad state (default 0.90)

    // FEC parameters
    double m_fecRate;            //!< FEC code rate (default 7/8 = 0.875)
    double m_fecThreshold;       //!< BER correction threshold for current rate

    // Transition granularity
    bool m_perSlotTransitions;   //!< If true, transition per DoCorrupt call

    // RNG
    Ptr<UniformRandomVariable> m_rng;
};

} // namespace ns3

#endif // TDMA_GE_CHANNEL_MODEL_H
