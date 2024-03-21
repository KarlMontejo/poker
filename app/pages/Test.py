import streamlit as st
from Poker import Game, Deck, Card, Player
import time


class Player:
    def __init__(self, id=None, is_user=False):
        self.hand = []
        self.current_bet = 0
        self.status = "active"
        self.is_user = is_user
        self.stack = 100.0
        self.container = None
        self.column = None
        self.id = id
    
    def display_data_html(self, cards):
        player_type = "You" if self.is_user else f"Player {self.id}"
        st.markdown(f"<h1 style='text-align: center;'>{cards}</h1><h5 style='text-align: center;'>{player_type}</h5><h5 style='text-align: center;'>{self.stack}  BB</h5>", unsafe_allow_html=True)
            
    def display(self):
        if self.container:
            with self.container:
                if self.hand:  
                    card_displays = [f"{card.value}{Card.suit_convert(card.suit)}" for card in self.hand]
                    cards_html = '&nbsp;'.join(card_displays)
                    self.display_data_html(cards_html)
    
    def cover_hand(self):
        if self.container:
            with self.container:
                if self.hand:  
                    cards_html = '❤️&nbsp;❤️'
                    self.display_data_html(cards_html)

    def show_hand(self):
        if self.hand:
            card_displays = [f"{card.value}{Card.suit_convert(card.suit)}" for card in self.hand]
            cards_html = '&nbsp;'.join(card_displays)
            hand_html = f"<h1 style='text-align: center;'>{cards_html}</h1>"
        return hand_html
        
    def bust_out(self):
        self.status = "eliminated"

    def all_in(self):
        self.status = "all-in"

