import streamlit as st

# Set up page configuration and header
st.set_page_config(page_title="QuLab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab")
st.divider()

# Navigation Sidebar for multi-page app
page = st.sidebar.selectbox("Navigate", 
    ["Market Representations", "Identifying Arbitrage Cycles", "Live Arbitrage Identification", "Practical Challenges of Arbitrage Trading"])

if page == "Market Representations":
    from pages import market_representations as mr
    mr.app()
elif page == "Identifying Arbitrage Cycles":
    from pages import arbitrage_cycle as ac
    ac.app()
elif page == "Live Arbitrage Identification":
    from pages import live_arbitrage as la
    la.app()
elif page == "Practical Challenges of Arbitrage Trading":
    from pages import practical_challenges as pc
    pc.app()

st.divider()
st.write("© 2025 QuantUniversity. All Rights Reserved.")
st.caption("The purpose of this demonstration is solely for educational use and illustration. "
           "Any reproduction of this demonstration requires prior written consent from QuantUniversity.")
