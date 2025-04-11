
import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px

def run_representations():
    st.subheader("Representations of a Market")

    # Exchange Rate Matrix Representation
    exchange_rate_matrix = pd.DataFrame({
        0: [1.00, 0.58, 0.63, 0.27, 0.17, 0.20],
        1: [1.68, 1.00, 0.39, 0.74, 0.47, 0.79],
        2: [1.57, 2.48, 1.00, 0.04, 0.15, 0.11],
        3: [3.64, 1.35, 22.94, 1.00, 0.22, 0.23],
        4: [5.84, 2.02, 6.84, 4.40, 1.00, 0.49],
        5: [4.76, 1.21, 8.59, 4.41, 1.97, 1.00]
    })

    st.subheader("Exchange Rate Matrix Representation")
    st.write("An exchange rate matrix displays the exchange rates between different currencies.")
    st.dataframe(exchange_rate_matrix)

    # Directed Graph Representation
    G = nx.DiGraph()
    for i in range(len(exchange_rate_matrix)):
        for j in range(len(exchange_rate_matrix)):
            G.add_edge(i, j, weight=exchange_rate_matrix.iloc[i, j])

    pos = nx.spring_layout(G)  # You can experiment with different layouts
    edge_labels = {(i, j): round(G[i][j]['weight'], 2) for i, j in G.edges()}

    # Create Plotly graph
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
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
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
            ),
            line_width=2))

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append(f"Currency: {node}")

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Directed Graph Representation',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="A directed graph represents currencies as nodes and exchange rates as edges.",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    st.subheader("Directed Graph Representation")
    st.write("A directed graph represents currencies as nodes and exchange rates as edges.")
    st.plotly_chart(fig, use_container_width=True)

    # Log-Transformed Representations
    log_exchange_rate_matrix = -np.log(exchange_rate_matrix)
    log_exchange_rate_matrix = pd.DataFrame(log_exchange_rate_matrix)
    st.subheader("Log-Transformed Representations")
    st.write("Log transformation converts multiplicative arbitrage detection into an additive problem.")
    st.dataframe(log_exchange_rate_matrix)

    # Create a directed graph from the log-transformed matrix
    G_log = nx.DiGraph()
    for i in range(len(log_exchange_rate_matrix)):
        for j in range(len(log_exchange_rate_matrix)):
            G_log.add_edge(i, j, weight=log_exchange_rate_matrix.iloc[i, j])

    pos_log = nx.spring_layout(G_log)  # You can experiment with different layouts
    edge_labels_log = {(i, j): round(G_log[i][j]['weight'], 2) for i, j in G_log.edges()}

    # Create Plotly graph
    edge_x_log = []
    edge_y_log = []
    for edge in G_log.edges():
        x0, y0 = pos_log[edge[0]]
        x1, y1 = pos_log[edge[1]]
        edge_x_log.append(x0)
        edge_x_log.append(x1)
        edge_x_log.append(None)
        edge_y_log.append(y0)
        edge_y_log.append(y1)
        edge_y_log.append(None)

    edge_trace_log = go.Scatter(
        x=edge_x_log, y=edge_y_log,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x_log = []
    node_y_log = []
    for node in G_log.nodes():
        x, y = pos_log[node]
        node_x_log.append(x)
        node_y_log.append(y)

    node_trace_log = go.Scatter(
        x=node_x_log, y=node_y_log,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
            ),
            line_width=2))

    node_adjacencies_log = []
    node_text_log = []
    for node, adjacencies in enumerate(G_log.adjacency()):
        node_adjacencies_log.append(len(adjacencies[1]))
        node_text_log.append(f"Currency: {node}")

    node_trace_log.marker.color = node_adjacencies_log
    node_trace_log.text = node_text_log

    fig_log = go.Figure(data=[edge_trace_log, node_trace_log],
                    layout=go.Layout(
                        title='Log-Transformed Directed Graph Representation',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="Log transformation converts multiplicative arbitrage detection into an additive problem.",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    st.subheader("Log-Transformed Directed Graph Representation")
    st.write("A directed graph represents currencies as nodes and log-transformed exchange rates as edges.")
    st.plotly_chart(fig_log, use_container_width=True)

