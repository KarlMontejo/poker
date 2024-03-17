import streamlit as st
import pandas as pd
import math
import streamlit_nested_layout
from Streamlit_Helpers import Streamlit_Card, Streamlit_Player
from Poker import Card, Deck, Player, Player_Decision

# title
st.title('Poker🃏')


# small text box
st.info(f"Play poker against opponents that utilize Langchain for decision-making.")

st.markdown("---")

# opponents user input sidebar
st.sidebar.markdown('Use the section below to adjust your opponents before starting the game')
st.sidebar.markdown('### Opponents')
with st.sidebar.expander("Opponent Options"):
    st.session_state.num_opponents = st.slider('Number of Opponents', min_value = 1, max_value = 10, step = 1)
    st.radio('Select Opponent Difficulty', ["Amateur", "Intermediate", "Expert"])

# table
st.header("Table")
st.markdown(f"<h1 style='text-align: center;'>DEALER</h1>", unsafe_allow_html=True)

# create a row of columns for the cards
col1_table,col2_table,col3_table,col4_table,col5_table,col6_table = st.columns(6)

pos_1, pos_2, pos_3, pos_4, pos_5, pos_6, pos_7, pos_8, pos_9, pos_10, hand_pos_1, hand_pos_2, hand_pos_3, hand_pos_4, hand_pos_5, hand_pos_6, hand_pos_7, hand_pos_8, hand_pos_9, hand_pos_10 = Streamlit_Player.get_position(st.session_state.num_opponents)

table_flop_1 = ["AS"]
table_flop_2 = ["KH"]
table_flop_3 = ["QC"]
table_burn = ["burn"]
table_turn = ["JH"]
table_river = ["10S"]

# position 9
Streamlit_Card.display_cards_in_column(pos_9, col1_table, hand_pos_9, 10, 130, 50) 
# flop 1
Streamlit_Card.display_cards_in_column("", col1_table, table_flop_1, 10, 0, 0)
# position 8
Streamlit_Card.display_cards_in_column(pos_8, col1_table, hand_pos_8, 10, 20, 0)
# position 10
Streamlit_Card.display_cards_in_column(pos_10, col2_table, hand_pos_10, 10, 0, 160)
# flop 2
Streamlit_Card.display_cards_in_column("", col2_table, table_flop_2, 10, 0, 0)
# position 7
Streamlit_Card.display_cards_in_column(pos_7, col2_table, hand_pos_7, 10, 130, 0)
# flop 3
Streamlit_Card.display_cards_in_column("", col3_table, [""], 10, 160, 0)
Streamlit_Card.display_cards_in_column("", col3_table, table_flop_3, 10, 0, 0)
# user
Streamlit_Card.display_cards_in_column("User", col3_table, hand_pos_6, 10, 240, 0)
# burn
Streamlit_Card.display_cards_in_column("", col4_table, [""], 10, 160, 0)
Streamlit_Card.display_cards_in_column("", col4_table, table_burn, 10, 0, 0)
# opponent 5
Streamlit_Card.display_cards_in_column(pos_5, col4_table, hand_pos_5, 10, 240, 30)
# opponent 1
Streamlit_Card.display_cards_in_column(pos_1, col5_table, hand_pos_1, 10, 0, 160)
# turn
Streamlit_Card.display_cards_in_column("", col5_table, table_turn, 10, 0, 0)
# opponent 4
Streamlit_Card.display_cards_in_column(pos_4, col5_table, hand_pos_4, 10, 130, 0)
# opponent 2
Streamlit_Card.display_cards_in_column(pos_2, col6_table, hand_pos_2, 10, 120, 60)
# river
Streamlit_Card.display_cards_in_column("", col6_table, table_river, 10, 00, 0)
# opponent 3
Streamlit_Card.display_cards_in_column(pos_3, col6_table, hand_pos_3, 10, 20, 0)

# player options
st.markdown ("### Make your move:")
col_fold, col_check, col_call, col_raise = st.columns(4)
col_fold.button('Fold', use_container_width=True)
col_check.button('Check', use_container_width=True)
col_call.button('Call', use_container_width=True)

# toggle slider
if col_raise.button('Raise', use_container_width=True):
    if 'show_raise_slider' not in st.session_state:
        st.session_state['show_raise_slider'] = True  
    else:
        st.session_state.show_raise_slider = not st.session_state.show_raise_slider  # toggle value if it exists


# check if the slider should be shown
if st.session_state.get('show_raise_slider', False):
    # display the slider
    with col_raise.expander("Choose your raise amount:"):
        raise_amount = st.slider("Raise Amount", min_value=0, max_value=1000, value=100, step=10)