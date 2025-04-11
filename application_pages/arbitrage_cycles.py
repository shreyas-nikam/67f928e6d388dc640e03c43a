import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Set page config
def run_arbitrage_cycles():
    st.title("Arbitrage Cycle Detection Demo")

    st.markdown(
        """
        This demo shows the step-by-step process to detect arbitrage opportunities using the Bellman-Ford algorithm.
        
        **Steps:**
        1. **Exchange Rate Matrix:** Display the initial conversion rates between currencies.
        2. **Log Transformation:** Convert the exchange rates using a negative log transform to expose arbitrage opportunities.
        3. **Graph Construction:** Build a directed graph from the transformed matrix.
        4. **Arbitrage Detection:** Apply the Bellman-Ford algorithm to detect a negative cycle.
        5. **Visualization:** Highlight the arbitrage cycle on the graph.
        
        Adjust the exchange rate for *Currency 1 → Currency 2* in the sidebar to see how the cycle and arbitrage multiplier change.
        """
    )

    #############################
    # Sidebar: Interactive Input
    #############################
    st.sidebar.header("Modify Exchange Rate")
    # User can adjust one conversion rate to see its effect.
    rate_1_to_2 = st.sidebar.slider(
        "Exchange rate for Currency 1 → Currency 2",
        min_value=0.1, max_value=5.0, value=0.39, step=0.01
    )

    #############################
    # Step 1: Define and Display Exchange Rate Matrix
    #############################
    st.subheader("Step 1: Exchange Rate Matrix")
    default_matrix = {
        0: [1.00, 0.58, 0.63, 0.27, 0.17, 0.20],
        1: [1.68, 1.00, rate_1_to_2, 0.74, 0.47, 0.79],
        2: [1.57, 2.48, 1.00, 0.04, 0.15, 0.11],
        3: [3.64, 1.35, 22.94, 1.00, 0.22, 0.23],
        4: [5.84, 2.02, 6.84, 4.40, 1.00, 0.49],
        5: [4.76, 1.21, 8.59, 4.41, 1.97, 1.00]
    }

    exchange_rate_matrix = pd.DataFrame(default_matrix)
    st.write("The exchange rate matrix shows conversion rates between 6 currencies (rows represent source and columns the target currencies).")
    st.dataframe(exchange_rate_matrix)

    #############################
    # Step 2: Log Transformation
    #############################
    st.subheader("Step 2: Log-Transformed Matrix")
    st.markdown(
        """
        To expose arbitrage opportunities, we perform a negative logarithmic transformation of the exchange rates.
        
        The transformation is:
        
        $$w_{ij} = -log(rate_{ij})$$
        
        A negative cycle (where the sum of $$w_{ij}$$ is negative) indicates an arbitrage opportunity.
        """
    )
    log_exchange_rate_matrix = -np.log(exchange_rate_matrix)
    log_exchange_rate_df = pd.DataFrame(log_exchange_rate_matrix)
    st.dataframe(log_exchange_rate_df)

    #############################
    # Step 3: Graph Construction
    #############################
    st.subheader("Step 3: Graph Construction")
    st.markdown("We construct a directed graph where each currency is a node and each edge is weighted by the log-transformed rate.")

    # Create graph from log-transformed matrix
    G_log = nx.DiGraph()
    n = len(log_exchange_rate_df)
    for i in range(n):
        for j in range(n):
            G_log.add_edge(i, j, weight=log_exchange_rate_df.iloc[i, j])

    # Draw the complete graph
    st.markdown("**Graph Visualization:**")
    pos = nx.spring_layout(G_log, k=1, seed=42)  # consistent layout
    plt.figure(figsize=(8, 6))
    nx.draw_networkx(G_log, pos, with_labels=True, node_color='lightblue', arrows=True, node_size=200)
    edge_labels = nx.get_edge_attributes(G_log, 'weight')
    nx.draw_networkx_edge_labels(G_log, pos, edge_labels={k: f"{v:.2f}" for k, v in edge_labels.items()}, font_size=6)
    st.pyplot(plt)

    #############################
    # Step 4: Detect Arbitrage Cycle (Bellman-Ford)
    #############################
    st.subheader("Step 4: Detecting Arbitrage Cycle")
    st.markdown(
        """
        We apply the Bellman-Ford algorithm to detect any negative cycle in the graph. 
        A negative cycle in the log-transformed graph implies an arbitrage opportunity.
        """
    )

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

        # Check for negative cycle
        for u, v, weight in graph.edges(data='weight'):
            if dist[u] != float('inf') and dist[u] + weight < dist[v]:
                # Negative cycle detected; reconstruct the cycle.
                cycle = []
                curr = v
                visited = {node: False for node in graph.nodes()}
                while not visited[curr]:
                    visited[curr] = True
                    cycle.append(curr)
                    curr = pred[curr]
                    if curr is None:
                        return None
                cycle.append(curr)
                return cycle[::-1]  # Reverse to correct order
        return None

    arbitrage_cycle = bf_negative_cycle(G_log)

    if arbitrage_cycle:
        st.success(f"Arbitrage Cycle Found: {arbitrage_cycle}")
        cycle_weight = sum(
            G_log[arbitrage_cycle[i]][arbitrage_cycle[(i + 1) % len(arbitrage_cycle)]]['weight'] 
            for i in range(len(arbitrage_cycle))
        )
        arbitrage_multiplier = np.exp(-cycle_weight)
        st.write("**Arbitrage Multiplier:**", arbitrage_multiplier)
    else:
        st.error("No Arbitrage Cycle Found.")

    #############################
    # Step 5: Highlight Arbitrage Cycle in Graph
    #############################
    if arbitrage_cycle:
        st.subheader("Step 5: Visualizing the Arbitrage Cycle")
        st.markdown(
            """
            The arbitrage cycle is highlighted in red in the graph below. 
            The red edges indicate the sequence of conversions that lead to an arbitrage opportunity.
            """
        )
        cycle_edges = [
            (arbitrage_cycle[i], arbitrage_cycle[(i + 1) % len(arbitrage_cycle)])
            for i in range(len(arbitrage_cycle))
        ]
        plt.figure(figsize=(8, 6))
        nx.draw_networkx(G_log, pos, with_labels=True, node_color='lightblue', arrows=True, node_size=200)
        nx.draw_networkx_edges(G_log, pos, edgelist=cycle_edges, edge_color='red', width=2)
        nx.draw_networkx_edge_labels(G_log, pos, edge_labels={k: f"{v:.2f}" for k, v in edge_labels.items()}, font_size=6)
        st.pyplot(plt)
