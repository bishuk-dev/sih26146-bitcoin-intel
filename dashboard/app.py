"""
Streamlit dashboard — the only module the judges directly click through, so
polish here has outsized impact.

CRITICAL: this must render with zero internet access. Two known traps:
  1. Pyvis defaults to pulling JS/CSS from a CDN -> configure
     Network(cdn_resources='local') or the graph view will be a blank page
     when the Wi-Fi is off.
  2. Streamlit itself is fine offline, but any custom font/icon import
     from a remote URL will silently fail air-gapped. Bundle assets locally.

Views to build:
  1. Overview: total transactions/wallets/IPs processed, alert counts.
  2. Ranked alert list: entity, risk score, top reasons (from src/scoring).
  3. Entity detail: click an alert -> show its local subgraph (Pyvis) +
     full SHAP-based explanation.
"""

import streamlit as st
from pyvis.network import Network

st.set_page_config(page_title="Bitcoin Transaction Intelligence", layout="wide")


def render_overview(stats: dict):
    raise NotImplementedError


def render_alert_list(alerts: list[dict]):
    raise NotImplementedError


def render_entity_detail(entity_id: str):
    """Renders subgraph via Pyvis. Must use cdn_resources='local':

        net = Network(cdn_resources='local')
    """
    raise NotImplementedError


if __name__ == "__main__":
    st.title("Bitcoin Transaction Intelligence — Offline Investigation Dashboard")
    st.info("Wire this up to src/scoring output once the pipeline runs end-to-end.")
