
# SIH26146 — AI-Powered Bitcoin Transaction Traffic Analysis

> **An offline, explainable cryptocurrency forensic intelligence platform for NTRO**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red.svg)](https://streamlit.io/)
[![NetworkX](https://img.shields.io/badge/Graph-NetworkX-green.svg)](https://networkx.org/)
[![ML-XGBoost](https://img.shields.io/badge/ML-XGBoost-orange.svg)](https://xgboost.readthedocs.io/)
[![License](https://img.shields.io/badge/License-TBD-lightgrey.svg)](#license)

## Overview

SIH26146 asks for an **offline AI-powered system for monitoring and analyzing Bitcoin transaction traffic**.

Our system takes synthetic Bitcoin-style blockchain and network metadata and turns it into **ranked investigative leads**.

The pipeline combines:

- blockchain transaction information,
- IP/port/timestamp observations,
- entity correlation,
- graph analysis,
- behavioral and temporal features,
- machine learning,
- anomaly detection,
- clustering,
- explainability,
- and an investigator-oriented dashboard.

The goal is **not** to prove that an entity is criminal.

The goal is:

> **Detect unusual and suspicious behavioral patterns, correlate the surrounding evidence, rank the entities by risk, and explain why each entity was flagged.**

The system is designed to run **completely offline on Linux**.

---

# Why this project is different

A generic Bitcoin analytics project can stop at:

```text
CSV
 ↓
ML model
 ↓
"SUSPICIOUS"
```

That is not enough for this problem.

Our system instead follows:

```text
Raw data
   ↓
Validation + normalization
   ↓
Blockchain ↔ network correlation
   ↓
Entity / transaction graph
   ↓
Behavioral + graph + temporal features
   ↓
XGBoost primary detector
   +
Isolation Forest secondary anomaly signal
   +
Clustering / community context
   ↓
Risk fusion
   ↓
SHAP + graph evidence
   ↓
Ranked investigative alerts
   ↓
Interactive dashboard
```

The important distinction is that the final result contains **evidence**, not just a model score.

---

# Core features

## 1. Bulk data ingestion

Supports the project's Bitcoin-style metadata model, including fields such as:

```text
timestamp
TXID
input wallet
output wallet
amount
fee
script type
source IP
destination IP
source port
destination port
```

Input validation and normalization happen before the analytics pipeline.

---

## 2. Blockchain + network correlation

The project combines two types of information:

### Blockchain layer

```text
Wallet
TXID
Amount
Fee
Timestamp
Script type
```

### Network layer

```text
Source IP
Destination IP
Source port
Destination port
Timestamp
TXID
```

This allows the system to build richer investigative relationships such as:

```text
IP
 │
 │ observed around
 ▼
Transaction
 │
 ├── Input wallet
 │
 └── Output wallet
```

---

## 3. Entity / transaction graph

The graph is built using NetworkX.

Conceptually:

```text
             IP_03
               │
            OBSERVED
               │
              TX1
             /  \
            /    \
        WAL_A    WAL_B
                   │
                  TX2
                   │
                 WAL_C
```

Graph analysis is used for:

- entity correlation,
- transaction relationships,
- neighborhood analysis,
- centrality,
- PageRank,
- fan-in/fan-out behavior,
- evidence-path generation.

---

## 4. Common Input Ownership (CIO)

The system can provisionally group wallet inputs that are spent together.

For example:

```text
TX100

Inputs:
  A
  B
  C
```

can produce an entity relationship such as:

```text
A ─┐
B ─┼── probable common entity
C ─┘
```

CIO is treated as a **heuristic**, not absolute truth.

---

# Machine Learning architecture

## Primary detector — XGBoost

XGBoost is the project's primary supervised ML model.

It receives behavioral, temporal, network, and graph features and learns patterns associated with the suspicious scenarios represented in the training data.

Typical inputs include:

```text
transaction count
total amount
amount statistics
counterparty count
degree
in-degree
out-degree
PageRank
clustering coefficient
burstiness
unique IPs
IP reuse rate
fan-in ratio
fan-out ratio
entity cluster size
```

The primary model outputs a suspicious-behavior probability that becomes one of the signals used by the risk engine.

---

## Secondary detector — Isolation Forest

Isolation Forest provides an independent **unsupervised anomaly signal**.

It answers:

> "How unusual does this entity look compared with the rest of the population?"

It is deliberately kept separate from the supervised detector.

This is useful because an entity can be:

- suspicious according to learned patterns,
- statistically unusual,
- both,
- or neither.

The final risk engine can combine those signals.

---

## Clustering — DBSCAN / HDBSCAN

Clustering is used as a supporting analysis layer.

It answers:

> "Which entities have similar behavioral profiles?"

A cluster does **not** automatically mean suspicious activity.

Likewise, a DBSCAN noise point does not automatically mean criminal behavior.

Cluster membership is contextual evidence.

---

## Explainability — SHAP

For XGBoost, SHAP TreeExplainer is used to determine which features contributed most to an individual prediction.

Instead of showing only:

```text
Risk = 0.91
```

the system aims to show:

```text
Risk = 0.91

Main model contributors:
- fan_out_ratio
- burstiness
- ip_reuse_rate
- entity_cluster_size
```

These are then combined with graph/network evidence to form a human-readable explanation.

---

# Synthetic data

Because the SIH problem uses synthetic data, we do not simply generate random rows.

The generator creates behavioral scenarios such as:

```text
NORMAL
BURST
FAN_OUT
FAN_IN
CHAIN
MIXED
```

Example:

### FAN_OUT

```text
          B
         /
        C
       /
A ────
       \
        D
         \
          E
```

### FAN_IN

```text
A ──┐
B ──┤
C ──┼──> D
D?  ┘
```

### CHAIN

```text
A → B → C → D → E
```

The generator maintains internal ground-truth information so the team can measure the detector after prediction.

## Important

Ground-truth labels are **not allowed to become an accidental feature**.

They are used for:

- supervised training where appropriate,
- held-out evaluation,
- precision/recall/F1 measurement,

but are never included as an input feature.

The project also aims to evaluate under **distribution shift**, rather than relying only on a random train/test split.

For example:

```text
TRAIN
Peeling length: 3–5

TEST
Peeling length: 6–12
```

This is intended to reduce trivial memorization of the synthetic generator.

---

# Explainability philosophy

The system separates:

## Model evidence

What the ML model found important:

```text
fan_out_ratio
burstiness
ip_reuse_rate
degree
cluster_size
```

## Forensic evidence

What the graph/network shows:

```text
shared IP
common-input relationship
multi-hop transaction path
temporal burst
cluster membership
fan-in / fan-out structure
```

The final alert should combine both.

Example:

```text
HIGH PRIORITY — Entity W17

Risk: 91/100

Why flagged:
• unusually high fan-out behavior
• activity concentrated into a short time window
• IP observed across multiple wallet entities
• strong model contribution from burstiness
• connected to a high-risk behavioral cluster
```

This wording represents an **investigative lead**, not a criminal determination.

---

# Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                         INPUT                               │
│                 CSV / JSON / XML                            │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ M1 — DATA + INGESTION                                       │
│                                                             │
│ Parse → validate → normalize → synthetic generation         │
└─────────────────────────────┬───────────────────────────────┘
                              │
                    blockchain_df
                    network_df
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ M2 — GRAPH + ENTITY RESOLUTION                              │
│                                                             │
│ CIO → NetworkX graph → graph/temporal/network features      │
└─────────────────────────────┬───────────────────────────────┘
                              │
                         features_df
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ M3 — MACHINE LEARNING                                       │
│                                                             │
│ XGBoost        PRIMARY                                      │
│ Isolation      SECONDARY                                    │
│ Forest                                                     │
│ DBSCAN/HDBSCAN SUPPORT                                      │
│ SHAP           EXPLAINABILITY                               │
└─────────────────────────────┬───────────────────────────────┘
                              │
                         ml_output_df
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ M4 — RISK + INTEGRATION + OFFLINE                           │
│                                                             │
│ Signal fusion → risk score → ranked alerts → offline test   │
└─────────────────────────────┬───────────────────────────────┘
                              │
                           alerts
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ M5 — DASHBOARD                                              │
│                                                             │
│ Overview → Alerts → Investigation → Graph → Evidence        │
└─────────────────────────────────────────────────────────────┘

                 M6 — QA / DOCS / DEMO
              validates the whole system
```

---

# Repository structure

```text
sih26146-bitcoin-intel/
│
├── data/
│   ├── generator/
│   │   └── generate.py
│   └── synthetic/
│
├── src/
│   ├── ingestion/
│   │   └── loader.py
│   │
│   ├── graph/
│   │   ├── build_graph.py
│   │   ├── cio.py
│   │   └── features.py
│   │
│   ├── ml/
│   │   ├── detect.py
│   │   ├── preprocess.py
│   │   ├── evaluate.py
│   │   └── explain.py
│   │
│   ├── scoring/
│   │   └── risk_engine.py
│   │
│   └── pipeline.py
│
├── dashboard/
│   └── app.py
│
├── docs/
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   └── ...
│
├── docker/
│   ├── Dockerfile
│   └── build_offline.sh
│
├── scripts/
│   └── test_offline.sh
│
├── tests/
│
├── requirements.txt
├── AI_CONTEXT.md
└── README.md
```

The exact starter repository may contain fewer/more helper files while the implementation is in progress. The important boundaries are the module responsibilities above.

---

# Team roles

| Member | Role | Owns |
|---|---|---|
| M1 | Data + Ingestion | `data/generator/`, `src/ingestion/` |
| M2 | Graph + Entity Resolution | `src/graph/` |
| M3 | ML / Detection | `src/ml/` |
| M4 | Risk + Integration + Offline | `src/scoring/`, pipeline, `docker/` |
| M5 | Dashboard | `dashboard/` |
| M6 | QA + Documentation + Pitch | `docs/`, write-up, demo |

Detailed role-by-role implementation plans are maintained in:

```text
docs/index.html
```

---

# Getting started

## 1. Clone

```bash
git clone <REPOSITORY_URL>
cd sih26146-bitcoin-intel
```

## 2. Create a virtual environment

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

## 3. Install dependencies

During normal development:

```bash
pip install -r requirements.txt
```

For final offline deployment, do **not** rely on the internet. Use the project's local wheelhouse/offline packaging process.

## 4. Run tests

```bash
pytest
```

## 5. Start the dashboard

```bash
streamlit run dashboard/app.py
```

The exact application entry point may change while the pipeline is being integrated.

---

# Offline deployment

Offline operation is a hard project requirement.

The final system must not require:

```text
OpenAI API
Gemini API
Cloud ML APIs
Live Bitcoin APIs
CDNs
Runtime package installation
Internet model downloads
```

The deployment strategy is:

```text
Internet-connected preparation machine
            │
            ├── download Python wheels
            ├── prepare model artifacts
            ├── bundle local visualization assets
            └── build Docker image
                         │
                         ▼
                 Offline target machine
                         │
                         ▼
                  Run completely local
```

Typical wheel preparation:

```bash
pip download -d ./wheels -r requirements.txt
```

Offline installation:

```bash
pip install --no-index --find-links=./wheels -r requirements.txt
```

Docker backup:

```bash
docker save sih26146-bitcoin-intel -o sih26146-bitcoin-intel.tar
```

PyVis must use local resources:

```python
Network(cdn_resources="local")
```

---

# Testing philosophy

We do not only test whether "the page opens."

We test the full investigation pipeline.

## Data tests

```text
valid input
missing columns
invalid timestamps
invalid IP addresses
duplicate TXIDs
zero/negative amounts
empty files
```

## ML tests

```text
feature schema
no label leakage
prediction shape
metric calculation
distribution-shift evaluation
```

## Graph tests

```text
CIO correctness
node counts
edge counts
hand-checkable relationships
feature extraction
```

## Integration tests

```text
M1 → M2
M2 → M3
M3 → M4
M4 → M5
```

## Offline tests

Disable Wi-Fi/network and verify:

```text
application starts
data loads
models load
graph renders
alerts appear
explanations appear
```

---

# ML evaluation

The final report should contain measured results.

Do not invent numbers.

For XGBoost:

```text
Precision
Recall
F1
PR-AUC
ROC-AUC
Confusion matrix
```

For Isolation Forest:

```text
Precision
Recall
F1
```

The team should also compare:

```text
XGBoost
Isolation Forest
XGBoost + Isolation Forest
```

and document whether combining them actually improves the evaluation results.

---

# Limitations

This is an experimental hackathon system.

Important limitations include:

1. The official SIH dataset is synthetic.
2. Synthetic behavior does not represent real-world criminal ground truth.
3. CIO is a heuristic and can make incorrect entity associations.
4. Anomalous behavior is not proof of criminal behavior.
5. IP correlation is contextual evidence, not proof of wallet ownership.
6. Model performance on synthetic test data does not guarantee production performance.
7. Larger real-world graphs would require more sophisticated storage and computation strategies.

These limitations should be openly documented rather than hidden.

---

# Responsible interpretation

The system should use language such as:

```text
Anomalous behavior
Investigative lead
Flagged for review
Suspicious pattern
High-priority entity
```

Avoid presenting an alert as:

```text
Confirmed criminal
Confirmed laundering
Proven identity
```

The system helps investigators prioritize and inspect evidence; it does not replace human judgment.

---

# Suggested demo flow

A strong demonstration should be simple:

### 1. Load the dataset

Show:

```text
Transactions
Entities
IPs
```

### 2. Run investigation

Show the processing stages:

```text
✓ Data validated
✓ Entities correlated
✓ Graph built
✓ Features generated
✓ XGBoost executed
✓ Anomaly detection executed
✓ Alerts ranked
```

### 3. Open the highest-risk alert

Show:

```text
Entity ID
Risk score
XGBoost probability
Anomaly score
Cluster
```

### 4. Show "Why flagged"

Display:

```text
model evidence
+
graph evidence
+
network evidence
```

### 5. Show the evidence graph

Highlight the relevant neighborhood/path.

### 6. Demonstrate offline capability

Disable internet connectivity.

Run the application again.

---

# Development rules

## 1. Do not work directly on `main`

Use feature branches:

```text
feature/m1-data
feature/m2-graph
feature/m3-ml
feature/m4-risk
feature/m5-dashboard
docs/m6-qa
```

## 2. Keep module contracts stable

If you change a shared column or output object, tell the downstream member first.

## 3. Small commits

Prefer:

```text
add fan-out generator
add graph degree features
add xgboost baseline
add alert ranking
```

over:

```text
final changes
```

## 4. Build the MVP before advanced features

MVP:

```text
ingestion
→ graph
→ features
→ XGBoost
→ Isolation Forest
→ risk
→ alerts
→ dashboard
→ offline
```

Only after that consider additional improvements.

---

# What we are NOT building

Not part of the critical path:

```text
GNN
LLM chatbot
cloud deployment
mobile app
live blockchain indexing
microservices
Kubernetes
real-time external APIs
complex authentication
```

The goal is a **working, understandable, explainable offline forensic prototype**, not a production cryptocurrency surveillance platform.

---

# Further reading / project context

For internal team use:

```text
AI_CONTEXT.md
```

contains the detailed project context for AI-assisted mentoring.

The role-based team handbook is available through:

```text
docs/index.html
```

Open the documentation site to see:

```text
Main
M1
M2
M3
M4
M5
M6
```

Each role has its own learning and implementation roadmap.

---

# Project status

This repository is actively under development.

Current focus:

```text
[ ] Finalize official external schema
[ ] Synthetic generator
[ ] Ingestion
[ ] Graph
[ ] Feature engineering
[ ] XGBoost baseline
[ ] Isolation Forest
[ ] Clustering
[ ] SHAP
[ ] Risk engine
[ ] Dashboard
[ ] Offline packaging
[ ] Full evaluation
```

Do not report a feature as complete until it has been tested.

---

# License

License: **TBD**

This project is being developed for the Smart India Hackathon 2026 submission.

---

# Team principle

> **Build something the team understands, not something the AI happened to generate.**

Every major module should be explainable by its owner without opening ChatGPT.

The AI is a mentor, debugger, reviewer, and coding assistant.

The team owns the architecture and the final understanding of the system.
