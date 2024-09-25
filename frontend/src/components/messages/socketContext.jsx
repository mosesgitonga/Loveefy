// import React, { createContext, useContext, useEffect, useState } from 'react';
// import io from 'socket.io-client';

// const SocketContext = createContext();

// export const SocketProvider = ({ children }) => {
//     const [socket, setSocket] = useState(null);

//     useEffect(() => {
//         const access_token  = sessionStorage.getItem('access_token')
//         if (!access_token) {
//             console.log('no access token')
//             return;
//         }
//         const socketIo = io('wss://www.loveefy.africa', {
//             extraHeaders: {
//                 Authorization: `Bearer ${access_token}`
//             },
//             transports: ['websocket'],
//         }); 

//         socketIo.on('connect_error', (error) => {
//             console.error('Connection Error:', error.message);
//         });
    
//         socketIo.on('connect', () => {
//             console.log('Socket connected');
//         });
    
//         socketIo.on('disconnect', () => {
//             console.log('Socket disconnected');
//         });

//         setSocket(socketIo);

//         return () => socketIo.disconnect();
//     }, []);

//     return (
//         <SocketContext.Provider value={socket}>
//             {children}
//         </SocketContext.Provider>
//     );
// };

// export const useSocket = () => useContext(SocketContext);