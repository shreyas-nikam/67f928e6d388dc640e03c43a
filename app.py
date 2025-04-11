import streamlit as st

st.set_page_config(page_title="QuLab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab")
st.divider()

# Navigation selectbox to choose pages
page = st.sidebar.selectbox("Navigation", [
    "Representations of a Market", 
    "Identifying Arbitrage Cycles", 
    "Live Arbitrage Identification", 
    "Practical Challenges of Arbitrage Trading"
])

if page == "Representations of a Market":
    from pages import market
    market.app()
elif page == "Identifying Arbitrage Cycles":
    from pages import arbitrage
    arbitrage.app()
elif page == "Live Arbitrage Identification":
    from pages import live_arbitrage
    live_arbitrage.app()
elif page == "Practical Challenges of Arbitrage Trading":
    from pages import challenges
    challenges.app()

st.divider()
st.write("© 2025 QuantUniversity. All Rights Reserved.")
st.caption("The purpose of this demonstration is solely for educational use and illustration. Any reproduction of this demonstration requires prior written consent from QuantUniversity.")
