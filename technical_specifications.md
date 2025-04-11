
# Streamlit Application: Crypto Arbitrage Identification Strategies

## Overview

This Streamlit application aims to visually and interactively explain and demonstrate various concepts related to cryptocurrency arbitrage. It will cover market representations, arbitrage cycle identification using the Bellman-Ford algorithm, finding optimal cycle sets, and live arbitrage identification, drawing inspiration from the structure and data within the provided source file.

## Step-by-Step Generation Process

1.  **Setup and Title:**
    *   The application will begin with a title: "Crypto Trading and Arbitrage Identification Strategies."
    *   It will also include a subtitle or brief description stating: "Interactive exploration of arbitrage opportunities in crypto markets."

2.  **Navigation:**
    *   A Streamlit sidebar will be used for navigation.
    *   The sidebar will contain a `st.selectbox` or similar component allowing the user to choose from the following sections:
        *   Representations of a Market
        *   Identifying Arbitrage Cycles
        *   Live Arbitrage Identification
        *   Practical Challenges of Arbitrage Trading

3.  **Representations of a Market Section:**
    *   **Exchange Rate Matrix Representation:**
        *   Explain the concept of an exchange rate matrix: "An exchange rate matrix displays the exchange rates between different currencies.  Each cell (i, j) represents the rate at which currency i can be exchanged for currency j."
        *   Example:  `matrix[i][j]` represents how much of currency `j` you get for 1 unit of currency `i`.
        *   Create a Pandas DataFrame using `st.dataframe` to display a synthetic exchange rate matrix, using the same values as shown in the source file. This will be a static representation.

        ```python
        import streamlit as st
        import pandas as pd
        import numpy as np
        import networkx as nx
        import matplotlib.pyplot as plt
        from cvxpy import *

        # Example exchange rate matrix
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
        ```

    *   **Directed Graph Representation:**
        *   Explain the concept of a directed graph representation: "A directed graph can represent the market, where nodes are currencies and edges represent the exchange rates. The weight of each edge (i, j) is the exchange rate from currency i to currency j."
        *   Create a directed graph using `networkx` and visualize it using `matplotlib`. Display this graph using `st.pyplot`. The graph should mirror the layout and edge labels of the example graph in the source file.

        ```python
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
        ```

    *   **Log-Transformed Representations:**
        *   Explain the concept of log-transformed representations: "Taking the logarithm of the exchange rates can transform a multiplicative problem (finding arbitrage cycles) into an additive one, making it easier to detect cycles with negative weights using algorithms like Bellman-Ford."
        *   Formula:  `log(a * b) = log(a) + log(b)`.  Taking the negative log makes arbitrage cycles detectable as negative cycles.
        *   Create a log-transformed exchange rate matrix and display it as a Pandas DataFrame using `st.dataframe`.
        *   Create a directed graph based on the log-transformed matrix and visualize it using `st.pyplot`. This graph should mirror the log-transformed example in the source file.

        ```python
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
        ```

4.  **Identifying Arbitrage Cycles Section:**
    *   **Finding an Arbitrage Cycle with Bellman-Ford:**
        *   Explain the Bellman-Ford algorithm: "The Bellman-Ford algorithm can detect negative cycles in a graph.  In the context of arbitrage, a negative cycle in the log-transformed graph indicates an arbitrage opportunity."
        * Demonstrate the bellman ford algorithm step by step. generate explanation and graph for each step.
        *   Implement the `bf_negative_cycle` function based on the code in the source file (or a simplified version).
        *   Apply the function to the log-transformed graph.
        *   Display the identified arbitrage cycle (if any) using `st.write`.
        *   Calculate and display the arbitrage multiplier for the identified cycle.

        ```python
        # Bellman-Ford Algorithm (Simplified for demonstration)
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
                            return None # No cycle
                    cycle.append(curr)
                    return cycle[::-1]  # Reverse the cycle to the correct order
            return None

        st.subheader("Identifying Arbitrage Cycles")
        st.subheader("Finding an Arbitrage Cycle with Bellman-Ford")
        st.write("The Bellman-Ford algorithm detects negative cycles, indicating arbitrage opportunities in the log-transformed graph.")
        arbitrage_cycle = bf_negative_cycle(G_log)

        if arbitrage_cycle:
            st.write("Arbitrage Cycle Found:", arbitrage_cycle)
            cycle_weight = sum(G_log[arbitrage_cycle[i]][arbitrage_cycle[(i + 1) % len(arbitrage_cycle)]]['weight']
                               for i in range(len(arbitrage_cycle)))
            arbitrage_multiplier = np.exp(-cycle_weight) #undo log transform and negative
            st.write("Arbitrage Multiplier:", arbitrage_multiplier)
        else:
            st.write("No Arbitrage Cycle Found.")
        ```

    *   **Finding an "Optimal" Set of Cycles:**
        *   Explain that finding the absolute best set of arbitrage trades is computationally hard.
        *   Mention that finding an "Optimal" Set of Cycles is an NP-hard problem.
        *   Explain the simplified problem using linear programming relaxation via CVXPY.

