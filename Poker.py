# Poker
# Version: 1.0
# Fully Working?: No

import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    def __init__(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        self.cards = [Card(suit, value) for suit in suits for value in values] # creates a list for cards in the deck with each comb. of suit and value

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_cards):
        return [self.cards.pop() for _ in range(num_cards)]
    
class Player:
    def __init__(self, id, is_user = False):
        self.id = id
        self.hand = []
        self.current_bet = 0
        self.status = "active"
        self.is_user = is_user
        self.stack = 1000
    
    def bust_out(self):
        self.status = "eliminated"

    def deal_hand(self, hand):
        self.hand = hand
    
    def show_hand(self):
        return f"{self.hand}"

class Chance: # temporary randomizer to simulate the random decisions of players (this will later be replaced by AI-driven decision making)
    @staticmethod
    def get_random_value():
        chance = random.uniform(0, 1)
        if chance <= 0.10:  # 10% chance
            return "fold"
        elif chance <= 0.50:  # additional 40% chance
            return "check"
        elif chance <= 0.75:  # additional 25% chance
            return "call"
        else:
            return "raise"


class User_Decision:
    def __init__(self, game):
        self.game = game
        self.players = game.players
        self.num_opponents = len(game.players) - 1
        self.user_index = game.user_index
        self.user_options = []
    
    def ask_user(self):
        player = self.players[self.user_index]
        if player.current_bet == self.game.min_bet: # add option to check if user's current bet matches the minimum bet
            self.user_options.append("check")
        if player.current_bet <= self.game.min_bet: # add options to call raise and fold if user's current bet is lower than the minimum bet
            self.user_options.append("call")
            self.user_options.append("raise")
            self.user_options.append("fold")
        user_decision = input(f"It's on you, here are your options: \n {self.user_options} \n")
        print(f"You chose: {user_decision}")

class PreFlop:
    def __init__ (self, game):
        self.game = game
        self.players = game.players

    def start_round(self):
        
        # begin round with small and big blinds
        self.bet_blinds(0,"small")
        self.bet_blinds(1,"big")

        another_round_needed = True # flag to track if another betting round is needed

        while another_round_needed:
            another_round_needed = False
            for player in self.players:
                if player.status == "eliminated":
                    continue
                if player.current_bet < self.game.min_bet: # check if the player needs to make a decision
                    self.player_action(player)
                    another_round_needed = True

    def player_action(self, player):
        user_decision = User_Decision(self.game)  # create an instance of User_Decisions
        decision = Chance.get_random_value()
        if player.is_user == True:
            user_decision.ask_user()
        else:
            if decision == "fold":
                self.fold(player)
            elif decision == "check":
                self.check(player)
            elif decision == "call":
                self.bet_call(player)
            elif decision == "raise":
                self.bet_raise(player, self.game.min_bet * 2)

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
            print(f"player {player.id} checks")
        else:
            self.game.num_opponents -= 1
            print(f"player {player.id} folds")
    
    def bet_call(self, player):
        if player.stack >= self.game.min_bet:
            player.stack -= self.game.min_bet
            player.current_bet += self.game.min_bet
            self.game.pot_total += self.game.min_bet
            print(f"Player {player.id} calls")
            print(f"Pot is now {self.game.pot_total}")
        else:
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
            print(f"Player {player.id} goes all-in (Player {player.id} does not have enough to raise)")

    def fold(self, player):
        player.bust_out()
        self.game.num_opponents -= 1
        print(f"Player {player.id} folds")

class Game:
    def __init__(self, num_opponents):
        self.deck = Deck()
        self.num_opponents = num_opponents
        self.user_index = round(self.num_opponents / 2)
        self.players = [Player(i, is_user=(i == self.user_index)) for i in range(1, num_opponents + 2)]
        self.pot_total = 0
        self.min_bet = 0
        self.preflop = PreFlop(self) # pass the game instance to PreFlop class

    def start(self):
        self.deck.shuffle()
        for player in self.players:
            player.deal_hand(self.deck.deal(2))
        print(f"Your cards are: {self.players[self.user_index].show_hand()} and you are seated {self.user_index}th from the dealer")
        self.preflop.start_round()
        

def main():
    # ask user how many players they want
    try:
        num_opponents = int(input("How many players at the table? "))
        if 2 <= num_opponents <= 10:
            game = Game(num_opponents)
            game.start()
        else:
            print("There must be at least 2 or no more than 10 opponents")
    except ValueError:
        print("Invalid input. Please enter a number.")
    

# run the game
if __name__ == "__main__":
    main()