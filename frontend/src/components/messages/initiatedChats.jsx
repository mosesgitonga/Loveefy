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
                    console.log(response.data);
                    setRooms(response.data);
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
            {/* <Sidebar /> */}
            <div className="chatsBox">
                <h1>Initiated Chats</h1>

                {rooms ? (
                    rooms.map((room) => (
                        <div
                            className="room"
                            key={room.room_id}
                            onClick={() => handleRoomClick(room.room_id)}
                        >
                            <p>{room.opposite_username}  </p> 
                        </div>
                    ))
                ) : (
                    <p>Loading...</p>
                )}
            </div>
        </div>
    );
};

export default InitiatedChats;
