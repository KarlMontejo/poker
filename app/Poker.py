from utils.lc import opponent_decision_langchain
import streamlit as st
import math
import random
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
        self.deck = Deck()
    
    # reveals the hand of the player in the table
    def display_data_html(self, cards):
        player_type = "<span style='color: #48D1CC;'>You</span>" if self.is_user else f"Player {self.id}"
        stack_html = f"<span style='background-color: #90EE90; padding: 5px 10px; border-radius: 5px; color: #505050;'>{self.stack} BB</span>"  # Added color: #505050 for dark grey
        st.markdown(f"<h2 style='text-align: center;'>{cards}</h2><h5 style='text-align: center;'>{player_type}</h5><h5 style='text-align: center;'>{stack_html}</h5>", unsafe_allow_html=True)

    # reveals the hand of the player in the table
    def reveal_hand(self):
        if self.container:
            with self.container:
                if self.hand:
                    if self.status == "active" and self.is_user: # user cards
                        card_displays = [
                            f"""<div style='background-color: white; border: 1px solid black; padding: 6px; border-radius: 6px; display: inline-flex; justify-content: center; align-items: center; margin: 1px; color: {"black" if card.suit in ["C", "S"] else "red"}; font-size: 28px; text-align: center; width: 48px; height: 67px; flex-direction: column;'>
                                <span style='margin-bottom: -10px;'>{card.value}</span> 
                                <span style='font-size: 28px; line-height: 1;'>{Card.suit_convert(card.suit)}</span>  
                            </div>"""
                            for card in self.hand
                        ]
                    elif self.status == "active" and not self.is_user: # back of cards
                        card_displays = [self.deck.card_back_html + self.deck.card_back_html]
                    elif self.status == "eliminated": # grey cards
                        card_displays = [self.deck.table_emoji('💀')]
                    elif self.status == "showdown": # opponent cards
                        card_displays = [
                            f"""<div style='background-color: white; border: 1px solid black; padding: 6px; border-radius: 6px; display: inline-flex; justify-content: center; align-items: center; margin: 1px; color: {"black" if card.suit in ["C", "S"] else "red"}; font-size: 28px; text-align: center; width: 48px; height: 67px; flex-direction: column;'>
                                <span style='margin-bottom: -10px;'>{card.value}</span> 
                                <span style='font-size: 28px; line-height: 1;'>{Card.suit_convert(card.suit)}</span>  
                            </div>"""
                            for card in self.hand
                        ]
                    cards_html = ''.join(card_displays)
                    self.display_data_html(cards_html)

    # reveals the hand of the player anywhere in the ui
    def show_hand(self):
        if self.hand:
            card_displays = [f"{card.value}{Card.suit_convert(card.suit)}" for card in self.hand]
            cards_html = '&nbsp;'.join(card_displays)
            hand_html = f"<h2 style='text-align: center;'>{cards_html}</h2>"
        return hand_html
        
    def bust_out(self):
        self.status = "eliminated"

    def all_in(self):
        self.status = "all-in"

class Game():
    def __init__(self, num_opponents, opp_difficulty, game_speed, parent_container):

        # parameters and attributes
        self.parent_container = parent_container
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

# --------------------------------------------------------------------- table init ---------------------------------------------------------------------
    
    # initialize table with players
    def init_table(self):
        with self.parent_container:
                        
            # table headers and dealer
            st.markdown(f"<h3 style='text-align: center;'>Table</h3>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center;'>DEALER</h1>", unsafe_allow_html=True)

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
                        st.markdown(f"<h2 style='text-align: center;'>&nbsp;&nbsp;{self.deck.table_emoji('&nbsp;')}</h2>", unsafe_allow_html=True)
            
            # standardized pixel spacing
            px_xl = "290"
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
            
            # deal players animation
            def deal_players_animation():
                card_back_html = self.deck.card_back_html

                for player in self.players_list:
                    with player.container:
                        st.markdown(f"<h2 style='text-align: center;'>&nbsp;</h2>", unsafe_allow_html=True)

                for player in self.players_list:
                    with player.container:
                        time.sleep(self.card_interval)
                        player.display_data_html(self.deck.table_emoji('✋')+self.deck.table_emoji('🤚'))

                for player in self.players_list:
                    with player.container:
                        time.sleep(self.card_interval)
                        player.display_data_html(card_back_html+self.deck.table_emoji('🤚'))

                for player in self.players_list:
                    with player.container:
                        time.sleep(self.card_interval)
                        player.display_data_html(card_back_html + card_back_html)

                        if player.is_user:
                            time.sleep(self.card_interval)
                            player.reveal_hand()

            # animation for community card deal
            def deal_cc_animation(container):
                with container: 
                    time.sleep(self.card_interval)
                    st.markdown(f"<h2 style='text-align: center;'>&nbsp;&nbsp;{self.deck.card_back_html}</h2>", unsafe_allow_html=True)

            # animation for burn deal
            def burn_animation(container):
                with container:
                    time.sleep(self.card_interval)
                    st.markdown(f"<h2 style='text-align: center;'>&nbsp;&nbsp;{self.deck.card_back_html}</h2>", unsafe_allow_html=True)
                    time.sleep(self.card_interval)
                    st.markdown(f"<h2 style='text-align: center;'>&nbsp;&nbsp;{self.deck.table_emoji('🔥')}</h2>", unsafe_allow_html=True)
                    time.sleep(self.card_interval)
                    st.markdown(f"<h2 style='text-align: center;'>&nbsp;&nbsp;{self.deck.table_emoji('💨')}</h2>", unsafe_allow_html=True)
                    time.sleep(self.card_interval)
                    st.markdown(f"<h2 style='text-align: center;'>&nbsp;&nbsp;{self.deck.table_emoji('&nbsp;')}</h2>", unsafe_allow_html=True)

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
            
            # animations
            deal_players_animation()                    # deal players
            burn_animation(self.burn_container)         # burn 1
            deal_cc_animation(self.flop_1_container)    # flop 1
            deal_cc_animation(self.flop_2_container)    # flop 2
            deal_cc_animation(self.flop_3_container)    # flop 3
            burn_animation(self.burn_container)         # burn 2
            deal_cc_animation(self.turn_container)      # turn
            burn_animation(self.burn_container)         # burn 3
            deal_cc_animation(self.river_container)     # river

            return self.parent_container

