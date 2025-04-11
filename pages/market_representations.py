import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import plotly.graph_objects as go

def draw_network_graph(G, title="Graph Visualization"):
    pos = nx.spring_layout(G)
    edge_x = []
    edge_y = []
    for u, v, data in G.edges(data=True):
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    node_x = []
    node_y = []
    node_text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(str(node))
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines')
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="bottom center",
        hoverinfo='text',
        marker=dict(
            size=20,
            color='pink',
            line_width=2))
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title=title,
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40)))
    return fig

def app():
    st.subheader("Market Representations")
    st.write("Interactive exploration of synthetic exchange rate matrix and its representations.")

    # Exchange Rate Matrix Representation
    st.markdown("### Exchange Rate Matrix Representation")
    st.write("An exchange rate matrix displays the exchange rates between different currencies. Each cell (i, j) represents the rate at which currency i can be exchanged for currency j.")
    exchange_rate_matrix = pd.DataFrame({
        0: [1.00, 0.58, 0.63, 0.27, 0.17, 0.20],
        1: [1.68, 1.00, 0.39, 0.74, 0.47, 0.79],
        2: [1.57, 2.48, 1.00, 0.04, 0.15, 0.11],
        3: [3.64, 1.35, 22.94, 1.00, 0.22, 0.23],
        4: [5.84, 2.02, 6.84, 4.40, 1.00, 0.49],
        5: [4.76, 1.21, 8.59, 4.41, 1.97, 1.00]
    })
    st.dataframe(exchange_rate_matrix)

    # Directed Graph Representation using Plotly
    st.markdown("### Directed Graph Representation")
    st.write("A directed graph represents the market, with nodes as currencies and edges displaying exchange rates.")
    G = nx.DiGraph()
    for i in range(len(exchange_rate_matrix)):
        for j in range(len(exchange_rate_matrix)):
            G.add_edge(i, j, weight=exchange_rate_matrix.iloc[i, j])
    fig_graph = draw_network_graph(G, title="Currency Exchange Graph")
    st.plotly_chart(fig_graph, use_container_width=True)

    # Log-Transformed Representations
    st.markdown("### Log-Transformed Representations")
    st.write("Log transformation converts the multiplicative problem into an additive one, which is useful for arbitrage detection.")
    log_exchange_rate_matrix = -np.log(exchange_rate_matrix)
    log_df = pd.DataFrame(log_exchange_rate_matrix)
    st.dataframe(log_df)

    # Directed Graph for log-transformed matrix using Plotly
    st.markdown("#### Log-Transformed Directed Graph Representation")
    G_log = nx.DiGraph()
    for i in range(len(log_df)):
        for j in range(len(log_df)):
            G_log.add_edge(i, j, weight=log_df.iloc[i, j])
    fig_graph_log = draw_network_graph(G_log, title="Log-Transformed Currency Graph")
    st.plotly_chart(fig_graph_log, use_container_width=True)
