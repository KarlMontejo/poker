from utils.lc import opponent_decision_langchain
import streamlit as st
import math
import random

class Player:
    def __init__(self, id, deck, is_user=False):
        self.id = id
        self.hand = []
        self.current_bet = 0
        self.status = "active"
        self.is_user = is_user
        self.stack = 1000
        self.player_id = id
        self.container = None
        self.column = None
        self.deck = deck
    
    def deal(self):
        self.hand = self.deck.deal(2)
        return self.hand

    
    def bust_out(self):
        self.status = "eliminated"

    def all_in(self):
        self.status = "all-in"

class Game():
    def __init__(self, deck, num_opponents, opp_difficulty):
        self.deck = deck
        self.num_opponents = num_opponents
        self.opp_difficulty = opp_difficulty
        self.num_players = num_opponents + 1
        self.players = []
        self.create_players()

    def create_players(self):
        # create the user as player 0
        self.players.append(Player(id=0, deck = self.deck, is_user=True))
        # create opponents
        for i in range(1, self.num_opponents + 1):
            self.players.append(Player(id=i, deck = self.deck, is_user=False))
        return self.players
    
    def deal_players(self):
        for player in self.players:
            player.deck.deal(2)


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