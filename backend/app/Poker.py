import random

class Player:
    def __init__(self, id, is_user=False):
        self.id = id
        self.is_user = is_user
        self.hand = []
        self.status = "active"  # just an example status

    def to_dict(self):
        return {
            'id': self.id,
            'name': f"Player {self.id}",
            'status': self.status
        }

class Deck:
    def __init__(self):
        self.cards = [f"{rank} of {suit}" for suit in ("Hearts", "Diamonds", "Clubs", "Spades")
                      for rank in ("2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace")]
        random.shuffle(self.cards)

    def deal(self, num_cards):
        return [self.cards.pop() for _ in range(num_cards)]

class Game:
    def __init__(self, num_opponents, opp_difficulty):
        self.num_opponents = num_opponents
        self.opp_difficulty = opp_difficulty
        self.players = {str(i): None for i in range(num_opponents + 1)}  # +1 for the user
        self.deck = Deck()

    def start(self):
        # initialize players
        self.players['0'] = Player(id=0, is_user=True)  # player '0' is always the user
        for i in range(1, self.num_opponents + 1):
            self.players[str(i)] = Player(id=i)
        
        # shuffle the deck
        self.deck = Deck()  # reinitialize the deck and shuffle

        # deal cards
        for player in self.players.values():
            if player is not None:
                player.hand = self.deck.deal(2)

        # other initialization tasks begin here:
        return self.to_dict()  # return the initial state of the game

    def to_dict(self):
        # serialize the game state for API response
        return {
            'players': [player.to_dict() for player in self.players.values() if player is not None],
            'difficulty': self.opp_difficulty,
        }