class Game():
    def __init__(self, num_opponents, opp_difficulty, game_speed):

        # parameters and attributes
        self.parent_container = st.empty()
        self.num_opponents = num_opponents
        self.opp_difficulty = opp_difficulty
        self.game_speed = game_speed
        self.num_players = num_opponents + 1
        self.card_interval = 2 + (0.1 - 2) * ((self.game_speed - 1) / (5 - 1))
        
        # player creation and position initialization
        self.players = {
            '0': None, '1': None, '2': None, '3': None, '4': None, '5': Player(is_user=True), '6': None, '7': None, '8': None, '9': None
        }
        self.create_players()
        self.players_list = [player for player in self.players.values() if player]
        
        # deck
        self.deck = Deck()                 # start with sorted deck
        self.deck.shuffle()                # shuffle deck
        self.deal_cards()                  # deal players
        self.burn_1 = self.deck.deal(1)    # burn
        self.flop_1 = self.deck.deal(1)    # deal flop 1
        self.flop_2 = self.deck.deal(1)    # deal flop 2
        self.flop_3 = self.deck.deal(1)    # deal flop 3
        self.burn_2 = self.deck.deal(1)    # burn
        self.turn = self.deck.deal(1)      # deal turn
        self.burn_3 = self.deck.deal(1)    # burn
        self.river = self.deck.deal(1)     # deal river

    # create players
    def create_players(self):
        # create opponents
        create_opponents = {
            "1" : [0], "2" : [1,8], "3" : [1,4,8], "4" : [0,4,7,9], "5" : [0,2,4,7,9], "6" : [0,2,4,6,7,9], "7" : [0,2,3,4,6,7,9], "8" : [0,1,2,3,4,6,7,9], "9" : [0,1,2,3,4,6,7,8,9]
        }
        opponent_id = 1
        opponents_map = create_opponents[str(self.num_opponents)]
        for opponent_idx in opponents_map:
            if opponent_idx > 5 and not self.players['5'].id:
                self.players['5'].id = opponent_id
                opponent_id += 1
            self.players[str(opponent_idx)] = Player(id=str(opponent_id))
            opponent_id += 1
    
    # deal players
    def deal_cards(self):
        for _ in range(2):
            for player in self.players_list:
                dealt_cards = self.deck.deal(1)
                player.hand += dealt_cards

    # empty all player containers
    def empty_player_containers(self):
        for player in self.players_list:
            with player.container:
                st.empty()
    
    # empty all player containers
    def empty_cc_containers(self):
        self.flop_1_container.empty()
        self.flop_2_container.empty()
        self.flop_3_container.empty()
        self.burn_container.empty()
        self.turn_container.empty()
        self.river_container.empty()

    # deal players animation
    def deal_players_animation(self):
        for player in self.players_list:
            with player.container:
                st.markdown(f"<h1 style='text-align: center;'>&nbsp;</h1>", unsafe_allow_html=True)
        for player in self.players_list:
            with player.container:
                time.sleep(self.card_interval)
                player.display_data_html('✋🤚')
        for player in self.players_list:
            with player.container:
                time.sleep(self.card_interval)
                player.display_data_html('🃏🤚')
        for player in self.players_list:
            with player.container:
                time.sleep(self.card_interval)
                player.display_data_html('🃏🃏')
                if player.is_user:
                    time.sleep(self.card_interval)
                    player.display()

    # animation for community card deal
    def deal_cc_animation(self, container):
        with container: 
            time.sleep(self.card_interval)
            st.markdown(f"<h1 style='text-align: center;'>🃏</h1>", unsafe_allow_html=True)

    # animation for burn deal
    def burn_animation(self, container):
        with container:
            time.sleep(self.card_interval)
            st.markdown(f"<h1 style='text-align: center;'>🃏</h1>", unsafe_allow_html=True)
            time.sleep(self.card_interval)
            st.markdown(f"<h1 style='text-align: center;'>🔥</h1>", unsafe_allow_html=True)
            time.sleep(self.card_interval)
            st.markdown(f"<h1 style='text-align: center;'>💨</h1>", unsafe_allow_html=True)
            time.sleep(self.card_interval)
            st.markdown(f"<h1 style='text-align: center;'>&nbsp;</h1>", unsafe_allow_html=True)
    
    # collected animations
    def deal_animation(self):
        with self.parent_container:
            # animations
            self.deal_players_animation()                    # deal players
            self.burn_animation(self.burn_container)         # burn 1
            self.deal_cc_animation(self.flop_1_container)    # flop 1
            self.deal_cc_animation(self.flop_2_container)    # flop 2
            self.deal_cc_animation(self.flop_3_container)    # flop 3
            self.burn_animation(self.burn_container)         # burn 2
            self.deal_cc_animation(self.turn_container)      # turn
            self.burn_animation(self.burn_container)         # burn 3
            self.deal_cc_animation(self.river_container)     # river

