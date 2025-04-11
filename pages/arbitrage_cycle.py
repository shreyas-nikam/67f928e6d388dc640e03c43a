import streamlit as st
import numpy as np
import networkx as nx

def bf_negative_cycle(graph):
    # Bellman-Ford Algorithm (Simplified)
    dist = {node: float('inf') for node in graph.nodes()}
    pred = {node: None for node in graph.nodes()}
    start_node = list(graph.nodes())[0]
    dist[start_node] = 0
    # Relax edges repeatedly
    for _ in range(len(graph.nodes()) - 1):
        for u, v, data in graph.edges(data=True):
            if dist[u] + data['weight'] < dist[v]:
                dist[v] = dist[u] + data['weight']
                pred[v] = u
    # Check for a negative cycle
    for u, v, data in graph.edges(data=True):
        if dist[u] + data['weight'] < dist[v]:
            # A negative cycle is detected; backtrack to recover the cycle.
            cycle = []
            curr = v
            for _ in range(len(graph.nodes())):
                curr = pred[curr]
            cycle_start = curr
            cycle.append(cycle_start)
            curr = pred[cycle_start]
            while curr != cycle_start:
                cycle.append(curr)
                curr = pred[curr]
            cycle.append(cycle_start)
            cycle.reverse()
            return cycle
    return None

def app():
    st.subheader("Identifying Arbitrage Cycles")
    st.write("This section implements the Bellman-Ford algorithm to detect arbitrage opportunities in the log-transformed market graph.")
    
    # Synthetic Exchange Rate Matrix and Log Transformation
    exchange_rate_matrix = np.array([
        [1.00, 0.58, 0.63, 0.27, 0.17, 0.20],
        [1.68, 1.00, 0.39, 0.74, 0.47, 0.79],
        [1.57, 2.48, 1.00, 0.04, 0.15, 0.11],
        [3.64, 1.35, 22.94, 1.00, 0.22, 0.23],
        [5.84, 2.02, 6.84, 4.40, 1.00, 0.49],
        [4.76, 1.21, 8.59, 4.41, 1.97, 1.00]
    ])
    log_matrix = -np.log(exchange_rate_matrix)
    
    # Build graph from log-transformed matrix
    G_log = nx.DiGraph()
    n = log_matrix.shape[0]
    for i in range(n):
        for j in range(n):
            G_log.add_edge(i, j, weight=log_matrix[i, j])
            
    cycle = bf_negative_cycle(G_log)
    if cycle:
        st.write("Arbitrage cycle found:", cycle)
        # Compute cycle weight (exclude repeating node at end)
        cycle_weight = sum(G_log[cycle[i]][cycle[(i+1)% (len(cycle)-1)]]['weight'] for i in range(len(cycle)-1))
        arbitrage_multiplier = np.exp(-cycle_weight)
        st.write("Arbitrage multiplier:", round(arbitrage_multiplier, 4))
    else:
        st.write("No arbitrage cycle found.")
