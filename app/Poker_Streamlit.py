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
st.sidebar.markdown('### Game Options')
st.sidebar.info('adjust your opponents before starting the game')
with st.sidebar.expander("Opponent Options"):
    st.session_state.num_opponents = st.slider('Number of Opponents', min_value = 1, max_value = 9, step = 1)
    st.session_state.opp_difficulty = st.radio('Select Opponent Difficulty', ["Amateur", "Intermediate", "Expert"])
with st.sidebar.expander("General Options"):
    st.session_state.game_speed = st.slider('Game speed', min_value = 1, max_value = 5, step = 1)
st.sidebar.markdown('---')

# temporary game
if 'game' not in st.session_state:
    st.session_state['game'] = Game(num_opponents=st.session_state.num_opponents, opp_difficulty=st.session_state.opp_difficulty, game_speed=st.session_state.game_speed)

# button to start game
st.sidebar.markdown('### Start game')
st.sidebar.info('click button to start game')
st.session_state.start_game = st.sidebar.button('start game')

# deal button
if st.session_state.start_game:
    
    st.session_state.game = Game(num_opponents=st.session_state.num_opponents, opp_difficulty=st.session_state.opp_difficulty, game_speed=st.session_state.game_speed)
    
    # setup initial table
    st.session_state.game.display_table()

    # deal players
    st.session_state.game.deal_players()

    # deal community cards
    st.session_state.game.display_community_cards("burn", st.session_state.game.burn_container)
    st.session_state.game.display_community_cards("flop_1", st.session_state.game.flop_1_container)
    st.session_state.game.display_community_cards("flop_2", st.session_state.game.flop_2_container)
    st.session_state.game.display_community_cards("flop_3", st.session_state.game.flop_3_container)
    st.session_state.game.display_community_cards("burn", st.session_state.game.burn_container)
    st.session_state.game.display_community_cards("turn", st.session_state.game.turn_container)
    st.session_state.game.display_community_cards("burn", st.session_state.game.burn_container)
    st.session_state.game.display_community_cards("river", st.session_state.game.river_container)
    time.sleep(1)

    # empty player containers
    st.session_state.game.empty_player_containers()
    # update table
    st.session_state.game.display_table()

    st.sidebar.markdown('---')

    
    # player options
    st.markdown("---")
    st.markdown("### Make your move:")

    # cards and stack
    col1_cards, col2_stack = st.columns(2)
    col1_cards.markdown(f"Your cards: {st.session_state.game.players[str(5)].show_hand()}", unsafe_allow_html=True)
    col2_stack.markdown(f"Your stack: <h1 style='text-align: center;'>{st.session_state.game.players[str(5)].stack}</h1>", unsafe_allow_html=True)

    # fold check call raise
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
            st.info(f"Game (num_players): {st.session_state.game.num_players}")
            st.info(f"Game (num_opponents): {st.session_state.game.num_opponents}")
            st.info(f"Game (opp_difficulty): {st.session_state.game.opp_difficulty}")
        with st.expander("Players"):
            with st.expander("User"):
                st.info(f"Player Object: {st.session_state.game.players[str(5)]}")
                st.info(f"User Hand: {st.session_state.game.players[str(5)].hand}")
        with st.expander("Deck"):
            with st.expander("Community Cards"):
                st.info(f"Burn: {st.session_state.game.deck.burnt}")
                st.info(f"Flop: {st.session_state.game.deck.flop}")
                st.info(f"Turn: {st.session_state.game.deck.turn}")
                st.info(f"River: {st.session_state.game.deck.river}")
else:
    st.sidebar.write("debug mode is off")


            