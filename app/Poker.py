from utils.lc import opponent_decision_langchain
import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    def __init__(self):
        suits = ['H', 'D', 'C', 'S']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(suit, value) for suit in suits for value in values] # creates a list for cards in the deck with each comb. of suit and value

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_cards):
        return [self.cards.pop() for _ in range(num_cards)]
    
    def burn(self):
        burn_card = [self.cards.pop() for _ in range(1)]
        return burn_card
    
    def reveal_flop(self):
        flop_cards = [self.cards.pop() for _ in range(3)]
        flop_str = ', '.join(str(card) for card in flop_cards)
        print(f"-------------------------------------- [Flop] --------------------------------------")
        print(f"The Flop is: {flop_str}")
        print(f"Community Cards: {flop_str}")
        return flop_cards
    
    def reveal_turn_river(self, type, flop_cards):
        flop_str = ', '.join(str(card) for card in flop_cards)
        turn_str = ""  # Initialize turn_str here

        if type == "Turn":
            turn_card = [self.cards.pop() for _ in range(1)]
            turn_str = ', '.join(str(card) for card in turn_card)
            print(f"-------------------------------------- [{type}] --------------------------------------")
            print(f"The {type} is: {turn_str}")
            print(f"Community Cards: {flop_str}, {turn_str}")
            return turn_card + flop_cards  # Return the updated list of community cards

        elif type == "River":
            river_card = [self.cards.pop() for _ in range(1)]
            river_str = ', '.join(str(card) for card in river_card)
            print(f"-------------------------------------- [{type}] --------------------------------------")
            print(f"The {type} is: {river_str}")
            print(f"Community Cards: {flop_str}, {turn_str}, {river_str}")
            return river_card + flop_cards + [turn_str]  # Return the updated list of community cards
    
class Player:
    def __init__(self, id, is_user = False):
        self.id = id
        self.hand = []
        self.current_bet = 0
        self.status = "active"
        self.is_user = is_user
        self.stack = 1000
        self.player_id = 0
    
    def bust_out(self):
        self.status = "eliminated"

    def all_in(self):
        self.status = "all-in"

    def deal_hand(self, hand):
        self.hand = hand
    
    def show_hand(self):
        return f"{self.hand}"


class Player_Decision:
    def __init__(self, game):
        self.game = game
        self.players = game.players
        self.num_opponents = len(game.players) - 1
        self.user_index = game.user_index
        self.user_options = []
    
    def ask_player(self, player):
        current_player = player 
        if current_player.is_user:
            # print the current situation for the user
            print(f"Your current bet: {current_player.current_bet}")
            print(f"Minimum bet to stay in the game: {self.game.min_bet}")
            print(f"Your stack: {current_player.stack}")
            print(f"Pot total: {self.game.pot_total}")

            # determine the options available to the user
            self.user_options = ['fold']
            if current_player.current_bet < self.game.min_bet:
                self.user_options += ['call', 'raise']
            if current_player.current_bet == self.game.min_bet:
                self.user_options.append('check')
            
            # get user decision
            user_decision = input(f"It's your turn. Here are your options: {self.user_options}\n")
            print(f"You chose: {user_decision}")
            return user_decision

        else:
            # temporary decision logic for non-user players
            chance = random.uniform(0, 1)
            if current_player.current_bet < self.game.min_bet:
                if chance <= 0.10:
                    return "fold"
                elif chance <= 0.60:
                    return "call"
                else:
                    return "raise"
            elif current_player.current_bet == self.game.min_bet:
                if chance <= 0.50:
                    return "check"
                elif chance <= 0.75: 
                    return "call"
                else:
                    return "raise"
                

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
                    

    def player_action(self, player):
        player_decision = Player_Decision(self.game)  # create an instance of User_Decisions
        decision = player_decision.ask_player(player)
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

class Game:
    def __init__(self, num_opponents):
        self.deck = Deck()
        self.num_opponents = num_opponents
        self.user_index = round(self.num_opponents / 2)
        self.players = [Player(i, is_user=(i == self.user_index)) for i in range(1, num_opponents + 2)]
        self.pot_total = 0
        self.sidepots = [0,0,0,0,0,0,0,0,0,0]
        self.min_bet = 0
        self.preflop = PreFlop(self) # pass the game instance to PreFlop class

    def start(self):
        self.deck.shuffle()
        i = 1
        for player in self.players:
            player.player_id = i
            player.deal_hand(self.deck.deal(2))
            i += 1
        print(f"Your cards are: {self.players[self.user_index].show_hand()} and you are seated {self.user_index}th from the dealer")
        self.preflop.start_round()
        

def main():
    # ask user how many players they want
    try:
        num_opponents = int(input("How many players at the table? ")) - 1
        if 2 <= num_opponents <= 10:
            game = Game(num_opponents)
            game.start()
        else:
            print("There must be at least 2 or no more than 10 opponents")
    except ValueError:
        print("Invalid input. Please enter a number.")


# define a new class that checks the end of each round to calculate side pots when necessary or do any other checks to determine how the pot is distributed or see what players are still in