# --------------------------------------------------------------------- table init ---------------------------------------------------------------------
    
    # initialize table with players
    def init_table(self):
        with self.parent_container:
            # table columns
            
            col1_table,col2_table,col3_table,col4_table,col5_table,col6_table = st.columns(6)

            # initialize community card containers
            def init_community_cards(cc_type):
                # Directly assign emptied containers to their respective class variables
                if cc_type == "flop_1":
                    self.flop_1_container = col1_table.empty()
                elif cc_type == "flop_2":
                    self.flop_2_container = col2_table.empty()
                elif cc_type == "flop_3":
                    self.flop_3_container = col3_table.empty()
                elif cc_type == "burn":
                    self.burn_container = col4_table.empty()
                elif cc_type == "turn":
                    self.turn_container = col5_table.empty()
                elif cc_type == "river":
                    self.river_container = col6_table.empty()

                # Get the target container based on cc_type
                target_container = getattr(self, f"{cc_type}_container", None)

                # Display an empty space in the target container
                if target_container is not None:
                    with target_container:
                        st.markdown(f"<h1 style='text-align: center;'>&nbsp;</h1>", unsafe_allow_html=True)
            
            # standardized pixel spacing
            px_xl = "280"
            px_xl2 = "230"
            px_lg = "110"
            px_md = "85" # must be <= 90
            px_sm = "25"
            px_zo = "0"

            # display container (initialized as empty)
            squares = {}
            def display_position(column, square_pos):
                nonlocal squares
                # assigns an empty container to a position in a dictionary of squares 
                squares[square_pos] = column.empty() 

            # display an empty space with column and pixel amount
            def display_space(column, pixel):
                column.markdown(f"<div style='height: {pixel}px;'>&nbsp;</div>", unsafe_allow_html=True)
            

            # position 1
            display_position(col5_table, 1)
            display_space(col5_table, px_lg)

            # turn
            init_community_cards("turn")

            # position 2
            display_space(col6_table, px_md)
            display_position(col6_table, 2) 
            display_space(col6_table, px_sm)

            # river
            init_community_cards("river")

            # position 3
            display_space(col6_table, px_sm)
            display_position(col6_table, 3) 
            display_space(col6_table, px_zo)

            # position 4
            display_space(col5_table, px_lg)
            display_position(col5_table, 4) 
            display_space(col5_table, px_zo)

            # burn
            display_space(col4_table, px_xl)
            init_community_cards("burn")

            # position 5
            display_space(col4_table, px_xl2)
            display_position(col4_table, 5)
            display_space(col4_table, px_zo)

            # flop 3
            display_space(col3_table, px_xl)
            init_community_cards("flop_3")

            # position 6 - YOU
            display_space(col3_table, px_xl2)
            display_position(col3_table, 6) 
            display_space(col3_table, px_zo)

            # posdition 10
            display_position(col2_table, 10) 
            display_space(col2_table, px_lg)

            # flop 2
            init_community_cards("flop_2")

            # position 7
            display_space(col2_table, px_lg)
            display_position(col2_table, 7) 
            display_space(col2_table, px_zo)

            # position 9
            display_space(col1_table, px_md)
            display_position(col1_table, 9) 
            display_space(col1_table, px_sm)

            # flop 1
            init_community_cards("flop_1")

            # position 8
            display_space(col1_table, px_sm)
            display_position(col1_table, 8) 
            display_space(col1_table, px_zo)

            # for key and container in squares dictionary
            for key, item_container in squares.items():
                if self.players[str(int(key)-1)]:
                    player = self.players[str(int(key)-1)]
                    player.container = item_container
                    time.sleep(self.card_interval)
            
            return self.parent_container
        
    def update_table_content(self):
        if 'game' in st.session_state:
            game = st.session_state.game
            for player in game.players_list:
                player.display()

    def update_table_game(self):
        if 'game' in st.session_state:
            game = st.session_state.game
            for player in game.players_list:
                player.cover_hand()
        
def init_game():
    """Initializes the game and stores it in session state."""
    if 'game' not in st.session_state:
        st.session_state['game'] = Game(9, "Average", 5)
        # Flag to indicate the table is initialized and avoid re-initialization
        st.session_state['table_initialized'] = False

def display_table():
    """Displays the game table and initializes UI elements if not already done."""
    if not st.session_state.get('table_initialized', False):
        st.session_state.game.init_table()
        st.session_state.game.deal_animation()
        st.session_state['table_initialized'] = True

        # Replace direct usage of deal_animation with a call to update UI based on the current state
        # For animations, consider using Streamlit components or periodic state updates
        update_ui()

def update_ui():
    """Updates the UI based on the current game state."""
    if 'game' in st.session_state:
        game = st.session_state['game']
        
        # Assuming there's a method to update player and community card displays based on current state
        game.update_table_content()  # Implement this method in the Game class

def update_game():
    """Triggered when the 'Update Game' button is pressed."""
    if 'game' in st.session_state:
        # Example of an update - add your game logic that changes the state
        game = st.session_state['game']
        game.update_table_game() 

        # Update UI elements based on the new game state
        update_ui()

# Initialize and display the game table upon app startup
init_game()
display_table()

# Button to update the game, tied to the update_game function
if st.button('Update Game'):
    update_game()
