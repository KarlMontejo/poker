import streamlit as st
import pandas as pd
import math
import streamlit_nested_layout

# title
st.title('Poker🃏')

# small text box
st.markdown(f"""
<div style="
    border-radius: 5px;
    background-color: #000080;
    color: white;
    padding: 10px;
    max-width: 1000px;
    margin: 10px 0;
    font-size: 16px;
">
    Play poker against opponents that utilize Langchain for decision-making.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown ("### Community Cards:")

# opponents user input sidebar
st.sidebar.markdown('### Define the number of opponents')
with st.sidebar.expander("Opponents"):
    num_opponents = st.slider('Number of Opponents', min_value = 1, max_value = 10, step = 1)
    st.multiselect('Select Difficulty of Opponents', [1,2,3])

