"""
Graph construction module.

Owns: entity resolution + graph building + graph-level feature engineering.
This is the module both reports agree is the heart of the project.

Steps:
  1. Common Input Ownership (CIO) heuristic — cluster addresses that
     co-appear as inputs to the same transaction into a single entity.
     This collapses the graph and is a prerequisite for everything else.
  2. Build a heterogeneous NetworkX graph:
       nodes: Wallet, IP_Address (+ optionally ASN, Country)
       edges: Transacts_With (wallet-wallet), Operates_From (wallet-IP)
  3. Extract per-node graph features: degree, in/out-degree, PageRank,
     clustering coefficient, betweenness centrality, k-core.

Output contract: a feature table (one row per wallet/entity) that
src/ml consumes directly — do not leak raw graph objects downstream,
only the engineered feature columns plus a reference id.
"""

import networkx as nx
import pandas as pd


def apply_cio_heuristic(transactions: pd.DataFrame) -> pd.DataFrame:
    """Cluster co-spent input addresses into single entities."""
    raise NotImplementedError


def build_graph(transactions: pd.DataFrame, network: pd.DataFrame) -> nx.Graph:
    """Build the heterogeneous wallet/IP graph from cleaned inputs."""
    raise NotImplementedError


def extract_graph_features(graph: nx.Graph) -> pd.DataFrame:
    """Compute degree, PageRank, centrality, clustering coefficient per node."""
    raise NotImplementedError
