from fastapi import FastAPI
from graph.graph_builder import create_graph
from graph.analyzer import analyze_graph, calculate_risk
from graph.risk_detector import find_high_value_transactions
from graph.pattern_detector import (
    find_transaction_chains,
    calculate_chain_risk
)


app = FastAPI(
    title="SIH26146 Bitcoin Intelligence API",
    version="1.0"
)


@app.get("/")
def home():

    return {
        "project": "SIH26146 Bitcoin Intelligence",
        "status": "running"
    }


@app.get("/analyze")
def analyze():

    graph = create_graph(
        "data/generator/transactions.csv"
    )

    sent, received, transaction_count = analyze_graph(
        graph
    )

    risk = calculate_risk(
        graph,
        sent,
        transaction_count
    )

    suspicious = find_high_value_transactions(
        graph
    )

    chains = find_transaction_chains(
        graph
    )

    chain_results = calculate_chain_risk(
        graph,
        chains
    )

    return {
        "wallets": [
            {
                "wallet": wallet,
                "sent": sent.get(wallet, 0),
                "received": received.get(wallet, 0),
                "transactions": transaction_count.get(wallet, 0),
                "risk": risk[wallet]
            }
            for wallet in graph.nodes()
        ],
        "high_value_transactions": suspicious,
        "transaction_chains": chain_results
    }