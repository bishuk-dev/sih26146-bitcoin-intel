def find_high_value_transactions(graph, threshold=10000):

    suspicious = []

    for source, target, data in graph.edges(data=True):

        if data["amount"] >= threshold:

            suspicious.append({
                "transaction_id": data["transaction_id"],
                "sender": source,
                "receiver": target,
                "amount": data["amount"],
                "timestamp": data["timestamp"]
            })

    return suspicious