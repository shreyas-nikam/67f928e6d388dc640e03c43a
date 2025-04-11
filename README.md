# Crypto Trading and Arbitrage Identification Strategies

This repository contains a multi-page Streamlit application demonstrating interactive visualizations and examples of cryptocurrency trading and arbitrage identification strategies.

## Overview

The app includes:
- **Representations of a Market:** Illustrations using a static exchange rate matrix, a directed graph representation, and log-transformed versions.
- **Identifying Arbitrage Cycles:** Implementation of the Bellman-Ford algorithm to detect negative cycles, indicating potential arbitrage opportunities.
- **Live Arbitrage Identification:** A conceptual page discussing live data identification using libraries like CCXT.
- **Practical Challenges of Arbitrage Trading:** Discussion of real-world challenges in executing arbitrage strategies.

## Usage

1. Install dependencies using:
   ```
   pip install -r requirements.txt
   ```
2. Run the app with:
   ```
   streamlit run app.py
   ```

## Docker

A Dockerfile is provided for containerized deployments. Build and run the container as follows:
   ```
   docker build -t qulab .
   docker run -p 8501:8501 qulab
   ```

## License

© 2025 QuantUniversity. All Rights Reserved.
