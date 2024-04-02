from app.Poker import Player, Game, Card, Deck
from flask import Flask, jsonify, request
from app.Poker import Game, Player, Deck, Card

app = Flask(__name__)

@app.route('/api/start-game', methods=['POST'])
def start_game():
    # Parse request data if needed
    data = request.json

    # Initialize the game with provided parameters
    game = Game(data['num_opponents'], data['opp_difficulty'], data['game_speed'])

    # Start the game and perform any necessary processing
    # For example: game.start()

    # Return the initial game state as JSON
    game_state = {}  # Modify this to return the game state
    return jsonify(game_state)

@app.route('/api/player-action', methods=['POST'])
def player_action():
    # Parse request data if needed
    data = request.json

    # Perform the player action (e.g., fold, call, raise)
    # Update the game state accordingly
    # For example: game.player_action(data['player_id'], data['action'])

    # Return the updated game state as JSON
    game_state = {}  # Modify this to return the updated game state
    return jsonify(game_state)

if __name__ == '__main__':
    app.run(debug=True)