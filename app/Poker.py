from utils.lc import opponent_decision_langchain
import streamlit as st
import math
import random

class Player:
    def __init__(self, id, is_user=False):
        self.hand = []
        self.current_bet = 0
        self.status = "active"
        self.is_user = is_user
        self.stack = 1000
        self.id = id
        self.container = None
        self.column = None
    
    def player_display(self):
        st.markdown(f"<h1 style='text-align: center;'>{self.hand}</h1>", unsafe_allow_html=True)
        if self.is_user:
            st.markdown(f"<h5 style='text-align: center;'>You</h5>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h5 style='text-align: center;'>Player {self.id}</h5>", unsafe_allow_html=True)

    def bust_out(self):
        self.status = "eliminated"

    def all_in(self):
        self.status = "all-in"

class Game():
    def __init__(self, num_opponents, opp_difficulty):
        self.deck = Deck()
        self.num_opponents = num_opponents
        self.opp_difficulty = opp_difficulty
        self.num_players = num_opponents + 1
        self.players = {
            '0': None,
            '1': None,
            '2': None,
            '3': None,
            '4': None,
            '5': Player(6, is_user=True),
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
            "2" : [0,9],
            "3" : [0,4,8],
            "4" : [0,4,7,9],
            "5" : [0,2,4,6,9],
            "6" : [0,2,4,6,7,9],
            "7" : [0,2,3,4,6,7,9],
            "8" : [0,1,2,3,4,6,7,9],
            "9" : [0,1,2,3,4,6,7,8,9]
        }

        opponents_map = create_opponents[str(self.num_opponents)]
        for opponent_idx in opponents_map:
            self.players[str(opponent_idx)] = Player(id=str(opponent_idx+1))
    
    def display_table(self):
        # table
        st.header("Table")
        st.markdown(f"<h1 style='text-align: center;'>DEALER</h1>", unsafe_allow_html=True)

        # create a row of columns for the cards
        col1_table,col2_table,col3_table,col4_table,col5_table,col6_table = st.columns(6)
        
        # standardized pixel spacing
        px_xl = "440"
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

        display_position(col5_table, px_zo, px_lg, 1)
        display_position(col6_table, px_md, px_sm, 2) 
        display_position(col6_table, px_sm, px_zo, 3) 
        display_position(col5_table, px_lg, px_zo, 4) 
        display_position(col4_table, px_xl, px_zo, 5) 
        display_position(col3_table, px_xl, px_zo, 6) 
        display_position(col2_table, px_zo, px_lg, 10) 
        display_position(col2_table, px_lg, px_zo, 7) 
        display_position(col1_table, px_md, px_sm, 9) 
        display_position(col1_table, px_sm, px_zo, 8) 

        st.expander('debug').json(self.players)

        for key, value in squares.items():
            with value:
                if self.players[str(int(key)-1)]:
                    player = self.players[str(int(key)-1)]
                    player.player_display()
                else:
                    st.markdown(f"<h1 style='text-align: center;'>&nbsp</h1>", unsafe_allow_html=True)
                    st.markdown(f"<h5 style='text-align: center;'>&nbsp</h5>", unsafe_allow_html=True)

    def deal_players(self):
        players_list = [player for player in self.players.values() if player]
        for player in players_list:
            dealt_cards = self.deck.deal(2)
            player.hand.append(dealt_cards)

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value}{self.suit}"
    
    @classmethod
    def split_card(cls,cards_str):
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

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_cards):
        if len(self.cards) < num_cards:
            raise ValueError("Not enough cards in the deck to deal.")
        return [self.cards.pop() for _ in range(num_cards)]

    def burn(self):
        return self.cards.pop()

    def reveal_flop(self):
        return self.deal(3)
    
    def reveal_turn_or_river(self):
        return self.deal(1)

class PreFlop:
    def __init__ (self, game):
        self.game = game
        self.players = game.players

    def start_round(self):
        
        # preflop
        self.bet_blinds(0,"small")
        self.bet_blinds(1,"big")
        self.player_betting_round()

        # flop
        flop_cards = self.game.deck.reveal_flop()
        self.player_betting_round()

        # turn
        self.game.deck.burn()
        turn_and_flop_cards = self.game.deck.reveal_turn_river("Turn", flop_cards)
        self.player_betting_round()

        # river
        self.game.deck.burn()
        self.game.deck.reveal_turn_river("River", turn_and_flop_cards)
        self.player_betting_round()

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