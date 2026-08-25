
# SIH26146 — Full Team + Project Context for AI-Assisted Development
## Version 2 — Authoritative project context
### Give this entire file to an AI before asking for project help

---

# 0. HOW TO USE THIS FILE

This file is the shared memory of the SIH26146 team.

Every team member should be able to paste this entire document into Claude, ChatGPT, Gemini, Cursor, or another coding/teaching AI and then say:

> I am Member 3. What should I work on right now?

or:

> I am Member 2. Explain my next task from absolute zero.

or:

> I am Member 4. Here is my error. Tell me what is wrong without changing the architecture.

The AI should use THIS DOCUMENT as the project's source of truth.

## Important instructions for the AI reading this

1. Do not redesign the whole project unless the user explicitly asks for an architecture change.
2. Do not replace the chosen ML architecture with a GNN, deep-learning system, LLM, cloud API, or another stack just because it sounds more advanced.
3. The current official project decision is:
   - XGBoost is the PRIMARY supervised detector.
   - Isolation Forest is a SECONDARY unsupervised anomaly signal.
   - DBSCAN/HDBSCAN and graph/community analysis are SUPPORTING structure signals.
   - SHAP is the PRIMARY XAI mechanism for the XGBoost model.
4. The team has five technical members and one non-coding QA/documentation/demo member.
5. When a member asks what to do, explain the task in this order:
   - what the concept means,
   - why the project needs it,
   - what exact file to open,
   - what to implement,
   - how to test it,
   - what output to hand off,
   - what "done" means.
6. Do not dump unexplained code. The team members are second-year CSE(AI/ML) students and are new to graph analytics and machine learning.
7. Prefer the simplest implementation that satisfies the PS. Complexity is not a goal.
8. Do not introduce dependencies that are not already approved by the project.
9. If the user gives an error, inspect the stated file/interface and preserve the module contract unless there is a documented reason to change it.
10. The system detects anomalies/investigative leads. It does NOT prove criminality, laundering, identity, or guilt.

---

# 1. PROJECT IN ONE PARAGRAPH

We are building an offline cryptocurrency forensic/intelligence prototype for Smart India Hackathon 2026 problem statement SIH26146 for NTRO.

The system receives synthetic Bitcoin-style blockchain and network metadata. It combines the blockchain layer (wallets, TXIDs, amounts, fees, timestamps) with the network layer (IP addresses, ports, timestamps), converts those relationships into a heterogeneous graph, derives behavioral/graph/temporal features for each wallet/entity, applies an ML detector, ranks suspicious entities, explains why the model considered them suspicious, and displays the result in an investigator-style dashboard.

The application must work on Linux with the internet completely disabled at runtime.

The project's key idea is:

> We are not trying to declare that an entity is a criminal. We are trying to discover unusual and suspicious behavioral patterns, correlate the evidence around those entities, and present ranked investigative leads to a human investigator.

---

# 2. OFFICIAL PS REQUIREMENTS WE ARE DESIGNING AROUND

The project must be capable of:

1. Ingesting bulk Bitcoin/network metadata in CSV/JSON/XML form.
2. Handling fields such as timestamp, source/destination IP and port, TXID, input/output wallet addresses, amounts, fee, and script type.
3. Correlating blockchain-layer and network-layer observations.
4. Building an entity/transaction graph connecting IPs, wallets, and transactions.
5. Running a real AI/ML model, not merely hand-written threshold rules.
6. Producing a ranked and explainable alert list.
7. Showing the findings in a dashboard or link-analysis visualization.
8. Running completely offline on Linux.

The team's final deliverables are:

- working repository,
- working ingestion + correlation + ML pipeline,
- technical write-up,
- dashboard/visualization with evidence.

The exact final official PS wording and minimum official field list must be verified against the current SIH portal before freezing the external input schema. Internal project interfaces below are the team's working contracts.

---

# 3. WHAT THE USER SEES VS WHAT IS UNDER THE HOOD

## What the user sees

```text
Upload Dataset
      ↓
Run Investigation
      ↓
Ranked Alerts
      ↓
Click an Entity
      ↓
See Graph + Timeline + Reasons
```

## What actually happens

```text
CSV / JSON / XML
        ↓
INGESTION
        ↓
VALIDATED DATAFRAMES
        ↓
CORRELATION
        ↓
ENTITY / TRANSACTION GRAPH
        ↓
FEATURE ENGINEERING
        ↓
XGBOOST PRIMARY DETECTOR
        +
ISOLATION FOREST SECONDARY SIGNAL
        +
CLUSTER / COMMUNITY SIGNALS
        +
NETWORK CORRELATION
        ↓
RISK FUSION
        ↓
RANKED ALERTS
        ↓
SHAP + FORENSIC EVIDENCE
        ↓
DASHBOARD
```

---

# 4. THE CORE IDEA IN PLAIN ENGLISH

Imagine an investigator has thousands or millions of records.

A spreadsheet can tell them:

```text
Wallet A sent 4.2 BTC to Wallet B.
Wallet B sent 4.0 BTC to Wallet C.
IP 10.0.0.3 was observed around both transactions.
```

But the investigator wants to know:

> "Are these records part of one interesting behavioral pattern?"

So the system turns those rows into a graph:

```text
             IP_03
               │
           observed
               │
              TX1
             /  \
            /    \
        WAL_A    WAL_B
                   │
                 sends
                   │
                  TX2
                   │
                 WAL_C
```

