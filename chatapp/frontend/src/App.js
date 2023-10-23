import React, { useState } from 'react';
import './App.css';
import userIcon from './assets/icons/user_icon_40.png';
import botIcon from './assets/icons/robot_icon_40.png';

function App() {
    const [inputMessage, setInputMessage] = useState('');
    const [chatLog, setChatLog] = useState([]);
    const [useAlternateAPI, setUseAlternateAPI] = useState(false);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async () => {
        setInputMessage('');  /* 送信ボタンを押した直後に入力フォームの文字列を消去 */
        setLoading(true);
        try {
            const apiUrl = useAlternateAPI ? 'http://localhost:8000/chat2/' : 'http://localhost:8000/chat/';
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({text: inputMessage}),
            });
            const data = await response.json();
            setChatLog([...chatLog, {from: 'user', message: inputMessage}, {from: 'bot', message: data.text}]);
        } catch (error) {
            console.error("There was an error:", error);
        } finally {
            setLoading(false);
        }
    };


    return (
        <div className="App">
            <div className="headerBar">Broken Chatbot beta</div>
            <div className="chatLog">
                {loading ? (
                    <div className="loading">Loading...</div>
                ) : (
                    chatLog.map((chat, index) => (
                        <div key={index} className={`bubble-container ${chat.from}-container`}>
                            <img src={chat.from === 'user' ? userIcon : botIcon} alt={`${chat.from}_icon`} className="icon" />
                            <div className={`${chat.from}-bubble`}>
                                {chat.message}
                            </div>
                        </div>
                    ))
                )}
            </div>
            <div className="inputArea">
                <input
                    type="text"
                    value={inputMessage}
                    onChange={e => setInputMessage(e.target.value)}
                    placeholder="Send a message"
                />
                <input
                    type="checkbox"
                    checked={useAlternateAPI}
                    onChange={e => setUseAlternateAPI(e.target.checked)}
                />
                <button onClick={handleSubmit}>Send</button>
            </div>
        </div>
    );
}

export default App;
