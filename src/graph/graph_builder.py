import networkx as nx
import csv


def create_graph(csv_file):

    graph = nx.MultiDiGraph()

    with open(csv_file, "r", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            sender = row["sender"]
            receiver = row["receiver"]

            graph.add_node(sender, type="wallet")
            graph.add_node(receiver, type="wallet")

            graph.add_edge(
                sender,
                receiver,
                type="transaction",
                amount=float(row["amount"]),
                transaction_id=row["transaction_id"],
                timestamp=row["timestamp"]
            )

    return graph