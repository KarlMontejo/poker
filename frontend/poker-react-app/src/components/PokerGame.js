import React, { useState, useEffect } from 'react';

function PokerGame({ numOpponents, oppDifficulty }) {
    const [gameState, setGameState] = useState(null);

    useEffect(() => {
        console.log("Fetching game data...");
        fetch('/api/start-game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                num_opponents: numOpponents,
                opp_difficulty: oppDifficulty,
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log("Data received:", data);
            setGameState(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }, [numOpponents, oppDifficulty]);

    const handlePlayerAction = (id, action) => {
        console.log(`Player ${id} action: ${action}`);
        fetch('/api/player-action', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                player_id: id,
                action: action 
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Action data received:", data);
            setGameState(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    };

    return (
        <div className="poker-table">
            <div className="players">
                {gameState && gameState.players ? (
                    gameState.players.map((player, index) => (
                        <div key={index} className="player">
                            <p>Player {player.id}: {player.name}</p>
                            <p>Status: {player.status}</p>
                        </div>
                    ))
                ) : (
                    <p>Loading players...</p>
                )}
            </div>
            <div className="actions">
                <button onClick={() => handlePlayerAction(0, 'fold')}>Fold</button>
                <button onClick={() => handlePlayerAction(0, 'call')}>Call</button>
                <button onClick={() => handlePlayerAction(0, 'raise')}>Raise</button>
            </div>
        </div>
    );
}

export default PokerGame;
