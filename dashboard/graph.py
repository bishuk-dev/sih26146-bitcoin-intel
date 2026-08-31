"""
M5: Graph Visualization Component

Renders an investigation subgraph using PyVis.

This module is responsible only for visualizing a NetworkX graph.
The graph data itself is supplied by app.py / the upstream pipeline.
"""

import streamlit as st
from pyvis.network import Network


def render_graph(subgraph):
    """
    Render a NetworkX investigation subgraph using PyVis.

    Parameters
    ----------
    subgraph : networkx.Graph
        The graph that should be displayed.
    """

    st.subheader("Investigation Graph")

    # --------------------------------------------------------
    # Check whether graph data exists
    # --------------------------------------------------------

    if subgraph is None:
        st.info(
            "No graph data available for this entity."
        )
        return

    try:

        # ----------------------------------------------------
        # Create PyVis network
        # ----------------------------------------------------

        net = Network(
            height="550px",
            width="100%",
            directed=True,
            cdn_resources="local"
        )

        # ----------------------------------------------------
        # Convert NetworkX graph to PyVis
        # ----------------------------------------------------

        net.from_nx(subgraph)

        # ----------------------------------------------------
        # Graph configuration
        # ----------------------------------------------------

        net.set_options(
            """
            {
                "nodes": {
                    "shape": "dot",
                    "size": 20,
                    "font": {
                        "size": 16
                    }
                },

                "edges": {
                    "arrows": {
                        "to": {
                            "enabled": true
                        }
                    },

                    "smooth": {
                        "enabled": true,
                        "type": "dynamic"
                    }
                },

                "physics": {
                    "enabled": true,

                    "stabilization": {
                        "enabled": true,
                        "iterations": 200
                    }
                },

                "interaction": {
                    "hover": true,
                    "navigationButtons": true,
                    "keyboard": true
                }
            }
            """
        )

        # ----------------------------------------------------
        # Save graph HTML
        # ----------------------------------------------------

        graph_file = "dashboard/graph_output.html"

        net.save_graph(graph_file)

        # ----------------------------------------------------
        # Read generated HTML
        # ----------------------------------------------------

        with open(
            graph_file,
            "r",
            encoding="utf-8"
        ) as file:

            html = file.read()

        # ----------------------------------------------------
        # Display graph in Streamlit
        # ----------------------------------------------------

        st.components.v1.html(
            html,
            height=600,
            scrolling=True
        )

    except Exception as error:

        st.error(
            f"Unable to render investigation graph: {error}"
        )