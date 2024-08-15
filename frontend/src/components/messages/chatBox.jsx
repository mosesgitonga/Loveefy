import React from "react";

const ChatBox = () => {
    const [socket, setSocket] = useState(null);

    useEffect(() => {
        // Initialize the socket connection only once
        const newSocket = io.connect('http://localhost:5000', {
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

    const receiveMessage = () => {

    }
}