import React, { useEffect, useState } from "react";
import "./initiatedChats.css"
import api from "../api/axios";

const InitiatedChats = () => {
    const [rooms, setRooms] = useState(null);

    useEffect(() => {
        const fetchRooms = async () => {
            try {
                const response = await api.get('/api/v1/rooms');
                if (response.status === 200) {
                    console.log(response.data)
                    setRooms(response.data);
                }
            } catch (error) {
                console.error("Error fetching rooms:", error);
            }
        };

        fetchRooms();
    }, []);

    return (
        <div className="container">
            <div className="chatsBox">
                <h1>Initiated Chats</h1>

                {rooms ? (
                    rooms.map((room) => (
                        <div className="room" key={room.id}>
                            <p>{room.opposite_username}</p> 
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
