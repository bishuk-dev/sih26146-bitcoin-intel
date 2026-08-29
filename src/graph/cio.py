class UnionFind:

    def __init__(self):
        self.parent = {}
        self.rank = {}

    def add(self, node):

        if node not in self.parent:
            self.parent[node] = node
            self.rank[node] = 0

    def find(self, node):

        self.add(node)

        if self.parent[node] != node:
            self.parent[node] = self.find(
                self.parent[node]
            )

        return self.parent[node]

    def union(self, a, b):

        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return

        if self.rank[root_a] < self.rank[root_b]:
            self.parent[root_a] = root_b

        elif self.rank[root_a] > self.rank[root_b]:
            self.parent[root_b] = root_a

        else:
            self.parent[root_b] = root_a
            self.rank[root_a] += 1


def build_cio(blockchain_df):

    uf = UnionFind()

    evidence = []

    for _, row in blockchain_df.iterrows():

        sender = str(row["sender"])
        receiver = str(row["receiver"])

        uf.add(sender)
        uf.add(receiver)

        # Conservative ownership heuristic:
        # wallets appearing together in the same
        # ownership/evidence group can be linked.

        uf.union(sender, receiver)

        evidence.append({
            "wallet_a": sender,
            "wallet_b": receiver,
            "evidence": "transaction_co_occurrence",
            "confidence": 0.50
        })

    groups = {}

    for wallet in uf.parent:

        root = uf.find(wallet)

        groups.setdefault(root, []).append(wallet)

    return groups, evidence