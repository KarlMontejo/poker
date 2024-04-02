from utils.lc import opponent_decision_langchain
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


class Game():
    def __init__(self, num_opponents, opp_difficulty, game_speed):

        # parameters and attributes
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