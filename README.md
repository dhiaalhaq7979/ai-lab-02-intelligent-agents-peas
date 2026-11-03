# AI Lab 02 — Intelligent Agents and the PEAS Framework

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/dependencies-none-success?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

In this lab I studied how an AI **agent** is described and built. The case study is a *smart classroom* controller that reads the temperature and whether the room is occupied, then chooses a mode: `COOL`, `WARM`, `IDLE` or `ECO`.

I started with the simple reflex agent from the manual, then built a **model-based agent** that remembers its last mode so it never sends the same command twice. As an extra experiment I added a small **hysteresis** version to handle a noisy sensor.

## Project structure

```
ai-lab-02-intelligent-agents-peas/
├── run_lab.py               # runs everything
├── agents/
│   ├── reflex_agent.py      # manual section 2.5 – simple reflex agent
│   ├── memory_agent.py      # Task 3 – MemoryAgent + HysteresisAgent
│   └── test_scenarios.py    # my test cases and comparisons
└── results/
    └── sample_run.txt       # output of my run
```

## How to run

```bash
python run_lab.py
```

Only the Python standard library is used.

## PEAS summary (Task 1)

| | Campus delivery robot | University student-support chatbot |
|---|---|---|
| **Performance** | right receiver, on time, zero collisions, parcel undamaged, low energy | correct answers with a source, problem solved first time, escalates when unsure, protects privacy |
| **Environment** | footpaths, ramps, doors, lifts, pedestrians, bikes, weather, charging dock | students on the portal, course and policy documents, LMS data, support staff |
| **Actuators** | motors, steering, brakes, box lock, lights and speaker | chat replies, source links, support tickets, clarifying questions |
| **Sensors** | cameras, LiDAR / ultrasonic, GPS, odometry, IMU, battery level | student messages, retrieved documents, read-only LMS data, ticket updates |

**Environment type (Task 2):** both are *partially observable* (the robot cannot see around corners; the chatbot cannot know exactly what the student means) and *stochastic* (wet floors and people moving; different student reactions and model outputs).

My main takeaway: the performance measure must not reward speed alone. For the robot, safety is a hard limit; for the chatbot, "I could not find this, I sent it to staff" is better than a confident answer with no source.

## Task 3 — Agent with memory

`MemoryAgent` uses exactly the same rules as the reflex agent (`> 26 °C → COOL`, `< 20 °C → WARM`, empty room → `ECO` first), but stores `last_mode` and only sends a command when the mode changes.

| t | Last mode | Percept (°C, occupied) | Mode | Send? |
|---|-----------|------------------------|------|-------|
| 1 | – | (24, True) | IDLE | yes |
| 2 | IDLE | (24, True) | IDLE | no |
| 3 | IDLE | (27, True) | COOL | yes |
| 4 | COOL | (26, True) | IDLE | yes |
| 5 | IDLE | (20, True) | IDLE | no |
| 6 | IDLE | (18, True) | WARM | yes |
| 7 | WARM | (18, False) | ECO | yes |
| 8 | ECO | (30, False) | ECO | no |
| 9 | ECO | (31, True) | COOL | yes |

**9 / 9 checks passed.** The scenario covers a repeated percept, both exact limits (26 °C and 20 °C), mode changes, and the empty-room priority.

On the manual's percept list both agents choose the same modes, but the reflex agent sends **6** commands and my memory agent sends only **4**.

## Extra — noisy sensor and hysteresis

With readings jumping around 20 °C (19.8, 20.3, 19.6, 20.1, 19.9, 19.7), the memory agent still sends **5 commands in 6 steps**, because memory alone does not stop flickering at a limit. My `HysteresisAgent` adds a 0.5 °C dead band and sends only **1 command**.

## Author

**Dhia Alhaq Saleh Al-Hindrish** — BS Software Engineering, Superior University, Lahore
GitHub: [@dhiaalhaq7979](https://github.com/dhiaalhaq7979)

Licensed under the [MIT License](LICENSE).
