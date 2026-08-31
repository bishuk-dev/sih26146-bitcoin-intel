"""
M5: Offline Bitcoin Transaction Intelligence Dashboard.

Main views:

1. Overview
2. Ranked Alert List
3. Entity Investigation
"""

import streamlit as st
import networkx as nx

from graph import render_graph


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Bitcoin Transaction Intelligence",
    page_icon="🔎",
    layout="wide"
)


# ============================================================
# DEMO DATA
# ============================================================

DEMO_ALERTS = [
    {
        "entity_id": "W17",
        "risk_score": 91,
        "priority": "HIGH",
        "cluster_id": 4,
        "xgb_probability": 0.89,
        "anomaly_score": 0.93,
        "reasons": [
            "High fan-out behavior",
            "Unusually bursty transaction activity",
            "IP reused across multiple wallets"
        ]
    },
    {
        "entity_id": "W43",
        "risk_score": 87,
        "priority": "HIGH",
        "cluster_id": 7,
        "xgb_probability": 0.84,
        "anomaly_score": 0.91,
        "reasons": [
            "Very high transaction burst",
            "Large number of counterparties",
            "Unusual IP reuse"
        ]
    },
    {
        "entity_id": "W91",
        "risk_score": 74,
        "priority": "MEDIUM",
        "cluster_id": 2,
        "xgb_probability": 0.69,
        "anomaly_score": 0.79,
        "reasons": [
            "High IP reuse rate",
            "Unusual transaction frequency"
        ]
    },
    {
        "entity_id": "W22",
        "risk_score": 61,
        "priority": "MEDIUM",
        "cluster_id": 8,
        "xgb_probability": 0.57,
        "anomaly_score": 0.68,
        "reasons": [
            "High transaction count",
            "Large number of counterparties"
        ]
    },
    {
        "entity_id": "W56",
        "risk_score": 48,
        "priority": "LOW",
        "cluster_id": 3,
        "xgb_probability": 0.42,
        "anomaly_score": 0.51,
        "reasons": [
            "Moderately unusual transaction pattern"
        ]
    }
]


# ============================================================
# TEMPORARY DEMO GRAPH
# ============================================================

def create_demo_graph(entity_id):

    graph = nx.DiGraph()

    # Main entity
    graph.add_node(
        entity_id,
        label=entity_id,
        type="Wallet"
    )

    # Connected wallets
    graph.add_node(
        "WALLET_A",
        label="WALLET_A",
        type="Wallet"
    )

    graph.add_node(
        "WALLET_B",
        label="WALLET_B",
        type="Wallet"
    )

    graph.add_node(
        "WALLET_C",
        label="WALLET_C",
        type="Wallet"
    )

    # IP address
    graph.add_node(
        "IP_001",
        label="IP_001",
        type="IP"
    )

    # Relationships
    graph.add_edge(
        entity_id,
        "WALLET_A",
        label="Transaction"
    )

    graph.add_edge(
        entity_id,
        "WALLET_B",
        label="Transaction"
    )

    graph.add_edge(
        entity_id,
        "WALLET_C",
        label="Transaction"
    )

    graph.add_edge(
        entity_id,
        "IP_001",
        label="IP Reuse"
    )

    return graph


# ============================================================
# OVERVIEW
# ============================================================

def render_overview(stats):

    st.title(
        "Bitcoin Transaction Intelligence"
    )

    st.write(
        "Offline investigation dashboard for "
        "cryptocurrency transaction analysis."
    )

    st.divider()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Transactions",
            stats.get("transactions", 0)
        )

    with col2:
        st.metric(
            "Wallets / Entities",
            stats.get("wallets", 0)
        )

    with col3:
        st.metric(
            "IP Addresses",
            stats.get("ips", 0)
        )

    with col4:
        st.metric(
            "Alerts",
            stats.get("alerts", 0)
        )

    with col5:
        st.metric(
            "High Risk",
            stats.get("high_risk", 0)
        )

    st.divider()

    st.subheader("Pipeline Status")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.success("✓ Ingestion")

    with col2:
        st.success("✓ Graph")

    with col3:
        st.success("✓ ML")

    with col4:
        st.success("✓ Risk Scoring")

    st.divider()

    st.info(
        "Alerts represent investigative leads and anomalous "
        "patterns. They do not establish criminality or guilt."
    )


# ============================================================
# ALERT LIST
# ============================================================

