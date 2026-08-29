import networkx as nx


def build_graph(blockchain_df, network_df, cio_groups):

    graph = nx.MultiDiGraph()

    # -------------------------
    # Wallet nodes
    # -------------------------

    wallets = set()

    wallets.update(
        blockchain_df["sender"].astype(str)
    )

    wallets.update(
        blockchain_df["receiver"].astype(str)
    )

    if "wallet" in network_df.columns:

        wallets.update(
            network_df["wallet"].astype(str)
        )

    for wallet in wallets:

        graph.add_node(
            f"wallet:{wallet}",
            node_type="wallet",
            wallet_id=wallet
        )

    # -------------------------
    # Transaction edges
    # -------------------------

    for _, row in blockchain_df.iterrows():

        sender = str(row["sender"])
        receiver = str(row["receiver"])

        graph.add_edge(
            f"wallet:{sender}",
            f"wallet:{receiver}",
            edge_type="transaction",
            tx_id=str(row["tx_id"]),
            amount=float(row["amount"]),
            timestamp=str(row["timestamp"])
        )

    # -------------------------
    # CIO entity nodes
    # -------------------------

    for index, (root, members) in enumerate(
        cio_groups.items()
    ):

        entity_id = f"entity:{index}"

        graph.add_node(
            entity_id,
            node_type="entity",
            entity_id=entity_id
        )

        for wallet in members:

            wallet_node = f"wallet:{wallet}"

            if wallet_node in graph:

                graph.add_edge(
                    wallet_node,
                    entity_id,
                    edge_type="cio",
                    confidence=0.50
                )

                graph.add_edge(
                    entity_id,
                    wallet_node,
                    edge_type="cio",
                    confidence=0.50
                )

    # -------------------------
    # Network metadata
    # -------------------------

    for _, row in network_df.iterrows():

        wallet = str(row["wallet"])
        wallet_node = f"wallet:{wallet}"

        if wallet_node not in graph:
            continue

        for column in network_df.columns:

            if column == "wallet":
                continue

            graph.nodes[wallet_node][column] = row[column]

    return graph