# --------------------------------------------------------------------- table init ---------------------------------------------------------------------
    
    def update_table_display(self):
        with self.parent_container:
            for player in self.players_list:
                    with player.container:
                        player.reveal_hand()

    # display community card based on type of community card and container
    def display_cc(self, cc_type, container):
        card_list_map = {
            "burn_1": self.burn_1, "flop_1": self.flop_1, "flop_2": self.flop_2, "flop_3": self.flop_3, "burn_2": self.burn_2, "turn": self.turn, "burn_3": self.burn_3, "river": self.river,
        }
        with container:
            card = card_list_map[cc_type]
            card_html = f"{card[0]}{Card.suit_convert(card[0].suit)}"
            st.markdown(f"<h2 style='text-align: center;'>{card_html}</h2>", unsafe_allow_html=True)
    
    def update_table(self):
        for player in self.players_list:
            time.sleep(self.card_interval)
            player.reveal_hand()
    
    # create a dictionary using object
    def get_object_dictionary(self, object, stage = None):
        # filter attributes
        excluded_attributes = ['deck', 'cards', 'burnt', 'flop_1', 'flop_2', 'flop_3', 'turn', 'river', 'hand'
                               'game_speed', 'card_interval', 'column', 'container', 'col1_table', 
                               'col2_table', 'col3_table', 'col4_table', 'col5_table', 'col6_table', 'turn_container'
                               , 'river_container', 'burn_container', 'flop_3_container', 'flop_2_container', 'flop_1_container'
                               , 'players', 'players_list']

        # remove certain attributes from list of excluded attributes before each betting stage
        if stage == "pre_flop":
            attributes_to_remove = []
            excluded_attributes = [attr for attr in excluded_attributes if attr not in attributes_to_remove]
            attributes_dict = {key: value for key, value in vars(object).items() if key not in excluded_attributes}
        elif stage == "post_flop":
            attributes_to_remove = ['flop_1', 'flop_2', 'flop_3']
            excluded_attributes = [attr for attr in excluded_attributes if attr not in attributes_to_remove]
            attributes_dict = {key: value for key, value in vars(object).items() if key not in excluded_attributes}
        elif stage == "post_turn":
            attributes_to_remove = ['turn']
            excluded_attributes = [attr for attr in excluded_attributes if attr not in attributes_to_remove]
            attributes_dict = {key: value for key, value in vars(object).items() if key not in excluded_attributes}
        elif stage == "post_river":
            attributes_to_remove = ['river']
            excluded_attributes = [attr for attr in excluded_attributes if attr not in attributes_to_remove]
            attributes_dict = {key: value for key, value in vars(object).items() if key not in excluded_attributes}
        elif stage == "debug":
            excluded_attributes = []
            attributes_dict = {key: value for key, value in vars(object).items() if key not in excluded_attributes}
        else:
            attributes_dict = {key: value for key, value in vars(object).items() if key not in excluded_attributes}

        return attributes_dict
    
    # adds info to a dictionary
    def add_info_to_dict(self, dictionary, info_name, info):
        dictionary[f'{info_name}'] = info
        return dictionary
    
    # god mode
    def god_reveal_hands(self):
        for player in self.players_list:
            time.sleep(self.card_interval)
            player.status = "showdown"
    
    # god mode
    def god_reveal_cc(self):
        self.display_cc("burn_1", self.burn_container) # burn 1
        self.display_cc("flop_1", self.flop_1_container) # flop 1
        self.display_cc("flop_2", self.flop_2_container) # flop 2
        self.display_cc("flop_3", self.flop_3_container) # flop 3
        self.display_cc("burn_2", self.burn_container) # burn 2
        self.display_cc("turn", self.turn_container) # turn
        self.display_cc("burn_3", self.burn_container) # burn 3
        self.display_cc("river", self.river_container) # river


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value}{self.suit}"
    
    @classmethod
    def split_card(cls, card_list):
        cards_str = card_list[0]  
        card1, card2 = cards_str.split(',') 
        return card1, card2

    @staticmethod
    def suit_convert(card_suit):
        if card_suit == "S":
            return "<span style='color: black;'>♠️</span>"
        elif card_suit == "D":
            return "<span style='color: red;'>♦️</span>"
        elif card_suit == "C":
            return "<span style='color: black;'>♣️</span>"
        elif card_suit == "H":
            return "<span style='color: red;'>♥️</span>"

