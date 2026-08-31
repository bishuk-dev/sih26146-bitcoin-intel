import networkx as nx


def calculate_network_features(graph):

    features = {}

    wallet_nodes = [
        node
        for node, data in graph.nodes(data=True)
        if data.get("node_type") == "wallet"
    ]

    for wallet in wallet_nodes:

        features[wallet] = {
            "pagerank": 0.0,
            "betweenness": 0.0,
            "clustering": 0.0
        }

    if not wallet_nodes:
        return features

    pagerank = nx.pagerank(
        graph,
        weight=None
    )

    betweenness = nx.betweenness_centrality(
        graph
    )

    undirected = graph.to_undirected()

    clustering = nx.clustering(
        undirected
    )

    for wallet in wallet_nodes:

        features[wallet][
            "pagerank"
        ] = pagerank.get(wallet, 0.0)

        features[wallet][
            "betweenness"
        ] = betweenness.get(wallet, 0.0)

        features[wallet][
            "clustering"
        ] = clustering.get(wallet, 0.0)

    return features