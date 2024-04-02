import React, { useState, useEffect } from 'react'; 
import PokerGame from './components/PokerGame';

import logo from './logo.svg';
import './App.css';

function App() {
  // state to store the list of items
  const [items, setItems] = useState([]);

  // simulate fetching data from an API
  useEffect(() => {
    const fetchData = async () => {
      // delay
      await new Promise(resolve => setTimeout(resolve, 1000));

      // simulated fetched data
      const fetchedItems = [
        { id: 1, name: 'Item 1' },
        { id: 2, name: 'Item 2' },
        { id: 3, name: 'Item 3' },
      ];

      setItems(fetchedItems);
    };

    fetchData();
  }, []); // empty array means this effect runs once after initial render

  return (
    <div className="App">
      <header className="App-header">
        <h1>Poker</h1>
          <PokerGame />
        <ul>
          {items.map(item => (
            <li key={item.id}>{item.name}</li>
          ))}
        </ul>
      </header>
    </div>
  );
}

export default App;
