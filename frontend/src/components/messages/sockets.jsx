import React, { useState, useEffect } from "react";
import { useSocket } from './socketContext'; 

const PrivateMessage = () => {
    const [message, setMessage] = useState("");
    const socket = useSocket(); 

    const handleSubmit = (e) => {
        e.preventDefault();
        if (message.trim() && socket) {
            console.log(message);
            socket.emit('private_message', { message });
            setMessage(""); 
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <textarea
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
