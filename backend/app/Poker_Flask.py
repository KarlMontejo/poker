from flask import Flask, jsonify, request
from flask_cors import CORS

import redis
import pickle

from Poker import Game

# run flask server:
# cd backend/app
# python3 Poker_Flask.py
# stop redis: sudo service redis-server stop
# start redis: redis-server

app = Flask(__name__)
CORS(app)
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)  # Configure Redis

@app.route('/api/start-game', methods=['POST'])
def start_game():
    try:
        data = request.json
        game = Game(data['num_opponents'], data['opp_difficulty'])
        game_state = game.start()
        r.set('game_state', pickle.dumps(game_state))  # Save the initial state in Redis
        return jsonify(game_state)  # send the initial state back to the frontend
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/player-action', methods=['POST'])
def player_action():
    data = request.json
    game_state = pickle.loads(r.get('game_state'))  # load the latest game state from Redis
    game = Game.from_state(game_state)
    game.player_action(data['player_id'], data['action'])
    game_state = game.to_dict()  # update the game state after the action
    r.set('game_state', pickle.dumps(game_state))  # save the updated state back to Redis
    return jsonify(game_state)

@app.route('/api/save', methods=['POST'])
def save_game():
    game_state = pickle.loads(r.get('game_state'))  # save the latest state
    r.set('game_data', pickle.dumps(game_state))  # save the current state separately as game data
    return jsonify({'status': 'Game saved'})

@app.route('/api/load', methods=['GET'])
def load_game():
    game_data = pickle.loads(r.get('game_data'))
    game = Game.from_state(game_data)
    game_state = game.to_dict()
    r.set('game_state', pickle.dumps(game_state))  # update the main game state with the loaded state
    return jsonify(game_state)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)