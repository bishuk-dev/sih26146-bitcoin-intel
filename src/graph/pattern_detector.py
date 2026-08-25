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

        # Check transactions along the chain
        for i in range(len(path) - 1):

            source = path[i]
            target = path[i + 1]

            for _, _, data in graph.edges(
                source,
                target,
                data=True
            ):

                if data["amount"] >= 10000:
                    score += 30

        # Longer chain = additional risk
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