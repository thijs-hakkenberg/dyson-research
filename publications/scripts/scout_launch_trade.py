"""
Scout launch trade (rq-0-52, open question 1.2): what a given way of leaving Earth costs in
scout mass, thruster hours and launcher capacity.

Three small models, each anchored on published or consensus figures:

  scout mass      rocket equation about each model's own scout (bom-0-1 keeps three positions);
  perigee kick    a chemical burn at perigee that raises a C3 < 0 orbit to the wanted C3;
  launcher        payload of a two-stage medium launcher against C3, from its second stage and
                  three published payload figures. An estimate: the provider's own curve was
                  not obtained.

Sources for the anchors are in rq-0-52 research/papers.yaml.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

G0 = 9.80665
MU_EARTH = 398600.4418  # km^3/s^2
R_PARK = 6578.0  # km, 200 km parking orbit


# ----------------------------------------------------------------------------- scout mass

@dataclass(frozen=True)
class ScoutDesign:
    """One model's scout from the bom-0-1 consensus. `dv_design` is the ideal Δv the stated
    wet mass carries; `power_w` is the power to the thrusters."""
    name: str
    wet_kg: float
    dv_design: float  # km/s
    isp_s: float
    power_w: float
    efficiency: float = 0.5
    tank_fraction: float = 0.08  # kg of tank and feed per kg of propellant (solid iodine)
    life_hours: float = 6500.0  # thruster life the position plans to qualify

    @property
    def ve(self) -> float:  # km/s
        return G0 * self.isp_s / 1e3

    @property
    def fixed_kg(self) -> float:
        """Mass that does not scale with propellant."""
        p = self.wet_kg * (1 - np.exp(-self.dv_design / self.ve))
        return self.wet_kg - p * (1 + self.tank_fraction)

    def wet_for(self, dv_kms):
        """Wet mass carrying `dv_kms`, with the same fixed mass. inf where it cannot close."""
        r = np.exp(np.asarray(dv_kms, float) / self.ve)
        den = 1 - self.tank_fraction * (r - 1)
        return np.where(den > 0, self.fixed_kg * r / np.where(den > 0, den, 1.0), np.inf)

    def propellant_for(self, dv_kms):
        w = self.wet_for(dv_kms)
        return w * (1 - np.exp(-np.asarray(dv_kms, float) / self.ve))

    def thrust_hours(self, dv_kms):
        """Thruster firing time to deliver `dv_kms` on the scout sized for it."""
        mdot = 2 * self.efficiency * self.power_w / (self.ve * 1e3) ** 2  # kg/s
        return self.propellant_for(dv_kms) / mdot / 3600.0

    def accel(self, dv_kms) -> float:  # m/s^2 at the start of the transfer
        return 2 * self.efficiency * self.power_w / (self.ve * 1e3) / float(self.wet_for(dv_kms))


# bom-0-1 consensus, "Fleet size and spacecraft class" and "Propulsion": positions are kept apart.
SCOUTS = (
    ScoutDesign('Claude', 550.0, 4.5, 1900.0, 2200.0, life_hours=6500.0),
    ScoutDesign('GPT', 500.0, 4.81, 1900.0, 2200.0, life_hours=12000.0),
    ScoutDesign('Gemini', 250.0, 3.7, 1900.0, 600.0, life_hours=6500.0),  # states no life target; Claude's used
)


# ----------------------------------------------------------------------------- perigee kick

def perigee_speed(c3, rp_km=R_PARK):
    return np.sqrt(np.asarray(c3, float) + 2 * MU_EARTH / rp_km)


def kick_dv(c3_from, c3_to, rp_km=R_PARK):
    """Δv (km/s) of a burn at perigee that changes C3."""
    return perigee_speed(c3_to, rp_km) - perigee_speed(c3_from, rp_km)


def kick_mass(payload_kg, dv_kms, isp_s=320.0, structure=0.15):
    """Propellant and stage dry mass (kg) of a chemical kick for `payload_kg`.
    structure = stage dry mass per kg of propellant."""
    r = np.exp(np.asarray(dv_kms, float) * 1e3 / (G0 * isp_s))
    prop = payload_kg * (r - 1) / (1 - structure * (r - 1))
    return prop, structure * prop


# ----------------------------------------------------------------------------- launcher

def leo_to_c3(c3, rp_km=R_PARK):
    """Δv (km/s) from the circular parking orbit to the given C3."""
    return perigee_speed(c3, rp_km) - np.sqrt(MU_EARTH / rp_km)


@dataclass(frozen=True)
class Launcher:
    """Second stage plus published payloads. The second stage's Δv to a destination is taken
    as linear in the Δv from the parking orbit, fitted through two published payloads of the
    expendable vehicle; recovering the first stage adds a fixed amount, fitted to the
    recoverable GTO payload."""
    name: str
    stage_dry_kg: float
    stage_prop_kg: float
    isp_s: float
    anchors: tuple  # ((Δv from parking orbit km/s, payload kg), (..)) expendable
    gto_recover_kg: float
    gto_dv: float = 2.45

    def _stage_dv(self, payload_kg):
        m0 = self.stage_dry_kg + self.stage_prop_kg + payload_kg
        return G0 * self.isp_s / 1e3 * np.log(m0 / (self.stage_dry_kg + payload_kg))

    def _payload(self, stage_dv):
        r = np.exp(np.asarray(stage_dv, float) * 1e3 / (G0 * self.isp_s))
        return (self.stage_prop_kg - (r - 1) * self.stage_dry_kg) / (r - 1)

    def payload(self, c3, recover=True):
        (x1, p1), (x2, p2) = self.anchors
        y1, y2 = self._stage_dv(p1), self._stage_dv(p2)
        need = y1 + (y2 - y1) * (leo_to_c3(c3) - x1) / (x2 - x1)
        if recover:
            (xg, pg) = min(self.anchors, key=lambda a: abs(a[0] - self.gto_dv))
            need = need + self._stage_dv(self.gto_recover_kg) - self._stage_dv(pg)
        return np.maximum(self._payload(need), 0.0)


# Falcon 9 Block 5: second stage 4.0 t empty, 107.5 t propellant, 348 s; expendable 22.8 t to
# LEO, 8.3 t to GTO, 4.02 t "to Mars"; 5.5 t to GTO with the first stage recovered.
# Two fits bracket the unknown C3 of the "to Mars" figure.
FALCON9_LOW = Launcher('Falcon 9 (GTO and Mars anchors, Mars at C3 = 10)', 4000.0, 107500.0, 348.0,
                       ((2.45, 8300.0), (float(leo_to_c3(10.0)), 4020.0)), 5500.0)
FALCON9_HIGH = Launcher('Falcon 9 (LEO and GTO anchors)', 4000.0, 107500.0, 348.0,
                        ((0.0, 22800.0), (2.45, 8300.0)), 5500.0)
