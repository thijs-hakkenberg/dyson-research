# Stellar Engines: Design Considerations for Maximizing Acceleration

**Source:** Caplan, M. (2019). Stellar Engines: Design Considerations for Maximizing Acceleration. *Acta Astronautica*, 165, 96-104.

## Abstract

This paper analyzes stellar engine designs for propelling the Sun and Solar System through the galaxy. Two main approaches are considered: passive thrusters (Shkadov mirrors) using radiation pressure, and active thrusters (Caplan engines) using thermonuclear jets powered by extracted solar material.

## 1. Introduction

A stellar engine is a megastructure designed to convert stellar energy into directed thrust, enabling the controlled movement of an entire star system. Such engines could serve multiple purposes:
- Avoiding cosmic hazards (supernovae, gamma-ray bursts)
- Adjusting stellar orbits within the galaxy
- Maintaining habitable conditions over geological timescales
- Interstellar migration

## 2. Passive Thrusters (Shkadov Mirror)

### 2.1 Concept

First proposed by Leonid Shkadov in 1987, the Shkadov thruster is a giant parabolic mirror positioned at the L1 Lagrange point between a star and some reference direction. By reflecting stellar radiation asymmetrically, net thrust is generated.

### 2.2 Design Parameters

- **Configuration:** Parabolic mirror at ~1 AU from the Sun
- **Mirror radius:** ~1.5 AU (to capture significant solar flux)
- **Mass:** ~10^22 kg (thin-film construction)
- **Material:** Reflective thin-film (~1 g/m^2)
- **Stability:** Maintained by radiation pressure equilibrium

### 2.3 Performance

- **Thrust:** ~10^15 N
- **Acceleration:** ~10^-12 m/s^2
- **Velocity change:** ~0.1 m/s per century
- **Time to move 1 light-year:** ~1 billion years

### 2.4 Advantages
- Passive operation (no fuel consumption)
- Conceptually simple
- Long operational lifetime

### 2.5 Disadvantages
- Extremely low acceleration
- Massive construction requirements
- Cannot adjust thrust magnitude easily

## 3. Active Thrusters (Caplan Engine)

### 3.1 Concept

The Caplan engine uses mass lifted from the Sun's surface to fuel a thermonuclear jet engine. By separating hydrogen and helium from solar wind and chromospheric material, two jets are created:
1. A fusion-powered helium jet providing primary thrust
2. A hydrogen jet reflected back at the Sun to maintain orbital stability

### 3.2 Mass Lifting System

Solar mass lifting extracts material from the Sun using:
- **Magnetic fields:** To channel plasma from the chromosphere
- **Solar wind collection:** Intercepting naturally escaping material
- **Concentrated energy beaming:** To increase local evaporation

Extraction rates of 10^12 kg/s are theoretically achievable.

### 3.3 Propulsion System

The engine consists of:
- **Helium separation plant:** Separates He-4 from collected material
- **Fusion reactor:** Burns helium in nuclear fusion
- **Electromagnetic accelerator:** Accelerates exhaust to ~0.01c
- **Hydrogen return system:** Redirects hydrogen back to Sun

### 3.4 Performance

- **Thrust:** Up to ~10^18 N
- **Acceleration:** ~10^-9 m/s^2 (1000x better than Shkadov)
- **Velocity change:** ~100 m/s per century
- **Time to move 1 light-year:** ~1 million years
- **Fuel consumption:** ~10^12 kg/s of solar material

### 3.5 Advantages
- Much higher acceleration than passive designs
- Controllable thrust vector
- Can combine with Dyson swarm infrastructure

### 3.6 Disadvantages
- Complex active systems
- Requires continuous mass extraction
- Slowly consumes the Sun (extends stellar lifetime by moving to red giant phase later)

## 4. Hybrid Approaches

### 4.1 Dyson Swarm Integration

A stellar engine can be integrated with a Dyson swarm:
- Swarm elements provide power for mass lifting
- Partial coverage creates natural thrust asymmetry
- Swarm can focus energy for enhanced mass lifting

### 4.2 Staged Development

1. **Stage 1:** Deploy Shkadov mirror for initial low-thrust capability
2. **Stage 2:** Add mass lifting infrastructure
3. **Stage 3:** Construct thermonuclear jet system
4. **Stage 4:** Full Caplan engine operation

## 5. Engineering Challenges

### 5.1 Structural
- Maintaining mirror stability at AU scales
- Handling thermal gradients
- Material fatigue over million-year timescales

### 5.2 Propulsion
- Containing fusion reactions at required scale
- Electromagnetic acceleration efficiency
- Exhaust beam collimation

### 5.3 Mass Lifting
- Extracting material without destabilizing the Sun
- Separating isotopes at industrial scales
- Managing extracted plasma

### 5.4 Control Systems
- Precision thrust vectoring
- Long-term trajectory planning
- Feedback control over century timescales

## 6. Key Equations

### 6.1 Shkadov Thrust
```
F = (L_sun × η) / c
```
Where:
- L_sun = Solar luminosity (~3.8 × 10^26 W)
- η = Mirror efficiency and coverage fraction
- c = Speed of light

### 6.2 Caplan Engine Thrust
```
F = ṁ × v_e
```
Where:
- ṁ = Mass flow rate (~10^12 kg/s)
- v_e = Exhaust velocity (~0.01c = 3 × 10^6 m/s)

### 6.3 Acceleration
```
a = F / M_sun
```
Where:
- M_sun = Solar mass (~2 × 10^30 kg)

## 7. Comparison Table

| Parameter | Shkadov Mirror | Caplan Engine |
|-----------|----------------|---------------|
| Acceleration | ~10^-12 m/s^2 | ~10^-9 m/s^2 |
| Thrust | ~10^15 N | ~10^18 N |
| Complexity | Low | High |
| Fuel required | None | Solar material |
| Time to move 1 ly | ~1 Gyr | ~1 Myr |
| Dyson prerequisite | Partial | Full |

## 8. Relevance to Project Dyson

Phase 3b (Stellar Engine) builds on the Phase 2 Dyson swarm infrastructure to implement a stellar propulsion capability. The recommended approach combines both passive and active systems:

1. **Shkadov Mirror Array:** Repurpose/augment swarm elements into reflective arrays
2. **Mass Lifting Systems:** Extract solar material using concentrated swarm power
3. **Thermonuclear Jet Engine:** Process extracted material into propellant
4. **Integration Layer:** Coordinate between Dyson swarm power generation and engine operation

## References

- Caplan, M. (2019). Stellar Engines: Design Considerations for Maximizing Acceleration. Acta Astronautica, 165, 96-104.
- Shkadov, L.M. (1987). Possibility of controlling solar system motion in the galaxy. 38th IAF Congress.
- Badescu, V., & Cathcart, R.B. (2000). Stellar engines for Kardashev's type II civilisations. Journal of the British Interplanetary Society, 53, 297-306.
