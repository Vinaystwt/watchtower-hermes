# WATCHTOWER 🗼
## Autonomous Self-Healing Infrastructure Agent
### Built on Hermes Agent | Nous Research Hackathon 2026

![Built on Hermes](https://img.shields.io/badge/Built%20on-Hermes%20Agent-blue)
![Status](https://img.shields.io/badge/Status-Active-green)
![Hardware](https://img.shields.io/badge/Hardware-MacBook%20Pro%202020%208GB-lightgrey)

---

## The Problem

3am. Server down. Engineer paged.
They investigate. They fix. They sleep.

Next week — same failure. Same investigation. Same fix.

**The system never learned. The engineer never slept.**

---

## The Solution

WATCHTOWER is an autonomous infrastructure agent 
built on Hermes Agent that:

- Monitors infrastructure health endpoints continuously
- Detects anomalies using EWMA statistical control limits
- Diagnoses failures using Bayesian fault probability
- Writes its own recovery skills for novel failures
- Recalls those skills instantly on future encounters
- Gets measurably faster with every incident

---

## Empirical Evidence

Real data. Not simulated.

| Incident | Failure Type | Time-to-Fix | Method |
|---|---|---|---|
| #1 | memory_leak | 36.2s | new_skill written |
| #2 | memory_leak | 0.8s | recalled_skill |

**44× improvement. Zero human code additions between sessions.**

---

## Hermes Integration

Hermes Agent autonomously:
- Read and understood the entire codebase
- Patched configuration files
- Launched the monitoring system
- Executed 15+ autonomous tool calls
- Wrote recovery skills to persistent Honcho memory

Tools used: `execute_code` · `read_file` · `patch` · 
`honcho_context` · `honcho_conclude`

---

## How It Works
```
HERMES AGENT (brain)
      ↓
WATCHTOWER (memory + learning)
      ↓
YOUR INFRASTRUCTURE (health endpoint)
      ↑
skills written back to Honcho memory
```

**The Loop:**
```
Observe → EWMA Detection → Bayesian Diagnosis →
Skill Exists? → Recall (0.8s) | Write New (36s) →
Update Honcho Memory → Repeat
```

---

## The Math

**EWMA anomaly detection:**
```
EWMA_t = λ·X_t + (1-λ)·EWMA_{t-1}
UCL = μ₀ + L·σ·√(λ/(2-λ))
```

**Bayesian fault attribution:**
```
P(failure | symptoms) ∝ P(symptoms | failure) × P(failure)
```

Priors update after each confirmed incident.
The agent gets smarter over time.

---

## Architecture
```
watchtower/
├── app/                    # Flask patient server
│   ├── app.py             # Health endpoint + failure injection
│   ├── Dockerfile
│   └── requirements.txt
├── monitor/               # Intelligence layer
│   ├── health_monitor.py  # EWMA anomaly detection
│   ├── bayesian_engine.py # Fault attribution
│   └── skill_manager.py   # Autonomous skill creation
├── skills/                # Self-authored recovery scripts
├── memory/                # Persistent learning data
│   └── learning_curve.log
├── watchtower_hermes.py   # Main Hermes-integrated loop
├── dashboard.py           # Terminal dashboard
├── inject_novel_failure.py
└── docker-compose.yml
```

---

## Run It
```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/watchtower-hermes
cd watchtower-hermes

# Start patient infrastructure
cd app && python3 app.py

# Open Hermes Agent
hermes

# Give Hermes this mission:
# "You are WATCHTOWER. Monitor localhost:5001/health.
#  Detect anomalies. Write skills. Show learning curve."
```

---

## Hardware

Built and demonstrated on:
```
MacBook Pro 2020
Intel Core i5
8GB RAM — No GPU — No cloud compute
```

**If Hermes runs on your machine — WATCHTOWER runs.**

---

## Results
```
44×   faster after learning
3     skills written autonomously
0     human code changes between sessions
15+   Hermes autonomous tool calls per session
```

---

## The Claim

Most agents execute tasks.

**WATCHTOWER accumulates operational expertise.**

The longer it runs, the more capable it becomes —
not because we updated the code,
but because it updated itself.

---

*Built for the Nous Research Hermes Agent Hackathon 2026*
*@NousResearch · Hermes Agent v0.2.0*
