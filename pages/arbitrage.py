import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx

def bf_negative_cycle(graph):
    nodes = list(graph.nodes())
    dist = {node: float('inf') for node in nodes}
    pred = {node: None for node in nodes}
    start_node = nodes[0]
    dist[start_node] = 0
    for _ in range(len(nodes)-1):
        for u, v, data in graph.edges(data=True):
            if dist[u] + data['weight'] < dist[v]:
                dist[v] = dist[u] + data['weight']
                pred[v] = u
    # Check for negative cycles
    for u, v, data in graph.edges(data=True):
        if dist[u] + data['weight'] < dist[v]:
            cycle = []
            cur = v
            visited = set()
            while cur not in visited:
                visited.add(cur)
                cur = pred[cur]
                if cur is None: 
                    break
            if cur is None:
                continue
            cycle_start = cur
            cycle = [cycle_start]
            cur = pred[cycle_start]
            while cur != cycle_start:
                cycle.append(cur)
                cur = pred[cur]
            cycle.append(cycle_start)
            return cycle[::-1]
    return None

def app():
    st.subheader("Identifying Arbitrage Cycles")
    st.write("The Bellman-Ford algorithm is used below on the log-transformed exchange rate graph to detect negative cycles (potential arbitrage opportunities).")

    # Recreate the log-transformed exchange rate matrix from static data
    exchange_rate_matrix = pd.DataFrame({
        0: [1.00, 0.58, 0.63, 0.27, 0.17, 0.20],
        1: [1.68, 1.00, 0.39, 0.74, 0.47, 0.79],
        2: [1.57, 2.48, 1.00, 0.04, 0.15, 0.11],
        3: [3.64, 1.35, 22.94, 1.00, 0.22, 0.23],
        4: [5.84, 2.02, 6.84, 4.40, 1.00, 0.49],
        5: [4.76, 1.21, 8.59, 4.41, 1.97, 1.00]
    })
    log_exchange_rate_matrix = -np.log(exchange_rate_matrix)
    n = len(log_exchange_rate_matrix)
    G_log = nx.DiGraph()
    for i in range(n):
        for j in range(n):
            G_log.add_edge(i, j, weight=log_exchange_rate_matrix.iloc[i, j])

    arbitrage_cycle = bf_negative_cycle(G_log)
    if arbitrage_cycle:
        st.write("Arbitrage Cycle Found:", arbitrage_cycle)
        cycle_weight = 0
        for i in range(len(arbitrage_cycle)-1):
            u = arbitrage_cycle[i]
            v = arbitrage_cycle[i+1]
            cycle_weight += G_log[u][v]['weight']
        arbitrage_multiplier = np.exp(-cycle_weight)
        st.write("Arbitrage Multiplier:", arbitrage_multiplier)
    else:
        st.write("No Arbitrage Cycle Found.")