5.  **Live Arbitrage Identification Section:**
    *   Explain that live data would be used for this section.
    *   Mention the use of CCXT to fetch the data.

6.  **Practical Challenges of Arbitrage Trading Section:**
    *   List the challenges, such as speed, timing issues, costs of inventory, available liquidity, precision, and error handling, as presented in the source file.  These can be displayed using `st.write` and `st.markdown` for formatting.

## Important Definitions, Examples, and Formulae

*   **Exchange Rate:** The price at which one currency can be exchanged for another.
*   **Exchange Rate Matrix:** A matrix where `matrix[i][j]` represents the exchange rate from currency `i` to currency `j`.
    *   Example: `matrix[0][1] = 0.75` means 1 unit of currency 0 can be exchanged for 0.75 units of currency 1.
*   **Arbitrage:** Exploiting price differences for the same asset in different markets to make a profit.
*   **Arbitrage Cycle:** A sequence of currency exchanges that results in a profit when starting and ending with the same currency.
*   **Directed Graph:** A graph where edges have a direction, representing the flow of exchange from one currency to another.
*   **Edge Weight:**  In our directed graph, the exchange rate between two currencies.
*   **Log Transformation:** Applying the logarithm to exchange rates to convert multiplication into addition, simplifying arbitrage detection.
    *   Formula: `log(a * b) = log(a) + log(b)`
*   **Bellman-Ford Algorithm:** A graph algorithm used to find the shortest paths from a source node to all other nodes in a weighted graph, capable of detecting negative cycles.
*   **Negative Cycle:** A cycle in a graph where the sum of the edge weights is negative. In the context of log-transformed exchange rates, a negative cycle indicates an arbitrage opportunity.
*   **Arbitrage Multiplier:** The profit factor obtained by executing an arbitrage cycle. It's calculated as the exponential of the negative sum of log-transformed exchange rates in the cycle (or, equivalently, the product of the original exchange rates).

## Libraries and Tools

*   **Streamlit:**  The primary framework for building the interactive web application. Used for creating the user interface, handling user input, and displaying data and visualizations.  Functions like `st.title`, `st.sidebar`, `st.dataframe`, `st.pyplot`, and `st.write` will be extensively used.
*   **Pandas:**  Used for creating and manipulating dataframes to represent exchange rate matrices and display them in a tabular format.
*   **NumPy:** Used for numerical computations, especially for applying the log transformation to the exchange rate matrix and calculating arbitrage multipliers.
*   **NetworkX:**  A Python library for creating, manipulating, and studying the structure, dynamics, and functions of complex networks. Used to create directed graph representations of the currency exchange market.
*   **Matplotlib:**  Used for generating static plots and visualizations, particularly for visualizing the directed graphs created with NetworkX.
*   **CVXPY:** A Python-embedded modeling language for convex optimization problems. Is used to solve the linear programming relaxation for finding the optimal set of arbitrage cycles.
*   **CCXT:** (Mentioned but likely not implemented in this simplified spec): A cryptocurrency exchange trading library for fetching live data from crypto exchanges.



### Appendix Code

```code
# set things up and create button
Button(description='New Example', style=ButtonStyle())
```

```code
# set some parameters, generate exchange rate matrix and the corresponding graph
N = 6 # number of currencies
max_spread_pct = 0.05 # maximum bid-ask spread in pct of bid, 0.05 for 5%
```

```code
# generate and display random exchange rate matrix
target
0
1
2 3
4
5
source 0 1.00 0.58
0.63 0.27 0.17 0.20
1 1.68 1.00
0.39 0.74 0.47 0.79
2 1.57 2.48
1.00 0.04 0.15 0.11
3 3.64 1.35 22.94 1.00 0.22 0.23
4 5.84 2.02 6.84 4.40 1.00 0.49
5 4.76 1.21 8.59 4.41 1.97 1.00
```

