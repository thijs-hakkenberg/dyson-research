"""ISL Link Budget Calculator.

Derives achievable data rate from ISL geometry and radio parameters.
Justifies 1 kbps as the RF-backup design point and confirms ISL
can support 24-30 kbps coordinator ingress.
"""

import math
from dataclasses import dataclass

# Physical constants
C_LIGHT = 2.998e8       # speed of light (m/s)
K_BOLTZMANN_DBW = -228.6  # Boltzmann constant (dBW/K/Hz)
T_SYS_DEFAULT = 290.0   # system noise temperature (K)


def _watts_to_dbw(watts: float) -> float:
    """Convert watts to dBW."""
    return 10.0 * math.log10(watts)


def _dbw_to_watts(dbw: float) -> float:
    """Convert dBW to watts."""
    return 10.0 ** (dbw / 10.0)


def compute_fspl(freq_hz: float, distance_m: float) -> float:
    """Free-Space Path Loss in dB.

    FSPL = 20*log10(4*pi*d*f/c)
    """
    return 20.0 * math.log10(4.0 * math.pi * distance_m * freq_hz / C_LIGHT)


def compute_link_budget(
    tx_power_w: float,
    tx_gain_dbi: float,
    rx_gain_dbi: float,
    freq_hz: float,
    distance_m: float,
    noise_figure_db: float = 3.0,
    implementation_loss_db: float = 2.0,
    required_ebn0_db: float = 9.6,
    fec_coding_gain_db: float = 0.0,
    t_sys_k: float = T_SYS_DEFAULT,
) -> dict:
    """Compute link budget and maximum achievable data rate.

    Parameters
    ----------
    tx_power_w : float
        Transmitter power (watts).
    tx_gain_dbi : float
        Transmitter antenna gain (dBi).
    rx_gain_dbi : float
        Receiver antenna gain (dBi).
    freq_hz : float
        Carrier frequency (Hz).
    distance_m : float
        ISL distance (metres).
    noise_figure_db : float
        Receiver noise figure (dB).
    implementation_loss_db : float
        System implementation loss (dB).
    required_ebn0_db : float
        Required Eb/N0 for target BER (dB).  Default 9.6 dB = BPSK BER<1e-5.
    fec_coding_gain_db : float
        FEC coding gain (dB).
    t_sys_k : float
        System noise temperature (K).

    Returns
    -------
    dict with keys:
        fspl_db, tx_power_dbw, received_power_dbw, noise_density_dbw_hz,
        ebn0_at_1kbps, ebn0_at_24kbps, max_data_rate_bps, link_margin_at_max_rate_db
    """
    tx_power_dbw = _watts_to_dbw(tx_power_w)

    # Free-space path loss
    fspl_db = compute_fspl(freq_hz, distance_m)

    # Received power (dBW)
    received_power_dbw = (
        tx_power_dbw + tx_gain_dbi - fspl_db + rx_gain_dbi - implementation_loss_db
    )

    # Noise spectral density N0 (dBW/Hz)
    # N0 = k_B * T_sys (in dBW/Hz) + noise figure
    n0_dbw_hz = K_BOLTZMANN_DBW + 10.0 * math.log10(t_sys_k) + noise_figure_db

    # Eb/N0 at specific data rates
    # Eb/N0 (dB) = Prx - N0 - 10*log10(Rb)
    ebn0_at_1kbps = received_power_dbw - n0_dbw_hz - 10.0 * math.log10(1_000)
    ebn0_at_24kbps = received_power_dbw - n0_dbw_hz - 10.0 * math.log10(24_000)

    # Effective required Eb/N0 (accounting for FEC gain)
    effective_required_ebn0 = required_ebn0_db - fec_coding_gain_db

    # Max data rate: solve Prx - N0 - 10*log10(Rb) = effective_required_ebn0
    # => 10*log10(Rb) = Prx - N0 - effective_required_ebn0
    # => Rb = 10^((Prx - N0 - effective_required_ebn0) / 10)
    log_rate = (received_power_dbw - n0_dbw_hz - effective_required_ebn0) / 10.0
    max_data_rate_bps = 10.0 ** log_rate

    # Link margin at max rate (should be ~0 by construction)
    link_margin_db = ebn0_at_1kbps - effective_required_ebn0  # margin at 1 kbps

    return {
        "fspl_db": fspl_db,
        "tx_power_dbw": tx_power_dbw,
        "received_power_dbw": received_power_dbw,
        "noise_density_dbw_hz": n0_dbw_hz,
        "ebn0_at_1kbps": ebn0_at_1kbps,
        "ebn0_at_24kbps": ebn0_at_24kbps,
        "max_data_rate_bps": max_data_rate_bps,
        "link_margin_at_1kbps_db": link_margin_db,
    }


