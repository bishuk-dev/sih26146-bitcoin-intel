def analyze_graph(graph):

    sent = {}
    received = {}
    transaction_count = {}

    for source, target, data in graph.edges(data=True):

        amount = data["amount"]

        sent[source] = sent.get(source, 0) + amount
        received[target] = received.get(target, 0) + amount
        transaction_count[source] = transaction_count.get(source, 0) + 1

    return sent, received, transaction_count


def calculate_risk(graph, sent, transaction_count):

    risk = {}

    for wallet in graph.nodes():

        score = 0

        total_sent = sent.get(wallet, 0)
        count = transaction_count.get(wallet, 0)

        if total_sent >= 10000:
            score += 50

        if count >= 2:
            score += 20

        if score >= 50:
            level = "HIGH"
        elif score >= 20:
            level = "MEDIUM"
        else:
            level = "LOW"

        risk[wallet] = {
            "score": score,
            "level": level
        }

    return risk