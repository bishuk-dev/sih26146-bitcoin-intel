import networkx as nx


def calculate_graph_features(graph):

    features = {}

    wallet_nodes = [
        node
        for node, data in graph.nodes(data=True)
        if data.get("node_type") == "wallet"
    ]

    for wallet in wallet_nodes:

        outgoing = 0.0
        incoming = 0.0
        tx_count = 0

        for _, _, data in graph.out_edges(
            wallet,
            data=True
        ):

            if data.get("edge_type") == "transaction":

                outgoing += float(
                    data.get("amount", 0)
                )

                tx_count += 1

        for _, _, data in graph.in_edges(
            wallet,
            data=True
        ):

            if data.get("edge_type") == "transaction":

                incoming += float(
                    data.get("amount", 0)
                )

        degree = graph.degree(wallet)

        features[wallet] = {
            "wallet": graph.nodes[wallet]["wallet_id"],
            "outgoing_volume": outgoing,
            "incoming_volume": incoming,
            "transaction_count": tx_count,
            "degree": degree,
            "net_flow": incoming - outgoing
        }

    return features