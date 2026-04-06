# Simulation5 — Evolutionary Ecosystem Simulator

A real-time 2D ecosystem simulation built with Python and Pygame, demonstrating **emergent evolutionary behavior** through natural selection, genetic inheritance, and population dynamics.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green?logo=pygame)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## Overview

Creatures roam a 1280×720 world, searching for food, finding mates, and passing their traits on to offspring. Trees grow, spread seeds, and get eaten. Over time, **natural selection shapes the population** — faster, hardier creatures survive longer and reproduce more, passing on their advantageous genes.

The simulation runs until the last creature starves, and logs every birth, death, and meal along the way.

> **Tip:** Add a demo GIF to really make this pop! Run the simulation, capture ~10 seconds with a screen recorder, save as `demo.gif` in the repo root, and replace this line with `![Demo](demo.gif)`.

---

## Features

- **Genetic inheritance** — offspring inherit mutated versions of parent traits
- **4 heritable traits** — speed, stomach size, starvation tolerance, and digestion rate
- **8 generations visualised** — each generation has a distinct sprite so you can watch lineages evolve in real time
- **Dual seed dispersal** — trees self-seed locally, and creatures scatter seeds when they digest food
- **Hunger mechanics** — creatures only eat when hungry (< 60% full), driving realistic foraging behavior
- **Full event logging** — every eat, birth, death, and starvation is recorded to `simulation5.log`
- **Live controls** — add creatures or trees mid-simulation and watch the ecosystem respond

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
git clone https://github.com/guvnor33/simulation5.git
cd simulation5
pip install -r requirements.txt
```

### Run

```bash
python main.py
```

---

## Controls

| Key | Action |
|-----|--------|
| `T` | Spawn a new tree at a random position |
| `C` | Spawn a new creature at a random position |
| `P` | Print full stats for all creatures and trees |
| `O` | Print creature stats only |
| `X` | Exit the simulation |

---

## How Evolution Works

Each creature is born with four genetic traits, inherited from both parents with small random mutations (±5% standard deviation, capped at ±20%):

| Trait | Effect |
|-------|--------|
| **Speed** | How fast the creature moves across the world |
| **Stomach Size** | Maximum food capacity — larger stomachs mean longer survival between meals |
| **Starvation Time Limit** | How long a creature can survive with an empty stomach (milliseconds) |
| **Food Reduction Interval** | How quickly the stomach empties over time — a metabolism proxy |

Creatures that strike the right balance survive long enough to mate and pass on their genes. Creatures that are too slow to find food, or burn through their stomach too fast, die before reproducing. Over many generations, fit trait combinations become dominant in the population.

---

## Project Structure

```
simulation5/
├── main.py             # Game loop, collision detection, breeding & eating logic
├── creature2.py        # Creature sprite — movement, hunger, mating, genetics
├── tree2.py            # Tree sprite — growth stages, self-seeding, consumption
├── creature.py         # Legacy v1 creature (kept for reference)
├── tree.py             # Legacy v1 tree (kept for reference)
├── requirements.txt
└── images/
    ├── creature_g0.png … creature_g8.png   # Sprites for generations 0–8
    └── fruit_tree-1.png … fruit_tree-8.png # Sprites for tree growth stages
```

---

## Architecture

The simulation is structured around three core classes:

**`Creature2`** manages all per-creature state: position, velocity, genetic traits, hunger level, starvation timer, mating cooldown, and lineage tracking. Mutation is applied at birth using a Gaussian distribution so trait drift is gradual and realistic.

**`Tree2`** models each tree through 8 growth stages with distinct sprites. Trees self-propagate by dropping seeds at random intervals; they also die after reaching maximum age. A proximity effect (green tint) gives visual feedback when a creature is feeding nearby.

**`main.py`** runs the game loop at 60 FPS with delta-time movement so speed is frame-rate independent. Proximity detection (Euclidean distance) handles both eating (creature–tree) and mating (creature–creature) collisions. A 25% chance on each digestion event triggers ecological seed dispersal, giving creatures an active role in shaping the environment.

---

## Sample Log Output

```
2024-09-14 11:39:08 - INFO - Simulation started
2024-09-14 11:39:14 - INFO - Creature ID:101-1 born. Parents: 100-0, 102-0. Speed: 10.52, Stomach: 21, Starvation limit: 9800ms
2024-09-14 11:39:21 - INFO - Creature ID:100-0 ate tree 601. Food: 18/20
2024-09-14 11:39:45 - INFO - Creature ID:103-2 STARVED. Lived 36.2s. Ate 4 times.
```

---

## Potential Extensions

- Vision radius — creatures detect food within a field of view instead of wandering randomly
- Predation — add carnivore creatures that hunt herbivores
- Energy model — replace discrete stomach units with a continuous energy budget
- Seasonal cycles — periodic food scarcity to drive stronger selection pressure
- Population graphs — real-time matplotlib overlay of population over time

---

## License

MIT