class Deck:
    def __init__(self):
        suits = ['S', 'H', 'C', 'D']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(suit, value) for suit in suits for value in values]
        self.card_back_html = f"""<div style='background-color: white; border: 1px solid black; padding: 2px; border-radius: 6px; display: inline-flex; justify-content: center; align-items: center; margin: 1px; font-size: 28px; text-align: center; width: 48px; height: 67px; position: relative;'>
                                        <div style='background-color: #FF6961; width: 80%; height: 80%; display: flex; justify-content: center; align-items: center; border-radius: 4px;'>
                                            <span style='color: white; font-size: 34px; display: block; transform: translateY(-10%);'>♠</span>
                                        </div>
                                    </div>"""

    def table_emoji(self, emoji):
        emoji_html = f"""<div style='border: 1px solid transparent; padding: 2px; border-radius: 6px; display: inline-flex; justify-content: center; align-items: center; margin: 1px; font-size: 28px; text-align: center; width: 48px; height: 67px; position: relative; background-color: rgba(255, 255, 255, 0);'>
                        <div style='width: 80%; height: 80%; display: flex; justify-content: center; align-items: center; border-radius: 4px;'>
                            <span style='color: black; font-size: 34px; display: block; transform: translateY(-10%);'>{emoji}</span>
                        </div>
                    </div>"""
        return emoji_html

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_cards):
        if len(self.cards) < num_cards:
            raise ValueError("Not enough cards in the deck to deal.")
        return [self.cards.pop() for _ in range(num_cards)]

class PreFlop:
    def __init__ (self, game):
        self.game = game
        self.players = game.players

    def player_betting_round(self):
        another_round_needed = True
        first_iteration = True
        while another_round_needed:
            another_round_needed = False
            for i, player in enumerate(self.players):
                if player.status in ["eliminated", "all-in"]:
                    continue
                if first_iteration and i < 2:
                    continue 
                if player.current_bet < self.game.min_bet:
                    self.player_action(player)
                    another_round_needed = True
            first_iteration = False

    def bet_blinds(self, player_index, blind):
        player = self.players[player_index]
        blind_type = blind
        if blind_type == "small":
            amount = 5
        else:
            amount = 10
        if player.stack >= amount:
            player.stack -= amount
            player.current_bet = amount
            self.game.min_bet = amount
            self.game.pot_total += amount
            print(f"Player {player.id} posts {blind_type} blind of {amount}")
            print(f"Pot is now {self.game.pot_total}")
        else:
            print(f"Player {player.id} does not have enough to post {blind_type} blind")
    
    def check(self, player):
        if player.current_bet == self.game.min_bet:
            print(f"Player {player.id} checks")
        else:
            self.game.num_opponents -= 1
            self.fold(player)
    
    def bet_call(self, player):
        if player.stack >= self.game.min_bet:
            player.stack -= self.game.min_bet
            player.current_bet += self.game.min_bet
            self.game.pot_total += self.game.min_bet
            print(f"Player {player.id} calls")
            print(f"Pot is now {self.game.pot_total}")
        else:
            self.bet_all_in(player)
            print(f"Player {player.id} goes all-in for {player.stack} (Player {player.id} does not have enough to call)")
    
    def bet_raise(self, player, amount):
        if player.stack >= (self.game.min_bet * 2):
            player.stack -= amount # the amount must be >= the current minimum bet
            player.current_bet += amount
            self.game.min_bet = amount
            self.game.pot_total += amount
            print(f"Player {player.id} raises for {amount}")
            print(f"Pot is now {self.game.pot_total}")
        else:
            self.bet_all_in(player)
            print(f"Player {player.id} goes all-in (Player {player.id} does not have enough to raise)")

    def fold(self, player):
        player.bust_out()
        self.game.num_opponents -= 1
        print(f"Player {player.id} folds")

    def bet_all_in(self, player):
        player.all_in
        player.current_bet = player.stack 
        player.stack = 0
        if self.game.min_bet < player.stack:
            self.game.min_bet = player.stack
            self.game.pot_total += player.stack
        elif self.game.min_bet >= player.stack:
            print(f"update logic to add side pot for player {player.player_id}")