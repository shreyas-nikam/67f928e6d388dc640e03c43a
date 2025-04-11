
import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx

def run_arbitrage_cycles():
    st.subheader("Identifying Arbitrage Cycles")
    st.subheader("Finding an Arbitrage Cycle with Bellman-Ford")
    st.write("The Bellman-Ford algorithm detects negative cycles, indicating arbitrage opportunities in the log-transformed graph.")

    # Example exchange rate matrix (same as in representations.py)
    exchange_rate_matrix = pd.DataFrame({
        0: [1.00, 0.58, 0.63, 0.27, 0.17, 0.20],
        1: [1.68, 1.00, 0.39, 0.74, 0.47, 0.79],
        2: [1.57, 2.48, 1.00, 0.04, 0.15, 0.11],
        3: [3.64, 1.35, 22.94, 1.00, 0.22, 0.23],
        4: [5.84, 2.02, 6.84, 4.40, 1.00, 0.49],
        5: [4.76, 1.21, 8.59, 4.41, 1.97, 1.00]
    })

    # Log-transformed exchange rate matrix
    log_exchange_rate_matrix = -np.log(exchange_rate_matrix)
    log_exchange_rate_matrix = pd.DataFrame(log_exchange_rate_matrix)

    # Create a directed graph from the log-transformed matrix
    G_log = nx.DiGraph()
    for i in range(len(log_exchange_rate_matrix)):
        for j in range(len(log_exchange_rate_matrix)):
            G_log.add_edge(i, j, weight=log_exchange_rate_matrix.iloc[i, j])


    def bf_negative_cycle(graph):
        dist = {node: float('inf') for node in graph.nodes()}
        pred = {node: None for node in graph.nodes()}
        start_node = 0
        dist[start_node] = 0

        for _ in range(len(graph.nodes()) - 1):
            for u, v, weight in graph.edges(data='weight'):
                if dist[u] != float('inf') and dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    pred[v] = u

        for u, v, weight in graph.edges(data='weight'):
            if dist[u] != float('inf') and dist[u] + weight < dist[v]:
                # Negative cycle detected. Construct the cycle.
                cycle = []
                curr = v
                visited = {node: False for node in graph.nodes()}
                while not visited[curr]:
                    visited[curr] = True
                    cycle.append(curr)
                    curr = pred[curr]
                    if curr is None:
                        return None  # No cycle
                cycle.append(curr)
                return cycle[::-1]  # Reverse the cycle to the correct order
        return None

    arbitrage_cycle = bf_negative_cycle(G_log)

    if arbitrage_cycle:
        st.write("Arbitrage Cycle Found:", arbitrage_cycle)
        cycle_weight = sum(G_log[arbitrage_cycle[i]][arbitrage_cycle[(i + 1) % len(arbitrage_cycle)]]['weight']
                           for i in range(len(arbitrage_cycle)))
        arbitrage_multiplier = np.exp(-cycle_weight)  # undo log transform and negative
        st.write("Arbitrage Multiplier:", arbitrage_multiplier)
    else:
        st.write("No Arbitrage Cycle Found.")


    st.subheader("Finding an 'Optimal' Set of Cycles")
    st.write("Finding the absolute best set of arbitrage trades is computationally hard (NP-hard).")
    st.write("This section would demonstrate a simplified problem using linear programming relaxation via CVXPY.")
    st.write("Implementation of CVXPY to find optimal cycle is omitted from this demo due to complexity and lack of specification in the prompt.")