Then it computes features such as:

- how many transactions the wallet is involved in,
- how many counterparties it has,
- how quickly it sends/receives funds,
- how many IPs it is associated with,
- whether it has fan-in/fan-out behavior,
- how central it is in the graph,
- how large its entity cluster is.

These numbers are what the ML models use.

---

# 5. WHY WE USE A GRAPH

The graph is NOT itself the ML model.

The graph solves the relationship problem.

A normal table naturally answers:

> "What happened in this row?"

A graph helps answer:

> "What is this entity connected to, and what happens around it?"

Example:

```text
Wallet A
  │
  ├── TX1 → Wallet B
  │
  ├── TX2 → Wallet C
  │
  └── observed from IP X

Wallet B
  │
  └── TX3 → Wallet D

Wallet C
  │
  └── TX4 → Wallet D
```

That structure creates signals such as:

- A has high fan-out.
- B and C converge on D.
- A and B may be part of one flow.
- IP X is associated with multiple entities.
- D is a convergence point.

These graph properties become ML features AND investigator evidence.

---

# 6. OUR FINAL ML DECISION

## Primary model: XGBoost

XGBoost is the main supervised detector.

It answers:

> "Given the behavioral and graph features we know about an entity, how strongly does this entity resemble the suspicious scenarios represented in our training data?"

Why it is primary:

- strong performance on structured/tabular data,
- works well on CPU,
- handles nonlinear feature interactions,
- fast enough for the hackathon,
- easier to debug than a GNN,
- works cleanly with SHAP TreeExplainer,
- produces a probability-like prediction that can be calibrated/used as one component of the final risk score.

Research used by the team reports strong performance for tree/boosting models on the Elliptic benchmark, including approximately F1 0.8265 for GBM with structural graph features and approximately F1 0.82 for Random Forest under a strict temporal evaluation in a separate 2026 study.

These benchmark numbers are NOT guarantees for our synthetic data.

## Secondary model: Isolation Forest

Isolation Forest remains in the architecture because it provides an independent unsupervised signal.

It answers:

> "Does this entity look statistically unusual compared with the population?"

It does not answer:

> "Is this criminal?"

This gives us a useful independent signal that does not require labels.

## Supporting: DBSCAN/HDBSCAN

Clustering answers:

> "Which entities behave similarly, and which entities do not belong to a dense group?"

A cluster is not automatically suspicious.

A DBSCAN noise point is not automatically criminal.

Cluster IDs are evidence/context that go into the risk layer.

## Supporting: graph/community analysis

Graph metrics and optionally Louvain/community analysis answer:

> "How is this entity connected to the rest of the network?"

This is an investigation/evidence layer, not the sole detector.

## Explainability: SHAP

For XGBoost, SHAP TreeExplainer is used to answer:

> "Which features pushed this model's prediction upward or downward?"

The UI should translate those feature contributions into plain English.

Example:

```text
Risk: 0.91

Main model contributors:
- fan_out_ratio
- burstiness
- ip_reuse_rate
- entity_cluster_size
- tx_count
```

Then the evidence layer can add:

```text
Additional evidence:
- IP observed with 5 other wallets
- 8-hop transaction chain
- unusually dense activity in a short time window
```

---

# 7. THE IMPORTANT SYNTHETIC-LABEL DECISION

This project has synthetic data.

That means WE write the scenario generator.

If we generate:

```text
FAN_OUT
ground_truth = suspicious
```

and then train a model directly on the exact same generator patterns, a judge can reasonably ask:

> "Didn't you just teach the model your own rules?"

That criticism is valid.

So our evaluation must be designed to reduce this problem.

## Labels are allowed for supervised XGBoost training

Because XGBoost is the primary supervised detector, it DOES use the synthetic training labels.

But we must NOT perform a trivial random split and claim that proves real-world intelligence.

Instead, use separate distributions:

```text
TRAIN GENERATOR
    ↓
training scenarios

VALIDATION GENERATOR
    ↓
different parameter ranges

TEST GENERATOR
    ↓
different parameter ranges / scenario mixes / seeds
```

Example:

```text
TRAIN
Peeling length: 3–5
Burst: 50–100 tx/min
Fan-out: 5–15 outputs

TEST
Peeling length: 6–12
Burst: 120–250 tx/min
Fan-out: 20–40 outputs
```

The model is therefore tested on behavior that is related to the learned concepts but not an exact copy of its training distribution.

## Labels also remain available for evaluation

Even for Isolation Forest:

```text
ground_truth
```

is used AFTER prediction to calculate:

- precision,
- recall,
- F1,
- PR-AUC,
- confusion matrix.

Never expose `ground_truth_anomalous` as an input feature.

---

# 8. WHY WE ARE NOT USING A GNN

We know Bitcoin data is a graph, so a GNN sounds attractive.

We explicitly choose not to make a GNN the critical path because:

- it adds significant implementation complexity,
- graph leakage can make benchmark results misleading,
- CPU-only execution is less comfortable,
- explanations are harder to surface cleanly,
- the graph already provides huge value through feature engineering and evidence visualization.

The project should be able to answer:

> "Why don't you use GNN?"

with:

> "We use graph structure where it provides the most operational value: entity resolution, graph features, community/context analysis, and evidence visualization. For the primary detector we use CPU-friendly gradient boosting because it gives us strong structured-data performance and straightforward SHAP explanations. We also keep an independent Isolation Forest signal for unsupervised anomaly detection."

