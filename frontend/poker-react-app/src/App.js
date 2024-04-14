import React, { useState } from 'react';
import PokerGame from './components/PokerGame';
import './App.css';

// run react app:
// cd frontend/poker-react-app
// npm start

function App() {
    const [numOpponents, setNumOpponents] = useState(9);
    const [oppDifficulty, setOppDifficulty] = useState('Amateur');
    const [gameStarted, setGameStarted] = useState(false);

    const handleStartGame = () => {
        setGameStarted(true);
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>Welcome to the Poker Game!</h1>
                {!gameStarted && (
                    <div>
                        <label>
                            Number of Opponents:
                            <input type="range" min="1" max="9" value={numOpponents}
                                onChange={(e) => setNumOpponents(e.target.value)} />
                            {numOpponents}
                        </label>
                        <label>
                            Difficulty:
                            <select value={oppDifficulty} onChange={(e) => setOppDifficulty(e.target.value)}>
                                <option value="Amateur">Amateur</option>
                                <option value="Intermediate">Intermediate</option>
                                <option value="Expert">Expert</option>
                            </select>
                        </label>
                        <button onClick={handleStartGame}>Start Game</button>
                    </div>
                )}
                {gameStarted && <PokerGame numOpponents={numOpponents} oppDifficulty={oppDifficulty} />}
            </header>
        </div>
    );
}

export default App;
