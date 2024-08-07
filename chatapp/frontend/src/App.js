import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import userIcon from './assets/icons/user_icon_40.png';
import botIcon from './assets/icons/robot_icon_40.png';
import loadingAnimation from './assets/animations/three-dots.svg';

function App() {
    const hostname = process.env.REACT_APP_HOST_NAME;
    const [inputMessage, setInputMessage] = useState('');
    const [chatLog, setChatLog] = useState([]);
    const [apiUrl, setApiUrl] = useState(`http://${hostname}:8000/prompt-leaking-lv1/`);
    const [botIsTyping, setBotIsTyping] = useState(false);
    const chatLogRef = useRef(null);

    useEffect(() => {
        if (chatLogRef.current) {
            chatLogRef.current.scrollTop = chatLogRef.current.scrollHeight;
        }
    }, [chatLog]);

    const handleSubmit = async () => {
        const newChatLog = [...chatLog, {from: 'user', message: inputMessage}, {from: 'bot', message: 'loading'}];
        setChatLog(newChatLog);
        setInputMessage('');
        setBotIsTyping(true);
        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({text: inputMessage}),
            });
            const data = await response.json();
            const updatedChatLog = [...newChatLog];
            updatedChatLog[updatedChatLog.length - 1].message = data.text;
            setChatLog(updatedChatLog);
        } catch (error) {
            console.error("There was an error:", error);
        } finally {
            setBotIsTyping(false);
        }
    };


    return (
        <div className="App">
            <div className="headerBar">Broken Chatbot beta</div>
            <div className="chatLog" ref={chatLogRef}>
                {chatLog.map((chat, index) => (
                    <div key={index} className={`bubble-container ${chat.from}-container`}>
                        <img src={chat.from === 'user' ? userIcon : botIcon} alt={`${chat.from}_icon`} className="icon" />
                        <div className={`${chat.from}-bubble`}>
                            {chat.from === 'bot' && botIsTyping && index === chatLog.length - 1 ? (
                                <img src={loadingAnimation} alt="Loading..." />
                                ) : (
                                    chat.message
                            )}
                        </div>
                    </div>
                    )
                )}
            </div>
            <div className="inputArea">
                <input
                    type="text"
                    value={inputMessage}
                    onChange={e => setInputMessage(e.target.value)}
                    placeholder="Send a message"
                />
                <select
                    value={apiUrl}
                    onChange={e => setApiUrl(e.target.value)}
                >
                    <option value={`http://${hostname}:8000/prompt-leaking-lv1/`}>Leak Lv.1</option>
                    <option value={`http://${hostname}:8000/p2sql-injection-lv1/`}>SQLi Lv.1</option>
                    <option value={`http://${hostname}:8000/p2sql-injection-lv2/`}>SQLi Lv.2</option>
                    <option value={`http://${hostname}:8000/llm4shell-lv1/`}>LLM4Shell Lv.1</option>
                    <option value={`http://${hostname}:8000/llm4shell-lv2/`}>LLM4Shell Lv.2</option>
                </select>
                <button onClick={handleSubmit}>Send</button>
            </div>
        </div>
    );
}

export default App;