def render_alert_list(alerts):

    st.title(
        "Ranked Investigative Alerts"
    )

    st.write(
        "Entities ranked by risk score for further investigation."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        priorities = st.multiselect(
            "Priority",
            ["HIGH", "MEDIUM", "LOW"],
            default=["HIGH", "MEDIUM", "LOW"]
        )

    with col2:

        minimum_risk = st.slider(
            "Minimum Risk Score",
            min_value=0,
            max_value=100,
            value=0
        )

    with col3:

        search_entity = st.text_input(
            "Search Entity",
            placeholder="Example: W17"
        )

    filtered_alerts = []

    for alert in alerts:

        if alert["priority"] not in priorities:
            continue

        if alert["risk_score"] < minimum_risk:
            continue

        if search_entity:

            if search_entity.lower() not in alert["entity_id"].lower():
                continue

        filtered_alerts.append(alert)

    filtered_alerts.sort(
        key=lambda alert: alert["risk_score"],
        reverse=True
    )

    if not filtered_alerts:

        st.warning(
            "No alerts match the selected filters."
        )

        return

    table_data = []

    for rank, alert in enumerate(
        filtered_alerts,
        start=1
    ):

        table_data.append(
            {
                "Rank": rank,
                "Entity": alert["entity_id"],
                "Risk": alert["risk_score"],
                "Priority": alert["priority"],
                "Cluster": alert["cluster_id"],
                "Main Reason": alert["reasons"][0]
            }
        )

    st.dataframe(
        table_data,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader(
        "Open Investigation"
    )

    entity_ids = [
        alert["entity_id"]
        for alert in filtered_alerts
    ]

    selected_entity = st.selectbox(
        "Select an entity",
        entity_ids
    )

    if st.button(
        "Investigate Selected Entity"
    ):

        st.session_state["selected_entity"] = selected_entity

        st.session_state["go_to_investigation"] = True

        st.rerun()


# ============================================================
# ENTITY INVESTIGATION
# ============================================================

def render_entity_detail(entity_id):

    st.title(
        f"Entity Investigation — {entity_id}"
    )

    # --------------------------------------------------------
    # Find selected alert
    # --------------------------------------------------------

    selected_alert = None

    for alert in DEMO_ALERTS:

        if alert["entity_id"] == entity_id:

            selected_alert = alert
            break

    if selected_alert is None:

        st.error(
            "No information available for this entity."
        )

        return

    # --------------------------------------------------------
    # Risk information
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Risk Score",
            f"{selected_alert['risk_score']}/100"
        )

    with col2:

        st.metric(
            "Priority",
            selected_alert["priority"]
        )

    with col3:

        st.metric(
            "XGBoost Probability",
            f"{selected_alert['xgb_probability']:.0%}"
        )

    with col4:

        st.metric(
            "Anomaly Score",
            f"{selected_alert['anomaly_score']:.0%}"
        )

    st.divider()

    # --------------------------------------------------------
    # Reasons
    # --------------------------------------------------------

    st.subheader(
        "Why Was This Entity Flagged?"
    )

    for reason in selected_alert["reasons"]:

        st.write(
            f"• {reason}"
        )

    st.divider()

    # --------------------------------------------------------
    # INVESTIGATION GRAPH
    # --------------------------------------------------------

    demo_graph = create_demo_graph(
        entity_id
    )

    render_graph(
        demo_graph
    )

    st.divider()

    # --------------------------------------------------------
    # Investigation note
    # --------------------------------------------------------

    st.info(
        "This dashboard presents anomalous behavior and "
        "supporting evidence as investigative leads. "
        "It does not establish criminality or guilt."
    )


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    stats = {
        "transactions": 24530,
        "wallets": 8921,
        "ips": 3421,
        "alerts": len(DEMO_ALERTS),
        "high_risk": sum(
            1
            for alert in DEMO_ALERTS
            if alert["priority"] == "HIGH"
        )
    }

    # --------------------------------------------------------
    # SIDEBAR
    # --------------------------------------------------------

    st.sidebar.title(
        "Investigation System"
    )

    st.sidebar.caption(
        "SIH26146 — Offline Prototype"
    )

    page = st.sidebar.radio(
        "Navigation",
        [
            "Overview",
            "Alerts",
            "Investigation"
        ],
        key="navigation_page"
    )

    # --------------------------------------------------------
    # HANDLE INVESTIGATION NAVIGATION
    # --------------------------------------------------------

    if st.session_state.get(
        "go_to_investigation",
        False
    ):

        page = "Investigation"

        st.session_state[
            "go_to_investigation"
        ] = False

    # --------------------------------------------------------
    # PAGE ROUTING
    # --------------------------------------------------------

    if page == "Overview":

        render_overview(
            stats
        )

    elif page == "Alerts":

        render_alert_list(
            DEMO_ALERTS
        )

    elif page == "Investigation":

        entity_id = st.session_state.get(
            "selected_entity"
        )

        if entity_id is None:

            st.warning(
                "No entity selected. "
                "Go to Alerts and select an entity."
            )

        else:

            render_entity_detail(
                entity_id
            )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()