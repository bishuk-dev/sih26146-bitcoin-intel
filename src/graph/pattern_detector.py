def find_transaction_chains(graph):

    chains = []

    for start in graph.nodes():

        for middle in graph.successors(start):

            for end in graph.successors(middle):

                if start != end:

                    chains.append({
                        "path": [
                            start,
                            middle,
                            end
                        ],
                        "length": 3
                    })

    return chains


def calculate_chain_risk(graph, chains):

    results = []

    for chain in chains:

        path = chain["path"]

        score = 0

        # Check every transaction in the chain
        for i in range(len(path) - 1):

            source = path[i]
            target = path[i + 1]

            # Get all transactions between source and target
            edge_data = graph.get_edge_data(
                source,
                target
            )

            if edge_data:

                for key, data in edge_data.items():

                    if data["amount"] >= 10000:
                        score += 30

        # A 3-wallet chain gets an additional score
        if chain["length"] >= 3:
            score += 20

        if score >= 50:
            level = "HIGH"
        elif score >= 20:
            level = "MEDIUM"
        else:
            level = "LOW"

        results.append({
            "path": path,
            "length": chain["length"],
            "score": score,
            "risk": level
        })

    return results