---

# 9. END-TO-END SYSTEM ARCHITECTURE

```text
                       INPUT
              CSV / JSON / XML
                       │
                       ▼
        ┌─────────────────────────────┐
        │        M1 DATA LAYER        │
        │                             │
        │ parse                       │
        │ validate                    │
        │ normalize                   │
        │ generate synthetic data     │
        └──────────────┬──────────────┘
                       │
              blockchain_df
              network_df
                       │
                       ▼
        ┌─────────────────────────────┐
        │       M2 GRAPH LAYER        │
        │                             │
        │ CIO entity clustering       │
        │ graph construction          │
        │ graph features              │
        │ network correlation         │
        └──────────────┬──────────────┘
                       │
                   features_df
                       │
                       ▼
        ┌─────────────────────────────┐
        │          M3 ML              │
        │                             │
        │ XGBoost (PRIMARY)            │
        │ Isolation Forest (SECONDARY)│
        │ DBSCAN/HDBSCAN              │
        │ SHAP                        │
        └──────────────┬──────────────┘
                       │
                   ml_output_df
                       │
                       ▼
        ┌─────────────────────────────┐
        │     M4 RISK / INTEGRATION   │
        │                             │
        │ normalize signals           │
        │ fuse evidence               │
        │ calculate risk              │
        │ generate explanations       │
        │ create ranked alerts        │
        │ offline packaging           │
        └──────────────┬──────────────┘
                       │
                    alerts
                       │
                       ▼
        ┌─────────────────────────────┐
        │          M5 UI              │
        │                             │
        │ Overview                    │
        │ Alert list                  │
        │ Investigation               │
        │ graph                       │
        │ timeline                    │
        │ explanation                 │
        └─────────────────────────────┘

               M6 WATCHES ALL LAYERS
             QA + docs + demo + pitch
```

---

# 10. TECH STACK

Approved baseline:

```text
Python
pandas
numpy
faker
networkx
scikit-learn
xgboost
shap
streamlit
pyvis
joblib
pytest
docker
```

Do not add large technologies unless the team explicitly agrees.

Do not make these dependencies:

```text
OpenAI API
Gemini API
Cloud ML API
live Bitcoin APIs
internet lookups
CDN assets
PyTorch
TensorFlow
Transformers
```

The application must run without internet.

---

# 11. REPOSITORY OWNERSHIP — 5 TECHNICAL MEMBERS

The team has SIX people total.

Five are technical owners:

| Member | Role | Main ownership |
|---|---|---|
| M1 | Data + Ingestion | `data/generator/`, `src/ingestion/` |
| M2 | Graph + Entity Resolution | `src/graph/` |
| M3 | ML / Detection | `src/ml/` |
| M4 | Risk + Integration + Offline | `src/scoring/`, `docker/`, pipeline |
| M5 | Dashboard / Product UI | `dashboard/`, UI assets |
| M6 | QA + Documentation + Pitch | `docs/`, write-up, test plans, demo |

M6 is intentionally non-coding. This is a real responsibility, not a filler role.

---

# 12. SHARED MODULE CONTRACTS

These interfaces are more important than the internal implementation.

Do not randomly rename columns.

## M1 output

```python
blockchain_df: pd.DataFrame
network_df: pd.DataFrame
```

## M2 output

```python
graph: nx.MultiDiGraph
features_df: pd.DataFrame
```

## M3 output

```python
ml_output_df: pd.DataFrame
```

## M4 output

```python
alerts: list[dict]
```

## M5 consumes alerts

M5 should NOT re-run ML.

---

# 13. DATA SCHEMAS

These are the team's working internal schemas. Verify exact official external fields against the final PS before freezing the upload contract.

## blockchain_df

```text
timestamp
txid
input_wallet
output_wallet
amount_btc
fee_btc
script_type
ground_truth_anomalous
scenario_type
```

Types:

```text
timestamp               datetime64
txid                    str
input_wallet            str
output_wallet           str
amount_btc              float
fee_btc                 float
script_type             str
ground_truth_anomalous  bool
scenario_type           str
```

Rules:

- `amount_btc > 0`
- `fee_btc >= 0`
- `txid` unique per transaction record
- `ground_truth_anomalous` is evaluation/training-label metadata, not a feature
- `scenario_type` is internal ground truth metadata, not a model feature

## network_df

```text
timestamp
src_ip
src_port
dst_ip
dst_port
txid
```

Rules:

- no ground-truth field in this DataFrame
- `txid` links to blockchain_df
- timestamps should be consistent with transaction observations

## features_df

One row per wallet/entity after entity clustering.

Recommended feature set:

```text
entity_id
degree
in_degree
out_degree
unique_counterparties
pagerank
clustering_coefficient
betweenness_centrality
tx_count
total_amount_btc
mean_amount_btc
std_amount_btc
total_fees_btc
fee_ratio
burstiness
unique_ips
wallets_per_ip
ip_reuse_rate
fan_in_ratio
fan_out_ratio
active_hours
entity_cluster_size
```

Potential later features:

```text
peeling_length
community_size
k_core
mean_interarrival
max_interarrival
unique_ports
transactions_per_ip
country_count
ASN_count
```

Only add expensive features after the MVP works.

## ml_output_df

FINAL target schema should support:

```text
entity_id
xgb_probability
anomaly_score
is_anomaly
cluster_id
cluster_size
shap_top_features
```

