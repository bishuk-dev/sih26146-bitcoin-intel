# SIH26146 — Offline Bitcoin Transaction Intelligence Platform

**Problem Statement:** AI-Powered Monitoring & Analysis of Bitcoin Transaction Traffic
**Organization:** NTRO
**One-liner:** An offline, explainable graph-intelligence platform that correlates
Bitcoin transaction behaviour with network metadata to surface anomalous entities
and rank investigative leads.

## Hard constraints (read before writing any code)

- **Must run fully offline.** No cloud APIs, no CDN-hosted JS, no runtime `pip install`.
  The evaluation machine will have zero inbound/outbound internet.
- **Working ML model required, not just rules.** `if amount > X: suspicious = True`
  does not satisfy the PS.
- **Output must be a ranked, explainable alert list** — a risk score alone is not enough;
  every flag needs a human-readable "why."

## ML approach — decided

**Primary detection: Isolation Forest (unsupervised) + DBSCAN/HDBSCAN (entity clustering).**
Random Forest is an optional bonus layer only, not the primary path.

Why: the real Elliptic dataset this problem is benchmarked against is only ~23%
labeled (77% unknown) — label scarcity is the realistic condition here, not an
edge case. More importantly, since we generate our own synthetic dataset, training
a supervised model on self-injected labels risks just re-learning our own
generator's rules, which is a fair thing for judges to call out. Isolation Forest
is the standard tool for exactly this "no reliable ground truth" class of problem.

**Ground-truth labels still get generated in `data/generator/` — for evaluation
only, never fed into training.** This is what lets us report real precision/recall/F1
numbers ("detected X% of injected anomalous wallets at Y% precision") without the
circular-reasoning problem of training and testing on the same self-authored rules.

If time permits after the primary pipeline works end-to-end, a Random Forest trained
on the held-out labels can be added as a secondary signal into `src/scoring` — framed
explicitly as a bonus ensemble layer, not the core detection method.

## Architecture

```
Raw data (CSV/JSON: blockchain + network metadata)
        │
        ▼
[ src/ingestion ]   parsing, schema validation, cleaning
        │
        ▼
[ src/graph ]       NetworkX graph build, CIO heuristic clustering,
        │           graph features (degree, PageRank, centrality)
        ▼
[ src/ml ]          anomaly detection / classification + entity clustering
        │           + SHAP explainability
        ▼
[ src/scoring ]     risk fusion (anomaly + graph + network + cluster signals)
        │           → 0-100 ranked, explainable alert list
        ▼
[ dashboard ]       Streamlit + Pyvis, fully local assets, offline-rendering
```

## Module contracts (fill in as each module lands)

- `src/ingestion` — input: raw CSV/JSON → output: validated pandas DataFrame(s)
- `src/graph` — input: DataFrame(s) → output: NetworkX graph + engineered feature table
- `src/ml` — input: feature table → output: per-entity anomaly score + cluster ID + SHAP values
- `src/scoring` — input: ml output + graph/network signals → output: ranked alert list (JSON)
- `dashboard` — input: alert list JSON + graph → output: local Streamlit UI

## Tech stack

Python, pandas, NetworkX, scikit-learn, SHAP, Streamlit, Pyvis, Docker.
See `requirements.txt` — all dependencies must be vendored as local wheels before
the offline freeze (see `docker/build_offline.sh`).

## Getting started

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Offline testing (mandatory before submission)

Run `scripts/test_offline.sh` with Wi-Fi physically disabled at least once before
the deadline — this is the single most common way teams lose points on this PS.

## Team / role assignments

See `docs/role_assignments.md`.
