"""
ML core module: anomaly detection + entity clustering + explainability.

DECIDED APPROACH (see root README for rationale):
  - Primary detector: Isolation Forest, UNSUPERVISED. `ground_truth_anomalous`
    from data/generator is NEVER passed into train_anomaly_detector — it is
    read only by evaluate_against_ground_truth(), after the fact.
  - Entity clustering: DBSCAN/HDBSCAN, runs alongside (not instead of) the
    anomaly detector — clustering answers "who's related", anomaly score
    answers "who's weird". Both feed src/scoring separately.
  - Optional bonus layer (only if time permits, after the above works
    end-to-end): a Random Forest trained on the held-out labels, added as
    an extra signal into src/scoring — must be clearly framed to judges as
    a secondary ensemble input, not the core detection method.

explain_predictions() must return SHAP values per entity so src/scoring can
build a human-readable "why flagged" string.
"""

import pandas as pd


def train_anomaly_detector(features: pd.DataFrame):
    """Train Isolation Forest. Do NOT pass ground_truth_anomalous in here."""
    raise NotImplementedError


def cluster_entities(features: pd.DataFrame):
    """DBSCAN/HDBSCAN clustering over behavioural + graph features."""
    raise NotImplementedError


def evaluate_against_ground_truth(predictions: pd.DataFrame,
                                   ground_truth: pd.Series) -> dict:
    """Eval-only. Compute precision/recall/F1 of predictions against the
    generator's injected ground_truth_anomalous column. Never used in training.
    """
    raise NotImplementedError


def explain_predictions(model, features: pd.DataFrame) -> pd.DataFrame:
    """Return SHAP-based top contributing factors per entity, human-readable."""
    raise NotImplementedError


def train_bonus_random_forest(features: pd.DataFrame, labels: pd.Series):
    """OPTIONAL bonus layer — only build this after the unsupervised pipeline
    works end-to-end and you have spare time. Frame as secondary signal only.
    """
    raise NotImplementedError
