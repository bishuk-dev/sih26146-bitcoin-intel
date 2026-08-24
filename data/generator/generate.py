"""
Synthetic dataset generator.

THIS FILE IS WHERE THE PATH A vs PATH B DECISION (see root README) GETS MADE.

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

If you go Path A (supervised): tag injected-anomalous wallets with a
ground-truth label column and keep it OUT of the feature set used for
training — use it only for evaluation (precision/recall/F1 against your
own injected ground truth).

If you go Path B (unsupervised): still inject the scenarios above so you
have something to validate the anomaly detector against, but never feed
the label into the model.
"""


def generate_dataset(n_wallets: int, n_transactions: int, anomaly_rate: float = 0.02,
                      labeled: bool = True):
    """Generate synthetic blockchain + network layer data with injected patterns.

    Returns two DataFrames (blockchain_df, network_df). If labeled=True,
    blockchain_df includes a `ground_truth_anomalous` column for evaluation only.
    """
    raise NotImplementedError