```code
# display corresponding directed graph
```

```code
# display log-transformed exchange rate matrix and corresponding graph
Taking negative logs...
```

```code
# The Bellman-Ford function used in this notebook
def bf_negative_cycle(G):
    # Remove nan edges
    n = len(G.nodes()) + 1
    edges = [edge for edge in G.edges().data() if ~np.isnan (edge[2]['weight'])]

    # Add a starting node and add edges with zero weight to all other nodes
    start_node_edges = [(n-1, i, {'weight': 0}) for i in range(n-1)]
    edges = edges + start_node_edges
    
    # Initialize node distances and predecessors
    d = np.ones(n) * np.inf
    d[n - 1] = 0 # Starting node has zero distance
    p = np.ones(n) * -1

    # Relax n times
    for i in range(n):
        X = -1
        for e in edges:
            if d[int(e[0])] + e[2]['weight'] < d[int(e[1])]:
                d[int(e[1])] = d[int(e[0])] + e[2]['weight']
                p[int(e[1])] = int(e[0])
                x = int(e[1])
        if x == -1: # If no relaxation possible, no negative cycle
            return None

    # Identify negative cycle
    for i in range(n):
        x = p[int(x)]
    cycle = []
    v = x
    while True:
        cycle.append(int(v))
        if v == x and len(cycle) > 1:
            break
        v = p[int(v)]
    return list(reversed(cycle))
```

```code
# Check if arbitrage cycle exists using Bellman-Ford. If so, output an arbitrage cycle
At least one arbitrage cycle exists! One such cycle is [2, 1, 5, 3, 2] with cycle leng
th -5.2893 which implies and arbitrage multiplier of 198.2033.
```

```code
# Alternative: Solve Assignment Problem with CVXPY
X = Variable((len(C_ln),len(C_ln)))
iota
= np.ones((len(C_ln),1))

constraints = [X <= 1,
               X >= 0,
               X*iota == 1,
               np.transpose(iota)*X == 1]

# Form objective.
obj = Minimize(sum(multiply(X, C_ln)))

# Form and solve problem.
prob = Problem(obj, constraints)
prob.solve()  # Returns the optimal value.
print ("status:", prob.status)
print ("optimal value", prob.value)
X = pd.DataFrame(X.value)
display(X.round(3))
```

```code
# Find best set of arbitrage cycles by solving the assignment problem
Optimal cycle set multiplier (assumes one has enough quantities in every sub-cycle):
389.5750080640003.
Multiplier is garuanteed to be at least as large as the multiplier found by Bellman-F
ord (198.2033 in this example).
```

```code
# Maximize inventory
target
0
1
2 3
4
5
source 0 1.00 0.58
0.63 0.27 0.17 0.20
1 1.68 1.00
0.39 0.74 0.47 0.79
2 1.57 2.48
1.00 0.04 0.15 0.11
3 3.64 1.35 22.94 1.00 0.22 0.23
4 5.84 2.02
6.84 4.40 1.00 0.49
5 4.76 1.21
8.59 4.41 1.97 1.00

inventory_start
currency
0
1.0
1
1.0
2
1.0
3
1.0
4
1.0
5
1.0

seconds it took: 0.017813920974731445
status: optimal
optimal value: 999.998326792761

Quantities matrix Q:
```

```code
# set some parameters
```

```code
# set things up and create button
Button(description='Find Arbitrage Cycles', style=ButtonStyle())
```

```code
# create real time exchange rate matrix
Updating all quotes (496 pairs overall) took 0.9450349807739258 seconds.
```

```code
# Check if arbitrage cycle exists using Bellman-Ford. If so, output an arbitrage cycle
Bellmann-Ford took 0.22376108169555664 seconds.
At least one arbitrage cycle exists! One such cycle is ['BTC', 'CDT', 'ETH', 'BTC'] wi
th cycle length -0.000546627229625 which implies and arbitrage multiplier of 1.0005467
766575147.
```

```code
# Find best set of arbitrage cycles by solving the assignment problem
Solving assignment problem took 0.053289175033569336 seconds.
Assignment problem multiplier is 1.0006195840057635.
```