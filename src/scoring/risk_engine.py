"""
Risk fusion + explainable alert generation module.

Owns: combining signals from src/ml (anomaly/cluster scores + SHAP) and
src/graph (graph-centrality-based risk) plus network correlation (IP
reuse, ASN grouping, GeoIP) into one 0-100 risk score per entity, and
turning that into the ranked, explainable alert list the PS requires.

Do NOT hardcode the fusion weights as "proven" — tune/validate them
against your synthetic ground truth and say so in the writeup, e.g.
"weights were tuned against injected scenario recall, not asserted."

Output contract: a JSON-serializable list of alerts, e.g.:
    {
      "entity_id": "...",
      "risk_score": 87,
      "reasons": ["High IP-reuse (+40%)", "Fan-out to 3 flagged clusters (+30%)"],
      "cluster_id": 17
    }
This is what dashboard/app.py renders directly — keep the shape stable.
"""

import pandas as pd


def compute_risk_scores(ml_output: pd.DataFrame, graph_features: pd.DataFrame,
                         network_signals: pd.DataFrame) -> pd.DataFrame:
    """Fuse anomaly/cluster/graph/network signals into a single 0-100 score."""
    raise NotImplementedError


def build_alert_list(risk_scores: pd.DataFrame, explanations: pd.DataFrame) -> list[dict]:
    """Produce the final ranked, explainable alert list for the dashboard."""
    raise NotImplementedError
