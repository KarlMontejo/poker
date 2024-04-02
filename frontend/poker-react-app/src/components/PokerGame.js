import React, { useState, useEffect } from 'react';

function PokerGame() {
  const [gameState, setGameState] = useState(null);

  useEffect(() => {
    // fetch initial game state when component mounts
    fetch('/api/start-game', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        num_opponents: 3,
        opp_difficulty: 'medium',
        game_speed: 'normal'
      })
    })
    .then(response => response.json())
    .then(data => setGameState(data))
    .catch(error => console.error('Error:', error));
  }, []);

  const handlePlayerAction = (action) => {
    // make API request to perform player action
    fetch('/api/player-action', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        player_id: 1, // player ID
        action: action // player action (fold, check, call, bet, raise)
      })
    })
    .then(response => response.json())
    .then(data => setGameState(data))
    .catch(error => console.error('Error:', error));
  };

  return (
    <div>
      {/* render game state and UI based on the gameState */}
      <button onClick={() => handlePlayerAction('fold')}>Fold</button>
      <button onClick={() => handlePlayerAction('call')}>Call</button>
      <button onClick={() => handlePlayerAction('raise')}>Raise</button>
    </div>
  );
}

export default PokerGame;

