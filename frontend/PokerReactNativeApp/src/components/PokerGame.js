import React, { useState, useEffect } from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

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
        <View style={styles.pokerTable}>
            <View style={styles.players}>
                {gameState && gameState.players ? (
                    gameState.players.map((player, index) => (
                        <View key={index} style={styles.player}>
                            <Text>Player {player.id}: {player.name}</Text>
                            <Text>Status: {player.status}</Text>
                        </View>
                    ))
                ) : (
                    <Text>Loading players...</Text>
                )}
            </View>
            <View style={styles.actions}>
                <Button title="Fold" onPress={() => handlePlayerAction(0, 'fold')} />
                <Button title="Call" onPress={() => handlePlayerAction(0, 'call')} />
                <Button title="Raise" onPress={() => handlePlayerAction(0, 'raise')} />
            </View>
        </View>
    );
}
