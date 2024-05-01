import React, { useState } from 'react';
import { View, Text, Button, Slider, Picker, StyleSheet } from 'react-native';
import PokerGame from './components/PokerGame';

function App() {
    const [numOpponents, setNumOpponents] = useState(9);
    const [oppDifficulty, setOppDifficulty] = useState('Amateur');
    const [gameStarted, setGameStarted] = useState(false);

    const handleStartGame = () => {
        setGameStarted(true);
    };

    return (
        <View style={styles.app}>
            <Text style={styles.header}>Welcome to the Poker Game!</Text>
            {!gameStarted && (
                <View>
                    <Text>Number of Opponents:</Text>
                    <Slider
                        minimumValue={1}
                        maximumValue={9}
                        step={1}
                        value={numOpponents}
                        onValueChange={(value) => setNumOpponents(parseInt(value))}
                    />
                    <Text>{numOpponents}</Text>
                    <Text>Difficulty:</Text>
                    <Picker
                        selectedValue={oppDifficulty}
                        onValueChange={(itemValue, itemIndex) => setOppDifficulty(itemValue)}
                    >
                        <Picker.Item label="Amateur" value="Amateur" />
                        <Picker.Item label="Intermediate" value="Intermediate" />
                        <Picker.Item label="Expert" value="Expert" />
                    </Picker>
                    <Button title="Start Game" onPress={handleStartGame} />
                </View>
            )}
            {gameStarted && <PokerGame numOpponents={numOpponents} oppDifficulty={oppDifficulty} />}
        </View>
    );
}

const styles = StyleSheet.create({
    app: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        padding: 20,
    },
    header: {
        fontSize: 20,
        fontWeight: 'bold',
    },
});

export default App;
