import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import plotly.graph_objects as go

def plot_nx_graph(G, title):
    pos = nx.spring_layout(G, seed=42)
    edge_x = []
    edge_y = []
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        mode='lines')
    
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=[str(node) for node in G.nodes()],
        textposition="bottom center",
        marker=dict(
            color='pink',
            size=20,
            line_width=2))
    
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title=title,
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40)))
    return fig

def app():
    st.subheader("Representations of a Market")
    st.write("Below is an explanation and visualization of the exchange rate matrix and its directed graph representation.")

    # Exchange rate matrix representation
    exchange_rate_matrix = pd.DataFrame({
        0: [1.00, 0.58, 0.63, 0.27, 0.17, 0.20],
        1: [1.68, 1.00, 0.39, 0.74, 0.47, 0.79],
        2: [1.57, 2.48, 1.00, 0.04, 0.15, 0.11],
        3: [3.64, 1.35, 22.94, 1.00, 0.22, 0.23],
        4: [5.84, 2.02, 6.84, 4.40, 1.00, 0.49],
        5: [4.76, 1.21, 8.59, 4.41, 1.97, 1.00]
    })
    st.markdown("### Exchange Rate Matrix Representation")
    st.write("An exchange rate matrix displays the exchange rates between different currencies. Each cell (i, j) represents the rate at which currency i can be exchanged for currency j.")
    st.dataframe(exchange_rate_matrix)

    # Create directed graph from exchange rate matrix and visualize with Plotly
    G = nx.DiGraph()
    n = len(exchange_rate_matrix)
    for i in range(n):
        for j in range(n):
            G.add_edge(i, j, weight=exchange_rate_matrix.iloc[i, j])
    st.markdown("### Directed Graph Representation")
    st.write("A directed graph represents the market where nodes are currencies and edges (with weights) represent exchange rates.")
    fig1 = plot_nx_graph(G, "Exchange Rate Graph")
    st.plotly_chart(fig1, use_container_width=True)

    # Log-transformed representations
    st.markdown("### Log-Transformed Representations")
    st.write("Taking the negative logarithm of the exchange rates transforms the multiplicative arbitrage problem into an additive one.")
    log_exchange_rate_matrix = -np.log(exchange_rate_matrix)
    log_exchange_rate_matrix = pd.DataFrame(log_exchange_rate_matrix)
    st.dataframe(log_exchange_rate_matrix)

    # Create directed graph from log-transformed matrix
    G_log = nx.DiGraph()
    for i in range(n):
        for j in range(n):
            G_log.add_edge(i, j, weight=log_exchange_rate_matrix.iloc[i, j])
    fig2 = plot_nx_graph(G_log, "Log-Transformed Exchange Rate Graph")
    st.plotly_chart(fig2, use_container_width=True)
