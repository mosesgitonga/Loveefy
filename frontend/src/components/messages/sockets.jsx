import React, { useState, useEffect } from "react";
import io from "socket.io-client";

const PrivateMessage = () => {
    const [message, setMessage] = useState("");
    const [socket, setSocket] = useState(null);

    useEffect(() => {
        // Initialize the socket connection only once
        const newSocket = io.connect('https://www.loveefy.africa', {
            query: { token: sessionStorage.getItem('access_token') }
        });   

        newSocket.on('connect', () => {
            console.log('connected to the server');
        });

        
        newSocket.on('disconnect', () => {
            console.log('Disconnected from server');
        });
        
        newSocket.on('error', (error) => {
            console.log('Error:', error);
        });

        setSocket(newSocket);

        // Cleanup the socket connection on unmount
        return () => {
            newSocket.disconnect();
        };
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (message.trim() && socket) {
            // Emit the message to the server
            socket.emit('private_message', { message });
            setMessage(""); // Clear the input field
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Type a message"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                />
                <button type="submit">Submit</button>
            </form>
        </div>
    );
};

export default PrivateMessage;
