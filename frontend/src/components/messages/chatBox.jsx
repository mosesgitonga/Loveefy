import React, { useState, useEffect, useRef } from "react";
import { useParams } from 'react-router-dom';
import io from 'socket.io-client';
import "./chatBox.css";
import api from "../api/axios";
import Sidebar from "../discovery/SideBar";

const useSocket = (roomId, username) => {
    const [socket, setSocket] = useState(null);

    useEffect(() => {
        const access_token = sessionStorage.getItem('access_token');
        if (!access_token) {
            console.log('No access token found');
            return;
        }
        const socketIo = io('http://localhost:5000', {
            extraHeaders: {
                Authorization: `Bearer ${access_token}`
            },
            transports: ['websocket'],
        });

        socketIo.on('connect_error', (error) => {
            console.error('Connection Error:', error.message);
        });

        socketIo.on('connect', () => {
            console.log('Socket connected');
            console.log('room', roomId)
            socketIo.emit('join_room', { room_id: roomId, username });
        });

        setSocket(socketIo);

        return () => {
            socketIo.emit('leave_room', { room_id: roomId, username });
            socketIo.disconnect();
        };
    }, [roomId, username]);

    return socket;
};

const ChatBox = () => {
    const { roomId } = useParams();
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState("");
    const currentUsername = sessionStorage.getItem('currentUsername');
    const access_token = sessionStorage.getItem('access_token');
    const endOfMessagesRef = useRef(null);
    const socket = useSocket(roomId, currentUsername);
    console.log('socket', socket)

    useEffect(() => {
        const fetchMessages = async () => {
            try {
                const response = await api.get('/api/v1/messages', {
                    params: { roomId, page: 1, per_page: 50 }
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
        if (socket) {
            socket.on('receive_message', (message) => {
                setMessages((prevMessages) => [...prevMessages, message]);
            });
        }
    }, [socket]);

    useEffect(() => {
        if (endOfMessagesRef.current) {
            endOfMessagesRef.current.scrollIntoView({ behavior: "smooth" });
        }
    }, [messages]);

    const sendMessage = () => {
        if (socket && inputMessage.trim()) {
            const messageData = {
                room_id: roomId,
                content: inputMessage,
                username: currentUsername,
                token: access_token,
            };
            setMessages((prev) => [...prev, messageData]);
            socket.emit('send_message', messageData);
            setInputMessage(""); 
        }
    };

    return (
        <div className="chat-container">
            <Sidebar className="sidebar"/>
            <div className="chatBox">
                <div className="messages">
                    {messages.length > 0 ? (
                        messages.map((msg, index) => (
                            <div 
                                key={index} 
                                className={`message ${msg.username === currentUsername ? 'sender' : 'receiver'}`}
                            >
                                <strong>{msg.time || msg.timestamp}<br/>{msg.username}</strong> {msg.content}
                            </div>
                        ))
                    ) : (
                        <p>Loading...</p>
                    )}
                    <div ref={endOfMessagesRef} />
                </div>
                <div className="send">
                    <textarea
                        type="text"
                        value={inputMessage}
                        onChange={(e) => setInputMessage(e.target.value)}
                        placeholder="Type your message..."
                        style={{ minHeight: '50px', resize: 'none' }} 
                    />
                    <button onClick={sendMessage}>Send</button>
                </div>
            </div>
        </div>
    );
};

export default ChatBox;
