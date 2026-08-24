"""
Synthetic dataset generator.

Plan:
  1. Use a public topology (e.g. Elliptic dataset structure) for realistic
     transaction graph shape.
  2. Use Faker to synthesize IP/port/ASN fields per wallet/transaction.
  3. Inject behavioural patterns for known scenario types so you have
     something to evaluate against later:
       - NORMAL       baseline wallet activity
       - BURST        sudden transaction spike
       - FAN_OUT      one wallet -> many
       - FAN_IN       many wallets -> one
       - CHAIN        rapid A -> B -> C -> D movement
       - MIXED        combination of the above

IMPORTANT: this generator ALWAYS injects a `ground_truth_anomalous` label
column (we know which wallets we made suspicious, since we wrote the
injection code). But that column is EVAL-ONLY — see src/ml/detect.py.
It must never be joined into the feature table that trains the model.
Its only job is to let src/ml compute precision/recall/F1 after the fact.
"""


def generate_dataset(n_wallets: int, n_transactions: int, anomaly_rate: float = 0.02):
    """Generate synthetic blockchain + network layer data with injected patterns.

    Returns two DataFrames (blockchain_df, network_df). blockchain_df always
    includes `ground_truth_anomalous` (eval-only, see module docstring) and
    `scenario_type` (NORMAL/BURST/FAN_OUT/FAN_IN/CHAIN/MIXED) for debugging.
    """
    raise NotImplementedError
