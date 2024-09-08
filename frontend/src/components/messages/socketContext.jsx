import React, { createContext, useContext, useEffect, useState } from 'react';
import io from 'socket.io-client';

const SocketContext = createContext();

export const SocketProvider = ({ children }) => {
    const [socket, setSocket] = useState(null);

    useEffect(() => {
        const access_token  = sessionStorage.getItem('access_token')
        const socketIo = io('http://localhost:5000', {
            extraHeaders: {
                Authorization: `Bearer ${access_token}`
        }
        }); 
        setSocket(socketIo);

        return () => socketIo.disconnect();
    }, []);

    return (
        <SocketContext.Provider value={socket}>
            {children}
        </SocketContext.Provider>
    );
};

export const useSocket = () => useContext(SocketContext);