Where:

- `xgb_probability` = primary supervised model output.
- `anomaly_score` = normalized Isolation Forest signal.
- `is_anomaly` = Isolation Forest threshold/flag.
- `cluster_id` = DBSCAN/HDBSCAN label.
- `shap_top_features` = top contributing features from XGBoost.

## alerts

Each alert should look like:

```python
{
    "entity_id": "W17",
    "risk_score": 91,
    "priority": "HIGH",
    "cluster_id": 4,
    "xgb_probability": 0.89,
    "anomaly_score": 0.93,
    "reasons": [
        "High fan-out behavior",
        "Unusually bursty transaction activity",
        "IP reused across multiple wallets"
    ],
    "model_evidence": [
        ("fan_out_ratio", 0.31),
        ("burstiness", 0.18)
    ],
    "graph_evidence": [
        "2-hop connection to anomalous entity cluster"
    ]
}
```

---

# 14. MEMBER 1 — DATA + INGESTION

## Owns

```text
data/generator/
src/ingestion/
```

## Main job

Make reliable input.

Everything downstream assumes your data is correct.

## Learn first

1. Python file I/O.
2. pandas DataFrames.
3. CSV/JSON reading.
4. Data validation.
5. Datetime handling.
6. Synthetic data generation.
7. Why correlated synthetic datasets are better than random rows.

## Build in this order

### Task 1 — schema

Create a documented internal schema.

Done when:

- required columns are explicit,
- types are defined,
- M2 has reviewed it.

### Task 2 — loaders

Implement:

```text
load_blockchain_layer()
load_network_layer()
```

Done when:

- small valid file loads,
- missing columns fail clearly,
- incorrect types are handled.

### Task 3 — validation

Implement:

```text
validate_schema()
```

Check:

- required columns,
- timestamp validity,
- amount validity,
- TXID validity,
- duplicate TXIDs,
- IP validity.

### Task 4 — wallet/tx/IP generators

Implement helpers such as:

```text
make_wallet()
make_txid()
make_ip()
```

### Task 5 — normal scenario

Implement ordinary activity first.

### Task 6 — suspicious scenarios

Implement:

```text
BURST
FAN_OUT
FAN_IN
CHAIN
MIXED
```

Do not begin with hundreds of scenarios.

### Task 7 — network layer

Generate network observations linked to transaction IDs.

This is critical because the project is specifically about correlating network and blockchain information.

### Task 8 — evaluation metadata

Keep:

```text
ground_truth_anomalous
scenario_type
```

inside the generated data but keep them out of model features.

### Task 9 — multiple generator modes

Provide something like:

```text
generate_train_dataset()
generate_validation_dataset()
generate_test_dataset()
```

or a configuration that changes the distributions.

The important thing is that test behavior isn't a copy of train behavior.

## Handoff

Give M2:

```text
blockchain_df
network_df
```

Give M3:

```text
ground_truth labels
```

ONLY after inference/evaluation is required.

## M1 done when

```text
python -c "
from data.generator.generate import generate_dataset
bc, net = generate_dataset(...)
print(bc.shape, net.shape)
print(bc.columns)
print(net.columns)
"
```

works and M2 confirms the data is usable.

## Biggest mistake

Random fake rows with random labels.

That creates a toy database, not a behavioral simulation.

---

# 15. MEMBER 2 — GRAPH + ENTITY RESOLUTION

## Owns

```text
src/graph/
```

## Main job

Turn rows into relationships and derive structural features.

## Learn first

1. Node and edge.
2. Directed graphs.
3. Weighted graphs.
4. NetworkX.
5. Degree.
6. PageRank.
7. centrality.
8. clustering coefficient.
9. connected components.
10. CIO / entity clustering.

## Graph shape

Use a heterogeneous graph conceptually like:

```text
IP
 │
 │ observed
 ▼
TX
 │
 ├── input → Wallet
 │
 └── output → Wallet
```

Wallet-to-wallet transaction relationships can be derived from transaction records.

## Task 1 — CIO

Understand:

> multiple input addresses spent together can be treated as a probable shared entity.

Use Union-Find.

Do NOT claim that the link is perfect.

Store:

```text
method = "CIO"
confidence = ...
```

## Task 2 — graph builder

Implement:

```text
build_graph()
```

It should create:

```text
wallet nodes
tx nodes
ip nodes
```

and appropriate edges.

## Task 3 — graph statistics

Compute:

```text
node count
edge count
degree distributions
```

## Task 4 — feature extraction

Implement:

```text
extract_graph_features()
```

Start with:

```text
degree
in_degree
out_degree
unique_counterparties
pagerank
clustering_coefficient
betweenness_centrality
```

Then add:

```text
fan_in_ratio
fan_out_ratio
entity_cluster_size
```

## Task 5 — temporal features

Compute:

```text
tx_count
active_hours
burstiness
mean_interarrival
```

## Task 6 — network features

Use the network layer to derive:

```text
unique_ips
wallets_per_ip
ip_reuse_rate
unique_ports
```

## Task 7 — performance

Only after correctness:

- profile graph operations,
- avoid expensive algorithms on enormous graphs unnecessarily,
- consider pruning or staged computation for expensive centrality measures.

## Handoff

Give M3:

```text
features_df
```

Give M4:

raw graph or enough identifiers/evidence to build the investigation subgraph.

## M2 done when

A small hand-checkable dataset produces graph relationships that humans can verify manually.

