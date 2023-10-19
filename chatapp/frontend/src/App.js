import React, { useState } from 'react';
import './App.css';

function App() {
  const [inputMessage, setInputMessage] = useState('');
  const [chatLog, setChatLog] = useState([]);
  const [useAlternateAPI, setUseAlternateAPI] = useState(false);

  const handleSubmit = async () => {
    try {
      const apiUrl = useAlternateAPI ? 'http://localhost:8000/chat2/' : 'http://localhost:8000/chat/';
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputMessage }),
      });
      const data = await response.json();
      setChatLog([...chatLog, { from: 'user', message: inputMessage }, { from: 'bot', message: data.text }]);
      setInputMessage('');
    } catch (error) {
      console.error("There was an error:", error);
    }
  };

  return (
    <div className="App">
      <div className="chatLog">
        {chatLog.map((chat, index) => (
          <div key={index} className={chat.from}>
            {chat.message}
          </div>
        ))}
      </div>
      <div className="inputArea">
        <input
          value={inputMessage}
          onChange={e => setInputMessage(e.target.value)}
          placeholder="メッセージを送信"
        />
        <input
          type="checkbox"
          checked={useAlternateAPI}
          onChange={e => setUseAlternateAPI(e.target.checked)}
        />
        <button onClick={handleSubmit}>送信</button>
      </div>
    </div>
  );
}

export default App;
