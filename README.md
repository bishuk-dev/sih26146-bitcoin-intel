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

## Open decision — resolve before ML work starts

The two research passes that informed this repo disagree on the ML approach:

| | Assumes | Model |
|---|---|---|
| Path A | Labeled synthetic data (you inject ground-truth labels during generation) | Random Forest (supervised) — matches Weber et al. 2019 benchmark on the Elliptic dataset |
| Path B | No reliable labels | Isolation Forest / DBSCAN-HDBSCAN (unsupervised anomaly detection + clustering) |

**Decide this in `data/generator/` first** — if you inject labeled anomalous wallets
into the synthetic generator, go Path A. If you want the system to discover anomalies
without ever seeing a label, go Path B. This choice determines the entire contract
of `src/ml/`, so lock it before other modules build against it.

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