Example:

```text
A → B
A → C
B → D
C → D
```

must produce the expected degrees and relationships.

## Biggest mistake

Implementing a fancy graph while the underlying links are wrong.

Correctness first.

---

# 16. MEMBER 3 — ML / DETECTION

## Owns

```text
src/ml/
```

## Main job

Build and evaluate the project's actual AI/ML detection layer.

## Current architecture

```text
features_df
      │
      ├───────────────► XGBoost PRIMARY
      │
      ├───────────────► Isolation Forest SECONDARY
      │
      └───────────────► DBSCAN/HDBSCAN SUPPORT
```

## Learn first

### 1. Features and labels

Understand:

```text
X = features
y = target label
```

### 2. Train/validation/test

Understand why:

```text
train ≠ test
```

and why temporal/distribution-shift evaluation is better than a random split for this project.

### 3. Overfitting

Learn:

> a model can perform extremely well on data resembling its training examples while failing on unseen patterns.

### 4. Classification metrics

Learn:

```text
precision
recall
F1
PR-AUC
ROC-AUC
confusion matrix
```

For an imbalanced detection problem, understand why accuracy alone is insufficient.

### 5. XGBoost

Learn only the practical core:

```text
fit()
predict()
predict_proba()
```

and parameters such as:

```text
n_estimators
max_depth
learning_rate
subsample
colsample_bytree
```

### 6. Isolation Forest

Understand it as the independent "unusualness" detector.

### 7. DBSCAN/HDBSCAN

Understand:

```text
dense region
noise
eps
min_samples
```

### 8. SHAP

Understand local feature contribution.

---

## M3 implementation order

### Task 1 — toy XGBoost

Before touching Bitcoin data, train XGBoost on a tiny table.

Goal:

```text
features
  ↓
model
  ↓
probability
  ↓
prediction
```

Done when you understand what `predict_proba()` returns.

### Task 2 — feature preprocessing

Create:

```text
src/ml/preprocess.py
```

Responsible for:

- selecting feature columns,
- handling missing values,
- optional scaling where appropriate,
- maintaining a stable feature order.

Tree models do not require standardization for performance in the same way as distance-based algorithms, so do NOT automatically standardize everything for XGBoost just because you saw `StandardScaler` in an ML tutorial.

DBSCAN is a distance-based algorithm, so its input should be appropriately scaled/normalized.

This distinction matters.

### Task 3 — XGBoost training

Implement:

```text
train_xgboost_classifier()
```

Inputs:

```text
features_df
training labels
```

Outputs:

```text
model
feature_names
```

Do NOT include:

```text
entity_id
scenario_type
ground_truth_anomalous
```

as features.

### Task 4 — prediction

Implement:

```text
predict_xgboost()
```

Return:

```text
xgb_probability
xgb_prediction
```

### Task 5 — evaluation

Implement:

```text
evaluate_xgboost()
```

Calculate:

```text
precision
recall
F1
PR-AUC
ROC-AUC
confusion matrix
```

Do this on a held-out test set.

### Task 6 — distribution-shift testing

This is important.

Do NOT only test:

```text
random 80/20
```

Use separate synthetic generator settings.

Example:

```text
TRAIN:
chain lengths 3–5

TEST:
chain lengths 6–12
```

Also create a different mix of suspicious scenarios in test data.

### Task 7 — SHAP

Implement:

```text
explain_xgboost()
```

For a selected entity:

```text
top feature
SHAP contribution
feature value
```

Return a small stable structure that M4 can serialize.

### Task 8 — Isolation Forest

Implement:

```text
train_anomaly_detector()
predict_anomaly()
```

Do NOT feed labels to this model.

Return:

```text
anomaly_score
is_anomaly
```

### Task 9 — DBSCAN/HDBSCAN

Implement:

```text
cluster_entities()
```

Use a scaled numerical feature matrix.

Experiment with:

```text
eps
min_samples
```

and document why the chosen values were selected.

### Task 10 — combine outputs

Produce:

```text
ml_output_df
```

with:

```text
entity_id
xgb_probability
anomaly_score
is_anomaly
cluster_id
cluster_size
shap_top_features
```

---

# 17. CRITICAL M3 RULE — NO LEAKAGE

Never do:

```python
FEATURE_COLUMNS = [
    ...,
    "ground_truth_anomalous"
]
```

Never do:

```python
X = df.drop(...)
```

without explicitly checking what remains.

Use an explicit feature allowlist.

The safe pattern is:

```python
FEATURE_COLUMNS = [
    "degree",
    "in_degree",
    "out_degree",
    "unique_counterparties",
    "pagerank",
    "clustering_coefficient",
    "betweenness_centrality",
    "tx_count",
    "total_amount_btc",
    "mean_amount_btc",
    "std_amount_btc",
    "total_fees_btc",
    "fee_ratio",
    "burstiness",
    "unique_ips",
    "wallets_per_ip",
    "ip_reuse_rate",
    "fan_in_ratio",
    "fan_out_ratio",
    "active_hours",
    "entity_cluster_size"
]
```

This protects against accidental future leakage.

---

# 18. WHAT M3 HANDS TO M4

M3 does NOT hand M4 a final criminal verdict.

M3 hands:

```text
entity_id
xgb_probability
anomaly_score
is_anomaly
cluster_id
cluster_size
shap_top_features
```

M4 decides how these signals participate in the final risk score.

Example:

