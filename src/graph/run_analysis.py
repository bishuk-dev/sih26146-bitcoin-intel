from graph_builder import create_graph
from analyzer import analyze_graph


graph = create_graph("data/generator/transactions.csv")

sent, received = analyze_graph(graph)


print("Wallet Analysis")
print("================")

for wallet in graph.nodes():

    print(
        wallet,
        "| Sent:", sent.get(wallet, 0),
        "| Received:", received.get(wallet, 0)
    )