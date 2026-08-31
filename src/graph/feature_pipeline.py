from data_loader import (
    load_parquet_data,
    validate_columns
)

from cio import build_cio
from graph_builder import build_graph
from graph_features import calculate_graph_features
from temporal_features import calculate_temporal_features
from network_features import calculate_network_features


def run_feature_pipeline():

    blockchain_df, network_df = (
        load_parquet_data()
    )

    validate_columns(
        blockchain_df,
        network_df
    )

    cio_groups, cio_evidence = build_cio(
        blockchain_df
    )

    graph = build_graph(
        blockchain_df,
        network_df,
        cio_groups
    )

    graph_features = calculate_graph_features(
        graph
    )

    temporal_features = (
        calculate_temporal_features(
            blockchain_df
        )
    )

    network_features = (
        calculate_network_features(
            graph
        )
    )

    return {
        "graph": graph,
        "cio_groups": cio_groups,
        "cio_evidence": cio_evidence,
        "graph_features": graph_features,
        "temporal_features": temporal_features,
        "network_features": network_features
    }