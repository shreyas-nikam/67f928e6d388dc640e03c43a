
# Crypto Trading and Arbitrage Identification Strategies

This Streamlit application provides an interactive exploration of arbitrage opportunities in cryptocurrency markets.

## Sections

*   **Representations of a Market:** Visualizes exchange rate matrices and directed graphs.
*   **Identifying Arbitrage Cycles:** Demonstrates the Bellman-Ford algorithm for detecting arbitrage cycles.
*   **Live Arbitrage Identification:** (Placeholder) Indicates where live data integration would occur.
*   **Practical Challenges of Arbitrage Trading:** Lists the challenges involved in arbitrage trading.

## How to Run

1.  Make sure you have docker installed.
2.  Clone this repository.
3.  Build the Docker image: `docker build -t crypto-arbitrage .`
4.  Run the Docker container: `docker run -p 8501:8501 crypto-arbitrage`
5.  Open your browser and go to `http://localhost:8501`.

## Dependencies

*   Streamlit
*   Pandas
*   NumPy
*   NetworkX
*   Plotly

