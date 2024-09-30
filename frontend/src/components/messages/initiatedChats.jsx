import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./initiatedChats.css";
import api from "../api/axios";

import Sidebar from "../discovery/SideBar";

const InitiatedChats = () => {
    const [rooms, setRooms] = useState(null);
    const navigate = useNavigate();   

    useEffect(() => {
        const fetchRooms = async () => {
            try {
                const response = await api.get('/api/v1/rooms');
                if (response.status === 200) {
                    // Sort the rooms by the updated_at key, latest first
                    const sortedRooms = response.data.sort((a, b) => {
                        return new Date(b.updated_at) - new Date(a.updated_at);
                    });
                    setRooms(sortedRooms);
                }
            } catch (error) {
                console.error("Error fetching rooms:", error);
            }
        };
    
        fetchRooms();
    }, []); 

    const handleRoomClick = (roomId) => {
        navigate(`/c/${roomId}`);  // Navigating to the conversation room
    };

    return (
        <div className="container">
            <Sidebar /> 
            <div className="chatsBox">
                <h1>Initiated Chats</h1>

                {rooms ? (
                    rooms.length > 0 ? (
                        rooms.map((room) => (
                            <div
                                className="room"
                                key={room.room_id}
                                onClick={() => handleRoomClick(room.room_id)}
                            >
                                <p>{room.opposite_username} - {room.updated_at} - {room.last_message}</p> 
                            </div>
                        ))
                    ) : (
                        <p>You have not matched with anyone yet! Chats will appear here when you do.</p>
                    )
                ) : (
                    <p>Loading...</p>
                )}
            </div>
        </div>
    );
};

export default InitiatedChats;
