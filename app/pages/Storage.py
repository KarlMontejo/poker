import streamlit as st
from Poker import Game, Deck, Player



# end of table 
st.sidebar.markdown('---')

# player options
st.markdown("---")
st.markdown("### Make your move")
st.info("It's your turn. Choose whether to fold, check, call, bet, or raise")

# cards and stack
col1_cards, col2_stack = st.columns(2)
col1_cards.markdown(f"<h3 style='text-align: center;'>Your cards:</h3> {st.session_state.game.players[str(5)].show_hand()}", unsafe_allow_html=True)
col2_stack.markdown(f"<h3 style='text-align: center;'>Your stack:</h3> <h1 style='text-align: center;'>{st.session_state.game.players[str(5)].stack}  BB</h1>", unsafe_allow_html=True)

# fold check call raise
col_fold, col_check, col_call, col_bet, col_raise = st.columns(5)
col_fold.button('Fold', use_container_width=True)
col_check.button('Check', use_container_width=True)
col_call.button('Call', use_container_width=True)

# bet
if col_bet.button('Bet', use_container_width=True):
    if 'show_bet_slider' not in st.session_state:
        st.session_state['show_bet_slider'] = True  
    else:
        st.session_state.show_bet_slider = not st.session_state.show_bet_slider
if st.session_state.get('show_bet_slider', False):
    with col_bet.expander("Choose your bet amount:"):
        bet_amount = st.slider("bet", min_value=0, max_value=1000, value=100, step=10)

# raise
if col_raise.button('Raise', use_container_width=True):
    if 'show_raise_slider' not in st.session_state:
        st.session_state['show_raise_slider'] = True  
    else:
        st.session_state.show_raise_slider = not st.session_state.show_raise_slider
if st.session_state.get('show_raise_slider', False):
    with col_raise.expander("Choose your raise amount:"):
        raise_amount = st.slider("Raise Amount", min_value=0, max_value=1000, value=100, step=10)

if st.session_state.get('reveal_all_hands'):
    st.session_state.game.god_reveal_hands()
    # Optionally reset the flag to prevent re-triggering if needed
    st.session_state.reveal_all_hands = False

if st.session_state.get('reveal_cc'):
    st.session_state.game.god_reveal_cc()
    # reset flag
    st.session_state.reveal_cc = False
