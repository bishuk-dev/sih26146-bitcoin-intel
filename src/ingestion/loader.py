"""
Ingestion module.

Owns: parsing raw CSV/JSON (blockchain layer + network layer), schema
validation, cleaning. Nothing downstream should ever see a malformed row.

Expected minimum fields (confirm exact names against the official PS PDF —
the field list in our working notes was truncated):

Blockchain layer:
    timestamp, txid, input_wallet, output_wallet, amount, fee, script_type

Network layer:
    src_ip, dst_ip, src_port, dst_port, timestamp, (geo/ASN if provided,
    else resolved downstream via GeoIP in src/scoring)

Output contract: a validated pandas DataFrame per layer, ready for
src/graph to consume. Do not do feature engineering here — that belongs
in src/graph.
"""

import pandas as pd


def load_blockchain_layer(path: str) -> pd.DataFrame:
    """Load and validate the blockchain-layer CSV/JSON."""
    raise NotImplementedError


def load_network_layer(path: str) -> pd.DataFrame:
    """Load and validate the network-layer CSV/JSON."""
    raise NotImplementedError


def validate_schema(df: pd.DataFrame, required_columns: list[str]) -> pd.DataFrame:
    """Raise a clear error if required columns are missing; drop malformed rows."""
    raise NotImplementedError
