import pandas as pd


def calculate_temporal_features(blockchain_df):

    df = blockchain_df.copy()

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["timestamp"]
    )

    features = {}

    for wallet in set(
        df["sender"].astype(str)
    ):

        wallet_df = df[
            df["sender"].astype(str) == wallet
        ].sort_values("timestamp")

        if len(wallet_df) < 2:

            features[wallet] = {
                "burst_count": 0,
                "avg_time_between_transactions": None
            }

            continue

        deltas = (
            wallet_df["timestamp"]
            .diff()
            .dt.total_seconds()
            .dropna()
        )

        features[wallet] = {
            "burst_count": int(
                (deltas <= 300).sum()
            ),
            "avg_time_between_transactions": float(
                deltas.mean()
            )
        }

    return features