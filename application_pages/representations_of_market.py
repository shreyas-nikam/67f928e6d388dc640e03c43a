import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Example exchange rate matrix
exchange_rate_matrix = pd.DataFrame({
    0: [1.00, 0.58, 0.63, 0.27, 0.17, 0.20],
    1: [1.68, 1.00, 0.39, 0.74, 0.47, 0.79],
    2: [1.57, 2.48, 1.00, 0.04, 0.15, 0.11],
    3: [3.64, 1.35, 22.94, 1.00, 0.22, 0.23],
    4: [5.84, 2.02, 6.84, 4.40, 1.00, 0.49],
    5: [4.76, 1.21, 8.59, 4.41, 1.97, 1.00]
})

def app():
    st.subheader("Exchange Rate Matrix Representation")
    st.write("An exchange rate matrix displays the exchange rates between different currencies.")
    st.dataframe(exchange_rate_matrix)

    # Create a directed graph from the exchange rate matrix
    G = nx.DiGraph()
    for i in range(len(exchange_rate_matrix)):
        for j in range(len(exchange_rate_matrix)):
            G.add_edge(i, j, weight=exchange_rate_matrix.iloc[i, j])

    # Visualization
    pos = nx.spring_layout(G)  # You can experiment with different layouts
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='pink', node_size=800, font_size=10, alpha=0.8)
    edge_labels = {(i, j): round(G[i][j]['weight'], 2) for i, j in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    st.subheader("Directed Graph Representation")
    st.write("A directed graph represents currencies as nodes and exchange rates as edges.")
    st.pyplot(plt)  # Display the graph in Streamlit
    plt.clf() #clear the plot to prevent issues when displaying multiple plots

    # Log-transformed exchange rate matrix
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

    # Visualization
    pos_log = nx.spring_layout(G_log)  # You can experiment with different layouts
    plt.figure(figsize=(8, 6))
    nx.draw(G_log, pos_log, with_labels=True, node_color='pink', node_size=800, font_size=10, alpha=0.8)
    edge_labels_log = {(i, j): round(G_log[i][j]['weight'], 2) for i, j in G_log.edges()}
    nx.draw_networkx_edge_labels(G_log, pos_log, edge_labels=edge_labels_log, font_size=8)
    st.pyplot(plt)
    plt.clf()