```text
XGBoost probability = 0.86
Isolation anomaly   = 0.91
Cluster context     = high
Graph evidence      = strong
Network evidence    = moderate
```

M4 then produces the final investigative risk.

---

# 19. MEMBER 4 — RISK + INTEGRATION + OFFLINE

## Owns

```text
src/scoring/
docker/
pipeline/orchestration files
```

## Main job

Connect the entire system and make the result usable.

## Learn first

1. Python modules/interfaces.
2. JSON.
3. pipeline orchestration.
4. weighted scoring.
5. Docker basics.
6. offline packaging.
7. integration testing.

## Task 1 — create the pipeline

Create/maintain a single orchestration entry point such as:

```text
src/pipeline.py
```

Conceptually:

```python
def run_pipeline(input_path):
    data = ingest(input_path)
    graph, features = build_graph(data)
    ml_output = run_ml(features)
    alerts = build_alerts(ml_output, graph, data)
    return alerts
```

The actual function names can differ; the important idea is one reliable entry point.

## Task 2 — provisional scoring

Start with a simple configurable fusion:

```text
risk =
    w1 * xgb_probability
  + w2 * anomaly_score
  + w3 * graph_signal
  + w4 * network_signal
  + w5 * cluster_signal
```

Normalize each component first.

Do not claim the weights are scientifically universal.

Tune them using validation data.

## Task 3 — explanations

Turn model evidence + graph evidence into human-readable text.

Example:

```text
Why flagged:
- model identifies a strong suspicious behavioral pattern
- unusually high fan-out
- IP reused across multiple wallet entities
- activity concentrated into a short time window
```

## Task 4 — ranked alerts

Sort:

```text
highest risk → lowest risk
```

and assign:

```text
HIGH
MEDIUM
LOW
```

## Task 5 — offline package

Create:

```text
requirements lock
local wheelhouse
Docker image
Docker tar archive
```

Runtime must not need:

```text
pip install from internet
```

## Task 6 — offline test

Run with Wi-Fi disabled.

Test:

```text
application starts
dataset loads
model loads
graph renders
alerts appear
explanation appears
```

## Handoff

M4 gives M5:

```text
alerts: list[dict]
```

M5 should not know how the risk score was internally computed.

## Biggest mistake

Waiting until everything is "finished" before integrating.

M4 should integrate fake outputs first.

---

# 20. MEMBER 5 — DASHBOARD / PRODUCT UI

## Owns

```text
dashboard/
```

## Main job

Turn the pipeline into a tool an investigator can understand in under a minute.

## Learn first

1. Streamlit basics.
2. PyVis basics.
3. basic dashboard UX.
4. local/offline assets.
5. how to consume JSON/Python objects without knowing ML internals.

## Build in this order

### Page 1 — Overview

Show:

```text
Transactions
Entities
IPs
Alerts
High-risk alerts
```

Also show a short pipeline status:

```text
Ingestion ✓
Graph ✓
ML ✓
Scoring ✓
```

### Page 2 — Alert list

Table:

```text
Rank
Entity
Risk
Priority
Cluster
Main reason
```

Sort high risk first.

### Page 3 — Investigation

When selecting an entity:

```text
Entity summary
Risk score
XGBoost probability
Anomaly score
Top reasons
Graph
Timeline
```

### Graph view

Use PyVis locally.

Important:

```python
Network(cdn_resources="local")
```

Do not use a CDN.

### Filters

Add:

```text
risk range
priority
cluster
entity ID search
```

Only after the basic page works.

## Handoff

A working dashboard for M6 to rehearse and the whole team to demo.

## Biggest mistake

Spending hours polishing colors before the actual investigation workflow works.

---

# 21. MEMBER 6 — QA + DOCUMENTATION + PITCH

## Owns

```text
docs/
technical write-up
test plans
demo script
judge Q&A
```

No coding required for the core system.

## Main job

Know the whole project well enough to:

- explain it,
- test it,
- challenge it,
- prepare the team for judges.

## Learn

1. Bitcoin vocabulary.
2. graph basics.
3. XGBoost vs Isolation Forest.
4. SHAP.
5. offline architecture.
6. the project's limitations.

## QA checklist

Test:

```text
empty file
missing columns
wrong type
invalid IP
duplicate TXID
negative amount
very large file
```

Also:

```text
internet disabled
```

and verify the entire pipeline.

## Write-up

Explain:

```text
problem
architecture
data generation
graph methodology
ML approach
evaluation
XAI
offline deployment
limitations
future work
```

## Demo

Prepare one known scenario:

```text
FAN_OUT
```

and one mixed scenario.

Know the exact injected behavior and actual measured model result.

Never invent a performance number.

## Judge language

Say:

```text
anomalous behavior
investigative lead
flagged for review
suspicious pattern
```

Do not say:

```text
criminal
confirmed laundering
proved identity
```

The system does not establish those claims.

---

# 22. TEAM-WIDE TEST DATA STRATEGY

We need at least three datasets.

## Dataset A — development

Small:

```text
100–1,000 wallets
```

Purpose:

- debugging,
- hand-checking.

## Dataset B — validation

Medium:

```text
5,000–20,000 wallets
```

Purpose:

- tuning features,
- model parameters,
- risk weights.

## Dataset C — test

Different seed and different distributions.

Purpose:

- final numbers,
- distribution shift.

Do not show test labels to M3 during ordinary development.

---

# 23. MODEL EVALUATION

