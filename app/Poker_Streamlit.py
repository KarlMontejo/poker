import streamlit as st
import pandas as pd
import math
import streamlit_nested_layout
from Poker import Game, Deck, Player



# title
st.title('Poker🃏')
st.info(f"Play poker against opponents that utilize Langchain for decision-making.")
st.markdown("---")

# opponents user input sidebar
st.sidebar.markdown('### Opponents')
st.sidebar.info('adjust your opponents before starting the game')
with st.sidebar.expander("Opponent Options"):
    st.session_state.num_opponents = st.slider('Number of Opponents', min_value = 1, max_value = 10, step = 1)
    st.session_state.opp_difficulty = st.radio('Select Opponent Difficulty', ["Amateur", "Intermediate", "Expert"])
st.sidebar.markdown('---')


# initialize game
if 'game' not in st.session_state:
    st.session_state.deck = Deck()
    st.session_state.deck.shuffle()
    st.session_state.game = Game(deck=st.session_state.deck, num_opponents=st.session_state.num_opponents, opp_difficulty=st.session_state.opp_difficulty)
    st.session_state.players = st.session_state.game.create_players()

# debug
st.sidebar.markdown('### Debug')
st.sidebar.info('click button to reveal debug options')
with st.sidebar.expander('Debugging Options'):
    st.session_state.debug_mode = st.toggle('debug')
    st.session_state.god_mode = st.toggle('god mode')
if st.session_state.get('debug_mode', False):
    st.session_state.game = Game(st.session_state.deck, st.session_state.num_opponents, st.session_state.opp_difficulty)
    st.session_state.players = st.session_state.game.create_players()
    with st.sidebar.expander('Debugging Section'):
        with st.expander("Session State"):
            st.json(st.session_state)
        with st.expander("Game"):
            st.markdown(f"Game (num_players): {st.session_state.game.num_players}")
            st.markdown(f"Game (num_opponents): {st.session_state.game.num_opponents}")
            st.markdown(f"Game (opp_difficulty): {st.session_state.game.opp_difficulty}")
        with st.expander("Deck"):
            st.markdown(f"Deck: {st.session_state.deck}")
        with st.expander("Players"):
            with st.expander("User"):
                st.markdown(f"Player: {st.session_state.players[0]}")
                st.markdown(f"Hand: {st.session_state.players[0].hand}")
            with st.expander("Opponents"):
                st.markdown(f"Players: {st.session_state.players}")
else:
    st.sidebar.write("debug mode is off")

# button to deal a new hand (not necessary)
if st.button('Deal Player'):
    st.session_state.game.deal_players()

# table
st.header("Table")
st.markdown(f"<h1 style='text-align: center;'>DEALER</h1>", unsafe_allow_html=True)

# create a row of columns for the cards
col1_table,col2_table,col3_table,col4_table,col5_table,col6_table = st.columns(6)

# create a placeholder for the cards display
if 'position1_hand' not in st.session_state:
    st.session_state.position1_hand = '1🃏'
    st.session_state.position2_hand = '2🃏'
    st.session_state.position3_hand = '3🃏'
    st.session_state.position4_hand = '4🃏'
    st.session_state.position5_hand = '5🃏'
    st.session_state.position6_hand = '6🃏'
    st.session_state.position7_hand = '7🃏'
    st.session_state.position8_hand = '8🃏'
    st.session_state.position9_hand = '9🃏'
    st.session_state.position10_hand = '10🃏'

px_xl = "380"
px_lg = "100"
px_md = "90" # must be <= 90
px_sm = "20"

# position 1
container_position1 = st.container()
with container_position1:
    with col5_table:
        st.markdown(f"<div style='height: 0px;'>&nbsp;</div>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center;'>{st.session_state.position1_hand}</h1>", unsafe_allow_html=True)
        st.markdown(f"<div style='height: {px_lg}px;'>&nbsp;</div>", unsafe_allow_html=True)

# position 2
container_position2 = st.container()
with container_position2:
    with col6_table:
        st.markdown(f"<div style='height: {px_md}px;'>&nbsp;</div>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center;'>{st.session_state.position2_hand}</h1>", unsafe_allow_html=True)
        st.markdown(f"<div style='height: {px_sm}px;'>&nbsp;</div>", unsafe_allow_html=True)

# position 3
container_position3 = st.container()
with container_position3:
    with col6_table:
        st.markdown(f"<div style='height: {px_sm}px;'>&nbsp;</div>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center;'>{st.session_state.position3_hand}</h1>", unsafe_allow_html=True)
        st.markdown(f"<div style='height: 0px;'>&nbsp;</div>", unsafe_allow_html=True)
    
# position 4
container_position4 = st.container()
with container_position4:
    with col5_table:
        st.markdown(f"<div style='height: {px_lg}px;'>&nbsp;</div>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center;'>{st.session_state.position4_hand}</h1>", unsafe_allow_html=True)
        st.markdown(f"<div style='height: 0px;'>&nbsp;</div>", unsafe_allow_html=True)

# position 5
container_position5 = st.container()
with container_position5:
    with col4_table:
        st.markdown(f"<div style='height: {px_xl}px;'>&nbsp;</div>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center;'>{st.session_state.position5_hand}</h1>", unsafe_allow_html=True)
        st.markdown(f"<div style='height: 0px;'>&nbsp;</div>", unsafe_allow_html=True)

# position 6
container_position6 = st.container()
with container_position6:
    with col3_table:
        st.markdown(f"<div style='height: {px_xl}px;'>&nbsp;</div>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center;'>{st.session_state.position6_hand}</h1>", unsafe_allow_html=True)
        st.markdown(f"<div style='height: 0px;'>&nbsp;</div>", unsafe_allow_html=True)

# position 8
container_position8 = st.container()
with container_position8:
    with col1_table:
        st.markdown(f"<div style='height: {px_md}px;'>&nbsp;</div>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center;'>{st.session_state.position8_hand}</h1>", unsafe_allow_html=True)
        st.markdown(f"<div style='height: {px_sm}px;'>&nbsp;</div>", unsafe_allow_html=True)

# position 9
container_position9 = st.container()
with container_position9:
    with col1_table:
        st.markdown(f"<div style='height: {px_sm}px;'>&nbsp;</div>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center;'>{st.session_state.position9_hand}</h1>", unsafe_allow_html=True)
        st.markdown(f"<div style='height: 0px;'>&nbsp;</div>", unsafe_allow_html=True)

# position 10
container_position6 = st.container()
with container_position6:
    with col2_table:
        st.markdown(f"<div style='height: 0px;'>&nbsp;</div>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center;'>{st.session_state.position10_hand}</h1>", unsafe_allow_html=True)
        st.markdown(f"<div style='height: {px_lg}px;'>&nbsp;</div>", unsafe_allow_html=True)

# position 7
container_position7 = st.container()
with container_position7:
    with col2_table:
        st.markdown(f"<div style='height: {px_lg}px;'>&nbsp;</div>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center;'>{st.session_state.position7_hand}</h1>", unsafe_allow_html=True)
        st.markdown(f"<div style='height: 0px;'>&nbsp;</div>", unsafe_allow_html=True)


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
        