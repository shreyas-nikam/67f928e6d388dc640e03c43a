import streamlit as st
from application_pages import representations_of_market, identifying_arbitrage_cycles, live_arbitrage_identification, practical_challenges

st.set_page_config(page_title="QuLab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab")
st.divider()

# Navigation
page = st.sidebar.selectbox(
    label="Navigation",
    options=[
        "Representations of a Market",
        "Identifying Arbitrage Cycles",
        "Live Arbitrage Identification",
        "Practical Challenges of Arbitrage Trading",
    ],
)

if page == "Representations of a Market":
    representations_of_market.app()
elif page == "Identifying Arbitrage Cycles":
    identifying_arbitrage_cycles.app()
elif page == "Live Arbitrage Identification":
    live_arbitrage_identification.app()
elif page == "Practical Challenges of Arbitrage Trading":
    practical_challenges.app()

st.divider()
st.write("© 2025 QuantUniversity. All Rights Reserved.")
st.caption(
    "The purpose of this demonstration is solely for educational use and illustration. "
    "Any reproduction of this demonstration "
    "requires prior written consent from QuantUniversity."
)