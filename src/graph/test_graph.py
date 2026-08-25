import networkx as nx

graph = nx.MultiDiGraph()

# Wallets
graph.add_node("W1", type="wallet")
graph.add_node("W2", type="wallet")

# Transaction 1
graph.add_edge(
    "W1",
    "W2",
    type="transaction",
    amount=5000,
    transaction_id="TX001",
    timestamp="2026-08-25"
)

# Transaction 2
graph.add_edge(
    "W2",
    "W1",
    type="transaction",
    amount=2500,
    transaction_id="TX002",
    timestamp="2026-08-25"
)

# Transaction 3
graph.add_edge(
    "W1",
    "W2",
    type="transaction",
    amount=7500,
    transaction_id="TX003",
    timestamp="2026-08-25"
)

print("Nodes:")
print(graph.nodes(data=True))

print("\nEdges:")
print(graph.edges(data=True))
total = 0

for source, target, data in graph.edges(data=True):
    total += data["amount"]

print("\nTotal transaction amount:", total)
sent = {}

for source, target, data in graph.edges(data=True):
    sent[source] = sent.get(source, 0) + data["amount"]

print("\nMoney sent by each wallet:")

for wallet, amount in sent.items():
    print(wallet, "sent:", amount)
    top_wallet = max(sent, key=sent.get)

print("\nMost active wallet:")
print(top_wallet, "with total sent:", sent[top_wallet])
threshold = 6000

print("\nHigh-value transactions:")

for source, target, data in graph.edges(data=True):
    if data["amount"] >= threshold:
        print(
            data["transaction_id"],
            "from", source,
            "to", target,
            "amount:", data["amount"]
        )
        # -----------------------------
# Money received by each wallet
# -----------------------------

received = {}

for source, target, data in graph.edges(data=True):
    received[target] = received.get(target, 0) + data["amount"]

print("\nMoney received by each wallet:")

for wallet, amount in received.items():
    print(wallet, "received:", amount)


# -----------------------------
# Net money flow
# -----------------------------

print("\nNet money flow:")

wallets = set(graph.nodes())

for wallet in wallets:
    money_sent = sent.get(wallet, 0)
    money_received = received.get(wallet, 0)

    net = money_received - money_sent

    print(
        wallet,
        "sent:", money_sent,
        "received:", money_received,
        "net:", net
    )


# -----------------------------
# Suspicious wallet test
# -----------------------------

print("\nWallets with high outgoing transactions:")

for wallet, amount in sent.items():
    if amount >= 10000:
        print(
            wallet,
            "is flagged for review. Total sent:",
            amount
        )
        # -----------------------------
# Transaction count
# -----------------------------

# -----------------------------
# Transaction count
# -----------------------------

transaction_count = {}

for source, target, data in graph.edges(data=True):
    transaction_count[source] = transaction_count.get(source, 0) + 1

print("\nTransaction count per wallet:")

for wallet, count in transaction_count.items():
    print(wallet, "transactions:", count)


# -----------------------------
# Average transaction value
# -----------------------------

print("\nAverage transaction value:")

for wallet, count in transaction_count.items():
    average = sent[wallet] / count
    print(wallet, "average:", average)


# -----------------------------
# Simple risk score
# -----------------------------

print("\nRisk score:")

for wallet in wallets:
    score = 0

    if sent.get(wallet, 0) >= 10000:
        score += 50

    if transaction_count.get(wallet, 0) >= 2:
        score += 20

    if score >= 50:
        level = "HIGH"
    elif score >= 20:
        level = "MEDIUM"
    else:
        level = "LOW"

    print(
        wallet,
        "score:", score,
        "risk:", level
    )
    # -----------------------------
# Direct wallet connections
# -----------------------------

print("\nWallet connections:")

for source, target in graph.edges():
    print(source, "->", target)
    # -----------------------------
# Unique connections
# -----------------------------

connections = {}

for source, target in graph.edges():
    connections.setdefault(source, set()).add(target)

print("\nUnique connections:")

for wallet, targets in connections.items():
    print(wallet, "connected to:", list(targets))
    # -----------------------------
# Connection count
# -----------------------------

print("\nConnection count:")

for wallet, targets in connections.items():
    print(wallet, "connections:", len(targets))
    # -----------------------------
# 3.20 - Incoming transaction count
# -----------------------------

incoming_count = {}

for source, target, data in graph.edges(data=True):
    incoming_count[target] = incoming_count.get(target, 0) + 1

print("\nIncoming transaction count:")

for wallet, count in incoming_count.items():
    print(wallet, "received", count, "transactions")


# -----------------------------
# 3.21 - Total transaction count
# -----------------------------

print("\nTotal transactions:", graph.number_of_edges())


# -----------------------------
# 3.22 - Wallet degree
# -----------------------------

print("\nWallet activity:")

for wallet in graph.nodes():
    outgoing = graph.out_degree(wallet)
    incoming = graph.in_degree(wallet)

    print(
        wallet,
        "outgoing:", outgoing,
        "incoming:", incoming
    )


# -----------------------------
# 3.23 - High activity wallet
# -----------------------------

print("\nHighly active wallets:")

for wallet in graph.nodes():
    activity = graph.out_degree(wallet) + graph.in_degree(wallet)

    if activity >= 3:
        print(
            wallet,
            "activity:", activity,
            "status: HIGH ACTIVITY"
        )


# -----------------------------
# 3.24 - Final wallet summary
# -----------------------------

print("\n========== WALLET SUMMARY ==========")

for wallet in graph.nodes():

    total_sent = sent.get(wallet, 0)
    total_received = received.get(wallet, 0)
    transactions = transaction_count.get(wallet, 0)
    risk_score = 0

    if total_sent >= 10000:
        risk_score += 50

    if transactions >= 2:
        risk_score += 20

    if risk_score >= 50:
        risk = "HIGH"
    elif risk_score >= 20:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    print(
        wallet,
        "| Sent:", total_sent,
        "| Received:", total_received,
        "| Transactions:", transactions,
        "| Risk:", risk
    )