import json


def generate_report(graph, sent, received, transaction_count, risk, chain_results):

    wallets = []

    for wallet in graph.nodes():

        wallets.append({
            "wallet": wallet,
            "sent": sent.get(wallet, 0),
            "received": received.get(wallet, 0),
            "transactions": transaction_count.get(wallet, 0),
            "risk": risk[wallet]["level"],
            "risk_score": risk[wallet]["score"]
        })

    report = {
        "total_wallets": graph.number_of_nodes(),
        "total_transactions": graph.number_of_edges(),
        "wallets": wallets,
        "chains": chain_results
    }

    return report


def save_report(report, filename="analysis_report.json"):

    with open(filename, "w") as file:

        json.dump(
            report,
            file,
            indent=4
        )