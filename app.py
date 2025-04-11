
import streamlit as st

st.set_page_config(page_title="QuLab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab")
st.divider()

# Your code goes here
page = st.sidebar.selectbox(label="Navigation", options=["Representations of a Market", "Identifying Arbitrage Cycles", "Live Arbitrage Identification", "Practical Challenges of Arbitrage Trading"])

if page == "Representations of a Market":
    from application_pages.representations import run_representations
    run_representations()
elif page == "Identifying Arbitrage Cycles":
    from application_pages.arbitrage_cycles import run_arbitrage_cycles
    run_arbitrage_cycles()
elif page == "Live Arbitrage Identification":
    from application_pages.live_arbitrage import run_live_arbitrage
    run_live_arbitrage()
elif page == "Practical Challenges of Arbitrage Trading":
    from application_pages.challenges import run_challenges
    run_challenges()


st.divider()
st.write("© 2025 QuantUniversity. All Rights Reserved.")
st.caption("The purpose of this demonstration is solely for educational use and illustration. "
           "Any reproduction of this demonstration "
           "requires prior written consent from QuantUniversity.")
