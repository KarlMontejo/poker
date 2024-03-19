import streamlit as st
import pandas as pd
import math
import streamlit_nested_layout
from Poker import Game, Deck, Player
import time


# title
st.title('Poker🃏')
st.info(f"Play poker against opponents that utilize Langchain for decision-making.")
st.markdown("---")

# opponents user input sidebar
st.sidebar.markdown('### Opponents')
st.sidebar.info('adjust your opponents before starting the game')
with st.sidebar.expander("Opponent Options"):
    st.session_state.num_opponents = st.slider('Number of Opponents', min_value = 1, max_value = 9, step = 1)
    st.session_state.opp_difficulty = st.radio('Select Opponent Difficulty', ["Amateur", "Intermediate", "Expert"])
st.sidebar.markdown('---')
    

# button to start game
st.sidebar.markdown('### Start game')
st.sidebar.info('click button to start game')
# deal button
if not st.sidebar.button('start game'):
    st.stop()
st.session_state.game = Game(num_opponents=st.session_state.num_opponents, opp_difficulty=st.session_state.opp_difficulty)
st.session_state.game.display_table()
st.session_state.game.deal_players()
st.sidebar.markdown('---')

# debug
st.sidebar.markdown('### Debug')
st.sidebar.info('click button to reveal debug options')
with st.sidebar.expander('Debugging Options'):
    st.session_state.debug_mode = st.toggle('debug')
    st.session_state.god_mode = st.toggle('god mode')
if st.session_state.get('debug_mode', False):
    with st.sidebar.expander('Debugging Section'):
        with st.expander("Session State"):
            st.json(st.session_state)
        with st.expander("Game"):
            st.markdown(f"Game (num_players): {st.session_state.game.num_players}")
            st.markdown(f"Game (num_opponents): {st.session_state.game.num_opponents}")
            st.markdown(f"Game (opp_difficulty): {st.session_state.game.opp_difficulty}")
        with st.expander("Players"):
            with st.expander("User"):
                st.markdown(f"Player: {st.session_state.game.players[0]}")
                st.markdown(f"Hand: {st.session_state.game.players[0].hand}")
            with st.expander("Opponents"):
                st.markdown(f"Players: {st.session_state.game.players}")
else:
    st.sidebar.write("debug mode is off")


# create a placeholder for the cards display
if 'position1_hand' not in st.session_state:
    st.session_state.position1_hand = '1🃏'
    st.session_state.position2_hand = '2🃏'
    st.session_state.position3_hand = '3🃏'
    st.session_state.position4_hand = '4🃏'
    st.session_state.position5_hand = '5🃏'
    st.session_state.position6_hand = 'U🃏'
    st.session_state.position7_hand = '7🃏'
    st.session_state.position8_hand = '8🃏'
    st.session_state.position9_hand = '9🃏'
    st.session_state.position10_hand = '10🃏'


# player options
st.markdown ("---")
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
        