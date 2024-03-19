import streamlit as st
from Poker import Deck, Player

st.session_state.hand = "x,x"

col1_table, col2_table = st.columns(2)

with col1_table:
    empty_position9 = st.empty()
    with empty_position9.container():
        st.markdown(f"<h1 style='text-align: center;'>{st.session_state.hand}</h1>", unsafe_allow_html=True)

with empty_position9.container():
    st.session_state.hand = "y,y"
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.hand}</h1>", unsafe_allow_html=True)