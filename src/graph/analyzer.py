def analyze_graph(graph):

    sent = {}
    received = {}

    for source, target, data in graph.edges(data=True):

        amount = data["amount"]

        sent[source] = sent.get(source, 0) + amount
        received[target] = received.get(target, 0) + amount

    return sent, received