def sweep_link_budget(
    distances_km: list,
    tx_powers_w: list,
    freq_hz: float,
    tx_gain_dbi: float,
    rx_gain_dbi: float,
    noise_figure_db: float = 3.0,
    implementation_loss_db: float = 2.0,
    required_ebn0_db: float = 9.6,
    fec_coding_gain_db: float = 0.0,
) -> dict:
    """Sweep distance x power -> achievable rate table.

    Returns dict with:
        distances_km, tx_powers_w, results[power_w][dist_km] = link_budget_dict
    """
    results: dict = {}
    for pw in tx_powers_w:
        results[pw] = {}
        for d_km in distances_km:
            d_m = d_km * 1_000
            results[pw][d_km] = compute_link_budget(
                tx_power_w=pw,
                tx_gain_dbi=tx_gain_dbi,
                rx_gain_dbi=rx_gain_dbi,
                freq_hz=freq_hz,
                distance_m=d_m,
                noise_figure_db=noise_figure_db,
                implementation_loss_db=implementation_loss_db,
                required_ebn0_db=required_ebn0_db,
                fec_coding_gain_db=fec_coding_gain_db,
            )
    return {
        "distances_km": distances_km,
        "tx_powers_w": tx_powers_w,
        "results": results,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("ISL Link Budget Analysis")
    print("=" * 70)

    # ISL mode: S-band, 2.2 GHz, 1 W, 6 dBi, 500 km
    isl = compute_link_budget(
        tx_power_w=1.0,
        tx_gain_dbi=6.0,
        rx_gain_dbi=6.0,
        freq_hz=2.2e9,
        distance_m=500e3,
    )
    print("\n--- ISL Mode (S-band, 2.2 GHz, 1W, 6 dBi, 500 km) ---")
    print(f"  FSPL:            {isl['fspl_db']:.1f} dB")
    print(f"  Prx:             {isl['received_power_dbw']:.1f} dBW")
    print(f"  N0:              {isl['noise_density_dbw_hz']:.1f} dBW/Hz")
    print(f"  Eb/N0 @ 1 kbps:  {isl['ebn0_at_1kbps']:.1f} dB")
    print(f"  Eb/N0 @ 24 kbps: {isl['ebn0_at_24kbps']:.1f} dB")
    print(f"  Max rate:        {isl['max_data_rate_bps']:.0f} bps ({isl['max_data_rate_bps']/1000:.1f} kbps)")

    # RF-backup mode: UHF, 400 MHz, 0.1 W, 0 dBi, 1000 km
    rf = compute_link_budget(
        tx_power_w=0.1,
        tx_gain_dbi=0.0,
        rx_gain_dbi=0.0,
        freq_hz=400e6,
        distance_m=1000e3,
    )
    print("\n--- RF-Backup Mode (UHF, 400 MHz, 0.1W, 0 dBi, 1000 km) ---")
    print(f"  FSPL:            {rf['fspl_db']:.1f} dB")
    print(f"  Prx:             {rf['received_power_dbw']:.1f} dBW")
    print(f"  N0:              {rf['noise_density_dbw_hz']:.1f} dBW/Hz")
    print(f"  Eb/N0 @ 1 kbps:  {rf['ebn0_at_1kbps']:.1f} dB")
    print(f"  Eb/N0 @ 24 kbps: {rf['ebn0_at_24kbps']:.1f} dB")
    print(f"  Max rate:        {rf['max_data_rate_bps']:.0f} bps ({rf['max_data_rate_bps']/1000:.1f} kbps)")

    # Sweep
    print("\n--- Distance x Power Sweep (UHF backup) ---")
    sweep = sweep_link_budget(
        distances_km=[100, 500, 1000, 2000],
        tx_powers_w=[0.1, 0.5, 1.0],
        freq_hz=400e6,
        tx_gain_dbi=0.0,
        rx_gain_dbi=0.0,
    )
    print(f"{'Dist (km)':>10} {'Power (W)':>10} {'Max Rate (kbps)':>16} {'Eb/N0@1k (dB)':>15}")
    for d_km in sweep["distances_km"]:
        for pw in sweep["tx_powers_w"]:
            r = sweep["results"][pw][d_km]
            print(f"{d_km:10.0f} {pw:10.2f} {r['max_data_rate_bps']/1000:16.1f} {r['ebn0_at_1kbps']:15.1f}")
