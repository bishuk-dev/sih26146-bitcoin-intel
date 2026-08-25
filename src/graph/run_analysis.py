from graph_builder import create_graph
from analyzer import analyze_graph, calculate_risk
from risk_detector import find_high_value_transactions
from pattern_detector import (
    find_transaction_chains,
    calculate_chain_risk
)
from report_generator import generate_report, save_report


# Create graph from CSV
graph = create_graph("data/generator/transactions.csv")


# Analyze wallets
sent, received, transaction_count = analyze_graph(graph)

risk = calculate_risk(
    graph,
    sent,
    transaction_count
)


# -----------------------------
# Wallet analysis
# -----------------------------

print("========== WALLET ANALYSIS ==========")

for wallet in graph.nodes():

    print(
        wallet,
        "| Sent:", sent.get(wallet, 0),
        "| Received:", received.get(wallet, 0),
        "| Transactions:", transaction_count.get(wallet, 0),
        "| Risk:", risk[wallet]["level"],
        "| Score:", risk[wallet]["score"]
    )


# -----------------------------
# High-value transactions
# -----------------------------

print("\n========== HIGH VALUE TRANSACTIONS ==========")

suspicious = find_high_value_transactions(graph)

for transaction in suspicious:

    print(
        transaction["transaction_id"],
        "|",
        transaction["sender"],
        "->",
        transaction["receiver"],
        "| Amount:", transaction["amount"]
    )


# -----------------------------
# Transaction chains
# -----------------------------

print("\n========== TRANSACTION CHAINS ==========")

chains = find_transaction_chains(graph)

chain_results = calculate_chain_risk(
    graph,
    chains
)
report = generate_report(
    graph,
    sent,
    received,
    transaction_count,
    risk,
    chain_results
)

save_report(report)

print("\nAnalysis report saved successfully.")

for chain in chain_results:

    print(
        "Path:",
        " -> ".join(chain["path"]),
        "| Length:", chain["length"],
        "| Risk:", chain["risk"],
        "| Score:", chain["score"]
    )