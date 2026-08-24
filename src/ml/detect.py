"""
ML core module: anomaly detection / classification + entity clustering + explainability.

Whoever owns this file must know which path (see root README) the team picked
BEFORE writing code here — the two paths have different function contracts.

Path A (supervised, if data/generator injected ground-truth labels):
    train_random_forest(features, labels) -> trained model
    Evaluate with F1 / accuracy against held-out ground truth.

Path B (unsupervised, no labels used in training):
    train_isolation_forest(features) -> trained model
    cluster_entities(features) -> cluster assignments (DBSCAN/HDBSCAN)
    Evaluate by checking how many of your OWN injected scenario-wallets
    (from data/generator) the model recovers as anomalous/clustered together.

Either path: explain_predictions() must return SHAP values per entity so
src/scoring can build a human-readable "why flagged" string. This function
signature should stay identical regardless of which path you pick, so the
scoring module doesn't care which one you chose.
"""

import pandas as pd


def train_model(features: pd.DataFrame, labels: pd.Series | None = None):
    """Train the anomaly/classification model. `labels` is None on Path B."""
    raise NotImplementedError


def cluster_entities(features: pd.DataFrame):
    """DBSCAN/HDBSCAN clustering over behavioural + graph features."""
    raise NotImplementedError


def explain_predictions(model, features: pd.DataFrame) -> pd.DataFrame:
    """Return SHAP-based top contributing factors per entity, human-readable."""
    raise NotImplementedError
