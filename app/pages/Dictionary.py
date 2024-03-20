import streamlit as st

sim_game_data = {
  "current player (you)": {
    "hand": [
        "7D",
        "9C"
    ],
    "current_bet": 0,
    "status": "active",
    "is_user": False,
    "stack": 1000,
    "id": "8",
    "current game data": {
        "num_opponents": 9,
        "opp_difficulty": "Amateur",
        "game_speed": 5,
        "num_players": 10,
    },
  },
  "player actions": {
    "post flop":{
        "current active players": [1, 3, 5, 6, 8, 9],
        "community cards": ["AH", "7D", "KH"],
        "player 1": {
            "player data": {
                "current_bet": 30,
                "status": "active",
                "is_user": False,
                "stack": 970,
                "id": "1",
            },
            "action": "bet",
            "bet amount": "30",
            "raise amount": "0",
            "decision time": "3s",
        },
        "player 2": {
            "player data": {
                "current_bet": 10,
                "status": "inactive",
                "is_user": False,
                "stack": 990,
                "id": "1",
            },
            "action": "none",
            "bet amount": "10",
            "raise amount": "0",
            "decision time": "none",
        },
        "player 3": {
            "player data": {
                "current_bet": 60,
                "status": "active",
                "is_user": False,
                "stack": 940,
                "id": "3",
            },
            "action": "raise",
            "bet amount": "30",
            "raise amount": "30",
            "decision time": "2s",
        },
        "player 4": {
            "player data": {
                "current_bet": 10,
                "status": "inactive",
                "is_user": False,
                "stack": 990,
                "id": "4",
            },
            "action": "none",
            "bet amount": "10",
            "raise amount": "0",
            "decision time": "none",
        },
        "player 5": {
            "player data": {
                "current_bet": 60,
                "status": "active",
                "is_user": True,
                "stack": 940,
                "id": "3",
            },
            "action": "call",
            "bet amount": "0",
            "raise amount": "0",
            "call amount": "60",
            "decision time": "9s",
        },
        "player 6": {
            "player data": {
                "current_bet": 60,
                "status": "active",
                "is_user": True,
                "stack": 940,
                "id": "3",
            },
            "action": "call",
            "bet amount": "0",
            "raise amount": "0",
            "call amount": "60",
            "decision time": "9s",
        },
        "player 7": {
            "player data": {
                "current_bet": 10,
                "status": "inactive",
                "is_user": False,
                "stack": 990,
                "id": "7",
            },
            "action": "none",
            "bet amount": "10",
            "raise amount": "0",
            "folded" : "no",
            "decision time": "none",
        },
        "player 8": {
            "player data": {
                "current_bet": 10,
                "status": "inactive",
                "is_user": False,
                "stack": 990,
                "id": "8",
            },
            "action": "none",
            "bet amount": "10",
            "raise amount": "0",
            "folded" : "no",
            "decision time": "3s",
        },
        "player 9": {
            "player data": {
                "current_bet": 0,
                "status": "inactive",
                "is_user": False,
                "stack": 100,
                "id": "7",
            },
            "action": "none",
            "bet amount": "10",
            "raise amount": "0",
            "folded" : "yes",
            "decision time": "5s",
        },
        "player 10": {
            "player data": {
                "current_bet": 10,
                "status": "inactive",
                "is_user": False,
                "stack": 990,
                "id": "7",
            },
            "action": "none",
            "bet amount": "10",
            "raise amount": "0",
            "folded" : "no",
            "decision time": "none",
        },
    }
  }
}

st.info('this page just displays and stores a simulated dictionary I made based off of what the structure of game context for langchain will likely be')
st.json(sim_game_data)