## XGBoost

Measure:

```text
precision
recall
F1
PR-AUC
ROC-AUC
```

Primary concern:

> how many suspicious examples are correctly detected without producing an unusable number of false alerts?

## Isolation Forest

Measure:

```text
precision
recall
F1
```

against synthetic ground truth AFTER prediction.

## Hybrid

Compare:

```text
XGBoost
Isolation Forest
XGBoost + Isolation Forest
```

Do not assume the hybrid wins.

Measure it.

---

# 24. WHY PR-AUC MATTERS

Suppose:

```text
100,000 normal entities
1,000 suspicious entities
```

A stupid model can achieve approximately:

```text
99% accuracy
```

by declaring everything normal.

That tells us almost nothing.

Precision/recall and PR-AUC are more informative when the positive class is relatively rare.

---

# 25. RISK SCORE

M4 can start with:

```text
XGBoost probability
        +
Isolation score
        +
graph signal
        +
network signal
        +
cluster context
```

Example starting weights:

```text
XGBoost        40%
Isolation      20%
Graph          20%
Network        10%
Cluster        10%
```

These are NOT ground truth.

The team must experiment.

The write-up should say:

> weights were treated as configurable parameters and evaluated against held-out synthetic scenarios.

---

# 26. EXPLANATION DESIGN

Do not make the dashboard print:

```text
SHAP = 0.17234
```

Instead:

```text
RISK: 91/100

Why this entity is high priority:

1. High fan-out behavior
2. Strong model contribution from burstiness
3. IP reused across several entities
4. Part of a large correlated cluster
5. Rapid downstream movement
```

The explanation should have TWO layers.

## Model evidence

```text
feature
value
SHAP contribution
```

## Forensic evidence

```text
graph relationship
IP relationship
transaction path
temporal pattern
cluster membership
```

Keep these conceptually separate.

---

# 27. OFFLINE REQUIREMENT

Offline means:

> the application continues to run when the network is disabled.

The strongest interpretation is:

> the target machine should not need internet even to install dependencies.

Therefore prepare:

```text
wheelhouse/
model artifacts/
PyVis local assets/
application files/
```

before final offline testing.

Do not:

```text
download model at runtime
call API
fetch CDN
pip install from internet
```

---

# 28. GITHUB / GIT RULES

Never work directly on `main`.

Use:

```text
feature/m1-generator
feature/m2-graph
feature/m3-xgboost
feature/m4-scoring
feature/m5-dashboard
docs/m6-qa
```

Each commit should explain what changed.

Good:

```text
add temporal features to entity table
```

Bad:

```text
updates
```

Before opening a pull request:

```text
run tests
run relevant sample
check imports
check schema
```

---

# 29. 36-HOUR BUILD PLAN

This is the FINAL hackathon plan after the pre-hackathon learning is done.

## Hours 0–3

M1:
- input schema
- tiny dataset

M2:
- graph skeleton

M3:
- ML environment + toy test

M4:
- pipeline skeleton + output contracts

M5:
- dashboard skeleton

M6:
- demo script + test checklist

## Hours 3–8

M1:
- generator scenarios

M2:
- graph construction + CIO

M3:
- feature pipeline + XGBoost baseline

M4:
- scoring using mock ML output

M5:
- alert page

M6:
- QA M1/M2

## Hours 8–14

M1:
- network generation + validation

M2:
- graph features

M3:
- XGBoost evaluation

M4:
- real integration

M5:
- investigation graph

M6:
- test cases

## Hours 14–18 — FIRST FULL PIPELINE

Target:

```text
input
→ graph
→ features
→ XGBoost
→ IF
→ risk
→ dashboard
```

If this is not working by hour 18:

STOP adding major features.

Fix integration.

## Hours 18–24

M3:
- SHAP
- DBSCAN
- distribution-shift evaluation

M2:
- evidence subgraph/path

M4:
- better risk fusion

M5:
- timeline/filtering

M1:
- improve synthetic realism

M6:
- QA + demo

## Hours 24–30

- offline packaging
- performance
- error handling
- evidence graph
- real demo dataset

## Hours 30–34

- offline test
- final evaluation numbers
- fix crashes
- technical write-up

## Hours 34–36

- freeze code
- demo rehearsal
- backup repository
- backup Docker tar
- final presentation

---

# 30. WHAT NOT TO BUILD

Do not spend hackathon time on:

```text
login
user accounts
cloud deployment
mobile app
LLM chatbot
real-time blockchain API
complex authentication
microservices
Kubernetes
GNN
massive distributed data platform
```

The goal is an excellent offline forensic prototype.

---

# 31. DEFINITION OF MVP

The MVP is complete when:

```text
1. Upload synthetic CSV/JSON.
2. Validate it.
3. Build graph.
4. Generate entity features.
5. Run XGBoost.
6. Run Isolation Forest.
7. Generate DBSCAN clusters.
8. Calculate risk.
9. Produce ranked alerts.
10. Explain an alert.
11. Show graph.
12. Run with internet disabled.
```

Everything else is optional.

---

# 32. COMMON FAILURE MODES

## Failure 1 — Model sees labels accidentally

Result:

fake performance.

Fix:

explicit feature allowlist.

## Failure 2 — Test set resembles training too closely

Result:

inflated performance.

Fix:

new seeds + new parameter ranges + new scenario mixes.

## Failure 3 — Graph is visually impressive but semantically wrong

Result:

