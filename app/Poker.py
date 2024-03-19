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
        self.stack = 1000
        self.container = None
        self.column = None
        self.id = id
            
    def player_display(self):
        if self.container:
            with self.container:
                if self.hand:  
                    card_displays = [f"{card.value}{Card.suit_convert(card.suit)}" for card in self.hand]
                    cards_html = ''.join(card_displays)
                    player_type = "You" if self.is_user else f"Player {self.id}"
                    st.markdown(f"<h1 style='text-align: center;'>{cards_html}</h1><h5 style='text-align: center;'>{player_type}</h5>", unsafe_allow_html=True)

    def show_hand(self):
        if self.hand:
            card_displays = [f"{card.value}{Card.suit_convert(card.suit)}" for card in self.hand]
            cards_html = ''.join(card_displays)
            hand_html = f"<h1 style='text-align: center;'>{cards_html}</h1>"
        return hand_html
        
    def bust_out(self):
        self.status = "eliminated"

    def all_in(self):
        self.status = "all-in"

class Game():
    def __init__(self, num_opponents, opp_difficulty, game_speed):
        self.deck = Deck()
        self.deck.shuffle()
        self.num_opponents = num_opponents
        self.opp_difficulty = opp_difficulty
        self.game_speed = game_speed
        self.num_players = num_opponents + 1
        self.card_interval = 2 + (0.1 - 2) * ((self.game_speed - 1) / (5 - 1))
        st.header("Table")
        st.markdown(f"<h1 style='text-align: center;'>DEALER</h1>", unsafe_allow_html=True)
        self.col1_table,self.col2_table,self.col3_table,self.col4_table,self.col5_table,self.col6_table = st.columns(6)
        self.players = {
            '0': None,
            '1': None,
            '2': None,
            '3': None,
            '4': None,
            '5': Player(is_user=True),
            '6': None,
            '7': None,
            '8': None,
            '9': None
        }
        self.positions_list = []
        self.create_players()

    def create_players(self):
        # create opponents
        create_opponents = {
            "1" : [0],
            "2" : [1,8],
            "3" : [1,4,8],
            "4" : [0,4,7,9],
            "5" : [0,2,4,7,9],
            "6" : [0,2,4,6,7,9],
            "7" : [0,2,3,4,6,7,9],
            "8" : [0,1,2,3,4,6,7,9],
            "9" : [0,1,2,3,4,6,7,8,9]
        }

        opponent_id = 1
        opponents_map = create_opponents[str(self.num_opponents)]
        for opponent_idx in opponents_map:
            if opponent_idx > 5 and not self.players['5'].id:
                self.players['5'].id = opponent_id
                opponent_id += 1
            self.players[str(opponent_idx)] = Player(id=str(opponent_id))
            opponent_id += 1

    def init_community_cards(self, cc_type):
        container_mapping = {
            "flop_1": self.col1_table.empty(),
            "flop_2": self.col2_table.empty(),
            "flop_3": self.col3_table.empty(),
            "burn": self.col4_table.empty(),
            "turn": self.col5_table.empty(),
            "river": self.col6_table.empty(),
        }

        target_container = container_mapping[cc_type]
        with target_container:
            st.markdown(f"<h1 style='text-align: center;'>&nbsp;</h1>", unsafe_allow_html=True)
        return target_container

    def display_community_cards(self, cc_type, container):
        card_list_map = {
            "flop_1": self.deck.flop,
            "flop_2": self.deck.flop,
            "flop_3": self.deck.flop,
            "burn": self.deck.burnt,
            "turn": self.deck.turn,
            "river": self.deck.river,
        }
        if cc_type in ["turn", "river", "flop_1", "flop_2", "flop_3"]:
            card = self.deck.reveal_community_card()[0] 
            card_list = card_list_map[cc_type]
            card_list.append(card)
            with container:
                card_html = f"{card.value}{Card.suit_convert(card.suit)}"
                time.sleep(self.card_interval)
                st.markdown(f"<h1 style='text-align: center;'>🃏</h1>", unsafe_allow_html=True)
                time.sleep(self.card_interval)
                st.markdown(f"<h1 style='text-align: center;'>{card_html}</h1>", unsafe_allow_html=True)
        elif cc_type == "burn":
            card = self.deck.burn()
            card_list = card_list_map[cc_type]
            card_list.append(card)
            with container:
                time.sleep(self.card_interval)
                st.markdown(f"<h1 style='text-align: center;'>🃏</h1>", unsafe_allow_html=True)
                time.sleep(self.card_interval)
                st.markdown(f"<h1 style='text-align: center;'>🔥</h1>", unsafe_allow_html=True)
                time.sleep(self.card_interval)
                st.markdown(f"<h1 style='text-align: center;'>💨</h1>", unsafe_allow_html=True)
                time.sleep(self.card_interval)
                st.markdown(f"<h1 style='text-align: center;'>&nbsp;</h1>", unsafe_allow_html=True)

    def display_table(self):
        # standardized pixel spacing
        px_xl = "250"
        px_lg = "110"
        px_md = "100" # must be <= 90
        px_sm = "20"
        px_zo = "0"

        squares = {}
        def display_position(column, pixel_1, pixel_2, square_pos):
            nonlocal squares
            column.markdown(f"<div style='height: {pixel_1}px;'>&nbsp;</div>", unsafe_allow_html=True)
            squares[square_pos] = column.empty()
            column.markdown(f"<div style='height: {pixel_2}px;'>&nbsp;</div>", unsafe_allow_html=True)

        # table positions
        display_position(self.col5_table, px_zo, px_lg, 1)
        self.turn_container = self.init_community_cards("turn")
        display_position(self.col6_table, px_md, px_sm, 2) 
        self.river_container = self.init_community_cards("river")
        display_position(self.col6_table, px_sm, px_zo, 3) 
        display_position(self.col5_table, px_lg, px_zo, 4) 
        self.col4_table.markdown(f"<div style='height: {px_xl}px;'>&nbsp;</div>", unsafe_allow_html=True)
        self.burn_container = self.init_community_cards("burn")
        display_position(self.col4_table, px_xl, px_zo, 5)
        self.col3_table.markdown(f"<div style='height: {px_xl}px;'>&nbsp;</div>", unsafe_allow_html=True)
        self.flop_3_container = self.init_community_cards("flop_3")
        display_position(self.col3_table, px_xl, px_zo, 6) 
        display_position(self.col2_table, px_zo, px_lg, 10) 
        self.flop_2_container = self.init_community_cards("flop_2")
        display_position(self.col2_table, px_lg, px_zo, 7) 
        display_position(self.col1_table, px_md, px_sm, 9) 
        self.flop_1_container = self.init_community_cards("flop_1")
        display_position(self.col1_table, px_sm, px_zo, 8) 

        for key, value in squares.items():
            if self.players[str(int(key)-1)]:
                player = self.players[str(int(key)-1)]
                player.player_display()
                player.container = value
                time.sleep(self.card_interval)

    def deal_players(self):
        players_list = [player for player in self.players.values() if player]
        for _ in range(2):
            for player in players_list:
                dealt_cards = self.deck.deal(1)
                player.hand += dealt_cards
        for player in players_list:
            with player.container:
                st.markdown(f"<h1 style='text-align: center;'>&nbsp;</h1>", unsafe_allow_html=True)
        for player in players_list:
            with player.container:
                player_type = "You" if player.is_user else f"Player {player.id}"
                time.sleep(self.card_interval)
                st.markdown(f"<h1 style='text-align: center;'>✋🤚</h1><h5 style='text-align: center;'>{player_type}</h5>", unsafe_allow_html=True)
        for player in players_list:
            with player.container:
                player_type = "You" if player.is_user else f"Player {player.id}"
                time.sleep(self.card_interval)
                st.markdown(f"<h1 style='text-align: center;'>🃏🤚</h1><h5 style='text-align: center;'>{player_type}</h5>", unsafe_allow_html=True)
        for player in players_list:
            with player.container:
                player_type = "You" if player.is_user else f"Player {player.id}"
                time.sleep(self.card_interval)
                st.markdown(f"<h1 style='text-align: center;'>🃏🃏</h1><h5 style='text-align: center;'>{player_type}</h5>", unsafe_allow_html=True)

    def empty_player_containers(self):
        players_list = [player for player in self.players.values() if player]
        for player in players_list:
            with player.container:
                st.empty()
        self.col4_table.empty()
        self.col3_table.empty()

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
        self.flop = []
        self.turn = []
        self.river = []
        self.burnt = []

        self.cards = [Card(suit, value) for suit in suits for value in values]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_cards):
        if len(self.cards) < num_cards:
            raise ValueError("Not enough cards in the deck to deal.")
        return [self.cards.pop() for _ in range(num_cards)]

    def burn(self):
        burnt_card = self.cards.pop()
        return burnt_card
    
    def reveal_community_card(self):
        community_card = self.deal(1)
        return community_card

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