
import streamlit as st

def run_challenges():
    st.subheader("Practical Challenges of Arbitrage Trading")
    st.write("Arbitrage trading faces several practical challenges:")
    challenges_list = [
        "**Speed:** The faster you can execute trades, the higher chance to profit.",
        "**Timing Issues:** Market conditions change rapidly, and arbitrage opportunities can disappear quickly.",
        "**Costs of Inventory:** Holding crypto inventory incurs costs (e.g., opportunity cost, storage fees).",
        "**Available Liquidity:** Sufficient liquidity is needed to execute large arbitrage trades without significantly impacting prices.",
        "**Precision:** Accurate price data and order execution are crucial for profitability.",
        "**Error Handling:** Robust error handling is necessary to deal with unexpected issues (e.g., exchange downtime)."
    ]
    for challenge in challenges_list:
        st.write(f"- {challenge}")
