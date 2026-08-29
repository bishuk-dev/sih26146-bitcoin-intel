from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

BLOCKCHAIN_PATH = PROJECT_ROOT / "data" / "raw" / "blockchain.parquet"
NETWORK_PATH = PROJECT_ROOT / "data" / "raw" / "network.parquet"


def load_parquet_data():

    if not BLOCKCHAIN_PATH.exists():
        raise FileNotFoundError(
            f"Missing blockchain parquet: {BLOCKCHAIN_PATH}"
        )

    if not NETWORK_PATH.exists():
        raise FileNotFoundError(
            f"Missing network parquet: {NETWORK_PATH}"
        )

    blockchain_df = pd.read_parquet(
        BLOCKCHAIN_PATH,
        engine="pyarrow"
    )

    network_df = pd.read_parquet(
        NETWORK_PATH,
        engine="pyarrow"
    )

    return blockchain_df, network_df


def validate_columns(blockchain_df, network_df):

    required_blockchain = {
        "tx_id",
        "sender",
        "receiver",
        "amount",
        "timestamp"
    }

    required_network = {
        "wallet"
    }

    missing_blockchain = (
        required_blockchain
        - set(blockchain_df.columns)
    )

    missing_network = (
        required_network
        - set(network_df.columns)
    )

    if missing_blockchain:
        raise ValueError(
            f"Blockchain data missing columns: "
            f"{sorted(missing_blockchain)}"
        )

    if missing_network:
        raise ValueError(
            f"Network data missing columns: "
            f"{sorted(missing_network)}"
        )

    return True