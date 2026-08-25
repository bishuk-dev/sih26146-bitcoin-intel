import networkx as nx


def create_graph():
    graph = nx.MultiDiGraph()

    graph.add_node("W1", type="wallet")
    graph.add_node("W2", type="wallet")

    graph.add_edge(
        "W1",
        "W2",
        type="transaction",
        amount=5000,
        transaction_id="TX001",
        timestamp="2026-08-25"
    )

    graph.add_edge(
        "W2",
        "W1",
        type="transaction",
        amount=2500,
        transaction_id="TX002",
        timestamp="2026-08-25"
    )

    graph.add_edge(
        "W1",
        "W2",
        type="transaction",
        amount=7500,
        transaction_id="TX003",
        timestamp="2026-08-25"
    )

    return graph