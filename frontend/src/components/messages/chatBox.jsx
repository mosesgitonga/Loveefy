import React, { useState, useEffect, useRef } from "react";
import { useParams } from 'react-router-dom';
import { useSocket } from "./socketContext.jsx"; // Import the useSocket hook
import "./chatBox.css";
import api from "../api/axios";
import Sidebar from "../discovery/SideBar";
import InitiatedChats from "./initiatedChats";

const ChatBox = () => {
    const { roomId } = useParams();
    const socket = useSocket(); // Use the socket from context
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState("");
    const currentUsername = sessionStorage.getItem('currentUsername');
    const endOfMessagesRef = useRef(null);

    useEffect(() => {
        if (socket) {
            socket.emit('join_room', { room_id: roomId, username: currentUsername });

            socket.on('receive_message', (message) => {
                setMessages(prevMessages => [...prevMessages, message]);
            });

            return () => {
                socket.emit('leave_room', { room_id: roomId, username: currentUsername });
                socket.off('receive_message'); // Clean up the event listener
            };
        }
    }, [socket, roomId, currentUsername]);

    useEffect(() => {
        const fetchMessages = async () => {
            try {
                const response = await api.get('/api/v1/messages', {
                    params: { roomId: roomId, page: 1, per_page: 50 }
                });
                if (response.data && Array.isArray(response.data.messages)) {
                    setMessages(response.data.messages);
                } else {
                    console.error('Unexpected response format:', response.data);
                }
            } catch (error) {
                console.error('Error fetching messages:', error);
            }
        };
        fetchMessages();
    }, [roomId]);

    useEffect(() => {
        if (endOfMessagesRef.current) {
            endOfMessagesRef.current.scrollIntoView({ behavior: "smooth" });
        }
    }, [messages]);

    const sendMessage = () => {
        if (socket && inputMessage.trim()) {
            socket.emit('send_message', {
                room_id: roomId,
                content: inputMessage,
                username: currentUsername
            });
            setInputMessage("");
        }
    };

    return (
        <div className="chat-container">
            <Sidebar className="sidebar"/>
            <div className="chatBox">
                <div className="messages">
                    {Array.isArray(messages) && messages.length > 0 ? (
                        messages.map((msg, index) => (
                            <div 
                                key={index} 
                                className={`message ${msg.username === currentUsername ? 'sender' : 'receiver'}`}
                            >
                                <strong>{msg.time}{msg.timestamp}<br/>{msg.username}</strong> {msg.content}
                            </div>
                        ))
                    ) : (
                        <p>Loading...</p>
                    )}
                    <div ref={endOfMessagesRef} />
                </div>
                <div className="send">
                    <input
                        type="text"
                        value={inputMessage}
                        onChange={(e) => setInputMessage(e.target.value)}
                        placeholder="Type your message..."
                    />
                    <button onClick={sendMessage}>Send</button>
                </div>
            </div>
        </div>
    );
};

export default ChatBox;
