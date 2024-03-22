import streamlit as st
import pandas as pd
import math
import streamlit_nested_layout
import os
import time

import Poker
import utils 
import pages
import importlib

importlib.reload(Poker)
importlib.reload(utils)
importlib.reload(pages)

from Poker import Game, Deck, Player
from utils.lc import opponent_decision_langchain
from pages.Dictionary import sim_game_data

# run the app: streamlit run app/Poker_Streamlit.py

# opponent decision wrapper function
def decision_wrapper(player, poker_data):
    # check if the current recipe differs from the previous
    with st.spinner(f"Player {player.id} is thinking..."):
        st.session_state.opponent_decision = opponent_decision_langchain(poker_data)
    st.info(st.session_state.opponent_decision)

# initialize game
def init_game(container):
    # session state for game object
    if 'game' not in st.session_state:
        st.session_state.game = Game(num_opponents=st.session_state.num_opponents, opp_difficulty=st.session_state.opp_difficulty, game_speed=st.session_state.game_speed, parent_container = container)
        st.session_state.table_initialized = False
    
def display_table():
    if 'game' in st.session_state and not st.session_state.get('table_initialized', False):
        st.session_state.table_container = st.session_state.game.init_table()
        st.session_state.table_initialized = True
    with st.session_state.table_container:
        st.session_state.game.update_table_display()
    
# title
st.title('Poker🃏')
st.info(f"Play poker against opponents that utilize Langchain for decision-making.")
st.markdown("---")


# table placeholder
if 'table_placeholder_created' not in st.session_state:
    st.session_state.table_placeholder = st.empty()
    st.session_state.table_placeholder_created = True

# opponents user input sidebar
st.sidebar.markdown('### Game Options')
st.sidebar.info('adjust your opponents before starting the game')
with st.sidebar.expander("Opponent Options"):
    st.session_state.num_opponents = st.slider('Number of Opponents', min_value = 1, max_value = 9, step = 1, value = 9) # temporarily defaulted
    st.session_state.opp_difficulty = st.radio('Select Opponent Difficulty', ["Amateur", "Intermediate", "Expert"])
with st.sidebar.expander("General Options"):
    st.session_state.game_speed = st.slider('Game speed', min_value = 1, max_value = 5, step = 1, value = 5) # temporarily defaulted
st.sidebar.markdown('---')

# button to start game
st.sidebar.markdown('### Start game')
st.sidebar.info('click button to start game')
if st.sidebar.button('Start Game', use_container_width=True):
    with st.spinner('initializing game'):
        time.sleep(1)
        
        init_game(st.session_state.table_placeholder)
    with st.spinner('initializing table'):
        time.sleep(1)
        display_table()

# debug options
st.sidebar.markdown('### Debug')
st.sidebar.info('click button to reveal debug options')
with st.sidebar.expander('Debugging Options'):
    st.session_state.debug_mode = st.toggle('debug', True) # temporarily defaulted
    st.session_state.god_mode = st.toggle('god mode', True) # temporarily defaulted

# debug mode
if st.session_state.get('debug_mode', False):
    with st.sidebar.expander('Debugging Section'):
        debug_section_empty = st.empty()
        debug_section_container = debug_section_empty.container()
else:
    st.sidebar.markdown("debug mode is off")

# god mode
if st.session_state.get('god_mode', False):
    with st.sidebar.expander('god mode'):
        god_section_empty = st.empty()
        god_section_container = god_section_empty.container()
    with god_section_container:
        st.session_state.reveal_all_hands = st.button('Reveal All Hands')
        st.session_state.reveal_cc = st.button('Reveal Community Cards')
else:
    st.sidebar.markdown("god mode is off")

# deal button
if 'game' not in st.session_state:
    st.stop()

if st.session_state.reveal_all_hands:
    st.session_state.game.god_reveal_hands()

# ---------------------------------------------------------------- dynamic table ----------------------------------------------------------------

display_table()

# # update player hands

# # empty player containers
# st.session_state.game.empty_player_containers()


# # display community cards
# st.session_state.game.display_cc("burn_1", st.session_state.game.burn_container) # burn 1
# st.session_state.game.display_cc("flop_1", st.session_state.game.flop_1_container) # flop 1
# st.session_state.game.display_cc("flop_2", st.session_state.game.flop_2_container) # flop 2
# st.session_state.game.display_cc("flop_3", st.session_state.game.flop_3_container) # flop 3
# st.session_state.game.display_cc("burn_2", st.session_state.game.burn_container) # burn 2
# st.session_state.game.display_cc("turn", st.session_state.game.turn_container) # turn
# st.session_state.game.display_cc("burn_3", st.session_state.game.burn_container) # burn 3
# st.session_state.game.display_cc("river", st.session_state.game.river_container) # river

# langchain
for player in enumerate(st.session_state.game.players_list):
    decision_wrapper(player[1], sim_game_data)

# ---------------------------------------------------------------- dynamic table ----------------------------------------------------------------

# debug mode update
if st.session_state.get('debug_mode', False):
    with debug_section_container:
        with st.expander("Session State"):
            st.json(st.session_state)
        with st.expander("Game"):
            game_debug_empty = st.empty()
            with st.expander("Game Dictionary"):
                debug_dictionary = st.session_state.game.get_object_dictionary(st.session_state.game, "debug")
                st.json(debug_dictionary)
            st.info(f"Game (num_players): {st.session_state.game.num_players}")
            st.info(f"Game (num_opponents): {st.session_state.game.num_opponents}")
            st.info(f"Game (opp_difficulty): {st.session_state.game.opp_difficulty}")
        with st.expander("User"):
            st.info(f"Player Id: {st.session_state.game.players_list[5].id}")
            st.info(f"User Hand: {st.session_state.game.players_list[5].hand}")
            st.info(f"User Stack: {st.session_state.game.players_list[5].stack}")
            st.info(f"User Status: {st.session_state.game.players_list[5].status}")
        with st.expander("Deck"):
            with st.expander("Deck Dictionary"):
                debug_dictionary = st.session_state.game.get_object_dictionary(st.session_state.game.deck, "debug")
                st.json(debug_dictionary)
            with st.expander("Community Cards"):
                st.info(f"Burn 1: {st.session_state.game.burn_1}")
                st.info(f"Burn 2: {st.session_state.game.burn_2}")
                st.info(f"Burn 3: {st.session_state.game.burn_3}")
                st.info(f"Flop 1: {st.session_state.game.flop_1}")
                st.info(f"Flop 2: {st.session_state.game.flop_2}")
                st.info(f"Flop 3: {st.session_state.game.flop_3}")
                st.info(f"Turn: {st.session_state.game.turn}")
                st.info(f"River: {st.session_state.game.river}")

        # dictionaries for each player
        with st.expander('Player Dictionaries'):
            for player in enumerate(st.session_state.game.players_list):
                # game and deck dictionaries
                game_dictionary = st.session_state.game.get_object_dictionary(st.session_state.game)
                
                # game data dictionary
                player_data = {}
                player_data["current player data"] = st.session_state.game.get_object_dictionary(player[1], "post_river")

                # update game data with game and deck dictionaries
                st.session_state.game.add_info_to_dict(player_data, "current game data", game_dictionary)

                # display game_data dictionary
                with st.expander(f'Player {player[1].id}'):
                    st.json(player_data)