bad evidence.

Fix:

hand-check small graphs before large graphs.

## Failure 4 — Risk score is arbitrary

Result:

judge asks "why 40%?"

Fix:

start with configurable weights and evaluate them.

## Failure 5 — PyVis works online but not offline

Result:

blank graph.

Fix:

local assets + Wi-Fi-off test.

## Failure 6 — System only works with prepared CSV

Result:

bad demo.

Fix:

test schema errors and malformed inputs.

## Failure 7 — People spend the whole time learning theory

Result:

no working product.

Fix:

learn exactly what the next implementation task requires.

---

# 33. HOW EACH MEMBER SHOULD USE AN AI

## M1

> "I am M1. Explain pandas groupby to me using our wallet feature-generation problem, then give me a 10-minute exercise before I implement it."

or:

> "I am M1. Implement `gen_fan_out()` against the schema in this context file. Explain every line."

## M2

> "I am M2. Teach me Union-Find from zero, then implement CIO using our blockchain_df schema."

## M3

> "I am M3. Teach me XGBoost from zero using our features_df. Do not introduce neural networks."

> "I am M3. Here is my F1/PR-AUC output. Help me interpret whether my model is actually useful."

## M4

> "I am M4. Here are the actual outputs from M2 and M3. Help me combine them without changing the module contracts."

## M5

> "I am M5. Build the Streamlit alert page around the exact `alerts` schema in this context."

## M6

> "I am M6. Pretend you are a skeptical SIH judge and ask me questions about this system one at a time."

---

# 34. IF A MEMBER IS STUCK

The AI should not immediately dump a complete replacement project.

Use this order:

1. Ask what they expected.
2. Ask what happened instead.
3. Inspect the exact error/output.
4. Explain the underlying concept.
5. Give the smallest fix.
6. Explain why it fixes the problem.
7. Tell them how to test the fix.
8. Only then consider refactoring.

---

# 35. CURRENT PROJECT STATUS TEMPLATE

Update this section in the real repository as work progresses.

```text
M1 DATA
[ ] schema confirmed
[ ] loader
[ ] validation
[ ] normal generator
[ ] burst generator
[ ] fan-out generator
[ ] fan-in generator
[ ] chain generator
[ ] network layer
[ ] train/val/test generator modes

M2 GRAPH
[ ] CIO
[ ] graph builder
[ ] graph features
[ ] temporal features
[ ] network features
[ ] performance sanity check

M3 ML
[ ] preprocessing
[ ] XGBoost baseline
[ ] temporal/distribution-shift evaluation
[ ] tuning
[ ] SHAP
[ ] Isolation Forest
[ ] DBSCAN
[ ] final ml_output_df

M4 INTEGRATION
[ ] pipeline
[ ] risk fusion
[ ] explanations
[ ] ranked alerts
[ ] offline package
[ ] offline test

M5 DASHBOARD
[ ] overview
[ ] alerts
[ ] investigation
[ ] graph
[ ] timeline
[ ] filters
[ ] offline test

M6
[ ] test matrix
[ ] technical write-up
[ ] Q&A
[ ] demo script
[ ] final rehearsal
```

---

# 36. FINAL PROJECT PHILOSOPHY

This project is not trying to prove that an algorithm can magically "find criminals."

It is trying to demonstrate a complete investigative workflow:

```text
messy data
   ↓
correlation
   ↓
entity graph
   ↓
behavioral features
   ↓
machine learning
   ↓
independent anomaly signal
   ↓
graph context
   ↓
explanation
   ↓
ranked investigative leads
```

The strongest version of this project is one where:

- M1 can explain the data,
- M2 can explain the graph,
- M3 can explain the ML,
- M4 can explain the risk fusion and offline packaging,
- M5 can demonstrate the product,
- M6 can explain and defend the entire system.

The team should understand the system well enough that an AI is a **mentor and coding assistant**, not the person who secretly understands the project better than the team.

---

# 37. AUTHORITATIVE DECISIONS — QUICK REFERENCE

```text
PS
SIH26146

CLIENT
NTRO

TEAM
5 technical + 1 QA/docs/demo

PRIMARY ML
XGBoost

SECONDARY ML
Isolation Forest

CLUSTERING
DBSCAN/HDBSCAN

GRAPH
NetworkX

ENTITY RESOLUTION
CIO + conservative heuristics

XAI
SHAP TreeExplainer for XGBoost

DASHBOARD
Streamlit

GRAPH VISUALIZATION
PyVis with local assets

STORAGE
Parquet / local files

DEPLOYMENT
Offline Linux
Python wheelhouse + Docker backup

NO:
LLM APIs
cloud inference
live APIs
CDN
GNN in critical path

CORE PRINCIPLE
Anomaly ≠ criminality

GROUND TRUTH
Used for supervised training/evaluation of synthetic scenarios
but never as an input feature.

EVALUATION
Temporal / distribution-shift testing, not just random split.

FINAL OUTPUT
Ranked, explainable investigative alerts.
```

---

# 38. VERSIONING RULE FOR THIS CONTEXT FILE

If the team intentionally changes an architecture decision, update this file immediately.

For example:

```text
OLD:
Isolation Forest primary

NEW:
XGBoost primary
Isolation Forest secondary
```

The new decision should be recorded here so every AI session gets the same project context.

Do not allow one member's AI chat to silently redesign the architecture while the rest of the team follows another design.

---

# END OF CONTEXT
